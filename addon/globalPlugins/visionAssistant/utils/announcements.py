# -*- coding: utf-8 -*-
import json
import threading
import webbrowser
import logging
from urllib import request
import wx

import addonHandler
import gui
import config as _real_config


class _ConfigProxy:
	def __getattr__(self, name):
		import sys

		cfg = sys.modules.get("config")
		if cfg is not None and hasattr(cfg, name):
			return getattr(cfg, name)
		return getattr(_real_config, name)


nvda_config = _ConfigProxy()

addonHandler.initTranslation()

log = logging.getLogger(__name__)

from .media_capture import get_proxy_opener

ANNOUNCEMENT_URLS = [
	"https://raw.githubusercontent.com/mahmoodhozhabri/VisionAssistantPro/master/announcement.json",
	"https://raw.githubusercontent.com/mahmoodhozhabri/VisionAssistantPro/main/announcement.json",
]


class AnnouncementDialog(wx.Dialog):
	def __init__(self, parent, title, message, url=""):
		# Translators: Default title for announcement window
		dlg_title = title if title else _("Vision Assistant Announcement")
		super().__init__(parent, title=dlg_title, size=(520, 380))
		self.Centre()
		self.url = (url or "").strip()

		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)

		# Translators: Label for the announcement message text box
		self.lbl_message = wx.StaticText(panel, label=_("&Message"))
		vbox.Add(self.lbl_message, 0, wx.LEFT | wx.RIGHT | wx.TOP, 15)

		self.txt_message = wx.TextCtrl(
			panel, value=message, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2
		)
		vbox.Add(self.txt_message, 1, wx.EXPAND | wx.ALL, 15)

		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.btn_open = None
		if self.url:
			# Translators: Button to open external announcement link in browser
			self.btn_open = wx.Button(panel, label=_("&Open Link"))
			self.btn_open.Bind(wx.EVT_BUTTON, self.on_open_link)
			btn_sizer.Add(self.btn_open, 0, wx.RIGHT, 10)

		# Translators: Button to close announcement
		self.btn_ok = wx.Button(panel, wx.ID_OK, label=_("&OK"))
		self.btn_ok.SetDefault()
		btn_sizer.Add(self.btn_ok, 0)

		vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
		panel.SetSizer(vbox)

		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_hook)
		self.btn_ok.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_OK))
		self.txt_message.SetFocus()

	def on_open_link(self, event):
		if self.url:
			try:
				webbrowser.open(self.url)
			except Exception as e:
				log.warning(f"Failed to open announcement url: {e}")
		self.EndModal(wx.ID_OK)

	def on_key_hook(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.EndModal(wx.ID_OK)
		else:
			event.Skip()


def _resolve_localized_text(val, current_lang):
	if isinstance(val, dict):
		if current_lang in val:
			return str(val[current_lang])
		short = current_lang.split("_")[0].split("-")[0]
		if short in val:
			return str(val[short])
		if "en" in val:
			return str(val["en"])
		for k, v in val.items():
			return str(v)
		return ""
	return str(val or "")


class AnnouncementManager:
	@staticmethod
	def check_announcements():
		threading.Thread(target=AnnouncementManager._worker, daemon=True).start()

	@staticmethod
	def _worker():
		try:
			last_seen_id = nvda_config.conf["VisionAssistant"].get("last_seen_announcement_id", "1")
		except Exception:
			last_seen_id = "1"

		data = None
		for url in ANNOUNCEMENT_URLS:
			try:
				req = request.Request(url, headers={"User-Agent": "NVDA-Addon"})
				opener = get_proxy_opener(url)
				with opener.open(req, timeout=5) as resp:
					if resp.status == 200:
						raw = resp.read().decode("utf-8", errors="ignore")
						data = json.loads(raw)
						break
			except Exception as e:
				log.debug(f"Announcement check failed for {url}: {e}")
				continue

		if not data or not isinstance(data, dict):
			return

		remote_id = str(data.get("id", "")).strip()
		if not remote_id or remote_id == last_seen_id:
			return

		try:
			nvda_config.conf["VisionAssistant"]["last_seen_announcement_id"] = remote_id
			if hasattr(nvda_config.conf, "save") and callable(getattr(nvda_config.conf, "save", None)):
				nvda_config.conf.save()
		except Exception as e:
			log.warning(f"Failed to save last_seen_announcement_id: {e}")

		cur_lang = "en"
		try:
			import languageHandler
			cur_lang = languageHandler.getLanguage() or "en"
		except Exception:
			pass

		title = _resolve_localized_text(data.get("title", ""), cur_lang)
		message = _resolve_localized_text(data.get("message", ""), cur_lang)
		link_url = str(data.get("url", "")).strip()

		if not message.strip():
			return

		wx.CallAfter(AnnouncementManager._show_dialog, title, message, link_url)

	@staticmethod
	def _show_dialog(title, message, link_url):
		try:
			try:
				import winsound

				winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
			except Exception:
				pass
			gui.mainFrame.prePopup()
			dlg = AnnouncementDialog(gui.mainFrame, title, message, link_url)
			dlg.ShowModal()
			dlg.Destroy()
		except Exception as e:
			log.warning(f"Error displaying AnnouncementDialog: {e}")
		finally:
			try:
				gui.mainFrame.postPopup()
			except Exception:
				pass
