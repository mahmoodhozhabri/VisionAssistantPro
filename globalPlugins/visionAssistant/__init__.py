# -*- coding: utf-8 -*-

import addonHandler
import globalPluginHandler
import config
import gui
import wx
import json
import threading
import ui
import api
import logging
import textInfos
import os
import base64
import io
import ctypes
import re
import tempfile
import time
import gc
import tones
import scriptHandler
from urllib import request, error

log = logging.getLogger(__name__)
addonHandler.initTranslation()

# --- Configuration ---

MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash"
]

BASE_LANGUAGES = [
    ("Arabic", "ar"), ("Bulgarian", "bg"), ("Chinese", "zh"), ("Czech", "cs"), ("Danish", "da"),
    ("Dutch", "nl"), ("English", "en"), ("Finnish", "fi"), ("French", "fr"),
    ("German", "de"), ("Greek", "el"), ("Hebrew", "he"), ("Hindi", "hi"),
    ("Hungarian", "hu"), ("Indonesian", "id"), ("Italian", "it"), ("Japanese", "ja"),
    ("Korean", "ko"), ("Norwegian", "no"), ("Persian", "fa"), ("Polish", "pl"),
    ("Portuguese", "pt"), ("Romanian", "ro"), ("Russian", "ru"), ("Spanish", "es"),
    ("Swedish", "sv"), ("Thai", "th"), ("Turkish", "tr"), ("Ukrainian", "uk"),
    ("Vietnamese", "vi")
]
SOURCE_LIST = [("Auto-detect", "auto")] + BASE_LANGUAGES
SOURCE_NAMES = [x[0] for x in SOURCE_LIST]
TARGET_LIST = BASE_LANGUAGES
TARGET_NAMES = [x[0] for x in TARGET_LIST]

confspec = {
    "proxy_url": "string(default='')",
    "api_key": "string(default='')",
    "model_name": "string(default='gemini-2.5-flash-lite')",
    "target_language": "string(default='English')",
    "source_language": "string(default='Auto-detect')",
    "ai_response_language": "string(default='English')",
    "smart_swap": "boolean(default=True)",
    "captcha_mode": "string(default='navigator')",
    "custom_prompts": "string(default='')"
}

GITHUB_REPO = "mahmoodhozhabri/VisionAssistantPro"

# --- Helpers ---

def clean_markdown(text):
    if not text: return ""
    text = re.sub(r'\*\*|__|[*_]', '', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'^\s*-\s+', '', text, flags=re.MULTILINE)
    return text.strip()

def get_mime_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf': return 'application/pdf'
    if ext in ['.jpg', '.jpeg']: return 'image/jpeg'
    if ext == '.png': return 'image/png'
    if ext == '.webp': return 'image/webp'
    if ext in ['.tif', '.tiff']: return 'image/jpeg'
    if ext == '.mp3': return 'audio/mpeg'
    if ext == '.wav': return 'audio/wav'
    if ext == '.ogg': return 'audio/ogg'
    return 'application/octet-stream'

def show_error_dialog(message):
    # Translators: Title of the error dialog box
    title = _("Vision Assistant Error")
    wx.CallAfter(gui.messageBox, message, title, wx.OK | wx.ICON_ERROR)

def send_ctrl_v():
    try:
        user32 = ctypes.windll.user32
        VK_CONTROL = 0x11
        VK_V = 0x56
        KEYEVENTF_KEYUP = 0x0002
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        user32.keybd_event(VK_V, 0, 0, 0)
        user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    except: pass

def process_tiff_pages(path):
    pages_data = []
    no_log = wx.LogNull() 
    try:
        img_count = wx.Image.GetImageCount(path, wx.BITMAP_TYPE_TIFF)
        if img_count == 0: img_count = 1
        
        for i in range(img_count):
            try:
                img = wx.Image(path, wx.BITMAP_TYPE_TIFF, i)
                if img.IsOk():
                    stream = io.BytesIO()
                    img.SaveFile(stream, wx.BITMAP_TYPE_JPEG)
                    pages_data.append(base64.b64encode(stream.getvalue()).decode('utf-8'))
            except: continue
    except: pass
    return pages_data

PROMPT_TRANSLATE = """
Role: Translator.
Directives:
1. Translate text inside "===" to {target_lang}.
2. IF SmartSwap={smart_swap} AND input is {target_lang} THEN translate to {swap_target}.
3. Output ONLY the translation.

Text:
===
{text_content}
===
"""

PROMPT_UI_LOCATOR = "Analyze UI (Size: {width}x{height}). Request: '{query}'. Output JSON: {{\"x\": int, \"y\": int, \"found\": bool}}."

# --- Update Manager ---

