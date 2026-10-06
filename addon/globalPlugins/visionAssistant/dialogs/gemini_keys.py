# -*- coding: utf-8 -*-
import logging
import threading

import wx
import addonHandler
import api
import gui
import ui

from .. import plugin_state
from ..features import gemini_keys
from ..utils.system import show_error_dialog
from ..vision_config import ADDON_NAME

addonHandler.initTranslation()

log = logging.getLogger(__name__)


def gemini_manager_message():
	return _(
		# Translators: Error shown when the Gemini API key manager is used while another provider is selected, {name} is the name of the add-on.
		"The Gemini API key manager only works with the Google Gemini provider. Change the provider in the {name} settings first."
	).format(name=ADDON_NAME)


class GeminiKeysDialog(wx.Dialog):
	def __init__(self, parent):
		# Translators: Title of the dialog that creates and manages Gemini API keys with the user's Google account, {name} is the name of the add-on.
		dlg_title = _("{name} - Gemini API Key Manager").format(name=ADDON_NAME)
		super().__init__(
			parent,
			title=dlg_title,
			size=(700, 580),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		self._alive = True
		self._busy = False
		self._project_ids = []
		self._key_strings = []
		self._key_records = []
		self._last_key = ""
		self._last_key_project = ""
		self._cancel_event = threading.Event()
		signed_in = gemini_keys.is_signed_in()
		email = gemini_keys.get_account_email() if signed_in else ""
		key_map = gemini_keys.stored_keys_by_project()
		key_map_list = gemini_keys.stored_keys_list_by_project()
		self._state = {
			"loaded": False,
			"signed_in": signed_in,
			"email": email,
			"projects": [],
			"key_map": key_map,
			"key_map_list": key_map_list,
		}
		self._init_ui()
		self._apply_state()
		self._run_task(lambda token_id: self._worker_load(announce=True), can_cancel=False)

	def _init_ui(self):
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		content_panel = wx.Panel(self)
		self.content_panel = content_panel

		# Translators: Title of the account section in the Gemini API keys dialog.
		account_box = wx.StaticBox(content_panel, label=_("Google Account"))
		account_sizer = wx.StaticBoxSizer(account_box, wx.VERTICAL)

		account_row = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button that starts the Google sign-in process and opens the browser.
		self.sign_in_btn = wx.Button(account_box, label=_("&Sign In and Open Browser..."))
		self.sign_in_btn.Bind(wx.EVT_BUTTON, self._on_sign_in)
		# Translators: Button that signs out of the Google account used for creating API keys.
		self.sign_out_btn = wx.Button(account_box, label=_("Sign &Out"))
		self.sign_out_btn.Bind(wx.EVT_BUTTON, self._on_sign_out)
		# Translators: Button that cancels the currently running operation.
		self.cancel_btn = wx.Button(account_box, label=_("&Cancel Operation"))
		self.cancel_btn.Bind(wx.EVT_BUTTON, self._on_cancel_operation)
		for button in (self.sign_in_btn, self.sign_out_btn, self.cancel_btn):
			account_row.Add(button, 0, wx.RIGHT, 5)
		account_sizer.Add(account_row, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
		main_sizer.Add(account_sizer, 0, wx.ALL | wx.EXPAND, 8)

		# Translators: Title of the box grouping Google Cloud project controls.
		projects_box = wx.StaticBox(content_panel, label=_("Projects"))
		projects_sizer = wx.StaticBoxSizer(projects_box, wx.VERTICAL)
		# Translators: Label showing how many Google Cloud projects were loaded and how many have a saved key.
		self.projects_label = wx.StaticText(projects_box, label=_("Projects: not loaded"))
		projects_sizer.Add(self.projects_label, 0, wx.ALL | wx.EXPAND, 5)

		self.projects_list = wx.ListBox(projects_box, style=wx.LB_SINGLE, size=(-1, 140))
		# Translators: Accessible name for the list of Google Cloud projects.
		self.projects_list.SetName(_("Projects"))
		self.projects_list.Bind(wx.EVT_LISTBOX, self._on_project_selected)
		self.projects_list.Bind(wx.EVT_LISTBOX_DCLICK, self._on_create_key)
		projects_sizer.Add(self.projects_list, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)

		projects_row = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button that reloads the list of Google Cloud projects.
		self.refresh_btn = wx.Button(projects_box, label=_("&Refresh Projects"))
		self.refresh_btn.Bind(wx.EVT_BUTTON, self._on_refresh_projects)
		# Translators: Button that creates a new Google Cloud project together with a Gemini API key.
		self.new_project_btn = wx.Button(projects_box, label=_("&New Project and Key"))
		self.new_project_btn.Bind(wx.EVT_BUTTON, self._on_create_project)
		# Translators: Button that creates a Gemini API key on the selected project.
		self.create_key_btn = wx.Button(projects_box, label=_("Create &Key for Selected Project"))
		self.create_key_btn.Bind(wx.EVT_BUTTON, self._on_create_key)
		for button in (self.refresh_btn, self.new_project_btn, self.create_key_btn):
			projects_row.Add(button, 0, wx.RIGHT, 5)
		projects_sizer.Add(projects_row, 0, wx.ALL, 5)
		main_sizer.Add(projects_sizer, 1, wx.ALL | wx.EXPAND, 8)

		# Translators: Title of the box grouping API key controls.
		keys_box = wx.StaticBox(content_panel, label=_("API Keys"))
		keys_sizer = wx.StaticBoxSizer(keys_box, wx.VERTICAL)

		# Translators: Label above the list of API keys for the selected Google Cloud project.
		self.keys_label = wx.StaticText(keys_box, label=_("API Keys:"))
		keys_sizer.Add(self.keys_label, 0, wx.ALL | wx.EXPAND, 5)

		self.keys_list = wx.ListBox(keys_box, style=wx.LB_SINGLE, size=(-1, 110))
		# Translators: Accessible name for the list of API keys.
		self.keys_list.SetName(_("API Keys"))
		self.keys_list.Bind(wx.EVT_LISTBOX, self._on_key_selected)
		self.keys_list.Bind(wx.EVT_LISTBOX_DCLICK, self._on_copy_selected)
		keys_sizer.Add(self.keys_list, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 5)

		key_row = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button that copies the selected API key to the clipboard.
		self.copy_selected_btn = wx.Button(keys_box, label=_("&Copy Selected Key"))
		self.copy_selected_btn.Bind(wx.EVT_BUTTON, self._on_copy_selected)
		# Translators: Button that copies the most recently created API key to the clipboard.
		self.copy_last_btn = wx.Button(keys_box, label=_("Copy &Last Created Key"))
		self.copy_last_btn.Bind(wx.EVT_BUTTON, self._on_copy_last)
		# Translators: Button that adds the available API key to the add-on's own key list.
		self.use_btn = wx.Button(keys_box, label=_("&Use in {name}").format(name=ADDON_NAME))
		self.use_btn.Bind(wx.EVT_BUTTON, self._on_use_key)
		for button in (self.copy_selected_btn, self.copy_last_btn, self.use_btn):
			key_row.Add(button, 0, wx.RIGHT, 5)
		keys_sizer.Add(key_row, 0, wx.ALL, 5)

		# Translators: Button that deletes the selected API key.
		self.delete_key_btn = wx.Button(keys_box, label=_("&Delete Key"))
		self.delete_key_btn.Bind(wx.EVT_BUTTON, self._on_delete_key)
		# Translators: Button that exports saved API keys to a file.
		self.export_btn = wx.Button(keys_box, label=_("&Export Saved Keys..."))
		self.export_btn.Bind(wx.EVT_BUTTON, self._on_export)
		buttons_row = wx.BoxSizer(wx.HORIZONTAL)
		buttons_row.Add(self.delete_key_btn, 0, wx.RIGHT, 5)
		buttons_row.Add(self.export_btn, 0, wx.RIGHT, 5)
		keys_sizer.Add(buttons_row, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
		main_sizer.Add(keys_sizer, 1, wx.ALL | wx.EXPAND, 8)

		close_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button that closes the Gemini API keys dialog.
		self.close_btn = wx.Button(content_panel, wx.ID_CANCEL, label=_("Close"))
		self.close_btn.SetDefault()
		close_sizer.Add(self.close_btn, 0)
		main_sizer.Add(close_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 8)

		content_panel.SetSizer(main_sizer)
		root_sizer = wx.BoxSizer(wx.VERTICAL)
		root_sizer.Add(content_panel, 1, wx.EXPAND)
		self.SetSizer(root_sizer)
		self.Bind(wx.EVT_INIT_DIALOG, self._on_init_dialog)
		self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)
		self.Bind(wx.EVT_CLOSE, self._on_close)

	def _on_init_dialog(self, event):
		if self._state.get("signed_in"):
			self.projects_list.SetFocus()
		else:
			self.sign_in_btn.SetFocus()

	def _show_content(self, show=True):
		pass

	def _all_buttons(self):
		return (
			self.sign_in_btn,
			self.sign_out_btn,
			self.refresh_btn,
			self.new_project_btn,
			self.create_key_btn,
			self.copy_selected_btn,
			self.copy_last_btn,
			self.use_btn,
			self.delete_key_btn,
			self.export_btn,
		)

	def _on_char_hook(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
			return
		event.Skip()

	def _on_close(self, event):
		self._alive = False
		self._cancel_event.set()
		if self.IsModal():
			self.EndModal(wx.ID_CANCEL)
		else:
			self.Destroy()

	def _call(self, func, *args):
		if not self._alive:
			return
		wx.CallAfter(self._invoke, func, args)

	def _invoke(self, func, args):
		if not self._alive:
			return
		try:
			func(*args)
		except Exception as e:
			log.debug(f"Gemini keys dialog callback failed: {e}")

	def _progress(self, message):
		plugin_state.speak_status(message)

	def _set_busy(self, busy, focus_cancel=False, can_cancel=True):
		self._busy = busy
		if busy:
			self.cancel_btn.Enable(can_cancel)
			if focus_cancel and can_cancel:
				self.cancel_btn.SetFocus()
			for control in self._all_buttons():
				control.Enable(False)
			return
		self.cancel_btn.Enable(False)
		self._cancel_event.clear()
		self._apply_state()

	def _run_task(self, worker, focus_cancel=False, can_cancel=True):
		if self._busy:
			# Translators: Message shown when the user starts a new operation while another one is still running.
			ui.message(_("Please wait for the current operation to finish."))
			return
		self._cancel_event.clear()
		self._set_busy(True, focus_cancel=focus_cancel, can_cancel=can_cancel)

		def runner():
			try:
				worker(0)
			except Exception as error:
				log.debug(f"Gemini key operation failed: {error}")
				self._call(self._task_error, str(error))
			finally:
				self._call(self._set_busy, False)

		threading.Thread(target=runner, daemon=True).start()

	def _task_error(self, message):
		log.debug(f"Gemini keys dialog error: {message}")
		self._state["loaded"] = True
		self._apply_state()
		self._show_content(True)
		show_error_dialog(message)

	def _confirm(self, message, title):
		gui.mainFrame.prePopup()
		try:
			return gui.messageBox(message, title, wx.YES_NO | wx.ICON_QUESTION) == wx.YES
		finally:
			gui.mainFrame.postPopup()

	def _selected_project_id(self):
		index = self.projects_list.GetSelection()
		if index < 0 or index >= len(self._project_ids):
			return ""
		return self._project_ids[index]

	def _stored_key_for_selected(self):
		sel = self.keys_list.GetSelection()
		if 0 <= sel < len(self._key_strings):
			return self._key_strings[sel]
		if self._key_strings:
			return self._key_strings[0]
		project_id = self._selected_project_id()
		if not project_id:
			return ""
		if self._last_key and self._last_key_project == project_id:
			return self._last_key
		record = self._state.get("key_map", {}).get(project_id)
		return record[1] if record else ""

	def _project_label(self, project):
		project_id = project.get("projectId", "?")
		name = project.get("name") or project.get("displayName") or ""
		label = "%s (%s)" % (name, project_id) if name else project_id
		state = project.get("lifecycleState", "")
		if state and state != "ACTIVE":
			label += " - " + state
		keys = self._state.get("key_map_list", {}).get(project_id, [])
		count = len(keys)
		if count == 1:
			# Translators: Suffix added to a project in the list when it has exactly 1 saved API key.
			label += " - " + _("1 key")
		elif count > 1:
			# Translators: Suffix added to a project in the list when it has multiple saved API keys, {count} is the key count.
			label += " - " + _("{count} keys").format(count=count)
		else:
			# Translators: Suffix added to a project in the list when it has no saved API keys.
			label += " - " + _("no keys")
		return label

	def _apply_state(self):
		loaded = self._state["loaded"]
		signed_in = self._state["signed_in"]
		email = self._state["email"]
		projects = self._state["projects"]
		key_map = self._state["key_map"]

		if signed_in and email:
			# Translators: Label of the button that signs out, showing the account that is currently signed in, {account} is the account email address.
			self.sign_out_btn.SetLabel(_("Sign &Out ({account})").format(account=email))
		else:
			# Translators: Button that signs out of the Google account used for creating API keys.
			self.sign_out_btn.SetLabel(_("Sign &Out"))

		if not loaded:
			# Translators: Label above the project list while the projects are being loaded.
			self.projects_label.SetLabel(_("Projects: checking..."))
		elif projects:
			saved = sum(1 for project in projects if project.get("projectId") in key_map)
			# Translators: Label above the project list showing how many projects were loaded and how many have keys, {total} and {saved} are numbers.
			proj_status = _("Projects: {total} ({saved} with keys)").format(total=len(projects), saved=saved)
			self.projects_label.SetLabel(proj_status)
		elif signed_in:
			# Translators: Label above the project list when the account has no Google Cloud projects.
			self.projects_label.SetLabel(_("Projects: none"))
		else:
			# Translators: Label above the project list before the projects are loaded.
			self.projects_label.SetLabel(_("Projects: not loaded"))
		self.projects_list.SetName(self.projects_label.GetLabel())

		selection = self.projects_list.GetSelection()
		self.projects_list.Clear()
		self._project_ids = []
		for project in projects:
			self.projects_list.Append(self._project_label(project))
			self._project_ids.append(project.get("projectId", "?"))
		if 0 <= selection < len(projects):
			self.projects_list.SetSelection(selection)

		self._update_keys_list()
		self._update_buttons()

	def _update_keys_list(self):
		project_id = self._selected_project_id()
		keys = self._state.get("key_map_list", {}).get(project_id, []) if project_id else []
		self._key_strings = []
		self._key_records = []
		self.keys_list.Clear()

		if not project_id:
			# Translators: Label above the API keys list when no project is selected.
			self.keys_label.SetLabel(_("API Keys: no project selected"))
		elif not keys:
			# Translators: Label above the API keys list when the selected project has no saved keys.
			self.keys_label.SetLabel(_("API Keys: none"))
		elif len(keys) == 1:
			# Translators: Label above the API keys list when the selected project has 1 key.
			self.keys_label.SetLabel(_("API Keys (1 key):"))
		else:
			# Translators: Label above the API keys list when the selected project has multiple keys, {count} is the key count.
			self.keys_label.SetLabel(_("API Keys ({count} keys):").format(count=len(keys)))
		self.keys_list.SetName(self.keys_label.GetLabel())

		for label, key_str in keys:
			masked = (key_str[:8] + "..." + key_str[-4:]) if len(key_str) >= 16 else key_str
			item_text = f"{label} ({masked})" if label else masked
			self.keys_list.Append(item_text)
			self._key_strings.append(key_str)
			self._key_records.append((label, key_str))

		if keys:
			self.keys_list.SetSelection(0)

	def _update_buttons(self):
		loaded = self._state["loaded"]
		signed_in = self._state["signed_in"]
		has_selection = bool(self._selected_project_id())
		has_selected_key = bool(self._stored_key_for_selected())
		has_last_key = bool(self._last_key)
		has_records = bool(self._state["key_map"])

		self.sign_in_btn.Enable(loaded and not signed_in)
		self.sign_out_btn.Enable(loaded and signed_in)
		self.refresh_btn.Enable(loaded and signed_in)
		self.new_project_btn.Enable(signed_in)
		self.create_key_btn.Enable(signed_in and has_selection)
		self.copy_selected_btn.Enable(has_selected_key)
		self.copy_last_btn.Enable(has_last_key)
		self.use_btn.Enable(has_selected_key or has_last_key)
		self.delete_key_btn.Enable(signed_in and has_selected_key)
		self.export_btn.Enable(has_records)

	def _select_project(self, project_id):
		if project_id in self._project_ids:
			index = self._project_ids.index(project_id)
			self.projects_list.SetSelection(index)
			self._update_keys_list()
			self._update_buttons()

	def _on_project_selected(self, event):
		self._update_keys_list()
		self._update_buttons()

	def _on_key_selected(self, event):
		self._update_buttons()

	def _worker_load(self, announce=False):
		signed_in = gemini_keys.is_signed_in()
		email = gemini_keys.get_account_email() if signed_in else ""
		projects = []
		if signed_in:
			token = gemini_keys.get_access_token()
			projects = gemini_keys.list_projects(token, cancel_check=self._cancel_event.is_set)
			try:
				gemini_keys.sync_cloud_keys(token, projects, cancel_check=self._cancel_event.is_set)
			except Exception as e:
				log.debug(f"Could not sync cloud keys: {e}")
		key_map = gemini_keys.stored_keys_by_project()
		key_map_list = gemini_keys.stored_keys_list_by_project()
		self._call(self._apply_load, signed_in, email, projects, key_map, key_map_list, announce)

	def _apply_load(self, signed_in, email, projects, key_map, key_map_list, announce):
		self._state["loaded"] = True
		self._state["signed_in"] = signed_in
		self._state["email"] = email
		self._state["projects"] = projects
		self._state["key_map"] = key_map
		self._state["key_map_list"] = key_map_list
		self._apply_state()
		log.debug(f"Loaded {len(projects)} project(s).")
		if projects:
			if self.FindFocus() != self.projects_list:
				self.projects_list.SetFocus()
		elif signed_in:
			if self.FindFocus() != self.new_project_btn:
				self.new_project_btn.SetFocus()
		else:
			if self.FindFocus() != self.sign_in_btn:
				self.sign_in_btn.SetFocus()
		if not announce:
			return
		if not signed_in:
			# Translators: Spoken message shown when no Google account is signed in.
			ui.message(_("Not signed in. Press Sign In and Open Browser."))
		elif projects:
			saved = sum(1 for project in projects if project.get("projectId") in key_map)
			# Translators: Spoken summary shown after loading the projects, {count} is the project count and {saved} is how many have keys.
			found_msg = _("Found {count} project(s), {saved} with keys.").format(
				count=len(projects), saved=saved
			)
			ui.message(found_msg)
		else:
			# Translators: Spoken message shown when the signed-in account has no Google Cloud projects.
			ui.message(_("No projects found. Press New Project and Key to create one."))

	def _prompt_text(self, message, title, default=""):
		gui.mainFrame.prePopup()
		try:
			dlg = wx.TextEntryDialog(self, message, title, default)
			try:
				if dlg.ShowModal() == wx.ID_OK:
					return dlg.GetValue().strip()
				return None
			finally:
				dlg.Destroy()
		finally:
			gui.mainFrame.postPopup()

	def _on_cancel_operation(self, event):
		self._cancel_event.set()
		# Translators: Message shown when the user asks to cancel the running Gemini key operation.
		ui.message(_("Cancelling..."))

	def _on_refresh_projects(self, event):
		self._run_task(lambda token_id: self._worker_load(announce=True))

	def _on_sign_in(self, event):
		def worker(token_id):
			gemini_keys.sign_in(self._progress, cancel_check=self._cancel_event.is_set)
			self._worker_load(announce=True)

		self._run_task(worker)

	def _on_sign_out(self, event):
		# Translators: Title of the confirmation dialog shown before signing out of Google.
		title = _("Sign Out")
		# Translators: Confirmation message shown before removing the stored Google credentials.
		message = _("Remove the stored Google credentials used for creating API keys?")
		if not self._confirm(message, title):
			return

		def worker(token_id):
			removed = gemini_keys.sign_out(self._progress)
			still_signed_in = gemini_keys.is_signed_in()
			self._call(self._signed_out, removed, still_signed_in)

		self._run_task(worker)

	def _signed_out(self, removed, still_signed_in):
		log.debug(f"Sign out removed {len(removed)} credential file(s).")
		if still_signed_in:
			# Translators: Error message shown when the sign-out did not take effect.
			show_error_dialog(_("Sign out did not complete. Please try again."))
			return
		self._state["signed_in"] = False
		self._state["email"] = ""
		self._state["projects"] = []
		self._state["key_map"] = gemini_keys.stored_keys_by_project()
		self._state["key_map_list"] = gemini_keys.stored_keys_list_by_project()
		self._apply_state()
		# Translators: Spoken message confirming that the user signed out of Google.
		ui.message(_("Signed out."))

	def _on_create_key(self, event):
		project_id = self._selected_project_id()
		if not project_id:
			# Translators: Error message shown when no project is selected in the Gemini API keys dialog.
			show_error_dialog(_("Select a project first."))
			return
		# Translators: Prompt message asking for a name for the new API key.
		prompt_msg = _("Name for the new API key:")
		# Translators: Title of the dialog that asks for a name for the new API key.
		dlg_title = _("Create API Key")
		label = self._prompt_text(prompt_msg, dlg_title, "gemini-key")
		if label is None:
			return
		if not label:
			label = "gemini-key"

		def worker(token_id):
			token = gemini_keys.get_access_token()
			gemini_keys.enable_service(
				token, project_id, gemini_keys.APIKEYS_SERVICE, self._cancel_event.is_set, self._progress
			)
			key = gemini_keys.create_gemini_key(
				token, project_id, label, self._cancel_event.is_set, self._progress
			)
			gemini_keys.save_key_record(project_id, label, key)
			self._call(self._key_created, project_id, label, key)

		self._run_task(worker)

	def _on_create_project(self, event):
		# Translators: Prompt message asking for a name for the new Google Cloud project.
		prompt_msg = _("Name for the new project:")
		# Translators: Title of the dialog that asks for a name for the new Google Cloud project.
		dlg_title = _("Create Project and Key")
		name = self._prompt_text(prompt_msg, dlg_title, "Gemini")
		if name is None:
			return
		if not name:
			name = "Gemini"
		project_id = gemini_keys.make_project_id()

		def worker(token_id):
			token = gemini_keys.get_access_token()
			gemini_keys.create_project(token, project_id, name, self._cancel_event.is_set, self._progress)
			gemini_keys.enable_service(
				token, project_id, gemini_keys.GEMINI_SERVICE, self._cancel_event.is_set, self._progress
			)
			gemini_keys.enable_service(
				token, project_id, gemini_keys.APIKEYS_SERVICE, self._cancel_event.is_set, self._progress
			)
			key = gemini_keys.create_gemini_key(
				token, project_id, name, self._cancel_event.is_set, self._progress
			)
			gemini_keys.save_key_record(project_id, name, key)
			self._call(self._key_created, project_id, name, key)
			self._worker_load()

		self._run_task(worker)

	def _key_created(self, project_id, label, key):
		self._last_key = key
		self._last_key_project = project_id
		self._state["key_map"] = gemini_keys.stored_keys_by_project()
		self._state["key_map_list"] = gemini_keys.stored_keys_list_by_project()
		self._apply_state()
		self._select_project(project_id)
		log.debug(f"Created an API key named '{label}' on {project_id}.")
		if api.copyToClip(key):
			# Translators: Spoken message confirming that the new API key was created and copied to the clipboard.
			ui.message(_("API key created and copied to the clipboard."))
		else:
			# Translators: Spoken message confirming that the new API key was created.
			ui.message(_("API key created."))
		self._offer_add_to_settings(key)

	def _offer_add_to_settings(self, key):
		# Translators: Title of the dialog that asks whether to add the new API key to the add-on settings.
		title = _("API Key Created")
		# Translators: Confirmation message shown after creating an API key, asking whether to add it to the add-on's API key list.
		message = _("Add this key to the {name} settings so the add-on can use it?").format(name=ADDON_NAME)
		if not self._confirm(message, title):
			return
		added = gemini_keys.add_keys_to_addon([key])
		if added:
			# Translators: Spoken message confirming that the API key was added to the add-on's API key list.
			ui.message(_("The key was added to the {name} settings.").format(name=ADDON_NAME))
		else:
			# Translators: Spoken message shown when the API key is already present in the add-on's API key list.
			ui.message(_("This key is already in the {name} settings.").format(name=ADDON_NAME))

	def _on_delete_key(self, event):
		project_id = self._selected_project_id()
		if not project_id:
			# Translators: Error message shown when no project is selected in the Gemini API keys dialog.
			show_error_dialog(_("Select a project first."))
			return
		sel = self.keys_list.GetSelection()
		if sel < 0 or sel >= len(self._key_records):
			# Translators: Error message shown when no API key is selected before attempting deletion.
			show_error_dialog(_("Select an API key to delete first."))
			return

		label, key_str = self._key_records[sel]
		# Translators: Title of the confirmation dialog when deleting an API key.
		title = _("Delete API Key")
		display_name = label if label else (key_str[:8] + "..." + key_str[-4:] if len(key_str) >= 16 else key_str)
		# Translators: Confirmation message before deleting an API key, {name} is the key name and {project} is the project id.
		message = _("Delete the API key '{name}' on project {project}?\n\nThis cannot be undone.").format(
			name=display_name, project=project_id
		)
		if not self._confirm(message, title):
			return

		def worker(token_id):
			token = gemini_keys.get_access_token()
			try:
				keys = gemini_keys.list_keys(token, project_id, self._cancel_event.is_set)
			except Exception as error:
				log.debug(f"Reading keys failed on delete: {error}")
				keys = []

			target_key_name = None
			for k in keys:
				k_name = k.get("name", "")
				if label and k.get("displayName") == label:
					target_key_name = k_name
					break
				try:
					k_str = gemini_keys.get_key_string(token, k_name, project_id)
					if k_str == key_str:
						target_key_name = k_name
						break
				except Exception:
					pass

			if target_key_name:
				try:
					gemini_keys.delete_key(token, target_key_name, project_id, self._cancel_event.is_set)
				except Exception as error:
					log.debug(f"Cloud key deletion error: {error}")

			self._call(self._key_deleted, project_id, label, key_str)

		self._run_task(worker)

	def _key_deleted(self, project_id, label, key_str):
		if key_str:
			gemini_keys.remove_key_record(project_id, key_str)
			if self._last_key == key_str:
				self._last_key = ""
				self._last_key_project = ""
			if gemini_keys.remove_keys_from_addon([key_str]):
				# Translators: Spoken message shown when a deleted API key was also removed from the add-on's API key list, {name} is the add-on name.
				removed_msg = _("The key was also removed from the {name} settings.").format(name=ADDON_NAME)
				plugin_state.speak_status(removed_msg)
		self._state["key_map"] = gemini_keys.stored_keys_by_project()
		self._state["key_map_list"] = gemini_keys.stored_keys_list_by_project()
		self._apply_state()
		self._select_project(project_id)
		display_name = label if label else (key_str[:8] + "..." + key_str[-4:] if len(key_str) >= 16 else key_str)
		# Translators: Spoken message confirming that an API key was deleted, {name} is the key name.
		ui.message(_("The API key '{name}' was deleted.").format(name=display_name))

	def _on_copy_selected(self, event):
		key = self._stored_key_for_selected()
		if not key:
			return
		if api.copyToClip(key):
			# Translators: Spoken message confirming that the API key of the selected project was copied to the clipboard.
			ui.message(_("API key for the selected project copied to the clipboard."))
		else:
			# Translators: Error message shown when copying an API key to the clipboard fails.
			show_error_dialog(_("Could not copy the key to the clipboard."))

	def _on_copy_last(self, event):
		if not self._last_key:
			return
		if api.copyToClip(self._last_key):
			# Translators: Spoken message confirming that the last created API key was copied to the clipboard.
			ui.message(_("API key copied to the clipboard."))

	def _on_use_key(self, event):
		key = self._stored_key_for_selected() or self._last_key
		if not key:
			return
		added = gemini_keys.add_keys_to_addon([key])
		if added:
			# Translators: Spoken message confirming that the API key was added to the add-on's API key list.
			ui.message(_("The key was added to the {name} settings.").format(name=ADDON_NAME))
		else:
			# Translators: Spoken message shown when the API key is already present in the add-on's API key list.
			ui.message(_("This key is already in the {name} settings.").format(name=ADDON_NAME))

	def _on_export(self, event):
		records = gemini_keys.load_key_records()
		if not records:
			# Translators: Error message shown when trying to export keys but no keys are saved.
			show_error_dialog(_("There are no saved API keys to export."))
			return

		# Translators: Export option to export API keys with project names and key labels into a CSV file.
		OPT_CSV_FULL = _("CSV file (.csv) - Full with project names")
		# Translators: Export option to export only the API keys into a text file, one key per line.
		OPT_TXT_KEYS_ONLY = _("Text file (.txt) - Keys only (one per line)")

		choices = [OPT_CSV_FULL, OPT_TXT_KEYS_ONLY]
		gui.mainFrame.prePopup()
		try:
			dlg = wx.SingleChoiceDialog(
				self,
				# Translators: Message asking the user which export format they want to use for saved keys.
				_("Select the export format:"),
				# Translators: Dialog title for selecting the export format for Gemini API keys.
				_("Export Format"),
				choices,
			)
			dlg.Raise()
			if dlg.ShowModal() != wx.ID_OK:
				dlg.Destroy()
				return
			sel_idx = dlg.GetSelection()
			dlg.Destroy()
		finally:
			gui.mainFrame.postPopup()

		from datetime import datetime
		date_str = datetime.now().strftime("%Y%m%d")
		if sel_idx == 0:
			default_name = f"gemini_api_keys_{date_str}.csv"
			wildcard = "CSV files (*.csv)|*.csv"
			export_fn = lambda p: gemini_keys.export_keys_csv(target_path=p, keys_only=False)
			# Translators: Title of the save file dialog for exported Gemini API keys.
			save_title = _("Export Saved Keys to CSV")
		else:
			default_name = f"gemini_api_keys_only_{date_str}.txt"
			wildcard = "Text files (*.txt)|*.txt"
			export_fn = lambda p: gemini_keys.export_keys_txt(target_path=p, keys_only=True)
			# Translators: Title of the save file dialog for exported Gemini API keys as text file.
			save_title = _("Export Saved Keys to Text")

		gui.mainFrame.prePopup()
		try:
			with wx.FileDialog(
				self,
				save_title,
				defaultFile=default_name,
				wildcard=wildcard,
				style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
			) as file_dlg:
				if file_dlg.ShowModal() != wx.ID_OK:
					return
				path = file_dlg.GetPath()
		finally:
			gui.mainFrame.postPopup()

		try:
			saved_path = export_fn(path)
		except Exception as error:
			show_error_dialog(str(error))
			return
		log.debug(f"Exported saved keys to: {saved_path}")
		# Translators: Spoken message confirming that the API keys were exported.
		plugin_state.speak_status(_("Saved keys exported successfully."))

