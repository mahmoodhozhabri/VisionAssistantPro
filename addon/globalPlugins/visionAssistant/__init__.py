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
from .ai.core import AIHandler
from .utils.system import show_error_dialog, _generate_object_signature
from .vision_config import LABELS_FILE, ADDON_NAME, GITHUB_REPO, HISTORY_FILE, _migrate_data_dir
_migrate_data_dir()
from .utils.updater import UpdateManager
from .features.vision import VisionMixin
from .features.screen_capture import ScreenCaptureMixin
from .features.audio import AudioMixin
from .features.video import VideoMixin
from .features.operator_captcha import OperatorCaptchaMixin
from .features.quick_settings import QuickSettingsMixin
from .features.upload import UploadMixin
from .dialogs.settings import SettingsPanel
from .prompt_utils import finally_, load_configured_custom_prompts, _format_hotkey_display

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
            os.makedirs(target_lib_dir, exist_ok=True)

            failed = False
            for item in os.listdir(backup_dir):
                if item == "backup_manifest.json":
                    continue
                src = os.path.join(backup_dir, item)
                dst = os.path.join(target_lib_dir, item)
                if os.path.exists(dst):
                    continue
                try:
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)
                except Exception as e:
                    failed = True
                    log.warning(f"Lib backup restore failed for {item}: {e}")

            if failed:
                log.warning("Lib backup restore incomplete; keeping backup for retry on next start.")
                return
            shutil.rmtree(backup_dir, ignore_errors=True)
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