class UpdateManager:
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.current_version = addonHandler.getCodeAddon().manifest['version']

    def check_for_updates(self, silent=True):
        threading.Thread(target=self._check_thread, args=(silent,), daemon=True).start()

    def _check_thread(self, silent):
        try:
            url = f"https://api.github.com/repos/{self.repo_name}/releases/latest"
            req = request.Request(url, headers={"User-Agent": "NVDA-Addon"})
            
            with request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    latest_tag = data.get("tag_name", "").lstrip("v")
                    
                    if self._compare_versions(latest_tag, self.current_version) > 0:
                        download_url = None
                        for asset in data.get("assets", []):
                            if asset["name"].endswith(".nvda-addon"):
                                download_url = asset["browser_download_url"]
                                break
                        
                        if download_url:
                            wx.CallAfter(self._prompt_update, latest_tag, download_url, data.get("body", ""))
                        elif not silent:
                            # Translators: Error message when update is detected but file is missing
                            msg = _("Update found but no .nvda-addon file in release.")
                            show_error_dialog(msg)
                    elif not silent:
                        # Translators: Message when no update is found
                        msg = _("You have the latest version.")
                        wx.CallAfter(ui.message, msg)
        except Exception as e:
            if not silent:
                # Translators: Error message for update check failure
                msg = _("Update check failed: {error}").format(error=e)
                show_error_dialog(msg)

    def _compare_versions(self, v1, v2):
        try:
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            return (parts1 > parts2) - (parts1 < parts2)
        except:
            return 0 if v1 == v2 else 1

    def _prompt_update(self, version, url, changes):
        # Translators: Message asking user to update. {version} is version number.
        msg = _("A new version ({version}) of Vision Assistant is available.\n\nChanges:\n{changes}\n\nDownload and Install?").format(version=version, changes=changes)
        # Translators: Title of update confirmation dialog
        title = _("Update Available")
        dlg = wx.MessageDialog(gui.mainFrame, msg, title, wx.YES_NO | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            threading.Thread(target=self._download_install_worker, args=(url,), daemon=True).start()
        dlg.Destroy()

    def _download_install_worker(self, url):
        try:
            # Translators: Message shown while downloading update
            msg = _("Downloading update...")
            wx.CallAfter(ui.message, msg)
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, "VisionAssistant_Update.nvda-addon")
            
            with request.urlopen(url) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            
            wx.CallAfter(os.startfile, file_path)
        except Exception as e:
            # Translators: Error message for download failure
            msg = _("Download failed: {error}").format(error=e)
            show_error_dialog(msg)

# --- UI Classes ---

