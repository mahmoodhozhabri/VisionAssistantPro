# -*- coding: utf-8 -*-
import datetime
import logging

import wx
import addonHandler
import config as nvda_config
import gui
import ui

from ..vision_config import ADDON_NAME

addonHandler.initTranslation()

log = logging.getLogger(__name__)

_FILTERS = (
	("all", "All"),
	("chat", "Chats"),
	("document", "Documents"),
)


def _format_item(item):
	ts = item.get("timestamp") or 0
	when = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
	title = item.get("title") or ""
	subtitle = item.get("subtitle") or ""
	if subtitle:
		return "{0} - {1} ({2})".format(title, subtitle, when)
	return "{0} ({1})".format(title, when)


def _confirm_dialog(msg, title, parent=None):
	if parent:
		return gui.messageBox(msg, title, wx.YES_NO | wx.ICON_QUESTION, parent=parent) == wx.YES
	gui.mainFrame.prePopup()
	try:
		return gui.messageBox(msg, title, wx.YES_NO | wx.ICON_QUESTION) == wx.YES
	finally:
		gui.mainFrame.postPopup()


class _DeleteDocumentDialog(wx.Dialog):
	def __init__(self, parent):
		# Translators: Title of the dialog shown when deleting a document from history.
		super().__init__(parent, title=_("Delete Document"), size=(460, 280))
		sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Radio choices label for deleting a document from history.
		mode_label = _("What should be deleted?")
		self.mode_box = wx.RadioBox(
			self,
			label=mode_label,
			choices=[
				# Translators: Deletion option that only removes the document entry from history.
				_("Delete from history only"),
				# Translators: Deletion option that removes the document from history and also clears its cached OCR text so the next open re-scans it.
				_("Delete from history and cached text"),
			],
		)
		sizer.Add(self.mode_box, 0, wx.ALL | wx.EXPAND, 10)
		# Translators: Checkbox that remembers the chosen deletion option so it is not asked again.
		self.chk_dont_ask = wx.CheckBox(self, label=_("Don't ask again"))
		sizer.Add(self.chk_dont_ask, 0, wx.ALL, 10)
		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button that confirms the document deletion.
		btn_ok = wx.Button(self, wx.ID_OK, label=_("Delete"))
		btn_ok.SetDefault()
		# Translators: Button that cancels the document deletion.
		btn_cancel = wx.Button(self, wx.ID_CANCEL, label=_("Cancel"))
		btn_sizer.Add(btn_ok, 0, wx.RIGHT, 10)
		btn_sizer.Add(btn_cancel, 0)
		sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		self.SetSizer(sizer)
		self.mode_box.SetSelection(0)

	def GetMode(self):
		return "cache" if self.mode_box.GetSelection() == 1 else "history"

	def GetDontAsk(self):
		return self.chk_dont_ask.IsChecked()


