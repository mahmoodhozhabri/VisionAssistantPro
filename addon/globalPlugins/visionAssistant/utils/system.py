# -*- coding: utf-8 -*-
import sys
import os
import json
import logging
import re
import tempfile
import ctypes
import html.parser
import wx
import winUser
import api
import globalVars
import config as nvda_config

from .error_contract import is_ai_error

try:
	import comtypes.client
except ImportError:
	pass

log = logging.getLogger(__name__)


def long_path(path):
	if os.name != "nt":
		return path
	absolute = os.path.abspath(path)
	if absolute.startswith("\\\\?\\"):
		return absolute
	return "\\\\?\\" + absolute


def is_gemini_provider(strict=False):
	import sys

	cfg = sys.modules.get("config") or nvda_config
	conf = cfg.conf["VisionAssistant"]
	provider = conf.get("active_provider", "gemini")
	if provider == "gemini":
		return True
	if strict:
		return False
	return provider == "custom" and conf.get("custom_api_type", "openai") == "gemini"


try:
	import fitz
except ImportError:
	fitz = None

try:
	import markdown as markdown_lib
except ImportError:
	markdown_lib = None

from .. import vision_config
from .storage import JsonStore

_ocr_progress_store = JsonStore(vision_config.OCR_PROGRESS_FILE)


class OCRProgressStore:
	@staticmethod
	def save(key, record):
		_ocr_progress_store.set(key, record)

	@staticmethod
	def load(key):
		return _ocr_progress_store.get(key)

	@staticmethod
	def clear(key):
		_ocr_progress_store.delete(key)


def _current_ocr_engine():
	try:
		cfg = sys.modules.get("config") or nvda_config

		return str(cfg.conf["VisionAssistant"].get("ocr_engine", "chrome"))
	except Exception:
		return "chrome"


def is_pdf_compression_supported():
	try:
		cfg = sys.modules.get("config") or nvda_config

		engine = str(cfg.conf["VisionAssistant"].get("ocr_engine", "chrome"))
		if engine != "gemini":
			return False
		p = str(cfg.conf["VisionAssistant"].get("active_provider", "gemini"))
		if p == "mistral" or p == "gemini":
			return True
		if p == "custom":
			custom_type = str(cfg.conf["VisionAssistant"].get("custom_api_type", "openai"))
			upload_supp = bool(cfg.conf["VisionAssistant"].get("custom_upload_support", False))
			return custom_type == "gemini" or upload_supp
		return False
	except Exception:
		return False


def ocr_cache_key(context, paths):
	key = context + "|" + "|".join(sorted(paths))
	if context in ("document", "smartfile"):
		key += "|engine=" + _current_ocr_engine()
	return key


def _is_failed_ocr_page(text):
	if not text:
		return True
	stripped = text.strip()
	return stripped.startswith("[") or is_ai_error(stripped)


TEXT_EXTENSIONS = (".txt", ".html", ".htm")


def _decode_text_file(raw):
	if raw.startswith(b"\xef\xbb\xbf"):
		return raw.decode("utf-8-sig")
	if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
		return raw.decode("utf-16")
	for enc in ("utf-8", "cp1256", "windows-1252", "latin-1"):
		try:
			return raw.decode(enc)
		except (UnicodeDecodeError, LookupError):
			continue
	return raw.decode("utf-8", errors="replace")


_TXT_PAGE_MARKER = re.compile(r"^---\s*Page\s+(\d+)\s*---\s*$", re.IGNORECASE)
_BLOCK_TAGS = {
	"p",
	"div",
	"table",
	"tr",
	"td",
	"th",
	"li",
	"ul",
	"ol",
	"pre",
	"blockquote",
	"h1",
	"h2",
	"h3",
	"h4",
	"h5",
	"h6",
	"br",
	"hr",
	"section",
	"article",
}


def _split_txt_pages(text):
	lines = text.splitlines()
	marker_idx = [i for i, ln in enumerate(lines) if _TXT_PAGE_MARKER.match(ln)]
	if not marker_idx:
		return None
	pages = []
	for k, start in enumerate(marker_idx):
		end = marker_idx[k + 1] if k + 1 < len(marker_idx) else len(lines)
		pages.append("\n".join(lines[start + 1 : end]).strip())
	return pages