class VisionQADialog(wx.Dialog):
    def __init__(self, parent, title, initial_text, context_data, callback_fn, extra_info=None):
        super(VisionQADialog, self).__init__(parent, title=title, size=(550, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.context_data = context_data 
        self.callback_fn = callback_fn
        self.extra_info = extra_info
        self.chat_history = [] 
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label for the AI response text area
        lbl_text = _("AI Response:")
        lbl = wx.StaticText(self, label=lbl_text)
        mainSizer.Add(lbl, 0, wx.ALL, 5)
        self.outputArea = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        mainSizer.Add(self.outputArea, 1, wx.EXPAND | wx.ALL, 5)
        
        clean_init = clean_markdown(initial_text)
        # Translators: Format for displaying AI message
        init_msg = _("AI: {text}\n").format(text=clean_init)
        self.outputArea.AppendText(init_msg)
        
        if not (extra_info and extra_info.get('skip_init_history')):
             self.chat_history.append({"role": "model", "parts": [{"text": initial_text}]})

        # Translators: Label for user input field
        ask_text = _("Ask:")
        inputLbl = wx.StaticText(self, label=ask_text)
        mainSizer.Add(inputLbl, 0, wx.ALL, 5)
        self.inputArea = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        mainSizer.Add(self.inputArea, 0, wx.EXPAND | wx.ALL, 5)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to send message
        self.askBtn = wx.Button(self, label=_("Send"))
        # Translators: Button to save chat
        self.saveBtn = wx.Button(self, label=_("Save Chat"))
        # Translators: Button to close dialog
        self.closeBtn = wx.Button(self, wx.ID_CANCEL, label=_("Close"))
        btnSizer.Add(self.askBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.saveBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.closeBtn, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT)
        
        self.SetSizer(mainSizer)
        self.inputArea.SetFocus()
        self.askBtn.Bind(wx.EVT_BUTTON, self.onAsk)
        self.saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        self.inputArea.Bind(wx.EVT_TEXT_ENTER, self.onAsk)
        
        wx.CallLater(300, ui.message, clean_init)

    def onAsk(self, event):
        question = self.inputArea.Value
        if not question.strip(): return
        # Translators: Format for displaying User message
        user_msg = _("\nYou: {text}\n").format(text=question)
        self.outputArea.AppendText(user_msg)
        self.inputArea.Clear()
        # Translators: Message shown while processing
        msg = _("Thinking...")
        ui.message(msg)
        threading.Thread(target=self.process_question, args=(question,), daemon=True).start()

    def process_question(self, question):
        result_tuple = self.callback_fn(self.context_data, question, self.chat_history, self.extra_info)
        response_text, _ = result_tuple
        
        if response_text:
            clean_resp = clean_markdown(response_text)
            if not (self.extra_info and self.extra_info.get('file_context')):
                 self.chat_history.append({"role": "user", "parts": [{"text": question}]})
                 self.chat_history.append({"role": "model", "parts": [{"text": response_text}]})
            wx.CallAfter(self.update_response, clean_resp)

    def update_response(self, text):
        # Translators: Format for displaying AI message
        ai_msg = _("AI: {text}\n").format(text=text)
        self.outputArea.AppendText(ai_msg)
        self.outputArea.ShowPosition(self.outputArea.GetLastPosition())
        ui.message(text)

    def onSave(self, event):
        # Translators: Save dialog title
        fd = wx.FileDialog(self, _("Save Chat Log"), wildcard="Text files (*.txt)|*.txt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fd.ShowModal() == wx.ID_OK:
            path = fd.GetPath()
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.outputArea.GetValue())
                # Translators: Message on successful save
                ui.message(_("Saved."))
            except Exception as e:
                msg = _("Save failed: {error}").format(error=e)
                show_error_dialog(msg)
        fd.Destroy()

class ResultDialog(wx.Dialog):
    def __init__(self, parent, title, content):
        super().__init__(parent, title=title, size=(600, 400), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        sizer = wx.BoxSizer(wx.VERTICAL)
        clean_content = clean_markdown(content)
        self.text_ctrl = wx.TextCtrl(self, value=clean_content, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        
        btn_sizer = wx.StdDialogButtonSizer()
        # Translators: Button to save content
        self.saveBtn = wx.Button(self, label=_("Save to File"))
        self.saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        
        # Translators: Close button label
        closeBtn = wx.Button(self, wx.ID_OK, label=_("Close"))
        
        btn_sizer.AddButton(self.saveBtn)
        btn_sizer.AddButton(closeBtn)
        btn_sizer.Realize()
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Centre()

    def onSave(self, event):
        # Translators: Save dialog title
        fd = wx.FileDialog(self, _("Save Result"), wildcard="Text files (*.txt)|*.txt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fd.ShowModal() == wx.ID_OK:
            path = fd.GetPath()
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.text_ctrl.GetValue())
                # Translators: Message on successful save
                ui.message(_("Saved."))
            except Exception as e:
                msg = _("Save failed: {error}").format(error=e)
                show_error_dialog(msg)
        fd.Destroy()

class SettingsPanel(gui.settingsDialogs.SettingsPanel):
    # Translators: Settings panel title
    title = _("Vision Assistant Pro")
    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        
        # Translators: Label for API Key input
        self.apiKey = sHelper.addLabeledControl(_("Gemini API Key:"), wx.TextCtrl)
        self.apiKey.Value = config.conf["VisionAssistant"]["api_key"]
        
        # Translators: Label for Model selection
        self.model = sHelper.addLabeledControl(_("AI Model:"), wx.Choice, choices=MODELS)
        try: self.model.SetSelection(MODELS.index(config.conf["VisionAssistant"]["model_name"]))
        except: self.model.SetSelection(0)

        # Translators: Label for Proxy URL input
        self.proxyUrl = sHelper.addLabeledControl(_("Proxy URL:"), wx.TextCtrl)
        self.proxyUrl.Value = config.conf["VisionAssistant"]["proxy_url"]
        
        sHelper.addItem(wx.StaticText(self, label=_("--- Languages ---")))
        # Translators: Label for Source Language selection
        self.sourceLang = sHelper.addLabeledControl(_("Source:"), wx.Choice, choices=SOURCE_NAMES)
        try: self.sourceLang.SetSelection(SOURCE_NAMES.index(config.conf["VisionAssistant"]["source_language"]))
        except: self.sourceLang.SetSelection(0)
        
        # Translators: Label for Target Language selection
        self.targetLang = sHelper.addLabeledControl(_("Target:"), wx.Choice, choices=TARGET_NAMES)
        try: self.targetLang.SetSelection(TARGET_NAMES.index(config.conf["VisionAssistant"]["target_language"]))
        except: self.targetLang.SetSelection(0)
        
        # Translators: Label for AI Response Language selection
        self.aiResponseLang = sHelper.addLabeledControl(_("AI Response:"), wx.Choice, choices=TARGET_NAMES)
        try: self.aiResponseLang.SetSelection(TARGET_NAMES.index(config.conf["VisionAssistant"]["ai_response_language"]))
        except: self.aiResponseLang.SetSelection(0)

        # Translators: Checkbox for Smart Swap feature
        self.smartSwap = sHelper.addItem(wx.CheckBox(self, label=_("Smart Swap")))
        self.smartSwap.Value = config.conf["VisionAssistant"]["smart_swap"]

        sHelper.addItem(wx.StaticText(self, label=_("--- CAPTCHA Mode ---")))
        # Translators: Radio box for CAPTCHA capture method
        self.captchaMode = wx.RadioBox(self, label=_("Capture Method:"), choices=[_("Navigator Object"), _("Full Screen")], style=wx.RA_SPECIFY_COLS)
        self.captchaMode.SetSelection(0 if config.conf["VisionAssistant"]["captcha_mode"] == 'navigator' else 1)
        sHelper.addItem(self.captchaMode)

        sHelper.addItem(wx.StaticText(self, label=_("--- Custom Prompts (Name:Content) ---")))
        self.customPrompts = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 100))
        self.customPrompts.Value = config.conf["VisionAssistant"]["custom_prompts"]
        sHelper.addItem(self.customPrompts)

    def onSave(self):
        config.conf["VisionAssistant"]["api_key"] = self.apiKey.Value.strip()
        config.conf["VisionAssistant"]["model_name"] = MODELS[self.model.GetSelection()]
        config.conf["VisionAssistant"]["proxy_url"] = self.proxyUrl.Value.strip()
        config.conf["VisionAssistant"]["source_language"] = SOURCE_NAMES[self.sourceLang.GetSelection()]
        config.conf["VisionAssistant"]["target_language"] = TARGET_NAMES[self.targetLang.GetSelection()]
        config.conf["VisionAssistant"]["ai_response_language"] = TARGET_NAMES[self.aiResponseLang.GetSelection()]
        config.conf["VisionAssistant"]["smart_swap"] = self.smartSwap.Value
        config.conf["VisionAssistant"]["captcha_mode"] = 'navigator' if self.captchaMode.GetSelection() == 0 else 'fullscreen'
        config.conf["VisionAssistant"]["custom_prompts"] = self.customPrompts.Value.strip()

# --- Global Plugin ---

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    # Translators: Name of the add-on category in Input Gestures
    scriptCategory = _("Vision Assistant")
    
    last_translation = "" 
    is_recording = False
    temp_audio_file = os.path.join(tempfile.gettempdir(), "vision_dictate.wav")
    
    translation_cache = {}
    _last_source_text = None
    _last_params = None
    update_timer = None

    def __init__(self):
        super(GlobalPlugin, self).__init__()
        config.conf.spec["VisionAssistant"] = confspec
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SettingsPanel)
        
        self.updater = UpdateManager(GITHUB_REPO)
        self.update_timer = wx.CallLater(10000, self.updater.check_for_updates, True)

    def terminate(self):
        try: gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsPanel)
        except: pass
        
        if self.update_timer and self.update_timer.IsRunning():
            self.update_timer.Stop()
        
        if self.is_recording:
            try:
                ctypes.windll.winmm.mciSendStringW('close all', None, 0, 0)
            except: pass
        
        self.translation_cache = {}
        self._last_source_text = None
        gc.collect()

    def _upload_file_to_gemini(self, file_path, mime_type):
        api_key = config.conf["VisionAssistant"]["api_key"].strip()
        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
        
        upload_url = f"{base_url}/upload/v1beta/files?key={api_key}"
        
        try:
            file_size = os.path.getsize(file_path)
            headers = {
                "X-Goog-Upload-Protocol": "raw",
                "X-Goog-Upload-Command": "start, upload, finalize",
                "X-Goog-Upload-Header-Content-Length": str(file_size),
                "X-Goog-Upload-File-Name": os.path.basename(file_path),
                "Content-Type": mime_type
            }
            
            with open(file_path, "rb") as f:
                file_data = f.read()
                
            req = request.Request(upload_url, data=file_data, headers=headers, method="POST")
            with request.urlopen(req, timeout=600) as response:
                if response.status == 200:
                    res_json = json.loads(response.read().decode('utf-8'))
                    return res_json.get('file', {}).get('uri')
        except error.URLError as e:
            # Translators: Connection error during upload
            msg = _("Upload Connection Error: {reason}").format(reason=e.reason)
            show_error_dialog(msg)
        except error.HTTPError as e:
            # Translators: HTTP error during upload
            msg = _("Upload Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
            show_error_dialog(msg)
        except Exception as e:
            # Translators: Generic upload error
            msg = _("File Upload Error: {error}").format(error=e)
            show_error_dialog(msg)
        return None

    def _call_gemini(self, prompt_or_contents, attachments=[], json_mode=False, raise_errors=False):
        api_key = config.conf["VisionAssistant"]["api_key"].strip()
        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        model = config.conf["VisionAssistant"]["model_name"]
        
        if not api_key:
            # Translators: Message when API Key is missing
            msg = _("API Key missing.")
            wx.CallAfter(ui.message, msg)
            return None

        base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
        url = f"{base_url}/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "x-api-key": api_key
        }
        
        contents = []
        if isinstance(prompt_or_contents, list):
            contents = prompt_or_contents
        else:
            parts = [{"text": prompt_or_contents}]
            for att in attachments:
                if 'file_uri' in att:
                    parts.append({"file_data": {"mime_type": att['mime_type'], "file_uri": att['file_uri']}})
                else:
                    parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
            contents = [{"parts": parts}]
            
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.0, 
                "topK": 40
            }
        }
        if json_mode: data["generationConfig"]["response_mime_type"] = "application/json"

        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                req = request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
                with request.urlopen(req, timeout=600) as response:
                    if response.status == 200:
                        res = json.loads(response.read().decode('utf-8'))
                        text = res['candidates'][0]['content']['parts'][0]['text'].strip()
                        return text if json_mode else clean_markdown(text)
            except error.HTTPError as e:
                if e.code == 503 and attempt < max_retries:
                    time.sleep(1)
                    continue
                log.error(f"Gemini HTTP Error: {e.code} - {e.reason}")
                if raise_errors: raise e
                return None
            except Exception as e:
                log.error(f"Gemini General Error: {e}")
                if raise_errors: raise e
                return None
        return None

    def _call_gemini_safe(self, *args, **kwargs):
        try:
            return self._call_gemini(*args, raise_errors=True, **kwargs)
        except error.URLError as e:
            # Translators: Connection error with technical reason
            msg = _("Connection Error: {reason}").format(reason=e.reason)
            show_error_dialog(msg)
        except error.HTTPError as e:
            if e.code == 400:
                # Translators: HTTP 400
                msg = _("Error 400: Bad Request (Check API Key Format)")
            elif e.code == 403:
                # Translators: HTTP 403
                msg = _("Error 403: Forbidden (Check Region/Permission)")
            elif e.code == 429:
                # Translators: HTTP 429
                msg = _("Error 429: Quota Exceeded (Try later)")
            else:
                # Translators: Generic HTTP error
                msg = _("Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
            show_error_dialog(msg)
        except Exception as e:
            # Translators: Generic fallback error
            msg = _("Error: {error}").format(error=e)
            show_error_dialog(msg)
        return None

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Records voice, transcribes it using AI, and types the result."))
    def script_smartDictation(self, gesture):
        if not self.is_recording:
            self.is_recording = True
            tones.beep(800, 100)
            try:
                ctypes.windll.winmm.mciSendStringW('open new type waveaudio alias myaudio', None, 0, 0)
                ctypes.windll.winmm.mciSendStringW('record myaudio', None, 0, 0)
                # Translators: Message when dictation starts
                msg = _("Listening...")
                ui.message(msg)
            except Exception as e:
                # Translators: Audio error message
                msg = _("Audio Hardware Error: {error}").format(error=e)
                show_error_dialog(msg)
                self.is_recording = False
        else:
            self.is_recording = False
            tones.beep(500, 100)
            try:
                ctypes.windll.winmm.mciSendStringW(f'save myaudio "{self.temp_audio_file}"', None, 0, 0)
                ctypes.windll.winmm.mciSendStringW('close myaudio', None, 0, 0)
                # Translators: Message when processing dictation
                msg = _("Typing...")
                ui.message(msg)
                threading.Thread(target=self._thread_dictation, daemon=True).start()
            except Exception as e:
                # Translators: Error saving dictation
                msg = _("Save Recording Error: {error}").format(error=e)
                show_error_dialog(msg)

    def _thread_dictation(self):
        try:
            if not os.path.exists(self.temp_audio_file): return
            with open(self.temp_audio_file, "rb") as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            p = "Transcribe speech. Use native script. No Fingilish. Fix stutters."
            
            res = self._call_gemini_safe(p, attachments=[{'mime_type': 'audio/wav', 'data': audio_data}])
            if res: wx.CallAfter(self._paste_text, res)
            else: 
                msg = _("No speech recognized or Error.")
                wx.CallAfter(ui.message, msg)
            
            try: os.remove(self.temp_audio_file)
            except: pass
        except: pass

    def _paste_text(self, text):
        api.copyToClip(text)
        send_ctrl_v()
        wx.CallLater(300, self._announce_paste, text)

    def _announce_paste(self, text):
        preview = text[:100]
        # Translators: Message showing typed text preview
        msg = _("Typed: {text}").format(text=preview)
        ui.message(msg)

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Translates the selected text or navigator object."))
    def script_translateSmart(self, gesture):
        text = self._get_text_smart()
        
        if not text:
            # Translators: Message when no text is found
            msg = _("No text found.")
            ui.message(msg)
            return
            
        # Translators: Message when translation starts
        msg = _("Translating...")
        ui.message(msg)
        threading.Thread(target=self._thread_translate, args=(text,), daemon=True).start()

    def _thread_translate(self, text):
        s = config.conf["VisionAssistant"]["source_language"]
        t = config.conf["VisionAssistant"]["target_language"]
        swap = config.conf["VisionAssistant"]["smart_swap"]
        fallback = "English" if s == "Auto-detect" else s
        
        current_params = f"{t}|{swap}"
        if text == self._last_source_text and current_params == self._last_params and self.last_translation:
            wx.CallAfter(self._announce_translation, self.last_translation)
            return

        safe_text = text.replace('{', '{{').replace('}', '}}')
        p = PROMPT_TRANSLATE.format(
            target_lang=t, 
            swap_target=fallback, 
            smart_swap=str(swap),
            text_content=safe_text
        )
        res = self._call_gemini_safe(p)
        if res:
            self._last_source_text = text
            self._last_params = current_params
            self.last_translation = res
            wx.CallAfter(self._announce_translation, res)

    def _announce_translation(self, text):
        api.copyToClip(text)
        # Translators: Message announcing translated text
        msg = _("Translated: {text}").format(text=text)
        ui.message(msg)

    def _get_text_smart(self):
        try:
            focus_obj = api.getFocusObject()
            if focus_obj:
                info = focus_obj.makeTextInfo(textInfos.POSITION_SELECTION)
                if info and info.text and not info.text.isspace():
                    return info.text
        except: pass

        try:
            obj = api.getNavigatorObject()
            if not obj: return None
            
            content = []
            if obj.name: content.append(obj.name)
            if obj.value: content.append(obj.value)
            if obj.description: content.append(obj.description)
            
            if hasattr(obj, 'makeTextInfo'):
                try: 
                    content.append(obj.makeTextInfo(textInfos.POSITION_ALL).text)
                except: pass
                
            final_text = " ".join(list(dict.fromkeys([c for c in content if c and not c.isspace()])))
            return final_text if final_text else None
        except Exception: 
            return None

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Opens a menu to Explain, Summarize, or Fix the selected text."))
    def script_refineText(self, gesture):
        text = self._get_text_smart()
        if not text: text = "" 
        
        # Translators: Message while preparing to open menu
        msg = _("Opening menu...")
        ui.message(msg)
        wx.CallLater(200, self._open_refine_dialog, text)

    def _open_refine_dialog(self, text):
        # Translators: Menu options for text refinement
        choices = [_("Summarize"), _("Fix Grammar"), _("Fix Grammar & Translate"), _("Explain")]
        custom_raw = config.conf["VisionAssistant"]["custom_prompts"]
        custom_dict = {}
        if custom_raw:
            for line in custom_raw.split('|'):
                if ':' in line:
                    parts = line.split(':', 1)
                    name = parts[0].strip()
                    content = parts[1].strip()
                    if name and content:
                        choices.append(f"Custom: {name}")
                        custom_dict[f"Custom: {name}"] = content
        
        # Translators: Title of the Refine dialog
        dlg = wx.SingleChoiceDialog(gui.mainFrame, _("Choose action:"), _("Refine"), choices)
        if dlg.ShowModal() == wx.ID_OK:
            sel_str = dlg.GetStringSelection()
            custom_content = ""
            
            if sel_str in custom_dict:
                custom_content = custom_dict[sel_str]
            else:
                if sel_str == _("Summarize"): custom_content = "[summarize]"
                elif sel_str == _("Fix Grammar"): custom_content = "[fix_grammar]"
                elif sel_str == _("Fix Grammar & Translate"): custom_content = "[fix_translate]"
                elif sel_str == _("Explain"): custom_content = "[explain]"

            file_path = None
            needs_file = False
            wc = "Files|*.*"
            
            if "[file_ocr]" in custom_content:
                needs_file = True
                wc = "Images/PDF/TIFF|*.png;*.jpg;*.webp;*.pdf;*.tif;*.tiff"
            elif "[file_read]" in custom_content:
                needs_file = True
                wc = "Documents|*.txt;*.py;*.md;*.html;*.pdf;*.tif;*.tiff"
            elif "[file_audio]" in custom_content:
                needs_file = True
                wc = "Audio|*.mp3;*.wav;*.ogg"
            
            if needs_file:
                # Translators: File dialog title
                title = _("Select File")
                if "[file_ocr]" in custom_content: title = _("Select Image/PDF/TIFF for OCR")
                fd = wx.FileDialog(gui.mainFrame, title, wildcard=wc, style=wx.FD_OPEN)
                if fd.ShowModal() == wx.ID_OK:
                    file_path = fd.GetPath()
                    wx.CallLater(500, lambda: threading.Thread(target=self._thread_refine, args=(text, custom_content, file_path), daemon=True).start())
                fd.Destroy()
            else:
                # Translators: Message while processing request
                msg = _("Processing...")
                ui.message(msg)
                threading.Thread(target=self._thread_refine, args=(text, custom_content, file_path), daemon=True).start()
        dlg.Destroy()

    def _thread_refine(self, text, custom_content, file_path=None):
        target_lang = config.conf["VisionAssistant"]["target_language"]
        source_lang = config.conf["VisionAssistant"]["source_language"]
        smart_swap = config.conf["VisionAssistant"]["smart_swap"]
        resp_lang = config.conf["VisionAssistant"]["ai_response_language"]
        
        prompt_text = custom_content
        attachments = []
        
        if "[fix_translate]" in prompt_text:
            fallback = "English" if source_lang == "Auto-detect" else source_lang
            swap_instr = f"If text is in {target_lang}, translate to {fallback}." if smart_swap else ""
            prompt_text = prompt_text.replace("[fix_translate]", 
                f"Fix grammar and translate to {target_lang}. {swap_instr} Output ONLY the result.")
        
        prompt_text = prompt_text.replace("[summarize]", f"Summarize the text below in {resp_lang}.")
        prompt_text = prompt_text.replace("[fix_grammar]", "Fix grammar in the text below. Output ONLY the fixed text.")
        prompt_text = prompt_text.replace("[explain]", f"Explain the text below in {resp_lang}.")
        
        used_selection = False
        if "[selection]" in prompt_text: 
            prompt_text = prompt_text.replace("[selection]", text)
            used_selection = True
            
        if "[clipboard]" in prompt_text: 
            prompt_text = prompt_text.replace("[clipboard]", api.getClipData())
        
        if "[screen_obj]" in prompt_text:
            d, w, h = self._capture_navigator()
            if d: attachments.append({'mime_type': 'image/png', 'data': d})
            prompt_text = prompt_text.replace("[screen_obj]", "")
            
        if "[screen_full]" in prompt_text:
            d, w, h = self._capture_fullscreen()
            if d: attachments.append({'mime_type': 'image/png', 'data': d})
            prompt_text = prompt_text.replace("[screen_full]", "")
            
        if file_path:
            try:
                # Translators: Message while uploading file
                msg = _("Uploading file...")
                wx.CallAfter(ui.message, msg)
                mime_type = get_mime_type(file_path)
                if "[file_ocr]" in prompt_text:
                    file_uri = self._upload_file_to_gemini(file_path, mime_type)
                    if file_uri:
                         attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                         prompt_text = prompt_text.replace("[file_ocr]", "")
                         if not prompt_text.strip():
                             prompt_text = "Extract all text from this file as plain text. Do not use JSON or bounding boxes."
                
                elif "[file_read]" in prompt_text:
                    file_uri = self._upload_file_to_gemini(file_path, mime_type)
                    if file_uri:
                        attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                        prompt_text = prompt_text.replace("[file_read]", "")
                    else:
                         with open(file_path, "rb") as f: raw = f.read()
                         txt = raw.decode('utf-8')
                         prompt_text = prompt_text.replace("[file_read]", f"\nFile Content:\n{txt}\n")
                         
                elif "[file_audio]" in prompt_text:
                    file_uri = self._upload_file_to_gemini(file_path, mime_type)
                    if file_uri:
                        attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                        prompt_text = prompt_text.replace("[file_audio]", "")
            except: pass
            
        if text and not used_selection and not file_path:
            prompt_text += f"\n\n---\nInput Text:\n{text}\n---\n"
            
        # Translators: Message while processing request
        msg = _("Analyzing...")
        wx.CallAfter(ui.message, msg)
        res = self._call_gemini_safe(prompt_text, attachments=attachments)
        
        if res:
             wx.CallAfter(self._open_refine_result_dialog, res, attachments, text)

    def _open_refine_result_dialog(self, result_text, attachments, original_text):
        def refine_callback(ctx, q, history, dum2):
            atts, orig = ctx
            parts = [{"text": q}]
            current_user_msg = {"role": "user", "parts": parts}
            
            messages = []
            
            has_file = any('file_uri' in a for a in atts)
            
            if not history:
                if has_file:
                     sys_parts = [{"text": f"Context: File attached. Task: Answer questions."}]
                     for att in atts:
                        if 'file_uri' in att:
                             sys_parts.append({"file_data": {"mime_type": att['mime_type'], "file_uri": att['file_uri']}})
                else:
                     context_msg = f"Context Text: {orig}\n\nTask: Answer questions."
                     sys_parts = [{"text": context_msg}]
                     for att in atts:
                        if 'data' in att:
                             sys_parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
                
                messages.append({"role": "user", "parts": sys_parts})
                messages.append({"role": "model", "parts": [{"text": result_text}]})
            else:
                messages.extend(history)
            
            messages.append(current_user_msg)
            return self._call_gemini_safe(messages), None

        context = (attachments, original_text)
        has_file_context = any('file_uri' in a for a in attachments)
        # Translators: Title of Refine Result dialog
        dlg = VisionQADialog(gui.mainFrame, _("Vision Assistant - Refine Result"), result_text, context, refine_callback, extra_info={'file_context': has_file_context, 'skip_init_history': False})
        dlg.Show()

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Recognizes text from a selected image or PDF file."))
    def script_fileOCR(self, gesture):
        # Translators: Message while preparing to open dialog
        msg = _("Select a file for OCR...")
        ui.message(msg)
        wx.CallLater(200, self._open_file_ocr_dialog)

    def _open_file_ocr_dialog(self):
        # Translators: File dialog title for File OCR
        dlg = wx.FileDialog(gui.mainFrame, _("Select Image or PDF"), wildcard="Files|*.pdf;*.jpg;*.jpeg;*.png;*.webp;*.tif;*.tiff", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            threading.Thread(target=self._process_file_ocr, args=(path,), daemon=True).start()
        dlg.Destroy()

    def _process_file_ocr(self, path):
        # Translators: Message while uploading file
        msg = _("Uploading & Extracting...")
        wx.CallAfter(ui.message, msg)
        mime_type = get_mime_type(path)
        
        file_uri = self._upload_file_to_gemini(path, mime_type)
        
        if file_uri:
            att = [{'mime_type': mime_type, 'file_uri': file_uri}]
            
            res = self._call_gemini_safe("Extract all text from this file as plain text. Do not use JSON or bounding boxes.", attachments=att)
            if res:
                wx.CallAfter(self._open_doc_chat_dialog, res, att, "")
        else:
            pass

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Allows asking questions about a selected document (PDF/Text/Image)."))
    def script_analyzeDocument(self, gesture):
        # Translators: Message while preparing to open dialog
        msg = _("Select a document...")
        ui.message(msg)
        wx.CallLater(200, self._open_doc_dialog)

    def _open_doc_dialog(self):
        # Translators: File dialog title for Document Analysis
        dlg = wx.FileDialog(gui.mainFrame, _("Select Document to Analyze"), wildcard="Doc|*.pdf;*.tif;*.tiff;*.txt;*.py;*.md", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            threading.Thread(target=self._process_doc_file, args=(path,), daemon=True).start()
        dlg.Destroy()

    def _process_doc_file(self, path):
        # Translators: Message while uploading file
        msg = _("Uploading & Analyzing...")
        wx.CallAfter(ui.message, msg)
        mime_type = get_mime_type(path)
        
        file_uri = self._upload_file_to_gemini(path, mime_type)
        
        if file_uri:
            att = [{'mime_type': mime_type, 'file_uri': file_uri}]
            # Translators: Initial message in document chat
            init_msg = _("Document ready. Ask your question.")
            
            wx.CallAfter(self._open_doc_chat_dialog, init_msg, att, "")
        else:
            pass
        
    def _open_doc_chat_dialog(self, init_msg, initial_attachments, doc_text):
        def doc_callback(ctx_atts, q, history, dum2):
            lang = config.conf["VisionAssistant"]["ai_response_language"]
            atts = ctx_atts if ctx_atts else []
            
            current_user_msg = {"role": "user", "parts": [{"text": f"{q} (STRICTLY Respond in {lang})"}]}
            
            messages = []
            if not history:
                parts = [{"text": f"Analyze this file. {q} (Respond in {lang})"}]
                for att in atts:
                    if 'file_uri' in att:
                        parts.append({"file_data": {"mime_type": att['mime_type'], "file_uri": att['file_uri']}})
                
                return self._call_gemini_safe([{"parts": parts}]), None
            else:
                messages.extend(history)
                messages.append(current_user_msg)
                return self._call_gemini_safe(messages), None
            
        # Translators: Dialog title for Chat
        dlg = VisionQADialog(gui.mainFrame, _("Vision Assistant - Chat"), init_msg, initial_attachments, doc_callback, extra_info={'skip_init_history': True})
        dlg.Show()

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Performs OCR and description on the entire screen."))
    def script_ocrFullScreen(self, gesture):
        self._start_vision(True)

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Describes the current object (Navigator Object)."))
    def script_describeObject(self, gesture):
        self._start_vision(False)

    def _start_vision(self, full):
        if full: d, w, h = self._capture_fullscreen()
        else: d, w, h = self._capture_navigator()
        if d:
            # Translators: Message while scanning screen
            msg = _("Scanning...")
            ui.message(msg)
            wx.CallLater(100, lambda: threading.Thread(target=self._thread_vision, args=(d, w, h), daemon=True).start())
        else: 
            # Translators: Message when capture fails
            ui.message(_("Capture failed."))

    def _thread_vision(self, img, w, h):
        lang = config.conf["VisionAssistant"]["ai_response_language"]
        p = f"Analyze this image and describe it. Language: {lang}. Ensure the response is strictly in {lang}."
        att = [{'mime_type': 'image/png', 'data': img}]
        res = self._call_gemini_safe(p, attachments=att)
        if res:
            wx.CallAfter(self._open_vision_dialog, res, att, None)
        
    def _open_vision_dialog(self, text, atts, size):
        def cb(atts, q, history, sz):
            lang = config.conf["VisionAssistant"]["ai_response_language"]
            current_user_msg = {"role": "user", "parts": [{"text": f"{q} (Answer strictly in {lang})"}]}
            
            messages = []
            if not history:
                parts = [{"text": f"Image Context. Target Language: {lang}"}]
                for att in atts:
                    parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
                messages.append({"role": "user", "parts": parts})
                messages.append({"role": "model", "parts": [{"text": text}]})
            else:
                messages.extend(history)
                
            messages.append(current_user_msg)
            return self._call_gemini_safe(messages), None
            
        # Translators: Dialog title for Image Analysis
        dlg = VisionQADialog(gui.mainFrame, _("Vision Assistant - Image Analysis"), text, atts, cb, None)
        dlg.Show()

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Transcribes a selected audio file."))
    def script_transcribeAudio(self, gesture):
        # Translators: Message while preparing to open audio dialog
        msg = _("Select an audio file...")
        ui.message(msg)
        wx.CallLater(200, self._open_audio)

    def _open_audio(self):
        # Translators: File dialog title for Audio Transcription
        dlg = wx.FileDialog(gui.mainFrame, _("Select Audio File to Transcribe"), wildcard="Audio|*.mp3;*.wav;*.ogg", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            threading.Thread(target=self._thread_audio, args=(dlg.GetPath(),), daemon=True).start()
        dlg.Destroy()

    def _thread_audio(self, path):
        # Translators: Message while uploading audio
        msg = _("Uploading...")
        wx.CallAfter(ui.message, msg)
        mime_type = get_mime_type(path)
        
        file_uri = self._upload_file_to_gemini(path, mime_type)
        if not file_uri: return

        # Translators: Message while analyzing audio
        msg = _("Analyzing...")
        wx.CallAfter(ui.message, msg)
        lang = config.conf["VisionAssistant"]["ai_response_language"]
        p = f"Transcribe this audio in {lang}."
        
        att = [{'mime_type': mime_type, 'file_uri': file_uri}]
        res = self._call_gemini_safe(p, attachments=att)
        
        if res:
            init_msg = res 
            wx.CallAfter(self._open_doc_chat_dialog, init_msg, att, "")

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Attempts to solve a CAPTCHA on the screen or navigator object."))
    def script_solveCaptcha(self, gesture):
        mode = config.conf["VisionAssistant"]["captcha_mode"]
        if mode == 'fullscreen': d, w, h = self._capture_fullscreen()
        else: d, w, h = self._capture_navigator()
        
        is_gov = False
        try:
            if api.getForegroundObject() and "پنجره ملی خدمات دولت هوشمند" in api.getForegroundObject().name: 
                is_gov = True
        except: pass

        if d:
            # Translators: Message while solving CAPTCHA
            msg = _("Solving...")
            ui.message(msg)
            threading.Thread(target=self._thread_cap, args=(d, is_gov), daemon=True).start()
        else: 
            # Translators: Message when capture fails
            ui.message(_("Capture failed."))
        
    def _thread_cap(self, d, is_gov):
        p = "Blind user. Return CAPTCHA code only."
        if is_gov: p += " Read 5 Persian digits, convert to English."
        else: p += " Convert to English digits."
        
        r = self._call_gemini_safe(p, attachments=[{'mime_type': 'image/png', 'data': d}])
        if r: wx.CallAfter(self._finish_captcha, r)
        else: wx.CallAfter(ui.message, _("Failed."))

    def _finish_captcha(self, text):
        api.copyToClip(text)
        send_ctrl_v()
        # Translators: Message announcing CAPTCHA result
        msg = _("Captcha: {text}").format(text=text)
        wx.CallLater(200, ui.message, msg)

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Checks for updates manually."))
    def script_checkUpdate(self, gesture):
        # Translators: Message when checking for updates
        msg = _("Checking for updates...")
        ui.message(msg)
        self.updater.check_for_updates(silent=False)

    def _capture_navigator(self):
        try:
            obj = api.getNavigatorObject()
            if not obj or not obj.location: return None,0,0
            x,y,w,h = obj.location
            if w<1 or h<1: return None,0,0
            bmp = wx.Bitmap(w,h)
            wx.MemoryDC(bmp).Blit(0,0,w,h,wx.ScreenDC(),x,y)
            s = io.BytesIO()
            bmp.ConvertToImage().SaveFile(s, wx.BITMAP_TYPE_PNG)
            return base64.b64encode(s.getvalue()).decode('utf-8'),w,h
        except: return None,0,0
    def _capture_fullscreen(self):
        try:
            w,h = wx.GetDisplaySize()
            bmp = wx.Bitmap(w,h)
            wx.MemoryDC(bmp).Blit(0,0,w,h,wx.ScreenDC(),0,0)
            s = io.BytesIO()
            bmp.ConvertToImage().SaveFile(s, wx.BITMAP_TYPE_PNG)
            return base64.b64encode(s.getvalue()).decode('utf-8'),w,h
        except: return None,0,0

    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Announces the last received translation."))
    def script_readLastTranslation(self, gesture):
        if self.last_translation: ui.message(f"Last: {self.last_translation}")
        else: 
            # Translators: Message when no history is available
            ui.message(_("No history."))
    
    # Translators: Script description for Input Gestures
    @scriptHandler.script(description=_("Translates the text currently in the clipboard."))
    def script_translateClipboard(self, gesture):
        t = api.getClipData()
        if t: 
            # Translators: Message when translating from clipboard
            msg = _("Translating Clipboard...")
            ui.message(msg)
            threading.Thread(target=self._thread_translate, args=(t,), daemon=True).start()
        else:
            # Translators: Message when clipboard is empty
            msg = _("Clipboard empty.")
            ui.message(msg)

    __gestures = {
        "kb:NVDA+control+shift+t": "translateSmart",
        "kb:NVDA+control+shift+r": "refineText",
        "kb:NVDA+control+shift+o": "ocrFullScreen",
        "kb:NVDA+control+shift+v": "describeObject",
        "kb:NVDA+control+shift+d": "analyzeDocument",
        "kb:NVDA+control+shift+f": "fileOCR",
        "kb:NVDA+control+shift+a": "transcribeAudio",
        "kb:NVDA+control+shift+c": "solveCaptcha",
        "kb:NVDA+control+shift+l": "readLastTranslation",
        "kb:NVDA+control+shift+y": "translateClipboard",
        "kb:NVDA+control+shift+s": "smartDictation",
        "kb:NVDA+control+shift+u": "checkUpdate",
    }