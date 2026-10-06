# -*- coding: utf-8 -*-
import os
import time
import logging
import threading

import wx
import addonHandler
import config as nvda_config
import api
import ui

from .. import plugin_state
from ..utils.error_contract import is_ai_error, ai_error_message
from ..utils.system import clean_markdown, markdown_to_html, show_error_dialog, get_file_path

log = logging.getLogger(__name__)
addonHandler.initTranslation()


class VisionQADialog(wx.Dialog):
	def __init__(
		self,
		parent,
		title,
		initial_text,
		context_data,
		callback_fn,
		extra_info=None,
		raw_content=None,
		status_callback=None,
		announce_on_open=True,
		allow_questions=True,
		allow_attachments=False,
	):
		super(VisionQADialog, self).__init__(
			parent,
			title=title,
			size=(550, 500),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		self.context_data = context_data
		self.callback_fn = callback_fn
		self.extra_info = extra_info if extra_info is not None else {}
		self.chat_history = []
		self.raw_content = raw_content
		self.status_callback = status_callback
		self.announce_on_open = announce_on_open
		self.allow_questions = allow_questions
		self.allow_attachments = allow_attachments
		self.attached_files = []
		self._session_attachments = []
		self._nav_messages = []
		self._nav_index = -1
		self._processing_range = None

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Label for the AI response text area in a chat dialog
		lbl_text = _("AI Response:")
		lbl = wx.StaticText(self, label=lbl_text)
		mainSizer.Add(lbl, 0, wx.ALL, 5)
		self.outputArea = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
		mainSizer.Add(self.outputArea, 1, wx.EXPAND | wx.ALL, 5)

		self.should_clean = nvda_config.conf["VisionAssistant"]["clean_markdown_chat"]

		display_text = None
		history_to_restore = extra_info.get("restore_history") if extra_info else None
		if history_to_restore:
			self.chat_history = history_to_restore[:]
			for h in self.chat_history:
				role = "user" if h.get("role") == "user" else "model"
				text = h.get("parts", [{}])[0].get("text", "")
				if role == "user":
					# Translators: Format for displaying User message in a chat dialog
					msg = _("\nYou: {text}\n").format(text=text)
					self._add_nav_message(text, "user")
				else:
					disp = clean_markdown(text) if self.should_clean else text
					# Translators: Format for displaying AI message in a chat dialog
					msg = _("AI: {text}\n").format(text=disp)
					display_text = disp
					self._add_nav_message(disp, "model")
				self.outputArea.AppendText(msg)
		else:
			display_text = clean_markdown(initial_text) if self.should_clean else initial_text
			if display_text:
				init_msg = _("AI: {text}\n").format(text=display_text)
				self.outputArea.AppendText(init_msg)
				self._add_nav_message(display_text, "model")
				if nvda_config.conf["VisionAssistant"]["copy_to_clipboard"] and not (
					extra_info and extra_info.get("skip_init_copy")
				):
					api.copyToClip(raw_content if raw_content else display_text)

			if not (extra_info and extra_info.get("skip_init_history")):
				self.chat_history.append({"role": "model", "parts": [{"text": initial_text}]})

			if plugin_state.plugin_instance:
				plugin_state.plugin_instance._last_chat_history = self.chat_history[:]

		restore_attachments = extra_info.get("restore_attachments") if extra_info else None
		if restore_attachments:
			self._session_attachments = [
				a.get("path") for a in restore_attachments if a.get("path") and os.path.exists(a.get("path"))
			]
			self.attached_files = list(self._session_attachments)

		self.inputArea = None
		if allow_questions:
			# Translators: Label for user input field in a chat dialog
			ask_text = _("Ask:")
			inputLbl = wx.StaticText(self, label=ask_text)
			mainSizer.Add(inputLbl, 0, wx.ALL, 5)
			self.inputArea = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 60))
			mainSizer.Add(self.inputArea, 0, wx.EXPAND | wx.ALL, 5)

		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.askBtn = None
		self.attachBtn = None
		if allow_questions:
			if self.allow_attachments:
				# Translators: Button to attach files in a chat dialog
				self.attachBtn = wx.Button(self, label=_("&Attach File"))
				self.attachBtn.Bind(wx.EVT_BUTTON, self.on_attach_file)
				if self._session_attachments:
					self.attachBtn.SetLabel(
						_("Attach File ({count})").format(count=len(self._session_attachments)),
					)
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

		if self.askBtn:
			if self.attachBtn:
				btnSizer.Add(self.attachBtn, 0, wx.ALL, 5)
			btnSizer.Add(self.askBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.viewBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.saveContentBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.saveBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.closeBtn, 0, wx.ALL, 5)
		mainSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT)

		self.SetSizer(mainSizer)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		if self.inputArea:
			self.inputArea.SetFocus()
		else:
			self.outputArea.SetFocus()
		if self.askBtn:
			self.askBtn.Bind(wx.EVT_BUTTON, self.onAsk)
		self.saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
		if self.inputArea:
			self.inputArea.Bind(wx.EVT_KEY_DOWN, self.onInputKeyDown)
		if display_text and self.announce_on_open:
			wx.CallLater(300, ui.message, display_text)
		if self.extra_info.get("initial_user_text"):
			self._save_to_history()

	def on_close(self, event):
		self._save_to_history()
		if plugin_state.plugin_instance:
			plugin_state.plugin_instance.current_status = _("Idle")
		event.Skip()

	def _save_to_history(self):
		try:
			if not nvda_config.conf["VisionAssistant"].get("save_chat_history", True):
				return
			history = list(self.chat_history)
			initial_text = self.extra_info.get("initial_user_text")
			if initial_text and not (history and history[0].get("role") == "user"):
				history.insert(0, {"role": "user", "parts": [{"text": initial_text}]})
			if not any(m.get("role") == "user" for m in history):
				return
			from .. import vision_config
			from ..utils.storage import HistoryStore

			user_msgs = [m for m in history if m.get("role") == "user"]
			first_text = user_msgs[0].get("parts", [{}])[0].get("text", "")
			subtitle = " ".join(first_text.split())[:60]
			attachments = []
			for path in self._session_attachments:
				if not os.path.exists(path):
					continue
				rec = {"path": path}
				try:
					from ..utils.system import get_mime_type

					rec["mime_type"] = get_mime_type(path)
				except Exception:
					pass
				attachments.append(rec)
			item_id = self.extra_info.get("history_id")
			if not item_id:
				item_id = "chat|" + str(time.time())
				self.extra_info["history_id"] = item_id
			item = {
				"id": item_id,
				"type": "chat",
				"title": self.GetTitle(),
				"subtitle": subtitle,
				"timestamp": time.time(),
				"data": {"history": history[-40:], "attachments": attachments},
			}
			HistoryStore(vision_config.HISTORY_FILE).save(item)
			if plugin_state.plugin_instance:
				plugin_state.plugin_instance._last_chat_id = item_id
		except Exception as e:
			log.debug(f"Chat history save failed: {e}")

	def onInputKeyDown(self, event):
		if event.GetKeyCode() == wx.WXK_RETURN and not event.ShiftDown():
			self.onAsk(None)

		else:
			event.Skip()

	def on_char_hook(self, event):
		if event.AltDown():
			key = event.GetKeyCode()
			if key == wx.WXK_UP:
				self._read_prev_message()
				return
			if key == wx.WXK_DOWN:
				self._read_next_message()
				return
			if key == ord("C"):
				self._copy_current_message()
				return
		event.Skip()

	def _add_nav_message(self, text, role="model"):
		if not text:
			return
		self._nav_messages.append((role, text))
		self._nav_index = len(self._nav_messages) - 1

	def _read_prev_message(self):
		if not self._nav_messages:
			return
		if self._nav_index > 0:
			self._nav_index -= 1
		self._speak_nav_message(self._nav_index)

	def _read_next_message(self):
		if not self._nav_messages:
			return
		if self._nav_index < len(self._nav_messages) - 1:
			self._nav_index += 1
		self._speak_nav_message(self._nav_index)

	def _speak_nav_message(self, index):
		role, text = self._nav_messages[index]
		if role == "user":
			prefix = _("\nYou: {text}\n").format(text="").strip()
		else:
			prefix = _("AI: {text}\n").format(text="").strip()
		if prefix:
			prefix += " "
		if index == 0:
			# Translators: Announced before the first message when reviewing a chat conversation with Alt+Up/Down.
			boundary = _("First message")
			ui.message(boundary + ". " + prefix + text)
		elif index == len(self._nav_messages) - 1:
			# Translators: Announced before the last message when reviewing a chat conversation with Alt+Up/Down.
			boundary = _("Last message")
			ui.message(boundary + ". " + prefix + text)
		else:
			ui.message(prefix + text)

	def _copy_current_message(self):
		if not self._nav_messages or self._nav_index < 0:
			return
		_role, text = self._nav_messages[self._nav_index]
		if text:
			api.copyToClip(text)
			# Translators: Announced when the currently selected chat message is copied to the clipboard.
			ui.message(_("Copied."))

	def onAsk(self, event):
		if not self.inputArea:
			return
		question = self.inputArea.Value
		if not (question.strip() or self.attached_files):
			return
		user_msg = _("\nYou: {text}\n").format(text=question)
		self.outputArea.AppendText(user_msg)
		self._add_nav_message(question, "user")
		self.inputArea.Clear()
		# Translators: Message shown while processing in a chat dialog
		msg = _("Thinking...")
		ui.message(msg)
		if question.strip() or self.attached_files:
			# Translators: Text appended to the chat window while waiting for the AI to respond.
			processing_msg = _("\nProcessing...\n")
			start = self.outputArea.GetLastPosition()
			self.outputArea.AppendText(processing_msg)
			self._processing_range = (start, self.outputArea.GetLastPosition())
			self.askBtn.Enable(False)
			if self.attachBtn:
				self.attachBtn.Enable(False)
			self.saveBtn.Enable(False)
			self.viewBtn.Enable(False)
			self.saveContentBtn.Enable(False)
			if plugin_state.plugin_instance:
				# Translators: Status when the AI is thinking in chat dialog
				plugin_state.plugin_instance.current_status = _("Processing response...")
			threading.Thread(
				target=self.process_question,
				args=(question, list(self.attached_files)),
				daemon=True,
			).start()

	def on_attach_file(self, event):
		wildcard = "All files (*.*)|*.*"
		# Translators: Title of the file selection dialog when attaching a file to a chat.
		attach_title = _("Select a file to attach")
		with wx.FileDialog(
			self,
			attach_title,
			wildcard=wildcard,
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_OK:
				path = fileDialog.GetPath()
				self.attached_files.append(path)
				if path not in self._session_attachments:
					self._session_attachments.append(path)
				# Translators: Label for attach button when files are attached
				self.attachBtn.SetLabel(_("Attach File ({count})").format(count=len(self.attached_files)))
				# Translators: Announcement when a file is attached to chat. {name} is the file name.
				ui.message(_("File attached: {name}").format(name=os.path.basename(path)))

	def process_question(self, question, attachments):
		try:
			self.extra_info["attachments"] = attachments
			result_tuple = self.callback_fn(self.context_data, question, self.chat_history, self.extra_info)

			response_text, _unused = result_tuple if result_tuple else (None, None)
			if response_text:
				if is_ai_error(response_text):
					wx.CallAfter(show_error_dialog, ai_error_message(response_text))
					if plugin_state.plugin_instance:
						# Translators: Error message shown when uploading a video file fails.
						plugin_state.plugin_instance.current_status = _("Idle")
					return

				self.chat_history.append({"role": "user", "parts": [{"text": question}]})
				self.chat_history.append({"role": "model", "parts": [{"text": response_text}]})
				if plugin_state.plugin_instance:
					plugin_state.plugin_instance._last_chat_history = self.chat_history[:]
				wx.CallAfter(self._save_to_history)

				final_text = clean_markdown(response_text) if self.should_clean else response_text
				wx.CallAfter(self.update_response, final_text, response_text)
				if plugin_state.plugin_instance:
					plugin_state.plugin_instance.current_status = _("Idle")
		except Exception as e:
			log.error(f"Process question failed: {e}", exc_info=True)
			wx.CallAfter(show_error_dialog, str(e))
		finally:
			wx.CallAfter(self._clear_processing)
			self.extra_info.pop("attachments", None)
			self.attached_files = []
			if self.attachBtn:
				wx.CallAfter(self.attachBtn.SetLabel, _("&Attach File"))
			wx.CallAfter(self.askBtn.Enable, True)
			if self.attachBtn:
				wx.CallAfter(self.attachBtn.Enable, True)
			wx.CallAfter(self.saveBtn.Enable, True)
			wx.CallAfter(self.viewBtn.Enable, True)
			wx.CallAfter(self.saveContentBtn.Enable, True)

	def _clear_processing(self):
		if self._processing_range is not None:
			start, end = self._processing_range
			self._processing_range = None
			try:
				self.outputArea.Remove(start, end)
			except Exception:
				pass

	def update_response(self, display_text, raw_text=None):
		self._clear_processing()
		if raw_text:
			self.raw_content = raw_text
			self.viewBtn.Enable(True)
			self.saveContentBtn.Enable(True)
		ai_msg = _("AI: {text}\n").format(text=display_text)
		self.outputArea.AppendText(ai_msg)
		self._add_nav_message(display_text, "model")
		self.saveBtn.Enable(True)
		if nvda_config.conf["VisionAssistant"]["copy_to_clipboard"]:
			api.copyToClip(raw_text if raw_text else display_text)
		self.outputArea.ShowPosition(self.outputArea.GetLastPosition())
		ui.message(display_text)

	def report_save(self, msg):
		if self.status_callback:
			self.status_callback(msg)
		else:
			ui.message(msg)

	def onView(self, event):
		full_html = ""
		user_label = _("\nYou: {text}\n").format(text="").strip()
		ai_label = _("AI: {text}\n").format(text="").strip()

		if self.chat_history:
			for item in self.chat_history:
				role = item.get("role", "")
				text = item.get("parts", [{}])[0].get("text", "")
				if role == "user":
					safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
					full_html += f"<h2>{user_label}</h2><p>{safe_text}</p>"
				elif role == "model":
					formatted_text = markdown_to_html(text, full_page=False)
					full_html += f"<h2>{ai_label}</h2>{formatted_text}<hr>"

		if not full_html and self.raw_content:
			formatted_text = markdown_to_html(self.raw_content, full_page=False)
			full_html += f"<h2>{ai_label}</h2>{formatted_text}"

		if not full_html:
			return
		try:
			# Translators: Title of the formatted result window
			ui.browseableMessage(full_html, _("Formatted Conversation"), isHtml=True)
		except Exception as e:
			# Translators: Error message if viewing fails
			msg = _("Error displaying content: {error}").format(error=e)
			show_error_dialog(msg)

	def onSave(self, event):
		# Translators: Save dialog title
		path = get_file_path(_("Save Chat Log"), "Text files (*.txt)|*.txt", mode="save")
		if path:
			try:
				with open(path, "w", encoding="utf-8") as f:
					f.write(self.outputArea.GetValue())
				# Translators: Message shown on successful save of a file.
				self.report_save(_("Saved."))
			except Exception as e:
				# Translators: Message in the error dialog when saving fails.
				msg = _("Save failed: {error}").format(error=e)
				show_error_dialog(msg)

	def onSaveContent(self, event):
		# Translators: File dialog title for saving chat content as HTML.
		save_title = _("Save Result")
		path = get_file_path(save_title, "HTML files (*.html)|*.html", mode="save")
		if path:
			try:
				full_html = markdown_to_html(self.raw_content, full_page=True)
				with open(path, "w", encoding="utf-8-sig") as f:
					f.write(full_html)
				self.report_save(_("Saved."))
			except Exception as e:
				msg = _("Save failed: {error}").format(error=e)
				show_error_dialog(msg)
