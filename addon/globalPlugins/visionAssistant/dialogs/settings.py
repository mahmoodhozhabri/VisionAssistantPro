# -*- coding: utf-8 -*-
import os
import json
import threading
import logging
import time

import wx

import addonHandler
import config as nvda_config
import core
import gui
import inputCore
import keyboardHandler
import ui

from .. import vision_config
from .. import plugin_state
from ..ai.core import AIHandler
from ..utils.secure_credentials import (
    get_credential,
    protect_credential,
    prepare_backup_credentials,
    prepare_restored_credentials,
)
from ..prompt_utils import (
    normalize_ptt_key,
    ptt_key_display,
    get_configured_default_prompts,
    get_refine_menu_options,
    get_prompt_text,
    load_configured_custom_prompts,
    load_default_prompt_overrides,
    serialize_default_prompt_overrides,
    serialize_custom_prompts_v2,
)
from .prompt_manager_dialog import PromptManagerDialog

log = logging.getLogger(__name__)

addonHandler.initTranslation()


class SettingsPanel(gui.settingsDialogs.SettingsPanel):
    title = vision_config.ADDON_NAME
    def makeSettings(self, settingsSizer):
        self._all_models_backup = []
        self._temp_models = {}
        self._ptt_capture_func = None
        self._ptt_gen = 0
        self._ptt_pending_modifier = None

        self.notebook = wx.Notebook(self)

        # --- Connection Group ---
        # Translators: Title of the settings group for connection and updates
        groupLabel = _("Connection")
        self.connectionBox = wx.Panel(self.notebook)
        connectionSizer = wx.BoxSizer(wx.VERTICAL)
        cHelper = gui.guiHelper.BoxSizerHelper(self.connectionBox, sizer=connectionSizer)

        providers = [
            # Translators: Name of the Google Gemini AI provider
            (_("Google Gemini"), "gemini"),
            # Translators: Name of the OpenAI provider
            (_("OpenAI"), "openai"),
            # Translators: Name of the Mistral AI provider
            (_("Mistral AI"), "mistral"),
            # Translators: Name of the Groq AI provider
            (_("Groq"), "groq"),
            # Translators: Name of the MiniMax AI provider
            (_("MiniMax"), "minimax"),
            # Translators: Option for a user-defined custom AI provider
            (_("Custom"), "custom")
        ]
        # Translators: Label for AI Provider selection
        self.provider_sel = cHelper.addLabeledControl(_("Provider:"), wx.Choice, choices=[x[0] for x in providers])
        curr_p = nvda_config.conf["VisionAssistant"]["active_provider"]
        try:
            self.provider_sel.SetSelection(next(i for i, x in enumerate(providers) if x[1] == curr_p))
        except Exception: self.provider_sel.SetSelection(0)
        self.provider_sel.Bind(wx.EVT_CHOICE, self.onProviderChange)

        # Translators: Label for API Key input
        apiLabel = wx.StaticText(self.connectionBox, label=_("API Key (Separate multiple keys with comma or newline):"))
        cHelper.addItem(apiLabel)

        curr_key = get_credential(
            nvda_config.conf["VisionAssistant"],
            "api_key" if curr_p == "gemini" else (f"{curr_p}_api_key" if curr_p != "custom" else "custom_api_key"),
        )
        self.apiKeyCtrl_hidden = wx.TextCtrl(self.connectionBox, value=curr_key, style=wx.TE_PASSWORD)
        self.apiKeyCtrl_visible = wx.TextCtrl(self.connectionBox, value=curr_key, style=wx.TE_MULTILINE | wx.TE_DONTWRAP, size=(-1, 60))
        self.apiKeyCtrl_visible.Hide()
        cHelper.addItem(self.apiKeyCtrl_hidden)
        cHelper.addItem(self.apiKeyCtrl_visible)

        # Translators: Checkbox to toggle API Key visibility
        self.showApiCheck = wx.CheckBox(self.connectionBox, label=_("Show API Key"))
        self.showApiCheck.Bind(wx.EVT_CHECKBOX, self.onToggleApiVisibility)
        cHelper.addItem(self.showApiCheck)

        # Custom Fields Box
        # Translators: Static box title for custom AI provider settings
        self.customBox = wx.StaticBox(self.connectionBox, label=_("Custom Provider Settings"))
        self.customSizer = wx.StaticBoxSizer(self.customBox, wx.VERTICAL)

        self.btn_setup_local_ai = wx.Button(self.customBox, label=_("Setup Local AI"))
        self.btn_setup_local_ai.Bind(wx.EVT_BUTTON, self.onSetupLocalAI)
        self.customSizer.Add(self.btn_setup_local_ai, 0, wx.ALL, 5)

        # Translators: Label for Custom API URL input
        self.customSizer.Add(wx.StaticText(self.customBox, label=_("API URL:")), 0, wx.ALL, 2)
        self.customUrl = wx.TextCtrl(self.customBox, value=nvda_config.conf["VisionAssistant"]["custom_api_url"])
        self.customSizer.Add(self.customUrl, 0, wx.EXPAND | wx.ALL, 2)
        self.customUrl.Bind(wx.EVT_TEXT, self.onCustomUrlChange)
        # Translators: Label for Custom API Type selection
        self.customSizer.Add(wx.StaticText(self.customBox, label=_("API Type:")), 0, wx.ALL, 2)
        # Translators: AI API compatibility types
        self.customType = wx.Choice(self.customBox, choices=[_("OpenAI Compatible"), _("Gemini Compatible")])
        self.customType.Bind(wx.EVT_CHOICE, self.onCustomTypeChange)
        self.customType.SetSelection(0 if nvda_config.conf["VisionAssistant"]["custom_api_type"] == "openai" else 1)
        self.customSizer.Add(self.customType, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom Model Name input
        self.lbl_customModelName = wx.StaticText(self.customBox, label=_("Model Name (Manual):"))
        self.customSizer.Add(self.lbl_customModelName, 0, wx.ALL, 2)
        self.customModelName = wx.TextCtrl(self.customBox, value=nvda_config.conf["VisionAssistant"]["custom_model_name"])
        self.customSizer.Add(self.customModelName, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Checkbox to indicate if custom provider supports file upload
        self.customUploadSupport = wx.CheckBox(self.customBox, label=_("Supports File Upload"))
        self.customUploadSupport.Value = nvda_config.conf["VisionAssistant"]["custom_upload_support"]
        self.customUploadSupport.Bind(wx.EVT_CHECKBOX, self.onCustomUploadSupportChange)
        self.customSizer.Add(self.customUploadSupport, 0, wx.ALL, 5)

        # Advanced Endpoints Section
        # Translators: Checkbox to toggle advanced endpoint URLs
        self.useAdvancedEndpoints = wx.CheckBox(self.customBox, label=_("Advanced Endpoint Configuration"))
        self.useAdvancedEndpoints.Value = nvda_config.conf["VisionAssistant"]["use_advanced_endpoints"]
        self.useAdvancedEndpoints.Bind(wx.EVT_CHECKBOX, self.onToggleAdvanced)
        self.customSizer.Add(self.useAdvancedEndpoints, 0, wx.ALL, 5)

        self.advEndpointBox = wx.Panel(self.customBox)
        advVBox = wx.BoxSizer(wx.VERTICAL)

        # Translators: Label for Custom Models List URL
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Models List URL:")), 0, wx.ALL, 2)
        self.customModelsUrl = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_models_url"])
        advVBox.Add(self.customModelsUrl, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom OCR URL
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("OCR Endpoint URL:")), 0, wx.ALL, 2)
        self.customOcrUrl = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_ocr_url"])
        advVBox.Add(self.customOcrUrl, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom OCR Model
        self.lblCustomOcrModel = wx.StaticText(self.advEndpointBox, label=_("Custom OCR Model (Optional):"))
        advVBox.Add(self.lblCustomOcrModel, 0, wx.ALL, 2)
        self.customOcrModel = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_ocr_model"])
        advVBox.Add(self.customOcrModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom STT URL
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Speech-to-Text (STT) URL:")), 0, wx.ALL, 2)
        self.customSttUrl = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_stt_url"])
        advVBox.Add(self.customSttUrl, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom STT Model
        self.lblCustomSttModel = wx.StaticText(self.advEndpointBox, label=_("Custom STT Model (Optional):"))
        advVBox.Add(self.lblCustomSttModel, 0, wx.ALL, 2)
        self.customSttModel = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_stt_model"])
        advVBox.Add(self.customSttModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom TTS URL
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Text-to-Speech (TTS) URL:")), 0, wx.ALL, 2)
        self.customTtsUrl = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_tts_url"])
        advVBox.Add(self.customTtsUrl, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom TTS Model
        self.lblCustomTtsModel = wx.StaticText(self.advEndpointBox, label=_("Custom TTS Model (Optional):"))
        advVBox.Add(self.lblCustomTtsModel, 0, wx.ALL, 2)
        self.customTtsModel = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_tts_model"])
        advVBox.Add(self.customTtsModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for a text field in the "Custom Provider Settings" section of settings where the user enters the AI Operator URL.
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("AI Operator URL:")), 0, wx.ALL, 2)
        self.customAssistantUrl = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"].get("custom_operator_url", ""))
        advVBox.Add(self.customAssistantUrl, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for a text field in the "Custom Provider Settings" section of settings where the user manually enters the model name for AI Operator.
        self.lblCustomOperatorModel = wx.StaticText(self.advEndpointBox, label=_("Custom Operator Model (Optional):"))
        advVBox.Add(self.lblCustomOperatorModel, 0, wx.ALL, 2)
        self.customAssistantModel = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_operator_model"])
        advVBox.Add(self.customAssistantModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom TTS Voice Name
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Custom TTS Voice Name (Optional):")), 0, wx.ALL, 2)
        self.customTtsVoice = wx.TextCtrl(self.advEndpointBox, value=nvda_config.conf["VisionAssistant"]["custom_tts_voice"])
        advVBox.Add(self.customTtsVoice, 0, wx.EXPAND | wx.ALL, 2)

        self.advEndpointBox.SetSizer(advVBox)
        self.customSizer.Add(self.advEndpointBox, 0, wx.EXPAND)
        self.advEndpointBox.Show(self.useAdvancedEndpoints.Value)
        cHelper.addItem(self.customSizer)

        # Standard Fetch & Model Logic
        # Translators: Button to fetch available models from the selected provider
        self.btn_fetch = wx.Button(self.connectionBox, label=_("Fetch Models"))
        self.btn_fetch.Bind(wx.EVT_BUTTON, self.onFetchModels)
        cHelper.addItem(self.btn_fetch)

        self.modelLabel = wx.StaticText(self.connectionBox, label=_("AI Model:"))
        cHelper.addItem(self.modelLabel)
        # Translators: Label for AI Model selection choice box
        self.model = wx.ComboBox(self.connectionBox, style=wx.TE_PROCESS_ENTER, name=_("AI Model:"))
        self.model.Bind(wx.EVT_TEXT, self.onModelFilter)
        cHelper.addItem(self.model)

        # Advanced Model Routing Box
        # Translators: Checkbox to toggle advanced model routing
        self.advRoutingCheck = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Advanced Model Routing (Task-specific)")))
        self.advRoutingCheck.Value = nvda_config.conf["VisionAssistant"].get("advanced_model_routing", False)
        self.advRoutingCheck.Bind(wx.EVT_CHECKBOX, self.onToggleAdvRouting)

        self.advRoutingBox = wx.Panel(self.connectionBox)
        advRSizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label for OCR model selection
        self.lbl_advOcr = wx.StaticText(self.advRoutingBox, label=_("OCR / Vision Model:"))
        advRSizer.Add(self.lbl_advOcr, 0, wx.ALL, 2)
        self.advOcrModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advOcrModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advOcrModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for STT model selection
        self.lbl_advStt = wx.StaticText(self.advRoutingBox, label=_("Speech-to-Text (STT) Model:"))
        advRSizer.Add(self.lbl_advStt, 0, wx.ALL, 2)
        self.advSttModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advSttModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advSttModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for TTS model selection (Assigning to self to toggle visibility)
        self.lbl_advTts = wx.StaticText(self.advRoutingBox, label=_("Text-to-Speech (TTS) Model:"))
        advRSizer.Add(self.lbl_advTts, 0, wx.ALL, 2)
        self.advTtsModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advTtsModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advTtsModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for a dropdown menu in the "Advanced Model Routing" section of settings to choose a specific model for AI Operator tasks.
        self.lbl_advOperator = wx.StaticText(self.advRoutingBox, label=_("AI Operator / CAPTCHA Model:"))
        advRSizer.Add(self.lbl_advOperator, 0, wx.ALL, 2)
        self.advOperatorModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advOperatorModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advOperatorModel, 0, wx.EXPAND | wx.ALL, 2)
        # Translators: Label for the Video Analysis model selection in the Advanced Model Routing section.
        self.lbl_advVideo = wx.StaticText(self.advRoutingBox, label=_("Video Analysis Model (Gemini only):"))
        advRSizer.Add(self.lbl_advVideo, 0, wx.ALL, 2)
        self.advVideoModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advVideoModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advVideoModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for the Live Assistant model selection in the Advanced Model Routing section (Gemini only).
        self.lbl_advLive = wx.StaticText(self.advRoutingBox, label=_("Live Assistant Model (Gemini only):"))
        advRSizer.Add(self.lbl_advLive, 0, wx.ALL, 2)
        self.advLiveModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advLiveModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advLiveModel, 0, wx.EXPAND | wx.ALL, 2)

        self.advRoutingBox.SetSizer(advRSizer)
        cHelper.addItem(self.advRoutingBox)

        # Translators: Label for Proxy URL input
        self.proxyUrl = cHelper.addLabeledControl(_("Proxy URL:"), wx.TextCtrl)
        self.proxyUrl.Value = nvda_config.conf["VisionAssistant"]["proxy_url"]

        # Translators: Checkbox to enable/disable automatic update checks on startup
        self.checkUpdateStartup = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Check for updates on startup")))
        self.checkUpdateStartup.Value = nvda_config.conf["VisionAssistant"]["check_update_startup"]
        # Translators: Checkbox to toggle markdown cleaning in chat windows
        self.cleanMarkdown = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Clean Markdown in Chat")))
        self.cleanMarkdown.Value = nvda_config.conf["VisionAssistant"]["clean_markdown_chat"]
        # Translators: Checkbox to enable copying AI responses to clipboard
        self.copyToClipboard = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Copy AI responses to clipboard")))
        self.copyToClipboard.Value = nvda_config.conf["VisionAssistant"]["copy_to_clipboard"]
        # Translators: Checkbox to skip chat window and only speak AI responses
        self.skipChatDialog = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Direct Output (No Chat Window)")))
        self.skipChatDialog.Value = nvda_config.conf["VisionAssistant"]["skip_chat_dialog"]
        self.connectionBox.SetSizer(connectionSizer)
        self.notebook.AddPage(self.connectionBox, groupLabel)

        # --- Live Assistant Group ---
        # Translators: Title of the settings group for Live Assistant features.
        groupLabel = _("Live Assistant")
        self.livePanel = wx.Panel(self.notebook)
        liveSizer = wx.BoxSizer(wx.VERTICAL)
        lvHelper = gui.guiHelper.BoxSizerHelper(self.livePanel, sizer=liveSizer)

        # Translators: Checkbox to start the Live Assistant without its conversation window (open it later with the Show Last Result key).
        self.liveDirectOutput = lvHelper.addItem(wx.CheckBox(self.livePanel, label=_("Live Assistant: Direct Output (No Window)")))
        self.liveDirectOutput.Value = nvda_config.conf["VisionAssistant"]["live_direct_output"]

        # Translators: Checkbox to enable push-to-talk mode for the Live Assistant.
        self.pttCheck = lvHelper.addItem(wx.CheckBox(self.livePanel, label=_("Push to Talk")))
        self.pttCheck.Value = nvda_config.conf["VisionAssistant"].get("live_push_to_talk", False)
        self.pttCheck.Bind(wx.EVT_CHECKBOX, self.onTogglePtt)

        # Translators: Label for the push-to-talk key field, instructing the user to press the keys to record it.
        self.lblPttKey = wx.StaticText(self.livePanel, label=_("Push to Talk Key (press the keys to record, for example F12 or Ctrl+F12):"))
        lvHelper.addItem(self.lblPttKey)
        self.pttKeyCtrl = wx.TextCtrl(self.livePanel, value=ptt_key_display(nvda_config.conf["VisionAssistant"].get("live_ptt_key", "")))
        self.pttKeyCtrl.Bind(wx.EVT_SET_FOCUS, self._on_ptt_key_focus)
        self.pttKeyCtrl.Bind(wx.EVT_KILL_FOCUS, self._on_ptt_key_kill_focus)
        lvHelper.addItem(self.pttKeyCtrl)

        self.livePanel.SetSizer(liveSizer)
        self.notebook.AddPage(self.livePanel, groupLabel)

        # --- AI Behavior Group ---
        # Translators: Title of the settings group for AI behavior
        groupLabel = _("AI Behavior")
        aiBox = wx.Panel(self.notebook)
        aiSizer = wx.BoxSizer(wx.VERTICAL)
        aiHelper = gui.guiHelper.BoxSizerHelper(aiBox, sizer=aiSizer)
        # Translators: Label for AI Temperature setting
        tempLabelText = _("Creativity (Temperature, does not affect OCR/Translation):")
        temp_choices = [f"{x/10:.1f}" for x in range(0, 21)]
        self.aiTemp = aiHelper.addLabeledControl(tempLabelText, wx.Choice, choices=temp_choices)
        current_temp = str(nvda_config.conf["VisionAssistant"].get("ai_temperature", 0.7))
        idx = self.aiTemp.FindString(current_temp)
        if idx != wx.NOT_FOUND: self.aiTemp.SetSelection(idx)
        else: self.aiTemp.SetSelection(7)
        aiBox.SetSizer(aiSizer)
        self.notebook.AddPage(aiBox, groupLabel)

        # --- Translation Languages Group ---
        # Translators: Title of the settings group for translation languages configuration
        groupLabel = _("Translation Languages")
        langBox = wx.Panel(self.notebook)
        langSizer = wx.BoxSizer(wx.VERTICAL)
        lHelper = gui.guiHelper.BoxSizerHelper(langBox, sizer=langSizer)
        self.sourceLang = lHelper.addLabeledControl(_("Source:"), wx.Choice, choices=vision_config.SOURCE_NAMES)
        curr_s_code = nvda_config.conf["VisionAssistant"]["source_language"]
        s_idx = next((i for i, x in enumerate(vision_config.SOURCE_LIST) if x[1] == curr_s_code), 0)
        self.sourceLang.SetSelection(s_idx)
        # Translators: Checkbox to enable translation
        self.targetLang = lHelper.addLabeledControl(_("Target:"), wx.Choice, choices=vision_config.TARGET_NAMES)
        curr_t_code = nvda_config.conf["VisionAssistant"]["target_language"]
        t_idx = next((i for i, x in enumerate(vision_config.TARGET_LIST) if x[1] == curr_t_code), 0)
        self.targetLang.SetSelection(t_idx)
        # Translators: Label for Target Language selection
        self.aiResponseLang = lHelper.addLabeledControl(_("AI Response:"), wx.Choice, choices=vision_config.TARGET_NAMES)
        curr_ai_code = nvda_config.conf["VisionAssistant"]["ai_response_language"]
        ai_idx = next((i for i, x in enumerate(vision_config.TARGET_LIST) if x[1] == curr_ai_code), 0)
        self.aiResponseLang.SetSelection(ai_idx)
        # Translators: Checkbox for Smart Swap feature
        self.smartSwap = lHelper.addItem(wx.CheckBox(langBox, label=_("Smart Swap")))
        self.smartSwap.Value = nvda_config.conf["VisionAssistant"]["smart_swap"]
        langBox.SetSizer(langSizer)
        self.notebook.AddPage(langBox, groupLabel)

        # --- Document Reader Settings ---
        # Translators: Title of settings group for Document Reader features
        groupLabel = _("Document Reader")
        self.docBox = wx.Panel(self.notebook)
        docSizer = wx.BoxSizer(wx.VERTICAL)
        dHelper = gui.guiHelper.BoxSizerHelper(self.docBox, sizer=docSizer)
        # Translators: Label for OCR Engine selection
        self.ocr_sel = dHelper.addLabeledControl(_("OCR Engine:"), wx.Choice, choices=[x[0] for x in vision_config.OCR_ENGINES])
        curr_ocr = nvda_config.conf["VisionAssistant"]["ocr_engine"]
        try:
            o_idx = next(i for i, v in enumerate(vision_config.OCR_ENGINES) if v[1] == curr_ocr)
            self.ocr_sel.SetSelection(o_idx)
        except Exception: self.ocr_sel.SetSelection(0)

        # Translators: Label for the OCR batch size setting. Set to 0 to process all pages in a single request.
        self.lbl_batch = wx.StaticText(self.docBox, label=_("OCR Batch Size (Pages per request, 0 to disable):"))
        dHelper.addItem(self.lbl_batch)
        self.batch_size = wx.SpinCtrl(self.docBox, min=0, max=100, initial=nvda_config.conf["VisionAssistant"]["ocr_batch_size"])
        dHelper.addItem(self.batch_size)

        # Translators: Label for the checkbox that enables image descriptions during OCR
        self.chk_describe_images = wx.CheckBox(self.docBox, label=_("Describe images inline during document OCR"))
        self.chk_describe_images.SetValue(nvda_config.conf["VisionAssistant"].get("describe_images_ocr", True))
        dHelper.addItem(self.chk_describe_images)

        # Translators: Label for the checkbox that enables page numbers when exporting documents
        self.chk_export_page_numbers = wx.CheckBox(self.docBox, label=_("Include page numbers when exporting documents"))
        self.chk_export_page_numbers.SetValue(nvda_config.conf["VisionAssistant"].get("document_export_page_numbers", True))
        dHelper.addItem(self.chk_export_page_numbers)

        self.lbl_voice = wx.StaticText(self.docBox, label=_("TTS Voice:"))
        dHelper.addItem(self.lbl_voice)
        self.voice_sel = wx.Choice(self.docBox, choices=[])
        self.voice_sel.Bind(wx.EVT_CHOICE, self.onVoiceSelectionChanged)
        dHelper.addItem(self.voice_sel)
        self.docBox.SetSizer(docSizer)
        self.notebook.AddPage(self.docBox, groupLabel)

        # --- Video Settings Group ---
        self.vidPanel = wx.Panel(self.notebook)
        # Translators: Labels for the AI and User in chat history
        groupLabel = _("Video")
        vidSizer = wx.BoxSizer(wx.VERTICAL)
        vHelper = gui.guiHelper.BoxSizerHelper(self.vidPanel, sizer=vidSizer)

        # Translators: Label for Video Chunk Size setting. Explains the trade-off between chunk size, API requests, and description quality.
        self.lbl_vid_chunk = wx.StaticText(self.vidPanel, label=_("Video Chunk Size for Audio Description (Minutes, 0 to disable):\nTip: Higher values use fewer API requests but rely on luck to succeed. Lower values guarantee highly detailed and precise descriptions."))
        vHelper.addItem(self.lbl_vid_chunk)
        self.vid_chunk_size = wx.SpinCtrl(self.vidPanel, min=0, max=300, initial=nvda_config.conf["VisionAssistant"]["video_srt_chunk_minutes"])
        vHelper.addItem(self.vid_chunk_size)

        # Translators: Checkbox label to add character list as the first subtitle in video SRT output.
        self.vid_chars_as_sub = wx.CheckBox(self.vidPanel, label=_("Add character list as first subtitle"))
        self.vid_chars_as_sub.SetValue(nvda_config.conf["VisionAssistant"].get("video_chars_as_subtitle", True))
        vHelper.addItem(self.vid_chars_as_sub)

        # Translators: Checkbox label to add an AI warning disclaimer at the beginning of the video SRT output.
        self.vid_add_disclaimer = wx.CheckBox(self.vidPanel, label=_("Add AI disclaimer at the beginning"))
        self.vid_add_disclaimer.SetValue(nvda_config.conf["VisionAssistant"].get("video_add_disclaimer", True))
        vHelper.addItem(self.vid_add_disclaimer)
        self.vidPanel.SetSizer(vidSizer)
        self.notebook.AddPage(self.vidPanel, groupLabel)

        # --- CAPTCHA Group ---
        groupLabel = _("CAPTCHA")
        capBox = wx.Panel(self.notebook)
        capSizer = wx.BoxSizer(wx.VERTICAL)
        capHelper = gui.guiHelper.BoxSizerHelper(capBox, sizer=capSizer)

        # Translators: Label for the checkbox that enables or disables the automated CAPTCHA solver feature.
        self.enableVisualCaptcha = capHelper.addItem(wx.CheckBox(capBox, label=_("Enable Visual CAPTCHA Solver")))
        self.enableVisualCaptcha.Value = nvda_config.conf["VisionAssistant"].get("enable_visual_captcha_solver", True)

        # Translators: Label for CAPTCHA capture method selection.
        self.captchaMode = capHelper.addLabeledControl(_("Text CAPTCHA Method:"), wx.Choice, choices=[
            # Translators: A choice for capture method. Captures only the specific object under the cursor.
            _("Navigator Object"),
            # Translators: A choice for capture method. Captures the entire visible screen area.
            _("Full Screen")
        ])

        self.captchaMode.SetSelection(0 if nvda_config.conf["VisionAssistant"]["captcha_mode"] == 'navigator' else 1)
        capBox.SetSizer(capSizer)
        self.notebook.AddPage(capBox, groupLabel)

        self.defaultPromptItems = get_configured_default_prompts()
        self.customPromptItems = load_configured_custom_prompts()

        # --- Prompts Group ---
        # Translators: Title of the settings group for prompt management.
        groupLabel = _("Prompts")
        promptsBox = wx.Panel(self.notebook)
        promptsSizer = wx.BoxSizer(wx.VERTICAL)
        pHelper = gui.guiHelper.BoxSizerHelper(promptsBox, sizer=promptsSizer)
        # Translators: Description for the prompt manager button.
        pHelper.addItem(wx.StaticText(promptsBox, label=_("Manage default and custom prompts.")))
        # Translators: Button label to open prompt manager dialog.
        self.managePromptsBtn = wx.Button(promptsBox, label=_("Manage Prompts..."))
        self.managePromptsBtn.Bind(wx.EVT_BUTTON, self.onManagePrompts)
        pHelper.addItem(self.managePromptsBtn)
        self.promptsSummary = wx.StaticText(promptsBox)
        pHelper.addItem(self.promptsSummary)
        self._refreshPromptSummary()
        promptsBox.SetSizer(promptsSizer)
        self.notebook.AddPage(promptsBox, groupLabel)

        # --- Advanced Group ---
        # Translators: Title of the advanced settings tab
        groupLabel = _("Advanced")
        advBox = wx.Panel(self.notebook)
        advSizer = wx.BoxSizer(wx.VERTICAL)
        aHelper = gui.guiHelper.BoxSizerHelper(advBox, sizer=advSizer)

        # Translators: Group box title for log management settings
        logMgmtBox = wx.StaticBox(advBox, label=_("Log Management"))
        logMgmtSizer = wx.StaticBoxSizer(logMgmtBox, wx.VERTICAL)
        logHelper = gui.guiHelper.BoxSizerHelper(logMgmtBox, sizer=logMgmtSizer)

        # Translators: Checkbox label to enable dedicated add-on logging to file
        self.enableFileLogging = logHelper.addItem(wx.CheckBox(logMgmtBox, label=_("Enable dedicated log file")))
        self.enableFileLogging.Value = nvda_config.conf["VisionAssistant"].get("enable_file_logging", False)

        self.logLevels = [
            # Translators: Log level choice: Debug (Logs all detailed technical events, API calls, and raw responses)
            (_("Debug (All Details)"), "DEBUG"),
            # Translators: Log level choice: Info (Logs general operational events and task completions)
            (_("Info (General Information)"), "INFO"),
            # Translators: Log level choice: Warning (Logs warnings and non-fatal retries)
            (_("Warning (Warnings Only)"), "WARNING"),
            # Translators: Log level choice: Error (Logs errors and critical exceptions only)
            (_("Error (Errors Only)"), "ERROR")
        ]
        # Translators: Label for Log Level selection
        self.logLevelSel = logHelper.addLabeledControl(_("Log Level:"), wx.Choice, choices=[x[0] for x in self.logLevels])
        curr_log_lvl = nvda_config.conf["VisionAssistant"].get("log_level", "DEBUG")
        try:
            lvl_idx = next(i for i, x in enumerate(self.logLevels) if x[1] == curr_log_lvl)
            self.logLevelSel.SetSelection(lvl_idx)
        except Exception:
            self.logLevelSel.SetSelection(0)

        self.logRetentionChoices = vision_config.LOG_RETENTION_OPTIONS
        # Translators: Label for Log Retention Duration selection
        self.logRetentionSel = logHelper.addLabeledControl(_("Keep Logs For:"), wx.Choice, choices=[x[0] for x in self.logRetentionChoices])
        curr_ret_hrs = nvda_config.conf["VisionAssistant"].get("log_retention_hours", 168)
        try:
            ret_idx = next(i for i, x in enumerate(self.logRetentionChoices) if x[1] == curr_ret_hrs)
            self.logRetentionSel.SetSelection(ret_idx)
        except Exception:
            self.logRetentionSel.SetSelection(6)

        # Translators: Group box title for log management buttons
        logBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Translators: Button to open log file
        self.btnOpenLogFile = wx.Button(logMgmtBox, label=_("Open Log File"))
        self.btnOpenLogFile.Bind(wx.EVT_BUTTON, self.onOpenLogFile)
        logBtnSizer.Add(self.btnOpenLogFile, 0, wx.ALL, 5)

        # Translators: Button to open log folder
        self.btnOpenLogFolder = wx.Button(logMgmtBox, label=_("Open Log Folder"))
        self.btnOpenLogFolder.Bind(wx.EVT_BUTTON, self.onOpenLogFolder)
        logBtnSizer.Add(self.btnOpenLogFolder, 0, wx.ALL, 5)

        # Translators: Button to clear log file
        self.btnClearLogFile = wx.Button(logMgmtBox, label=_("Clear Log File"))
        self.btnClearLogFile.Bind(wx.EVT_BUTTON, self.onClearLogFile)
        logBtnSizer.Add(self.btnClearLogFile, 0, wx.ALL, 5)

        logMgmtSizer.Add(logBtnSizer, 0, wx.EXPAND | wx.ALL, 5)

        aHelper.addItem(logMgmtSizer)

        # Translators: Group box title for the settings backup and restore buttons
        backupBox = wx.StaticBox(advBox, label=_("Backup and Restore"))
        backupSizer = wx.StaticBoxSizer(backupBox, wx.VERTICAL)

        # Translators: Checkbox controlling whether API keys remain encrypted in settings backup files.
        self.protectBackupKeysCheck = wx.CheckBox(
            advBox,
            label=_("Protect API keys in backup files (recommended)"),
        )
        self.protectBackupKeysCheck.SetValue(
            nvda_config.conf["VisionAssistant"].get("protect_api_keys_in_backups", True)
        )
        self.protectBackupKeysCheck.SetToolTip(
            _("When disabled, backup JSON files contain plaintext API keys so they can be transferred to another Windows account or computer.")
        )
        self.protectBackupKeysCheck.Bind(wx.EVT_CHECKBOX, self.onToggleBackupKeyProtection)
        backupSizer.Add(self.protectBackupKeysCheck, 0, wx.ALL, 5)

        backupButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Translators: Button to save add-on settings and data to a backup file
        self.btnBackupSettings = wx.Button(advBox, label=_("Backup..."))
        self.btnBackupSettings.Bind(wx.EVT_BUTTON, self.onBackupSettings)
        backupButtonSizer.Add(self.btnBackupSettings, 0, wx.ALL, 5)

        # Translators: Button to restore add-on settings and data from a backup file
        self.btnRestoreSettings = wx.Button(advBox, label=_("Restore..."))
        self.btnRestoreSettings.Bind(wx.EVT_BUTTON, self.onRestoreSettings)
        backupButtonSizer.Add(self.btnRestoreSettings, 0, wx.ALL, 5)

        backupSizer.Add(backupButtonSizer, 0, wx.EXPAND)

        aHelper.addItem(backupSizer)
        advBox.SetSizer(advSizer)
        self.notebook.AddPage(advBox, groupLabel)

        settingsSizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        self.refreshModelList(curr_p)
        self.updateVoiceList(curr_p)
        self.updateCustomFieldsVisibility(curr_p)


    def updateVoiceList(self, p_name):
        self.voice_sel.Clear()
        if p_name == "openai" or p_name == "custom":
            voices = vision_config.OPENAI_VOICES
        else:
            voices = AIHandler.get_voices(p_name) or vision_config.GEMINI_VOICES
        for v in voices:
            self.voice_sel.Append(f"{v[0]} - {v[1]}", v[0])
        if p_name == "minimax":
            threading.Thread(target=self._refresh_minimax_voices, daemon=True).start()
        else:
            curr_voice = nvda_config.conf["VisionAssistant"].get("tts_voice", "Puck")
            self._select_voice_in_list(curr_voice)

    def _refresh_minimax_voices(self):
        try:
            nvda_config.conf["VisionAssistant"]["minimax_voices_cache"] = ""
            nvda_config.conf["VisionAssistant"]["minimax_voices_cache_time"] = 0
            voices = AIHandler.get_voices("minimax")
            if voices and hasattr(self, 'voice_sel'):
                wx.CallAfter(self._populate_voice_sel, voices)
        except Exception as e:
            log.warning(f"Background MiniMax voice refresh failed: {e}")

    def _populate_voice_sel(self, voices):
        try:
            self.voice_sel.Clear()
            for v in voices:
                self.voice_sel.Append(f"{v[0]} - {v[1]}", v[0])
            curr_voice = nvda_config.conf["VisionAssistant"].get("tts_voice", "English_expressive_narrator")
            self._select_voice_in_list(curr_voice)
        except Exception as e:
            log.warning(f"Failed to populate voice_sel: {e}")

    def _select_voice_in_list(self, voice_id):
        try:
            for i in range(self.voice_sel.GetCount()):
                if self.voice_sel.GetClientData(i) == voice_id:
                    self.voice_sel.SetSelection(i)
                    return
            if self.voice_sel.GetCount() > 0:
                self.voice_sel.SetSelection(0)
        except Exception:
            pass

    def _refreshPromptSummary(self):
        # Translators: Summary text for prompt counts in settings.
        summary = _("Default prompts: {defaultCount}, Custom prompts: {customCount}").format(
            defaultCount=len(self.defaultPromptItems),
            customCount=len(self.customPromptItems),
        )
        self.promptsSummary.SetLabel(summary)

    def onManagePrompts(self, event):
        top = wx.GetTopLevelParent(self)
        gui.mainFrame.prePopup()
        try:
            dlg = PromptManagerDialog(
                self,
                self.defaultPromptItems,
                self.customPromptItems,
                vision_config.PROMPT_VARIABLES_GUIDE,
            )
            if dlg.ShowModal() == wx.ID_OK:
                self.defaultPromptItems = dlg.get_default_items()
                self.customPromptItems = dlg.get_custom_items()
                self._refreshPromptSummary()
            dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()
            if top:
                top.Enable(True)
                top.SetFocus()

    def _live_supported_for(self, provider):
        if provider == "gemini":
            return True
        if provider == "custom":
            if hasattr(self, "customType") and self.customType.GetSelection() != wx.NOT_FOUND:
                return self.customType.GetSelection() == 1
            return nvda_config.conf["VisionAssistant"].get("custom_api_type", "openai") == "gemini"
        return False

    def updateCustomFieldsVisibility(self, provider):
        is_custom = (provider == "custom")
        self.customBox.Show(is_custom)
        self.advRoutingCheck.Show(True)

        tts_supported = AIHandler.is_tts_supported(provider)
        routing_enabled = self.advRoutingCheck.Value
        self.advRoutingBox.Show(routing_enabled)

        live_supported = self._live_supported_for(provider)
        ptt_on = live_supported and self.pttCheck.Value
        self.liveDirectOutput.Show(live_supported)
        self.pttCheck.Show(live_supported)
        self.lblPttKey.Show(ptt_on)
        self.pttKeyCtrl.Show(ptt_on)

        if routing_enabled:
            self.advOcrModel.Show(True)
            self.advSttModel.Show(True)
            self.advTtsModel.Show(tts_supported)
            self.lbl_advTts.Show(tts_supported)
            self.advOperatorModel.Show(True)
            self.lbl_advOperator.Show(True)
            self.advVideoModel.Show(live_supported)
            self.lbl_advVideo.Show(live_supported)
            self.advLiveModel.Show(live_supported)
            self.lbl_advLive.Show(live_supported)

        self.voice_sel.Show(tts_supported)
        self.lbl_voice.Show(tts_supported)
        self.btn_fetch.Show(True)

        has_fetched_models = self.model.GetCount() > 0
        if is_custom:
            self.modelLabel.Show(has_fetched_models)
            self.model.Show(has_fetched_models)

            if hasattr(self, 'lbl_customModelName'):
                self.lbl_customModelName.Show(not has_fetched_models)
            self.customModelName.Show(not has_fetched_models)

            self.advEndpointBox.Show(self.useAdvancedEndpoints.Value)

            show_manual_fields = self.useAdvancedEndpoints.Value and not has_fetched_models

            if hasattr(self, 'lblCustomOcrModel'):
                self.lblCustomOcrModel.Show(show_manual_fields)
            self.customOcrModel.Show(show_manual_fields)

            if hasattr(self, 'lblCustomSttModel'):
                self.lblCustomSttModel.Show(show_manual_fields)
            self.customSttModel.Show(show_manual_fields)

            if hasattr(self, 'lblCustomTtsModel'):
                self.lblCustomTtsModel.Show(show_manual_fields)
            self.customTtsModel.Show(show_manual_fields)

            if hasattr(self, 'lblCustomOperatorModel'):
                self.lblCustomOperatorModel.Show(show_manual_fields)
            self.customAssistantModel.Show(show_manual_fields)

            self.customTtsVoice.Show(self.useAdvancedEndpoints.Value)
        else:
            self.modelLabel.Show(True)
            self.model.Show(True)
            if hasattr(self, 'lbl_customModelName'):
                self.lbl_customModelName.Show(False)
            self.customModelName.Hide()

        if hasattr(self, 'advEndpointBox'):
            self.advEndpointBox.Layout()
        self.connectionBox.Layout()
        self.Layout()
        is_gemini_api = False
        if provider == "gemini":
            is_gemini_api = True
        elif provider == "custom":
            custom_type_idx = self.customType.GetSelection()
            if custom_type_idx != wx.NOT_FOUND:
                is_gemini_api = (custom_type_idx == 1)
            else:
                is_gemini_api = (nvda_config.conf["VisionAssistant"].get("custom_api_type") == "gemini")

        if hasattr(self, 'notebook'):
            if hasattr(self, 'vidPanel'):
                vid_index = -1
                for i in range(self.notebook.GetPageCount()):
                    if self.notebook.GetPage(i) == self.vidPanel:
                        vid_index = i
                        break
                
                if is_gemini_api and vid_index == -1:
                    self.notebook.InsertPage(4, self.vidPanel, _("Video"))
                elif not is_gemini_api and vid_index != -1:
                    self.notebook.RemovePage(vid_index)

            if hasattr(self, 'aiTemp'):
                ai_box = self.aiTemp.GetParent()
                ai_index = -1
                for i in range(self.notebook.GetPageCount()):
                    if self.notebook.GetPage(i) == ai_box:
                        ai_index = i
                        break
                
                if not is_gemini_api and ai_index == -1:
                    self.notebook.InsertPage(1, ai_box, _("AI Behavior"))
                elif is_gemini_api and ai_index != -1:
                    self.notebook.RemovePage(ai_index)

            if hasattr(self, 'livePanel'):
                live_index = -1
                for i in range(self.notebook.GetPageCount()):
                    if self.notebook.GetPage(i) == self.livePanel:
                        live_index = i
                        break
                
                if is_gemini_api and live_index == -1:
                    self.notebook.InsertPage(1, self.livePanel, _("Live Assistant"))
                elif not is_gemini_api and live_index != -1:
                    self.notebook.RemovePage(live_index)
        self.Layout()
        p = self.connectionBox.GetParent()
        if p: p.Layout()
        show_batch_size = False
        if provider == "gemini" or provider == "mistral":
            show_batch_size = True
        elif provider == "custom":
            custom_type_idx = self.customType.GetSelection()
            if custom_type_idx != wx.NOT_FOUND:
                is_custom_gemini = (custom_type_idx == 1)
            else:
                is_custom_gemini = (nvda_config.conf["VisionAssistant"].get("custom_api_type") == "gemini")

            is_upload_supported = self.customUploadSupport.Value
            if is_custom_gemini and is_upload_supported:
                show_batch_size = True

        self.lbl_batch.Show(show_batch_size)
        self.batch_size.Show(show_batch_size)

    def onCustomUploadSupportChange(self, event):
        self.updateCustomFieldsVisibility("custom")

    def onToggleAdvRouting(self, event):
        self.advRoutingBox.Show(self.advRoutingCheck.Value)
        self.connectionBox.Layout()
        p = self.connectionBox.GetParent()
        if p: p.Layout()

    def onProviderChange(self, event):
        p_idx = self.provider_sel.GetSelection()
        p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]

        key_name = "api_key" if p_name == "gemini" else (f"{p_name}_api_key" if p_name != "custom" else "custom_api_key")
        val = get_credential(nvda_config.conf["VisionAssistant"], key_name)

        self.Freeze()
        try:
            self.apiKeyCtrl_hidden.SetValue(val)
            self.apiKeyCtrl_visible.SetValue(val)

            self.refreshModelList(p_name)
            self.updateVoiceList(p_name)
            self.updateCustomFieldsVisibility(p_name)
        finally:
            self.Thaw()
            p = self.connectionBox.GetParent()
            if p:
                p.Layout()

    def onCustomTypeChange(self, event):
        self.updateCustomFieldsVisibility("custom")

    def onSetupLocalAI(self, event):
        # Translators: Button label to automatically configure local AI engines (Ollama, LM Studio, etc.)
        title = _("Setup Local AI")
        # Translators: Prompt message to select local AI engine
        msg = _("Select the local AI engine you are running:")
        choices = [
            "Ollama (http://127.0.0.1:11434)",
            "LM Studio (http://127.0.0.1:1234)",
            "Jan.ai (http://127.0.0.1:1337)",
            "KoboldCPP (http://127.0.0.1:5001)"
        ]

        gui.mainFrame.prePopup()
        try:
            with wx.SingleChoiceDialog(self, msg, title, choices) as dlg:
                if dlg.ShowModal() != wx.ID_OK:
                    return
                idx = dlg.GetSelection()
        finally:
            gui.mainFrame.postPopup()

        ports = ["11434", "1234", "1337", "5001"]
        url = f"http://127.0.0.1:{ports[idx]}"

        # Translators: Progress message shown when testing connection to local AI
        ui.message(_("Connecting to Local AI..."))

        def worker():
            try:
                endpoint = f"{url}/api/tags" if idx == 0 else f"{url}/v1/models"

                from ..utils.media_capture import get_proxy_opener
                from urllib import request
                opener = get_proxy_opener(endpoint)
                req = request.Request(endpoint, method="GET")
                with opener.open(req, timeout=15) as r:
                    res_body = r.read().decode('utf-8')
                    data = json.loads(res_body)

                models_info = []
                if idx == 0:
                    if "models" in data and isinstance(data["models"], list):
                        for m in data["models"]:
                            name = m.get("name")
                            if name:
                                models_info.append((name, name))
                else:
                    if "data" in data and isinstance(data["data"], list):
                        for m in data["data"]:
                            m_id = m.get("id")
                            if m_id:
                                models_info.append((m_id, m_id))

                wx.CallAfter(self._onSetupLocalAISuccess, url, models_info)
            except Exception:
                # Translators: Error message when connection to local AI fails
                err_msg = _("Could not connect to the selected local AI. Make sure it is running on {url}").format(url=url)
                wx.CallAfter(self._onSetupLocalAIFail, err_msg)

        threading.Thread(target=worker, daemon=True).start()

    def _onSetupLocalAISuccess(self, url, models_info):
        self.customUrl.SetValue(url)
        self.customType.SetSelection(0)
        self.customUploadSupport.SetValue(False)

        self._on_fetch_models_complete("custom", models_info)

        # Translators: Announcement message when local AI setup succeeds
        ui.message(_("Local AI configured successfully!"))

    def _onSetupLocalAIFail(self, err_msg):
        wx.MessageBox(err_msg, _("Error"), wx.OK | wx.ICON_ERROR)

    def onFetchModels(self, event):
        p_idx = self.provider_sel.GetSelection()
        p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]

        val = self.apiKeyCtrl_visible.Value if self.showApiCheck.IsChecked() else self.apiKeyCtrl_hidden.Value
        k_key = "api_key" if p_name == "gemini" else (f"{p_name}_api_key" if p_name != "custom" else "custom_api_key")
        # DPAPI failure aborts model fetching; plaintext is never persisted.
        nvda_config.conf["VisionAssistant"][k_key] = protect_credential(val)
        nvda_config.conf["VisionAssistant"]["active_provider"] = p_name

        if p_name == "custom":
            nvda_config.conf["VisionAssistant"]["custom_api_url"] = self.customUrl.Value.strip()
            nvda_config.conf["VisionAssistant"]["custom_api_type"] = "openai" if self.customType.GetSelection() == 0 else "gemini"
            nvda_config.conf["VisionAssistant"]["use_advanced_endpoints"] = self.useAdvancedEndpoints.Value
            nvda_config.conf["VisionAssistant"]["custom_models_url"] = self.customModelsUrl.Value.strip()

        self.btn_fetch.Disable()
        # Translators: Progress message shown while fetching AI models from the server
        ui.message(_("Fetching models..."))
        threading.Thread(target=self._fetch_models_thread, args=(p_name,), daemon=True).start()

    def _fetch_models_thread(self, p_name):
        models_info = AIHandler.get_models(task="all")
        wx.CallAfter(self._on_fetch_models_complete, p_name, models_info)

    def _current_combo_id(self, combo):
        sel = combo.GetSelection()
        if sel != wx.NOT_FOUND:
            return combo.GetClientData(sel)
        return combo.GetValue()

    def _restore_combo(self, combo, saved_id):
        if saved_id is not None:
            for i in range(combo.GetCount()):
                if combo.GetClientData(i) == saved_id:
                    combo.SetSelection(i)
                    combo.ChangeValue(combo.GetString(i))
                    return
            if saved_id:
                combo.SetValue(saved_id)
                return
        if combo.GetCount() > 0:
            combo.SetSelection(0)
            combo.ChangeValue(combo.GetString(0))

    def _on_fetch_models_complete(self, p_name, models_info):
        self.btn_fetch.Enable()
        if models_info:
            prev_main = self._current_combo_id(self.model)
            prev_routing = {}
            for attr in (self.advOcrModel, self.advSttModel, self.advTtsModel, self.advOperatorModel, self.advVideoModel, self.advLiveModel):
                prev_routing[attr] = self._current_combo_id(attr)
            self.model.Freeze()
            self.model.Clear()
            self.advOcrModel.Clear()
            self.advSttModel.Clear()
            self.advTtsModel.Clear()
            self.advOperatorModel.Clear()
            self.advVideoModel.Clear()
            self.advLiveModel.Clear()

            # Translators: Option to follow the main model selected in the primary dropdown
            default_main_label = _("Default (Main Model)")
            # Translators: Option for the system to automatically choose the best model for this specific task
            auto_task_label = _("Auto (Optimized)")

            self.advOcrModel.Append(default_main_label, "")
            self.advSttModel.Append(default_main_label, "")
            self.advOperatorModel.Append(default_main_label, "")
            self.advVideoModel.Append(default_main_label, "")
            self.advLiveModel.Append(auto_task_label, "")
            self.advTtsModel.Append(auto_task_label, "")

            self._current_model_ids = []
            storage_parts = []
            main_models = AIHandler.filter_models(p_name, models_info, task="main")
            for m_id, m_name in main_models:
                self.model.Append(m_name, m_id)
                self._current_model_ids.append(m_id)
            for m_id, m_name in models_info:
                self.advOcrModel.Append(m_name, m_id)
                self.advSttModel.Append(m_name, m_id)
                self.advTtsModel.Append(m_name, m_id)
                self.advOperatorModel.Append(m_name, m_id)
                self.advVideoModel.Append(m_name, m_id)
                self.advLiveModel.Append(m_name, m_id)
                storage_parts.append(f"{m_id}|{m_name}")

            nvda_config.conf["VisionAssistant"][f"{p_name}_models_list"] = ",".join(storage_parts)

            self.model.Thaw()

            self._restore_combo(self.model, prev_main)
            for attr in (self.advOcrModel, self.advSttModel, self.advTtsModel, self.advOperatorModel, self.advVideoModel, self.advLiveModel):
                self._restore_combo(attr, prev_routing.get(attr))

            self._all_models_backup = [(self.model.GetString(i), self.model.GetClientData(i)) for i in range(self.model.GetCount())]

            self.updateVoiceList(p_name)

            self.updateCustomFieldsVisibility(p_name)
            # Translators: Status message when the AI models list is successfully refreshed.
            ui.message(_("Models updated"))
        else:
            # Translators: Error message shown when the add-on cannot retrieve the list of models from the server.
            ui.message(_("Failed to fetch models"))

    def refreshModelList(self, p_name):
        self.model.Clear()
        self.advOcrModel.Clear()
        self.advSttModel.Clear()
        self.advTtsModel.Clear()
        self.advOperatorModel.Clear()
        self.advVideoModel.Clear()
        self.advLiveModel.Clear()

        default_main_label = _("Default (Main Model)")
        auto_task_label = _("Auto (Optimized)")

        self.advOcrModel.Append(default_main_label, "")
        self.advSttModel.Append(default_main_label, "")
        self.advOperatorModel.Append(default_main_label, "")
        self.advVideoModel.Append(default_main_label, "")
        self.advLiveModel.Append(auto_task_label, "")
        self.advTtsModel.Append(auto_task_label, "")

        self._current_model_ids = []
        saved_models_raw = nvda_config.conf["VisionAssistant"].get(f"{p_name}_models_list", "")
        all_models = []
        if saved_models_raw:
            items = saved_models_raw.split(",")
            for item in items:
                if "|" in item:
                    m_id, m_name = item.split("|", 1)
                    all_models.append((m_id, m_name))
        elif p_name == "gemini":
            for m_name, m_id in vision_config.MODELS: all_models.append((m_id, m_name))

        main_models = AIHandler.filter_models(p_name, all_models, task="main")
        for m_id, m_name in main_models:
            self.model.Append(m_name, m_id)
            self._current_model_ids.append(m_id)
        for m_id, m_name in all_models:
            self.advOcrModel.Append(m_name, m_id)
            self.advSttModel.Append(m_name, m_id)
            self.advTtsModel.Append(m_name, m_id)
            self.advOperatorModel.Append(m_name, m_id)
            self.advVideoModel.Append(m_name, m_id)
            self.advLiveModel.Append(m_name, m_id)
            if m_id not in self._current_model_ids: self._current_model_ids.append(m_id)

        m_key = "model_name" if p_name == "gemini" else f"{p_name}_model_name"
        curr_model = self._temp_models.get(p_name, nvda_config.conf["VisionAssistant"].get(m_key, ""))
        if p_name == "custom" and not curr_model:
            curr_model = nvda_config.conf["VisionAssistant"].get("custom_model_name", "")

        for i in range(self.model.GetCount()):
            if self.model.GetClientData(i) == curr_model:
                self.model.SetSelection(i)
                self.model.ChangeValue(self.model.GetString(i))
                break
        else:
            if self.model.GetCount() > 0:
                self.model.SetSelection(0)
                self.model.ChangeValue(self.model.GetString(0))
            else:
                self.model.ChangeValue("")

        routing_map = [
            (self.advOcrModel, f"{p_name}_ocr_model"),
            (self.advSttModel, f"{p_name}_stt_model"),
            (self.advTtsModel, f"{p_name}_tts_model"),
            (self.advOperatorModel, f"{p_name}_operator_model"),
        ]
        if self._live_supported_for(p_name):
            routing_map.append((self.advVideoModel, f"{p_name}_video_model"))
            routing_map.append((self.advLiveModel, f"{p_name}_live_model"))
        for attr, conf_key in routing_map:
            saved_id = nvda_config.conf["VisionAssistant"].get(conf_key, "")
            for i in range(attr.GetCount()):
                if attr.GetClientData(i) == saved_id:
                    attr.SetSelection(i)
                    break
            else: attr.SetSelection(0)
        self._all_models_backup = [(self.model.GetString(i), self.model.GetClientData(i)) for i in range(self.model.GetCount())]
        self.updateCustomFieldsVisibility(p_name)


    def onToggleAdvanced(self, event):
        p_idx = self.provider_sel.GetSelection()
        if p_idx != wx.NOT_FOUND:
            p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
            self.updateCustomFieldsVisibility(p_name)

    def onToggleApiVisibility(self, event):
        if self.showApiCheck.IsChecked():
            self.apiKeyCtrl_visible.SetValue(self.apiKeyCtrl_hidden.GetValue())
            self.apiKeyCtrl_hidden.Hide()
            self.apiKeyCtrl_visible.Show()
        else:
            self.apiKeyCtrl_hidden.SetValue(self.apiKeyCtrl_visible.GetValue())
            self.apiKeyCtrl_visible.Hide()
            self.apiKeyCtrl_hidden.Show()
        self.connectionBox.GetParent().Layout()

    def onModelPickerChange(self, event):
        cb = event.GetEventObject()
        sel = cb.GetSelection()
        if sel != wx.NOT_FOUND:
            model_id = cb.GetClientData(sel)
            if model_id:
                p_idx = self.provider_sel.GetSelection()
                p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
                self._temp_models[p_name] = model_id
                if p_name == "custom":
                    self.customModelName.SetValue(model_id)

    def onVoiceSelectionChanged(self, event):
        sel = self.voice_sel.GetSelection()
        if sel != wx.NOT_FOUND:
            voice_id = self.voice_sel.GetClientData(sel)
            p_idx = self.provider_sel.GetSelection()
            if p_idx != wx.NOT_FOUND:
                p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
                if p_name == "custom":
                    self.customTtsVoice.SetValue(voice_id)

    def onCustomUrlChange(self, event):
        self.model.Clear()
        self._all_models_backup = []
        p_idx = self.provider_sel.GetSelection()
        if p_idx != wx.NOT_FOUND:
            p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
            if p_name == "custom":
                nvda_config.conf["VisionAssistant"]["custom_models_list"] = ""
                self.updateCustomFieldsVisibility("custom")
        event.Skip()

    def _on_ptt_key_focus(self, event):
        try:
            if inputCore.manager._captureFunc is not None:
                event.Skip()
                return
        except Exception:
            pass
        self._ptt_capture_func = self._ptt_captor
        self._ptt_last_combo = None
        self._ptt_last_time = 0.0
        try:
            inputCore.manager._captureFunc = self._ptt_capture_func
        except Exception:
            pass
        event.Skip()

    def _on_ptt_key_kill_focus(self, event):
        self._stop_ptt_capture()
        event.Skip()

    def _stop_ptt_capture(self):
        try:
            if inputCore.manager._captureFunc is getattr(self, "_ptt_capture_func", None):
                inputCore.manager._captureFunc = None
        except Exception:
            pass
        self._ptt_capture_func = None
        self._ptt_gen = getattr(self, "_ptt_gen", 0) + 1
        self._ptt_pending_modifier = None

    def _ptt_captor(self, gesture):
        if not isinstance(gesture, keyboardHandler.KeyboardInputGesture):
            return True
        try:
            identifier = gesture.identifiers[-1]
        except Exception:
            return True
        if ":" not in identifier:
            return True
        combo = identifier.rsplit(":", 1)[1].strip().lower()
        parts = combo.split("+")
        if gesture.isModifier:
            spec = normalize_ptt_key(combo)
            if spec:
                self._ptt_pending_modifier = spec
                gen = getattr(self, "_ptt_gen", 0) + 1
                self._ptt_gen = gen
                core.callLater(600, self._ptt_finalize_modifier, gen)
            return False
        self._ptt_gen = getattr(self, "_ptt_gen", 0) + 1
        self._ptt_pending_modifier = None
        if parts and parts[-1] in ("tab", "insert"):
            return True
        if combo in ("escape", "enter"):
            return None
        now = time.monotonic()
        if combo == self._ptt_last_combo and now - self._ptt_last_time < 0.5:
            return False
        self._ptt_last_combo = combo
        self._ptt_last_time = now
        if combo in ("backspace", "delete"):
            wx.CallAfter(self._set_ptt_key_value, "")
            return False
        if not normalize_ptt_key(combo):
            return False
        wx.CallAfter(self._set_ptt_key_value, combo)
        return False

    def _ptt_finalize_modifier(self, gen):
        if gen != getattr(self, "_ptt_gen", 0):
            return
        spec = self._ptt_pending_modifier
        self._ptt_pending_modifier = None
        self._stop_ptt_capture()
        if spec:
            self._set_ptt_key_value(spec)

    def _set_ptt_key_value(self, combo):
        try:
            display = ptt_key_display(combo)
            if self.pttKeyCtrl.GetValue() == display:
                return
            self.pttKeyCtrl.SetValue(display)
            if display:
                ui.message(display)
        except Exception:
            pass

    def onTogglePtt(self, event):
        show = self.pttCheck.Value
        self.lblPttKey.Show(show)
        self.pttKeyCtrl.Show(show)
        self.livePanel.Layout()

    def onToggleBackupKeyProtection(self, event):
        if self.protectBackupKeysCheck.IsChecked():
            return
        # Translators: Warning shown when the user chooses to export transferable plaintext API keys in backup files.
        gui.messageBox(
            _("API keys in newly created backup JSON files will be stored as readable plaintext. Anyone who can access a backup file can use those keys. NVDA's configuration and log files will remain protected."),
            _("Unprotected Backup API Keys"),
            wx.OK | wx.ICON_WARNING,
            parent=self,
        )

    def isValid(self):
        if not self.pttCheck.Value or normalize_ptt_key(self.pttKeyCtrl.Value):
            return True
        p_idx = self.provider_sel.GetSelection()
        p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx] if p_idx != wx.NOT_FOUND else "gemini"
        if not self._live_supported_for(p_name):
            return True
        # Translators: Warning shown when Push to Talk is enabled but no key has been assigned in settings.
        gui.messageBox(
            _("You have not assigned a Push to Talk key. Please press a key in the Push to Talk Key field, or disable Push to Talk."),
            # Translators: Title of the warning dialog about the missing push-to-talk key.
            _("Push to Talk Key"),
            wx.OK | wx.ICON_WARNING,
            parent=self,
        )
        return False

    def onDiscard(self):
        self._stop_ptt_capture()

    def onSave(self):
        self._stop_ptt_capture()
        try:
            p_idx = self.provider_sel.GetSelection()
            p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
            nvda_config.conf["VisionAssistant"]["active_provider"] = p_name

            val = self.apiKeyCtrl_visible.Value if self.showApiCheck.IsChecked() else self.apiKeyCtrl_hidden.Value
            k_key = "api_key" if p_name == "gemini" else (f"{p_name}_api_key" if p_name != "custom" else "custom_api_key")
            # DPAPI failure aborts the save; plaintext is never used as a fallback.
            nvda_config.conf["VisionAssistant"][k_key] = protect_credential(val)

            m_key = "model_name" if p_name == "gemini" else f"{p_name}_model_name"
            has_fetched_models = self.model.GetCount() > 0
            if p_name == "custom":
                model_val = ""
                if has_fetched_models and self.model.GetSelection() != wx.NOT_FOUND:
                    model_val = self.model.GetClientData(self.model.GetSelection())
                if not model_val:
                    model_val = self.customModelName.Value.strip()
                if model_val:
                    nvda_config.conf["VisionAssistant"]["custom_model_name"] = model_val
                    nvda_config.conf["VisionAssistant"][m_key] = model_val
            else:
                sel_idx = self.model.GetSelection()
                if sel_idx != wx.NOT_FOUND:
                    model_val = self.model.GetClientData(sel_idx)
                    nvda_config.conf["VisionAssistant"][m_key] = model_val

            nvda_config.conf["VisionAssistant"]["advanced_model_routing"] = self.advRoutingCheck.Value
            routing_save = [
                (self.advOcrModel, f"{p_name}_ocr_model"),
                (self.advSttModel, f"{p_name}_stt_model"),
                (self.advTtsModel, f"{p_name}_tts_model"),
                (self.advOperatorModel, f"{p_name}_operator_model"),
            ]
            if self._live_supported_for(p_name):
                routing_save.append((self.advVideoModel, f"{p_name}_video_model"))
                routing_save.append((self.advLiveModel, f"{p_name}_live_model"))
            for attr, conf_key in routing_save:
                idx = attr.GetSelection()
                if idx != wx.NOT_FOUND:
                    nvda_config.conf["VisionAssistant"][conf_key] = attr.GetClientData(idx)

            if p_name == "custom":
                nvda_config.conf["VisionAssistant"]["custom_api_url"] = self.customUrl.Value.strip()
                nvda_config.conf["VisionAssistant"]["custom_api_type"] = "openai" if self.customType.GetSelection() == 0 else "gemini"
                nvda_config.conf["VisionAssistant"]["custom_upload_support"] = self.customUploadSupport.Value
                nvda_config.conf["VisionAssistant"]["use_advanced_endpoints"] = self.useAdvancedEndpoints.Value
                nvda_config.conf["VisionAssistant"]["custom_models_url"] = self.customModelsUrl.Value.strip()
                nvda_config.conf["VisionAssistant"]["custom_ocr_url"] = self.customOcrUrl.Value.strip()
                nvda_config.conf["VisionAssistant"]["custom_stt_url"] = self.customSttUrl.Value.strip()
                nvda_config.conf["VisionAssistant"]["custom_tts_url"] = self.customTtsUrl.Value.strip()
                nvda_config.conf["VisionAssistant"]["custom_operator_url"] = self.customAssistantUrl.Value.strip()
                if not has_fetched_models:
                    nvda_config.conf["VisionAssistant"]["custom_ocr_model"] = self.customOcrModel.Value.strip()
                    nvda_config.conf["VisionAssistant"]["custom_stt_model"] = self.customSttModel.Value.strip()
                    nvda_config.conf["VisionAssistant"]["custom_tts_model"] = self.customTtsModel.Value.strip()
                    nvda_config.conf["VisionAssistant"]["custom_operator_model"] = self.customAssistantModel.Value.strip()

                nvda_config.conf["VisionAssistant"]["custom_tts_voice"] = self.customTtsVoice.Value.strip()

            final_voice = ""
            if p_name == "custom" and self.customTtsVoice.Value.strip():
                final_voice = self.customTtsVoice.Value.strip()
            else:
                v_idx = self.voice_sel.GetSelection()
                if v_idx != wx.NOT_FOUND:
                    final_voice = self.voice_sel.GetClientData(v_idx)

            if final_voice:
                nvda_config.conf["VisionAssistant"]["tts_voice"] = final_voice

            nvda_config.conf["VisionAssistant"]["ai_temperature"] = float(self.aiTemp.GetStringSelection())
            nvda_config.conf["VisionAssistant"]["proxy_url"] = self.proxyUrl.Value.strip()
            nvda_config.conf["VisionAssistant"]["source_language"] = vision_config.SOURCE_LIST[self.sourceLang.GetSelection()][1]
            nvda_config.conf["VisionAssistant"]["target_language"] = vision_config.TARGET_LIST[self.targetLang.GetSelection()][1]
            nvda_config.conf["VisionAssistant"]["ai_response_language"] = vision_config.TARGET_LIST[self.aiResponseLang.GetSelection()][1]
            nvda_config.conf["VisionAssistant"]["smart_swap"] = self.smartSwap.Value
            nvda_config.conf["VisionAssistant"]["check_update_startup"] = self.checkUpdateStartup.Value
            nvda_config.conf["VisionAssistant"]["clean_markdown_chat"] = self.cleanMarkdown.Value
            nvda_config.conf["VisionAssistant"]["copy_to_clipboard"] = self.copyToClipboard.Value
            nvda_config.conf["VisionAssistant"]["skip_chat_dialog"] = self.skipChatDialog.Value
            nvda_config.conf["VisionAssistant"]["live_direct_output"] = self.liveDirectOutput.Value
            nvda_config.conf["VisionAssistant"]["live_push_to_talk"] = self.pttCheck.Value
            nvda_config.conf["VisionAssistant"]["live_ptt_key"] = normalize_ptt_key(self.pttKeyCtrl.Value)
            nvda_config.conf["VisionAssistant"]["captcha_mode"] = 'navigator' if self.captchaMode.GetSelection() == 0 else 'fullscreen'
            nvda_config.conf["VisionAssistant"]["enable_visual_captcha_solver"] = self.enableVisualCaptcha.Value
            nvda_config.conf["VisionAssistant"]["ocr_engine"] = vision_config.OCR_ENGINES[self.ocr_sel.GetSelection()][1]
            nvda_config.conf["VisionAssistant"]["ocr_batch_size"] = self.batch_size.GetValue()
            nvda_config.conf["VisionAssistant"]["describe_images_ocr"] = self.chk_describe_images.Value
            nvda_config.conf["VisionAssistant"]["document_export_page_numbers"] = self.chk_export_page_numbers.Value
            nvda_config.conf["VisionAssistant"]["video_srt_chunk_minutes"] = self.vid_chunk_size.GetValue()
            nvda_config.conf["VisionAssistant"]["video_chars_as_subtitle"] = self.vid_chars_as_sub.Value
            nvda_config.conf["VisionAssistant"]["video_add_disclaimer"] = self.vid_add_disclaimer.Value
            nvda_config.conf["VisionAssistant"]["enable_file_logging"] = self.enableFileLogging.Value
            nvda_config.conf["VisionAssistant"]["protect_api_keys_in_backups"] = self.protectBackupKeysCheck.Value
            l_idx = self.logLevelSel.GetSelection()
            if l_idx != wx.NOT_FOUND:
                nvda_config.conf["VisionAssistant"]["log_level"] = self.logLevels[l_idx][1]
            r_idx = self.logRetentionSel.GetSelection()
            if r_idx != wx.NOT_FOUND:
                nvda_config.conf["VisionAssistant"]["log_retention_hours"] = self.logRetentionChoices[r_idx][1]
            nvda_config.conf["VisionAssistant"]["custom_prompts_v2"] = serialize_custom_prompts_v2(self.customPromptItems)
            nvda_config.conf["VisionAssistant"]["default_refine_prompts"] = serialize_default_prompt_overrides(self.defaultPromptItems)

            try:
                inst = plugin_state.plugin_instance
                if inst is not None:
                    inst._refresh_custom_prompt_scripts()
            except Exception as e:
                log.warning(f"Failed to refresh custom prompt shortcuts: {e}")

            try:
                from ..utils.logging_utils import setup_file_logging
                setup_file_logging()
            except Exception as le:
                log.warning(f"Failed to re-apply logging settings: {le}")
        except Exception as e:
            # Translators: Message box content for successful save
            wx.CallAfter(gui.messageBox, _("Save Error: {error}").format(error=e), _("Error"), wx.OK | wx.ICON_ERROR)

    def onOpenLogFile(self, event):
        try:
            from ..utils.logging_utils import open_log_file
            open_log_file()
        except Exception as e:
            log.error(f"onOpenLogFile failed: {e}", exc_info=True)

    def onOpenLogFolder(self, event):
        try:
            from ..utils.logging_utils import open_log_folder
            open_log_folder()
        except Exception as e:
            log.error(f"onOpenLogFolder failed: {e}", exc_info=True)

    def onClearLogFile(self, event):
        try:
            from ..utils.logging_utils import clear_log_file
            clear_log_file()
            # Translators: Message reported when log file is cleared.
            ui.message(_("Log file cleared."))
        except Exception as e:
            log.error(f"onClearLogFile failed: {e}", exc_info=True)

    def onBackupSettings(self, event):
        from datetime import datetime
        default_name = f"VisionAssistant_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        gui.mainFrame.prePopup()
        try:
            with wx.FileDialog(
                self,
                # Translators: Title of the save file dialog for the add-on backup
                _("Save Backup"),
                defaultFile=default_name,
                wildcard="JSON files (*.json)|*.json",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            ) as dlg:
                if dlg.ShowModal() != wx.ID_OK:
                    return
                path = dlg.GetPath()
        finally:
            gui.mainFrame.postPopup()
        gui.mainFrame.prePopup()
        try:
            # Translators: Options for what to include in the settings backup.
            choices = [_("Everything (Settings, Labels, OCR Progress, History)"), _("Settings Only")]
            scope_dlg = wx.SingleChoiceDialog(
                self,
                # Translators: Message of the backup scope dialog asking what to include.
                _("What would you like to back up?"),
                # Translators: Title of the backup scope dialog.
                _("Backup Options"),
                choices,
            )
            scope_dlg.Raise()
            if scope_dlg.ShowModal() != wx.ID_OK:
                scope_dlg.Destroy()
                return
            include_data = scope_dlg.GetSelection() == 0
            scope_dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()
        protect_backup_keys = self.protectBackupKeysCheck.IsChecked()
        if not protect_backup_keys:
            gui.mainFrame.prePopup()
            try:
                # Translators: Confirmation before saving a portable backup containing plaintext API keys.
                if gui.messageBox(
                    _("This backup will contain your API keys as readable plaintext so they can be transferred to another Windows account or computer. Anyone with access to the file can use the keys. Do you want to continue?"),
                    _("Create Backup With Plaintext API Keys?"),
                    wx.YES_NO | wx.ICON_WARNING,
                    parent=self,
                ) != wx.YES:
                    return
            finally:
                gui.mainFrame.postPopup()
        try:
            settings_data = nvda_config.conf["VisionAssistant"].dict()
            # This transforms only the copied backup data. Live NVDA configuration
            # always retains DPAPI-protected credentials.
            prepare_backup_credentials(settings_data, protect=protect_backup_keys)
            settings_data["custom_prompts_v2"] = serialize_custom_prompts_v2(self.customPromptItems)
            settings_data["default_refine_prompts"] = serialize_default_prompt_overrides(self.defaultPromptItems)
            payload = {
                "format": "VisionAssistantSettingsBackup",
                "version": 2,
                "settings": settings_data,
            }
            if include_data:
                data = {}
                for key, fpath in (("labels", vision_config.LABELS_FILE), ("ocr_progress", vision_config.OCR_PROGRESS_FILE), ("history", vision_config.HISTORY_FILE)):
                    if os.path.exists(fpath):
                        try:
                            with open(fpath, "r", encoding="utf-8") as f:
                                data[key] = json.load(f)
                        except Exception as e:
                            log.warning(f"Backup: failed to read {key}: {e}")
                payload["data"] = data
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
            # Translators: Message announced after a successful backup.
            ui.message(_("Backup saved."))
        except Exception as e:
            log.error(f"onBackupSettings failed: {e}", exc_info=True)
            gui.mainFrame.prePopup()
            try:
                # Translators: Error message when the settings backup fails.
                gui.messageBox(_("Backup failed: {error}").format(error=e), _("Error"), wx.OK | wx.ICON_ERROR)
            finally:
                gui.mainFrame.postPopup()

    def onRestoreSettings(self, event):
        gui.mainFrame.prePopup()
        try:
            with wx.FileDialog(
                self,
                # Translators: Title of the open file dialog for restoring a backup.
                _("Choose a Backup File"),
                wildcard="JSON files (*.json)|*.json",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
            ) as dlg:
                if dlg.ShowModal() != wx.ID_OK:
                    return
                path = dlg.GetPath()
            try:
                with open(path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
            except Exception as e:
                # Translators: Error message when the chosen backup file cannot be read.
                gui.messageBox(_("Could not read the backup file: {error}").format(error=e), _("Error"), wx.OK | wx.ICON_ERROR)
                return
            if not isinstance(payload, dict) or payload.get("format") != "VisionAssistantSettingsBackup" or not isinstance(payload.get("settings"), dict):
                # Translators: Error message when the chosen file is not a valid settings backup.
                gui.messageBox(_("This file is not a valid Vision Assistant settings backup."), _("Error"), wx.OK | wx.ICON_ERROR)
                return
            has_data = isinstance(payload.get("data"), dict)
            if has_data:
                # Translators: Confirmation prompt shown before restoring a full backup, because it replaces all current settings and data.
                confirm_msg = _("Restoring will replace all current settings and data (labels, OCR progress, and history). Do you want to continue?")
            else:
                # Translators: Confirmation prompt shown before restoring, because it replaces all current settings.
                confirm_msg = _("Restoring will replace all current settings. Do you want to continue?")
            if gui.messageBox(
                confirm_msg,
                # Translators: Title of the confirmation dialog for restoring settings.
                _("Restore Settings"),
                wx.YES_NO | wx.ICON_WARNING,
            ) != wx.YES:
                return
        finally:
            gui.mainFrame.postPopup()
        try:
            restored_settings = payload["settings"]
            # Protect legacy plaintext credentials and clear DPAPI values that
            # belong to another Windows user or computer before installing the
            # restored configuration.
            unavailable_credentials = prepare_restored_credentials(restored_settings)
            nvda_config.conf["VisionAssistant"] = restored_settings
        except Exception as e:
            log.error(f"onRestoreSettings failed to apply: {e}", exc_info=True)
            gui.mainFrame.prePopup()
            try:
                # Translators: Error message when applying the restored settings fails.
                gui.messageBox(_("Restore failed: {error}").format(error=e), _("Error"), wx.OK | wx.ICON_ERROR)
            finally:
                gui.mainFrame.postPopup()
            return
        self.defaultPromptItems = get_configured_default_prompts()
        self.customPromptItems = load_configured_custom_prompts()
        self._refreshPromptSummary()
        self._reloadControlsFromConfig()
        try:
            inst = plugin_state.plugin_instance
            if inst is not None:
                inst._refresh_custom_prompt_scripts()
        except Exception as e:
            log.warning(f"Failed to refresh custom prompt shortcuts after restore: {e}")
        if has_data:
            for key, fpath in (("labels", vision_config.LABELS_FILE), ("ocr_progress", vision_config.OCR_PROGRESS_FILE), ("history", vision_config.HISTORY_FILE)):
                if key in payload["data"]:
                    try:
                        with open(fpath, "w", encoding="utf-8") as f:
                            json.dump(payload["data"][key], f, ensure_ascii=False)
                    except Exception as e:
                        log.warning(f"Restore: failed to write {key}: {e}")
            try:
                inst = plugin_state.plugin_instance
                if inst is not None and "labels" in payload["data"]:
                    inst.labels_cache = payload["data"].get("labels", {})
            except Exception as e:
                log.warning(f"Restore: failed to reload labels: {e}")
        if unavailable_credentials:
            provider_names = {
                "api_key": "Gemini",
                "openai_api_key": "OpenAI",
                "mistral_api_key": "Mistral",
                "groq_api_key": "Groq",
                "minimax_api_key": "MiniMax",
                "custom_api_key": _("Custom provider"),
            }
            unavailable_providers = ", ".join(
                provider_names[field] for field in unavailable_credentials
            )
            gui.mainFrame.prePopup()
            try:
                # Translators: Warning after restoring a backup whose encrypted API keys were created by another Windows user or computer. {providers} is a comma-separated list of provider names.
                message = _(
                    "The backup was restored, but these API keys could not be recovered because they were protected by a different Windows account or computer: {providers}. The unavailable keys have been cleared. Enter them again in Vision Assistant Settings."
                ).format(providers=unavailable_providers)
                gui.messageBox(message, _("API Keys Required"), wx.OK | wx.ICON_WARNING)
            finally:
                gui.mainFrame.postPopup()
        else:
            # Translators: Message announced after a successful restore.
            ui.message(_("Backup restored successfully."))

    def _reloadControlsFromConfig(self):
        conf = nvda_config.conf["VisionAssistant"]
        providers = ["gemini", "openai", "mistral", "groq", "minimax", "custom"]
        curr_p = conf.get("active_provider", "gemini")
        try:
            p_idx = next(i for i, x in enumerate(providers) if x == curr_p)
        except Exception:
            p_idx = 0
        self.provider_sel.SetSelection(p_idx)

        k_key = "api_key" if curr_p == "gemini" else (f"{curr_p}_api_key" if curr_p != "custom" else "custom_api_key")
        key_val = get_credential(conf, k_key)
        self.apiKeyCtrl_hidden.SetValue(key_val)
        self.apiKeyCtrl_visible.SetValue(key_val)
        self.showApiCheck.SetValue(False)
        self.apiKeyCtrl_hidden.Show()
        self.apiKeyCtrl_visible.Hide()

        self.customUrl.SetValue(conf.get("custom_api_url", ""))
        self.customType.SetSelection(0 if conf.get("custom_api_type", "openai") == "openai" else 1)
        self.customModelName.SetValue(conf.get("custom_model_name", ""))
        self.customUploadSupport.SetValue(conf.get("custom_upload_support", False))
        self.useAdvancedEndpoints.SetValue(conf.get("use_advanced_endpoints", False))
        self.customModelsUrl.SetValue(conf.get("custom_models_url", ""))
        self.customOcrUrl.SetValue(conf.get("custom_ocr_url", ""))
        self.customOcrModel.SetValue(conf.get("custom_ocr_model", ""))
        self.customSttUrl.SetValue(conf.get("custom_stt_url", ""))
        self.customSttModel.SetValue(conf.get("custom_stt_model", ""))
        self.customTtsUrl.SetValue(conf.get("custom_tts_url", ""))
        self.customTtsModel.SetValue(conf.get("custom_tts_model", ""))
        self.customAssistantUrl.SetValue(conf.get("custom_operator_url", ""))
        self.customAssistantModel.SetValue(conf.get("custom_operator_model", ""))
        self.customTtsVoice.SetValue(conf.get("custom_tts_voice", ""))

        self.advRoutingCheck.SetValue(conf.get("advanced_model_routing", False))
        self.proxyUrl.SetValue(conf.get("proxy_url", ""))
        self.checkUpdateStartup.SetValue(conf.get("check_update_startup", False))
        self.cleanMarkdown.SetValue(conf.get("clean_markdown_chat", True))
        self.copyToClipboard.SetValue(conf.get("copy_to_clipboard", False))
        self.skipChatDialog.SetValue(conf.get("skip_chat_dialog", False))
        self.liveDirectOutput.SetValue(conf.get("live_direct_output", False))
        self.pttCheck.SetValue(conf.get("live_push_to_talk", False))
        self.pttKeyCtrl.SetValue(ptt_key_display(conf.get("live_ptt_key", "")))

        temp_str = str(conf.get("ai_temperature", 0.7))
        t_idx = self.aiTemp.FindString(temp_str)
        self.aiTemp.SetSelection(t_idx if t_idx != wx.NOT_FOUND else 7)

        s_code = conf.get("source_language", "auto")
        s_idx = next((i for i, x in enumerate(vision_config.SOURCE_LIST) if x[1] == s_code), 0)
        self.sourceLang.SetSelection(s_idx)
        t_code = conf.get("target_language", "en")
        t_idx = next((i for i, x in enumerate(vision_config.TARGET_LIST) if x[1] == t_code), 0)
        self.targetLang.SetSelection(t_idx)
        ai_code = conf.get("ai_response_language", "en")
        ai_idx = next((i for i, x in enumerate(vision_config.TARGET_LIST) if x[1] == ai_code), 0)
        self.aiResponseLang.SetSelection(ai_idx)
        self.smartSwap.SetValue(conf.get("smart_swap", True))

        ocr_code = conf.get("ocr_engine", "chrome")
        ocr_idx = next((i for i, v in enumerate(vision_config.OCR_ENGINES) if v[1] == ocr_code), 0)
        self.ocr_sel.SetSelection(ocr_idx)
        self.batch_size.SetValue(conf.get("ocr_batch_size", 20))
        self.chk_describe_images.SetValue(conf.get("describe_images_ocr", True))
        self.chk_export_page_numbers.SetValue(conf.get("document_export_page_numbers", True))

        self.vid_chunk_size.SetValue(conf.get("video_srt_chunk_minutes", 10))
        self.vid_chars_as_sub.SetValue(conf.get("video_chars_as_subtitle", True))
        self.vid_add_disclaimer.SetValue(conf.get("video_add_disclaimer", True))

        self.enableVisualCaptcha.SetValue(conf.get("enable_visual_captcha_solver", True))
        self.captchaMode.SetSelection(0 if conf.get("captcha_mode", "navigator") == "navigator" else 1)

        self.enableFileLogging.SetValue(conf.get("enable_file_logging", False))
        self.protectBackupKeysCheck.SetValue(conf.get("protect_api_keys_in_backups", True))
        lvl = conf.get("log_level", "DEBUG")
        lvl_idx = next((i for i, x in enumerate(self.logLevels) if x[1] == lvl), 0)
        self.logLevelSel.SetSelection(lvl_idx)
        ret_hrs = conf.get("log_retention_hours", 168)
        ret_idx = next((i for i, x in enumerate(self.logRetentionChoices) if x[1] == ret_hrs), 6)
        self.logRetentionSel.SetSelection(ret_idx)

        self._temp_models = {}
        self.refreshModelList(curr_p)
        self.updateVoiceList(curr_p)
        self.updateCustomFieldsVisibility(curr_p)

    def onModelFilter(self, event):
        cb = event.GetEventObject()
        if cb.IsFrozen(): return

        sel = cb.GetSelection()
        if sel != wx.NOT_FOUND:
            model_id = cb.GetClientData(sel)
            if cb == getattr(self, 'model', None):
                p_idx = getattr(self, 'provider_sel', None).GetSelection() if getattr(self, 'provider_sel', None) else -1
                if p_idx == 4 and model_id:
                    self.customModelName.SetValue(model_id)
            return

        query = cb.GetValue()
        query_low = query.lower()

        if not hasattr(cb, '_all_models_backup') and cb.GetCount() > 0:
            cb._all_models_backup = [(cb.GetString(i), cb.GetClientData(i)) for i in range(cb.GetCount())]

        backup = getattr(cb, '_all_models_backup', [])

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

        if filtered:
            # Translators: Notification showing the number of items found after filtering the model list.
            ui.message(_("{count} items found").format(count=len(filtered)))
