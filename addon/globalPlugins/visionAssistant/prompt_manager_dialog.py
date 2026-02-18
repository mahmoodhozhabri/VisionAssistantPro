# -*- coding: utf-8 -*-
import re

import wx

import addonHandler
import ui

addonHandler.initTranslation()


class PromptItemDialog(wx.Dialog):
    def __init__(self, parent, title, name="", prompt_text="", variables_guide=None):
        super().__init__(parent, title=title, size=(620, 360), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.name_ctrl = None
        self.prompt_ctrl = None
        self.variables_guide = tuple(variables_guide or ())

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Translators: Label for prompt name input field.
        name_label = wx.StaticText(self, label=_("Name:"))
        main_sizer.Add(name_label, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self.name_ctrl = wx.TextCtrl(self, value=name)
        main_sizer.Add(self.name_ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

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
        if not prompt_text.strip():
            # Translators: Validation error for empty prompt text.
            msg = _("Prompt text cannot be empty.")
            # Translators: Title of validation warning dialog.
            title = _("Validation Error")
            wx.MessageBox(msg, title, wx.OK | wx.ICON_WARNING)
            self.prompt_ctrl.SetFocus()
            return
        event.Skip()

    def on_open_variables(self, event):
        dlg = PromptVariablesGuideDialog(self, self.variables_guide)
        dlg.ShowModal()
        dlg.Destroy()

    def get_item(self):
        return {
            "name": self.name_ctrl.GetValue().strip(),
            "content": self.prompt_ctrl.GetValue(),
        }


class PromptVariablesGuideDialog(wx.Dialog):
    def __init__(self, parent, variables_guide):
        # Translators: Title for the prompt variables help dialog.
        super().__init__(parent, title=_("Prompt Variables Guide"), size=(620, 420), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Translators: Intro text for the prompt variables help dialog.
        intro = wx.StaticText(self, label=_("Use these variables inside prompt text:"))
        main_sizer.Add(intro, 0, wx.ALL, 10)

        lines = []
        for token, description, input_type in variables_guide:
            lines.append(f"{token} - {description} ({input_type})")

        content = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP)
        content.SetValue("\n".join(lines))
        main_sizer.Add(content, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        close_btn = wx.Button(self, wx.ID_OK, label=_("Close"))
        close_btn.SetDefault()
        main_sizer.Add(close_btn, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(main_sizer)


class PromptManagerDialog(wx.Dialog):
    def __init__(self, parent, default_items, custom_items, variables_guide=None):
        # Translators: Title for the prompt manager dialog.
        super().__init__(parent, title=_("Prompt Manager"), size=(760, 560), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.default_items = [dict(item) for item in default_items]
        self.custom_items = [dict(item) for item in custom_items]
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
        # Translators: Button label to open the variables help dialog.
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
        # Translators: Label above the list of default prompt entries.
        default_list_label = wx.StaticText(self.default_panel, label=_("Default Prompts"))
        left_sizer.Add(default_list_label, 0, wx.BOTTOM, 5)
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
        # Translators: Label above the prompt editor textarea.
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

        if self.default_items:
            self.default_list.SetSelection(0)
            self._default_selection = 0
            self.default_prompt_ctrl.SetValue(self.default_items[0]["prompt"])
        else:
            self.default_prompt_ctrl.Disable()
            self.save_default_btn.Disable()
            self.reset_selected_btn.Disable()
            self.reset_all_btn.Disable()

    def _build_custom_tab(self):
        tab_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label above the list of custom prompts.
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
        self.custom_preview = wx.TextCtrl(self.custom_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP)
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
            _("This prompt is used by {feature}. To save it, add the required text below:").format(feature=feature),
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
        # Translators: Confirmation message shown before saving a guarded prompt.
        msg = _(
            "You are editing a prompt used by {feature}.\n\nIf this prompt is changed, this feature may not work correctly.\n\nDo you understand the risk and want to save anyway?"
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
            # Translators: Validation error for empty prompt text.
            msg = _("Prompt text cannot be empty.")
            # Translators: Title of validation warning dialog.
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
            self.default_list.SetSelection(self._default_selection)
            return

        new_selection = self.default_list.GetSelection()
        if new_selection == wx.NOT_FOUND or new_selection >= len(self.default_items):
            return

        self._default_selection = new_selection
        self.default_prompt_ctrl.SetValue(self.default_items[new_selection]["prompt"])

    def on_save_selected_default(self, event):
        if self._save_current_default_editor():
            # Translators: Message shown after applying changes to the selected default prompt.
            ui.message(_("Selected prompt updated."))

    def on_reset_selected_default(self, event):
        idx = self.default_list.GetSelection()
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
        idx = self.default_list.GetSelection()
        if idx != wx.NOT_FOUND and idx < len(self.default_items):
            self.default_prompt_ctrl.SetValue(self.default_items[idx]["prompt"])
        else:
            self.default_prompt_ctrl.SetValue("")

    def _refresh_custom_list(self, selection=None):
        self.custom_list.Set([item["name"] for item in self.custom_items])
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
                # Translators: Title of validation warning dialog.
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
            variables_guide=self.variables_guide,
        )
        if dlg.ShowModal() == wx.ID_OK:
            item = dlg.get_item()
            if self._name_exists(item["name"], skip_index=idx):
                # Translators: Validation error for duplicate custom prompt name.
                msg = _("A custom prompt with this name already exists.")
                # Translators: Title of validation warning dialog.
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
        # Translators: Title of confirmation dialog.
        title = _("Confirm Remove")
        if wx.MessageBox(msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) != wx.YES:
            return
        del self.custom_items[idx]
        self._refresh_custom_list(selection=idx)

    def on_move_custom_up(self, event):
        idx = self.custom_list.GetSelection()
        if idx <= 0 or idx >= len(self.custom_items):
            return
        self.custom_items[idx - 1], self.custom_items[idx] = self.custom_items[idx], self.custom_items[idx - 1]
        self._refresh_custom_list(selection=idx - 1)

    def on_move_custom_down(self, event):
        idx = self.custom_list.GetSelection()
        if idx == wx.NOT_FOUND or idx >= len(self.custom_items) - 1:
            return
        self.custom_items[idx], self.custom_items[idx + 1] = self.custom_items[idx + 1], self.custom_items[idx]
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
