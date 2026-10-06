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
from ..utils.system import apply_model_filter, is_gemini_provider
from ..ai.core import AIHandler, PROVIDERS, provider_key_name, provider_model_name
from ..prompt_utils import (
	normalize_ptt_key,
	ptt_key_display,
	get_configured_default_prompts,
	load_configured_custom_prompts,
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
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onNotebookPageChanged)

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
			(_("Custom"), "custom"),
		]
		self.provider_sel = cHelper.addLabeledControl(
			# Translators: Label for AI Provider selection
			_("Provider:"),
			wx.Choice,
			choices=[x[0] for x in providers],
		)
		curr_p = nvda_config.conf["VisionAssistant"]["active_provider"]
		try:
			self.provider_sel.SetSelection(next(i for i, x in enumerate(providers) if x[1] == curr_p))
		except Exception:
			self.provider_sel.SetSelection(0)
		self.provider_sel.Bind(wx.EVT_CHOICE, self.onProviderChange)

		apiLabel = wx.StaticText(
			self.connectionBox,
			# Translators: Label for API Key input
			label=_("API Key (Separate multiple keys with comma or newline):"),
		)
		cHelper.addItem(apiLabel)

		curr_key = nvda_config.conf["VisionAssistant"][provider_key_name(curr_p)]
		self.apiKeyCtrl_hidden = wx.TextCtrl(self.connectionBox, value=curr_key, style=wx.TE_PASSWORD)
		self.apiKeyCtrl_visible = wx.TextCtrl(
			self.connectionBox,
			value=curr_key,
			style=wx.TE_MULTILINE | wx.TE_DONTWRAP,
			size=(-1, 60),
		)
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
		self.customUrl = wx.TextCtrl(
			self.customBox,
			value=nvda_config.conf["VisionAssistant"]["custom_api_url"],
		)
		self.customSizer.Add(self.customUrl, 0, wx.EXPAND | wx.ALL, 2)
		self.customUrl.Bind(wx.EVT_TEXT, self.onCustomUrlChange)
		# Translators: Label for Custom API Type selection
		self.customSizer.Add(wx.StaticText(self.customBox, label=_("API Type:")), 0, wx.ALL, 2)
		# Translators: Compatibility option for OpenAI API format
		OPT_OPENAI = _("OpenAI Compatible")
		# Translators: Compatibility option for Gemini API format
		OPT_GEMINI = _("Gemini Compatible")
		self.customType = wx.Choice(self.customBox, choices=[OPT_OPENAI, OPT_GEMINI])
		self.customType.Bind(wx.EVT_CHOICE, self.onCustomTypeChange)
		self.customType.SetSelection(
			0 if nvda_config.conf["VisionAssistant"]["custom_api_type"] == "openai" else 1,
		)
		self.customSizer.Add(self.customType, 0, wx.EXPAND | wx.ALL, 2)

		# Translators: Label for Custom Model Name input
		self.lbl_customModelName = wx.StaticText(self.customBox, label=_("Model Name (Manual):"))
		self.customSizer.Add(self.lbl_customModelName, 0, wx.ALL, 2)
		self.customModelName = wx.TextCtrl(
			self.customBox,
			value=nvda_config.conf["VisionAssistant"]["custom_model_name"],
		)
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
		self.customModelsUrl = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_models_url"],
		)
		advVBox.Add(self.customModelsUrl, 0, wx.EXPAND | wx.ALL, 2)

		# Translators: Label for Custom OCR URL
		advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("OCR Endpoint URL:")), 0, wx.ALL, 2)
		self.customOcrUrl = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_ocr_url"],
		)
		advVBox.Add(self.customOcrUrl, 0, wx.EXPAND | wx.ALL, 2)

		# Translators: Label for Custom OCR Model
		self.lblCustomOcrModel = wx.StaticText(self.advEndpointBox, label=_("Custom OCR Model (Optional):"))
		advVBox.Add(self.lblCustomOcrModel, 0, wx.ALL, 2)
		self.customOcrModel = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_ocr_model"],
		)
		advVBox.Add(self.customOcrModel, 0, wx.EXPAND | wx.ALL, 2)

		# Translators: Label for Custom STT URL
		advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Speech-to-Text (STT) URL:")), 0, wx.ALL, 2)
		self.customSttUrl = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_stt_url"],
		)
		advVBox.Add(self.customSttUrl, 0, wx.EXPAND | wx.ALL, 2)

		# Translators: Label for Custom STT Model
		self.lblCustomSttModel = wx.StaticText(self.advEndpointBox, label=_("Custom STT Model (Optional):"))
		advVBox.Add(self.lblCustomSttModel, 0, wx.ALL, 2)
		self.customSttModel = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_stt_model"],
		)
		advVBox.Add(self.customSttModel, 0, wx.EXPAND | wx.ALL, 2)

		# Translators: Label for Custom TTS URL
		advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Text-to-Speech (TTS) URL:")), 0, wx.ALL, 2)
		self.customTtsUrl = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_tts_url"],
		)
		advVBox.Add(self.customTtsUrl, 0, wx.EXPAND | wx.ALL, 2)

		# Translators: Label for Custom TTS Model
		self.lblCustomTtsModel = wx.StaticText(self.advEndpointBox, label=_("Custom TTS Model (Optional):"))
		advVBox.Add(self.lblCustomTtsModel, 0, wx.ALL, 2)
		self.customTtsModel = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_tts_model"],
		)
		advVBox.Add(self.customTtsModel, 0, wx.EXPAND | wx.ALL, 2)

		# Translators: Label for a text field in the "Custom Provider Settings" section of settings where the user enters the AI Operator URL.
		advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("AI Operator URL:")), 0, wx.ALL, 2)
		self.customAssistantUrl = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"].get("custom_operator_url", ""),
		)
		advVBox.Add(self.customAssistantUrl, 0, wx.EXPAND | wx.ALL, 2)

		self.lblCustomOperatorModel = wx.StaticText(
			self.advEndpointBox,
			# Translators: Label for a text field in the "Custom Provider Settings" section of settings where the user manually enters the model name for AI Operator.
			label=_("Custom Operator Model (Optional):"),
		)
		advVBox.Add(self.lblCustomOperatorModel, 0, wx.ALL, 2)
		self.customAssistantModel = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_operator_model"],
		)
		advVBox.Add(self.customAssistantModel, 0, wx.EXPAND | wx.ALL, 2)

		advVBox.Add(
			# Translators: Label for Custom TTS Voice Name
			wx.StaticText(self.advEndpointBox, label=_("Custom TTS Voice Name (Optional):")),
			0,
			wx.ALL,
			2,
		)
		self.customTtsVoice = wx.TextCtrl(
			self.advEndpointBox,
			value=nvda_config.conf["VisionAssistant"]["custom_tts_voice"],
		)
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

		# Translators: Button to open the Gemini API keys manager that creates keys with the user's Google account
		self.btn_gemini_keys = wx.Button(self.connectionBox, label=_("Get a Gemini API Key..."))
		self.btn_gemini_keys.Bind(wx.EVT_BUTTON, self.onGetGeminiKey)
		cHelper.addItem(self.btn_gemini_keys)

		self.modelLabel = wx.StaticText(self.connectionBox, label=_("AI Model:"))
		cHelper.addItem(self.modelLabel)
		# Translators: Label for AI Model selection choice box
		self.model = wx.ComboBox(self.connectionBox, style=wx.TE_PROCESS_ENTER, name=_("AI Model:"))
		self.model.Bind(wx.EVT_TEXT, self.onModelFilter)
		cHelper.addItem(self.model)

		# Advanced Model Routing Box
		self.advRoutingCheck = cHelper.addItem(
			# Translators: Checkbox to toggle advanced model routing
			wx.CheckBox(self.connectionBox, label=_("Advanced Model Routing (Task-specific)")),
		)
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

		self.proxyMode = cHelper.addLabeledControl(
			# Translators: Label for Proxy Mode choice in settings
			_("Proxy Mode:"),
			wx.Choice,
			choices=[label for mode_id, label in vision_config.PROXY_MODES],
		)
		mode_ids = [mode_id for mode_id, label in vision_config.PROXY_MODES]
		cur_mode = nvda_config.conf["VisionAssistant"].get("proxy_mode", "auto")
		self.proxyMode.SetSelection(mode_ids.index(cur_mode) if cur_mode in mode_ids else 0)
		self.proxyMode.Bind(wx.EVT_CHOICE, self.onProxyModeChange)

		# Translators: Label for Proxy URL input
		self.proxyUrl = cHelper.addLabeledControl(_("Proxy URL:"), wx.TextCtrl)
		self.proxyUrl.Value = nvda_config.conf["VisionAssistant"]["proxy_url"]

		# Translators: Label for Proxy Username input
		self.proxyUsername = cHelper.addLabeledControl(_("Proxy Username:"), wx.TextCtrl)
		self.proxyUsername.Value = nvda_config.conf["VisionAssistant"].get("proxy_username", "")

		self.proxyPassword = cHelper.addLabeledControl(
			# Translators: Label for Proxy Password input
			_("Proxy Password:"),
			wx.TextCtrl,
			style=wx.TE_PASSWORD,
		)
		self.proxyPassword.Value = nvda_config.conf["VisionAssistant"].get("proxy_password", "")

		self.testProxyBtn = cHelper.addItem(
			# Translators: Label for button to test proxy connection
			wx.Button(self.connectionBox, label=_("&Test Proxy Connection")),
		)
		self.testProxyBtn.Bind(wx.EVT_BUTTON, self.onTestProxy)
		self.onProxyModeChange()

		self.checkUpdateStartup = cHelper.addItem(
			# Translators: Checkbox to enable/disable automatic update checks on startup
			wx.CheckBox(self.connectionBox, label=_("Check for updates on startup")),
		)
		self.checkUpdateStartup.Value = nvda_config.conf["VisionAssistant"]["check_update_startup"]
		self.cleanMarkdown = cHelper.addItem(
			# Translators: Checkbox to toggle markdown cleaning in chat windows
			wx.CheckBox(self.connectionBox, label=_("Clean Markdown in Chat")),
		)
		self.cleanMarkdown.Value = nvda_config.conf["VisionAssistant"]["clean_markdown_chat"]
		self.copyToClipboard = cHelper.addItem(
			# Translators: Checkbox to enable copying AI responses to clipboard
			wx.CheckBox(self.connectionBox, label=_("Copy AI responses to clipboard")),
		)
		self.copyToClipboard.Value = nvda_config.conf["VisionAssistant"]["copy_to_clipboard"]
		self.saveChatHistory = cHelper.addItem(
			# Translators: Checkbox to save chat conversations in the History list
			wx.CheckBox(self.connectionBox, label=_("Save chats to history")),
		)
		self.saveChatHistory.Value = nvda_config.conf["VisionAssistant"]["save_chat_history"]
		self.skipChatDialog = cHelper.addItem(
			# Translators: Checkbox to skip chat window and only speak AI responses
			wx.CheckBox(self.connectionBox, label=_("Direct Output (No Chat Window)")),
		)
		self.skipChatDialog.Value = nvda_config.conf["VisionAssistant"]["skip_chat_dialog"]
		self.connectionBox.SetSizer(connectionSizer)
		self.notebook.AddPage(self.connectionBox, groupLabel)

		# --- Live Assistant Group ---
		# Translators: Title of the settings group for Live Assistant features.
		groupLabel = _("Live Assistant")
		self.livePanel = wx.Panel(self.notebook)
		liveSizer = wx.BoxSizer(wx.VERTICAL)
		lvHelper = gui.guiHelper.BoxSizerHelper(self.livePanel, sizer=liveSizer)

		# 1. General Live Settings Group
		self.generalLiveGroupPanel = wx.Panel(self.livePanel)
		genGroupSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Title of the shared settings group for all Live features in the Live Assistant tab.
		generalLiveBox = wx.StaticBox(self.generalLiveGroupPanel, label=_("General Live Settings"))
		genBoxSizer = wx.StaticBoxSizer(generalLiveBox, wx.VERTICAL)
		genHelper = gui.guiHelper.BoxSizerHelper(generalLiveBox, sizer=genBoxSizer)

		self.audioDevices = vision_config.get_audio_output_devices()
		self.liveOutputDevice = genHelper.addLabeledControl(
			# Translators: Label for the audio output device selection choice box in Live settings.
			_("Audio Output Device:"),
			wx.Choice,
			choices=[d[1] for d in self.audioDevices],
		)
		curr_out_dev = nvda_config.conf["VisionAssistant"].get("live_output_device", "")
		sel_out = next((i for i, d in enumerate(self.audioDevices) if d[0] == curr_out_dev), 0)
		self.liveOutputDevice.SetSelection(sel_out)

		saved_interval = int(
			nvda_config.conf["VisionAssistant"].get(
				"live_frame_interval",
				nvda_config.conf["VisionAssistant"].get("ambient_frame_interval", 3),
			),
		)
		self.liveInterval = genHelper.addLabeledControl(
			# Translators: Label for the unified Live frame capture interval spin control.
			_("Frame Interval (seconds, 1 to 10):"),
			wx.SpinCtrl,
			min=1,
			max=10,
			value=str(saved_interval),
		)
		self.liveInterval.SetValue(saved_interval)
		self.ambientInterval = self.liveInterval

		# Translators: Label for selecting how deeply the Live Assistant thinks before answering.
		self.lblLiveThinking = wx.StaticText(generalLiveBox, label=_("Thinking &Depth:"))
		genHelper.addItem(self.lblLiveThinking)
		self.liveThinking = wx.Choice(
			generalLiveBox,
			choices=[x[0] for x in vision_config.LIVE_THINKING_CHOICES],
		)
		self.liveThinking.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.LIVE_THINKING_CHOICES)
					if x[1] == nvda_config.conf["VisionAssistant"].get("live_thinking_level", "medium")
				),
				2,
			),
		)
		genHelper.addItem(self.liveThinking)
		self._update_live_thinking_visibility()

		genGroupSizer.Add(genBoxSizer, 1, wx.EXPAND)
		self.generalLiveGroupPanel.SetSizer(genGroupSizer)

		# 2. Live Voice Assistant Group
		self.liveGroupPanel = wx.Panel(self.livePanel)
		liveGroupSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Title of the Live Voice Assistant settings group inside the Live Assistant tab.
		liveGroupBox = wx.StaticBox(self.liveGroupPanel, label=_("Live Voice Assistant"))
		liveGroupBoxSizer = wx.StaticBoxSizer(liveGroupBox, wx.VERTICAL)
		liveHelper = gui.guiHelper.BoxSizerHelper(liveGroupBox, sizer=liveGroupBoxSizer)

		self.liveDirectOutput = liveHelper.addItem(
			# Translators: Checkbox to start the Live Assistant without its conversation window (open it later with the Show Last Result key).
			wx.CheckBox(liveGroupBox, label=_("Direct Output (No Window)")),
		)
		self.liveDirectOutput.Value = nvda_config.conf["VisionAssistant"]["live_direct_output"]

		# Translators: Checkbox to enable push-to-talk mode for the Live Assistant.
		self.pttCheck = liveHelper.addItem(wx.CheckBox(liveGroupBox, label=_("Push to Talk")))
		self.pttCheck.Value = nvda_config.conf["VisionAssistant"].get("live_push_to_talk", False)
		self.pttCheck.Bind(wx.EVT_CHECKBOX, self.onTogglePtt)

		self.lblPttKey = wx.StaticText(
			liveGroupBox,
			# Translators: Label for the push-to-talk key field, instructing the user to press the keys to record it.
			label=_("Push to Talk Key (press the keys to record, for example F12 or Ctrl+F12):"),
		)
		liveHelper.addItem(self.lblPttKey)
		self.pttKeyCtrl = wx.TextCtrl(
			liveGroupBox,
			value=ptt_key_display(nvda_config.conf["VisionAssistant"].get("live_ptt_key", "")),
		)
		self.pttKeyCtrl.Bind(wx.EVT_SET_FOCUS, self._on_ptt_key_focus)
		self.pttKeyCtrl.Bind(wx.EVT_KILL_FOCUS, self._on_ptt_key_kill_focus)
		liveHelper.addItem(self.pttKeyCtrl)

		liveGroupSizer.Add(liveGroupBoxSizer, 1, wx.EXPAND)
		self.liveGroupPanel.SetSizer(liveGroupSizer)

		# 3. Ambient Observer Group
		self.ambientGroupPanel = wx.Panel(self.livePanel)
		ambientGroupSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Title of the Ambient Observer settings group in the Live Assistant tab.
		self.ambientBox = wx.StaticBox(self.ambientGroupPanel, label=_("Ambient Observer"))
		ambientSizer = wx.StaticBoxSizer(self.ambientBox, wx.VERTICAL)
		amHelper = gui.guiHelper.BoxSizerHelper(self.ambientBox, sizer=ambientSizer)
		self.ambientMode = amHelper.addLabeledControl(
			# Translators: Label for selecting the working mode of the Ambient Observer.
			_("Observer Mode:"),
			wx.Choice,
			choices=vision_config.AMBIENT_MODE_NAMES,
		)
		self.ambientMode.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.AMBIENT_MODE_LIST)
					if x[0] == nvda_config.conf["VisionAssistant"].get("ambient_observer_mode", "audio")
				),
				0,
			),
		)
		self.ambientSource = amHelper.addLabeledControl(
			# Translators: Label for selecting the audio source used by the Ambient Observer.
			_("Audio Source:"),
			wx.Choice,
			choices=vision_config.AMBIENT_SOURCE_NAMES,
		)
		self.ambientSource.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.AMBIENT_SOURCE_LIST)
					if x[0] == nvda_config.conf["VisionAssistant"].get("ambient_audio_source", "system")
				),
				0,
			),
		)
		self.ambientStyle = amHelper.addLabeledControl(
			# Translators: Label for selecting how detailed the Ambient Observer reports are.
			_("Reporting Style:"),
			wx.Choice,
			choices=vision_config.AMBIENT_STYLE_NAMES,
		)
		self.ambientStyle.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.AMBIENT_STYLE_LIST)
					if x[0] == nvda_config.conf["VisionAssistant"].get("ambient_reporting_style", "brief")
				),
				0,
			),
		)
		ambientGroupSizer.Add(ambientSizer, 1, wx.EXPAND)
		self.ambientGroupPanel.SetSizer(ambientGroupSizer)

		lvHelper.addItem(self.generalLiveGroupPanel)
		lvHelper.addItem(self.liveGroupPanel)
		lvHelper.addItem(self.ambientGroupPanel)

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
		temp_choices = [f"{x / 10:.1f}" for x in range(0, 21)]
		self.aiTemp = aiHelper.addLabeledControl(tempLabelText, wx.Choice, choices=temp_choices)
		current_temp = str(nvda_config.conf["VisionAssistant"].get("ai_temperature", 0.7))
		idx = self.aiTemp.FindString(current_temp)
		if idx != wx.NOT_FOUND:
			self.aiTemp.SetSelection(idx)
		else:
			self.aiTemp.SetSelection(7)
		aiBox.SetSizer(aiSizer)
		self.notebook.AddPage(aiBox, groupLabel)

		# --- Translation Languages Group ---
		# Translators: Title of the settings group for translation languages configuration
		groupLabel = _("Translation Languages")
		langBox = wx.Panel(self.notebook)
		langSizer = wx.BoxSizer(wx.VERTICAL)
		lHelper = gui.guiHelper.BoxSizerHelper(langBox, sizer=langSizer)
		self.sourceLang = lHelper.addLabeledControl(
			# Translators: Label for translation source language selection combo box.
			_("Source:"),
			wx.Choice,
			choices=vision_config.SOURCE_NAMES,
		)
		curr_s_code = nvda_config.conf["VisionAssistant"]["source_language"]
		s_idx = next((i for i, x in enumerate(vision_config.SOURCE_LIST) if x[1] == curr_s_code), 0)
		self.sourceLang.SetSelection(s_idx)
		self.targetLang = lHelper.addLabeledControl(
			# Translators: Checkbox to enable translation
			_("Target:"),
			wx.Choice,
			choices=vision_config.TARGET_NAMES,
		)
		curr_t_code = nvda_config.conf["VisionAssistant"]["target_language"]
		t_idx = next((i for i, x in enumerate(vision_config.TARGET_LIST) if x[1] == curr_t_code), 0)
		self.targetLang.SetSelection(t_idx)
		self.aiResponseLang = lHelper.addLabeledControl(
			# Translators: Label for Target Language selection
			_("AI Response:"),
			wx.Choice,
			choices=vision_config.TARGET_NAMES,
		)
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
		self.ocr_sel = dHelper.addLabeledControl(
			# Translators: Label for OCR Engine selection
			_("OCR Engine:"),
			wx.Choice,
			choices=[x[0] for x in vision_config.OCR_ENGINES],
		)
		curr_ocr = nvda_config.conf["VisionAssistant"]["ocr_engine"]
		try:
			o_idx = next(i for i, v in enumerate(vision_config.OCR_ENGINES) if v[1] == curr_ocr)
			self.ocr_sel.SetSelection(o_idx)
		except Exception:
			self.ocr_sel.SetSelection(0)

		self.lbl_batch = wx.StaticText(
			self.docBox,
			# Translators: Label for the OCR batch size setting. Set to 0 to process all pages in a single request.
			label=_("OCR Batch Size (Pages per request, 0 to disable):"),
		)
		dHelper.addItem(self.lbl_batch)
		self.batch_size = wx.SpinCtrl(
			self.docBox,
			min=0,
			max=100,
			initial=nvda_config.conf["VisionAssistant"]["ocr_batch_size"],
		)
		dHelper.addItem(self.batch_size)

		self.chk_describe_images = wx.CheckBox(
			self.docBox,
			# Translators: Label for the checkbox that enables image descriptions during OCR
			label=_("Describe images inline during document OCR"),
		)
		self.chk_describe_images.SetValue(
			nvda_config.conf["VisionAssistant"].get("describe_images_ocr", True),
		)
		dHelper.addItem(self.chk_describe_images)

		self.chk_export_page_numbers = wx.CheckBox(
			self.docBox,
			# Translators: Label for the checkbox that enables page numbers when exporting documents
			label=_("Include page numbers when exporting documents"),
		)
		self.chk_export_page_numbers.SetValue(
			nvda_config.conf["VisionAssistant"].get("document_export_page_numbers", True),
		)
		dHelper.addItem(self.chk_export_page_numbers)

		self.chk_save_doc_history = wx.CheckBox(
			self.docBox,
			# Translators: Checkbox to save documents in the History list
			label=_("Save documents to history"),
		)
		self.chk_save_doc_history.SetValue(
			nvda_config.conf["VisionAssistant"].get("save_document_history", True),
		)
		dHelper.addItem(self.chk_save_doc_history)

		# Translators: Label for the text-to-speech voice selection combo box in Document settings.
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

		self.lbl_vid_chunk = wx.StaticText(
			self.vidPanel,
			label=_(
				# Translators: Label for Video Chunk Size setting. Explains the trade-off between chunk size, API requests, and description quality.
				"Video Chunk Size for Audio Description (Minutes, 0 to disable):\nTip: Higher values use fewer API requests but rely on luck to succeed. Lower values guarantee highly detailed and precise descriptions.",
			),
		)
		vHelper.addItem(self.lbl_vid_chunk)
		self.vid_chunk_size = wx.SpinCtrl(
			self.vidPanel,
			min=0,
			max=300,
			initial=nvda_config.conf["VisionAssistant"]["video_srt_chunk_minutes"],
		)
		vHelper.addItem(self.vid_chunk_size)

		# Translators: Checkbox label to add character list as the first subtitle in video SRT output.
		self.vid_chars_as_sub = wx.CheckBox(self.vidPanel, label=_("Add character list as first subtitle"))
		self.vid_chars_as_sub.SetValue(
			nvda_config.conf["VisionAssistant"].get("video_chars_as_subtitle", True),
		)
		vHelper.addItem(self.vid_chars_as_sub)

		# Translators: Checkbox label to add an AI warning disclaimer at the beginning of the video SRT output.
		self.vid_add_disclaimer = wx.CheckBox(self.vidPanel, label=_("Add AI disclaimer at the beginning"))
		self.vid_add_disclaimer.SetValue(
			nvda_config.conf["VisionAssistant"].get("video_add_disclaimer", True),
		)
		vHelper.addItem(self.vid_add_disclaimer)
		# Translators: Button label to open the character dictionary management dialog from settings.
		self.manageSeriesBtn = wx.Button(self.vidPanel, label=_("Manage Characters..."))
		self.manageSeriesBtn.Bind(wx.EVT_BUTTON, self.onManageSeriesCharacters)
		vHelper.addItem(self.manageSeriesBtn)
		self.vidPanel.SetSizer(vidSizer)
		self.notebook.AddPage(self.vidPanel, groupLabel)

		# --- CAPTCHA Group ---
		groupLabel = _("CAPTCHA")
		capBox = wx.Panel(self.notebook)
		capSizer = wx.BoxSizer(wx.VERTICAL)
		capHelper = gui.guiHelper.BoxSizerHelper(capBox, sizer=capSizer)

		self.enableVisualCaptcha = capHelper.addItem(
			# Translators: Label for the checkbox that enables or disables the automated CAPTCHA solver feature.
			wx.CheckBox(capBox, label=_("Enable Visual CAPTCHA Solver")),
		)
		self.enableVisualCaptcha.Value = nvda_config.conf["VisionAssistant"].get(
			"enable_visual_captcha_solver",
			True,
		)

		self.captchaMode = capHelper.addLabeledControl(
			# Translators: Label for CAPTCHA capture method selection.
			_("Text CAPTCHA Method:"),
			wx.Choice,
			choices=[
				# Translators: A choice for capture method. Captures only the specific object under the cursor.
				_("Navigator Object"),
				# Translators: A choice for capture method. Captures the entire visible screen area.
				_("Full Screen"),
			],
		)

		self.captchaMode.SetSelection(
			0 if nvda_config.conf["VisionAssistant"]["captcha_mode"] == "navigator" else 1,
		)
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

		self.enableFileLogging = logHelper.addItem(
			# Translators: Checkbox label to enable dedicated add-on logging to file
			wx.CheckBox(logMgmtBox, label=_("Enable dedicated log file")),
		)
		self.enableFileLogging.Value = nvda_config.conf["VisionAssistant"].get("enable_file_logging", False)

		self.logLevels = [
			# Translators: Log level choice: Debug (Logs all detailed technical events, API calls, and raw responses)
			(_("Debug (All Details)"), "DEBUG"),
			# Translators: Log level choice: Info (Logs general operational events and task completions)
			(_("Info (General Information)"), "INFO"),
			# Translators: Log level choice: Warning (Logs warnings and non-fatal retries)
			(_("Warning (Warnings Only)"), "WARNING"),
			# Translators: Log level choice: Error (Logs errors and critical exceptions only)
			(_("Error (Errors Only)"), "ERROR"),
		]
		self.logLevelSel = logHelper.addLabeledControl(
			# Translators: Label for Log Level selection
			_("Log Level:"),
			wx.Choice,
			choices=[x[0] for x in self.logLevels],
		)
		curr_log_lvl = nvda_config.conf["VisionAssistant"].get("log_level", "DEBUG")
		try:
			lvl_idx = next(i for i, x in enumerate(self.logLevels) if x[1] == curr_log_lvl)
			self.logLevelSel.SetSelection(lvl_idx)
		except Exception:
			self.logLevelSel.SetSelection(0)

		self.logRetentionChoices = vision_config.LOG_RETENTION_OPTIONS
		self.logRetentionSel = logHelper.addLabeledControl(
			# Translators: Label for Log Retention Duration selection
			_("Keep Logs For:"),
			wx.Choice,
			choices=[x[0] for x in self.logRetentionChoices],
		)
		curr_ret_hrs = nvda_config.conf["VisionAssistant"].get("log_retention_hours", 168)
		try:
			ret_idx = next(i for i, x in enumerate(self.logRetentionChoices) if x[1] == curr_ret_hrs)
			self.logRetentionSel.SetSelection(ret_idx)
		except Exception:
			self.logRetentionSel.SetSelection(6)

		self.enableFileLogging.Bind(wx.EVT_CHECKBOX, self.onFileLoggingToggle)
		self.updateLoggingControlsState()

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
		backupSizer = wx.StaticBoxSizer(backupBox, wx.HORIZONTAL)

		# Translators: Button to save add-on settings and data to a backup file
		self.btnBackupSettings = wx.Button(advBox, label=_("Backup..."))
		self.btnBackupSettings.Bind(wx.EVT_BUTTON, self.onBackupSettings)
		backupSizer.Add(self.btnBackupSettings, 0, wx.ALL, 5)

		# Translators: Button to restore add-on settings and data from a backup file
		self.btnRestoreSettings = wx.Button(advBox, label=_("Restore..."))
		self.btnRestoreSettings.Bind(wx.EVT_BUTTON, self.onRestoreSettings)
		backupSizer.Add(self.btnRestoreSettings, 0, wx.ALL, 5)

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
			if voices and hasattr(self, "voice_sel"):
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

	def onManageSeriesCharacters(self, event):
		from ..dialogs.media import SeriesCharactersDialog

		gui.mainFrame.prePopup()
		try:
			dlg = SeriesCharactersDialog(self)
			dlg.ShowModal()
			dlg.Destroy()
		finally:
			gui.mainFrame.postPopup()

	def _live_supported_for(self, provider):
		if provider == "gemini":
			return True
		if provider == "custom":
			if hasattr(self, "customType") and self.customType.GetSelection() != wx.NOT_FOUND:
				return self.customType.GetSelection() == 1
			return nvda_config.conf["VisionAssistant"].get("custom_api_type", "openai") == "gemini"
		return False

	def updateCustomFieldsVisibility(self, provider):
		is_custom = provider == "custom"
		self.customBox.Show(is_custom)
		self.advRoutingCheck.Show(True)

		tts_supported = AIHandler.is_tts_supported(provider)
		routing_enabled = self.advRoutingCheck.Value
		self.advRoutingBox.Show(routing_enabled)

		live_supported = self._live_supported_for(provider)
		ptt_on = live_supported and self.pttCheck.Value
		self.liveGroupPanel.Show(live_supported)
		self.lblPttKey.Show(ptt_on)
		self.pttKeyCtrl.Show(ptt_on)
		self.ambientGroupPanel.Show(live_supported)

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

			if hasattr(self, "lbl_customModelName"):
				self.lbl_customModelName.Show(not has_fetched_models)
			self.customModelName.Show(not has_fetched_models)

			self.advEndpointBox.Show(self.useAdvancedEndpoints.Value)

			show_manual_fields = self.useAdvancedEndpoints.Value and not has_fetched_models

			if hasattr(self, "lblCustomOcrModel"):
				self.lblCustomOcrModel.Show(show_manual_fields)
			self.customOcrModel.Show(show_manual_fields)

			if hasattr(self, "lblCustomSttModel"):
				self.lblCustomSttModel.Show(show_manual_fields)
			self.customSttModel.Show(show_manual_fields)

			if hasattr(self, "lblCustomTtsModel"):
				self.lblCustomTtsModel.Show(show_manual_fields)
			self.customTtsModel.Show(show_manual_fields)

			if hasattr(self, "lblCustomOperatorModel"):
				self.lblCustomOperatorModel.Show(show_manual_fields)
			self.customAssistantModel.Show(show_manual_fields)

			self.customTtsVoice.Show(self.useAdvancedEndpoints.Value)
		else:
			self.modelLabel.Show(True)
			self.model.Show(True)
			if hasattr(self, "lbl_customModelName"):
				self.lbl_customModelName.Show(False)
			self.customModelName.Hide()

		if hasattr(self, "advEndpointBox"):
			self.advEndpointBox.Layout()
		self.connectionBox.Layout()
		self.Layout()
		is_gemini_api = False
		if provider == "gemini":
			is_gemini_api = True
		elif provider == "custom":
			custom_type_idx = self.customType.GetSelection()
			if custom_type_idx != wx.NOT_FOUND:
				is_gemini_api = custom_type_idx == 1
			else:
				is_gemini_api = nvda_config.conf["VisionAssistant"].get("custom_api_type") == "gemini"

		if hasattr(self, "notebook"):
			if hasattr(self, "vidPanel"):
				vid_index = -1
				for i in range(self.notebook.GetPageCount()):
					if self.notebook.GetPage(i) == self.vidPanel:
						vid_index = i
						break

				if is_gemini_api and vid_index == -1:
					self.notebook.InsertPage(4, self.vidPanel, _("Video"))
				elif not is_gemini_api and vid_index != -1:
					self.notebook.RemovePage(vid_index)

			if hasattr(self, "aiTemp"):
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

			if hasattr(self, "livePanel"):
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
		if p:
			p.Layout()
		show_batch_size = False
		if provider == "gemini" or provider == "mistral":
			show_batch_size = True
		elif provider == "custom":
			custom_type_idx = self.customType.GetSelection()
			if custom_type_idx != wx.NOT_FOUND:
				is_custom_gemini = custom_type_idx == 1
			else:
				is_custom_gemini = nvda_config.conf["VisionAssistant"].get("custom_api_type") == "gemini"

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
		if p:
			p.Layout()

	def onProviderChange(self, event):
		p_idx = self.provider_sel.GetSelection()
		p_name = PROVIDERS[p_idx]

		key_name = provider_key_name(p_name)
		val = nvda_config.conf["VisionAssistant"].get(key_name, "")

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
		self._update_live_thinking_visibility()

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
			"KoboldCPP (http://127.0.0.1:5001)",
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
					res_body = r.read().decode("utf-8")
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
				err_msg = _(
					# Translators: Error message when connection to local AI fails
					"Could not connect to the selected local AI. Make sure it is running on {url}",
				).format(url=url)
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
		p_name = PROVIDERS[p_idx]

		val = self.apiKeyCtrl_visible.Value if self.showApiCheck.IsChecked() else self.apiKeyCtrl_hidden.Value
		k_key = provider_key_name(p_name)
		nvda_config.conf["VisionAssistant"][k_key] = val.strip()
		nvda_config.conf["VisionAssistant"]["active_provider"] = p_name

		if p_name == "custom":
			nvda_config.conf["VisionAssistant"]["custom_api_url"] = self.customUrl.Value.strip()
			nvda_config.conf["VisionAssistant"]["custom_api_type"] = (
				"openai" if self.customType.GetSelection() == 0 else "gemini"
			)
			nvda_config.conf["VisionAssistant"]["use_advanced_endpoints"] = self.useAdvancedEndpoints.Value
			nvda_config.conf["VisionAssistant"]["custom_models_url"] = self.customModelsUrl.Value.strip()

		if getattr(self, "model", None) and self.model.IsShown():
			self.model.SetFocus()
		elif hasattr(self, "customModelName") and self.customModelName.IsShown():
			self.customModelName.SetFocus()

		self.btn_fetch.Disable()
		# Translators: Progress message shown while fetching AI models from the server
		ui.message(_("Fetching models..."))
		threading.Thread(target=self._fetch_models_thread, args=(p_name,), daemon=True).start()

	def onGetGeminiKey(self, event):
		try:
			from .gemini_keys import GeminiKeysDialog, gemini_manager_message
		except Exception as e:
			wx.MessageBox(str(e), _("Error"), wx.OK | wx.ICON_ERROR)
			return
		if not is_gemini_provider(strict=True):
			wx.MessageBox(gemini_manager_message(), _("Error"), wx.OK | wx.ICON_ERROR)
			return
		gui.mainFrame.prePopup()
		try:
			dlg = GeminiKeysDialog(gui.mainFrame)
			dlg.ShowModal()
			dlg.Destroy()
		except Exception as e:
			log.debug(f"Gemini API keys dialog failed: {e}")
			wx.MessageBox(str(e), _("Error"), wx.OK | wx.ICON_ERROR)
		finally:
			gui.mainFrame.postPopup()
		curr_p = nvda_config.conf["VisionAssistant"]["active_provider"]
		value = nvda_config.conf["VisionAssistant"][provider_key_name(curr_p)]
		self.apiKeyCtrl_hidden.SetValue(value)
		self.apiKeyCtrl_visible.SetValue(value)

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

	def _reset_advanced_model_lists(self):
		self.model.Clear()
		self.advOcrModel.Clear()
		self.advSttModel.Clear()
		self.advTtsModel.Clear()
		self.advOperatorModel.Clear()
		self.advVideoModel.Clear()
		self.advLiveModel.Clear()

		for cb in (
			self.model,
			self.advOcrModel,
			self.advSttModel,
			self.advTtsModel,
			self.advOperatorModel,
			self.advVideoModel,
			self.advLiveModel,
		):
			try:
				cb._all_models_backup = None
			except Exception:
				pass

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

	def _on_fetch_models_complete(self, p_name, models_info):
		self.btn_fetch.Enable()
		if models_info:
			prev_main = self._current_combo_id(self.model)
			prev_routing = {}
			for attr in (
				self.advOcrModel,
				self.advSttModel,
				self.advTtsModel,
				self.advOperatorModel,
				self.advVideoModel,
				self.advLiveModel,
			):
				prev_routing[attr] = self._current_combo_id(attr)
			self.model.Freeze()
			self._reset_advanced_model_lists()
			storage_parts = [f"{m_id}|{m_name}" for m_id, m_name in models_info]
			nvda_config.conf["VisionAssistant"][f"{p_name}_models_list"] = ",".join(storage_parts)

			main_models = AIHandler.filter_models(p_name, models_info, task="main")
			for m_id, m_name in main_models:
				self.model.Append(m_name, m_id)
				self._current_model_ids.append(m_id)

			ocr_models = AIHandler.filter_models(p_name, models_info, task="ocr")
			for m_id, m_name in ocr_models:
				self.advOcrModel.Append(m_name, m_id)

			stt_models = AIHandler.filter_models(p_name, models_info, task="stt")
			for m_id, m_name in stt_models:
				self.advSttModel.Append(m_name, m_id)

			tts_models = AIHandler.filter_models(p_name, models_info, task="tts")
			for m_id, m_name in tts_models:
				self.advTtsModel.Append(m_name, m_id)

			op_models = AIHandler.filter_models(p_name, models_info, task="operator")
			for m_id, m_name in op_models:
				self.advOperatorModel.Append(m_name, m_id)

			vid_models = AIHandler.filter_models(p_name, models_info, task="video")
			for m_id, m_name in vid_models:
				self.advVideoModel.Append(m_name, m_id)

			live_models = AIHandler.filter_models(p_name, models_info, task="live")
			for m_id, m_name in live_models:
				self.advLiveModel.Append(m_name, m_id)

			self.model.Thaw()

			self._restore_combo(self.model, prev_main)
			for attr in (
				self.advOcrModel,
				self.advSttModel,
				self.advTtsModel,
				self.advOperatorModel,
				self.advVideoModel,
				self.advLiveModel,
			):
				self._restore_combo(attr, prev_routing.get(attr))

			for cb in (
				self.model,
				self.advOcrModel,
				self.advSttModel,
				self.advTtsModel,
				self.advOperatorModel,
				self.advVideoModel,
				self.advLiveModel,
			):
				cb._all_models_backup = [(cb.GetString(i), cb.GetClientData(i)) for i in range(cb.GetCount())]

			self._all_models_backup = list(getattr(self.model, "_all_models_backup", []))

			self.updateVoiceList(p_name)

			self.updateCustomFieldsVisibility(p_name)
			# Translators: Status message when the AI models list is successfully refreshed.
			ui.message(_("Models updated"))
		else:
			# Translators: Error message shown when the add-on cannot retrieve the list of models from the server.
			ui.message(_("Failed to fetch models"))

		target_ctrl = (
			self.model
			if getattr(self, "model", None) and self.model.IsShown()
			else getattr(self, "btn_fetch", None)
		)
		if target_ctrl:
			wx.CallAfter(target_ctrl.SetFocus)

	def refreshModelList(self, p_name):
		self._reset_advanced_model_lists()
		saved_models_raw = nvda_config.conf["VisionAssistant"].get(f"{p_name}_models_list", "")
		all_models = []
		if saved_models_raw:
			items = saved_models_raw.split(",")
			for item in items:
				if "|" in item:
					m_id, m_name = item.split("|", 1)
					all_models.append((m_id, m_name))
		elif p_name == "gemini":
			for m_name, m_id in vision_config.MODELS:
				all_models.append((m_id, m_name))

		main_models = AIHandler.filter_models(p_name, all_models, task="main")
		for m_id, m_name in main_models:
			self.model.Append(m_name, m_id)
			self._current_model_ids.append(m_id)

		ocr_models = AIHandler.filter_models(p_name, all_models, task="ocr")
		for m_id, m_name in ocr_models:
			self.advOcrModel.Append(m_name, m_id)

		stt_models = AIHandler.filter_models(p_name, all_models, task="stt")
		for m_id, m_name in stt_models:
			self.advSttModel.Append(m_name, m_id)

		tts_models = AIHandler.filter_models(p_name, all_models, task="tts")
		for m_id, m_name in tts_models:
			self.advTtsModel.Append(m_name, m_id)

		op_models = AIHandler.filter_models(p_name, all_models, task="operator")
		for m_id, m_name in op_models:
			self.advOperatorModel.Append(m_name, m_id)

		vid_models = AIHandler.filter_models(p_name, all_models, task="video")
		for m_id, m_name in vid_models:
			self.advVideoModel.Append(m_name, m_id)

		live_models = AIHandler.filter_models(p_name, all_models, task="live")
		for m_id, m_name in live_models:
			self.advLiveModel.Append(m_name, m_id)

		for m_id, m_name in all_models:
			if m_id not in self._current_model_ids:
				self._current_model_ids.append(m_id)

		for cb in (
			self.model,
			self.advOcrModel,
			self.advSttModel,
			self.advTtsModel,
			self.advOperatorModel,
			self.advVideoModel,
			self.advLiveModel,
		):
			cb._all_models_backup = [(cb.GetString(i), cb.GetClientData(i)) for i in range(cb.GetCount())]
		self._all_models_backup = list(getattr(self.model, "_all_models_backup", []))

		m_key = provider_model_name(p_name)
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
			else:
				attr.SetSelection(0)
		self._all_models_backup = [
			(self.model.GetString(i), self.model.GetClientData(i)) for i in range(self.model.GetCount())
		]
		self.updateCustomFieldsVisibility(p_name)

	def onToggleAdvanced(self, event):
		p_idx = self.provider_sel.GetSelection()
		if p_idx != wx.NOT_FOUND:
			p_name = PROVIDERS[p_idx]
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

	def onVoiceSelectionChanged(self, event):
		sel = self.voice_sel.GetSelection()
		if sel != wx.NOT_FOUND:
			voice_id = self.voice_sel.GetClientData(sel)
			p_idx = self.provider_sel.GetSelection()
			if p_idx != wx.NOT_FOUND:
				p_name = PROVIDERS[p_idx]
				if p_name == "custom":
					self.customTtsVoice.SetValue(voice_id)

	def onCustomUrlChange(self, event):
		self.model.Clear()
		self._all_models_backup = []
		p_idx = self.provider_sel.GetSelection()
		if p_idx != wx.NOT_FOUND:
			p_name = PROVIDERS[p_idx]
			if p_name == "custom":
				nvda_config.conf["VisionAssistant"]["custom_models_list"] = ""
				self.updateCustomFieldsVisibility("custom")
		event.Skip()

	def onProxyModeChange(self, event=None):
		sel = self.proxyMode.GetSelection()
		if sel != wx.NOT_FOUND:
			mode_id = vision_config.PROXY_MODES[sel][0]
		else:
			mode_id = "auto"
		is_reverse = mode_id == "reverse"
		self.proxyUsername.Enable(not is_reverse)
		self.proxyPassword.Enable(not is_reverse)
		if event and hasattr(event, "Skip"):
			event.Skip()

	def onTestProxy(self, event=None):
		# Translators: Spoken message when proxy connection test starts
		ui.message(_("Testing proxy connection..."))

		raw_url = (self.proxyUrl.Value or "").strip()
		if not raw_url:
			# Translators: Spoken message when proxy URL is missing during connection test
			ui.message(_("Please enter a proxy URL first."))
			return

		proxy_mode_idx = self.proxyMode.GetSelection()
		proxy_mode = (
			vision_config.PROXY_MODES[proxy_mode_idx][0] if proxy_mode_idx != wx.NOT_FOUND else "auto"
		)
		proxy_user = (self.proxyUsername.Value or "").strip()
		proxy_pass = (self.proxyPassword.Value or "").strip()

		p_idx = self.provider_sel.GetSelection()
		provider = PROVIDERS[p_idx] if p_idx != wx.NOT_FOUND else "gemini"

		active_key = (
			self.apiKeyCtrl_visible.Value if self.showApiCheck.IsChecked() else self.apiKeyCtrl_hidden.Value
		).strip()
		if active_key:
			api_key = active_key.replace("\r", "\n").split("\n")[0].split(",")[0].strip()
		else:
			keys = AIHandler.get_keys(provider)
			api_key = keys[0] if keys else ""

		def _run():
			try:
				from ..utils.media_capture import test_proxy_connection

				success, msg, latency = test_proxy_connection(
					proxy_url=raw_url,
					proxy_mode=proxy_mode,
					proxy_user=proxy_user,
					proxy_pass=proxy_pass,
					provider=provider,
					api_key=api_key,
				)
				wx.CallAfter(ui.message, msg)
			except Exception as e:
				log.error(f"Error testing proxy connection: {e}", exc_info=True)
				# Translators: Spoken message when testing proxy connection fails with error details
				err_msg = _("Proxy test error: {error}").format(error=str(e))
				wx.CallAfter(ui.message, err_msg)

		t = threading.Thread(target=_run, daemon=True)
		t.start()

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

	def isValid(self):
		if not self.pttCheck.Value or normalize_ptt_key(self.pttKeyCtrl.Value):
			return True
		p_idx = self.provider_sel.GetSelection()
		p_name = PROVIDERS[p_idx] if p_idx != wx.NOT_FOUND else "gemini"
		if not self._live_supported_for(p_name):
			return True
		gui.messageBox(
			_(
				# Translators: Warning shown when Push to Talk is enabled but no key has been assigned in settings.
				"You have not assigned a Push to Talk key. Please press a key in the Push to Talk Key field, or disable Push to Talk.",
			),
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
			vision_config.register_config_spec()
		except Exception as e:
			log.debug(f"Config spec refresh failed: {e}")
		try:
			p_idx = self.provider_sel.GetSelection()
			p_name = PROVIDERS[p_idx]
			nvda_config.conf["VisionAssistant"]["active_provider"] = p_name

			val = (
				self.apiKeyCtrl_visible.Value
				if self.showApiCheck.IsChecked()
				else self.apiKeyCtrl_hidden.Value
			)
			k_key = provider_key_name(p_name)
			nvda_config.conf["VisionAssistant"][k_key] = val.strip()

			m_key = provider_model_name(p_name)
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
				nvda_config.conf["VisionAssistant"]["custom_api_type"] = (
					"openai" if self.customType.GetSelection() == 0 else "gemini"
				)
				nvda_config.conf["VisionAssistant"]["custom_upload_support"] = self.customUploadSupport.Value
				nvda_config.conf["VisionAssistant"]["use_advanced_endpoints"] = (
					self.useAdvancedEndpoints.Value
				)
				nvda_config.conf["VisionAssistant"]["custom_models_url"] = self.customModelsUrl.Value.strip()
				nvda_config.conf["VisionAssistant"]["custom_ocr_url"] = self.customOcrUrl.Value.strip()
				nvda_config.conf["VisionAssistant"]["custom_stt_url"] = self.customSttUrl.Value.strip()
				nvda_config.conf["VisionAssistant"]["custom_tts_url"] = self.customTtsUrl.Value.strip()
				nvda_config.conf["VisionAssistant"]["custom_operator_url"] = (
					self.customAssistantUrl.Value.strip()
				)
				if not has_fetched_models:
					nvda_config.conf["VisionAssistant"]["custom_ocr_model"] = (
						self.customOcrModel.Value.strip()
					)
					nvda_config.conf["VisionAssistant"]["custom_stt_model"] = (
						self.customSttModel.Value.strip()
					)
					nvda_config.conf["VisionAssistant"]["custom_tts_model"] = (
						self.customTtsModel.Value.strip()
					)
					nvda_config.conf["VisionAssistant"]["custom_operator_model"] = (
						self.customAssistantModel.Value.strip()
					)

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
			proxy_mode_idx = self.proxyMode.GetSelection()
			if proxy_mode_idx != wx.NOT_FOUND:
				nvda_config.conf["VisionAssistant"]["proxy_mode"] = vision_config.PROXY_MODES[proxy_mode_idx][
					0
				]
			nvda_config.conf["VisionAssistant"]["proxy_username"] = self.proxyUsername.Value.strip()
			nvda_config.conf["VisionAssistant"]["proxy_password"] = self.proxyPassword.Value.strip()
			nvda_config.conf["VisionAssistant"]["source_language"] = vision_config.SOURCE_LIST[
				self.sourceLang.GetSelection()
			][1]
			nvda_config.conf["VisionAssistant"]["target_language"] = vision_config.TARGET_LIST[
				self.targetLang.GetSelection()
			][1]
			nvda_config.conf["VisionAssistant"]["ai_response_language"] = vision_config.TARGET_LIST[
				self.aiResponseLang.GetSelection()
			][1]
			nvda_config.conf["VisionAssistant"]["smart_swap"] = self.smartSwap.Value
			nvda_config.conf["VisionAssistant"]["check_update_startup"] = self.checkUpdateStartup.Value
			nvda_config.conf["VisionAssistant"]["clean_markdown_chat"] = self.cleanMarkdown.Value
			nvda_config.conf["VisionAssistant"]["copy_to_clipboard"] = self.copyToClipboard.Value
			nvda_config.conf["VisionAssistant"]["skip_chat_dialog"] = self.skipChatDialog.Value
			nvda_config.conf["VisionAssistant"]["live_direct_output"] = self.liveDirectOutput.Value
			nvda_config.conf["VisionAssistant"]["live_push_to_talk"] = self.pttCheck.Value
			nvda_config.conf["VisionAssistant"]["live_ptt_key"] = normalize_ptt_key(self.pttKeyCtrl.Value)
			live_thinking_idx = self.liveThinking.GetSelection()
			if live_thinking_idx != wx.NOT_FOUND:
				nvda_config.conf["VisionAssistant"]["live_thinking_level"] = (
					vision_config.LIVE_THINKING_CHOICES[live_thinking_idx][1]
				)
			amb_mode_idx = self.ambientMode.GetSelection()
			if amb_mode_idx != wx.NOT_FOUND:
				nvda_config.conf["VisionAssistant"]["ambient_observer_mode"] = (
					vision_config.AMBIENT_MODE_LIST[amb_mode_idx][0]
				)
			amb_src_idx = self.ambientSource.GetSelection()
			if amb_src_idx != wx.NOT_FOUND:
				nvda_config.conf["VisionAssistant"]["ambient_audio_source"] = (
					vision_config.AMBIENT_SOURCE_LIST[amb_src_idx][0]
				)
			dev_idx = self.liveOutputDevice.GetSelection()
			if dev_idx != wx.NOT_FOUND and hasattr(self, "audioDevices") and dev_idx < len(self.audioDevices):
				nvda_config.conf["VisionAssistant"]["live_output_device"] = self.audioDevices[dev_idx][0]
			try:
				amb_interval = int(self.liveInterval.GetValue())
			except Exception as e:
				log.debug(f"Live frame interval read failed: {e}")
				amb_interval = 3
			amb_interval = max(1, min(10, amb_interval))
			nvda_config.conf["VisionAssistant"]["live_frame_interval"] = amb_interval
			nvda_config.conf["VisionAssistant"]["ambient_frame_interval"] = amb_interval
			amb_style_idx = self.ambientStyle.GetSelection()
			if amb_style_idx != wx.NOT_FOUND:
				nvda_config.conf["VisionAssistant"]["ambient_reporting_style"] = (
					vision_config.AMBIENT_STYLE_LIST[amb_style_idx][0]
				)
			nvda_config.conf["VisionAssistant"]["captcha_mode"] = (
				"navigator" if self.captchaMode.GetSelection() == 0 else "fullscreen"
			)
			nvda_config.conf["VisionAssistant"]["enable_visual_captcha_solver"] = (
				self.enableVisualCaptcha.Value
			)
			nvda_config.conf["VisionAssistant"]["ocr_engine"] = vision_config.OCR_ENGINES[
				self.ocr_sel.GetSelection()
			][1]
			nvda_config.conf["VisionAssistant"]["ocr_batch_size"] = self.batch_size.GetValue()
			nvda_config.conf["VisionAssistant"]["describe_images_ocr"] = self.chk_describe_images.Value
			nvda_config.conf["VisionAssistant"]["document_export_page_numbers"] = (
				self.chk_export_page_numbers.Value
			)
			nvda_config.conf["VisionAssistant"]["save_chat_history"] = self.saveChatHistory.Value
			nvda_config.conf["VisionAssistant"]["save_document_history"] = self.chk_save_doc_history.Value
			nvda_config.conf["VisionAssistant"]["video_srt_chunk_minutes"] = self.vid_chunk_size.GetValue()
			nvda_config.conf["VisionAssistant"]["video_chars_as_subtitle"] = self.vid_chars_as_sub.Value
			nvda_config.conf["VisionAssistant"]["video_add_disclaimer"] = self.vid_add_disclaimer.Value
			nvda_config.conf["VisionAssistant"]["enable_file_logging"] = self.enableFileLogging.Value
			l_idx = self.logLevelSel.GetSelection()
			if l_idx != wx.NOT_FOUND:
				nvda_config.conf["VisionAssistant"]["log_level"] = self.logLevels[l_idx][1]
			r_idx = self.logRetentionSel.GetSelection()
			if r_idx != wx.NOT_FOUND:
				nvda_config.conf["VisionAssistant"]["log_retention_hours"] = self.logRetentionChoices[r_idx][
					1
				]
			nvda_config.conf["VisionAssistant"]["custom_prompts_v2"] = serialize_custom_prompts_v2(
				self.customPromptItems,
			)
			nvda_config.conf["VisionAssistant"]["default_refine_prompts"] = (
				serialize_default_prompt_overrides(self.defaultPromptItems)
			)

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
			wx.CallAfter(
				gui.messageBox,
				# Translators: Message box content when saving settings fails
				_("Save Error: {error}").format(error=e),
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)

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

	def onFileLoggingToggle(self, event):
		self.updateLoggingControlsState()
		event.Skip()

	def updateLoggingControlsState(self):
		enabled = self.enableFileLogging.Value
		self.logLevelSel.Enable(enabled)
		self.logRetentionSel.Enable(enabled)

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
			# Translators: Backup option in settings to export everything including settings, labels, OCR progress, and history
			BACKUP_ALL = _("Everything (Settings, Labels, OCR Progress, History)")
			# Translators: Backup option in settings to export settings configuration only
			BACKUP_SETTINGS_ONLY = _("Settings Only")
			choices = [BACKUP_ALL, BACKUP_SETTINGS_ONLY]
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
		try:
			settings_data = nvda_config.conf["VisionAssistant"].dict()
			settings_data["custom_prompts_v2"] = serialize_custom_prompts_v2(self.customPromptItems)
			settings_data["default_refine_prompts"] = serialize_default_prompt_overrides(
				self.defaultPromptItems,
			)
			payload = {
				"format": "VisionAssistantSettingsBackup",
				"version": 2,
				"settings": settings_data,
			}
			if include_data:
				data = {}
				for key, fpath in (
					("labels", vision_config.LABELS_FILE),
					("ocr_progress", vision_config.OCR_PROGRESS_FILE),
					("ocr_text_cache", vision_config.OCR_TEXT_CACHE_FILE),
					("series", vision_config.SERIES_FILE),
					("history", vision_config.HISTORY_FILE),
				):
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
				gui.messageBox(
					# Translators: Error message when the chosen backup file cannot be read.
					_("Could not read the backup file: {error}").format(error=e),
					_("Error"),
					wx.OK | wx.ICON_ERROR,
				)
				return
			if (
				not isinstance(payload, dict)
				or payload.get("format") != "VisionAssistantSettingsBackup"
				or not isinstance(payload.get("settings"), dict)
			):
				gui.messageBox(
					# Translators: Error message when the chosen file is not a valid settings backup.
					_("This file is not a valid Vision Assistant settings backup."),
					_("Error"),
					wx.OK | wx.ICON_ERROR,
				)
				return
			has_data = isinstance(payload.get("data"), dict)
			if has_data:
				confirm_msg = _(
					# Translators: Confirmation prompt shown before restoring a full backup, because it replaces all current settings and data.
					"Restoring will replace all current settings and data (labels, OCR progress, and history). Do you want to continue?",
				)
			else:
				# Translators: Confirmation prompt shown before restoring, because it replaces all current settings.
				confirm_msg = _("Restoring will replace all current settings. Do you want to continue?")
			if (
				gui.messageBox(
					confirm_msg,
					# Translators: Title of the confirmation dialog for restoring settings.
					_("Restore Settings"),
					wx.YES_NO | wx.ICON_WARNING,
				)
				!= wx.YES
			):
				return
		finally:
			gui.mainFrame.postPopup()
		try:
			nvda_config.conf["VisionAssistant"] = payload["settings"]
		except Exception as e:
			log.error(f"onRestoreSettings failed to apply: {e}", exc_info=True)
			gui.mainFrame.prePopup()
			try:
				gui.messageBox(
					# Translators: Error message when applying the restored settings fails.
					_("Restore failed: {error}").format(error=e),
					_("Error"),
					wx.OK | wx.ICON_ERROR,
				)
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
			for key, fpath in (
				("labels", vision_config.LABELS_FILE),
				("ocr_progress", vision_config.OCR_PROGRESS_FILE),
				("ocr_text_cache", vision_config.OCR_TEXT_CACHE_FILE),
				("series", vision_config.SERIES_FILE),
				("history", vision_config.HISTORY_FILE),
			):
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
		# Translators: Message announced after a successful restore.
		ui.message(_("Backup restored successfully."))

	def _reloadControlsFromConfig(self):
		conf = nvda_config.conf["VisionAssistant"]
		providers = PROVIDERS
		curr_p = conf.get("active_provider", "gemini")
		try:
			p_idx = next(i for i, x in enumerate(providers) if x == curr_p)
		except Exception:
			p_idx = 0
		self.provider_sel.SetSelection(p_idx)

		k_key = provider_key_name(curr_p)
		key_val = conf.get(k_key, "")
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
		self.proxyMode.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.PROXY_MODES)
					if x[0] == conf.get("proxy_mode", "auto")
				),
				0,
			),
		)
		self.proxyUsername.SetValue(conf.get("proxy_username", ""))
		self.proxyPassword.SetValue(conf.get("proxy_password", ""))
		self.onProxyModeChange()
		self.checkUpdateStartup.SetValue(conf.get("check_update_startup", False))
		self.cleanMarkdown.SetValue(conf.get("clean_markdown_chat", True))
		self.copyToClipboard.SetValue(conf.get("copy_to_clipboard", False))
		self.skipChatDialog.SetValue(conf.get("skip_chat_dialog", False))
		self.saveChatHistory.SetValue(conf.get("save_chat_history", True))
		self.liveDirectOutput.SetValue(conf.get("live_direct_output", False))
		self.pttCheck.SetValue(conf.get("live_push_to_talk", False))
		self.pttKeyCtrl.SetValue(ptt_key_display(conf.get("live_ptt_key", "")))
		self.liveThinking.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.LIVE_THINKING_CHOICES)
					if x[1] == conf.get("live_thinking_level", "medium")
				),
				2,
			),
		)
		self.ambientMode.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.AMBIENT_MODE_LIST)
					if x[0] == conf.get("ambient_observer_mode", "audio")
				),
				0,
			),
		)
		self.ambientSource.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.AMBIENT_SOURCE_LIST)
					if x[0] == conf.get("ambient_audio_source", "system")
				),
				0,
			),
		)
		curr_out_dev = conf.get("live_output_device", "")
		if hasattr(self, "audioDevices") and hasattr(self, "liveOutputDevice"):
			self.liveOutputDevice.SetSelection(
				next((i for i, d in enumerate(self.audioDevices) if d[0] == curr_out_dev), 0),
			)
		if hasattr(self, "liveInterval"):
			self.liveInterval.SetValue(
				int(conf.get("live_frame_interval", conf.get("ambient_frame_interval", 3))),
			)
		self.ambientStyle.SetSelection(
			next(
				(
					i
					for i, x in enumerate(vision_config.AMBIENT_STYLE_LIST)
					if x[0] == conf.get("ambient_reporting_style", "brief")
				),
				0,
			),
		)

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
		self.chk_save_doc_history.SetValue(conf.get("save_document_history", True))

		self.vid_chunk_size.SetValue(conf.get("video_srt_chunk_minutes", 10))
		self.vid_chars_as_sub.SetValue(conf.get("video_chars_as_subtitle", True))
		self.vid_add_disclaimer.SetValue(conf.get("video_add_disclaimer", True))

		self.enableVisualCaptcha.SetValue(conf.get("enable_visual_captcha_solver", True))
		self.captchaMode.SetSelection(0 if conf.get("captcha_mode", "navigator") == "navigator" else 1)

		self.enableFileLogging.SetValue(conf.get("enable_file_logging", False))
		lvl = conf.get("log_level", "DEBUG")
		lvl_idx = next((i for i, x in enumerate(self.logLevels) if x[1] == lvl), 0)
		self.logLevelSel.SetSelection(lvl_idx)
		ret_hrs = conf.get("log_retention_hours", 168)
		ret_idx = next((i for i, x in enumerate(self.logRetentionChoices) if x[1] == ret_hrs), 6)
		self.logRetentionSel.SetSelection(ret_idx)
		self.updateLoggingControlsState()

		self._temp_models = {}
		self.refreshModelList(curr_p)
		self.updateVoiceList(curr_p)
		self.updateCustomFieldsVisibility(curr_p)

	def onNotebookPageChanged(self, event):
		event.Skip()
		self._update_live_thinking_visibility()

	def _current_live_model(self):
		conf = nvda_config.conf["VisionAssistant"]
		from ..utils.media_capture import resolve_live_model

		model = ""
		if conf.get("advanced_model_routing", False):
			try:
				sel = self.advLiveModel.GetSelection()
				if sel != wx.NOT_FOUND:
					model = (self.advLiveModel.GetClientData(sel) or "").strip()
				if not model:
					model = self.advLiveModel.GetValue().strip()
			except Exception as e:
				log.debug(f"Live model UI read failed: {e}")
				model = ""
		return model or resolve_live_model()

	def _update_live_thinking_visibility(self):
		lbl = getattr(self, "lblLiveThinking", None)
		ctrl = getattr(self, "liveThinking", None)
		panel = getattr(self, "liveGroupPanel", None)
		if lbl is None or ctrl is None:
			return
		from ..utils.media_capture import live_thinking_choices, live_thinking_level, live_thinking_supported

		model = self._current_live_model()
		choices = live_thinking_choices(model)
		current = nvda_config.conf["VisionAssistant"].get("live_thinking_level", "medium")
		selection = ctrl.GetSelection()
		if selection != wx.NOT_FOUND and selection < len(vision_config.LIVE_THINKING_CHOICES):
			current = vision_config.LIVE_THINKING_CHOICES[selection][1]
		current = live_thinking_level(model, current)
		ctrl.Set([choice[0] for choice in choices])
		levels = [choice[1] for choice in choices]
		if current in levels:
			ctrl.SetSelection(levels.index(current))
		else:
			ctrl.SetSelection(next((i for i, level in enumerate(levels) if level == "medium"), 0))
		shown = live_thinking_supported(model)
		for item in (lbl, ctrl):
			item.Show(shown)
		if panel is not None:
			panel.Layout()

	def onModelFilter(self, event):
		cb = event.GetEventObject()
		if cb.IsFrozen():
			return
		if cb is getattr(self, "advLiveModel", None):
			self._update_live_thinking_visibility()

		sel = cb.GetSelection()
		if sel != wx.NOT_FOUND:
			model_id = cb.GetClientData(sel)
			if cb == getattr(self, "model", None):
				p_idx = (
					getattr(self, "provider_sel", None).GetSelection()
					if getattr(self, "provider_sel", None)
					else -1
				)
				if p_idx == 4 and model_id:
					self.customModelName.SetValue(model_id)
			return

		filtered = apply_model_filter(cb, cb.GetValue())

		if filtered:
			# Translators: Notification showing the number of items found after filtering the model list.
			ui.message(_("{count} items found").format(count=len(filtered)))