class GlobalPlugin(globalPluginHandler.GlobalPlugin, VisionMixin, ScreenCaptureMixin,
                   AudioMixin, VideoMixin, OperatorCaptchaMixin, QuickSettingsMixin, UploadMixin):

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

    # Translators: Error message shown when uploading a video file fails.
    current_status = _("Idle")

    def __init__(self):
        super(GlobalPlugin, self).__init__()

        # Migrate legacy plaintext credentials before any provider or logger can
        # consume them. Encryption errors fail closed and prevent add-on startup.
        from .utils.secure_credentials import migrate_credentials
        if migrate_credentials(nvda_config.conf["VisionAssistant"]):
            nvda_config.conf.save()

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
            self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_document_reader), item_doc)

            # Translators: Menu item for media transcription and dubbing
            item_audio = self.va_menu.Append(wx.ID_ANY, _("Media Transcription and &Dubbing..."))
            self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_audio), item_audio)

            # Translators: Menu item for Video Analysis
            item_video = self.va_menu.Append(wx.ID_ANY, _("Analyze &Video..."))
            self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_video_dialog), item_video)

            self.va_menu.AppendSeparator()

            # Translators: Menu item to open settings
            item_settings = self.va_menu.Append(wx.ID_ANY, _("&Settings..."))
            self.va_menu.Bind(wx.EVT_MENU, self.on_settings_click, item_settings)

            # Translators: Menu item to check for updates
            item_update = self.va_menu.Append(wx.ID_ANY, _("Check for &Update"))
            self.va_menu.Bind(wx.EVT_MENU, lambda e: self.updater.check_for_updates(silent=False), item_update)

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
        self._live_history = ""

        self.is_video_recording = False
        self.recording_process = None
        self.recording_output_path = None
        self.recording_start_time = None

        self.labels_cache = {}
        if os.path.exists(LABELS_FILE):
            try:
                with open(LABELS_FILE, "r", encoding="utf-8") as f:
                    self.labels_cache = json.load(f)
            except Exception as e: log.debug(f"Labels cache load failed: {e}")

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
        
    # Translators: Script description for 'Shows a list of available commands in the layer.' in Input Gestures dialog.
    @scriptHandler.script(description=_("Shows a list of available commands in the layer."), category=ADDON_NAME)
    def script_showHelp(self, gesture):
        if self.toggling: self.finish()
        help_msg = (
            "Shift+A: " + _("Asks the AI Operator to perform an action or describe the screen.") + "\n" +
            "E: " + _("Toggles the interactive UI elements explorer.") + "\n" +
            "T: " + _("Translates the selected text or navigator object.") + "\n" +
            "Shift+T: " + _("Translates the text currently in the clipboard.") + "\n" +
            "Control+T: " + _("Records voice, transcribes and translates it using AI, and types the result.") + "\n" +
            # Translators: Script description for 'Opens a menu to Explain, Summarize, or Fix the selected text.' in Input Gestures dialog.
            "R: " + _("Opens a menu to Explain, Summarize, or Fix the selected text.") + "\n" +
            # Translators: Script description for 'Performs OCR and description on the entire screen.' in Input Gestures dialog.
            "O: " + _("Performs OCR and description on the entire screen.") + "\n" +
            # Translators: Script description for 'Describes the current object (Navigator Object).' in Input Gestures dialog.
            "V: " + _("Describes the current object (Navigator Object).") + "\n" +
            # Translators: Script description for 'Opens the Document Reader for detailed page-by-page analysis (PDF/Images).' in Input Gestures dialog.
            "D: " + _("Opens the Document Reader for detailed page-by-page analysis (PDF/Images).") + "\n" +
            # Translators: Script description for 'Performs smart actions (OCR or Description) on a selected image or PDF file.' in Input Gestures dialog.
            "F: " + _("Performs smart actions (OCR or Description) on a selected image or PDF file.") + "\n" +
            # Translators: Script description for 'Transcribes or dubs a selected media file.' in Input Gestures dialog.
            "M: " + _("Transcribes or dubs a selected media file.") + "\n" +
            # Translators: Script description for 'Analyzes a local video file or an online video URL.' in Input Gestures dialog.
            "Shift+V: " + _("Analyzes a local video file or an online video URL.") + "\n" +
            # Translators: Script description for 'Starts or stops local video recording of the screen.' in Input Gestures dialog.
            "Control+V: " + _("Starts or stops local video recording of the screen.") + "\n" +
            # Translators: Script description for 'Attempts to solve a CAPTCHA on the screen or navigator object.' in Input Gestures dialog.
            "C: " + _("Attempts to solve a CAPTCHA on the screen or navigator object.") + "\n" +
            "Shift+C: " + _("Opens a chat dialog to directly prompt the AI with text or files.") + "\n" +
            # Translators: Script description for 'Records voice, transcribes it using AI, and types the result.' in Input Gestures dialog.
            "S: " + _("Records voice, transcribes it using AI, and types the result.") + "\n" +
            "I: " + _("Announces the current status of the add-on.") + "\n" +
            "L: " + _("Labels the current navigator object using AI.") + "\n" +
            "Shift+L: " + _("Manages existing labels or scans the entire app to label unnamed elements.") + "\n" +
            "U: " + _("Checks for updates manually.") + "\n" +
            # Translators: Script description for 'Shows the last AI response in a chat dialog for review or follow-up questions.' in Input Gestures dialog.
            "Space: " + _("Shows the last AI response in a chat dialog for review or follow-up questions.") + "\n" +
            "H: " + _("Shows a list of available commands in the layer.") + "\n" +
            # Translators: Script description for 'Opens the History dialog to review past chats and documents.' in Input Gestures dialog.
            "Control+H: " + _("Opens the History dialog to review past chats and documents.") + "\n" +
            # Translators: Script description for 'Starts or ends a live voice conversation with the AI assistant.' in Input Gestures dialog.
            "Control+L: " + _("Starts or ends a live voice conversation with the AI assistant.") + "\n" +
            # Translators: Script description for 'Opens the Vision Assistant settings dialog.' in Input Gestures dialog.
            "Alt+S: " + _("Opens the Vision Assistant settings dialog.") + "\n" +
            # Translators: Script description for 'Reports the number of Gemini API keys that have exceeded their daily quota and their reset time.' in Input Gestures dialog.
            "Alt+Q: " + _("Reports the number of Gemini API keys that have exceeded their daily quota and their reset time.") + "\n" +
            # Translators: Script description for 'Reports the AI models selected in advanced routing.' in Input Gestures dialog.
            "Alt+M: " + _("Reports the AI models selected in advanced routing.")
        )
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
        if self.toggling: self.finish()
        idle_msg = _("Idle")
        msg = self.current_status if self.current_status else idle_msg
        ui.message(msg)

    @scriptHandler.script(description=_("Starts or ends a live voice conversation with the AI assistant."), category=ADDON_NAME)
    def script_toggleLiveAssistant(self, gesture):
        if self.toggling: self.finish()
        if self.live_session:
            self._end_live_session()
            return
        if not AIHandler.is_gemini():
            # Translators: Error shown when the Live Assistant is used with a non-Gemini provider.
            show_error_dialog(_("The Live Assistant is only supported with the Gemini provider (or a Custom provider with API type set to Gemini)."))
            return
        self._start_live_session()

    @scriptHandler.script(description=_("Opens the Vision Assistant settings dialog."), category=ADDON_NAME)
    def script_openSettings(self, gesture):
        if self.toggling: self.finish()
        wx.CallAfter(self.on_settings_click, None)

    # Translators: Script description for 'Opens the History dialog to review past chats and documents.' in Input Gestures dialog.
    @scriptHandler.script(description=_("Opens the History dialog to review past chats and documents."), category=ADDON_NAME)
    def script_openHistory(self, gesture):
        if self.toggling: self.finish()
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
        threading.Thread(target=self._scan_and_open, args=(paths,), kwargs={"start_at": start_at}, daemon=True).start()

    # Translators: Script description for 'Checks for updates manually.' in Input Gestures dialog.
    @scriptHandler.script(description=_("Checks for updates manually."), category=ADDON_NAME)
    def script_checkUpdate(self, gesture):
        if self.toggling: self.finish()
        # Translators: Message reported when calling the update command
        msg = _("Checking for updates...")
        self.report_status(msg)
        self.updater.check_for_updates(silent=False)


    # Translators: Script description for 'Reports the number of Gemini API keys that have exceeded their daily quota and their reset time.' in Input Gestures dialog.
    @scriptHandler.script(description=_("Reports the number of Gemini API keys that have exceeded their daily quota and their reset time."), category=ADDON_NAME)
    def script_reportQuotaExhaustedKeys(self, gesture):
        if getattr(self, "toggling", False): self.finish()
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
                if k not in unique_keys: unique_keys[k] = []
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
            # Translators: Prefix for time when the daily quota resets on the next day
            if ban_date > today: time_str = _("tomorrow at {time}").format(time=time_str)
            # Translators: Shows detailed information for a banned API key fingerprint. {key} is a non-secret hash, {model} is the model name, {time_str} is the reset time.
            key_info = _("Key fingerprint: {key}\nModel: {model}\nResets around: {time_str}\n").format(key=k, model=model_str, time_str=time_str)
            msg_parts.append(key_info)
        model_counts = {}
        for models in unique_keys.values():
            for m in models: model_counts[m] = model_counts.get(m, 0) + 1
        summary_parts = []
        for m, count in model_counts.items():
            # Translators: Shows how many API keys have exceeded their quota for a specific model. {count} is the number of keys, {model} is the model name.
            summary_parts.append(_("{count} keys for model {model}").format(count=count, model=m))
        # Translators: Message shown when API keys run out of quota.
        summary_msg = ", ".join(summary_parts) + " " + _("have exceeded their daily quota.")
        final_msg = summary_msg + "\n\n" + "\n".join(msg_parts).strip()
        # Translators: Title of the browseable message dialog showing exhausted API keys
        ui.browseableMessage(final_msg, _("Exhausted API Keys"))

    # Translators: Script description for 'Reports the AI models selected in advanced routing.' in Input Gestures dialog.
    @scriptHandler.script(description=_("Reports the AI models selected in advanced routing."), category=ADDON_NAME)
    def script_reportSelectedModels(self, gesture):
        if getattr(self, "toggling", False): self.finish()
        models = []
        conf = nvda_config.conf["VisionAssistant"]
        p = conf.get("active_provider", "gemini")
        m_key = "model_name" if p == "gemini" else f"{p}_model_name"
        main_m = conf.get(m_key, "")
        # Translators: Prefix for main model status
        if main_m: models.append(_("Main: {model}").format(model=main_m))
        def add_adv(task, name):
            m = conf.get(f"{p}_{task}_model", "")
            if m and "Default" not in m and "Auto" not in m: models.append(f"{name}: {m}")
        add_adv("ocr", _("OCR"))
        # Translators: Abbreviation for Speech-to-Text.
        add_adv("stt", _("STT"))
        # Translators: Abbreviation for Text-to-Speech.
        add_adv("tts", _("TTS"))
        # Translators: Labels for the AI and User in chat history
        add_adv("operator", _("Operator"))
        add_adv("video", _("Video"))
        add_adv("live", _("Live"))
        # Translators: Message when no specific AI models are selected in advanced routing
        if not models: ui.message(_("No specific models selected."))
        else: ui.message(". ".join(models))


    def terminate(self):
        try:
            if not globalVars.appArgs.secure:
                if hasattr(self, 'va_submenu_item') and self.va_submenu_item:
                    self.tools_menu.Remove(self.va_submenu_item.GetId())

            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsPanel)

        except Exception as e: log.debug(f"Settings panel remove failed: {e}")

        if hasattr(self, 'update_timer') and self.update_timer and self.update_timer.IsRunning():
            self.update_timer.Stop()

        self._abort_operator = True
        self._is_operator_running = False
        self._operator_thread_token = getattr(self, "_operator_thread_token", 0) + 1

        if self.live_session:
            try: self.live_session.stop()
            except Exception as e: log.debug(f"Live session stop failed: {e}")
            self.live_session = None

        for dlg in [self.refine_dlg, self.refine_menu_dlg, self.vision_dlg, self.doc_dlg, self.doc_viewer_dlg, self.translation_dlg]:
            if dlg:
                try:
                    if getattr(dlg, "abort", None) is not None:
                        dlg.abort = True
                    dlg.Destroy()
                except Exception as e: log.debug(f"Dialog abort/destroy failed: {e}")

        if self.is_recording:
            try:
                ctypes.windll.winmm.mciSendStringW('close all', None, 0, 0)
            except Exception as e: log.debug(f"MCI close all failed: {e}")

        self.translation_cache = {}
        self._last_source_text = None
        plugin_state.plugin_instance = None
        for fpath in getattr(self, "_temp_files_to_cleanup", []):
            try:
                if os.path.exists(fpath):
                    os.remove(fpath)
            except Exception as e: log.debug(f"Temp file removal failed: {e}")
        self._temp_files_to_cleanup = []
        gc.collect()

    def report_status(self, msg):
        self.current_status = msg
        plugin_state.speak_status(msg)

    # Translators: Script description for 'Activates the Command Layer for quick access to all features.' in Input Gestures dialog.
    @scriptHandler.script(description=_("Activates the Command Layer for quick access to all features."), category=ADDON_NAME)
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

    def _make_custom_prompt_script(self, prompt_name, content, script_name):
        # Translators: Script description in Input Gestures for a shortcut that runs a custom prompt. {name} is the prompt name.
        description = _("Runs the custom prompt \"{name}\".").format(name=prompt_name)

        def make(prompt_content):
            def script(self, gesture):
                if self.toggling:
                    self.finish()
                captured_text = self._get_text_smart()
                if not captured_text:
                    captured_text = ""
                wx.CallLater(100, self._run_refine_prompt, captured_text, prompt_content)
            script.__name__ = "script_" + script_name
            return scriptHandler.script(description=description, category=ADDON_NAME)(script)

        return make(content)

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
                self._make_custom_prompt_script(item.get("name", ""), item.get("content", ""), script_name),
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
            help_url = "https://github.com/mahmoodhozhabri/VisionAssistantPro"
            os.startfile(help_url)
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
            except Exception as e: log.debug(f"Foreground object name get failed: {e}")
        return appName

    __gestures = {
        "kb:NVDA+shift+v": "activateLayer",
    }

    __VisionGestures = {
        "kb:t": "translateSmart",
        "kb:r": "refineText",
        "kb:o": "ocrFullScreen",
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
        "kb:control+l": "toggleLiveAssistant",
        "kb:alt+s": "openSettings",
        "kb:alt+q": "reportQuotaExhaustedKeys",
        "kb:alt+m": "reportSelectedModels",
        "kb:downArrow": "layerDown",
        "kb:upArrow": "layerUp",
        "kb:rightArrow": "layerRight",
        "kb:leftArrow": "layerLeft",
        "kb:control+t": "voiceTranslation",
        "kb:control+h": "openHistory",
    }