def _group_paragraphs(text, target_chars=2500):
	text = text.strip()
	if not text:
		return []
	paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
	pages = []
	cur = []
	cur_len = 0
	for p in paras:
		if len(p) > target_chars:
			if cur:
				pages.append("\n\n".join(cur))
				cur, cur_len = [], 0
			lines = p.splitlines() or [p]
			part = []
			part_len = 0
			for ln in lines:
				while len(ln) > target_chars:
					if part:
						pages.append("\n".join(part))
						part, part_len = [], 0
					pages.append(ln[:target_chars])
					ln = ln[target_chars:]
				if part and part_len + len(ln) > target_chars:
					pages.append("\n".join(part))
					part, part_len = [], 0
				part.append(ln)
				part_len += len(ln)
			if part:
				pages.append("\n".join(part))
			continue
		if cur and cur_len + len(p) > target_chars:
			pages.append("\n\n".join(cur))
			cur, cur_len = [], 0
		cur.append(p)
		cur_len += len(p)
	if cur:
		pages.append("\n\n".join(cur))
	return pages


def _html_to_plain_text(text):
	out = []
	skip = [0]

	class _Parser(html.parser.HTMLParser):
		def handle_starttag(self, tag, attrs):
			tag = tag.lower()
			if tag in ("script", "style"):
				skip[0] += 1
			elif not skip[0] and tag in _BLOCK_TAGS:
				out.append("\n")

		def handle_endtag(self, tag):
			tag = tag.lower()
			if tag in ("script", "style"):
				if skip[0]:
					skip[0] -= 1
			elif not skip[0] and tag in _BLOCK_TAGS:
				out.append("\n")

		def handle_data(self, data):
			if not skip[0]:
				out.append(data)

	parser = _Parser(convert_charrefs=True)
	try:
		parser.feed(text)
		parser.close()
	except Exception:
		pass
	text = "".join(out).replace("\r\n", "\n").replace("\r", "\n")
	return re.sub(r"\n{3,}", "\n\n", text).strip()


def _is_page_label(txt):
	t = (txt or "").strip()
	if not t or len(t) > 25:
		return False
	if not re.search(r"\d", t):
		return False
	word = re.sub(r"[\d\s\.:،,؛\-–—]+", "", t)
	return len(word) <= 12


class _PageHTMLParser(html.parser.HTMLParser):
	def __init__(self):
		super().__init__(convert_charrefs=True)
		self.pages = []
		self._cur = []
		self._cur_started = False
		self._div_depth = 0
		self._skip_depth = 0
		self._in_h2 = False
		self._h2_parts = []

	def handle_starttag(self, tag, attrs):
		tag = tag.lower()
		if tag in ("script", "style"):
			self._skip_depth += 1
			return
		if tag == "div":
			if self._div_depth == 0 and dict(attrs).get("dir", "").lower() == "auto":
				if self._cur_started:
					self._flush()
				self._cur_started = True
			self._div_depth += 1
			self._block_newline(tag)
			return
		if self._skip_depth:
			return
		if tag == "h2":
			self._in_h2 = True
			self._h2_parts = []
			return
		self._block_newline(tag)

	def handle_startendtag(self, tag, attrs):
		self._block_newline(tag.lower())

	def handle_endtag(self, tag):
		tag = tag.lower()
		if tag in ("script", "style"):
			if self._skip_depth:
				self._skip_depth -= 1
			return
		if self._skip_depth:
			return
		if tag == "div":
			if self._div_depth > 0:
				self._div_depth -= 1
			self._block_newline(tag)
			return
		if tag == "h2":
			if self._in_h2:
				txt = "".join(self._h2_parts).strip()
				if not _is_page_label(txt):
					self._cur.append(txt)
				self._in_h2 = False
			self._block_newline(tag)
			return
		self._block_newline(tag)

	def handle_data(self, data):
		if self._skip_depth:
			return
		if self._in_h2:
			self._h2_parts.append(data)
			return
		if data.strip():
			self._cur_started = True
		self._cur.append(data)

	def _block_newline(self, tag):
		if tag in _BLOCK_TAGS:
			self._cur.append("\n")

	def _flush(self):
		text = "".join(self._cur).replace("\r\n", "\n").replace("\r", "\n")
		text = re.sub(r"[ \t]+\n", "\n", text)
		text = re.sub(r"\n{3,}", "\n\n", text)
		self.pages.append(text.strip())
		self._cur = []
		self._cur_started = False

	def close(self):
		super().close()
		if self._cur_started:
			self._flush()


