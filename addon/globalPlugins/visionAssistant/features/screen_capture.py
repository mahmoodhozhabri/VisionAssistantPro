# -*- coding: utf-8 -*-
import wx
import io
import base64
import ctypes
import logging
import tempfile
import os
import subprocess
import shutil
import threading
import time
import winreg

import api
import textInfos
import NVDAObjects.behaviors
import core

import addonHandler

log = logging.getLogger(__name__)
addonHandler.initTranslation()


class ScreenCaptureMixin:
	def _getClipboardImageFile(self):
		path = None
		if not wx.TheClipboard.Open():
			return None
		try:
			if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_BITMAP)):
				bmp_data = wx.BitmapDataObject()
				if wx.TheClipboard.GetData(bmp_data):
					bmp = bmp_data.GetBitmap()
					if bmp.IsOk():
						fd, path = tempfile.mkstemp(suffix=".png")
						os.close(fd)
						if not bmp.SaveFile(path, wx.BITMAP_TYPE_PNG):
							try:
								os.remove(path)
							except Exception as e:
								log.debug(f"Screenshot temp file removal failed: {e}")
							path = None
		except Exception as e:
			log.error(f"Clipboard image extraction failed: {e}")
			path = None
		finally:
			wx.TheClipboard.Close()
		return path

	def _capture_navigator(self):
		try:
			obj = api.getNavigatorObject()
			if not obj or not obj.location:
				return None, 0, 0, ""
			x, y, w, h = obj.location
			if w < 1 or h < 1:
				return None, 0, 0, ""
			bmp = wx.Bitmap(w, h)
			wx.MemoryDC(bmp).Blit(0, 0, w, h, wx.ScreenDC(), x, y)
			s = io.BytesIO()
			img = bmp.ConvertToImage()
			img.SetOption("quality", 90)
			img.SaveFile(s, wx.BITMAP_TYPE_JPEG)
			m = "image/jpeg"
			return base64.b64encode(s.getvalue()).decode("utf-8"), w, h, m
		except Exception as e:
			log.error(f"Screen capture failed: {e}")
			return None, 0, 0, ""

	def _capture_fullscreen(self, quality=90, max_width=None):
		try:
			hwnd = ctypes.windll.user32.GetForegroundWindow()
			dpi = 96
			if hwnd:
				try:
					dpi = int(ctypes.windll.user32.GetDpiForWindow(hwnd))
				except Exception:
					dpi = 96
			if dpi <= 0:
				dpi = 96
			scale = dpi / 96.0

			w_logical, h_logical = wx.GetDisplaySize()
			w_physical = int(round(w_logical * scale))
			h_physical = int(round(h_logical * scale))

			bmp = wx.Bitmap(w_physical, h_physical)
			screen = wx.ScreenDC()
			memory = wx.MemoryDC()
			memory.SelectObject(bmp)
			try:
				memory.Blit(0, 0, w_physical, h_physical, screen, 0, 0)
			finally:
				memory.SelectObject(wx.NullBitmap)

			image = bmp.ConvertToImage()
			if scale != 1.0:
				image = image.Scale(w_logical, h_logical, wx.IMAGE_QUALITY_HIGH)
			if max_width and w_logical > max_width:
				out_h = max(1, int(round(h_logical * (max_width / float(w_logical)))))
				image = image.Scale(max_width, out_h, wx.IMAGE_QUALITY_HIGH)
				w_logical, h_logical = max_width, out_h

			s = io.BytesIO()
			image.SetOption("quality", quality)
			image.SaveFile(s, wx.BITMAP_TYPE_JPEG)
			m = "image/jpeg"
			return base64.b64encode(s.getvalue()).decode("utf-8"), w_logical, h_logical, m
		except Exception as e:
			log.error(f"DPI-aware capture failed: {e}", exc_info=True)
			return None, 0, 0, ""

	def _capture_foreground(self, quality=85, max_width=1600):
		try:
			obj = api.getForegroundObject()
			if not obj or not obj.location:
				return None, 0, 0, 0, 0, ""
			x, y, w, h = obj.location
			if w < 1 or h < 1:
				return None, 0, 0, 0, 0, ""
			bmp = wx.Bitmap(w, h)
			wx.MemoryDC(bmp).Blit(0, 0, w, h, wx.ScreenDC(), x, y)
			img = bmp.ConvertToImage()
			if max_width and w > max_width:
				out_h = max(1, int(round(h * (max_width / float(w)))))
				img = img.Scale(max_width, out_h, wx.IMAGE_QUALITY_HIGH)
				w, h = max_width, out_h
			s = io.BytesIO()
			img.SetOption("quality", quality)
			img.SaveFile(s, wx.BITMAP_TYPE_JPEG)
			m = "image/jpeg"
			return base64.b64encode(s.getvalue()).decode("utf-8"), x, y, w, h, m
		except Exception as e:
			log.error(f"Foreground capture failed: {e}")
			return None, 0, 0, 0, 0, ""

	def _get_text_smart(self):
		focus_obj = api.getFocusObject()
		if not focus_obj:
			return None

		if hasattr(focus_obj, "treeInterceptor") and focus_obj.treeInterceptor:
			try:
				info = focus_obj.treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
				if info and info.text and not info.text.isspace():
					return info.text
			except Exception as e:
				log.debug(f"Selection extraction via treeInterceptor skipped: {e}")

		try:
			info = focus_obj.makeTextInfo(textInfos.POSITION_SELECTION)
			if info and info.text and not info.text.isspace():
				return info.text
		except Exception as e:
			log.debug(f"Selection extraction skipped: {e}")

		if isinstance(focus_obj, NVDAObjects.behaviors.EditableText):
			try:
				info = focus_obj.makeTextInfo(textInfos.POSITION_ALL)
				if info and info.text and not info.text.isspace():
					return info.text
			except Exception as e:
				log.debug(f"EditableText extraction skipped: {e}")

		if isinstance(focus_obj, NVDAObjects.behaviors.Terminal):
			try:
				info = focus_obj.makeTextInfo(textInfos.POSITION_ALL)
				return info.text
			except Exception as e:
				log.debug(f"Terminal text extraction skipped: {e}")

		try:
			obj = api.getNavigatorObject()
			if not obj:
				return None

			content = []
			if getattr(obj, "name", None):
				content.append(obj.name)
			if getattr(obj, "value", None):
				content.append(obj.value)
			if getattr(obj, "description", None):
				content.append(obj.description)

			if hasattr(obj, "makeTextInfo"):
				try:
					ti = obj.makeTextInfo(textInfos.POSITION_ALL)
					if ti.text and len(ti.text) < 2000:
						content.append(ti.text)
				except Exception as e:
					log.debug(f"Navigator obj makeTextInfo skipped: {e}")

			final_text = " ".join(list(dict.fromkeys([c for c in content if c and not c.isspace()])))
			return final_text if final_text else None
		except Exception as e:
			log.debug(f"Smart text extraction final fallback skipped: {e}")
			return None

	def _capture_fullscreen_sync(self):
		res = [None, 0, 0, ""]
		evt = threading.Event()

		def do_cap():
			try:
				res[0], res[1], res[2], res[3] = self._capture_fullscreen()
			except Exception as e:
				log.warning(f"Capture fullscreen sync failed: {e}")
			finally:
				evt.set()

		core.callLater(0, do_cap)
		evt.wait()
		return res[0], res[1], res[2], res[3]

	def _get_fg_app_name_sync(self):
		res = [""]
		evt = threading.Event()

		def do_get():
			try:
				res[0] = api.getForegroundObject().appModule.appName
			except Exception as e:
				log.warning(f"Get fg app name sync failed: {e}")
			finally:
				evt.set()

		core.callLater(0, do_get)
		evt.wait()
		return res[0]

	def _browse_and_run(self, worker_fn, wildcard, multiple=False):
		from ..utils.system import get_file_path

		# Translators: Message announced by NVDA when the live voice conversation ends.
		title = _("Open")
		path = get_file_path(title, wildcard, multiple=multiple)
		if path:
			threading.Thread(target=worker_fn, args=(path,), daemon=True).start()


