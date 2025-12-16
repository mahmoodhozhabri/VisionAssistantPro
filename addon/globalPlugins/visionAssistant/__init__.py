# -*- coding: utf-8 -*-

import sys
import os
import json
import threading
import logging
import base64
import io
import ctypes
import re
import tempfile
import time
import wave
import gc
from contextlib import contextmanager
from urllib import request, error
from urllib.parse import quote

@contextmanager
def scoped_import():
    lib_dir = os.path.join(os.path.dirname(__file__), "lib")
    sys.path.insert(0, lib_dir)
    try:
        yield
    finally:
        if lib_dir in sys.path:
            sys.path.remove(lib_dir)

with scoped_import():
    import markdown

import addonHandler
import globalPluginHandler
import config
import gui
import wx
import ui
import api
import textInfos
import tones
import NVDAObjects.behaviors
import scriptHandler

log = logging.getLogger(__name__)
addonHandler.initTranslation()

ADDON_NAME = addonHandler.getCodeAddon().manifest["summary"]

# --- Configuration ---

MODELS = [
    # --- 1. Recommended (Auto-Updating) ---
    # Translators: AI Model info. [Auto] = Automatic updates. (Latest) = Newest version.
    (_("[Auto]") + " Gemini Flash " + _("(Latest)"), "gemini-flash-latest"),
    (_("[Auto]") + " Gemini Flash Lite " + _("(Latest)"), "gemini-flash-lite-latest"),

    # --- 2. Current Standard (Free & Fast) ---
    # Translators: AI Model info. [Free] = Generous usage limits.
    (_("[Free]") + " Gemini 2.5 Flash", "gemini-2.5-flash"),
    (_("[Free]") + " Gemini 2.5 Flash Lite", "gemini-2.5-flash-lite"),

    # --- 3. High Intelligence (Paid/Pro/Preview) ---
    # Translators: AI Model info. [Pro] = High intelligence/Paid. (Preview) = Experimental version.
    (_("[Pro]") + " Gemini 3.0 Pro " + _("(Preview)"), "gemini-3-pro-preview"),
    (_("[Pro]") + " Gemini 2.5 Pro", "gemini-2.5-pro"),

    # --- 4. Legacy (Older Versions) ---
    # Translators: AI Model info. [Legacy] = Older versions.
    (_("[Legacy]") + " Gemini 2.0 Flash", "gemini-2.0-flash"),
    (_("[Legacy]") + " Gemini 2.0 Flash Lite", "gemini-2.0-flash-lite"),
]