def _read_text_pages(path):
	try:
		with open(path, "rb") as f:
			raw = f.read()
	except Exception as e:
		log.error(f"Error reading text file {path}: {e}", exc_info=True)
		return None
	text = _decode_text_file(raw)
	ext = os.path.splitext(path)[1].lower()
	if ext in (".html", ".htm"):
		if "<div" in text.lower() and 'dir="auto"' in text.lower():
			parser = _PageHTMLParser()
			try:
				parser.feed(text)
				parser.close()
			except Exception as e:
				log.warning(f"HTML page parsing failed for {path}: {e}")
			if parser.pages:
				return parser.pages
		text = _html_to_plain_text(text)
	pages = _split_txt_pages(text)
	if pages:
		return pages
	return _group_paragraphs(text)


def get_focused_explorer_files():
	paths = []
	is_desktop = False
	hwnds = set()

	try:
		for obj_getter in (api.getFocusObject, api.getForegroundObject):
			try:
				obj = obj_getter()
				if obj and getattr(obj, "windowHandle", 0):
					h = obj.windowHandle
					hwnds.add(h)
					try:
						hwnds.add(winUser.getAncestor(h, winUser.GA_ROOT))
					except Exception:
						pass
			except Exception:
				pass

		if not hwnds:
			return []

		for h in hwnds:
			try:
				cls = winUser.getClassName(h)
				if cls in ("Progman", "WorkerW", "SysListView32", "SHELLDLL_DefView"):
					is_desktop = True
					break
			except Exception:
				pass

		shell = None
		windows = None
		try:
			shell = comtypes.client.CreateObject("Shell.Application")
			windows = shell.Windows()
			for win in windows:
				doc = None
				selected = None
				try:
					win_hwnd = getattr(win, "HWND", None)
					if not win_hwnd:
						continue

					is_target = win_hwnd in hwnds
					if not is_target and is_desktop:
						try:
							win_cls = winUser.getClassName(win_hwnd)
							if win_cls in ("Progman", "WorkerW"):
								is_target = True
						except Exception:
							pass

					if is_target:
						doc = win.Document
						if doc:
							selected = doc.SelectedItems()
							if selected and selected.Count > 0:
								for i in range(selected.Count):
									try:
										item = selected.Item(i)
										p = getattr(item, "Path", "")
										if not p and hasattr(item, "Target"):
											try:
												p = item.Target.Path
											except Exception:
												pass
										if p:
											paths.append(p)
										del item
									except Exception:
										continue
								if paths:
									break
				except Exception:
					continue
				finally:
					if selected:
						del selected
					if doc:
						del doc
		except Exception:
			pass
		finally:
			if windows:
				del windows
			if shell:
				del shell

	except Exception:
		pass

	return paths


def _optimize_pdf_images(doc, max_dimension=1600, quality=75):
	if not fitz or not doc:
		return
	processed_xrefs = set()
	for page in doc:
		try:
			images = page.get_images()
		except Exception as e:
			log.debug(f"Could not get images from page: {e}")
			continue
		for img_info in images:
			xref = img_info[0]
			if xref in processed_xrefs:
				continue
			processed_xrefs.add(xref)
			try:
				base = doc.extract_image(xref)
				if not base:
					continue
				w = base.get("width", 0)
				h = base.get("height", 0)
				raw_len = len(base.get("image", b""))
				if w > max_dimension or h > max_dimension or raw_len > 80_000:
					pix = fitz.Pixmap(doc, xref)
					if pix.alpha or pix.n >= 4:
						pix = fitz.Pixmap(fitz.csRGB, pix)
					max_d = max(pix.w, pix.h)
					if max_d > max_dimension:
						scale = max_dimension / max_d
						target_w = max(1, int(pix.w * scale))
						target_h = max(1, int(pix.h * scale))
						scaled_pix = fitz.Pixmap(pix, target_w, target_h, False)
					else:
						scaled_pix = pix
					jpg_data = scaled_pix.tobytes("jpg", jpg_quality=quality)
					if len(jpg_data) < raw_len:
						page.replace_image(xref, stream=jpg_data)
			except Exception as e:
				log.debug(f"Image compression skipped for xref {xref}: {e}")


