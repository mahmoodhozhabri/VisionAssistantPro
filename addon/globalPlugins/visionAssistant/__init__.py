# -*- coding: utf-8 -*-
import sys
import os
import json
import threading
import logging
import tempfile
import time
import datetime
import gc
import ctypes
import shutil
import wx

import addonHandler
import globalPluginHandler
import globalVars
import config as nvda_config
import gui
import ui
import core
import api
import tones
import scriptHandler
import NVDAObjects

lib_dir = os.path.join(os.path.dirname(__file__), "lib")
if lib_dir not in sys.path:
	sys.path.append(lib_dir)

arch_lib_dir = os.path.join(lib_dir, "x64" if sys.maxsize > 2**32 else "x86")
if arch_lib_dir not in sys.path:
	sys.path.insert(0, arch_lib_dir)

log = logging.getLogger(__name__)
addonHandler.initTranslation()

from . import plugin_state
from .ai.core import AIHandler, provider_model_name, is_ai_error, ai_error_message
from .utils.system import (
	show_error_dialog,
	_generate_object_signature,
	long_path as _long_path,
	is_gemini_provider,
)
from .utils import logging_utils
from .vision_config import (
	LABELS_FILE,
	ADDON_NAME,
	GITHUB_REPO,
	HISTORY_FILE,
	_migrate_data_dir,
	AMBIENT_MODE_LIST,
)

_migrate_data_dir()
from .utils.updater import UpdateManager
from .utils.announcements import AnnouncementManager
from .features.vision import VisionMixin
from .features.screen_capture import ScreenCaptureMixin
from .features.audio import AudioMixin
from .features.video import VideoMixin
from .features.operator_captcha import OperatorCaptchaMixin
from .features.quick_settings import QuickSettingsMixin
from .features.upload import UploadMixin
from .features.ambient import AmbientObserver, MODE_AUDIO, MODE_WEBCAM, context_instruction
from .dialogs.media import AmbientStartDialog
from .features.screen_capture import find_ffmpeg_silent, enumerate_webcams
from .dialogs.settings import SettingsPanel
from .prompt_utils import (
	finally_,
	load_configured_custom_prompts,
	_format_hotkey_display,
	parse_ambient_prompt,
)

from .dialogs import donate


def check_and_restore_lib_backup():
	def _restore_worker():
		time.sleep(10.0)
		try:
			backup_dir = os.path.join(tempfile.gettempdir(), "VisionAssistant_Lib_Backup")
			manifest_file = os.path.join(backup_dir, "backup_manifest.json")
			if not os.path.exists(manifest_file):
				return

			target_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
			os.makedirs(_long_path(target_lib_dir), exist_ok=True)

			failed = False
			for item in os.listdir(_long_path(backup_dir)):
				if item in ("backup_manifest.json", "google-cloud-sdk"):
					continue
				src = os.path.join(backup_dir, item)
				dst = os.path.join(target_lib_dir, item)
				try:
					if os.path.isdir(_long_path(src)):
						shutil.copytree(_long_path(src), _long_path(dst), dirs_exist_ok=True)
					elif not os.path.exists(_long_path(dst)):
						shutil.copy2(_long_path(src), _long_path(dst))
				except Exception as e:
					failed = True
					log.warning(f"Lib backup restore failed for {item}: {e}")

			if failed:
				log.warning("Lib backup restore incomplete; keeping backup for retry on next start.")
				return
			shutil.rmtree(_long_path(backup_dir), ignore_errors=True)
		except Exception as e:
			log.warning(f"Lib backup restore failed: {e}")

	def _start():
		threading.Thread(target=_restore_worker, daemon=True).start()

	wx.CallLater(5000, _start)


class CustomLabelOverlay(NVDAObjects.NVDAObject):
	@property
	def name(self):
		instance = plugin_state.plugin_instance
		uniqueId = instance._getAppId(self) if instance else self.appModule.appName

		key = _generate_object_signature(self)
		cache = getattr(instance, "labels_cache", {})
		if uniqueId in cache:
			if key and key in cache[uniqueId]:
				return cache[uniqueId][key]

		return super().name