class HistoryDialog(wx.Dialog):
	def __init__(self, parent, store, on_open_chat=None, on_open_document=None):
		# Translators: Title of the dialog that lists recent chats and documents.
		dlg_title = _("History")
		super().__init__(
			parent,
			title=dlg_title,
			size=(560, 420),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		self.store = store
		self.on_open_chat = on_open_chat
		self.on_open_document = on_open_document
		self._items = []
		self._init_ui()
		self._refresh()

	def _init_ui(self):
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		filter_row = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Label for the filter combo box in the History dialog.
		filter_label = wx.StaticText(self, label=_("Show:"))
		filter_row.Add(filter_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		self.filter_combo = wx.Choice(self, choices=[label for _k, label in _FILTERS])
		self.filter_combo.SetSelection(0)
		self.filter_combo.Bind(wx.EVT_CHOICE, self._on_filter_change)
		filter_row.Add(self.filter_combo, 0, wx.RIGHT, 10)
		main_sizer.Add(filter_row, 0, wx.ALL, 10)

		self.list_ctrl = wx.ListBox(self, style=wx.LB_SINGLE)
		# Translators: Accessible name for the list of history entries.
		self.list_ctrl.SetName(_("History"))
		self.list_ctrl.Bind(wx.EVT_LISTBOX_DCLICK, self._on_open)
		self.list_ctrl.Bind(wx.EVT_KEY_DOWN, self._on_list_key_down)
		main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button to open the selected history item.
		self.open_btn = wx.Button(self, label=_("Open"))
		self.open_btn.SetDefault()
		self.open_btn.Bind(wx.EVT_BUTTON, self._on_open)
		# Translators: Button to delete the selected history item.
		self.delete_btn = wx.Button(self, label=_("Delete"))
		self.delete_btn.Bind(wx.EVT_BUTTON, self._on_delete)
		# Translators: Button to clear all history items.
		self.clear_btn = wx.Button(self, label=_("Clear All"))
		self.clear_btn.Bind(wx.EVT_BUTTON, self._on_clear)
		# Translators: Button to close the History dialog.
		close_btn = wx.Button(self, wx.ID_CANCEL, label=_("Close"))
		for btn in (self.open_btn, self.delete_btn, self.clear_btn, close_btn):
			btn_sizer.Add(btn, 0, wx.RIGHT | wx.TOP, 5)
		main_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

		self.SetSizer(main_sizer)
		self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)
		self.list_ctrl.SetFocus()

	def _on_char_hook(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
			return
		event.Skip()

	def _on_filter_change(self, event):
		self._refresh()

	def _on_list_key_down(self, event):
		if event.GetKeyCode() == wx.WXK_DELETE:
			self._delete_selected(confirm=False)
			return
		event.Skip()

	def _selected_item(self):
		sel = self.list_ctrl.GetSelection()
		if sel < 0 or sel >= len(self._items):
			return None
		return self._items[sel]

	def _refresh(self):
		kind = _FILTERS[self.filter_combo.GetSelection()][0]
		all_items = self.store.load_all()
		if kind != "all":
			all_items = [i for i in all_items if i.get("type") == kind]
		self._items = all_items
		self.list_ctrl.Clear()
		for item in all_items:
			self.list_ctrl.Append(_format_item(item))
		has_items = bool(all_items)
		self.open_btn.Enable(has_items)
		self.delete_btn.Enable(has_items)
		self.clear_btn.Enable(has_items)
		if all_items:
			self.list_ctrl.SetSelection(0)
		else:
			# Translators: Message announced when the history list is empty.
			wx.CallLater(150, ui.message, _("No history yet."))

	def _on_open(self, event):
		item = self._selected_item()
		if not item:
			return
		self.Destroy()
		if item.get("type") == "chat" and self.on_open_chat:
			self.on_open_chat(item)
		elif item.get("type") == "document" and self.on_open_document:
			self.on_open_document(item)

	def _delete_selected(self, confirm=True):
		item = self._selected_item()
		if not item:
			return
		if item.get("type") == "document":
			self._delete_document(item)
			return
		# Translators: Message confirming deletion of the selected history item.
		if confirm and not _confirm_dialog(_("Delete this item from history?"), _("Delete"), parent=self):
			self.Raise()
			if self.list_ctrl.IsEnabled():
				self.list_ctrl.SetFocus()
			return
		self.store.delete(item.get("id"))
		self._refresh()
		# Translators: Announcement when a history item is deleted.
		ui.message(_("Deleted."))
		self.Raise()
		if self.list_ctrl.IsEnabled():
			self.list_ctrl.SetFocus()

	def _delete_document(self, item):
		mode = self._document_delete_mode(parent=self)
		if not mode:
			self.Raise()
			if self.list_ctrl.IsEnabled():
				self.list_ctrl.SetFocus()
			return
		self.store.delete(item.get("id"))
		if mode == "cache":
			self._clear_document_cache(item)
		self._refresh()
		# Translators: Announcement when a document is deleted from history.
		ui.message(_("Deleted."))
		self.Raise()
		if self.list_ctrl.IsEnabled():
			self.list_ctrl.SetFocus()

	@staticmethod
	def _document_delete_mode(parent=None):
		pref = nvda_config.conf["VisionAssistant"].get("document_delete_mode", "ask")
		if pref in ("history", "cache"):
			return pref
		if parent:
			dlg = _DeleteDocumentDialog(parent)
			try:
				if dlg.ShowModal() != wx.ID_OK:
					return None
				mode = dlg.GetMode()
				if dlg.GetDontAsk():
					nvda_config.conf["VisionAssistant"]["document_delete_mode"] = mode
				return mode
			finally:
				dlg.Destroy()
		gui.mainFrame.prePopup()
		try:
			dlg = _DeleteDocumentDialog(gui.mainFrame)
			if dlg.ShowModal() != wx.ID_OK:
				return None
			mode = dlg.GetMode()
			if dlg.GetDontAsk():
				nvda_config.conf["VisionAssistant"]["document_delete_mode"] = mode
			return mode
		finally:
			dlg.Destroy()
			gui.mainFrame.postPopup()

	@staticmethod
	def _clear_document_cache(item):
		try:
			paths = (item.get("data") or {}).get("paths") or []
			if not paths:
				return
			from .. import vision_config
			from ..utils.storage import OCRTextCache

			OCRTextCache(vision_config.OCR_TEXT_CACHE_FILE).delete_matching(paths)
		except Exception as e:
			log.debug(f"Document OCR cache clear failed: {e}")

	def _on_delete(self, event):
		self._delete_selected(confirm=True)

	def _on_clear(self, event):
		if not self._items:
			return
		kind = _FILTERS[self.filter_combo.GetSelection()][0]
		if kind == "chat":
			# Translators: Message confirming clearing of all chats in the History dialog.
			confirm_msg = _("Clear all chats? This cannot be undone.")
		elif kind == "document":
			# Translators: Message confirming clearing of all documents in the History dialog.
			confirm_msg = _("Clear all documents? This cannot be undone.")
		else:
			# Translators: Message confirming clearing of all history.
			confirm_msg = _("Clear all history? This cannot be undone.")
		if not _confirm_dialog(confirm_msg, _("Clear All"), parent=self):
			self.Raise()
			if self.list_ctrl.IsEnabled():
				self.list_ctrl.SetFocus()
			return
		self.store.clear(kind if kind != "all" else None)
		self._refresh()
		# Translators: Announcement when history is cleared.
		ui.message(_("History cleared."))
		self.Raise()
		if self.list_ctrl.IsEnabled():
			self.list_ctrl.SetFocus()
		else:
			self.filter_combo.SetFocus()


class RecentDocumentsDialog(wx.Dialog):
	def __init__(self, parent, store, on_open_document=None, on_browse=None):
		title = "{0} - {1}".format(ADDON_NAME, _("Document Reader"))
		super().__init__(
			parent,
			title=title,
			size=(560, 420),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		self.store = store
		self.on_open_document = on_open_document
		self.on_browse = on_browse
		self._items = []
		self._init_ui()
		self._refresh()

	def _init_ui(self):
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Label for the recent documents list in the Document Reader.
		lbl = wx.StaticText(self, label=_("Recent Documents:"))
		main_sizer.Add(lbl, 0, wx.ALL, 10)

		self.list_ctrl = wx.ListBox(self, style=wx.LB_SINGLE)
		# Translators: Accessible name for the list of recent documents.
		self.list_ctrl.SetName(_("Recent Documents"))
		self.list_ctrl.Bind(wx.EVT_LISTBOX_DCLICK, self._on_open)
		self.list_ctrl.Bind(wx.EVT_KEY_DOWN, self._on_list_key_down)
		main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button to open the selected recent document.
		self.open_btn = wx.Button(self, label=_("Open"))
		self.open_btn.SetDefault()
		self.open_btn.Bind(wx.EVT_BUTTON, self._on_open)
		# Translators: Button to delete the selected recent document.
		self.delete_btn = wx.Button(self, label=_("Delete"))
		self.delete_btn.Bind(wx.EVT_BUTTON, self._on_delete)
		# Translators: Button to clear all recent documents.
		self.clear_btn = wx.Button(self, label=_("Clear All"))
		self.clear_btn.Bind(wx.EVT_BUTTON, self._on_clear)
		# Translators: Button to browse for a document file instead of opening a recent one. Ctrl+O is the shortcut.
		self.open_file_btn = wx.Button(self, label=_("Open File..."))
		self.open_file_btn.Bind(wx.EVT_BUTTON, self._on_browse)
		# Translators: Button to close the recent documents dialog.
		close_btn = wx.Button(self, wx.ID_CANCEL, label=_("Close"))
		for btn in (self.open_btn, self.delete_btn, self.clear_btn, self.open_file_btn, close_btn):
			btn_sizer.Add(btn, 0, wx.RIGHT | wx.TOP, 5)
		main_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

		self.SetSizer(main_sizer)
		self.Bind(wx.EVT_CHAR_HOOK, self._on_char_hook)
		self.list_ctrl.SetFocus()

	def _on_char_hook(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
			return
		if event.ControlDown() and event.GetKeyCode() in (ord("O"), ord("o")):
			self._on_browse(None)
			return
		event.Skip()

	def _on_list_key_down(self, event):
		if event.GetKeyCode() == wx.WXK_DELETE:
			self._delete_selected(confirm=False)
			return
		event.Skip()

	def _selected(self):
		sel = self.list_ctrl.GetSelection()
		if sel < 0 or sel >= len(self._items):
			return None
		return self._items[sel]

	def _refresh(self):
		docs = [i for i in self.store.load_all() if i.get("type") == "document"]
		self._items = docs
		self.list_ctrl.Clear()
		for item in docs:
			self.list_ctrl.Append(_format_item(item))
		has_items = bool(docs)
		self.delete_btn.Enable(has_items)
		self.clear_btn.Enable(has_items)
		if has_items:
			self.list_ctrl.SetSelection(0)
		else:
			# Translators: Message announced when the recent documents list is empty.
			wx.CallLater(150, ui.message, _("No recent documents."))

	def _on_open(self, event):
		item = self._selected()
		if not item:
			return
		self.Destroy()
		if self.on_open_document:
			self.on_open_document(item)

	def _on_browse(self, event):
		if not self.on_browse:
			return
		self.Destroy()
		self.on_browse()

	def _delete_selected(self, confirm=True):
		item = self._selected()
		if not item:
			return
		# Translators: Message confirming deletion of the selected recent document.
		if confirm and not _confirm_dialog(_("Delete this item from history?"), _("Delete"), parent=self):
			self.Raise()
			if self.list_ctrl.IsEnabled():
				self.list_ctrl.SetFocus()
			return
		self.store.delete(item.get("id"))
		self._refresh()
		# Translators: Announcement when a history item is deleted.
		ui.message(_("Deleted."))
		self.Raise()
		if self.list_ctrl.IsEnabled():
			self.list_ctrl.SetFocus()

	def _on_delete(self, event):
		self._delete_selected(confirm=True)

	def _on_clear(self, event):
		if not self._items:
			return
		# Translators: Message confirming clearing of all recent documents.
		if not _confirm_dialog(_("Clear all recent documents?"), _("Clear All"), parent=self):
			self.Raise()
			if self.list_ctrl.IsEnabled():
				self.list_ctrl.SetFocus()
			return
		self.store.clear("document")
		self._refresh()
		# Translators: Announcement when all recent documents are cleared.
		ui.message(_("History cleared."))
		self.Raise()
		if self.list_ctrl.IsEnabled():
			self.list_ctrl.SetFocus()