BASE_LANGUAGES = [
    ("Arabic", "ar"), ("Bulgarian", "bg"), ("Chinese", "zh"), ("Czech", "cs"), ("Danish", "da"),
    ("Dutch", "nl"), ("English", "en"), ("Finnish", "fi"), ("French", "fr"),
    ("German", "de"), ("Greek", "el"), ("Hebrew", "he"), ("Hindi", "hi"),
    ("Hungarian", "hu"), ("Indonesian", "id"), ("Italian", "it"), ("Japanese", "ja"),
    ("Korean", "ko"), ("Nepali", "ne"), ("Norwegian", "no"), ("Persian", "fa"), ("Polish", "pl"),
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
    "model_name": "string(default='gemini-flash-lite-latest')",
    "target_language": "string(default='English')",
    "source_language": "string(default='Auto-detect')",
    "ai_response_language": "string(default='English')",
    "smart_swap": "boolean(default=True)",
    "captcha_mode": "string(default='navigator')",
    "custom_prompts": "string(default='')",
    "check_update_startup": "boolean(default=False)",
    "clean_markdown_chat": "boolean(default=True)"
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

def text_to_html(text, full_page=False):
    if not text: return ""
    
    try:
        html_body = markdown.markdown(text, extensions=['fenced_code', 'tables', 'nl2br'])
    except:
        html_body = markdown.markdown(text)
        html_body = html_body.replace("\n", "<br>")
        
    if not full_page:
        return html_body

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{ADDON_NAME} Result</title>
        <style>
            body {{ font-family: "Segoe UI", Arial, sans-serif; line-height: 1.6; padding: 20px; color: #333; max-width: 800px; margin: 0 auto; }}
            h1, h2, h3 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; font-family: Consolas, monospace; }}
            code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: Consolas, monospace; }}
            strong {{ color: #000; }}
            li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

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
    title = _("{name} Error").format(name=ADDON_NAME)
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
Task: Translate the text below.

Configuration:
- Target Language: "{target_lang}"
- Swap Language: "{swap_target}"
- Smart Swap: {smart_swap}

Rules:
1. DEFAULT: Translate the input strictly to "{target_lang}".
2. EXCEPTION: If (and ONLY if) the input is already completely in "{target_lang}" AND "Smart Swap" is True, then translate to "{swap_target}".

Constraints:
- Output ONLY the translation.
- Do NOT explain your logic or add notes.
- Do NOT translate technical terms, code, or protocol names.

Input Text:
{text_content}
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
                            raw_changes = data.get("body", "")
                            clean_changes = clean_markdown(raw_changes)
                            wx.CallAfter(self._prompt_update, latest_tag, download_url, clean_changes)
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
        msg = _("A new version ({version}) of {name} is available.\n\nChanges:\n{changes}\n\nDownload and Install?").format(version=version, name=ADDON_NAME, changes=changes)
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
    def __init__(self, parent, title, initial_text, context_data, callback_fn, extra_info=None, raw_content=None, status_callback=None):
        super(VisionQADialog, self).__init__(parent, title=title, size=(550, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.context_data = context_data 
        self.callback_fn = callback_fn
        self.extra_info = extra_info
        self.chat_history = [] 
        self.raw_content = raw_content
        self.status_callback = status_callback
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label for the AI response text area in a chat dialog
        lbl_text = _("AI Response:")
        lbl = wx.StaticText(self, label=lbl_text)
        mainSizer.Add(lbl, 0, wx.ALL, 5)
        self.outputArea = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        mainSizer.Add(self.outputArea, 1, wx.EXPAND | wx.ALL, 5)
        
        self.should_clean = config.conf["VisionAssistant"]["clean_markdown_chat"]
        
        # Translators: Format for displaying AI message in a chat dialog
        display_text = clean_markdown(initial_text) if self.should_clean else initial_text
        if display_text:
            init_msg = _("AI: {text}\n").format(text=display_text)
            self.outputArea.AppendText(init_msg)
        
        if not (extra_info and extra_info.get('skip_init_history')):
             self.chat_history.append({"role": "model", "parts": [{"text": initial_text}]})

        # Translators: Label for user input field in a chat dialog
        ask_text = _("Ask:")
        inputLbl = wx.StaticText(self, label=ask_text)
        mainSizer.Add(inputLbl, 0, wx.ALL, 5)
        self.inputArea = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        mainSizer.Add(self.inputArea, 0, wx.EXPAND | wx.ALL, 5)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to send message in a chat dialog
        self.askBtn = wx.Button(self, label=_("Send"))
        
        # Translators: Button to view the content in a formatted HTML window
        self.viewBtn = wx.Button(self, label=_("View Formatted"))
        self.viewBtn.Bind(wx.EVT_BUTTON, self.onView)
        
        # Translators: Button to save only the result content without chat history
        self.saveContentBtn = wx.Button(self, label=_("Save Content"))
        self.saveContentBtn.Bind(wx.EVT_BUTTON, self.onSaveContent)

        # Translators: Button to save chat in a chat dialog
        self.saveBtn = wx.Button(self, label=_("Save Chat"))
        # Translators: Button to close chat dialog
        self.closeBtn = wx.Button(self, wx.ID_CANCEL, label=_("Close"))
        
        self.saveBtn.Enable(bool(initial_text.strip()))
        self.viewBtn.Enable(bool(self.raw_content))
        self.saveContentBtn.Enable(bool(self.raw_content))

        btnSizer.Add(self.askBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.viewBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.saveContentBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.saveBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.closeBtn, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT)
        
        self.SetSizer(mainSizer)
        self.inputArea.SetFocus()
        self.askBtn.Bind(wx.EVT_BUTTON, self.onAsk)
        self.saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        self.inputArea.Bind(wx.EVT_TEXT_ENTER, self.onAsk)
        
        if display_text:
            wx.CallLater(300, ui.message, display_text)

    def onAsk(self, event):
        question = self.inputArea.Value
        if not question.strip(): return
        # Translators: Format for displaying User message in a chat dialog
        user_msg = _("\nYou: {text}\n").format(text=question)
        self.outputArea.AppendText(user_msg)
        self.inputArea.Clear()
        # Translators: Message shown while processing in a chat dialog
        msg = _("Thinking...")
        ui.message(msg)
        threading.Thread(target=self.process_question, args=(question,), daemon=True).start()

    def process_question(self, question):
        result_tuple = self.callback_fn(self.context_data, question, self.chat_history, self.extra_info)
        response_text, _ = result_tuple
        
        if response_text:
            if not (self.extra_info and self.extra_info.get('file_context')):
                 self.chat_history.append({"role": "user", "parts": [{"text": question}]})
                 self.chat_history.append({"role": "model", "parts": [{"text": response_text}]})
            
            final_text = clean_markdown(response_text) if self.should_clean else response_text
            wx.CallAfter(self.update_response, final_text, response_text)

    def update_response(self, display_text, raw_text=None):
        if raw_text:
            self.raw_content = raw_text
            self.viewBtn.Enable(True)
            self.saveContentBtn.Enable(True)

        # Translators: Format for displaying AI message in a chat dialog
        ai_msg = _("AI: {text}\n").format(text=display_text)
        self.outputArea.AppendText(ai_msg)
        self.saveBtn.Enable(True)
        
        self.outputArea.ShowPosition(self.outputArea.GetLastPosition())
        ui.message(display_text)

    def report_save(self, msg):
        if self.status_callback:
            self.status_callback(msg)
        else:
            ui.message(msg)

    def onView(self, event):
        full_html = ""
        
        # Translators: Format for displaying User message in a chat dialog
        user_label = _("\nYou: {text}\n").format(text="").strip()
        # Translators: Format for displaying AI message in a chat dialog
        ai_label = _("AI: {text}\n").format(text="").strip()
        
        if self.chat_history:
            for item in self.chat_history:
                role = item.get("role", "")
                text = item.get("parts", [{}])[0].get("text", "")
                
                if role == "user":
                    safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    full_html += f"<h2>{user_label}</h2><p>{safe_text}</p>"
                elif role == "model":
                    formatted_text = text_to_html(text, full_page=False)
                    full_html += f"<h2>{ai_label}</h2>{formatted_text}<hr>"
        
        if not full_html and self.raw_content:
             formatted_text = text_to_html(self.raw_content, full_page=False)
             full_html += f"<h2>{ai_label}</h2>{formatted_text}"

        if not full_html: return

        try:
            # Translators: Title of the formatted result window
            ui.browseableMessage(full_html, _("Formatted Conversation"), isHtml=True)
        except Exception as e:
            # Translators: Error message if viewing fails
            msg = _("Error displaying content: {error}").format(error=e)
            show_error_dialog(msg)

    def onSave(self, event):
        # Translators: Save dialog title
        fd = wx.FileDialog(self, _("Save Chat Log"), wildcard="Text files (*.txt)|*.txt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fd.ShowModal() == wx.ID_OK:
            path = fd.GetPath()
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.outputArea.GetValue())
                # Translators: Message on successful save
                self.report_save(_("Saved."))
            except Exception as e:
                # Translators: Message in the error dialog when saving fails.
                msg = _("Save failed: {error}").format(error=e)
                show_error_dialog(msg)
        fd.Destroy()

    def onSaveContent(self, event):
        # Translators: Save dialog title
        fd = wx.FileDialog(self, _("Save Result"), wildcard="HTML files (*.html)|*.html", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if fd.ShowModal() == wx.ID_OK:
            path = fd.GetPath()
            try:
                full_html = text_to_html(self.raw_content, full_page=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(full_html)
                # Translators: Message on successful save
                self.report_save(_("Saved."))
            except Exception as e:
                # Translators: Message in the error dialog when saving fails.
                msg = _("Save failed: {error}").format(error=e)
                show_error_dialog(msg)
        fd.Destroy()

class SettingsPanel(gui.settingsDialogs.SettingsPanel):
    title = ADDON_NAME
    def makeSettings(self, settingsSizer):
        # --- Connection Group ---
        # Translators: Title of the settings group for connection and updates
        groupLabel = _("Connection")
        connectionBox = wx.StaticBox(self, label=groupLabel)
        connectionSizer = wx.StaticBoxSizer(connectionBox, wx.VERTICAL)
        cHelper = gui.guiHelper.BoxSizerHelper(connectionBox, sizer=connectionSizer)

        # Translators: Label for API Key input
        self.apiKey = cHelper.addLabeledControl(_("Gemini API Key:"), wx.TextCtrl)
        self.apiKey.Value = config.conf["VisionAssistant"]["api_key"]
        
        model_display_names = [opt[0] for opt in MODELS]
        
        # Translators: Label for Model selection
        self.model = cHelper.addLabeledControl(_("AI Model:"), wx.Choice, choices=model_display_names)
        
        current_id = config.conf["VisionAssistant"]["model_name"]
        try:
            index = next(i for i, v in enumerate(MODELS) if v[1] == current_id)
            self.model.SetSelection(index)
        except StopIteration:
            self.model.SetSelection(0)

        # Translators: Label for Proxy URL input
        self.proxyUrl = cHelper.addLabeledControl(_("Proxy URL:"), wx.TextCtrl)
        self.proxyUrl.Value = config.conf["VisionAssistant"]["proxy_url"]

        # Translators: Checkbox to enable/disable automatic update checks on NVDA startup
        self.checkUpdateStartup = cHelper.addItem(wx.CheckBox(connectionBox, label=_("Check for updates on startup")))
        self.checkUpdateStartup.Value = config.conf["VisionAssistant"]["check_update_startup"]
        
        # Translators: Checkbox to toggle markdown cleaning in chat windows
        self.cleanMarkdown = cHelper.addItem(wx.CheckBox(connectionBox, label=_("Clean Markdown in Chat")))
        self.cleanMarkdown.Value = config.conf["VisionAssistant"]["clean_markdown_chat"]

        settingsSizer.Add(connectionSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- Translation Languages Group ---
        # Translators: Title of the settings group for translation languages configuration
        groupLabel = _("Translation Languages")
        langBox = wx.StaticBox(self, label=groupLabel)
        langSizer = wx.StaticBoxSizer(langBox, wx.VERTICAL)
        lHelper = gui.guiHelper.BoxSizerHelper(langBox, sizer=langSizer)

        # Translators: Label for Source Language selection
        self.sourceLang = lHelper.addLabeledControl(_("Source:"), wx.Choice, choices=SOURCE_NAMES)
        try: self.sourceLang.SetSelection(SOURCE_NAMES.index(config.conf["VisionAssistant"]["source_language"]))
        except: self.sourceLang.SetSelection(0)
        
        # Translators: Label for Target Language selection
        self.targetLang = lHelper.addLabeledControl(_("Target:"), wx.Choice, choices=TARGET_NAMES)
        try: self.targetLang.SetSelection(TARGET_NAMES.index(config.conf["VisionAssistant"]["target_language"]))
        except: self.targetLang.SetSelection(0)
        
        # Translators: Label for AI Response Language selection
        self.aiResponseLang = lHelper.addLabeledControl(_("AI Response:"), wx.Choice, choices=TARGET_NAMES)
        try: self.aiResponseLang.SetSelection(TARGET_NAMES.index(config.conf["VisionAssistant"]["ai_response_language"]))
        except: self.aiResponseLang.SetSelection(0)

        # Translators: Checkbox for Smart Swap feature
        self.smartSwap = lHelper.addItem(wx.CheckBox(langBox, label=_("Smart Swap")))
        self.smartSwap.Value = config.conf["VisionAssistant"]["smart_swap"]

        settingsSizer.Add(langSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- CAPTCHA Group ---
        # Translators: Title of the settings group for CAPTCHA options
        groupLabel = _("CAPTCHA")
        capBox = wx.StaticBox(self, label=groupLabel)
        capSizer = wx.StaticBoxSizer(capBox, wx.VERTICAL)
        capHelper = gui.guiHelper.BoxSizerHelper(capBox, sizer=capSizer)

        # Translators: Label for CAPTCHA capture method selection
        self.captchaMode = capHelper.addLabeledControl(
            _("Capture Method:"), 
            wx.Choice, 
            choices=[
                # Translators: A choice for capture method. Captures only the specific object under the NVDA navigator cursor.
                _("Navigator Object"),
                # Translators: A choice for capture method. Captures the entire visible screen area.
                _("Full Screen")
            ]
        )
        self.captchaMode.SetSelection(0 if config.conf["VisionAssistant"]["captcha_mode"] == 'navigator' else 1)

        settingsSizer.Add(capSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- Custom Prompts Group ---
        # Translators: Title of the settings group for custom prompts
        groupLabel = _("Custom Prompts")
        promptsBox = wx.StaticBox(self, label=groupLabel)
        promptsSizer = wx.StaticBoxSizer(promptsBox, wx.VERTICAL)
        pHelper = gui.guiHelper.BoxSizerHelper(promptsBox, sizer=promptsSizer)

        # Translators: Helper text explaining the format for custom prompts
        pHelper.addItem(wx.StaticText(promptsBox, label=_("Format: Name:Content")))
        self.customPrompts = wx.TextCtrl(promptsBox, style=wx.TE_MULTILINE, size=(-1, 100))
        self.customPrompts.Value = config.conf["VisionAssistant"]["custom_prompts"]
        pHelper.addItem(self.customPrompts)

        settingsSizer.Add(promptsSizer, 1, wx.EXPAND | wx.ALL, 5)

    def onSave(self):
        config.conf["VisionAssistant"]["api_key"] = self.apiKey.Value.strip()
        # Save the Model ID (second element of the tuple), not the display name
        config.conf["VisionAssistant"]["model_name"] = MODELS[self.model.GetSelection()][1]
        config.conf["VisionAssistant"]["proxy_url"] = self.proxyUrl.Value.strip()
        config.conf["VisionAssistant"]["source_language"] = SOURCE_NAMES[self.sourceLang.GetSelection()]
        config.conf["VisionAssistant"]["target_language"] = TARGET_NAMES[self.targetLang.GetSelection()]
        config.conf["VisionAssistant"]["ai_response_language"] = TARGET_NAMES[self.aiResponseLang.GetSelection()]
        config.conf["VisionAssistant"]["smart_swap"] = self.smartSwap.Value
        config.conf["VisionAssistant"]["check_update_startup"] = self.checkUpdateStartup.Value
        config.conf["VisionAssistant"]["clean_markdown_chat"] = self.cleanMarkdown.Value
        config.conf["VisionAssistant"]["captcha_mode"] = 'navigator' if self.captchaMode.GetSelection() == 0 else 'fullscreen'
        config.conf["VisionAssistant"]["custom_prompts"] = self.customPrompts.Value.strip()

# --- Global Plugin ---

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    # Translators: Name of the add-on category in Input Gestures
    scriptCategory = ADDON_NAME
    
    last_translation = "" 
    is_recording = False
    temp_audio_file = os.path.join(tempfile.gettempdir(), "vision_dictate.wav")
    
    translation_cache = {}
    _last_source_text = None
    _last_params = None
    update_timer = None
    
    # Translators: Initial status when the add-on is doing nothing
    current_status = _("Idle")

    def __init__(self):
        super(GlobalPlugin, self).__init__()
        config.conf.spec["VisionAssistant"] = confspec
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SettingsPanel)
        
        self.updater = UpdateManager(GITHUB_REPO)
        
        self.refine_dlg = None
        self.refine_menu_dlg = None
        self.vision_dlg = None
        self.doc_dlg = None
        
        if config.conf["VisionAssistant"]["check_update_startup"]:
            self.update_timer = wx.CallLater(10000, self.updater.check_for_updates, True)

    def terminate(self):
        try: gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsPanel)
        except: pass
        
        if self.update_timer and self.update_timer.IsRunning():
            self.update_timer.Stop()
        
        for dlg in [self.refine_dlg, self.refine_menu_dlg, self.vision_dlg, self.doc_dlg]:
            if dlg:
                try: dlg.Destroy()
                except: pass
        
        if self.is_recording:
            try:
                ctypes.windll.winmm.mciSendStringW('close all', None, 0, 0)
            except: pass
        
        self.translation_cache = {}
        self._last_source_text = None
        gc.collect()

    def report_status(self, msg):
        self.current_status = msg
        ui.message(msg)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Announces the current status of the add-on."))
    def script_announceStatus(self, gesture):
        # Translators: Status message when the add-on is doing nothing
        idle_msg = _("Idle")
        msg = self.current_status if self.current_status else idle_msg
        ui.message(msg)

    def _browse_file(self, wildcard):
        # Translators: Standard title for opening a file
        dlg = wx.FileDialog(gui.mainFrame, _("Open"), wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        path = None
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        return path

    def _upload_file_to_gemini(self, file_path, mime_type):
        api_key = config.conf["VisionAssistant"]["api_key"].strip()
        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
        
        upload_url = f"{base_url}/upload/v1beta/files?key={api_key}"
        
        try:
            file_size = os.path.getsize(file_path)
            
            filename = os.path.basename(file_path)
            safe_filename = quote(filename)
            
            headers = {
                "X-Goog-Upload-Protocol": "raw",
                "X-Goog-Upload-Command": "start, upload, finalize",
                "X-Goog-Upload-Header-Content-Length": str(file_size),
                "X-Goog-Upload-File-Name": safe_filename,
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
            # Translators: Message of a dialog which may pop up while trying to upload a file
            msg = _("Upload Connection Error: {reason}").format(reason=e.reason)
            self.report_status(msg)
            show_error_dialog(msg)
        except error.HTTPError as e:
            # Translators: Message of a dialog which may pop up while trying to upload a file
            msg = _("Upload Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
            self.report_status(msg)
            show_error_dialog(msg)
        except Exception as e:
            # Translators: Message of a dialog which may pop up while trying to upload a file
            msg = _("File Upload Error: {error}").format(error=e)
            self.report_status(msg)
            show_error_dialog(msg)
        return None

    def _call_gemini(self, prompt_or_contents, attachments=[], json_mode=False, raise_errors=False):
        api_key = config.conf["VisionAssistant"]["api_key"].strip()
        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        model = config.conf["VisionAssistant"]["model_name"]
        
        if not api_key:
            # Translators: Message of a dialog which may pop up while performing an AI call
            msg = _("API Key missing.")
            wx.CallAfter(self.report_status, msg)
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
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }
        if json_mode: data["generationConfig"]["response_mime_type"] = "application/json"

        max_retries = 3
        for attempt in range(max_retries + 1):
            try:
                req = request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
                with request.urlopen(req, timeout=600) as response:
                    if response.status == 200:
                        res = json.loads(response.read().decode('utf-8'))
                        
                        if not res.get('candidates'):
                            return None
                            
                        candidate = res['candidates'][0]
                        
                        if candidate.get('finishReason') == 'SAFETY':
                            # Translators: Error message when AI refuses to answer due to safety guidelines
                            return _("Error: Response blocked by AI safety filters.")
                        
                        content = candidate.get('content', {})
                        parts = content.get('parts', [])
                        
                        if parts and 'text' in parts[0]:
                            text = parts[0]['text'].strip()
                            return text 
                        else:
                            return None

            except error.HTTPError as e:
                if (e.code == 503 or e.code == 429) and attempt < max_retries:
                    time.sleep(2)
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
        except error.HTTPError as e:
            if e.code == 400:
                # Translators: Message of a dialog which may pop up while performing an AI call
                msg = _("Error 400: Bad Request (Check API Key Format)")
            elif e.code == 403:
                # Translators: Message of a dialog which may pop up while performing an AI call
                msg = _("Error 403: Forbidden (Check Region/Permission)")
            elif e.code == 429:
                # Translators: Message of a dialog which may pop up while performing an AI call
                msg = _("Error 429: Quota Exceeded (Try later)")
            else:
                # Translators: Message of a dialog which may pop up while performing an AI call
                msg = _("Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
            self.report_status(msg) # Added to reset status on error
            show_error_dialog(msg)
        except error.URLError as e:
            # Translators: Message of a dialog which may pop up while performing an AI call
            msg = _("Connection Error: {reason}").format(reason=e.reason)
            self.report_status(msg) # Added to reset status on error
            show_error_dialog(msg)
        except Exception as e:
            # Translators: Message of a dialog which may pop up while performing an AI call
            msg = _("Error: {error}").format(error=e)
            self.report_status(msg) # Added to reset status on error
            show_error_dialog(msg)
        return None

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Records voice, transcribes it using AI, and types the result."))
    def script_smartDictation(self, gesture):
        if not self.is_recording:
            self.is_recording = True
            tones.beep(800, 100)
            try:
                ctypes.windll.winmm.mciSendStringW('open new type waveaudio alias myaudio', None, 0, 0)
                ctypes.windll.winmm.mciSendStringW('record myaudio', None, 0, 0)
                # Translators: Message reported when dictation starts
                msg = _("Listening...")
                self.report_status(msg)
            except Exception as e:
                # Translators: Message in an error dialog which can pop up while trying dictation.
                msg = _("Audio Hardware Error: {error}").format(error=e)
                show_error_dialog(msg)
                self.is_recording = False
        else:
            self.is_recording = False
            tones.beep(500, 100)
            try:
                ctypes.windll.winmm.mciSendStringW(f'save myaudio "{self.temp_audio_file}"', None, 0, 0)
                ctypes.windll.winmm.mciSendStringW('close myaudio', None, 0, 0)
                # Translators: Message reported when processing dictation
                msg = _("Typing...")
                self.report_status(msg)
                threading.Thread(target=self._thread_dictation, daemon=True).start()
            except Exception as e:
                # Translators: Message in an error dialog which can pop up while trying dictation.
                msg = _("Save Recording Error: {error}").format(error=e)
                show_error_dialog(msg)

    def _thread_dictation(self):
        try:
            if not os.path.exists(self.temp_audio_file): return
            
            try:
                with wave.open(self.temp_audio_file, "rb") as wave_file:
                    frame_rate = wave_file.getframerate()
                    n_frames = wave_file.getnframes()
                    duration = n_frames / float(frame_rate)
                
                if duration < 1.0:
                    # Translators: Message reported when the AI detects silence or empty speech
                    msg = _("No speech detected.")
                    wx.CallAfter(self.report_status, msg)
                    try: os.remove(self.temp_audio_file)
                    except: pass
                    return
            except Exception:
                pass

            with open(self.temp_audio_file, "rb") as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            p = 'Transcribe speech. Use native script. Fix stutters. If there is no speech, silence, or background noise only, write exactly: [[[NOSPEECH]]]'
            
            res = self._call_gemini_safe(p, attachments=[{'mime_type': 'audio/wav', 'data': audio_data}])
            
            if res:
                clean_res = res.strip()
                if "[[[NOSPEECH]]]" in clean_res:
                    # Translators: Message reported when the AI detects silence or empty speech
                    msg = _("No speech detected.")
                    wx.CallAfter(self.report_status, msg)
                else:
                    cleaned_text = clean_markdown(res)
                    wx.CallAfter(self._paste_text, cleaned_text)
            else: 
                # Translators: Message reported while trying dictation.
                msg = _("No speech recognized or Error.")
                wx.CallAfter(self.report_status, msg)
            
            try: os.remove(self.temp_audio_file)
            except: pass
        except: pass

    def _paste_text(self, text):
        api.copyToClip(text)
        send_ctrl_v()
        wx.CallLater(300, self._announce_paste, text)

    def _announce_paste(self, text):
        preview = text[:100]
        # Translators: Message reported when dictation is complete
        msg = _("Typed: {text}").format(text=preview)
        self.report_status(msg)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Translates the selected text or navigator object."))
    def script_translateSmart(self, gesture):
        text = self._get_text_smart()
        
        if not text:
            # Translators: Message reported when calling translation command
            msg = _("No text found.")
            self.report_status(msg)
            return
            
        # Translators: Message reported when calling translation command
        msg = _("Translating...")
        self.report_status(msg)
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
            clean_res = clean_markdown(res)
            self._last_source_text = text
            self._last_params = current_params
            self.last_translation = clean_res
            wx.CallAfter(self._announce_translation, clean_res)

    def _announce_translation(self, text):
        api.copyToClip(text)
        # Translators: Message reported when calling translation command
        msg = _("Translated: {text}").format(text=text)
        self.report_status(msg)

    def _get_text_smart(self):
        focus_obj = api.getFocusObject()
        if not focus_obj: return None

        if hasattr(focus_obj, "treeInterceptor") and focus_obj.treeInterceptor:
            try:
                info = focus_obj.treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
                if info and info.text and not info.text.isspace():
                    return info.text
            except: pass

        try:
            info = focus_obj.makeTextInfo(textInfos.POSITION_SELECTION)
            if info and info.text and not info.text.isspace():
                return info.text
        except: pass

        if isinstance(focus_obj, NVDAObjects.behaviors.EditableText):
            try:
                info = focus_obj.makeTextInfo(textInfos.POSITION_ALL)
                if info and info.text and not info.text.isspace():
                    return info.text
            except: pass
        
        if isinstance(focus_obj, NVDAObjects.behaviors.Terminal):
            try:
                info = focus_obj.makeTextInfo(textInfos.POSITION_ALL)
                return info.text
            except: pass

        try:
            obj = api.getNavigatorObject()
            if not obj: return None
            
            content = []
            if getattr(obj, 'name', None): content.append(obj.name)
            if getattr(obj, 'value', None): content.append(obj.value)
            if getattr(obj, 'description', None): content.append(obj.description)
            
            if hasattr(obj, 'makeTextInfo'):
                try: 
                    ti = obj.makeTextInfo(textInfos.POSITION_ALL)
                    if ti.text and len(ti.text) < 2000: 
                        content.append(ti.text)
                except: pass
                
            final_text = " ".join(list(dict.fromkeys([c for c in content if c and not c.isspace()])))
            return final_text if final_text else None
        except Exception: 
            return None

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Opens a menu to Explain, Summarize, or Fix the selected text."))
    def script_refineText(self, gesture):
        if self.refine_menu_dlg:
            self.refine_menu_dlg.Raise()
            self.refine_menu_dlg.SetFocus()
            return
        
        text = self._get_text_smart()
        if not text: text = "" 
        
        wx.CallLater(100, self._open_refine_dialog, text)

    def _open_refine_dialog(self, text):
        options = [
            # Translators: A choice in the menu of the text refinement command
            (_("Summarize"), "[summarize]"),
            # Translators: A choice in the menu of the text refinement command
            (_("Fix Grammar"), "[fix_grammar]"),
            # Translators: A choice in the menu of the text refinement command
            (_("Fix Grammar & Translate"), "[fix_translate]"),
            # Translators: A choice in the menu of the text refinement command
            (_("Explain"), "[explain]"),
        ]
        
        custom_raw = config.conf["VisionAssistant"]["custom_prompts"]
        if custom_raw:
            for line in custom_raw.split('|'):
                if ':' in line:
                    parts = line.split(':', 1)
                    name = parts[0].strip()
                    content = parts[1].strip()
                    if name and content:
                        # Translators: Prefix for custom prompts in the Refine menu                        options.append((_("Custom: ") + name, content))
        
        display_choices = [opt[0] for opt in options]
        
        self.refine_menu_dlg = wx.SingleChoiceDialog(
            gui.mainFrame,
            # Translators: Title of the Refine dialog
            _("Choose action:"),
            # Translators: main message of the Refine dialog
            _("Refine"),
            display_choices,
        )
        
        self.refine_menu_dlg.Raise()
        self.refine_menu_dlg.SetFocus()
        
        if self.refine_menu_dlg.ShowModal() == wx.ID_OK:
            selection_index = self.refine_menu_dlg.GetSelection()
            custom_content = options[selection_index][1]

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
                file_path = self._browse_file(wc)
                if file_path:
                    wx.CallLater(200, lambda: threading.Thread(target=self._thread_refine, args=(text, custom_content, file_path), daemon=True).start())
            else:
                # Translators: Message while processing request of the refine text command
                msg = _("Processing...")
                self.report_status(msg)
                threading.Thread(target=self._thread_refine, args=(text, custom_content, file_path), daemon=True).start()
        
        self.refine_menu_dlg.Destroy()
        self.refine_menu_dlg = None

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
                # Translators: Message reported when executing the refine command
                msg = _("Uploading file...")
                wx.CallAfter(self.report_status, msg)
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
            
        # Translators: Message reported when executing the refine command
        msg = _("Analyzing...")
        wx.CallAfter(self.report_status, msg)
        res = self._call_gemini_safe(prompt_text, attachments=attachments)
        
        if res:
             self.current_status = _("Idle") # Reset status on success
             wx.CallAfter(self._open_refine_result_dialog, res, attachments, text)

    def _open_refine_result_dialog(self, result_text, attachments, original_text):
        if self.refine_dlg:
            try: self.refine_dlg.Destroy()
            except: pass

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
        self.refine_dlg = VisionQADialog(
            gui.mainFrame, 
            _("{name} - Refine Result").format(name=ADDON_NAME), 
            result_text, 
            context, 
            refine_callback, 
            extra_info={'file_context': has_file_context, 'skip_init_history': False},
            raw_content=result_text,
            status_callback=self.report_status
        )
        self.refine_dlg.Show()
        self.refine_dlg.Raise()

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Recognizes text from a selected image or PDF file."))
    def script_fileOCR(self, gesture):
        wx.CallLater(100, self._open_file_ocr_dialog)

    def _open_file_ocr_dialog(self):
        wc = "Files|*.pdf;*.jpg;*.jpeg;*.png;*.webp;*.tif;*.tiff"
        path = self._browse_file(wc)
        if path:
            threading.Thread(target=self._process_file_ocr, args=(path,), daemon=True).start()

    def _process_file_ocr(self, path):
        # Translators: Message reported when calling the OCR file recognition command
        msg = _("Uploading & Extracting...")
        wx.CallAfter(self.report_status, msg)
        mime_type = get_mime_type(path)
        
        file_uri = self._upload_file_to_gemini(path, mime_type)
        
        if file_uri:
            att = [{'mime_type': mime_type, 'file_uri': file_uri}]
            
            p = "Extract all visible text from this file. Preserve original formatting (headings, lists, tables) using Markdown. Output ONLY the extracted text, without any introductory or concluding remarks."
            
            res = self._call_gemini_safe(p, attachments=att)
            if res:
                wx.CallAfter(self._open_doc_chat_dialog, res, att, "", res)
        else:
            pass

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Allows asking questions about a selected document (PDF/Text/Image)."))
    def script_analyzeDocument(self, gesture):
        wx.CallLater(100, self._open_doc_dialog)

    def _open_doc_dialog(self):
        wc = "Doc|*.pdf;*.tif;*.tiff;*.txt;*.py;*.md"
        path = self._browse_file(wc)
        if path:
            threading.Thread(target=self._process_doc_file, args=(path,), daemon=True).start()

    def _process_doc_file(self, path):
        # Translators: Message reported when calling the file analysis command
        msg = _("Uploading & Analyzing...")
        wx.CallAfter(self.report_status, msg)
        mime_type = get_mime_type(path)
        
        file_uri = self._upload_file_to_gemini(path, mime_type)
        
        if file_uri:
            att = [{'mime_type': mime_type, 'file_uri': file_uri}]
            # Translators: Initial message in document chat when calling the file analysis command
            init_msg = _("Document ready. Ask your question.")
            
            self.current_status = _("Idle") # Reset status on success
            wx.CallAfter(self._open_doc_chat_dialog, init_msg, att, "")
        else:
            self.current_status = _("Idle") # Reset status on failure
        
    def _open_doc_chat_dialog(self, init_msg, initial_attachments, doc_text, raw_text_for_save=None):
        if self.doc_dlg:
            try: 
                self.doc_dlg.Destroy()
            except: pass
            self.doc_dlg = None

        def doc_callback(ctx_atts, q, history, dum2):
            lang = config.conf["VisionAssistant"]["ai_response_language"]
            atts = ctx_atts if ctx_atts else []
            
            system_instr = (
                f"STRICTLY Respond in {lang}. "
                "Use Markdown formatting (bold, headings, lists). "
                "Analyze both text and visual elements (images/charts) to answer the request."
            )
            
            full_prompt = f"{q}\n\n[{system_instr}]"
            
            current_user_msg = {"role": "user", "parts": [{"text": full_prompt}]}
            
            messages = []
            if not history:
                parts = [{"text": f"Analyze this content. {full_prompt}"}]
                for att in atts:
                    if 'file_uri' in att:
                        parts.append({"file_data": {"mime_type": att['mime_type'], "file_uri": att['file_uri']}})
                
                return self._call_gemini_safe([{"parts": parts}]), None
            else:
                messages.extend(history)
                messages.append(current_user_msg)
                return self._call_gemini_safe(messages), None
            
        # Translators: Dialog title for a Chat dialog
        self.doc_dlg = VisionQADialog(
            gui.mainFrame, 
            _("{name} - Chat").format(name=ADDON_NAME), 
            init_msg, 
            initial_attachments, 
            doc_callback, 
            extra_info={'skip_init_history': True},
            raw_content=raw_text_for_save,
            status_callback=self.report_status
        )
        self.doc_dlg.Show()
        self.doc_dlg.Raise()

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Performs OCR and description on the entire screen."))
    def script_ocrFullScreen(self, gesture):
        self._start_vision(True)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Describes the current object (Navigator Object)."))
    def script_describeObject(self, gesture):
        self._start_vision(False)

    def _start_vision(self, full):
        if full: d, w, h = self._capture_fullscreen()
        else: d, w, h = self._capture_navigator()
        if d:
            # Translators: Message reported when calling an image analysis command
            msg = _("Scanning...")
            self.report_status(msg)
            wx.CallLater(100, lambda: threading.Thread(target=self._thread_vision, args=(d, w, h), daemon=True).start())
        else: 
            # Translators: Message reported when calling an image analysis command
            msg = _("Capture failed.")
            self.report_status(msg)

    def _thread_vision(self, img, w, h):
        lang = config.conf["VisionAssistant"]["ai_response_language"]
        
        p = (
            f"Analyze this image. Describe the layout, visible text, and UI elements. "
            f"Use Markdown formatting (headings, lists) to organize the description. "
            f"Language: {lang}. Ensure the response is strictly in {lang}. "
            "IMPORTANT: Start directly with the description content. Do not add introductory sentences like 'Here is the analysis' or 'The image shows'."
        )
        
        att = [{'mime_type': 'image/png', 'data': img}]
        res = self._call_gemini_safe(p, attachments=att)
        if res:
            self.current_status = _("Idle") # Reset status on success
            wx.CallAfter(self._open_vision_dialog, res, att, None)
        else:
            self.current_status = _("Idle") # Reset status on failure
        
    def _open_vision_dialog(self, text, atts, size):
        if self.vision_dlg:
            try: self.vision_dlg.Destroy()
            except: pass

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
        self.vision_dlg = VisionQADialog(
            gui.mainFrame, 
            _("{name} - Image Analysis").format(name=ADDON_NAME), 
            text, 
            atts, 
            cb, 
            None,
            raw_content=text,
            status_callback=self.report_status
        )
        self.vision_dlg.Show()
        self.vision_dlg.Raise()

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Transcribes a selected audio file."))
    def script_transcribeAudio(self, gesture):
        wx.CallLater(100, self._open_audio)

    def _open_audio(self):
        wc = "Audio|*.mp3;*.wav;*.ogg"
        path = self._browse_file(wc)
        if path:
            threading.Thread(target=self._thread_audio, args=(path,), daemon=True).start()

    def _thread_audio(self, path):
        try:
            # Translators: Message reported when calling the audio transcription command
            msg = _("Uploading...")
            wx.CallAfter(self.report_status, msg)
            mime_type = get_mime_type(path)
            
            file_uri = self._upload_file_to_gemini(path, mime_type)
            if not file_uri: 
                self.current_status = _("Idle") # Reset status on failure
                return

            # Translators: Message reported when calling the audio transcription command
            msg = _("Analyzing...")
            wx.CallAfter(self.report_status, msg)
            lang = config.conf["VisionAssistant"]["ai_response_language"]
            p = f"Transcribe this audio in {lang}."
            
            att = [{'mime_type': mime_type, 'file_uri': file_uri}]
            res = self._call_gemini_safe(p, attachments=att)
            
            if res:
                init_msg = res 
                self.current_status = _("Idle") # Reset status on success
                wx.CallAfter(self._open_doc_chat_dialog, init_msg, att, "", res)
            else:
                self.current_status = _("Idle") # Reset status on failure
        except: 
            # Translators: Generic error message when audio processing fails
            msg = _("Error processing audio.")
            wx.CallAfter(self.report_status, msg)
            self.current_status = _("Idle") # Reset status on failure

    # Translators: Script description for Input Gestures dialog
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
            # Translators: Message reported when calling the CAPTCHA solving command
            msg = _("Solving...")
            self.report_status(msg)
            threading.Thread(target=self._thread_cap, args=(d, is_gov), daemon=True).start()
        else: 
            # Translators: Message reported when calling the CAPTCHA solving command
            msg = _("Capture failed.")
            self.report_status(msg)
        
    def _thread_cap(self, d, is_gov):
        p = "Blind user. Return CAPTCHA code only."
        if is_gov: p += " Read 5 Persian digits, convert to English."
        else: p += " Convert to English digits."
        
        r = self._call_gemini_safe(p, attachments=[{'mime_type': 'image/png', 'data': d}])
        if r: 
            self.current_status = _("Idle") # Reset status on success
            wx.CallAfter(self._finish_captcha, r)
        else: 
            # Translators: Message reported when calling the CAPTCHA solving command
            msg = _("Failed.")
            wx.CallAfter(self.report_status, msg)
            self.current_status = _("Idle") # Reset status on failure

    def _finish_captcha(self, text):
        api.copyToClip(text)
        send_ctrl_v()
        # Translators: Message reported when calling the CAPTCHA solving command
        msg = _("Captcha: {text}").format(text=text)
        wx.CallLater(200, self.report_status, msg)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Checks for updates manually."))
    def script_checkUpdate(self, gesture):
        # Translators: Message reported when calling the update command
        msg = _("Checking for updates...")
        self.report_status(msg)
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

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Announces the last received translation."))
    def script_readLastTranslation(self, gesture):
        if self.last_translation: ui.message(f"Last: {self.last_translation}")
        else: 
            # Translators: Message called when trying to repeat the last translation
            msg = _("No history.")
            self.report_status(msg)
    
    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Translates the text currently in the clipboard."))
    def script_translateClipboard(self, gesture):
        t = api.getClipData()
        if t: 
            # Translators: Message when calling the command to translate from clipboard
            msg = _("Translating Clipboard...")
            self.report_status(msg)
            threading.Thread(target=self._thread_translate, args=(t,), daemon=True).start()
        else:
            # Translators: Message when calling the command to translate from clipboard
            msg = _("Clipboard empty.")
            self.report_status(msg)

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
        "kb:NVDA+control+shift+i": "announceStatus",
    }