class VirtualDocument:
	def __init__(self, file_paths):
		self.file_paths = file_paths
		self.page_map = []
		self.total_pages = 0
		self.text_pages = {}
		self.is_single_pdf = len(file_paths) == 1 and file_paths[0].lower().endswith(".pdf")
		self.single_pdf_path = file_paths[0] if self.is_single_pdf else None

	def scan(self):
		for path in self.file_paths:
			ext = os.path.splitext(path)[1].lower()
			if ext in TEXT_EXTENSIONS:
				pages = _read_text_pages(path)
				if pages:
					self.text_pages[path] = pages
					for k in range(len(pages)):
						self.page_map.append((path, k))
					continue
			if not fitz:
				continue
			try:
				doc = fitz.open(path)
				count = len(doc)
				for i in range(count):
					self.page_map.append((path, i))
				doc.close()
			except Exception as e:
				log.error(f"Error scanning file {path}: {e}", exc_info=True)
		self.total_pages = len(self.page_map)

	def get_page_info(self, global_page_index):
		if 0 <= global_page_index < self.total_pages:
			return self.page_map[global_page_index]
		return None, None

	def create_merged_pdf(self, start_page, end_page, compress=False):
		if not fitz:
			return None
		try:
			out_doc = fitz.open()
			for i in range(start_page, end_page + 1):
				f_path, f_idx = self.get_page_info(i)
				src_doc = fitz.open(f_path)
				if src_doc.is_pdf:
					out_doc.insert_pdf(src_doc, from_page=f_idx, to_page=f_idx)
				else:
					pdf_bytes = src_doc.convert_to_pdf(from_page=f_idx, to_page=f_idx)
					img_pdf = fitz.open("pdf", pdf_bytes)
					out_doc.insert_pdf(img_pdf)
					img_pdf.close()
				src_doc.close()

			if compress:
				_optimize_pdf_images(out_doc)

			fd, temp_path = tempfile.mkstemp(suffix=".pdf")
			os.close(fd)
			if compress:
				out_doc.save(
					temp_path,
					garbage=4,
					clean=True,
					deflate=True,
					deflate_images=True,
					deflate_fonts=True,
					use_objstms=1,
				)
			else:
				out_doc.save(temp_path)
			out_doc.close()
			return temp_path
		except Exception as e:
			log.error(f"Error merging PDF: {e}", exc_info=True)
			return None


def apply_model_filter(combo_box, query):
	cb = combo_box
	query_low = query.lower()

	if not hasattr(cb, "_all_models_backup") and cb.GetCount() > 0:
		cb._all_models_backup = [(cb.GetString(i), cb.GetClientData(i)) for i in range(cb.GetCount())]

	backup = getattr(cb, "_all_models_backup", [])

	if not query_low:
		if cb.GetCount() != len(backup):
			cb.Freeze()
			cb.Clear()
			for name, data in backup:
				cb.Append(name, data)
			cb.SetValue("")
			cb.Thaw()
		return

	filtered = [(name, data) for name, data in backup if query_low in name.lower()]

	cb.Freeze()
	cb.Clear()
	for name, data in filtered:
		cb.Append(name, data)

	cb.ChangeValue(query)
	cb.SetInsertionPointEnd()
	cb.Thaw()

	return filtered


def clean_markdown(text):
	if not text:
		return ""
	text = re.sub(r"\*\*|__|[*_]", "", text)
	text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
	text = re.sub(r"```", "", text)
	text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
	text = re.sub(r"^\s*-\s+", "", text, flags=re.MULTILINE)
	return text.strip()


def strip_thinking_tags(text):
	if not text:
		return ""
	text = re.sub(r"\s*<think>.*?</think>\s*", "\n\n", text, flags=re.DOTALL | re.IGNORECASE)
	text = re.sub(r"\s*<reasoning>.*?</reasoning>\s*", "\n\n", text, flags=re.DOTALL | re.IGNORECASE)
	text = re.sub(r"\s*<thought>.*?</thought>\s*", "\n\n", text, flags=re.DOTALL | re.IGNORECASE)
	return text.strip()


