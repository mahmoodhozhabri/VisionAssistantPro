# -*- coding: utf-8 -*-
import logging
import collections
import threading
import time

import ctypes
from ctypes import wintypes
import wx
import config as nvda_config
import gui

from .. import vision_config
from ..ai.live_session import LiveSession
from ..utils import logging_utils
from ..utils.error_contract import is_ai_error
from ..utils.system import check_screen_curtain_active, desktop_protection_reason
from ..prompt_utils import get_prompt_text

log = logging.getLogger(__name__)

_ = vision_config._ if hasattr(vision_config, "_") else (lambda x: x)

MODE_AUDIO = "audio"
MODE_SCREEN = "screen"
MODE_WEBCAM = "webcam"

_MODE_VIDEO = {MODE_SCREEN: "screen"}

_REPORTING_INSTRUCTIONS = {
	"brief": (
		"Answer in ONE short sentence of about 10 to 15 words, saying only what just changed or the one most "
		"important newly visible thing. No preamble, no repetition. If nothing meaningful has changed, remain completely silent."
	),
	"detailed": (
		"Answer in two or three sentences: first what appeared, changed, or became selected, then the most "
		"important newly visible text such as a dialog message, buttons, or menu items, word for word. Never "
		"repeat anything you have already reported. If nothing meaningful has changed, remain completely silent."
	),
	"custom": (
		"Follow the user context instructions for reporting style, format, and detail level. "
		"If no specific instructions are provided, report newly changed or appeared items clearly and concisely. "
		"If nothing meaningful has changed or if the screen is the same, remain completely silent."
	),
}


def _get_reporting_instruction(style):
	prompt_key = f"ambient_style_{style}"
	custom_text = get_prompt_text(prompt_key)
	if custom_text:
		return custom_text
	return _REPORTING_INSTRUCTIONS.get(style, _REPORTING_INSTRUCTIONS["brief"])


_VISION_CHANGED_TURN = (
	"New image received. Report only what newly changed, appeared, or was selected, following your reporting style and user context. "
	"If a rapid transition or sequence of changes occurred across recent frames (such as navigating through folders, menus, or windows), "
	"briefly summarize the path or action and state the final active location in one concise sentence. "
	"CRITICAL: If nothing meaningful has changed or appeared, remain completely silent and do not speak. "
	"Never say that nothing changed, never announce the absence of changes, and only speak when describing new changes. "
	"Do not repeat previous reports, do not re-name the active window unless it changed, and do not invent details."
)

_VISION_INITIAL_TURN = (
	"State in one short sentence that observation has started, and describe what is visible on the screen, "
	"following your reporting style and user context. Do not invent details."
)

_AMBIENT_WELCOME_PROMPT = (
	"Say only this, in one short sentence: that observation has started. "
	"Do not introduce yourself, do not mention any name, and do not add anything else. "
	"Speak strictly in {lang}."
)


def context_instruction(mode, context):
	if not context:
		return ""
	webcam = mode == MODE_WEBCAM
	prefix = "ambient_webcam_context" if webcam else "ambient_context"
	contexts = vision_config.AMBIENT_WEBCAM_CONTEXTS if webcam else vision_config.AMBIENT_CONTEXTS
	for key, _label, instruction in contexts:
		if key == context:
			override = get_prompt_text(f"{prefix}_{key}").strip()
			return override or instruction
	return "Additional context from the user: " + context


class BITMAPINFOHEADER(ctypes.Structure):
	_fields_ = [
		("biSize", ctypes.c_uint32),
		("biWidth", ctypes.c_int32),
		("biHeight", ctypes.c_int32),
		("biPlanes", ctypes.c_uint16),
		("biBitCount", ctypes.c_uint16),
		("biCompression", ctypes.c_uint32),
		("biSizeImage", ctypes.c_uint32),
		("biXPelsPerMeter", ctypes.c_int32),
		("biYPelsPerMeter", ctypes.c_int32),
		("biClrUsed", ctypes.c_uint32),
		("biClrImportant", ctypes.c_uint32),
	]


class BITMAPINFO(ctypes.Structure):
	_fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", ctypes.c_uint32 * 3)]

TRANSLATE_MODEL = "gemini-3.5-live-translate-preview"


