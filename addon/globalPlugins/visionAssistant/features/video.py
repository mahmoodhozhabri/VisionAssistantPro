# -*- coding: utf-8 -*-
import wx
import os
import json
import logging
import threading
import time
import subprocess
import tempfile
import re
import ctypes
import sys
from urllib.parse import urlparse
from collections import Counter

import addonHandler
import gui
import ui
import core
import api
import tones
import scriptHandler
import config as nvda_config

from .. import vision_config
from ..vision_config import ADDON_NAME
from ..prompt_utils import apply_prompt_template, get_prompt_text
from ..ai.core import AIHandler, is_ai_error, ai_error_message, is_server_busy_error
from ..utils.error_contract import is_key_exhausted_error, is_daily_quota_error
from ..ai.providers.gemini import GeminiHandler
from ..utils.media_capture import (
	_LocalVideoSource,
	_DownloadVideoSource,
	_YouTubeVideoSource,
	_InvalidVideoSource,
	ensure_ffmpeg,
)
from ..utils.storage import SeriesCharacterStore
from ..utils.system import (
	convert_json_to_srt_string,
	show_error_dialog,
	check_screen_curtain_active,
	get_focused_explorer_files,
	clean_json_fence,
)
from ..dialogs.media import VideoSourceDialog, VideoSRTProgressDialog

log = logging.getLogger(__name__)

addonHandler.initTranslation()


