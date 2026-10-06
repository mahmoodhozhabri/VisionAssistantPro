# -*- coding: utf-8 -*-
import threading
import logging
import wx

import addonHandler
import gui
import ui
import core
import api
import controlTypes

log = logging.getLogger(__name__)
addonHandler.initTranslation()

ADDON_NAME = addonHandler.getCodeAddon().manifest["summary"]

from ..utils.system import (
	_generate_object_signature,
)


class LabelManagerDialog(wx.Dialog):
	def __init__(self, parent, app_name, labels_dict):
		# Translators: Title of the Label Manager dialog.
		title_text = _("Label Manager - {app}").format(app=app_name)
		super().__init__(parent, title=title_text, size=(550, 700))
		self.app_name = app_name
		self.labels_dict = labels_dict
		self.action_type = None
		self.target_keys = []
		self.new_name = ""

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Instruction for managing labels using the list view.
		instruction_text = _("Check items to delete, or select one to rename:")
		instruction = wx.StaticText(self, label=instruction_text)
		main_sizer.Add(instruction, 0, wx.ALL, 10)

		self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
		self.list_ctrl.EnableCheckBoxes()

		# Translators: Header for the label name column in the manager list.
		self.list_ctrl.InsertColumn(0, _("Label Name"), width=300)
		# Translators: Header for the role column in the manager list.
		self.list_ctrl.InsertColumn(1, _("Role"), width=150)

		self.keys_list = list(labels_dict.keys())
		self.list_ctrl.Freeze()
		for i, k in enumerate(self.keys_list):
			try:
				role_id = int(k.split(":")[0])
				role_name = controlTypes.roleLabels.get(role_id, str(role_id))
			except Exception:
				role_name = "Unknown"
			self.list_ctrl.InsertItem(i, labels_dict[k])
			self.list_ctrl.SetItem(i, 1, role_name)
		self.list_ctrl.Thaw()

		main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

		selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button to check all items in the list.
		self.btn_select_all = wx.Button(self, label=_("Select &All"))
		self.btn_select_all.Bind(wx.EVT_BUTTON, self.on_select_all)
		# Translators: Button to uncheck all items in the list.
		self.btn_deselect_all = wx.Button(self, label=_("Deselect A&ll"))
		self.btn_deselect_all.Bind(wx.EVT_BUTTON, self.on_deselect_all)

		selection_sizer.Add(self.btn_select_all, 1, wx.RIGHT, 5)
		selection_sizer.Add(self.btn_deselect_all, 1, wx.LEFT, 5)
		main_sizer.Add(selection_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

		btn_grid = wx.GridSizer(2, 2, 5, 5)
		# Translators: Button to rename the currently focused label.
		self.btn_rename = wx.Button(self, label=_("&Rename"))
		self.btn_rename.Bind(wx.EVT_BUTTON, self.on_rename)
		# Translators: Button to delete all checked labels.
		self.btn_delete = wx.Button(self, label=_("&Delete Checked"))
		self.btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
		# Translators: Button to trigger a new full scan of the application.
		btn_rescan = wx.Button(self, label=_("Re&scan"))
		btn_rescan.Bind(wx.EVT_BUTTON, self.on_rescan)
		# Translators: Button to close the label manager.
		btn_close = wx.Button(self, wx.ID_CANCEL, label=_("&Close"))

		btn_grid.Add(self.btn_rename, 0, wx.EXPAND)
		btn_grid.Add(self.btn_delete, 0, wx.EXPAND)
		btn_grid.Add(btn_rescan, 0, wx.EXPAND)
		btn_grid.Add(btn_close, 0, wx.EXPAND)

		main_sizer.Add(btn_grid, 0, wx.EXPAND | wx.ALL, 10)
		self.SetSizer(main_sizer)

		self.list_ctrl.Bind(wx.EVT_LIST_ITEM_CHECKED, self.update_ui)
		self.list_ctrl.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.update_ui)
		self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.update_ui)
		self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.update_ui)
		self.list_ctrl.Bind(wx.EVT_CHAR_HOOK, self.on_key_event)

		self.update_ui()
		self.list_ctrl.SetFocus()

	def on_key_event(self, event):
		if event.ControlDown() and event.GetKeyCode() == ord("A"):
			self.on_select_all(None)
		else:
			event.Skip()

	def update_ui(self, event=None):
		count = self.list_ctrl.GetItemCount()
		checked_count = sum(1 for i in range(count) if self.list_ctrl.IsItemChecked(i))
		selected_idx = self.list_ctrl.GetFirstSelected()
		can_rename = (checked_count == 1) or (checked_count == 0 and selected_idx != -1)
		self.btn_rename.Enable(can_rename)
		self.btn_delete.Enable(checked_count > 0 or selected_idx != -1)

	def on_select_all(self, event):
		self.list_ctrl.Freeze()
		for i in range(self.list_ctrl.GetItemCount()):
			self.list_ctrl.CheckItem(i, True)
		self.list_ctrl.Thaw()
		self.update_ui()

	def on_deselect_all(self, event):
		self.list_ctrl.Freeze()
		for i in range(self.list_ctrl.GetItemCount()):
			self.list_ctrl.CheckItem(i, False)
		self.list_ctrl.Thaw()
		self.update_ui()

	def on_rename(self, event):
		idx = -1
		for i in range(self.list_ctrl.GetItemCount()):
			if self.list_ctrl.IsItemChecked(i):
				idx = i
				break
		if idx == -1:
			idx = self.list_ctrl.GetFirstSelected()
		if idx == -1:
			# Translators: Error message shown when no item is selected for renaming.
			ui.message(_("Please select an item from the list to rename."))
			return

		key = self.keys_list[idx]
		current_name = self.labels_dict[key]
		# Translators: Prompt message for entering a new label name.
		rename_prompt = _("Enter new name:")
		# Translators: Window title for the rename dialog.
		rename_title = _("Rename Label")

		with wx.TextEntryDialog(self, rename_prompt, rename_title, value=current_name) as dlg:
			if dlg.ShowModal() == wx.ID_OK:
				self.action_type = "rename"
				self.target_keys = [key]
				self.new_name = dlg.GetValue()
				self.EndModal(wx.ID_OK)

	def on_delete(self, event):
		self.target_keys = [
			self.keys_list[i] for i in range(self.list_ctrl.GetItemCount()) if self.list_ctrl.IsItemChecked(i)
		]
		if not self.target_keys:
			idx = self.list_ctrl.GetFirstSelected()
			if idx != -1:
				self.target_keys = [self.keys_list[idx]]
		if not self.target_keys:
			# Translators: Error message shown when no items are checked for deletion.
			ui.message(_("Please check at least one item to delete."))
			return
		self.action_type = "delete"
		self.EndModal(wx.ID_OK)

	def on_rescan(self, event):
		self.action_type = "rescan"
		self.EndModal(wx.ID_OK)