class AmbientObserver:
	MAX_RECONNECTS = 3
	RECONNECT_DELAY = 5.0
	MAX_PENDING_FRAMES = 12
	DIFF_THRESHOLD = 0.04
	PIXEL_DELTA = 24
	SIG_WIDTH = 96
	SIG_HEIGHT = 54
	MIN_GAP_SECONDS = 0.5
	REPORT_MIN_INTERVAL = 3.0
	DETECT_INTERVAL_MS = 300
	FRAME_LOG_EVERY = 20
	DESKTOP_CHECK_INTERVAL = 1.0
	HALFTONE = 4
	SRCCOPY = 0x00CC0020

	def __init__(self, status_callback, text_callback=None, closed_callback=None, capture_fullscreen=None, capture_window=None):
		self.status_callback = status_callback
		self.text_callback = text_callback
		self.closed_callback = closed_callback
		self.capture_fullscreen = capture_fullscreen
		self.capture_window = capture_window
		self.mode = MODE_AUDIO
		self.session = None
		self.timer = None
		self.video_source = None
		self.audio_enabled = True
		self.interval_ms = 3000
		self._started = False
		self._stopping = False
		self._prev_sig = None
		self._last_queued_sig = None
		self._last_sent = 0.0
		self._reconnect_attempts = 0
		self._last_target_code = None
		self._last_context = None
		self._last_audio_source = "system"
		self._resume_handle = ""
		self._frame_queue = collections.deque()
		self._queue_lock = threading.Lock()
		self._sender_thread = None
		self._video_loop_started = False
		self._report_pending = False
		self._first_frame_done = False
		self._initial_report_sent = False
		self._reconnect_timer = None
		self._next_report_at = 0.0
		self._send_interval = self.MIN_GAP_SECONDS
		self._wake = threading.Event()
		self._frames_captured = 0
		self._frames_sent = 0
		self._capture_paused = False
		self._blocked_checked_at = 0.0

	def start(self, mode=None, target_code=None, context=None, retry=False, audio_source=None, style=None):
		conf = nvda_config.conf["VisionAssistant"]
		self.mode = mode or conf.get("ambient_observer_mode", MODE_AUDIO)
		video = _MODE_VIDEO.get(self.mode)
		translation_mode = self.mode == MODE_AUDIO
		chosen_source = audio_source or conf.get("ambient_audio_source", "system")
		self.audio_enabled = translation_mode
		self.video_source = video
		self._stopping = False
		if getattr(self, "_reconnect_timer", None):
			try:
				self._reconnect_timer.cancel()
			except Exception:
				pass
			self._reconnect_timer = None
		if not retry:
			self._reconnect_attempts = 0
			self._resume_handle = ""
			self._initial_report_sent = False
			self._first_frame_done = False
		self._last_target_code = target_code
		self._last_context = context
		self._last_audio_source = chosen_source
		if context is None:
			context = conf.get("ambient_context", "")
		context_text = context_instruction(self.mode, context)
		self._video_loop_started = False
		if video:
			try:
				seconds = int(conf.get("live_frame_interval", conf.get("ambient_frame_interval", 3)))
			except Exception as e:
				log.debug(f"Ambient frame interval read failed: {e}")
				seconds = 3
			self.interval_ms = max(1, min(10, seconds)) * 1000
			self._send_interval = max(self.MIN_GAP_SECONDS, self.interval_ms / 1000.0)
		style = style or conf.get("ambient_reporting_style", "brief")
		model = ""
		translation_config = None
		if translation_mode:
			model = TRANSLATE_MODEL
			target_lang = vision_config.get_lang_name("target_language")
			translation_config = {
				"targetLanguageCode": target_code or vision_config.TARGET_CODES.get(target_lang, "en"),
				"echoTargetLanguage": bool(conf.get("smart_swap", False)),
			}
		source = self._last_audio_source if self.audio_enabled else "silence"
		if translation_config:
			session_prompt_kwargs = {"greet": False, "announce_start": False}
		else:
			session_prompt_kwargs = {
				"prompt_key": "ambient_observer_system",
				"greet": False if video else (not retry),
				"announce_start": False,
				"welcome_prompt": _AMBIENT_WELCOME_PROMPT,
			}
		self.session = LiveSession(
			on_text=self._on_text,
			on_status=self._on_session_status,
			on_closed=self._on_session_closed,
			audio_source=source,
			model=model,
			reporting_style=_get_reporting_instruction(style),
			barge_in=False,
			voice_enabled=not translation_mode,
			translation_config=translation_config,
			push_to_talk=False,
			context=context_text,
			resume_handle=self._resume_handle,
			**session_prompt_kwargs,
		)
		if not self.session.start():
			self.session = None
			return False
		if self._stopping:
			if self.session:
				try:
					self.session.stop()
				except Exception:
					pass
				self.session = None
			return False
		logging_utils.log_addon(
			logging.INFO,
			f"Ambient Observer started: mode={self.mode}, audio={self.audio_enabled}, video={video}, style={style}, model={model or 'default'}",
		)
		self._started = True
		if video:
			self._start_sender()
		return True

	def _on_text(self, line):
		if self.text_callback:
			try:
				self.text_callback(line)
			except Exception as e:
				log.debug(f"Ambient text callback failed: {e}")

	def _on_session_status(self, msg):
		if self._resume_handle and is_ai_error(msg):
			self._resume_handle = ""
			log.warning(f"Ambient Observer session resume was refused; reconnecting without it: {msg}")
			session = self.session
			if session:
				threading.Thread(target=session.stop, daemon=True).start()
			return
		try:
			self.status_callback(msg)
		except Exception as e:
			log.debug(f"Ambient status callback failed: {e}")

	def _start_video_loop(self):
		if self._video_loop_started or not self.video_source or not self.session:
			return
		self._video_loop_started = True
		self._start_sender()
		if wx.IsMainThread():
			self._start_timer()
			self._tick_screen()
		else:
			wx.CallAfter(self._start_timer)
			wx.CallAfter(self._tick_screen)

	def _on_session_closed(self):
		session = self.session
		self._started = False
		self._stop_timer()
		if getattr(self, "_reconnect_timer", None):
			try:
				self._reconnect_timer.cancel()
			except Exception:
				pass
			self._reconnect_timer = None
		with self._queue_lock:
			self._frame_queue.clear()
		handle = getattr(session, "resumption_handle", "") if session else ""
		if handle and getattr(session, "resumable", False):
			self._resume_handle = handle
			log.info("Ambient Observer kept the session handle to resume after the connection loss.")
		else:
			self._resume_handle = ""
		if self._stopping or self._reconnect_attempts >= self.MAX_RECONNECTS:
			self._notify_closed()
			return
		self._reconnect_attempts += 1
		self.session = None
		log.warning(
			f"Ambient Observer connection lost; reconnect attempt {self._reconnect_attempts}"
		)
		if self.status_callback:
			try:
				# Translators: Status message announced when the connection to the server is lost and the Ambient Observer tries to reconnect.
				self.status_callback("STATUS:" + _("Connection lost. Reconnecting..."))
			except Exception as e:
				log.debug(f"Ambient status callback failed: {e}")
		self._reconnect_timer = threading.Timer(self.RECONNECT_DELAY, self._reconnect)
		self._reconnect_timer.daemon = True
		self._reconnect_timer.start()

	def _reconnect(self):
		self._reconnect_timer = None
		if self._stopping:
			return
		try:
			if not self.start(
				self.mode, self._last_target_code, self._last_context, retry=True,
				audio_source=self._last_audio_source,
			):
				self._notify_closed()
		except Exception as e:
			log.error(f"Ambient Observer reconnect failed: {e}", exc_info=True)
			self._notify_closed()

	def _notify_closed(self):
		if not self.closed_callback:
			return
		try:
			self.closed_callback()
		except Exception as e:
			log.debug(f"Ambient closed callback failed: {e}")

	def is_running(self):
		return bool(self.session) and self._started

	def _start_timer(self):
		if self.timer or not self.session:
			return
		self.timer = wx.Timer(gui.mainFrame)
		gui.mainFrame.Bind(wx.EVT_TIMER, self._on_tick, self.timer)
		self.timer.Start(self.DETECT_INTERVAL_MS)

	def _stop_timer(self):
		if not self.timer:
			return
		if not wx.IsMainThread():
			wx.CallAfter(self._stop_timer)
			return
		try:
			self.timer.Stop()
			gui.mainFrame.Unbind(wx.EVT_TIMER, handler=self._on_tick, source=self.timer)
		except Exception as e:
			log.debug(f"Ambient timer cleanup failed: {e}")
		self.timer = None

	def _on_tick(self, event):
		if not self.session:
			return
		self._tick_screen()

	def _desktop_blocked(self):
		now = time.time()
		if now - self._blocked_checked_at < self.DESKTOP_CHECK_INTERVAL:
			return bool(getattr(self, "_blocked_reason", None))
		self._blocked_checked_at = now
		reason = desktop_protection_reason()
		previous = getattr(self, "_blocked_reason", None)
		if reason == "curtain" and previous != "curtain":
			check_screen_curtain_active()
		if reason:
			if previous != reason:
				self._blocked_reason = reason
				log.info(f"Ambient Observer paused while the desktop is protected: {reason}")
			return True
		self._blocked_reason = None
		return False

	def _capture_pause_pending(self):
		with self._queue_lock:
			pending_count = len(self._frame_queue)
		if pending_count >= self.MAX_PENDING_FRAMES:
			if not self._capture_paused:
				self._capture_paused = True
				log.debug(f"Ambient capture paused: {pending_count} frames are waiting to be sent.")
			return True
		self._capture_paused = False
		return False

	def _tick_screen(self):
		if self._desktop_blocked():
			return
		if self._capture_pause_pending():
			return
		session = self.session
		if not session or not session.ready:
			return
		now = time.time()
		region = self._foreground_region() if self.capture_window else None
		if self.capture_window and region is None:
			return
		sig = self._screen_signature(region)
		if not self._should_send(sig, now):
			return
		try:
			if self.capture_window:
				image = self.capture_window()
				b64 = image[0] if image else None
			else:
				if not self.capture_fullscreen:
					return
				b64 = self.capture_fullscreen()[0]
		except Exception as e:
			log.debug(f"Ambient screen capture failed: {e}")
			return
		if not b64:
			return
		self._send_frame(b64, sig)

	def _foreground_region(self):
		try:
			user32 = ctypes.windll.user32
			hwnd = user32.GetForegroundWindow()
			if not hwnd:
				return None
			rect = wintypes.RECT()
			user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
			if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
				return None
			width, height = rect.right - rect.left, rect.bottom - rect.top
			if width < 1 or height < 1:
				return None
			return (rect.left, rect.top, width, height)
		except Exception as e:
			log.debug(f"Ambient foreground window check failed: {e}")
			return None

	def _send_frame(self, jpeg_b64, sig=None):
		session = self.session
		if not session or not session.ready:
			return False
		try:
			number = self._frames_captured + 1
			prompt = _VISION_CHANGED_TURN if self.video_source else ""
			with self._queue_lock:
				self._frame_queue.append((jpeg_b64, prompt, sig, number))
			self._frames_captured = number
			self._last_sent = time.time()
			if sig is not None:
				self._last_queued_sig = sig
			self._wake.set()
			return True
		except Exception as e:
			log.debug(f"Ambient frame send failed: {e}")
			return False

	def _start_sender(self):
		if self._sender_thread and self._sender_thread.is_alive():
			return
		self._sender_thread = threading.Thread(target=self._sender_loop, daemon=True)
		self._sender_thread.start()

	def _sender_loop(self):
		while not self._stopping:
			try:
				session = self.session
				if session and session.ready and not self._video_loop_started:
					self._start_video_loop()
				if (
					self._report_pending
					and session
					and session.ready
					and not session.model_busy()
					and time.time() >= self._next_report_at
				):
					self._report_pending = False
					self._next_report_at = time.time() + self.REPORT_MIN_INTERVAL
					self._request_report(session)

				with self._queue_lock:
					item = self._frame_queue[0] if self._frame_queue else None
				if not item:
					self._wake.clear()
					self._wake.wait(0.05 if self._report_pending else 0.5)
					continue

				jpeg_b64, prompt, sig, number = item
				session = self.session
				if not session or not session.ready:
					self._wake.clear()
					self._wake.wait(0.05)
					continue

				sent = False
				try:
					sent = bool(session.send_video_frame(jpeg_b64))
					if sent:
						log.debug("Ambient frame sent to the conversation")
				except Exception as e:
					log.debug(f"Ambient frame send failed: {e}")

				if not sent:
					self._wake.clear()
					self._wake.wait(0.05)
					continue

				with self._queue_lock:
					if self._frame_queue:
						self._frame_queue.popleft()
						pending_count = len(self._frame_queue)
					else:
						pending_count = 0

				self._frames_sent += 1
				if self._frames_sent % self.FRAME_LOG_EVERY == 0:
					log.debug(
						f"Ambient frames: {self._frames_sent} sent of {self._frames_captured} captured, "
						f"{pending_count} waiting (frame {number})."
					)
				if sig is not None:
					self._prev_sig = sig
				if self.video_source == "screen":
					if not self._first_frame_done:
						self._first_frame_done = True
						if session.send_image_turn(jpeg_b64, _VISION_INITIAL_TURN):
							self._initial_report_sent = True
							self._next_report_at = time.time() + self.REPORT_MIN_INTERVAL
							log.debug("Ambient initial report sent with image")
						else:
							self._report_pending = True
					else:
						self._report_pending = True
			except Exception as e:
				log.exception(f"Error in ambient sender loop: {e}")
				self._wake.clear()
				self._wake.wait(0.1)

		log.debug(f"Ambient frames: {self._frames_sent} sent of {self._frames_captured} captured.")
		with self._queue_lock:
			self._frame_queue.clear()

	def _screen_signature(self, region=None):
		user32 = ctypes.windll.user32
		gdi32 = ctypes.windll.gdi32
		screen_dc = user32.GetDC(0)
		if not screen_dc:
			return None
		mem_dc = None
		bitmap = None
		old_bitmap = None
		try:
			src_x, src_y, src_w, src_h = region or (
				user32.GetSystemMetrics(76),
				user32.GetSystemMetrics(77),
				user32.GetSystemMetrics(78) or user32.GetSystemMetrics(0),
				user32.GetSystemMetrics(79) or user32.GetSystemMetrics(1),
			)
			if src_w < 1 or src_h < 1:
				return None
			mem_dc = gdi32.CreateCompatibleDC(screen_dc)
			if not mem_dc:
				return None
			bitmap = gdi32.CreateCompatibleBitmap(screen_dc, self.SIG_WIDTH, self.SIG_HEIGHT)
			if not bitmap:
				return None
			old_bitmap = gdi32.SelectObject(mem_dc, bitmap)
			gdi32.SetStretchBltMode(mem_dc, self.HALFTONE)
			gdi32.StretchBlt(
				mem_dc,
				0,
				0,
				self.SIG_WIDTH,
				self.SIG_HEIGHT,
				screen_dc,
				src_x,
				src_y,
				src_w,
				src_h,
				self.SRCCOPY,
			)
			buffer = ctypes.create_string_buffer(self.SIG_WIDTH * self.SIG_HEIGHT * 4)
			info = BITMAPINFO()
			info.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
			info.bmiHeader.biWidth = self.SIG_WIDTH
			info.bmiHeader.biHeight = -self.SIG_HEIGHT
			info.bmiHeader.biPlanes = 1
			info.bmiHeader.biBitCount = 32
			gdi32.GetDIBits(mem_dc, bitmap, 0, self.SIG_HEIGHT, buffer, ctypes.byref(info), 0)
			return (region, bytes(buffer))
		except Exception as e:
			log.debug(f"Ambient screen signature failed: {e}")
			return None
		finally:
			if mem_dc and old_bitmap:
				gdi32.SelectObject(mem_dc, old_bitmap)
			if bitmap:
				gdi32.DeleteObject(bitmap)
			if mem_dc:
				gdi32.DeleteDC(mem_dc)
			if screen_dc:
				user32.ReleaseDC(0, screen_dc)

	def _diff_ratio(self, prev, cur):
		if prev is None or cur is None:
			return 1.0
		prev_region, prev_bytes = prev
		cur_region, cur_bytes = cur
		if prev_region != cur_region or not cur_bytes or len(prev_bytes) != len(cur_bytes):
			return 1.0
		total = len(cur_bytes) // 4
		if total < 1:
			return 0.0
		changed = 0
		for i in range(0, len(cur_bytes), 4):
			delta = (
				abs(cur_bytes[i] - prev_bytes[i])
				+ abs(cur_bytes[i + 1] - prev_bytes[i + 1])
				+ abs(cur_bytes[i + 2] - prev_bytes[i + 2])
			)
			if delta > self.PIXEL_DELTA:
				changed += 1
		return changed / total

	def _should_send(self, sig, now):
		if sig is None:
			return False
		ref_sig = getattr(self, "_last_queued_sig", None)
		if ref_sig is None:
			ref_sig = self._prev_sig
		if ref_sig is None or len(ref_sig) != len(sig):
			return True
		if now - self._last_sent < self._send_interval:
			return False
		return self._diff_ratio(ref_sig, sig) >= self.DIFF_THRESHOLD

	def _request_report(self, session):
		try:
			if not self._initial_report_sent:
				if session.send_client_text(_VISION_INITIAL_TURN):
					self._initial_report_sent = True
					log.debug("Ambient report requested (initial=True)")
				else:
					log.debug("Ambient report request send returned False")
				return
			if session.send_client_text(_VISION_CHANGED_TURN):
				log.debug("Ambient report requested")
			else:
				log.debug("Ambient report request send returned False")
		except Exception as e:
			log.debug(f"Ambient report request failed: {e}")

	def stop(self):
		self._started = False
		self._stopping = True
		self._prev_sig = None
		self._last_queued_sig = None
		self._resume_handle = ""
		self._first_frame_done = False
		self._initial_report_sent = False
		if getattr(self, "_reconnect_timer", None):
			try:
				self._reconnect_timer.cancel()
			except Exception:
				pass
			self._reconnect_timer = None
		with self._queue_lock:
			self._frame_queue.clear()
		self._wake.set()
		self._stop_timer()
		session = self.session
		self.session = None
		if not session:
			return
		try:
			session.stop()
		except Exception as e:
			log.debug(f"Ambient session stop failed: {e}")