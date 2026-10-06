# -*- coding: utf-8 -*-
import logging
import os

import wx
import addonHandler
import config as nvda_config

from .. import plugin_state
from .. import vision_config

log = logging.getLogger(__name__)

addonHandler.initTranslation()


class LiveAssistantDialog(wx.Dialog):
	instance = None

	def __init__(
		self,
		parent,
		start_callback,
		end_callback,
		initial_history="",
		webcam_callback=None,
		webcam_device_callback=None,
	):
		# Translators: Title of the Live Assistant conversation window.
		title_text = _("{name} - Live Assistant").format(name=vision_config.ADDON_NAME)
		super().__init__(
			parent, title=title_text, size=(500, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		self.start_callback = start_callback
		self.end_callback = end_callback
		self.webcam_callback = webcam_callback
		self.webcam_device_callback = webcam_device_callback
		self.is_active = True
		LiveAssistantDialog.instance = self

		panel = wx.Panel(self)
		self.panel = panel
		sizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Label for the conversation history area in the Live Assistant window.
		sizer.Add(wx.StaticText(panel, label=_("Conversation:")), 0, wx.ALL, 5)
		self.history = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
		if initial_history:
			self.history.SetValue(initial_history)
			self.history.SetInsertionPointEnd()
		sizer.Add(self.history, 1, wx.EXPAND | wx.ALL, 5)

		hbox_voice = wx.BoxSizer(wx.HORIZONTAL)
		hbox_voice.Add(
			# Translators: Label for TTS Voice selection in the Live Assistant window.
			wx.StaticText(panel, label=_("&TTS Voice:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5
		)

		self.voice_sel = wx.Choice(panel, choices=[f"{v[0]} - {v[1]}" for v in vision_config.GEMINI_VOICES])
		curr_voice = nvda_config.conf["VisionAssistant"].get("tts_voice", "Puck")
		for i, v in enumerate(vision_config.GEMINI_VOICES):
			if v[0] == curr_voice:
				self.voice_sel.SetSelection(i)
				break
		else:
			if self.voice_sel.GetCount() > 0:
				self.voice_sel.SetSelection(0)

		self.voice_sel.Bind(wx.EVT_CHOICE, self.on_voice_change)
		hbox_voice.Add(self.voice_sel, 1, wx.EXPAND)
		sizer.Add(hbox_voice, 0, wx.EXPAND | wx.ALL, 5)

		hbox_thinking = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Label for Thinking Depth selection in the Live Assistant window.
		hbox_thinking.Add(
			wx.StaticText(panel, label=_("Thinking &Depth:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5
		)

		from ..utils.media_capture import (
			live_thinking_choices,
			live_thinking_level,
			live_thinking_supported,
			resolve_live_model,
		)

		live_model = resolve_live_model()
		self.thinking_choices = live_thinking_choices(live_model)
		self.thinking_sel = wx.Choice(panel, choices=[x[0] for x in self.thinking_choices])
		curr_thinking = live_thinking_level(
			live_model, nvda_config.conf["VisionAssistant"].get("live_thinking_level", "medium")
		)
		self.thinking_sel.SetSelection(
			next((i for i, x in enumerate(self.thinking_choices) if x[1] == curr_thinking), 0)
		)
		if not live_thinking_supported(live_model):
			self.thinking_sel.Enable(False)
			self.thinking_sel.SetSelection(
				next((i for i, x in enumerate(self.thinking_choices) if x[1] == "medium"), 0)
			)

		self.thinking_sel.Bind(wx.EVT_CHOICE, self.on_thinking_change)
		hbox_thinking.Add(self.thinking_sel, 1, wx.EXPAND)
		sizer.Add(hbox_thinking, 0, wx.EXPAND | wx.ALL, 5)

		hbox_device = wx.BoxSizer(wx.HORIZONTAL)
		hbox_device.Add(
			# Translators: Label for Audio Output Device selection in the Live Assistant window.
			wx.StaticText(panel, label=_("&Audio Device:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5
		)
		self.audio_devices = vision_config.get_audio_output_devices()
		self.device_sel = wx.Choice(panel, choices=[d[1] for d in self.audio_devices])
		curr_device = nvda_config.conf["VisionAssistant"].get("live_output_device", "")
		sel_dev = next((i for i, d in enumerate(self.audio_devices) if d[0] == curr_device), 0)
		self.device_sel.SetSelection(sel_dev)
		self.device_sel.Bind(wx.EVT_CHOICE, self.on_device_change)
		hbox_device.Add(self.device_sel, 1, wx.EXPAND)
		sizer.Add(hbox_device, 0, wx.EXPAND | wx.ALL, 5)

		# Translators: Checkbox in the Live Assistant window to enable push-to-talk mode.
		self.ptt_check = wx.CheckBox(panel, label=_("Push to &Talk"))
		self.ptt_check.Value = bool(nvda_config.conf["VisionAssistant"].get("live_push_to_talk", False))
		self.ptt_check.Bind(wx.EVT_CHECKBOX, self.on_ptt_change)
		sizer.Add(self.ptt_check, 0, wx.ALL, 5)

		# Translators: Read-only label showing the assigned push-to-talk key in the Live Assistant window.
		self.ptt_key_label = wx.StaticText(panel, label="")
		sizer.Add(self.ptt_key_label, 0, wx.LEFT | wx.RIGHT, 5)
		self._update_ptt_key_label()

		hbox_webcam = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Checkbox in the Live Assistant window to send webcam frames instead of the screen.
		self.webcam_check = wx.CheckBox(panel, label=_("Use &Webcam"))
		self.webcam_check.Bind(wx.EVT_CHECKBOX, self.on_webcam_change)
		hbox_webcam.Add(self.webcam_check, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

		# Translators: Button in the Live Assistant window to open Windows Camera privacy settings.
		self.camera_privacy_btn = wx.Button(panel, label=_("Camera &Privacy Settings..."))
		self.camera_privacy_btn.Bind(wx.EVT_BUTTON, self.on_camera_privacy)
		self.camera_privacy_btn.Hide()
		hbox_webcam.Add(self.camera_privacy_btn, 0, wx.ALIGN_CENTER_VERTICAL)

		self.webcam_row = hbox_webcam
		self.webcam_device_names = []
		self.webcam_choice = None
		self.webcam_choice_label = None

		sizer.Add(hbox_webcam, 0, wx.ALL, 5)

		# Translators: Button cancelling the Live Assistant's current computer operation without ending the conversation.
		self.operator_stop = wx.Button(panel, label=_("Stop operator action"))
		self.operator_stop.Bind(wx.EVT_BUTTON, self.on_operator_stop)
		sizer.Add(self.operator_stop, 0, wx.ALL, 5)
		inst = plugin_state.plugin_instance
		operator_active = bool(inst and inst._live_operator_on())
		self.operator_stop.Show(operator_active)
		self.operator_stop.Enable(operator_active)
		self._apply_webcam_lock()

		# Translators: Button that ends the live voice conversation.
		self.toggle_btn = wx.Button(panel, label=_("&End"))
		self.toggle_btn.Bind(wx.EVT_BUTTON, self.on_toggle)
		sizer.Add(self.toggle_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

		panel.SetSizer(sizer)

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		main_sizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(main_sizer)

		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)
		self.history.SetFocus()

	def on_operator_stop(self, event):
		inst = plugin_state.plugin_instance
		if inst:
			inst._stop_live_operator()

	def on_voice_change(self, event):
		sel = self.voice_sel.GetSelection()
		if sel != wx.NOT_FOUND:
			nvda_config.conf["VisionAssistant"]["tts_voice"] = vision_config.GEMINI_VOICES[sel][0]
			if self.is_active:
				# Translators: Message shown in conversation log when voice is changed
				self.append_line(_("--- Changing voice, reconnecting... ---"))
				self._restart_session()

	def on_thinking_change(self, event):
		sel = self.thinking_sel.GetSelection()
		if sel != wx.NOT_FOUND:
			from ..utils.media_capture import live_thinking_level, resolve_live_model

			value = live_thinking_level(resolve_live_model(), self.thinking_choices[sel][1])
			nvda_config.conf["VisionAssistant"]["live_thinking_level"] = value
			index = next((i for i, x in enumerate(self.thinking_choices) if x[1] == value), sel)
			if index != sel:
				self.thinking_sel.SetSelection(index)
			if self.is_active:
				# Translators: Message shown in conversation log when thinking depth is changed
				self.append_line(_("--- Changing thinking depth, reconnecting... ---"))
				self._restart_session()

	def on_device_change(self, event):
		sel = self.device_sel.GetSelection()
		if sel != wx.NOT_FOUND and sel < len(self.audio_devices):
			dev_id = self.audio_devices[sel][0]
			nvda_config.conf["VisionAssistant"]["live_output_device"] = dev_id
			inst = plugin_state.plugin_instance
			if inst and getattr(inst, "live_session", None):
				try:
					inst.live_session.set_output_device(dev_id)
				except Exception as e:
					log.debug(f"Live device dynamic update failed: {e}")

	def on_ptt_change(self, event):
		enabled = bool(self.ptt_check.Value)
		nvda_config.conf["VisionAssistant"]["live_push_to_talk"] = enabled
		inst = plugin_state.plugin_instance
		if inst and getattr(inst, "live_session", None):
			inst.live_session.set_push_to_talk(enabled)

	def _update_ptt_key_label(self):
		from ..prompt_utils import ptt_key_display

		key = nvda_config.conf["VisionAssistant"].get("live_ptt_key", "")
		display = ptt_key_display(key)
		if display:
			# Translators: Label showing the assigned push-to-talk key in the Live Assistant window. {key} is replaced with the key name.
			self.ptt_key_label.SetLabel(_("Push to Talk Key: {key}").format(key=display))
			self.ptt_key_label.Show()
		else:
			self.ptt_key_label.SetLabel("")
			self.ptt_key_label.Hide()

	def clear_history(self):
		self.history.SetValue("")

	def _restart_session(self):
		self._restarting = True
		webcam = bool(self.webcam_check.Value)
		if self.end_callback:
			self.end_callback()

		def restart():
			if self.start_callback:
				self.start_callback()
			self._restarting = False
			if webcam and self.webcam_callback:
				self.webcam_callback(True)

		self._restart_timer = wx.CallLater(1200, restart)

	def on_webcam_change(self, event):
		if self._operator_locks_webcam():
			self.webcam_check.SetValue(False)
			if self.webcam_callback:
				self.webcam_callback(False)
			return
		if self.webcam_callback:
			self.webcam_callback(bool(self.webcam_check.Value))
		self._sync_webcam_choice_state()

	def on_webcam_device_change(self, event):
		choice = getattr(self, "webcam_choice", None)
		if choice is None:
			return
		idx = choice.GetSelection()
		if idx == wx.NOT_FOUND:
			return
		device = choice.GetString(idx)
		try:
			nvda_config.conf["VisionAssistant"]["live_webcam_device"] = device
		except Exception as e:
			log.debug(f"Webcam device preference save failed: {e}")
		if self.webcam_device_callback:
			self.webcam_device_callback(device)

	def on_camera_privacy(self, event):
		try:
			os.startfile("ms-settings:privacy-webcam")
		except Exception as e:
			log.debug(f"Failed to open camera privacy settings: {e}")

	def set_webcam_available(self, devices, ffmpeg_path, privacy_blocked=False):
		if privacy_blocked:
			self._remove_webcam_choice()
			self.webcam_check.Show()
			self.webcam_check.Disable()
			self.webcam_check.SetValue(False)
			# Translators: Label shown when camera access is blocked in Windows privacy settings.
			self.webcam_check.SetLabel(_("Use &Webcam (camera access blocked in Windows Privacy)"))
			self.camera_privacy_btn.Show()
			self.panel.Layout()
		elif devices:
			self.webcam_check.Show()
			self.webcam_check.Enable()
			# Translators: Checkbox in the Live Assistant window to send webcam frames instead of the screen.
			self.webcam_check.SetLabel(_("Use &Webcam"))
			self.camera_privacy_btn.Hide()
			self._ensure_webcam_choice(devices)
			self.panel.Layout()
		elif not ffmpeg_path:
			self._remove_webcam_choice()
			self.webcam_check.Show()
			self.webcam_check.Enable()
			self.webcam_check.SetValue(False)
			# Translators: Label shown when ffmpeg is missing; ticking the checkbox starts the ffmpeg download.
			self.webcam_check.SetLabel(_("Use &Webcam (ffmpeg required)"))
			self.camera_privacy_btn.Hide()
			self.panel.Layout()
		else:
			self._remove_webcam_choice()
			self.webcam_check.Hide()
			self.camera_privacy_btn.Hide()
			self.panel.Layout()
		self._apply_webcam_lock()

	def _operator_locks_webcam(self):
		inst = plugin_state.plugin_instance
		return bool(inst and inst._live_operator_on())

	def _apply_webcam_lock(self):
		if self._operator_locks_webcam():
			if self.webcam_check.Value:
				self.webcam_check.SetValue(False)
				if self.webcam_callback:
					self.webcam_callback(False)
			self.webcam_check.Disable()
			# Translators: Label shown when the webcam cannot be used because Live operator control is on.
			self.webcam_check.SetLabel(_("Use &Webcam (not available with operator control)"))
			if self.webcam_choice is not None:
				self.webcam_choice.Disable()
		elif self.webcam_check.GetLabel() == _("Use &Webcam (not available with operator control)"):
			self.webcam_check.SetLabel(_("Use &Webcam"))
			self.webcam_check.Enable()
			self._sync_webcam_choice_state()
		self.panel.Layout()

	def set_webcam_active(self, active):
		if active and self._operator_locks_webcam():
			active = False
		self.webcam_check.SetValue(bool(active))
		self._sync_webcam_choice_state()

	def _sync_webcam_choice_state(self):
		if self.webcam_choice is not None:
			self.webcam_choice.Enable(bool(self.webcam_check.Value and self.webcam_check.IsEnabled()))

	def _remove_webcam_choice(self):
		if self.webcam_choice is None:
			return
		for ctrl in (self.webcam_choice_label, self.webcam_choice):
			if ctrl is None:
				continue
			try:
				self.webcam_row.Detach(ctrl)
			except Exception as e:
				log.debug(f"Webcam device picker detach failed: {e}")
			try:
				ctrl.Destroy()
			except Exception as e:
				log.debug(f"Webcam device picker destroy failed: {e}")
		self.webcam_choice_label = None
		self.webcam_choice = None
		self.panel.Layout()

	def _ensure_webcam_choice(self, devices):
		names = list(devices or [])
		if len(names) < 2:
			self._remove_webcam_choice()
			return
		if self.webcam_choice is None:
			# Translators: Label for selecting which video device is used for webcam frames in the Live Assistant window.
			self.webcam_choice_label = wx.StaticText(self.panel, label=_("Video device:"))
			self.webcam_choice = wx.Choice(self.panel)
			self.webcam_choice.Bind(wx.EVT_CHOICE, self.on_webcam_device_change)
			self.webcam_row.Add(self.webcam_choice_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
			self.webcam_row.Add(self.webcam_choice, 0, wx.ALIGN_CENTER_VERTICAL)
		self.webcam_choice.Clear()
		self.webcam_choice.AppendItems(names)
		saved = nvda_config.conf["VisionAssistant"].get("live_webcam_device", "")
		selected = saved if saved in names else names[0]
		self.webcam_choice.SetStringSelection(selected)
		self._sync_webcam_choice_state()

	def on_char_hook(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
		else:
			event.Skip()

	def append_line(self, line):
		self.history.AppendText(line + "\n")

	def append_raw(self, text):
		self.history.AppendText(text)

	def set_active(self, active):
		self.is_active = active
		# Translators: Button that ends the live voice conversation.
		btn_end = _("&End")
		# Translators: Button that starts the live voice conversation.
		btn_start = _("&Start")
		self.toggle_btn.SetLabel(btn_end if active else btn_start)

	def on_toggle(self, event):
		if self.is_active:
			if self.end_callback:
				self.end_callback()
		else:
			if self.start_callback:
				self.start_callback()

	def on_close(self, event):
		t = getattr(self, "_restart_timer", None)
		if t:
			t.Stop()
			self._restart_timer = None
		if self.is_active and self.end_callback:
			self.end_callback()
		if self.webcam_callback:
			self.webcam_callback(False)
		LiveAssistantDialog.instance = None
		self.Destroy()
