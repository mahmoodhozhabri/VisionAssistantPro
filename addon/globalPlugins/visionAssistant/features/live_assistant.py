# -*- coding: utf-8 -*-
import logging
import threading
import time

import wx
import addonHandler
import config as nvda_config
import gui
import tones

from ..ai.core import AIHandler, ai_error_message, is_ai_error
from ..ai.live_session import LiveSession
from ..dialogs.live_assistant import LiveAssistantDialog
from ..prompt_utils import get_prompt_text
from ..utils.system import show_error_dialog
from .live_operator import LIVE_OPERATOR_TOOLS, LIVE_OPERATOR_WELCOME_PROMPT
from .screen_capture import enumerate_webcams, find_ffmpeg_silent, is_camera_privacy_blocked

log = logging.getLogger(__name__)

addonHandler.initTranslation()


class LiveAssistantMixin:
	LIVE_RESUME_MAX_ATTEMPTS = 5
	LIVE_FRAME_KEEPALIVE = 15.0

	def _end_live_session(self):
		self._stop_live_operator()
		self._live_user_stop = True
		self._live_resume_handle = ""
		self._live_resume_attempts = 0
		if self.live_session:
			try:
				self.live_session.stop()
			except Exception as e:
				log.debug(f"Live session stop failed: {e}")
			self.live_session = None

	def _live_append(self, line):
		self._live_history += line + "\n"
		if getattr(self, "live_dlg", None):
			try:
				self.live_dlg.append_line(line)
			except Exception as e:
				log.debug(f"Live dialog append_line failed: {e}")

	def _live_on_closed(self):
		session = self.live_session
		resume_handle = getattr(session, "resumption_handle", "") if session else ""
		resuming = bool(
			resume_handle
			and getattr(session, "resumable", False)
			and not getattr(self, "_live_user_stop", False)
			and getattr(self, "_live_resume_attempts", 0) < self.LIVE_RESUME_MAX_ATTEMPTS
		)
		if getattr(self, "_live_history", ""):
			self._last_live_history = self._live_history
		self.live_session = None
		if getattr(self, "_live_video_timer", None):
			try:
				self._live_video_timer.Stop()
				gui.mainFrame.Unbind(
					wx.EVT_TIMER, handler=self._on_live_video_tick, source=self._live_video_timer
				)
			except Exception as e:
				log.debug(f"Live video timer cleanup failed: {e}")
			self._live_video_timer = None
		if getattr(self, "live_dlg", None) and LiveAssistantDialog.instance:
			try:
				self.live_dlg.set_active(False)
				if not resuming:
					# Translators: Line appended to the conversation when the live session has ended.
					self._live_history += _("--- Session ended ---") + "\n"
					self.live_dlg.append_line(_("--- Session ended ---"))
			except Exception as e:
				log.debug(f"Live dialog session-ended append failed: {e}")
		else:
			self.live_dlg = None
		self._webcam_wanted = False
		self._webcam_gen = getattr(self, "_webcam_gen", 0) + 1
		self._stop_webcam_source()
		if getattr(self, "live_dlg", None) and LiveAssistantDialog.instance:
			try:
				self.live_dlg.set_webcam_active(False)
			except Exception as e:
				log.debug(f"Live webcam state reset failed: {e}")
		if resuming:
			self._live_resume_handle = resume_handle
			self._live_resume_attempts = getattr(self, "_live_resume_attempts", 0) + 1
			log.info(
				"Live: session ended by the server; resuming with the previous handle "
				f"(attempt {self._live_resume_attempts})."
			)
			tones.beep(660, 120)
			wx.CallLater(1200, self._start_live_session, True)
			return
		self._live_resume_handle = ""
		self._live_resume_attempts = 0
		tones.beep(440, 120)
		# Translators: Message announced by NVDA when the live voice conversation ends.
		self.report_status(_("Live conversation ended."))

	def _live_status(self, msg):
		if is_ai_error(msg):
			show_error_dialog(ai_error_message(msg))
			self._end_live_session()
		elif msg.startswith("STATUS:"):
			self.report_status(msg[7:])

	def _live_stream(self, chunk):
		self._live_history += chunk
		if getattr(self, "live_dlg", None):
			try:
				self.live_dlg.append_raw(chunk)
			except Exception as e:
				log.debug(f"Live dialog append_raw failed: {e}")

	def _on_live_video_tick(self, event):
		self._send_live_frame()

	def _send_live_frame(self, force=False):
		session = self.live_session
		if not session:
			return
		if getattr(self, "_live_frame_in_flight", False):
			return
		self._live_frame_in_flight = True
		threading.Thread(target=self._live_frame_worker, args=(session, force), daemon=True).start()

	def _live_keepalive_due(self):
		return time.time() - getattr(self, "_live_frame_sent_at", 0) >= self.LIVE_FRAME_KEEPALIVE

	def _log_frame_sent(self, source, size):
		self._live_frame_sent_at = time.time()
		self._live_frame_skip_reason = None
		now = time.time()
		if now - getattr(self, "_live_frame_log_at", 0) >= self.LIVE_FRAME_LOG_INTERVAL:
			self._live_frame_log_at = now
			log.debug("Live frame sent: source=%s size=%s", source, size)

	def _log_frame_skip(self, reason):
		if getattr(self, "_live_frame_skip_reason", None) == reason:
			return
		self._live_frame_skip_reason = reason
		log.debug("Live frame not sent: %s", reason)

	def _live_frame_worker(self, session, force=False):
		try:
			if not force and session.user_speaking() and not self._live_keepalive_due():
				self._log_frame_skip("push to talk is idle")
				return
			jpeg_b64 = None
			size = "-"
			source = "screen"
			if getattr(self, "_webcam_wanted", False):
				source = "webcam"
				src = getattr(self, "_webcam_source", None)
				if src:
					jpeg_b64 = src.get_frame()
				if not jpeg_b64:
					if not getattr(self, "_webcam_no_frame_logged", False):
						self._webcam_no_frame_logged = True
						log.warning(
							f"Live webcam is enabled but no camera frame is available; no frame will be sent (source: {'running' if src else 'not started'}). Check camera availability and the ffmpeg dshow device."
						)
					self._log_frame_skip("webcam produced no frame")
					return
				self._webcam_no_frame_logged = False
			else:
				self._webcam_no_frame_logged = False
				jpeg_b64, width, height, _mime = self._capture_fullscreen(quality=85, max_width=1600)
				size = "{0}x{1}".format(width, height)
			if jpeg_b64:
				session.send_video_frame(jpeg_b64)
				self._log_frame_sent(source, size)
			else:
				self._log_frame_skip("screen capture returned no image")
		except Exception as e:
			log.warning(f"Live video frame capture failed: {e}")
		finally:
			self._live_frame_in_flight = False

	def _send_live_frame_when_ready(self, attempt=0):
		session = self.live_session
		if not session:
			return
		if getattr(session, "ready", False):
			self._send_live_frame(force=True)
			return
		if attempt < 12:
			wx.CallLater(400, self._send_live_frame_when_ready, attempt + 1)

	def _show_live_window(self, force_show=False, is_recall=False):
		self._last_result_data = (self._show_live_window, ())
		if getattr(self, "live_dlg", None) and LiveAssistantDialog.instance is self.live_dlg:
			self.live_dlg.set_active(bool(self.live_session))
		else:
			if is_recall:
				self._live_history = getattr(self, "_last_live_history", "") or ""
			self.live_dlg = LiveAssistantDialog(
				gui.mainFrame,
				self._start_live_session,
				self._end_live_session,
				initial_history=self._live_history,
				webcam_callback=self._set_live_source,
				webcam_device_callback=self._set_live_device,
			)
			self.live_dlg.set_active(bool(self.live_session))
			self.live_dlg.Show()
		self.live_dlg.Raise()
		self.live_dlg.history.SetFocus()
		threading.Thread(target=self._check_webcam_availability, args=(self.live_dlg,), daemon=True).start()

	def _start_live_session(self, resume=False, webcam=False, push_to_talk=None, context="", operator=False):
		if self.live_session or not AIHandler.is_gemini():
			return
		if not resume:
			self._live_user_stop = False
			self._live_resume_handle = ""
			self._live_resume_attempts = 0
			self._set_live_operator_session(bool(operator))
		dlg = getattr(self, "live_dlg", None)
		restarting = False
		if dlg and LiveAssistantDialog.instance is dlg:
			restarting = bool(getattr(dlg, "_restarting", False))
			dlg._restarting = False
		if not restarting and not resume:
			self._live_history = ""
			if dlg and LiveAssistantDialog.instance is dlg:
				try:
					dlg.clear_history()
				except Exception as e:
					log.debug(f"Live dialog history clear failed: {e}")
		tones.beep(660, 120)
		direct = nvda_config.conf["VisionAssistant"]["live_direct_output"]
		live_kwargs = {"resume_handle": getattr(self, "_live_resume_handle", "")}
		if push_to_talk is not None:
			live_kwargs["push_to_talk"] = push_to_talk
		if context:
			live_kwargs["context"] = context
		operator_enabled = self._live_operator_on()
		if operator_enabled:
			live_kwargs["welcome_prompt"] = LIVE_OPERATOR_WELCOME_PROMPT
			webcam = False
		tool_instruction = get_prompt_text("live_operator_system") if operator_enabled else ""
		self.live_session = LiveSession(
			on_text=lambda line: wx.CallAfter(self._live_append, line),
			on_status=lambda msg: wx.CallAfter(self._live_status, msg),
			on_closed=lambda: wx.CallAfter(self._live_on_closed),
			on_stream=lambda chunk: wx.CallAfter(self._live_stream, chunk),
			on_user_speech=lambda: wx.CallAfter(self._send_live_frame, True),
			tools=LIVE_OPERATOR_TOOLS if operator_enabled else None,
			tool_instruction=tool_instruction,
			on_tool_call=lambda session, call: wx.CallAfter(self._live_operator_call, session, call),
			on_tool_cancel=self._live_operator_cancel,
			**live_kwargs,
		)
		if webcam or not direct:
			self._show_live_window()
		if webcam:
			self._set_live_source(True)
			dlg = getattr(self, "live_dlg", None)
			if dlg and LiveAssistantDialog.instance is dlg:
				try:
					dlg.set_webcam_active(True)
				except Exception as e:
					log.debug(f"Webcam UI state update failed: {e}")
		self._live_video_timer = wx.Timer(gui.mainFrame)
		gui.mainFrame.Bind(wx.EVT_TIMER, self._on_live_video_tick, self._live_video_timer)
		try:
			sec = int(
				nvda_config.conf["VisionAssistant"].get(
					"live_frame_interval",
					nvda_config.conf["VisionAssistant"].get("ambient_frame_interval", 3),
				)
			)
		except Exception:
			sec = 3
		interval_ms = max(1, min(10, sec)) * 1000
		self._live_video_timer.Start(interval_ms)
		self._live_frame_sent_at = 0
		self._live_frame_log_at = 0
		self._live_frame_skip_reason = None
		wx.CallLater(400, self._send_live_frame_when_ready)
		threading.Thread(target=self._start_live_worker, daemon=True).start()

	def _start_live_worker(self):
		session = self.live_session
		if session and not session.start():
			wx.CallAfter(self._live_on_closed)

	def _check_webcam_availability(self, dlg):
		try:
			privacy_blocked = is_camera_privacy_blocked()
		except Exception as e:
			log.debug(f"Webcam privacy check failed: {e}")
			privacy_blocked = False
		try:
			ffmpeg_path = find_ffmpeg_silent()
			devices = enumerate_webcams(ffmpeg_path) if ffmpeg_path else []
		except Exception as e:
			log.debug(f"Webcam availability check failed: {e}")
			devices = []
			ffmpeg_path = None
		self._webcam_devices = devices
		self._webcam_ffmpeg_path = ffmpeg_path
		saved = nvda_config.conf["VisionAssistant"].get("live_webcam_device", "")
		if devices and saved not in devices:
			saved = devices[0]
			try:
				nvda_config.conf["VisionAssistant"]["live_webcam_device"] = saved
			except Exception as e:
				log.debug(f"Webcam default device save failed: {e}")
		self._webcam_device = saved
		wx.CallAfter(self._apply_webcam_availability, dlg, devices, ffmpeg_path, privacy_blocked)

	def _set_live_source(self, enabled):
		if enabled and self._live_operator_on():
			# Translators: The webcam cannot be used while Live operator control is switched on.
			self.report_status(_("The webcam is not available while operator control is on."))
			dlg = getattr(self, "live_dlg", None)
			if dlg and LiveAssistantDialog.instance is dlg:
				try:
					dlg.set_webcam_active(False)
				except Exception as e:
					log.debug(f"Webcam checkbox reset failed: {e}")
			return
		self._webcam_wanted = bool(enabled)
		if enabled:
			self._start_webcam_worker()
		else:
			self._webcam_gen = getattr(self, "_webcam_gen", 0) + 1
			self._stop_webcam_source()

	def _set_live_device(self, device):
		if not device:
			return
		self._webcam_device = device
		try:
			nvda_config.conf["VisionAssistant"]["live_webcam_device"] = device
		except Exception as e:
			log.debug(f"Webcam device preference save failed: {e}")
		if self._webcam_wanted:
			self._start_webcam_worker()