def find_ffmpeg_silent():
	lib_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib")
	ffmpeg_lib_path = os.path.join(lib_dir, "ffmpeg.exe")
	if os.path.exists(ffmpeg_lib_path):
		return ffmpeg_lib_path
	path_ffmpeg = shutil.which("ffmpeg")
	if path_ffmpeg:
		return path_ffmpeg
	return None


def is_camera_privacy_blocked():
	paths = [
		(
			winreg.HKEY_CURRENT_USER,
			r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam",
		),
		(
			winreg.HKEY_LOCAL_MACHINE,
			r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam",
		),
		(
			winreg.HKEY_CURRENT_USER,
			r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam\NonPackaged",
		),
	]
	for root, path in paths:
		try:
			with winreg.OpenKey(root, path) as k:
				val, _ = winreg.QueryValueEx(k, "Value")
				if isinstance(val, str) and val.strip().lower() == "deny":
					return True
		except Exception:
			pass
	return False


def _decode_ffmpeg_stderr(data):
	for encoding in ("utf-8", "cp{0}".format(ctypes.windll.kernel32.GetOEMCP())):
		try:
			return data.decode(encoding)
		except UnicodeDecodeError:
			continue
	return data.decode("utf-8", "replace")


def enumerate_webcams(ffmpeg_path):
	names = []
	if ffmpeg_path:
		cmd = [ffmpeg_path, "-list_devices", "true", "-f", "dshow", "-i", "dummy"]
		creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
		text = ""
		try:
			res = subprocess.run(cmd, capture_output=True, timeout=10, creationflags=creationflags)
			text = _decode_ffmpeg_stderr(res.stderr)
			in_video = False
			for raw in text.splitlines():
				line = raw.strip()
				low = line.lower()
				if "directshow video devices" in low or "video devices" in low:
					in_video = True
					continue
				if "directshow audio devices" in low or "audio devices" in low:
					in_video = False
					continue
				if "alternative name" in low:
					continue
				if '"' not in line:
					continue
				start = line.find('"')
				end = line.rfind('"')
				if end <= start:
					continue
				dev_name = line[start + 1 : end].strip()
				if not dev_name:
					continue
				if "(video)" in low:
					if dev_name not in names:
						names.append(dev_name)
				elif in_video and "(audio)" not in low:
					if dev_name not in names:
						names.append(dev_name)
		except Exception as e:
			log.debug(f"Webcam enumeration failed: {e}")

		if not names:
			log.debug(f"No webcams found in FFmpeg output:\n{text}")

	log.debug(f"Discovered webcam devices: {names}")
	return names


