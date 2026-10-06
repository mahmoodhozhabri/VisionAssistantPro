# -*- coding: utf-8 -*-
import re
import time

import wx

import addonHandler
import inputCore
import keyboardHandler
import ui

from ..prompt_utils import (
	_normalize_hotkey,
	_format_hotkey_display,
	validate_custom_prompt_content,
	get_feedback_behavior_options,
)
from ..vision_config import LAYER_BUSY_GESTURES

addonHandler.initTranslation()


class PromptItemDialog(wx.Dialog):
	def __init__(
		self,
		parent,
		title,
		name="",
		prompt_text="",
		hotkey="",
		variables_guide=None,
		feedback_behavior="global",
	):
		super().__init__(
			parent,
			title=title,
			size=(620, 420),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		self.name_ctrl = None
		self.prompt_ctrl = None
		self.variables_guide = tuple(variables_guide or ())
		self._capture_func = None
		self._last_captured_combo = None
		self._last_captured_time = 0.0

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Label for prompt name input field.
		name_label = wx.StaticText(self, label=_("Name:"))
		main_sizer.Add(name_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
		self.name_ctrl = wx.TextCtrl(self, value=name)
		main_sizer.Add(self.name_ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		hotkey_label = wx.StaticText(
			self,
			# Translators: Label for the optional shortcut key assigned to this custom prompt, instructing the user to press the keys to record it.
			label=_("Shortcut Key (optional): press the keys to record, for example Ctrl+Shift+1"),
		)
		main_sizer.Add(hotkey_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		self.hotkey_ctrl = wx.TextCtrl(self, value=hotkey)
		self.hotkey_ctrl.Bind(wx.EVT_SET_FOCUS, self._on_hotkey_focus)
		self.hotkey_ctrl.Bind(wx.EVT_KILL_FOCUS, self._on_hotkey_kill_focus)
		self.Bind(wx.EVT_CLOSE, self._on_close)
		main_sizer.Add(self.hotkey_ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		# Translators: Label for the feedback behavior choice of a custom prompt.
		feedback_label = wx.StaticText(self, label=_("Feedback behavior:"))
		main_sizer.Add(feedback_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		self.feedback_choices = get_feedback_behavior_options()
		self.feedback_ctrl = wx.Choice(
			self,
			choices=[label for _val, label in self.feedback_choices],
		)
		selected_fb_idx = 0
		for idx, (val, _lbl) in enumerate(self.feedback_choices):
			if val == feedback_behavior:
				selected_fb_idx = idx
				break
		self.feedback_ctrl.SetSelection(selected_fb_idx)
		main_sizer.Add(self.feedback_ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		# Translators: Label for prompt text input field.
		prompt_label = wx.StaticText(self, label=_("Prompt Text:"))
		main_sizer.Add(prompt_label, 0, wx.LEFT | wx.RIGHT, 10)
		self.prompt_ctrl = wx.TextCtrl(
			self,
			value=prompt_text,
			style=wx.TE_MULTILINE | wx.TE_DONTWRAP,
		)
		main_sizer.Add(self.prompt_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		button_sizer = wx.StdDialogButtonSizer()
		ok_btn = wx.Button(self, wx.ID_OK)
		ok_btn.SetDefault()
		cancel_btn = wx.Button(self, wx.ID_CANCEL)
		button_sizer.AddButton(ok_btn)
		button_sizer.AddButton(cancel_btn)
		button_sizer.Realize()

		footer_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button label to open the variables help dialog.
		self.variables_btn = wx.Button(self, label=_("Variables Guide"))
		self.variables_btn.Bind(wx.EVT_BUTTON, self.on_open_variables)
		footer_sizer.Add(self.variables_btn, 0, wx.RIGHT, 10)
		footer_sizer.AddStretchSpacer()
		footer_sizer.Add(button_sizer, 0)
		main_sizer.Add(footer_sizer, 0, wx.EXPAND | wx.ALL, 10)

		self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)
		self.SetSizer(main_sizer)
		self.name_ctrl.SetFocus()

	def on_ok(self, event):
		self._stop_hotkey_capture()
		name = self.name_ctrl.GetValue().strip()
		prompt_text = self.prompt_ctrl.GetValue()

		if not name:
			# Translators: Validation error for empty prompt name.
			msg = _("Name cannot be empty.")
			# Translators: Title of validation warning dialog.
			title = _("Validation Error")
			wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			self.name_ctrl.SetFocus()
			return
		raw_hotkey = self.hotkey_ctrl.GetValue().strip()
		normalized_hotkey = _normalize_hotkey(raw_hotkey)
		if raw_hotkey and not normalized_hotkey:
			msg = _(
				# Translators: Validation error for an invalid shortcut key.
				"Shortcut key must be a key or key combination, for example: 1, p, alt+1, control+shift+p, insert+1, or f3.",
			)
			title = _("Validation Error")
			wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			self.hotkey_ctrl.SetFocus()
			return
		if normalized_hotkey in LAYER_BUSY_GESTURES:
			msg = _(
				# Translators: Validation error when the chosen shortcut key is already used by another command in the command layer.
				"This key is already used by another command in the command layer (NVDA+Shift+V). Please choose a different key.",
			)
			title = _("Validation Error")
			wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			self.hotkey_ctrl.SetFocus()
			return
		if not prompt_text.strip():
			# Translators: Validation error for empty prompt text.
			msg = _("Prompt text cannot be empty.")
			title = _("Validation Error")
			wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			self.prompt_ctrl.SetFocus()
			return
		is_valid, err_msg = validate_custom_prompt_content(prompt_text)
		if not is_valid:
			title = _("Validation Error")
			wx.MessageBox(err_msg, title, wx.OK | wx.ICON_WARNING)
			self.prompt_ctrl.SetFocus()
			return
		event.Skip()

	def on_open_variables(self, event):
		dlg = PromptVariablesGuideDialog(self, self.variables_guide)
		dlg.ShowModal()
		dlg.Destroy()

	def get_item(self):
		sel = self.feedback_ctrl.GetSelection()
		if 0 <= sel < len(self.feedback_choices):
			feedback_behavior = self.feedback_choices[sel][0]
		else:
			feedback_behavior = "global"
		return {
			"name": self.name_ctrl.GetValue().strip(),
			"content": self.prompt_ctrl.GetValue(),
			"hotkey": _normalize_hotkey(self.hotkey_ctrl.GetValue()),
			"feedback_behavior": feedback_behavior,
		}

	def _on_hotkey_focus(self, event):
		try:
			if inputCore.manager._captureFunc is not None:
				event.Skip()
				return
		except Exception:
			pass
		self._capture_func = self._hotkey_captor
		self._last_captured_combo = None
		self._last_captured_time = 0.0
		try:
			inputCore.manager._captureFunc = self._capture_func
		except Exception:
			pass
		event.Skip()

	def _on_hotkey_kill_focus(self, event):
		self._stop_hotkey_capture()
		event.Skip()

	def _on_close(self, event):
		self._stop_hotkey_capture()
		event.Skip()

	def _stop_hotkey_capture(self):
		try:
			if inputCore.manager._captureFunc is getattr(self, "_capture_func", None):
				inputCore.manager._captureFunc = None
				self._capture_func = None
		except Exception:
			pass

	def _hotkey_captor(self, gesture):
		if not isinstance(gesture, keyboardHandler.KeyboardInputGesture):
			return True
		if gesture.isModifier:
			return False
		try:
			identifier = gesture.identifiers[-1]
		except Exception:
			return True
		if ":" not in identifier:
			return True
		combo = identifier.rsplit(":", 1)[1].strip().lower()
		if combo in ("escape", "enter", "tab"):
			return None
		now = time.monotonic()
		if combo == self._last_captured_combo and now - self._last_captured_time < 0.5:
			return False
		self._last_captured_combo = combo
		self._last_captured_time = now
		if combo in ("backspace", "delete"):
			wx.CallAfter(self._set_hotkey_value, "")
			return False
		if not _normalize_hotkey(combo):
			return False
		wx.CallAfter(self._set_hotkey_value, combo)
		return False

	def _set_hotkey_value(self, combo):
		try:
			display = _format_hotkey_display(_normalize_hotkey(combo))
			if self.hotkey_ctrl.GetValue() == display:
				return
			self.hotkey_ctrl.SetValue(display)
			if display:
				ui.message(display)
		except Exception:
			pass


class PromptVariablesGuideDialog(wx.Dialog):
	def __init__(self, parent, variables_guide):
		# Translators: Title for the prompt variables help dialog.
		dlg_title = _("Prompt Variables Guide")
		super().__init__(
			parent,
			title=dlg_title,
			size=(620, 420),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Intro text for the prompt variables help dialog.
		intro = wx.StaticText(self, label=_("Use these variables inside prompt text:"))
		main_sizer.Add(intro, 0, wx.ALL, 10)

		lines = []
		for token, description, input_type in variables_guide:
			if not description and not input_type:
				if lines:
					lines.append("")
				lines.append(f"--- {token} ---")
			else:
				lines.append(f"{token} - {description} ({input_type})")

		content = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP)
		content.SetValue("\n".join(lines))
		main_sizer.Add(content, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		# Translators: Button to close chat dialog
		close_btn = wx.Button(self, wx.ID_OK, label=_("Close"))
		close_btn.SetDefault()
		main_sizer.Add(close_btn, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		self.SetSizer(main_sizer)


class PromptManagerDialog(wx.Dialog):
	def __init__(self, parent, default_items, custom_items, variables_guide=None):
		# Translators: Title for the prompt manager dialog.
		dlg_title = _("Prompt Manager")
		super().__init__(
			parent,
			title=dlg_title,
			size=(760, 560),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		self.default_items = [dict(item) for item in default_items]
		self.custom_items = []
		for item in custom_items:
			item = dict(item)
			item.setdefault("hotkey", "")
			item.setdefault("feedback_behavior", "global")
			self.custom_items.append(item)
		self.variables_guide = tuple(variables_guide or ())
		self._default_selection = wx.NOT_FOUND

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.notebook = wx.Notebook(self)
		self.default_panel = wx.Panel(self.notebook)
		self.custom_panel = wx.Panel(self.notebook)
		# Translators: Notebook tab for built-in refine prompts.
		self.notebook.AddPage(self.default_panel, _("Default Prompts"))
		# Translators: Notebook tab for user-defined prompts.
		self.notebook.AddPage(self.custom_panel, _("Custom Prompts"))
		main_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)

		self._build_default_tab()
		self._build_custom_tab()

		footer_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.variables_btn = wx.Button(self, label=_("Variables Guide"))
		self.variables_btn.Bind(wx.EVT_BUTTON, self.on_open_variables)
		footer_sizer.Add(self.variables_btn, 0, wx.RIGHT, 10)
		# Translators: Note explaining when prompt changes are persisted.
		self.save_note = wx.StaticText(self, label=_("Changes are applied only when you press OK."))
		footer_sizer.Add(self.save_note, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
		footer_sizer.AddStretchSpacer()

		ok_btn = wx.Button(self, wx.ID_OK)
		ok_btn.SetDefault()
		cancel_btn = wx.Button(self, wx.ID_CANCEL)
		ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
		footer_sizer.Add(ok_btn, 0, wx.RIGHT, 8)
		footer_sizer.Add(cancel_btn, 0)
		main_sizer.Add(footer_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		self.SetSizer(main_sizer)
		self.CentreOnParent()

	def _build_default_tab(self):
		tab_sizer = wx.BoxSizer(wx.HORIZONTAL)

		left_sizer = wx.BoxSizer(wx.VERTICAL)
		default_list_label = wx.StaticText(self.default_panel, label=_("Default Prompts"))
		left_sizer.Add(default_list_label, 0, wx.BOTTOM, 5)
		filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
		filter_sizer.Add(
			# Translators: Label for the filter field above the default prompts list in the Prompt Manager.
			wx.StaticText(self.default_panel, label=_("Filter:")),
			0,
			wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
			5,
		)
		self.default_filter = wx.ComboBox(self.default_panel, style=wx.CB_READONLY)
		self.default_filter.Bind(wx.EVT_COMBOBOX, self.on_default_filter_change)
		filter_sizer.Add(self.default_filter, 1, wx.EXPAND)
		left_sizer.Add(filter_sizer, 0, wx.EXPAND | wx.BOTTOM, 8)
		self.default_list = wx.ListBox(
			self.default_panel,
			choices=[item.get("display_label", item["label"]) for item in self.default_items],
			style=wx.LB_SINGLE,
		)
		self.default_list.SetMinSize((320, -1))
		self.default_list.Bind(wx.EVT_LISTBOX, self.on_default_selected)
		left_sizer.Add(self.default_list, 1, wx.EXPAND | wx.BOTTOM, 8)

		# Translators: Button label to reset currently selected default prompt.
		self.reset_selected_btn = wx.Button(self.default_panel, label=_("Reset Selected"))
		self.reset_selected_btn.Bind(wx.EVT_BUTTON, self.on_reset_selected_default)
		left_sizer.Add(self.reset_selected_btn, 0, wx.EXPAND | wx.BOTTOM, 5)

		# Translators: Button label to reset all default prompts.
		self.reset_all_btn = wx.Button(self.default_panel, label=_("Reset All"))
		self.reset_all_btn.Bind(wx.EVT_BUTTON, self.on_reset_all_defaults)
		left_sizer.Add(self.reset_all_btn, 0, wx.EXPAND)

		right_sizer = wx.BoxSizer(wx.VERTICAL)
		default_prompt_label = wx.StaticText(self.default_panel, label=_("Prompt Text:"))
		right_sizer.Add(default_prompt_label, 0, wx.BOTTOM, 5)
		self.default_prompt_ctrl = wx.TextCtrl(
			self.default_panel,
			style=wx.TE_MULTILINE | wx.TE_DONTWRAP,
		)
		right_sizer.Add(self.default_prompt_ctrl, 1, wx.EXPAND | wx.BOTTOM, 8)

		# Translators: Button label to apply current editor text to the selected default prompt.
		self.save_default_btn = wx.Button(self.default_panel, label=_("Apply to Selected"))
		self.save_default_btn.Bind(wx.EVT_BUTTON, self.on_save_selected_default)
		right_sizer.Add(self.save_default_btn, 0, wx.ALIGN_RIGHT)

		tab_sizer.Add(left_sizer, 0, wx.EXPAND | wx.ALL, 10)
		tab_sizer.Add(right_sizer, 1, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 10)
		self.default_panel.SetSizer(tab_sizer)

		self._default_view = []
		self._apply_default_filter()

	def _default_filter_choices(self):
		sections = sorted(
			{str(item.get("section", "")).strip() for item in self.default_items if item.get("section")},
		)
		# Translators: Option in the Prompt Manager filter list that shows prompts from every section.
		self._default_filter_all = _("All")
		return [self._default_filter_all] + sections

	def _apply_default_filter(self):
		if self.default_filter.GetCount() == 0 and self.default_items:
			self.default_filter.Set(self._default_filter_choices())
			self.default_filter.SetSelection(0)
		wanted = self.default_filter.GetValue()
		if wanted == getattr(self, "_default_filter_all", ""):
			wanted = ""
		view = []
		for i, item in enumerate(self.default_items):
			if not wanted or str(item.get("section", "")).strip() == wanted:
				view.append(i)
		self._default_view = view
		self.default_list.Set(
			[
				self.default_items[i].get("display_label", self.default_items[i]["label"])
				for i in self._default_view
			],
		)
		if not self._default_view:
			self._default_selection = wx.NOT_FOUND
			self.default_prompt_ctrl.SetValue("")
			self.save_default_btn.Disable()
			self.reset_selected_btn.Disable()
			self.reset_all_btn.Disable()
			return
		if self._default_selection in self._default_view:
			position = self._default_view.index(self._default_selection)
		else:
			position = 0
			self._default_selection = self._default_view[0]
		self.default_list.SetSelection(position)
		self.default_prompt_ctrl.SetValue(self.default_items[self._default_selection]["prompt"])
		self.save_default_btn.Enable()
		self.reset_selected_btn.Enable()
		self.reset_all_btn.Enable()

	def _select_default_item(self, item_index):
		if item_index in self._default_view:
			self.default_list.SetSelection(self._default_view.index(item_index))

	def on_default_filter_change(self, event):
		self._apply_default_filter()

	def _build_custom_tab(self):
		tab_sizer = wx.BoxSizer(wx.HORIZONTAL)

		left_sizer = wx.BoxSizer(wx.VERTICAL)
		custom_list_label = wx.StaticText(self.custom_panel, label=_("Custom Prompts"))
		left_sizer.Add(custom_list_label, 0, wx.BOTTOM, 5)
		self.custom_list = wx.ListBox(self.custom_panel, style=wx.LB_SINGLE)
		self.custom_list.SetMinSize((240, -1))
		self.custom_list.Bind(wx.EVT_LISTBOX, self.on_custom_selected)
		left_sizer.Add(self.custom_list, 1, wx.EXPAND | wx.BOTTOM, 8)

		action_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button label for adding a custom prompt.
		self.add_custom_btn = wx.Button(self.custom_panel, label=_("Add"))
		# Translators: Button label for editing a custom prompt.
		self.edit_custom_btn = wx.Button(self.custom_panel, label=_("Edit"))
		# Translators: Button label for removing a custom prompt.
		self.remove_custom_btn = wx.Button(self.custom_panel, label=_("Remove"))
		self.add_custom_btn.Bind(wx.EVT_BUTTON, self.on_add_custom)
		self.edit_custom_btn.Bind(wx.EVT_BUTTON, self.on_edit_custom)
		self.remove_custom_btn.Bind(wx.EVT_BUTTON, self.on_remove_custom)
		action_sizer.Add(self.add_custom_btn, 0, wx.RIGHT, 5)
		action_sizer.Add(self.edit_custom_btn, 0, wx.RIGHT, 5)
		action_sizer.Add(self.remove_custom_btn, 0)
		left_sizer.Add(action_sizer, 0, wx.EXPAND | wx.BOTTOM, 5)

		move_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button label for moving selected custom prompt up in the list.
		self.move_up_btn = wx.Button(self.custom_panel, label=_("Move Up"))
		# Translators: Button label for moving selected custom prompt down in the list.
		self.move_down_btn = wx.Button(self.custom_panel, label=_("Move Down"))
		self.move_up_btn.Bind(wx.EVT_BUTTON, self.on_move_custom_up)
		self.move_down_btn.Bind(wx.EVT_BUTTON, self.on_move_custom_down)
		move_sizer.Add(self.move_up_btn, 0, wx.RIGHT, 5)
		move_sizer.Add(self.move_down_btn, 0)
		left_sizer.Add(move_sizer, 0, wx.EXPAND)

		right_sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Label above the custom prompt preview area.
		custom_preview_label = wx.StaticText(self.custom_panel, label=_("Prompt Preview:"))
		right_sizer.Add(custom_preview_label, 0, wx.BOTTOM, 5)
		self.custom_preview = wx.TextCtrl(
			self.custom_panel,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP,
		)
		right_sizer.Add(self.custom_preview, 1, wx.EXPAND)

		tab_sizer.Add(left_sizer, 0, wx.EXPAND | wx.ALL, 10)
		tab_sizer.Add(right_sizer, 1, wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, 10)
		self.custom_panel.SetSizer(tab_sizer)

		self._refresh_custom_list()

	def _is_guarded_prompt(self, item):
		return bool(item.get("guarded"))

	def _get_guarded_feature_label(self, item):
		label = item.get("guardedFeatureLabel") or item.get("label") or item.get("key") or ""
		return str(label).strip()

	def _validate_guarded_prompt(self, item, prompt_text):
		if not self._is_guarded_prompt(item):
			return True

		missing_markers = []
		for marker in item.get("requiredMarkers", []):
			if not isinstance(marker, str):
				continue
			marker = marker.strip()
			if marker and marker not in prompt_text:
				missing_markers.append(marker)

		failed_regex = []
		for check in item.get("requiredRegex", []):
			pattern = ""
			description = ""
			if isinstance(check, dict):
				pattern = str(check.get("pattern", "")).strip()
				description = str(check.get("description", "")).strip()
			elif isinstance(check, str):
				pattern = check.strip()
			if not pattern:
				continue
			try:
				if re.search(pattern, prompt_text, re.MULTILINE | re.DOTALL):
					continue
			except re.error:
				continue
			failed_regex.append(description or pattern)

		if not missing_markers and not failed_regex:
			return True

		feature = self._get_guarded_feature_label(item)
		required_items = []
		seen_required_items = set()
		for required_item in list(missing_markers) + list(failed_regex):
			required_item = str(required_item).strip()
			if not required_item or required_item in seen_required_items:
				continue
			seen_required_items.add(required_item)
			required_items.append(required_item)
		lines = [
			# Translators: Validation message shown when required text is missing in a guarded prompt.
			_("This prompt is used by {feature}. To save it, add the required text below:").format(
				feature=feature,
			),
			"",
		]
		lines.extend([f"- {required_item}" for required_item in required_items])
		lines.append("")
		# Translators: Guidance shown after listing missing required text.
		lines.append(_("Add these items exactly as written, then try again."))
		# Translators: Title of validation warning dialog for guarded prompt checks.
		title = _("Required Text Missing")
		wx.MessageBox("\n".join(lines), title, wx.OK | wx.ICON_WARNING)
		self.default_prompt_ctrl.SetFocus()
		return False

	def _confirm_guarded_save(self, item):
		if not self._is_guarded_prompt(item):
			return True

		feature = self._get_guarded_feature_label(item)
		msg = _(
			# Translators: Confirmation message shown before saving a guarded prompt.
			"You are editing a prompt used by {feature}.\n\nIf this prompt is changed, this feature may not work correctly.\n\nDo you understand the risk and want to save anyway?",
		).format(feature=feature)
		# Translators: Title of confirmation dialog shown before saving guarded prompts.
		title = _("Confirm")
		dlg = wx.MessageDialog(self, msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
		try:
			# Translators: Confirm button label for guarded prompt save confirmation.
			yes_label = _("Yes, Save Anyway")
			# Translators: Cancel button label for guarded prompt save confirmation.
			no_label = _("No, Go Back")
			dlg.SetYesNoLabels(yes_label, no_label)
			return dlg.ShowModal() == wx.ID_YES
		finally:
			dlg.Destroy()

	def _save_current_default_editor(self):
		if self._default_selection == wx.NOT_FOUND or self._default_selection >= len(self.default_items):
			return True

		prompt_text = self.default_prompt_ctrl.GetValue()
		if not prompt_text.strip():
			msg = _("Prompt text cannot be empty.")
			title = _("Validation Error")
			wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			self.default_prompt_ctrl.SetFocus()
			return False

		current_item = self.default_items[self._default_selection]
		if prompt_text == current_item.get("prompt", ""):
			return True

		if self._is_guarded_prompt(current_item):
			if not self._validate_guarded_prompt(current_item, prompt_text):
				return False
			if not self._confirm_guarded_save(current_item):
				self.default_prompt_ctrl.SetFocus()
				return False

		self.default_items[self._default_selection]["prompt"] = prompt_text
		return True

	def on_default_selected(self, event):
		if not self._save_current_default_editor():
			self._select_default_item(self._default_selection)
			return

		position = self.default_list.GetSelection()
		if position == wx.NOT_FOUND or position >= len(self._default_view):
			return

		self._default_selection = self._default_view[position]
		self.default_prompt_ctrl.SetValue(self.default_items[self._default_selection]["prompt"])

	def on_save_selected_default(self, event):
		if self._save_current_default_editor():
			# Translators: Message shown after applying changes to the selected default prompt.
			ui.message(_("Selected prompt updated."))

	def on_reset_selected_default(self, event):
		idx = self._default_selection
		if idx == wx.NOT_FOUND or idx >= len(self.default_items):
			return
		self.default_items[idx]["prompt"] = self.default_items[idx]["default"]
		self.default_prompt_ctrl.SetValue(self.default_items[idx]["prompt"])

	def on_reset_all_defaults(self, event):
		if not self.default_items:
			return
		# Translators: Confirmation text before resetting all default prompts.
		msg = _("Reset all default prompts to built-in values?")
		# Translators: Title of confirmation dialog.
		title = _("Confirm Reset")
		if wx.MessageBox(msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) != wx.YES:
			return
		for item in self.default_items:
			item["prompt"] = item["default"]
		idx = self._default_selection
		if idx != wx.NOT_FOUND and idx < len(self.default_items):
			self.default_prompt_ctrl.SetValue(self.default_items[idx]["prompt"])
		else:
			self.default_prompt_ctrl.SetValue("")

	def _custom_display_name(self, item):
		hotkey = _format_hotkey_display(_normalize_hotkey(item.get("hotkey")))
		if hotkey:
			return "%s (%s)" % (item["name"], hotkey)
		return item["name"]

	def _refresh_custom_list(self, selection=None):
		self.custom_list.Set([self._custom_display_name(item) for item in self.custom_items])
		if not self.custom_items:
			self.custom_preview.SetValue("")
			self._update_custom_buttons()
			return

		if selection is None:
			selection = self.custom_list.GetSelection()
			if selection == wx.NOT_FOUND:
				selection = 0

		selection = max(0, min(selection, len(self.custom_items) - 1))
		self.custom_list.SetSelection(selection)
		self.custom_preview.SetValue(self.custom_items[selection]["content"])
		self._update_custom_buttons()

	def _update_custom_buttons(self):
		idx = self.custom_list.GetSelection()
		has_selection = idx != wx.NOT_FOUND and idx < len(self.custom_items)
		self.edit_custom_btn.Enable(has_selection)
		self.remove_custom_btn.Enable(has_selection)
		self.move_up_btn.Enable(has_selection and idx > 0)
		self.move_down_btn.Enable(has_selection and idx < len(self.custom_items) - 1)

	def _name_exists(self, name, skip_index=None):
		wanted = name.strip().lower()
		for idx, item in enumerate(self.custom_items):
			if skip_index is not None and idx == skip_index:
				continue
			if item["name"].strip().lower() == wanted:
				return True
		return False

	@staticmethod
	def _effective_normal_gesture(hotkey):
		hotkey = _normalize_hotkey(hotkey)
		if not hotkey:
			return ""
		if "+" in hotkey:
			return hotkey
		return "nvda+shift+" + hotkey

	def _hotkey_exists(self, hotkey, skip_index=None):
		wanted = self._effective_normal_gesture(hotkey)
		if not wanted:
			return False
		for idx, item in enumerate(self.custom_items):
			if skip_index is not None and idx == skip_index:
				continue
			if self._effective_normal_gesture(item.get("hotkey")) == wanted:
				return True
		return False

	def on_custom_selected(self, event):
		idx = self.custom_list.GetSelection()
		if idx == wx.NOT_FOUND or idx >= len(self.custom_items):
			self.custom_preview.SetValue("")
		else:
			self.custom_preview.SetValue(self.custom_items[idx]["content"])
		self._update_custom_buttons()

	def on_add_custom(self, event):
		# Translators: Title of dialog for adding a custom prompt.
		dlg = PromptItemDialog(self, _("Add Custom Prompt"), variables_guide=self.variables_guide)
		if dlg.ShowModal() == wx.ID_OK:
			item = dlg.get_item()
			if self._name_exists(item["name"]):
				# Translators: Validation error for duplicate custom prompt name.
				msg = _("A custom prompt with this name already exists.")
				title = _("Validation Error")
				wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			elif self._hotkey_exists(item.get("hotkey", "")):
				# Translators: Validation error when another custom prompt already uses the chosen shortcut key.
				msg = _("Another custom prompt already uses this shortcut key.")
				title = _("Validation Error")
				wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			else:
				self.custom_items.append(item)
				self._refresh_custom_list(selection=len(self.custom_items) - 1)
		dlg.Destroy()

	def on_edit_custom(self, event):
		idx = self.custom_list.GetSelection()
		if idx == wx.NOT_FOUND or idx >= len(self.custom_items):
			return

		current = self.custom_items[idx]
		# Translators: Title of dialog for editing a custom prompt.
		dlg = PromptItemDialog(
			self,
			# Translators: Title of the dialog for editing an existing custom prompt.
			_("Edit Custom Prompt"),
			current["name"],
			current["content"],
			current.get("hotkey", ""),
			variables_guide=self.variables_guide,
			feedback_behavior=current.get("feedback_behavior", "global"),
		)
		if dlg.ShowModal() == wx.ID_OK:
			item = dlg.get_item()
			if self._name_exists(item["name"], skip_index=idx):
				msg = _("A custom prompt with this name already exists.")
				title = _("Validation Error")
				wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			elif self._hotkey_exists(item.get("hotkey", ""), skip_index=idx):
				# Translators: Validation error when another custom prompt already uses the chosen shortcut key.
				msg = _("Another custom prompt already uses this shortcut key.")
				title = _("Validation Error")
				wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
			else:
				self.custom_items[idx] = item
				self._refresh_custom_list(selection=idx)
		dlg.Destroy()

	def on_remove_custom(self, event):
		idx = self.custom_list.GetSelection()
		if idx == wx.NOT_FOUND or idx >= len(self.custom_items):
			return
		name = self.custom_items[idx].get("name", "")
		# Translators: Confirmation text before deleting a custom prompt.
		msg = _("Remove custom prompt '{name}'?").format(name=name)
		# Translators: Title of confirmation dialog before deleting a custom prompt.
		title = _("Confirm Remove")
		if wx.MessageBox(msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) != wx.YES:
			return
		del self.custom_items[idx]
		self._refresh_custom_list(selection=idx)

	def on_move_custom_up(self, event):
		idx = self.custom_list.GetSelection()
		if idx <= 0 or idx >= len(self.custom_items):
			return
		self.custom_items[idx - 1], self.custom_items[idx] = (
			self.custom_items[idx],
			self.custom_items[idx - 1],
		)
		self._refresh_custom_list(selection=idx - 1)

	def on_move_custom_down(self, event):
		idx = self.custom_list.GetSelection()
		if idx == wx.NOT_FOUND or idx >= len(self.custom_items) - 1:
			return
		self.custom_items[idx], self.custom_items[idx + 1] = (
			self.custom_items[idx + 1],
			self.custom_items[idx],
		)
		self._refresh_custom_list(selection=idx + 1)

	def on_open_variables(self, event):
		dlg = PromptVariablesGuideDialog(self, self.variables_guide)
		dlg.ShowModal()
		dlg.Destroy()

	def on_ok(self, event):
		if not self._save_current_default_editor():
			return
		self.EndModal(wx.ID_OK)

	def get_default_items(self):
		return [dict(item) for item in self.default_items]

	def get_custom_items(self):
		return [dict(item) for item in self.custom_items]