class VideoMixin:
	@scriptHandler.script(
		# Translators: Script description for 'Analyzes a local video file or an online video URL.' in Input Gestures dialog.
		description=_("Analyzes a local video file or an online video URL."),
		category=ADDON_NAME,
	)
	def script_analyzeOnlineVideo(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		if getattr(self, "_dialog_open", False):
			return

		focused_paths = get_focused_explorer_files()
		valid_exts = (
			".mp4",
			".avi",
			".mkv",
			".mov",
			".wmv",
			".flv",
			".webm",
			".mpg",
			".mpeg",
			".m4v",
			".3gp",
			".3g2",
			".ts",
			".mts",
			".m2ts",
			".vob",
			".asf",
			".divx",
			".ogv",
		)
		valid_paths = [p for p in focused_paths if p.lower().endswith(valid_exts)]

		target_path = None
		is_local = False

		if valid_paths:
			target_path = valid_paths[0]
			is_local = True
		else:
			try:
				clip_data = api.getClipData().strip()
				if clip_data.startswith(("http://", "https://", "www.")):
					domain = urlparse(clip_data).netloc.lower()
					if any(
						d in domain
						for d in [
							"youtube.com",
							"youtu.be",
							"instagram.com",
							"twitter.com",
							"x.com",
							"tiktok.com",
						]
					):
						target_path = clip_data
						is_local = False
			except Exception as e:
				log.warning(f"Clip data check failed: {e}")

		if target_path:
			if is_local:
				wx.CallLater(100, self._open_video_dialog, target_path)
			else:
				wx.CallLater(100, self._ask_video_action, target_path, is_local)
		else:
			wx.CallLater(100, self._open_video_dialog)

	def _prompt_youtube_duration(self, is_youtube, is_srt_mode):
		if not (is_youtube and is_srt_mode):
			return None, False
		gui.mainFrame.prePopup()
		msg = _(
			# Translators: Prompt asking the user to manually input YouTube video duration.
			"Please enter the YouTube video duration in minutes (e.g., 10 or 10.5).\nIf you enter an incorrect duration, the audio description may not be complete.",
		)
		# Translators: Title for the YouTube duration input dialog.
		title = _("YouTube Video Duration")
		d = wx.TextEntryDialog(gui.mainFrame, msg, title)
		d_res = d.ShowModal()
		val = d.GetValue().strip()

		d.Destroy()
		gui.mainFrame.postPopup()

		if d_res != wx.ID_OK:
			return None, True

		manual_duration_sec = None
		try:
			if ":" in val:
				parts = val.split(":")
				if len(parts) == 2:
					manual_duration_sec = float(parts[0]) * 60 + float(parts[1])
				elif len(parts) >= 3:
					manual_duration_sec = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
			else:
				manual_duration_sec = float(val) * 60
		except ValueError:
			# Translators: Error message shown when the entered YouTube duration is invalid.
			core.callLater(0, self.report_status, _("Invalid duration entered. Video analysis cancelled."))
			return None, True
		return manual_duration_sec, False

	def _ask_video_action(self, target_path, is_local):
		self._dialog_open = True
		choices = [
			# Translators: Option for general video analysis without timestamps.
			_("General Video Analysis"),
			# Translators: Option to generate an Audio Description SRT file.
			_("Generate Audio Description (SRT File)"),
		]

		gui.mainFrame.prePopup()
		# Translators: Prompt message asking the user to choose an action for the video.
		action_prompt = _("Choose action:")
		# Translators: Title of the video action selection dialog.
		dlg_title = _("Video Action")
		dlg = wx.SingleChoiceDialog(gui.mainFrame, action_prompt, dlg_title, choices)
		dlg.Raise()
		dlg.SetFocus()
		res = dlg.ShowModal()
		selection = dlg.GetSelection()

		dlg.Destroy()
		gui.mainFrame.postPopup()

		if res == wx.ID_OK:
			is_srt_mode = selection == 1
			is_youtube = not is_local and any(d in target_path.lower() for d in ["youtube.com", "youtu.be"])
			manual_duration_sec, cancelled = self._prompt_youtube_duration(is_youtube, is_srt_mode)
			if cancelled:
				self._dialog_open = False
				return

			series_name = self._guess_series_name(target_path) if (is_srt_mode and is_local) else ""

			prog_dlg = None
			if is_srt_mode:

				def run_generation(dialog_instance):
					if is_local:
						threading.Thread(
							target=self._thread_local_video,
							args=(
								target_path,
								True,
								dialog_instance,
								getattr(dialog_instance, "series_name", None),
							),
							daemon=True,
						).start()
					else:
						threading.Thread(
							target=self._thread_video,
							args=(
								target_path,
								True,
								dialog_instance,
								manual_duration_sec,
								getattr(dialog_instance, "series_name", None),
							),
							daemon=True,
						).start()

				def run_retry(dialog_instance):
					rs = getattr(dialog_instance, "retry_state", None)
					if not rs:
						return
					if is_local:
						threading.Thread(
							target=self._thread_local_video,
							args=(
								target_path,
								True,
								dialog_instance,
								getattr(dialog_instance, "series_name", None),
								rs,
							),
							daemon=True,
						).start()
					else:
						threading.Thread(
							target=self._thread_video,
							args=(
								target_path,
								True,
								dialog_instance,
								manual_duration_sec,
								getattr(dialog_instance, "series_name", None),
								rs,
							),
							daemon=True,
						).start()

				prog_dlg = VideoSRTProgressDialog(
					gui.mainFrame,
					regenerate_cb=run_generation,
					original_path=target_path if is_local else None,
					series_name=series_name,
				)
				prog_dlg.retry_cb = run_retry
				prog_dlg.Show()

			if is_local:
				threading.Thread(
					target=self._thread_local_video,
					args=(target_path, is_srt_mode, prog_dlg, series_name),
					daemon=True,
				).start()
			else:
				threading.Thread(
					target=self._thread_video,
					args=(target_path, is_srt_mode, prog_dlg, manual_duration_sec, series_name),
					daemon=True,
				).start()

			self._dialog_open = False
		else:
			self._dialog_open = False

	def _open_video_dialog(self, initial_path=""):
		self._dialog_open = True
		if not AIHandler.is_gemini():
			self._dialog_open = False
			# Translators: Error message when video analysis is attempted with a non-Gemini provider.
			core.callLater(0, self.report_status, _("Video analysis is only supported by Gemini providers."))
			return

		gui.mainFrame.prePopup()
		dlg = VideoSourceDialog(
			gui.mainFrame,
			guess_series=self._guess_series_name,
			initial_path=initial_path,
		)
		dlg.Raise()
		res = dlg.ShowModal()

		is_srt_mode = False
		chars_as_sub = True
		add_disclaimer = True
		input_val = ""
		series_name = ""

		if res == wx.ID_OK:
			is_srt_mode = dlg.action_choice.GetSelection() == 1
			if is_srt_mode:
				chars_as_sub = dlg.chars_as_sub_check.Value
				add_disclaimer = dlg.disclaimer_check.Value
				series_name = dlg.selected_series()
			input_val = dlg.url_input.GetValue().strip()
			auto_series = dlg.is_auto_series()

		dlg.Destroy()
		gui.mainFrame.postPopup()

		if res != wx.ID_OK or not input_val:
			self._dialog_open = False
			return

		is_local_file = False
		try:
			if os.path.exists(input_val) and os.path.isfile(input_val):
				is_local_file = True
		except Exception as e:
			log.warning(f"Local file check failed: {e}")

		if is_srt_mode:
			nvda_config.conf["VisionAssistant"]["video_chars_as_subtitle"] = chars_as_sub
			nvda_config.conf["VisionAssistant"]["video_add_disclaimer"] = add_disclaimer
			if not series_name and is_local_file and auto_series:
				series_name = self._guess_series_name(input_val)

		is_youtube = not is_local_file and any(d in input_val.lower() for d in ["youtube.com", "youtu.be"])
		manual_duration_sec, cancelled = self._prompt_youtube_duration(is_youtube, is_srt_mode)
		if cancelled:
			self._dialog_open = False
			return

		prog_dlg = None
		if is_srt_mode:

			def run_generation(dialog_instance):
				if is_local_file:
					threading.Thread(
						target=self._thread_local_video,
						args=(
							input_val,
							True,
							dialog_instance,
							getattr(dialog_instance, "series_name", None),
						),
						daemon=True,
					).start()
				else:
					threading.Thread(
						target=self._thread_video,
						args=(
							input_val,
							True,
							dialog_instance,
							manual_duration_sec,
							getattr(dialog_instance, "series_name", None),
						),
						daemon=True,
					).start()

			def run_retry(dialog_instance):
				rs = getattr(dialog_instance, "retry_state", None)
				if not rs:
					return
				if is_local_file:
					threading.Thread(
						target=self._thread_local_video,
						args=(
							input_val,
							True,
							dialog_instance,
							getattr(dialog_instance, "series_name", None),
							rs,
						),
						daemon=True,
					).start()
				else:
					threading.Thread(
						target=self._thread_video,
						args=(
							input_val,
							True,
							dialog_instance,
							manual_duration_sec,
							getattr(dialog_instance, "series_name", None),
							rs,
						),
						daemon=True,
					).start()

			prog_dlg = VideoSRTProgressDialog(
				gui.mainFrame,
				regenerate_cb=run_generation,
				original_path=input_val if is_local_file else None,
				series_name=series_name,
			)
			prog_dlg.retry_cb = run_retry
			prog_dlg.Show()

		if is_local_file:
			threading.Thread(
				target=self._thread_local_video,
				args=(input_val, is_srt_mode, prog_dlg, series_name),
				daemon=True,
			).start()
		else:
			threading.Thread(
				target=self._thread_video,
				args=(input_val, is_srt_mode, prog_dlg, manual_duration_sec, series_name),
				daemon=True,
			).start()

		self._dialog_open = False

	def _is_segment_complete(self, json_str, start_sec, end_sec, total_duration):
		try:
			expected_end = end_sec if end_sec != -1 else total_duration
			if not expected_end:
				return True

			chunk_length = expected_end - start_sec
			if chunk_length <= 0:
				return True

			clean_json = clean_json_fence(json_str)

			descriptions = None
			try:
				data = json.loads(clean_json)
				if isinstance(data, list):
					descriptions = data
				elif isinstance(data, dict):
					descriptions = data.get("descriptions", data.get("descriptions_list", []))
			except Exception:
				pass

			max_generated_sec = 0
			ts_counter = Counter()

			if descriptions and isinstance(descriptions, list):
				if len(descriptions) < 2:
					return False
				for desc in descriptions:
					if not isinstance(desc, dict):
						continue
					ts_str = desc.get("end") or desc.get("start")
					if ts_str:
						ts_counter[ts_str] += 1
						t_sec = self.parse_sec(ts_str)
						if t_sec > max_generated_sec:
							max_generated_sec = t_sec
			else:
				matches = re.findall(r'"end"\s*:\s*"([^"]+)"', clean_json)
				if not matches or len(matches) < 2:
					return False
				for ts_str in matches:
					ts_counter[ts_str] += 1
					t_sec = self.parse_sec(ts_str)
					if t_sec > max_generated_sec:
						max_generated_sec = t_sec

			if any(count >= 5 for count in ts_counter.values()):
				log.warning("Segment rejected due to AI looping on the same timestamp.")
				return False

			target_to_reach = (
				chunk_length if (start_sec > 0 and max_generated_sec < start_sec) else expected_end
			)
			tolerance = max(60, chunk_length * 0.15)

			if max_generated_sec >= (target_to_reach - tolerance):
				return True
			return False
		except Exception as e:
			log.warning(f"Segment validation error: {e}")
			return False

	def _guess_series_name(self, path):
		if not path or path.startswith(("http://", "https://", "www.")):
			return ""
		try:
			base = os.path.splitext(os.path.basename(path))[0]
		except Exception:
			return ""
		cleaned = re.sub(
			r"(?i)\s*(?:S\d+E\d+|S\d+|E\d+|\d+x\d+|Season\s+\d+\s*(?:Episode\s+\d+)?|Episode\s+\d+|Part\s+\d+).*$",
			"",
			base,
		)
		return re.sub(r"[_.\- ]+$", "", cleaned).strip()

	def _thread_local_video(
		self,
		path,
		is_srt_mode=False,
		prog_dlg=None,
		series_name=None,
		resume_state=None,
	):
		self._run_video_analysis(
			_LocalVideoSource(path),
			is_srt_mode=is_srt_mode,
			prog_dlg=prog_dlg,
			series_name=series_name,
			resume_state=resume_state,
		)

	def _thread_video(
		self,
		url,
		is_srt_mode=False,
		prog_dlg=None,
		manual_duration_sec=None,
		series_name=None,
		resume_state=None,
	):
		source = self._build_online_video_source(url)
		self._run_video_analysis(
			source,
			is_srt_mode=is_srt_mode,
			prog_dlg=prog_dlg,
			manual_duration_sec=manual_duration_sec,
			series_name=series_name,
			resume_state=resume_state,
		)

	def _build_online_video_source(self, url):
		parsed_url = urlparse(url)
		domain = parsed_url.netloc.lower()
		if not domain:
			# Translators: Error message when the provided video URL is not valid.
			return _InvalidVideoSource(_("Error: Invalid URL."))

		if any(d in domain for d in ["youtube.com", "youtu.be"]):
			return _YouTubeVideoSource(url)
		if "instagram.com" in domain:
			return _DownloadVideoSource(url, "instagram")
		if any(d in domain for d in ["twitter.com", "x.com"]):
			return _DownloadVideoSource(url, "twitter")
		if "tiktok.com" in domain:
			return _DownloadVideoSource(url, "tiktok")

		return _InvalidVideoSource(
			# Translators: Error message when the video URL is from an unsupported website.
			_("Error: Unsupported platform. Only YouTube, Instagram, Twitter, and TikTok are supported."),
		)

	def parse_sec(self, val):
		if isinstance(val, (int, float)):
			return float(val)
		if isinstance(val, str):
			val = val.strip()
			if ":" in val:
				val = val.replace(".", ",").split(",", 1)[0].strip()
				parts = val.split(":")
				try:
					if len(parts) == 2:
						return float(parts[0]) * 60 + float(parts[1])
					if len(parts) >= 3:
						return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
				except Exception as e:
					log.debug(f"Timestamp HH:MM:SS parse failed for {val!r}: {e}")
			try:
				return float(val)
			except Exception as e:
				log.debug(f"Timestamp float parse failed for {val!r}: {e}")
		return 0.0

	def _scan_chunk_described_names(self, seg_res, chars):
		found = set()
		try:
			clean_res = clean_json_fence(seg_res)
			parsed = json.loads(clean_res)
			descs = (
				parsed
				if isinstance(parsed, list)
				else parsed.get("descriptions", parsed.get("descriptions_list", []))
			)
		except Exception:
			return found
		if not isinstance(descs, list):
			return found
		names = [c for c in chars if isinstance(c, dict) and c.get("name")]
		for d in descs:
			if not isinstance(d, dict):
				continue
			label = (d.get("label") or d.get("text") or "").strip()
			if not label:
				continue
			label_key = SeriesCharacterStore.character_key(label)
			if not label_key:
				continue
			for c in names:
				n = c.get("name").strip()
				key = SeriesCharacterStore.character_key(n)
				if len(key) >= 3 and (label_key == key or key in label_key.split()):
					found.add(n)
		return found

	def _run_video_analysis(
		self,
		source,
		is_srt_mode=False,
		prog_dlg=None,
		manual_duration_sec=None,
		series_name=None,
		resume_state=None,
	):
		log.info(
			f"Video analysis started: srt={is_srt_mode}, source={getattr(source, 'log_label', source.__class__.__name__)}",
		)
		intervals = []
		master_data_list = []
		final_res_string = ""
		global_character_context = ""
		full_srt_character_context = ""
		resume_seg_idx = 0
		if resume_state:
			resume_seg_idx = resume_state.get("seg_idx", 0)
			intervals = list(resume_state.get("intervals", []))
			master_data_list = list(resume_state.get("master_data_list", []))
			full_srt_character_context = resume_state.get("full_srt_character_context", "")
			global_character_context = resume_state.get("global_character_context", "")
		srt_disclaimer = _(
			# Translators: Disclaimer added at the beginning of AI-generated SRT files.
			"Disclaimer: This audio description was generated by AI. Some details, including character identities or events, may not be entirely accurate.",
		)

		def abort_check():
			if prog_dlg is not None:
				try:
					return prog_dlg.abort
				except Exception:
					return True
			return False

		def fmt_time_short(sec):
			s = int(sec)
			m, s = s // 60, s % 60
			h, m = m // 60, m % 60
			if h > 0:
				return f"{h:02d}:{m:02d}:{s:02d}"
			return f"{m:02d}:{s:02d}"

		def char_ranges(c_obj):
			if not isinstance(c_obj, dict):
				return None
			out = []
			ranges = c_obj.get("appearance_ranges") or c_obj.get("appearanceRanges")
			if isinstance(ranges, list):
				for r in ranges:
					if isinstance(r, (list, tuple)) and len(r) >= 2:
						s, e = self.parse_sec(r[0]), self.parse_sec(r[1])
					elif isinstance(r, dict):
						s, e = self.parse_sec(r.get("start", 0)), self.parse_sec(r.get("end", 0))
					else:
						continue
					if s < 0 or e <= 0 or e < s:
						continue
					out.append((s, e))
			if out:
				return out
			first_s = self.parse_sec(c_obj.get("first_appeared_sec", 0))
			last_s = self.parse_sec(c_obj.get("last_appeared_sec", 999999))
			if last_s <= 0:
				last_s = 999999
			return [(first_s, last_s)]

		def char_first_last(c_obj):
			ranges = char_ranges(c_obj)
			if not ranges:
				return (0, 999999)
			return (min(s for s, e in ranges), max(e for s, e in ranges))

		def is_char_in_segment(c_obj, seg_start, seg_end):
			if seg_end == -1:
				return True
			ranges = char_ranges(c_obj)
			if not ranges:
				return True
			return any((s <= seg_end) and (e >= seg_start) for s, e in ranges)

		def report(msg, speak=True):
			if abort_check():
				return
			display_text = msg
			if is_srt_mode and master_data_list:
				combined_header = ""
				if nvda_config.conf["VisionAssistant"].get("video_add_disclaimer", True):
					combined_header = srt_disclaimer
				if full_srt_character_context and nvda_config.conf["VisionAssistant"].get(
					"video_chars_as_subtitle",
					True,
				):
					combined_header = (
						combined_header + "\n\n" if combined_header else ""
					) + full_srt_character_context

				partial_srt = convert_json_to_srt_string(
					master_data_list,
					segments=intervals[: len(master_data_list)],
					global_chars=combined_header,
				)
				if partial_srt:
					display_text = msg + "\n\n" + partial_srt
			elif not is_srt_mode and final_res_string:
				display_text = msg + "\n\n" + final_res_string.strip()

			if prog_dlg is not None:
				try:
					wx.CallAfter(prog_dlg.txt_status.SetValue, display_text)
				except Exception as e:
					log.debug(f"Progress dialog update failed: {e}")
				if speak:
					self.report_status(msg)
			else:
				if speak:
					self.report_status(msg)

		try:
			lang = vision_config.get_lang_name("ai_response_language")
			recover_char_extract = False
			if resume_state:
				recover_char_extract = resume_state.get("recover_char_extract", False)
				file_uri = resume_state.get("file_uri")
				current_key = resume_state.get("current_key")
				local_path = resume_state.get("local_path")
				duration_sec = resume_state.get("duration_sec")
				chars = resume_state.get("chars", [])
				prev_descriptions = resume_state.get("prev_descriptions", "")
				if "intervals" in resume_state:
					intervals[:] = resume_state["intervals"]
				if "source" in resume_state:
					source = resume_state["source"]
			else:
				if not source.prepare(report, abort_check):
					# Translators: Error message shown when uploading a video file fails.
					if not prog_dlg:
						self.current_status = _("Idle")
					return

				file_uri = getattr(prog_dlg, "file_uri", None) if prog_dlg else None
				current_key = getattr(prog_dlg, "current_key", None) if prog_dlg else None
				local_path = getattr(prog_dlg, "local_path", None) if prog_dlg else None
				duration_sec = None

				uri_from_cache = False
				if source.is_direct:
					file_uri = source.direct_uri
					duration_sec = manual_duration_sec or source.duration(file_uri)
				else:
					if not file_uri:
						keys = GeminiHandler._get_api_keys(task="video")
						source_path = getattr(source, "path", None)
						if keys and source_path and os.path.isfile(source_path):
							cached_uri, cached_dur = GeminiHandler._get_cached_video_uri(source_path, keys[0])
							if cached_uri:
								file_uri = cached_uri
								duration_sec = cached_dur
								uri_from_cache = True
					if not file_uri:
						if not local_path or not os.path.exists(local_path):
							local_path = source.ensure_local(self, report, abort_check)
							if abort_check():
								return
							if not local_path:
								if not prog_dlg:
									self.current_status = _("Idle")
								return
							if prog_dlg:
								prog_dlg.local_path = local_path

						file_uri, duration_sec, current_key = GeminiHandler.upload_and_get_duration(
							local_path,
							report_callback=report,
							abort_checker=abort_check,
							cache_path=getattr(source, "path", None),
						)
						if not file_uri:
							upload_err = GeminiHandler._last_upload_error or ""
							# Translators: Status message when uploading the video to the AI service fails. {error} holds the service-provided message.
							report(_("Video upload failed: {error}").format(error=upload_err))
							if not prog_dlg:
								self.current_status = _("Idle")
							return
						if prog_dlg:
							prog_dlg.file_uri = file_uri
							prog_dlg.current_key = current_key
					else:
						duration_sec = manual_duration_sec or duration_sec or source.duration(file_uri)

				intervals.clear()
				chunk_minutes = nvda_config.conf["VisionAssistant"].get("video_srt_chunk_minutes", 10)
				chunk_size_sec = chunk_minutes * 60

				if is_srt_mode and chunk_size_sec > 0 and duration_sec and duration_sec > chunk_size_sec:
					start = 0
					while start < duration_sec:
						end = min(start + chunk_size_sec, duration_sec)
						intervals.append((start, end))
						start = end
				else:
					intervals.append((0, duration_sec if duration_sec else -1))

				chars = []

			if (not resume_state or recover_char_extract) and is_srt_mode:
				# Translators: Status message when the AI is analyzing the whole video to extract character names and appearances.
				report(_("Extracting characters (First pass)..."))
				char_template = get_prompt_text("video_character_extraction")
				char_prompt = apply_prompt_template(char_template, [("response_lang", lang)])

				user_chars = []
				if series_name:
					user_chars = SeriesCharacterStore(vision_config.SERIES_FILE).get_series(series_name)
				user_pairs = []
				for c in user_chars:
					if isinstance(c, dict) and c.get("name"):
						n = c["name"].strip()
						if n:
							notes = (c.get("notes") or "").strip()
							user_edited = bool(c.get("user_edited"))
							user_pairs.append((n, notes, user_edited))
				user_names = [n for n, _, _ in user_pairs]
				if user_names:
					lines = []
					for n, notes, user_edited in user_pairs:
						line = "- " + (n + ": " + notes if notes else n)
						if user_edited:
							line = "- [USER-CONFIRMED] " + (n + ": " + notes if notes else n)
						lines.append(line)
					known_template = get_prompt_text("video_character_known_names")
					known_block = apply_prompt_template(known_template, [("known_names", "\n".join(lines))])
					char_prompt = char_prompt + "\n\n" + known_block

				log.debug(f"Character extraction PROMPT (first 2000 chars):\n{char_prompt[:2000]}")
				char_res, file_uri, current_key = GeminiHandler.process_video_task(
					local_path,
					char_prompt,
					None,
					None,
					True,
					report,
					abort_check,
					file_uri,
					current_key,
					source.is_direct,
					cache_path=getattr(source, "path", None),
				)
				log.debug(f"Character extraction RAW response:\n{char_res}")
				if prog_dlg:
					prog_dlg.file_uri = file_uri
					prog_dlg.current_key = current_key

				if not char_res or is_ai_error(char_res):
					char_err = (
						ai_error_message(char_res)
						if char_res and is_ai_error(char_res)
						# Translators: Error message shown when the AI fails to extract character information from the video.
						else _("Character extraction failed.")
					)
					if prog_dlg and is_server_busy_error(char_err):
						prog_dlg.retry_state = {
							"recover_char_extract": True,
							"file_uri": file_uri,
							"current_key": current_key,
							"local_path": local_path,
							"duration_sec": duration_sec,
							"source": source,
							"chars": [],
							"full_srt_character_context": "",
							"intervals": list(intervals),
							"master_data_list": [],
						}
						wx.CallAfter(prog_dlg.show_try_again, char_err)
						return
					if uri_from_cache and (
						is_key_exhausted_error(char_err) or is_daily_quota_error(char_err)
					):
						log.warning(
							f"Cache file_uri rejected by API ({char_err[:80]}), clearing cache and retrying with fresh upload",
						)
						source_path = getattr(source, "path", None)
						if source_path:
							GeminiHandler._clear_cached_video_uri(source_path)
						file_uri = None
						current_key = None
						uri_from_cache = False
						if not local_path or not os.path.exists(local_path):
							local_path = source.ensure_local(self, report, abort_check)
							if abort_check():
								return
							if not local_path:
								if not prog_dlg:
									self.current_status = _("Idle")
								return
							if prog_dlg:
								prog_dlg.local_path = local_path
						file_uri, duration_sec, current_key = GeminiHandler.upload_and_get_duration(
							local_path,
							report_callback=report,
							abort_checker=abort_check,
							cache_path=getattr(source, "path", None),
						)
						if not file_uri:
							upload_err = GeminiHandler._last_upload_error or ""
							# Translators: Status message when re-uploading the video after clearing its cache fails. {error} holds the service-provided message.
							upload_failed_msg = _("Video upload failed after cache retry: {error}").format(
								error=upload_err
							)
							report(upload_failed_msg)
							if not prog_dlg:
								self.current_status = _("Idle")
							return
						if prog_dlg:
							prog_dlg.file_uri = file_uri
							prog_dlg.current_key = current_key
						log.debug(
							"Retrying character extraction with fresh upload.",
						)
						char_res, file_uri, current_key = GeminiHandler.process_video_task(
							local_path,
							char_prompt,
							None,
							None,
							True,
							report,
							abort_check,
							file_uri,
							current_key,
							source.is_direct,
							cache_path=getattr(source, "path", None),
						)
						if prog_dlg:
							prog_dlg.file_uri = file_uri
							prog_dlg.current_key = current_key
						if not char_res or is_ai_error(char_res):
							char_err2 = (
								ai_error_message(char_res)
								if char_res and is_ai_error(char_res)
								else _("Character extraction failed.")
							)
							log.error(
								f"Video analysis failed permanently even after fresh upload: {char_err2}",
							)
							if not prog_dlg:
								self.current_status = _("Idle")
							return
					else:
						log.error(f"Video analysis failed permanently: {char_err}")
						if not prog_dlg:
							self.current_status = _("Idle")
						return

				if char_res and not is_ai_error(char_res):
					try:
						clean_json = clean_json_fence(char_res)
						try:
							char_data = json.loads(clean_json)
							if isinstance(char_data, list):
								chars = char_data
							elif "characters" in char_data:
								chars = char_data["characters"]
							else:
								for v in char_data.values():
									if isinstance(v, list):
										chars = v
										break
						except Exception as e:
							log.debug(f"Character extraction JSON parse failed: {e}")

						if not chars:
							names = re.findall(r'"name"\s*:\s*"([^"]+)"', clean_json, re.IGNORECASE)
							descs = re.findall(r'"description"\s*:\s*"([^"]+)"', clean_json, re.IGNORECASE)
							for i in range(min(len(names), len(descs))):
								chars.append(
									{
										"name": names[i],
										"description": descs[i],
										"first_appeared_sec": 0,
										"last_appeared_sec": 999999,
									},
								)

						if user_names and chars:
							user_lookup = {SeriesCharacterStore.character_key(n): n for n in user_names}
							for c in chars:
								if isinstance(c, dict) and c.get("name"):
									key = SeriesCharacterStore.character_key(c["name"])
									if key in user_lookup:
										c["name"] = user_lookup[key]
							matched = {
								SeriesCharacterStore.character_key(c.get("name", ""))
								for c in chars
								if isinstance(c, dict)
							}
							unmatched = [
								n for n in user_names if SeriesCharacterStore.character_key(n) not in matched
							]
							if unmatched:
								log.info(
									f"Series dictionary: {len(user_names) - len(unmatched)} of {len(user_names)} names matched; unmatched: {', '.join(unmatched)}",
								)

						if series_name and chars:
							store = SeriesCharacterStore(vision_config.SERIES_FILE)
							if store.merge_auto_characters(series_name, chars):
								learned_count = len(store.get_series(series_name))
								log.info(
									f"Series dictionary (auto-learned): {series_name} now has {learned_count} characters",
								)

						if chars:
							full_ctx_lines = []
							for c in chars:
								if isinstance(c, dict):
									n = c.get("name") or c.get("Name") or "Unknown"
									d = c.get("description") or c.get("Description") or ""
									first_s, last_s = char_first_last(c)

									time_tag = ""
									if 0 < first_s < 999999 and 0 < last_s < 999999:
										time_tag = f" [{fmt_time_short(first_s)}-{fmt_time_short(last_s)}]"
									elif 0 < first_s < 999999:
										time_tag = f" [{fmt_time_short(first_s)}]"

									full_ctx_lines.append(f"- {n}{time_tag}: {d}")
								elif isinstance(c, str):
									full_ctx_lines.append(f"- {c}")

							if full_ctx_lines:
								# Translators: Header for the list of extracted characters in the generated subtitle.
								dict_title = _("GLOBAL CHARACTER DICTIONARY:") + "\n"
								full_srt_character_context = dict_title + "\n".join(full_ctx_lines)
					except Exception as e:
						log.warning(f"Failed to parse character extraction JSON: {e}")

			if not resume_state:
				master_data_list.clear()
				prev_descriptions = ""
			described_names = set()
			for chunk_res in master_data_list:
				described_names |= self._scan_chunk_described_names(chunk_res, chars)
			segment_success = True
			final_res_string = ""

			for seg_idx in range(resume_seg_idx, len(intervals)):
				start_sec, end_sec = intervals[seg_idx]
				if abort_check():
					return

				needs_cooldown = (seg_idx > 0) or (seg_idx == 0 and is_srt_mode)
				if needs_cooldown:
					cooldown_seconds = 30 if (seg_idx == 0 and is_srt_mode) else 20
					# Translators: Status message shown when the add-on pauses briefly between API requests to prevent hitting server rate limits. {seconds} is the number of seconds.
					cooldown_msg = _("Cooling down to prevent rate limits ({seconds} seconds)...").format(
						seconds=cooldown_seconds,
					)
					report(cooldown_msg)
					for step in range(cooldown_seconds * 2):
						if abort_check():
							return
						time.sleep(0.5)

				video_template = get_prompt_text(
					"video_audio_description" if is_srt_mode else "video_analysis",
				)

				h_start, m_start, s_start = (
					int(start_sec // 3600),
					int((start_sec % 3600) // 60),
					int(start_sec % 60),
				)
				h_end, m_end, s_end = (
					int(end_sec // 3600),
					int((end_sec % 3600) // 60),
					int(end_sec % 60) if end_sec != -1 else (0, 0, 0),
				)

				start_str = f"{h_start:02d}:{m_start:02d}:{s_start:02d}"
				end_str = f"{h_end:02d}:{m_end:02d}:{s_end:02d}" if end_sec != -1 else "end"

				segment_template = get_prompt_text("video_segment_instruction")
				end_text = f"{end_str} ({int(end_sec)} seconds)" if end_sec != -1 else "the end of the video"
				segment_instruction = apply_prompt_template(
					segment_template,
					[("start_str", f"{start_str} ({int(start_sec)} seconds)"), ("end_str", end_text)],
				)

				p = apply_prompt_template(video_template, [("response_lang", lang)])

				visible_lines = []
				already_desc_names = []
				must_desc_names = []
				for c in chars:
					if isinstance(c, dict):
						if is_char_in_segment(c, start_sec, end_sec):
							n = c.get("name") or c.get("Name") or "Unknown"
							d = c.get("description") or c.get("Description") or ""
							visible_lines.append(f"- {n}: {d}")
							first_s, last_s = char_first_last(c)
							has_ranges = bool(c.get("appearance_ranges") or c.get("appearanceRanges"))
							if n in described_names or (has_ranges and first_s < start_sec):
								already_desc_names.append(n)
							elif has_ranges and start_sec <= first_s <= end_sec:
								must_desc_names.append(n)
					elif isinstance(c, str):
						visible_lines.append(f"- {c}")

				if visible_lines:
					# Translators: Header for the list of characters introduced up to the current video scene.
					dict_title = _("GLOBAL CHARACTER DICTIONARY (Active characters in this scene):") + "\n"
					global_character_context = dict_title + "\n".join(visible_lines)
				else:
					global_character_context = ""

				if global_character_context:
					p = f"{global_character_context}\n\n{p}"
				if already_desc_names or must_desc_names:
					already_template = get_prompt_text("video_already_described")
					if already_template:
						already_str = apply_prompt_template(
							already_template,
							[
								("already_names", ", ".join(already_desc_names)),
								("first_names", ", ".join(must_desc_names)),
							],
						)
						p = f"{already_str}\n\n{p}"
				if prev_descriptions:
					prev_context_template = get_prompt_text("video_previous_context")
					if prev_context_template:
						prev_context_str = apply_prompt_template(
							prev_context_template,
							[("prev_descriptions", prev_descriptions)],
						)
						p = f"{p}\n\n{prev_context_str}"

				prompt_with_segment = f"{segment_instruction}\n\n{p}" if len(intervals) > 1 else p

				if len(intervals) > 1:
					# Translators: Status message reporting which segment of the video is currently being analyzed. {current} is the current segment number and {total} is the total segment count.
					seg_msg = _("Analyzing video segment {current} of {total}...").format(
						current=seg_idx + 1,
						total=len(intervals),
					)
					report(seg_msg)
				else:
					report(_("Analyzing video..."))

				validator = (
					(lambda r: self._is_segment_complete(r, start_sec, end_sec, duration_sec))
					if (is_srt_mode and len(intervals) > 1)
					else None
				)

				seg_res, file_uri, current_key = GeminiHandler.process_video_task(
					local_path,
					prompt_with_segment,
					start_sec,
					end_sec,
					is_srt_mode,
					report,
					abort_check,
					file_uri,
					current_key,
					source.is_direct,
					validator=validator,
					cache_path=getattr(source, "path", None),
				)
				if prog_dlg:
					prog_dlg.file_uri = file_uri
					prog_dlg.current_key = current_key

				log.debug(f"Segment {seg_idx + 1} of {len(intervals)} RAW response:\n{seg_res}")

				if not seg_res or is_ai_error(seg_res):
					# Translators: Error message reported when video segment analysis fails after multiple retries due to network issues.
					conn_failed_msg = _("Connection failed after retries.")
					report_err = (
						ai_error_message(seg_res) if seg_res and is_ai_error(seg_res) else conn_failed_msg
					)
					if prog_dlg and is_server_busy_error(report_err):
						prog_dlg.retry_state = {
							"seg_idx": seg_idx,
							"intervals": list(intervals),
							"master_data_list": list(master_data_list),
							"full_srt_character_context": full_srt_character_context,
							"global_character_context": global_character_context,
							"file_uri": file_uri,
							"current_key": current_key,
							"local_path": local_path,
							"duration_sec": duration_sec,
							"chars": chars,
							"prev_descriptions": prev_descriptions,
						}
						wx.CallAfter(prog_dlg.show_try_again, report_err)
						return
					segment_success = False
					break

				if is_srt_mode:
					master_data_list.append(seg_res)
					described_names |= self._scan_chunk_described_names(seg_res, chars)
					prev_descriptions = ""
					try:
						clean_res = clean_json_fence(seg_res)
						parsed = json.loads(clean_res)
						descs = (
							parsed
							if isinstance(parsed, list)
							else parsed.get("descriptions", parsed.get("descriptions_list", []))
						)
						if descs:
							cutoff_sec = max(0, end_sec - 120)
							recent = []
							for d in descs:
								try:
									t = d.get("end", d.get("start", ""))
									t = t.split(",")[0].split(".")[0]
									parts = t.split(":")
									if len(parts) >= 3:
										ds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
										if ds >= cutoff_sec:
											label = d.get("label", d.get("text", "")).strip()
											s = d.get("start", "")
											if label:
												recent.append(f"[{s}] {label}")
								except Exception as e:
									log.debug(f"Description timestamp parse skipped: {e}")
									continue
							if recent:
								prev_descriptions = "\n".join(recent[-10:])
					except Exception as e:
						log.warning(f"Failed to build previous descriptions for segment continuity: {e}")
				else:
					if len(intervals) > 1:
						final_res_string += (
							f"\n\n--- [Part {seg_idx + 1}: {start_str} - {end_str}] ---\n" + seg_res
						)
					else:
						final_res_string = seg_res

				if seg_idx + 1 < len(intervals):
					# Translators: Status message shown when a video segment finishes processing and the system is moving to the next one. {current} is the completed segment number.
					report(_("Segment {current} finished. Preparing next...").format(current=seg_idx + 1))
				else:
					# Translators: Status message when all segments are done and it is finalizing.
					report(_("Finalizing..."))

			if abort_check():
				return

			if segment_success:
				if is_srt_mode:
					combined_header = ""
					if nvda_config.conf["VisionAssistant"].get("video_add_disclaimer", True):
						combined_header = srt_disclaimer

					if full_srt_character_context and nvda_config.conf["VisionAssistant"].get(
						"video_chars_as_subtitle",
						True,
					):
						combined_header = (
							combined_header + "\n\n" if combined_header else ""
						) + full_srt_character_context

					srt_content = convert_json_to_srt_string(
						master_data_list,
						segments=intervals,
						global_chars=combined_header,
					)
					if srt_content:
						wx.CallAfter(prog_dlg.on_finished, srt_content)
					else:
						# Translators: Error message shown when the AI output cannot be converted into a valid SRT subtitle file.
						wx.CallAfter(prog_dlg.on_error, _("Failed to parse AI output into SRT."))

					wx.CallAfter(setattr, self, "current_status", _("Idle"))
				else:
					attachments = [{"mime_type": "video/mp4", "file_uri": file_uri}] if file_uri else []

					wx.CallAfter(
						self._open_doc_chat_dialog,
						final_res_string.strip(),
						attachments,
						final_res_string.strip(),
						final_res_string.strip(),
					)
					wx.CallAfter(setattr, self, "current_status", _("Idle"))
			else:
				# Translators: Error message reported when video segment analysis fails after multiple retries due to network issues.
				conn_failed_msg = _("Connection failed after retries.")
				report_err = (
					ai_error_message(seg_res) if seg_res and is_ai_error(seg_res) else conn_failed_msg
				)
				log.error(f"Video analysis failed permanently: {report_err}")
				if prog_dlg:
					wx.CallAfter(prog_dlg.on_error, report_err)
				else:
					wx.CallAfter(show_error_dialog, report_err)

				wx.CallAfter(setattr, self, "current_status", _("Idle"))

		except Exception as e:
			log.error(f"{source.log_label}: {e}", exc_info=True)
			report(source.error_message)
		finally:
			source.cleanup()
			wx.CallAfter(setattr, self, "current_status", _("Idle"))

	@scriptHandler.script(
		description=_("Starts or stops local video recording of the screen."),
		category=ADDON_NAME,
	)
	def script_recordLocalVideo(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		if not self.is_video_recording:
			threading.Thread(target=self._start_local_video_recording, daemon=True).start()
		else:
			threading.Thread(target=self._stop_and_analyze_recording, daemon=True).start()

	def _start_local_video_recording(self, force_desktop=False):
		if not AIHandler.is_gemini():
			# Translators: Error message when video recording is attempted with a non-Gemini provider
			core.callLater(0, self.report_status, _("Video recording is only supported by Gemini providers."))
			return
		if check_screen_curtain_active():
			return
		ffmpeg_path = ensure_ffmpeg()
		if not ffmpeg_path:
			return

		try:
			fd, temp_path = tempfile.mkstemp(suffix=".mp4", prefix="vision_assistant_rec_")
			os.close(fd)
			self.recording_output_path = temp_path

			if not force_desktop:
				# Translators: Status message reported when starting video recording
				core.callLater(0, self.report_status, _("Starting recording..."))

			crop_filter = ""
			if not force_desktop:
				try:
					fg_obj = api.getForegroundObject()
					if fg_obj and fg_obj.location:
						x, y, w, h = fg_obj.location
						screen_w, screen_h = (
							ctypes.windll.user32.GetSystemMetrics(0),
							ctypes.windll.user32.GetSystemMetrics(1),
						)
						if x < 0:
							w += x
							x = 0
						if y < 0:
							h += y
							y = 0
						if x + w > screen_w:
							w = screen_w - x
						if y + h > screen_h:
							h = screen_h - y
						if w > 100 and h > 100:
							w = w if w % 2 == 0 else w - 1
							h = h if h % 2 == 0 else h - 1
							crop_filter = f"crop={w}:{h}:{x}:{y},"
				except Exception as e:
					log.warning(f"Failed to calculate window dimensions: {e}")

			cmd = [ffmpeg_path, "-f", "gdigrab", "-framerate", "15", "-i", "desktop"]
			cmd.extend(
				[
					"-vf",
					f"{crop_filter}scale=854:-2,format=yuv420p",
					"-c:v",
					"libx264",
					"-preset",
					"ultrafast",
					"-crf",
					"28",
					"-y",
					temp_path,
				],
			)

			startupinfo = None
			creationflags = 0
			if sys.platform == "win32":
				startupinfo = subprocess.STARTUPINFO()
				startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
				startupinfo.wShowWindow = subprocess.SW_HIDE
				creationflags = 0x08000000

			self.recording_process = subprocess.Popen(
				cmd,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				stdin=subprocess.PIPE,
				startupinfo=startupinfo,
				creationflags=creationflags,
			)
			self.is_video_recording = True
			self.recording_start_time = time.time()

			def check_process_status():
				if self.is_video_recording and self.recording_process:
					if self.recording_process.poll() is not None:
						self.recording_process = None
						self.is_video_recording = False
						if not force_desktop:
							log.warning("ffmpeg crashed on window capture. Retrying full screen.")
							# Translators: Message when window capture fails and switches to full screen capture
							core.callLater(0, ui.message, _("Window capture failed. Trying full screen..."))
							threading.Thread(
								target=self._start_local_video_recording,
								args=(True,),
								daemon=True,
							).start()
						else:
							# Translators: Error message when ffmpeg fails completely
							err_msg = _("Recording failed to start. FFmpeg encountered a fatal error.")
							wx.CallAfter(
								show_error_dialog,
								err_msg,
							)

			wx.CallAfter(wx.CallLater, 2000, check_process_status)

			if not force_desktop:
				# Translators: Message when video recording starts
				msg = _("Recording started. Press the same shortcut again to stop.")

				def announce_start():
					if self.is_video_recording:
						tones.beep(800, 100)
						self.report_status(msg)

				wx.CallAfter(wx.CallLater, 2500, announce_start)

		except Exception as e:
			log.error(f"Failed to start recording: {e}", exc_info=True)
			self.is_video_recording = False
			self.recording_process = None
			# Translators: Error message when recording fails to start
			wx.CallAfter(show_error_dialog, _("Failed to start recording: {error}").format(error=str(e)))

	def _stop_and_analyze_recording(self):
		if not self.is_video_recording or not self.recording_process:
			return
		try:
			self.is_video_recording = False
			try:
				self.recording_process.communicate(input=b"q", timeout=5)
			except Exception:
				try:
					self.recording_process.terminate()
				except Exception as e:
					log.debug(f"Recording process terminate failed: {e}")
			time.sleep(0.5)
			duration = time.time() - self.recording_start_time if self.recording_start_time else 0
			tones.beep(400, 100)

			if not os.path.exists(self.recording_output_path):
				# Translators: Error when recorded video file is not found
				wx.CallAfter(show_error_dialog, _("Recording file not found."))
				return

			file_size = os.path.getsize(self.recording_output_path)
			size_mb = file_size / (1024 * 1024)

			if file_size < 1024:
				wx.CallAfter(
					show_error_dialog,
					_(
						# Translators: Error when recorded video file is too small/corrupted
						"The recording was too short or the video file is corrupted. Please try recording for at least a few seconds.",
					),
				)
				return

			# Translators: Status message showing recording info, {duration} is seconds, {size} is MB
			stopped_msg = _("Recording stopped ({duration:.0f} seconds, {size:.1f} MB)").format(
				duration=duration,
				size=size_mb,
			)
			core.callLater(
				0,
				ui.message,
				stopped_msg,
			)

			def report(msg):
				self.current_status = msg
				core.callLater(0, ui.message, msg)

			file_uri, _dur, current_key = GeminiHandler.upload_and_get_duration(
				self.recording_output_path,
				report_callback=report,
			)
			if not file_uri:
				self.current_status = _("Idle")
				return

			lang = vision_config.get_lang_name("ai_response_language")
			video_template = get_prompt_text("local_video_recording")
			prompt = apply_prompt_template(video_template, [("response_lang", lang)])

			# Translators: Message reported when AI is analyzing the video
			report(_("Analyzing video..."))

			res, file_uri, current_key = GeminiHandler.process_video_task(
				self.recording_output_path,
				prompt,
				None,
				None,
				False,
				report,
				None,
				file_uri,
				current_key,
				False,
			)

			if res:
				if is_ai_error(res):
					wx.CallAfter(show_error_dialog, ai_error_message(res))
				else:
					wx.CallAfter(
						self._open_doc_chat_dialog,
						res,
						[{"mime_type": "video/mp4", "file_uri": file_uri}],
						res,
						res,
					)

		except Exception as e:
			log.error(f"Failed to process recording: {e}", exc_info=True)
			# Translators: Error message when processing recorded video fails
			wx.CallAfter(show_error_dialog, _("Failed to process recording: {error}").format(error=str(e)))
		finally:
			wx.CallAfter(setattr, self, "current_status", _("Idle"))
			self.recording_process = None
			if self.recording_output_path and os.path.exists(self.recording_output_path):
				try:
					os.remove(self.recording_output_path)
				except Exception as e:
					log.debug(f"Recording temp file removal failed: {e}")
			self.recording_output_path = None
			self.recording_start_time = None