class WebcamSource:
	MAX_FRAME_AGE = 5.0

	def __init__(self, ffmpeg_path, device_name):
		self._ffmpeg = ffmpeg_path
		self._device = device_name
		self._proc = None
		self._latest = None
		self._latest_time = 0.0
		self._lock = threading.Lock()
		self._stop = threading.Event()
		self._thread = None

	def start(self):
		if self._thread and self._thread.is_alive():
			return
		self._stop.clear()
		with self._lock:
			self._latest = None
			self._latest_time = 0.0
		self._thread = threading.Thread(target=self._run, daemon=True)
		self._thread.start()

	def stop(self):
		self._stop.set()
		proc = self._proc
		if proc:
			try:
				proc.terminate()
			except Exception:
				pass
		with self._lock:
			self._latest = None
			self._latest_time = 0.0
		thread = self._thread
		if thread and thread is not threading.current_thread():
			thread.join(timeout=0.2)

	def get_frame(self):
		with self._lock:
			if not self._latest:
				return None
			if time.monotonic() - self._latest_time > self.MAX_FRAME_AGE:
				return None
			return self._latest

	def _run(self):
		cmd = [
			self._ffmpeg,
			"-f",
			"dshow",
			"-i",
			"video={0}".format(self._device),
			"-r",
			"5",
			"-f",
			"image2pipe",
			"-vcodec",
			"mjpeg",
			"-q:v",
			"5",
			"-nostdin",
			"-",
		]
		creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
		try:
			self._proc = subprocess.Popen(
				cmd,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				creationflags=creationflags,
			)
		except Exception as e:
			log.error(f"Webcam process start failed: {e}")
			return
		if self._stop.is_set():
			try:
				self._proc.terminate()
			except Exception:
				pass
			return
		buf = b""
		got_any = False
		err_lines = []

		def _read_err():
			try:
				for line in iter(self._proc.stderr.readline, b""):
					if not line:
						break
					err_lines.append(line.decode("utf-8", "replace").strip())
			except Exception:
				pass

		err_thread = threading.Thread(target=_read_err, daemon=True)
		err_thread.start()

		try:
			while not self._stop.is_set():
				try:
					chunk = self._proc.stdout.read(65536)
				except Exception:
					break
				if not chunk:
					break
				buf += chunk
				while True:
					start = buf.find(b"\xff\xd8")
					if start == -1:
						buf = buf[-4:]
						break
					end = buf.find(b"\xff\xd9", start + 2)
					if end == -1:
						buf = buf[start:]
						break
					frame = buf[start : end + 2]
					buf = buf[end + 2 :]
					got_any = True
					with self._lock:
						self._latest = base64.b64encode(frame).decode("utf-8")
						self._latest_time = time.monotonic()
		finally:
			try:
				self._proc.terminate()
			except Exception:
				pass
			with self._lock:
				self._latest = None
				self._latest_time = 0.0
		if not got_any:
			err_text = " | ".join(err_lines[-5:]) if err_lines else "no stderr"
			log.debug(
				f"Webcam '{self._device}' produced no frames. Exit code: {self._proc.returncode}. Stderr: {err_text}",
			)