class UIExplorerDialog(wx.Dialog):
	def __init__(self, parent, choices, valid_elements, sw, sh, plugin_instance):
		# Translators: Instruction for the elements list dialog
		super(UIExplorerDialog, self).__init__(parent, title=_("UI Elements Explorer"))
		self.choices = choices
		self.valid_elements = valid_elements
		self.sw = sw
		self.sh = sh
		self.plugin = plugin_instance
		self.action_taken = False

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Instruction for the elements list dialog
		label = wx.StaticText(self, label=_("Select an element:"))
		mainSizer.Add(label, 0, wx.ALL, 5)

		self.listBox = wx.ListBox(self, choices=choices)
		self.listBox.SetSelection(0)
		mainSizer.Add(self.listBox, 1, wx.EXPAND | wx.ALL, 5)

		btnSizer = wx.BoxSizer(wx.HORIZONTAL)

		# Translators: Button to click the selected element
		self.btnClick = wx.Button(self, label=_("&Click"))
		self.btnClick.SetDefault()
		self.btnClick.Bind(wx.EVT_BUTTON, self.on_click)
		btnSizer.Add(self.btnClick, 0, wx.ALL, 5)

		# Translators: Button to add a label for the selected element
		self.btnAddLabel = wx.Button(self, label=_("&Add Label"))
		self.btnAddLabel.Bind(wx.EVT_BUTTON, self.on_add_label)
		btnSizer.Add(self.btnAddLabel, 0, wx.ALL, 5)

		self.btnCancel = wx.Button(self, id=wx.ID_CANCEL, label=_("Cancel"))
		btnSizer.Add(self.btnCancel, 0, wx.ALL, 5)

		mainSizer.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

		self.SetSizerAndFit(mainSizer)
		self.CenterOnParent()

	def on_click(self, evt):
		idx = self.listBox.GetSelection()
		if idx != wx.NOT_FOUND:
			target = self.valid_elements[idx]
			x, y = int(target["x"] * self.sw / 1000), int(target["y"] * self.sh / 1000)
			self.action_taken = True
			self.Close()
			gui.mainFrame.postPopup()
			self.plugin._do_mouse_action(x, y, "click")
			wx.CallLater(
				2000,
				lambda: threading.Thread(target=self.plugin._thread_ui_explorer, daemon=True).start(),
			)

	def on_add_label(self, evt):
		idx = self.listBox.GetSelection()
		if idx != wx.NOT_FOUND:
			target = self.valid_elements[idx]
			x, y = int(target["x"] * self.sw / 1000), int(target["y"] * self.sh / 1000)
			lbl = target.get("label", "").strip()

			old_pos = self.GetPosition()
			self.SetPosition((-10000, -10000))

			def do_label():
				obj = api.getDesktopObject().objectFromPoint(x, y)
				if not obj or not obj.location:
					# Translators: Error message shown when a screen object cannot be located.
					ui.message(_("Could not find object at coordinates."))
				else:
					uniqueId = self.plugin._getAppId(obj)
					if uniqueId in ["chrome", "msedge", "firefox", "opera", "brave"]:
						ui.message(_("AI Labeling is currently not supported in web browsers."))
					else:
						sig_key = _generate_object_signature(obj)
						if not sig_key:
							# Translators: Error message shown when a unique signature cannot be created for a screen object.
							ui.message(_("Could not generate signature for this object."))
						else:
							if uniqueId not in self.plugin.labels_cache:
								self.plugin.labels_cache[uniqueId] = {}
							self.plugin.labels_cache[uniqueId][sig_key] = lbl
							self.plugin._save_all_labels()
							# Translators: Success message when a label is added to a UI element.
							ui.message(_("Label added successfully: {name}").format(name=lbl))

				wx.CallAfter(self.SetPosition, old_pos)
				wx.CallAfter(self.listBox.SetFocus)

			core.callLater(50, do_label)