class GlobalPlugin(
	globalPluginHandler.GlobalPlugin,
	VisionMixin,
	ScreenCaptureMixin,
	AudioMixin,
	VideoMixin,
	OperatorCaptchaMixin,
	QuickSettingsMixin,
	UploadMixin,
):
	scriptCategory = ADDON_NAME

	last_translation = ""
	is_recording = False
	temp_audio_file = os.path.join(tempfile.gettempdir(), "vision_dictate.wav")

	translation_cache = {}
	_last_source_text = None
	_last_params = None
	update_timer = None

	is_ui_explorer_active = False

	_operator_history = []
	_operator_context = {}

	_live_operator_description = _(
		# Translators: Script description for 'Starts or ends a live voice conversation with the AI Operator in control of the computer.' in Input Gestures dialog.
		"Starts or ends a live voice conversation with the AI Operator in control of the computer.",
	)

	# Translators: Error message shown when uploading a video file fails.
	current_status = _("Idle")

	def __init__(self):
		super(GlobalPlugin, self).__init__()

		plugin_state.plugin_instance = self
		log.info("Vision Assistant loaded")

		try:
			check_and_restore_lib_backup()
		except Exception as be:
			log.warning(f"Lib restore schedule skipped: {be}")

		try:
			from .utils.logging_utils import setup_file_logging

			setup_file_logging()
		except Exception as le:
			log.warning(f"Failed to initialize file logging: {le}")

		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SettingsPanel)
			self.updater = UpdateManager(GITHUB_REPO)
			self._is_operator_running = False
			self._abort_operator = False
			self._operator_thread_token = 0
			self._dialog_open = False
			self.va_menu = wx.Menu()

			# Translators: Menu item for Document Reader
			item_doc = self.va_menu.Append(wx.ID_ANY, _("&Document Reader..."))
			self.va_menu.Bind(
				wx.EVT_MENU,
				lambda e: wx.CallAfter(self._open_document_reader_with_recent),
				item_doc,
			)

			# Translators: Menu item for Direct Chat dialog
			item_chat = self.va_menu.Append(wx.ID_ANY, _("Direct &Chat..."))
			self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_direct_chat_dialog), item_chat)

			# Translators: Menu item for media transcription and dubbing
			item_audio = self.va_menu.Append(wx.ID_ANY, _("Media Transcription and &Dubbing..."))
			self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_audio), item_audio)

			# Translators: Menu item for Video Analysis
			item_video = self.va_menu.Append(wx.ID_ANY, _("Analyze &Video..."))
			self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_video_dialog), item_video)

			self.va_menu.AppendSeparator()

			# Translators: Menu item to start or stop the Live Assistant
			item_live = self.va_menu.Append(wx.ID_ANY, _("&Live Assistant"))
			self.va_menu.Bind(wx.EVT_MENU, self.on_live_assistant_click, item_live)

			# Translators: Menu item to start or stop the live voice conversation with the AI Operator
			item_operator = self.va_menu.Append(wx.ID_ANY, _("AI &Operator (Live)"))
			self.va_menu.Bind(wx.EVT_MENU, self.on_live_operator_click, item_operator)

			# Translators: Menu item to start or stop the Ambient Observer background assistant
			item_ambient = self.va_menu.Append(wx.ID_ANY, _("A&mbient Observer"))
			self.va_menu.Bind(wx.EVT_MENU, self.on_ambient_observer_click, item_ambient)

			# Translators: Menu item for the Gemini API keys manager
			item_keys = self.va_menu.Append(wx.ID_ANY, _("Gemini API Key &Manager..."))
			self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_gemini_keys_dialog), item_keys)

			self.va_menu.AppendSeparator()

			# Translators: Menu item to open settings
			item_settings = self.va_menu.Append(wx.ID_ANY, _("&Settings..."))
			self.va_menu.Bind(wx.EVT_MENU, self.on_settings_click, item_settings)

			# Translators: Menu item to check for updates
			item_update = self.va_menu.Append(wx.ID_ANY, _("Check for &Update"))
			self.va_menu.Bind(
				wx.EVT_MENU,
				lambda e: self.updater.check_for_updates(silent=False),
				item_update,
			)

			# Translators: Menu item to open documentation
			item_help = self.va_menu.Append(wx.ID_ANY, _("Docu&mentation"))
			self.va_menu.Bind(wx.EVT_MENU, self.on_help_click, item_help)

			# Translators: Menu item for donations
			item_donate = self.va_menu.Append(wx.ID_ANY, _("D&onate"))
			self.va_menu.Bind(wx.EVT_MENU, self.on_donate_click, item_donate)

			# Translators: Menu item to open the Telegram channel
			item_telegram = self.va_menu.Append(wx.ID_ANY, _("Telegram &Channel"))
			self.va_menu.Bind(wx.EVT_MENU, self.on_telegram_click, item_telegram)

			self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
			# Translators: The name of the addon's sub-menu in the NVDA Tools menu.
			self.va_submenu_item = self.tools_menu.AppendSubMenu(self.va_menu, _("Vision Assistant"))

			if nvda_config.conf["VisionAssistant"]["check_update_startup"]:
				self.update_timer = wx.CallLater(10000, self.updater.check_for_updates, True)

			self.announcement_timer = wx.CallLater(7000, AnnouncementManager.check_announcements)

		self.refine_dlg = None
		self.refine_menu_dlg = None
		self.vision_dlg = None
		self.doc_dlg = None
		self.doc_viewer_dlg = None
		self.translation_dlg = None
		self.toggling = False
		self._last_result_data = None
		self.live_session = None
		self.live_dlg = None
		self.ambient_observer = None
		self.ambient_menu_dlg = None
		self._live_history = ""
		self._last_live_history = ""

		self.is_video_recording = False
		self.recording_process = None
		self.recording_output_path = None
		self.recording_start_time = None

		self.labels_cache = {}
		if os.path.exists(LABELS_FILE):
			try:
				with open(LABELS_FILE, "r", encoding="utf-8") as f:
					self.labels_cache = json.load(f)
			except Exception as e:
				log.debug(f"Labels cache load failed: {e}")

		self._ocr_task_running = {"smartfile": False, "document": False}
		self._ocr_abort = {"smartfile": False, "document": False}

		self._register_custom_prompt_scripts()
		self.bindGestures(self._custom_prompt_normal_gestures)

	def getScript(self, gesture):
		if not self.toggling:
			return super(GlobalPlugin, self).getScript(gesture)

		script = super(GlobalPlugin, self).getScript(gesture)
		if getattr(script, "keep_layer_alive", False):
			return script
		if not script:
			script = finally_(self.script_error, self.finish)
		return finally_(script, self.finish)

	def finish(self):
		self.toggling = False
		self._quick_settings_idx = 0
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		self.bindGestures(getattr(self, "_custom_prompt_normal_gestures", {}))

	def script_error(self, gesture):
		tones.beep(120, 100)

	@scriptHandler.script(
		# Translators: Script description for 'Shows a list of available commands in the layer.' in Input Gestures dialog.
		description=_("Shows a list of available commands in the layer."),
		category=ADDON_NAME,
	)
	def script_showHelp(self, gesture):
		if self.toggling:
			self.finish()
		help_entries = [
			# Translators: Command layer help description for Shift+A (AI Operator).
			("Shift+A", _("Asks the AI Operator to perform an action or describe the screen.")),
			# Translators: Command layer help description for E (interactive UI explorer).
			("E", _("Toggles the interactive UI elements explorer.")),
			# Translators: Command layer help description for T (translate selection or navigator object).
			("T", _("Translates the selected text or navigator object.")),
			# Translators: Command layer help description for Shift+T (translate clipboard text).
			("Shift+T", _("Translates the text currently in the clipboard.")),
			# Translators: Command layer help description for Control+T (voice dictation with translation).
			("Control+T", _("Records voice, transcribes and translates it using AI, and types the result.")),
			# Translators: Command layer help description for R (explain, summarize, or fix text).
			("R", _("Opens a menu to Explain, Summarize, or Fix the selected text.")),
			# Translators: Command layer help description for O (describe screen and read text).
			("O", _("Describes the entire screen and reads its text.")),
			# Translators: Command layer help description for V (describe navigator object).
			("V", _("Describes the current object (Navigator Object).")),
			# Translators: Command layer help description for D (document reader).
			("D", _("Opens the Document Reader for detailed page-by-page analysis (PDF/Images).")),
			# Translators: Command layer help description for F (smart file actions).
			("F", _("Performs smart actions (OCR or Description) on a selected image or PDF file.")),
			# Translators: Command layer help description for M (media transcription and dubbing).
			("M", _("Transcribes or dubs a selected media file.")),
			# Translators: Command layer help description for Shift+V (video analysis).
			("Shift+V", _("Analyzes a local video file or an online video URL.")),
			# Translators: Command layer help description for Control+V (screen video recording).
			("Control+V", _("Starts or stops local video recording of the screen.")),
			# Translators: Command layer help description for C (CAPTCHA solving).
			("C", _("Attempts to solve a CAPTCHA on the screen or navigator object.")),
			# Translators: Command layer help description for Shift+C (open chat dialog).
			("Shift+C", _("Opens a chat dialog to directly prompt the AI with text or files.")),
			# Translators: Command layer help description for S (voice dictation).
			("S", _("Records voice, transcribes it using AI, and types the result.")),
			# Translators: Command layer help description for I (announce status).
			("I", _("Announces the current status of the add-on.")),
			# Translators: Command layer help description for L (label navigator object).
			("L", _("Labels the current navigator object using AI.")),
			# Translators: Command layer help description for Shift+L (manage element labels).
			("Shift+L", _("Manages existing labels or scans the entire app to label unnamed elements.")),
			# Translators: Command layer help description for U (manual update check).
			("U", _("Checks for updates manually.")),
			# Translators: Command layer help description for Space (show last AI response).
			("Space", _("Shows the last AI response in a chat dialog for review or follow-up questions.")),
			# Translators: Command layer help description for H (layer help commands list).
			("H", _("Shows a list of available commands in the layer.")),
			# Translators: Command layer help description for Control+H (history dialog).
			("Control+H", _("Opens the History dialog to review past chats and documents.")),
			# Translators: Command layer help description for Shift+O (Ambient Observer).
			("Shift+O", _("Starts or stops the Ambient Observer background assistant.")),
			# Translators: Command layer help description for Control+L (Live Assistant).
			("Control+L", _("Starts or ends a live voice conversation with the AI assistant.")),
			("Control+A", self._live_operator_description),
			# Translators: Command layer help description for Alt+S (settings dialog).
			("Alt+S", _("Opens the Vision Assistant settings dialog.")),
			# Translators: Command layer help description for G (Gemini API key manager).
			("G", _("Opens the Gemini API key manager when the Gemini provider is active.")),
			(
				"Alt+Q",
				_(
					# Translators: Command layer help description for Alt+Q (exhausted API keys report).
					"Reports the number of Gemini API keys that have exceeded their daily quota and their reset time."
				),
			),
			# Translators: Command layer help description for Alt+M (advanced routing models report).
			("Alt+M", _("Reports the AI models selected in advanced routing.")),
		]
		help_msg = "\n".join(f"{key}: {desc}" for key, desc in help_entries)
		custom_prompt_shortcuts = getattr(self, "_custom_prompt_layer_info", [])
		if custom_prompt_shortcuts:
			# Translators: Section header in the command layer help listing custom prompt shortcuts.
			help_msg += "\n\n" + _("Custom Prompts:") + "\n"
			for hotkey, prompt_name in custom_prompt_shortcuts:
				help_msg += "%s: %s\n" % (_format_hotkey_display(hotkey), prompt_name)
		# Translators: Title of the help dialog
		ui.browseableMessage(help_msg, _("{name} Help").format(name=ADDON_NAME))

	@scriptHandler.script(description=_("Announces the current status of the add-on."), category=ADDON_NAME)
	def script_announceStatus(self, gesture):
		if self.toggling:
			self.finish()
		idle_msg = _("Idle")
		msg = self.current_status if self.current_status else idle_msg
		ui.message(msg)

	@scriptHandler.script(
		description=_("Starts or ends a live voice conversation with the AI assistant."),
		category=ADDON_NAME,
	)
	def script_toggleLiveAssistant(self, gesture):
		if self.toggling:
			self.finish()
		if self.live_session:
			self._end_live_session()
			return
		if not AIHandler.is_gemini():
			show_error_dialog(
				_(
					# Translators: Error shown when the Live Assistant is used with a non-Gemini provider.
					"The Live Assistant is only supported with the Gemini provider (or a Custom provider with API type set to Gemini).",
				),
			)
			return
		self._start_live_session()

	@scriptHandler.script(description=_live_operator_description, category=ADDON_NAME)
	def script_startLiveOperator(self, gesture):
		if self.toggling:
			self.finish()
		if self.live_session:
			self._end_live_session()
			return
		if not AIHandler.is_gemini():
			show_error_dialog(
				_(
					# Translators: Error shown when the Live Assistant is used with a non-Gemini provider.
					"The Live Assistant is only supported with the Gemini provider (or a Custom provider with API type set to Gemini).",
				),
			)
			return
		self._start_live_session(operator=True)

	@scriptHandler.script(
		description=_("Starts or stops the Ambient Observer background assistant."),
		category=ADDON_NAME,
	)
	def script_toggleAmbientObserver(self, gesture):
		if self.toggling:
			self.finish()
		if self.ambient_menu_dlg:
			self.ambient_menu_dlg.Raise()
			self.ambient_menu_dlg.SetFocus()
			return
		if self.ambient_observer:
			wx.CallLater(100, self._stop_ambient_observer)
			return
		if not AIHandler.is_gemini():
			show_error_dialog(
				_(
					# Translators: Error shown when the Ambient Observer is used with a non-Gemini provider.
					"The Ambient Observer is only supported with the Gemini provider (or a Custom provider with API type set to Gemini).",
				),
			)
			return
		wx.CallLater(100, self._show_ambient_observer_menu)

	def _ambient_mode_label(self, mode):
		return next((label for key, label in AMBIENT_MODE_LIST if key == mode), mode)

	def _start_webcam_live_session(self, context=None, use_ptt=None):
		if self.live_session or not AIHandler.is_gemini():
			return
		context_text = context_instruction(MODE_WEBCAM, context)
		self._start_live_session(webcam=True, push_to_talk=use_ptt, context=context_text)

	def _start_ambient_observer(
		self, mode, target_code=None, context=None, audio_source=None, use_ptt=None, style=None
	):
		if self.ambient_observer:
			return
		if mode == MODE_WEBCAM:
			self._start_webcam_live_session(context, use_ptt)
			return
		observer = AmbientObserver(
			status_callback=lambda msg: wx.CallAfter(self._ambient_status, msg),
			text_callback=lambda line: logging_utils.log_addon(logging.DEBUG, f"Ambient Observer: {line}"),
			closed_callback=lambda: wx.CallAfter(self._ambient_on_closed),
			capture_fullscreen=self._capture_fullscreen,
			capture_window=self._capture_foreground,
		)
		self.ambient_observer = observer
		threading.Thread(
			target=self._start_ambient_worker,
			args=(observer, mode, target_code, context, audio_source, style),
			daemon=True,
		).start()

	def _start_ambient_worker(self, observer, mode, target_code, context, audio_source=None, style=None):
		try:
			started = observer.start(mode, target_code, context, audio_source=audio_source, style=style)
		except Exception as e:
			log.error(f"Ambient Observer start failed: {e}", exc_info=True)
			started = False
		if started:
			wx.CallAfter(self._ambient_started, observer, mode)
		else:
			wx.CallAfter(self._ambient_failed, observer)

	def _ambient_started(self, observer, mode):
		if self.ambient_observer is not observer:
			return
		tones.beep(660, 120)
		# Translators: Message announced when the Ambient Observer starts. {mode} is the name of the selected observer mode.
		self.report_status(_("Observer started: {mode}").format(mode=self._ambient_mode_label(mode)))

	def _ambient_failed(self, observer):
		if self.ambient_observer is observer:
			self.ambient_observer = None
		try:
			observer.stop()
		except Exception as e:
			log.debug(f"Ambient Observer cleanup failed: {e}")
		tones.beep(220, 120)

	def _stop_ambient_observer(self):
		observer = self.ambient_observer
		self.ambient_observer = None
		if not observer:
			return
		tones.beep(440, 120)
		# Translators: Status when no operation is running.
		self.current_status = _("Idle")
		# Translators: Message announced when the Ambient Observer is stopped.
		plugin_state.speak_status(_("Observer stopped."))
		threading.Thread(target=observer.stop, daemon=True).start()

	def _ambient_on_closed(self):
		if not self.ambient_observer:
			return
		self.ambient_observer = None
		tones.beep(440, 120)
		# Translators: Status when no operation is running.
		self.current_status = _("Idle")
		# Translators: Message announced when the Ambient Observer session ends on its own.
		plugin_state.speak_status(_("Observer stopped."))

	def _ambient_status(self, msg):
		if is_ai_error(msg):
			show_error_dialog(ai_error_message(msg))
			self._stop_ambient_observer()
		elif msg.startswith("STATUS:"):
			self.report_status(msg[7:])

	def _handle_ambient_custom_prompt(self, prompt_content):
		if self.ambient_observer:
			wx.CallLater(100, self._stop_ambient_observer)
			return
		if getattr(self, "live_session", None):
			wx.CallLater(100, self._end_live_session)
			return
		if getattr(self, "ambient_menu_dlg", None):
			self.ambient_menu_dlg.Raise()
			self.ambient_menu_dlg.SetFocus()
			return
		if not AIHandler.is_gemini():
			show_error_dialog(
				_(
					# Translators: Error shown when the Ambient Observer is used with a non-Gemini provider.
					"The Ambient Observer is only supported with the Gemini provider (or a Custom provider with API type set to Gemini).",
				),
			)
			return
		params = parse_ambient_prompt(prompt_content)
		mode = params.get("mode")
		if not mode:
			return
		audio_source = params.get("audio_source")
		target_code = params.get("target_code")
		style = params.get("style")
		context = params.get("context")
		use_ptt = params.get("use_ptt")
		self._start_ambient_observer(
			mode,
			target_code=target_code,
			context=context,
			audio_source=audio_source,
			use_ptt=use_ptt,
			style=style,
		)

	def _available_ambient_modes(self):
		devices = getattr(self, "_webcam_devices", None)
		return [(key, label) for key, label in AMBIENT_MODE_LIST if key != MODE_WEBCAM or devices]

	def _check_webcam_for_menu(self):
		devices = []
		ffmpeg_path = None
		try:
			ffmpeg_path = find_ffmpeg_silent()
			if ffmpeg_path:
				devices = enumerate_webcams(ffmpeg_path)
		except Exception as e:
			log.debug(f"Ambient webcam availability check failed: {e}")
		self._webcam_devices = devices
		self._webcam_ffmpeg_path = ffmpeg_path
		wx.CallAfter(self._open_ambient_start_dialog)

	def _show_ambient_observer_menu(self):
		if getattr(self, "_webcam_devices", None) is None:
			threading.Thread(target=self._check_webcam_for_menu, daemon=True).start()
			return
		self._open_ambient_start_dialog()

	def _open_ambient_start_dialog(self):
		conf = nvda_config.conf["VisionAssistant"]
		settings = None
		dlg = None
		gui.mainFrame.prePopup()
		try:
			initial_mode = conf.get("ambient_observer_mode", MODE_AUDIO)
			if initial_mode == "webcam":
				initial_context = conf.get("ambient_webcam_context", conf.get("ambient_context", "general"))
			else:
				initial_context = conf.get("ambient_context", "general")
			dlg = AmbientStartDialog(
				gui.mainFrame,
				self._available_ambient_modes(),
				initial_mode=initial_mode,
				initial_context=initial_context,
				initial_audio_source=conf.get("ambient_audio_source", "system"),
				initial_ptt=bool(conf.get("live_push_to_talk", False)),
				initial_style=conf.get("ambient_reporting_style", "brief"),
			)
			self.ambient_menu_dlg = dlg
			dlg.Raise()
			dlg.SetFocus()
			if dlg.ShowModal() == wx.ID_OK:
				settings = dlg.get_settings()
		except Exception as e:
			log.debug(f"Ambient start dialog failed: {e}")
		finally:
			gui.mainFrame.postPopup()
			self.ambient_menu_dlg = None
			if dlg:
				try:
					dlg.Destroy()
				except Exception as e:
					log.debug(f"Ambient start dialog destroy failed: {e}")
		if not settings:
			return
		mode, target_code, context, audio_source, use_ptt, style = settings
		try:
			conf["ambient_observer_mode"] = mode
			conf["ambient_audio_source"] = audio_source
			conf["ambient_reporting_style"] = style
			if mode == "webcam":
				conf["ambient_webcam_context"] = context
				conf["live_push_to_talk"] = use_ptt
			else:
				conf["ambient_context"] = context
		except Exception as e:
			log.debug(f"Ambient settings save failed: {e}")
		self._start_ambient_observer(mode, target_code, context, audio_source, use_ptt, style)

	@scriptHandler.script(description=_("Opens the Vision Assistant settings dialog."), category=ADDON_NAME)
	def script_openSettings(self, gesture):
		if self.toggling:
			self.finish()
		wx.CallAfter(self.on_settings_click, None)

	@scriptHandler.script(
		# Translators: Script description for 'Opens the History dialog to review past chats and documents.' in Input Gestures dialog.
		description=_("Opens the History dialog to review past chats and documents."),
		category=ADDON_NAME,
	)
	def script_openHistory(self, gesture):
		if self.toggling:
			self.finish()
		wx.CallAfter(self._open_history_dialog)

	def _open_history_dialog(self):
		dlg = getattr(self, "_history_dlg", None)
		if dlg:
			try:
				dlg.Raise()
				dlg.SetFocus()
				return
			except Exception:
				pass
		from .dialogs.history_dialog import HistoryDialog
		from .utils.storage import HistoryStore

		store = HistoryStore(HISTORY_FILE)
		self._history_dlg = HistoryDialog(
			gui.mainFrame,
			store,
			on_open_chat=self._open_chat_from_history,
			on_open_document=self._open_document_from_history,
		)
		self._history_dlg.Show()
		self._history_dlg.Raise()

	def _open_chat_from_history(self, item):
		data = item.get("data") or {}
		self._last_chat_history = data.get("history", [])
		self._last_chat_attachments = data.get("attachments", [])
		self._last_chat_id = item.get("id")
		self._open_direct_chat_dialog(is_recall=True)

	def _open_document_from_history(self, item):
		data = item.get("data") or {}
		paths = data.get("paths") or []
		if not paths:
			return
		start_at = data.get("current_page")
		threading.Thread(
			target=self._scan_and_open,
			args=(paths,),
			kwargs={"start_at": start_at},
			daemon=True,
		).start()

	# Translators: Script description for 'Checks for updates manually.' in Input Gestures dialog.
	@scriptHandler.script(description=_("Checks for updates manually."), category=ADDON_NAME)
	def script_checkUpdate(self, gesture):
		if self.toggling:
			self.finish()
		# Translators: Message reported when calling the update command
		msg = _("Checking for updates...")
		self.report_status(msg)
		self.updater.check_for_updates(silent=False)

	@scriptHandler.script(
		description=_(
			# Translators: Script description for 'Reports the number of Gemini API keys that have exceeded their daily quota and their reset time.' in Input Gestures dialog.
			"Reports the number of Gemini API keys that have exceeded their daily quota and their reset time.",
		),
		category=ADDON_NAME,
	)
	def script_reportQuotaExhaustedKeys(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		if not AIHandler.is_gemini():
			# Translators: Message shown when a user tries to check Gemini API quotas but another provider is active.
			core.callLater(0, ui.message, _("This feature is only available for Google Gemini."))
			return
		try:
			banned_str = nvda_config.conf["VisionAssistant"].get("banned_gemini_keys", "{}")
			banned = json.loads(banned_str)
		except Exception as e:
			log.warning(f"Parse banned keys failed: {e}")
			banned = {}
		now = time.time()
		unique_keys = {}
		max_time_per_key = {}
		for k_m, ban_time in list(banned.items()):
			if now < ban_time:
				parts = k_m.split("::")
				k = parts[0]
				m = parts[1] if len(parts) > 1 else "Unknown"
				if k not in unique_keys:
					unique_keys[k] = []
				unique_keys[k].append(m)
				max_time_per_key[k] = max(max_time_per_key.get(k, 0), ban_time)
			else:
				del banned[k_m]
		nvda_config.conf["VisionAssistant"]["banned_gemini_keys"] = json.dumps(banned)
		if not unique_keys:
			# Translators: Message when no API keys are out of quota
			ui.message(_("No API keys have exceeded their daily quota."))
			return
		today = datetime.date.today()
		msg_parts = []
		for k, models in unique_keys.items():
			models.sort()
			max_time = max_time_per_key[k]
			model_str = ", ".join(models)
			ban_date = datetime.datetime.fromtimestamp(max_time).date()
			time_str = time.strftime("%H:%M", time.localtime(max_time))
			if ban_date > today:
				# Translators: Reset time string when key quota resets on the next day. {time} is the formatted time (e.g. 14:30).
				time_str = _("tomorrow at {time}").format(time=time_str)
			# Translators: Shows detailed information for a banned API key. {key} is the API key, {model} is the model name, {time_str} is the reset time.
			key_info = _("Key: {key}\nModel: {model}\nResets around: {time_str}\n").format(
				key=k,
				model=model_str,
				time_str=time_str,
			)
			msg_parts.append(key_info)
		model_counts = {}
		for models in unique_keys.values():
			for m in models:
				model_counts[m] = model_counts.get(m, 0) + 1
		summary_parts = []
		for m, count in model_counts.items():
			# Translators: Shows how many API keys have exceeded their quota for a specific model. {count} is the number of keys, {model} is the model name.
			summary_parts.append(_("{count} keys for model {model}").format(count=count, model=m))
		# Translators: Message shown when API keys run out of quota.
		summary_msg = ", ".join(summary_parts) + " " + _("have exceeded their daily quota.")
		final_msg = summary_msg + "\n\n" + "\n".join(msg_parts).strip()
		# Translators: Title of the browseable message dialog showing exhausted API keys
		ui.browseableMessage(final_msg, _("Exhausted API Keys"))

	@scriptHandler.script(
		# Translators: Script description for 'Reports the AI models selected in advanced routing.' in Input Gestures dialog.
		description=_("Reports the AI models selected in advanced routing."),
		category=ADDON_NAME,
	)
	def script_reportSelectedModels(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		models = []
		conf = nvda_config.conf["VisionAssistant"]
		p = conf.get("active_provider", "gemini")
		m_key = provider_model_name(p)
		main_m = conf.get(m_key, "")
		if main_m:
			# Translators: Spoken status reporting the active primary model in advanced routing. {model} is the AI model name.
			models.append(_("Main: {model}").format(model=main_m))

		def add_adv(task, name):
			m = conf.get(f"{p}_{task}_model", "")
			if m and "Default" not in m and "Auto" not in m:
				models.append(f"{name}: {m}")

		# Translators: Advanced routing label for Optical Character Recognition.
		add_adv("ocr", _("OCR"))
		# Translators: Advanced routing label for Speech-to-Text.
		add_adv("stt", _("STT"))
		# Translators: Advanced routing label for Text-to-Speech.
		add_adv("tts", _("TTS"))
		# Translators: Advanced routing label for AI Operator model.
		add_adv("operator", _("Operator"))
		# Translators: Advanced routing label for video analysis model.
		add_adv("video", _("Video"))
		# Translators: Advanced routing label for live voice assistant model.
		add_adv("live", _("Live"))
		if not models:
			# Translators: Message announced when advanced routing has no custom task models selected.
			ui.message(_("No specific models selected."))
		else:
			ui.message(". ".join(models))

	def terminate(self):
		try:
			if not globalVars.appArgs.secure:
				if hasattr(self, "va_submenu_item") and self.va_submenu_item:
					self.tools_menu.Remove(self.va_submenu_item.GetId())

			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsPanel)

		except Exception as e:
			log.debug(f"Settings panel remove failed: {e}")

		if hasattr(self, "update_timer") and self.update_timer and self.update_timer.IsRunning():
			self.update_timer.Stop()

		self._abort_operator = True
		self._is_operator_running = False
		self._operator_thread_token = getattr(self, "_operator_thread_token", 0) + 1

		if self.live_session:
			try:
				self.live_session.stop()
			except Exception as e:
				log.debug(f"Live session stop failed: {e}")
			self.live_session = None

		if self.ambient_observer:
			try:
				self.ambient_observer.stop()
			except Exception as e:
				log.debug(f"Ambient Observer stop failed: {e}")
			self.ambient_observer = None

		for dlg in [
			self.refine_dlg,
			self.refine_menu_dlg,
			self.ambient_menu_dlg,
			self.vision_dlg,
			self.doc_dlg,
			self.doc_viewer_dlg,
			self.translation_dlg,
		]:
			if dlg:
				try:
					if getattr(dlg, "abort", None) is not None:
						dlg.abort = True
					dlg.Destroy()
				except Exception as e:
					log.debug(f"Dialog abort/destroy failed: {e}")

		if self.is_recording:
			try:
				ctypes.windll.winmm.mciSendStringW("close all", None, 0, 0)
			except Exception as e:
				log.debug(f"MCI close all failed: {e}")

		self.translation_cache = {}
		self._last_source_text = None
		plugin_state.plugin_instance = None
		for fpath in getattr(self, "_temp_files_to_cleanup", []):
			try:
				if os.path.exists(fpath):
					os.remove(fpath)
			except Exception as e:
				log.debug(f"Temp file removal failed: {e}")
		self._temp_files_to_cleanup = []
		gc.collect()

	def report_status(self, msg):
		self.current_status = msg
		plugin_state.speak_status(msg)

	@scriptHandler.script(
		# Translators: Script description for 'Activates the Command Layer for quick access to all features.' in Input Gestures dialog.
		description=_("Activates the Command Layer for quick access to all features."),
		category=ADDON_NAME,
	)
	def script_activateLayer(self, gesture):
		if globalVars.appArgs.secure:
			return

		if self.toggling:
			self.script_error(gesture)
			return

		self.clearGestureBindings()
		self.bindGestures(self._build_layer_gestures())
		self.bindGestures(self.__gestures)
		self.toggling = True
		tones.beep(500, 100)

	def _build_layer_gestures(self):
		gestures = dict(self.__VisionGestures)
		for gesture_id, script_name in getattr(self, "_custom_prompt_layer_gestures", {}).items():
			if gesture_id not in gestures:
				gestures[gesture_id] = script_name
		return gestures

	def _make_custom_prompt_script(self, prompt_name, content, script_name, feedback_behavior="global"):
		# Translators: Script description in Input Gestures for a shortcut that runs a custom prompt. {name} is the prompt name.
		description = _('Runs the custom prompt "{name}".').format(name=prompt_name)

		def make(prompt_content, behavior):
			def script(self, gesture):
				if self.toggling:
					self.finish()
				captured_text = self._get_text_smart()
				if not captured_text:
					captured_text = ""
				captured_url = self._get_current_document_url()
				captured_edit_text = self._get_focused_edit_text()
				wx.CallLater(
					100,
					self._run_refine_prompt,
					captured_text,
					prompt_content,
					behavior,
					captured_url,
					captured_edit_text,
				)

			script.__name__ = "script_" + script_name
			return scriptHandler.script(description=description, category=ADDON_NAME)(script)

		return make(content, feedback_behavior)

	def _register_custom_prompt_scripts(self):
		items = load_configured_custom_prompts()
		self._custom_prompt_script_names = []
		self._custom_prompt_layer_gestures = {}
		self._custom_prompt_normal_gestures = {}
		self._custom_prompt_layer_info = []
		for item in items:
			hotkey = (item.get("hotkey") or "").strip().lower()
			if not hotkey:
				continue
			script_name = "customPrompt_" + hotkey.replace("+", "_")
			self._custom_prompt_script_names.append(script_name)
			layer_id = "kb:" + hotkey
			self._custom_prompt_layer_gestures[layer_id] = script_name
			if "+" in hotkey:
				self._custom_prompt_normal_gestures[layer_id] = script_name
			else:
				self._custom_prompt_normal_gestures["kb:nvda+shift+" + hotkey] = script_name
			self._custom_prompt_layer_info.append((hotkey, item.get("name", "")))
			setattr(
				type(self),
				"script_" + script_name,
				self._make_custom_prompt_script(
					item.get("name", ""),
					item.get("content", ""),
					script_name,
					feedback_behavior=item.get("feedback_behavior", "global"),
				),
			)

	def _refresh_custom_prompt_scripts(self):
		try:
			for script_name in getattr(self, "_custom_prompt_script_names", []):
				try:
					delattr(type(self), "script_" + script_name)
				except Exception:
					pass
			self._register_custom_prompt_scripts()
			self.clearGestureBindings()
			self.bindGestures(self.__gestures)
			self.bindGestures(getattr(self, "_custom_prompt_normal_gestures", {}))
			if self.toggling:
				self.bindGestures(self._build_layer_gestures())
		except Exception as e:
			log.warning("Failed to refresh custom prompt shortcuts: %s" % e)

	def on_settings_click(self, event):
		instance = getattr(gui.settingsDialogs.NVDASettingsDialog, "instance", None)
		if instance:
			try:
				instance.Show(True)
				instance.Raise()
				instance.SetFocus()
				if hasattr(instance, "setPanel"):
					instance.setPanel(SettingsPanel)
				return
			except Exception:
				gui.settingsDialogs.NVDASettingsDialog.instance = None

		def _force_open():
			gui.settingsDialogs.NVDASettingsDialog.instance = None
			try:
				gui.mainFrame.prePopup()
				new_inst = gui.settingsDialogs.NVDASettingsDialog(gui.mainFrame, SettingsPanel)
				new_inst.Show()
				new_inst.Raise()
				gui.mainFrame.postPopup()
			except Exception:
				gui.settingsDialogs.NVDASettingsDialog.instance = None
				try:
					gui.mainFrame.postPopup()
				except Exception:
					pass

		wx.CallLater(100, _force_open)

	def on_help_click(self, event):
		try:
			addon = addonHandler.getCodeAddon()
			doc_path = addon.getDocFilePath() if addon else None
			if not (doc_path and os.path.isfile(doc_path)) and addon:
				en_path = os.path.join(addon.path, "doc", "en", "readme.html")
				if os.path.isfile(en_path):
					doc_path = en_path
			if doc_path and os.path.isfile(doc_path):
				os.startfile(doc_path)
			else:
				# Translators: Error message shown when documentation file cannot be found.
				show_error_dialog(_("Documentation file not found."))
		except Exception as e:
			show_error_dialog(str(e))

	def on_donate_click(self, event):
		try:
			wx.CallAfter(donate.requestDonations, gui.mainFrame)
		except Exception as e:
			show_error_dialog(str(e))

	def on_telegram_click(self, event):
		try:
			os.startfile("https://t.me/VisionAssistantPro")
		except Exception as e:
			show_error_dialog(str(e))

	def on_live_assistant_click(self, event):
		wx.CallAfter(self.script_toggleLiveAssistant, None)

	def on_live_operator_click(self, event):
		wx.CallAfter(self.script_startLiveOperator, None)

	def on_ambient_observer_click(self, event):
		wx.CallAfter(self.script_toggleAmbientObserver, None)

	@scriptHandler.script(
		# Translators: Script description for 'Opens the Gemini API key manager when the Gemini provider is active.' in Input Gestures dialog.
		description=_("Opens the Gemini API key manager when the Gemini provider is active."),
		category=ADDON_NAME,
	)
	def script_openGeminiKeys(self, gesture):
		if self.toggling:
			self.finish()
		wx.CallAfter(self._open_gemini_keys_dialog)

	def _open_gemini_keys_dialog(self):
		try:
			from .dialogs.gemini_keys import GeminiKeysDialog, gemini_manager_message
		except Exception as e:
			show_error_dialog(str(e))
			return
		if not is_gemini_provider(strict=True):
			show_error_dialog(gemini_manager_message())
			return
		gui.mainFrame.prePopup()
		try:
			dlg = GeminiKeysDialog(gui.mainFrame)
			dlg.ShowModal()
			dlg.Destroy()
		except Exception as e:
			log.debug(f"Gemini API keys dialog failed: {e}")
			show_error_dialog(str(e))
		finally:
			gui.mainFrame.postPopup()

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if not hasattr(self, "labels_cache"):
			return
		app_module = getattr(obj, "appModule", None)
		if not app_module:
			return
		app_name = app_module.appName.lower()
		if app_name in ["chrome", "msedge", "firefox", "opera", "brave"]:
			return

		class_name = getattr(obj, "windowClassName", None)
		if class_name == "Internet Explorer_Server":
			return

		uniqueId = self._getAppId(obj)
		if uniqueId not in self.labels_cache:
			return

		key = _generate_object_signature(obj)
		if key and key in self.labels_cache[uniqueId]:
			clsList.insert(0, CustomLabelOverlay)
			return

	def _getAppId(self, obj):
		try:
			appName = obj.appModule.appName.lower()
		except Exception:
			appName = "unknown_app"

		if appName == "applicationframehost":
			try:
				fg = api.getForegroundObject()
				if fg and fg.name:
					return f"{appName}_{fg.name}"
			except Exception as e:
				log.debug(f"Foreground object name get failed: {e}")
		return appName

	__gestures = {
		"kb:NVDA+shift+v": "activateLayer",
	}

	__VisionGestures = {
		"kb:t": "translateSmart",
		"kb:r": "refineText",
		"kb:o": "analyzeFullScreen",
		"kb:v": "describeObject",
		"kb:d": "analyzeDocument",
		"kb:f": "smartFileAction",
		"kb:m": "mediaTranscriber",
		"kb:c": "solveCaptcha",
		"kb:shift+c": "openDirectChat",
		"kb:i": "announceStatus",
		"kb:s": "smartDictation",
		"kb:u": "checkUpdate",
		"kb:shift+t": "translateClipboard",
		"kb:shift+v": "analyzeOnlineVideo",
		"kb:control+v": "recordLocalVideo",
		"kb:space": "showLastResult",
		"kb:h": "showHelp",
		"kb:e": "toggleUIExplorer",
		"kb:shift+a": "aiOperatorAction",
		"kb:l": "labelObject",
		"kb:shift+l": "manageOrScanApp",
		"kb:control+a": "startLiveOperator",
		"kb:control+l": "toggleLiveAssistant",
		"kb:shift+o": "toggleAmbientObserver",
		"kb:alt+s": "openSettings",
		"kb:alt+q": "reportQuotaExhaustedKeys",
		"kb:alt+m": "reportSelectedModels",
		"kb:downArrow": "layerDown",
		"kb:upArrow": "layerUp",
		"kb:rightArrow": "layerRight",
		"kb:leftArrow": "layerLeft",
		"kb:control+t": "voiceTranslation",
		"kb:control+h": "openHistory",
		"kb:g": "openGeminiKeys",
	}