def markdown_to_html(text, full_page=False):
	if not text:
		return ""

	html_body = ""
	use_regex_fallback = False

	if markdown_lib:
		try:
			html_body = markdown_lib.markdown(text, extensions=["tables", "fenced_code"])
		except Exception as e:
			log.warning(f"Markdown library failed: {e}")
			use_regex_fallback = True
	else:
		use_regex_fallback = True

	if use_regex_fallback:
		html = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
		html = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", html)
		html = re.sub(r"__(.*?)__", r"<b>\1</b>", html)
		html = re.sub(r"^### (.*)", r"<h3>\1</h3>", html, flags=re.M)
		html = re.sub(r"^## (.*)", r"<h2>\1</h2>", html, flags=re.M)
		html = re.sub(r"^# (.*)", r"<h1>\1</h1>", html, flags=re.M)

		lines = html.split("\n")
		in_table = False
		new_lines = []
		table_style = 'border="1" style="border-collapse: collapse; width: 100%; margin-bottom: 10px;"'
		td_style = 'style="padding: 5px; border: 1px solid #ccc;"'

		for line in lines:
			stripped = line.strip()
			if stripped.startswith("|") or (stripped.count("|") > 1 and len(stripped) > 5):
				if not in_table:
					new_lines.append(f"<table {table_style}>")
					in_table = True
				if "---" in stripped:
					continue
				row_content = stripped.strip("|").split("|")
				cells = "".join([f"<td {td_style}>{c.strip()}</td>" for c in row_content])
				new_lines.append(f"<tr>{cells}</tr>")
			else:
				if in_table:
					new_lines.append("</table>")
					in_table = False
				if stripped:
					new_lines.append(line + "<br>")
				else:
					new_lines.append("<br>")
		if in_table:
			new_lines.append("</table>")
		html_body = "".join(new_lines)

	if not full_page:
		return html_body
	return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{{font-family:"Segoe UI",Arial,sans-serif;line-height:1.6;padding:20px;color:#333;max-width:800px;margin:0 auto}}h1,h2,h3{{color:#2c3e50;border-bottom:1px solid #eee;padding-bottom:5px}}pre{{background-color:#f4f4f4;padding:10px;border-radius:5px;overflow-x:auto;font-family:Consolas,monospace}}code{{background-color:#f4f4f4;padding:2px 5px;border-radius:3px;font-family:Consolas,monospace}}table{{border-collapse:collapse;width:100%;margin-bottom:10px}}td,th{{border:1px solid #ccc;padding:8px;text-align:left}}strong,b{{color:#000;font-weight:bold}}li{{margin-bottom:5px}}</style></head><body>{html_body}</body></html>"""


def convert_json_to_srt_string(json_text, chunk_size=1200, segments=None, global_chars=None):
	def parse_seconds(ts):
		ts_str = str(ts).strip()
		total_seconds = 0.0
		if re.match(r"^\d+(?:[.,]\d+)?$", ts_str):
			try:
				total_seconds = float(ts_str.replace(",", "."))
			except Exception:
				pass
		else:
			ts_clean = ts_str.replace(".", ",")
			main_time = ts_clean.split(",", 1)[0]
			parts = main_time.split(":")
			try:
				if len(parts) == 2:
					total_seconds = float(int(parts[0]) * 60 + int(parts[1]))
				elif len(parts) == 3:
					total_seconds = float(int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2]))
			except Exception:
				pass
		return total_seconds

	def format_srt_time(total_seconds):
		if total_seconds < 0:
			total_seconds = 0.0
		h = int(total_seconds // 3600)
		m = int((total_seconds % 3600) // 60)
		s = int(total_seconds % 60)
		ms = int(round((total_seconds - int(total_seconds)) * 1000))
		return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

	def normalize_timestamp(ts, seg_window=None):
		total_seconds = parse_seconds(ts)
		if seg_window is not None:
			seg_start, seg_end = seg_window
			if total_seconds < seg_start:
				if total_seconds < (seg_end - seg_start + 10):
					total_seconds += seg_start
				else:
					total_seconds = seg_start
			if total_seconds > seg_end and seg_end > 0:
				total_seconds = seg_end
		return format_srt_time(total_seconds)

	if isinstance(json_text, list):
		chunks = json_text
	else:
		chunks = [json_text]

	srt_content = ""
	counter = 1
	is_first_subtitle = True

	for chunk_idx, raw_chunk in enumerate(chunks):
		seg_window = None
		if segments and chunk_idx < len(segments):
			sw = segments[chunk_idx]
			if sw and sw[1] is not None and sw[1] > sw[0] >= 0:
				seg_window = sw
		clean_text = raw_chunk.strip()

		clean_text = clean_json_fence(clean_text)

		try:
			data = json.loads(clean_text)
			descriptions = []
			if isinstance(data, list):
				descriptions = data
			elif isinstance(data, dict):
				descriptions = data.get("descriptions", data.get("descriptions_list", []))

			for desc in descriptions:
				start_val = desc.get("start")
				end_val = desc.get("end")
				text = desc.get("label", desc.get("text", "")).strip()

				if not text:
					continue

				start = normalize_timestamp(start_val, seg_window)
				end = normalize_timestamp(end_val, seg_window)

				if start == "00:00:00,000" and end == "00:00:00,000":
					continue

				if is_first_subtitle and global_chars:
					text = f"{global_chars.strip()}\n{text}"
					is_first_subtitle = False

				srt_content += f"{counter}\n{start} --> {end}\n{text}\n\n"
				counter += 1

		except Exception:
			blocks = re.findall(r'\{[^{}]*?"start"\s*:[^{}]*?\}', clean_text, re.DOTALL | re.IGNORECASE)
			if blocks:
				for block in blocks:
					start_m = re.search(r'"start"\s*:\s*"([^"]+)"', block, re.IGNORECASE)
					end_m = re.search(r'"end"\s*:\s*"([^"]+)"', block, re.IGNORECASE)

					label_m = re.search(
						r'"(?:label|text)"\s*:\s*"(.*?)"\s*(?:,|})',
						block,
						re.IGNORECASE | re.DOTALL,
					)

					if start_m and end_m and label_m:
						start_val = start_m.group(1)
						end_val = end_m.group(1)
						text = label_m.group(1).strip().replace('\\"', '"')

						start = normalize_timestamp(start_val, seg_window)
						end = normalize_timestamp(end_val, seg_window)

						if start == "00:00:00,000" and end == "00:00:00,000":
							continue

						if is_first_subtitle and global_chars:
							text = f"{global_chars.strip()}\n{text}"
							is_first_subtitle = False

						srt_content += f"{counter}\n{start} --> {end}\n{text}\n\n"
						counter += 1
			else:
				pattern = r"\[(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.*)"
				matches = re.finditer(pattern, clean_text)
				for match in matches:
					start_time = normalize_timestamp(match.group(1), seg_window)
					end_time = normalize_timestamp(match.group(2), seg_window)
					desc_text = match.group(3).strip()

					if desc_text:
						if is_first_subtitle and global_chars:
							desc_text = f"{global_chars.strip()}\n\n{desc_text}"
							is_first_subtitle = False
						srt_content += f"{counter}\n{start_time} --> {end_time}\n{desc_text}\n\n"
						counter += 1

	if srt_content:
		return srt_content

	fallback_text = clean_json_fence(chunks[0])
	if not fallback_text or len(fallback_text) < 10 or "{" in fallback_text or '"start"' in fallback_text:
		log.warning("SRT fallback rejected: output does not look like parsed descriptions.")
		return ""

	if global_chars:
		fallback_text = f"{global_chars.strip()}\n\n{fallback_text}"

	return f"1\n00:00:00,000 --> 00:00:05,000\n{fallback_text.strip()}\n\n"


def clean_json_fence(text):
	if not text:
		return text
	t = text.strip()
	for fence_kw in ("```json", "```srt", "```"):
		needle = fence_kw
		idx = t.lower().find(needle)
		if idx == -1:
			idx = t.find(fence_kw)
		if idx != -1:
			t = t[idx + len(fence_kw) :]
			end = t.find("```")
			if end != -1:
				t = t[:end]
			return t.strip()
	return text.strip()


def get_mime_type(path):
	ext = os.path.splitext(path)[1].lower().strip()
	if ext == ".pdf":
		return "application/pdf"
	if ext in [".jpg", ".jpeg"]:
		return "image/jpeg"
	if ext == ".png":
		return "image/png"
	if ext == ".webp":
		return "image/webp"
	if ext in [".tif", ".tiff"]:
		return "image/jpeg"
	if ext in [".heic", ".heif"]:
		return "image/heic"
	if ext == ".mp3":
		return "audio/mpeg"
	if ext == ".wav":
		return "audio/wav"
	if ext == ".ogg":
		return "audio/ogg"
	if ext == ".mp4":
		return "video/mp4"
	import mimetypes

	guessed, _ = mimetypes.guess_type(path)
	if guessed:
		return guessed

	try:
		with open(path, "rb") as f:
			header = f.read(12)
			if header.startswith(b"%PDF"):
				return "application/pdf"
			if header.startswith(b"\xff\xd8"):
				return "image/jpeg"
			if header.startswith(b"\x89PNG"):
				return "image/png"
			if header.startswith(b"RIFF") and b"WEBP" in header:
				return "image/webp"
	except Exception:
		pass

	text_exts = [".txt", ".csv", ".md", ".py", ".js", ".html", ".css", ".json", ".xml", ".log"]
	if ext in text_exts:
		return "text/plain"

	return "application/octet-stream"


def show_error_dialog(message):
	import gui

	def run_dialog():
		gui.mainFrame.prePopup()
		title = f"{vision_config.ADDON_NAME} Error"
		gui.messageBox(message, title, wx.OK | wx.ICON_ERROR)
		gui.mainFrame.postPopup()

	wx.CallAfter(run_dialog)


def check_screen_curtain_active(quiet=False):
	try:
		if bool(ctypes.windll.nvdaHelperLocal.isScreenFullyBlack()):
			if not quiet:
				# Translators: Error message shown when trying to take a screenshot while NVDA's Screen Curtain is enabled.
				msg = "The Screen Curtain is currently enabled. Please disable it (NVDA+Control+Escape) before using visual recognition features."
				show_error_dialog(msg)
			return True
	except Exception:
		pass
	return False


def desktop_protection_reason():
	try:
		if globalVars.appArgs.secure:
			return "secure"
	except Exception as e:
		log.debug(f"Secure mode check failed: {e}")
	try:
		from utils.security import isRunningOnSecureDesktop

		if isRunningOnSecureDesktop():
			return "secure_desktop"
	except Exception as e:
		log.debug(f"Secure desktop check failed: {e}")
	try:
		from winAPI.sessionTracking import isLockScreenModeActive

		if isLockScreenModeActive():
			return "lock"
	except Exception as e:
		log.debug(f"Lock screen check failed: {e}")
	if check_screen_curtain_active(quiet=True):
		return "curtain"
	return ""


def get_file_path(title, wildcard, mode="open", multiple=False, default_name="", default_dir=""):
	import gui

	style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST if mode == "open" else wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
	if multiple:
		style |= wx.FD_MULTIPLE
	gui.mainFrame.prePopup()
	try:
		with wx.FileDialog(
			gui.mainFrame,
			title,
			wildcard=wildcard,
			style=style,
			defaultDir=default_dir,
			defaultFile=default_name,
		) as dlg:
			if dlg.ShowModal() == wx.ID_OK:
				return dlg.GetPaths() if multiple else dlg.GetPath()
	finally:
		gui.mainFrame.postPopup()
	return None


def _generate_object_signature(obj):
	role_type = int(getattr(obj, "role", 0))
	unique_signature = ""

	try:
		if hasattr(obj, "UIAElement") and obj.UIAElement.currentAutomationId:
			unique_signature = f"uia_{obj.UIAElement.currentAutomationId}"
	except Exception:
		pass

	if not unique_signature:
		try:
			win_ctrl_id = getattr(obj, "windowControlID", None)
			class_name = getattr(obj, "windowClassName", None)
			if win_ctrl_id and class_name:
				unique_signature = f"win_{class_name}_{win_ctrl_id}"
		except Exception:
			pass

	if not unique_signature:
		loc = getattr(obj, "location", None)
		if loc:
			try:
				handle = getattr(obj, "windowHandle", None)
				if handle:
					rect = winUser.getWindowRect(handle)
					w_left, w_top = rect.left, rect.top
				else:
					w_left, w_top = 0, 0
			except Exception:
				w_left, w_top = 0, 0
			rel_x = loc.left - w_left
			rel_y = loc.top - w_top
			unique_signature = f"coords_{rel_x},{rel_y}"

	if not unique_signature:
		return None

	try:
		raw_name = obj._get_name() if hasattr(obj, "_get_name") else getattr(obj, "name", "")
	except Exception:
		raw_name = getattr(obj, "name", "")
	raw_name = raw_name or ""

	return f"sig_{role_type}_{unique_signature}_{raw_name}"
