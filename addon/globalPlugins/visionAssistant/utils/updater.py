# -*- coding: utf-8 -*-
import os
import json
import re
import threading
import tempfile
import wx
from urllib import request

import addonHandler
import gui
import ui
import core
import logging

addonHandler.initTranslation()

log = logging.getLogger(__name__)

from .media_capture import get_proxy_opener
from .system import clean_markdown, show_error_dialog
from ..vision_config import ADDON_NAME
from .. import plugin_state


class UpdateDialog(wx.Dialog):
	def __init__(self, parent, version, name, changes):
		# Translators: Title of update confirmation dialog
		super().__init__(parent, title=_("Update Available"), size=(500, 450))
		self.Centre()

		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)

		# Translators: Message asking user to update. {version} is version number.
		msg = _("A new version ({version}) of {name} is available.").format(version=version, name=name)
		header = wx.StaticText(panel, label=msg)
		vbox.Add(header, 0, wx.ALL, 15)

		# Translators: Label for the changes text box
		change_lbl = wx.StaticText(panel, label=_("Changes:"))
		vbox.Add(change_lbl, 0, wx.LEFT | wx.RIGHT, 15)

		self.changes_ctrl = wx.TextCtrl(
			panel,
			value=changes,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2,
		)
		vbox.Add(self.changes_ctrl, 1, wx.EXPAND | wx.ALL, 15)

		# Translators: Question to download and install
		question = wx.StaticText(panel, label=_("Download and Install?"))
		vbox.Add(question, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button to accept update
		self.yes_btn = wx.Button(panel, wx.ID_YES, label=_("&Yes"))
		# Translators: Button to reject update
		self.no_btn = wx.Button(panel, wx.ID_NO, label=_("&No"))

		btn_sizer.Add(self.yes_btn, 0, wx.RIGHT, 10)
		btn_sizer.Add(self.no_btn, 0)
		vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 15)

		panel.SetSizer(vbox)
		self.yes_btn.SetDefault()
		self.yes_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_YES))
		self.no_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_NO))


class UpdateManager:
	def __init__(self, repo_name):
		self.repo_name = repo_name
		self.current_version = addonHandler.getCodeAddon().manifest["version"]

	def check_for_updates(self, silent=True):
		threading.Thread(target=self._check_thread, args=(silent,), daemon=True).start()

	def _check_thread(self, silent):
		try:
			if self._is_prerelease(self.current_version):
				url = f"https://api.github.com/repos/{self.repo_name}/releases?per_page=5"
			else:
				url = f"https://api.github.com/repos/{self.repo_name}/releases/latest"
			req = request.Request(url, headers={"User-Agent": "NVDA-Addon"})
			opener = get_proxy_opener(url)
			with opener.open(req, timeout=60) as response:
				if response.status == 200:
					raw_data = json.loads(response.read().decode("utf-8"))
					if isinstance(raw_data, list):
						if not raw_data:
							if not silent:
								core.callLater(0, ui.message, _("You have the latest version."))
							return
						data = raw_data[0]
					else:
						data = raw_data
					latest_tag = data.get("tag_name", "").lstrip("v")
					if self._compare_versions(latest_tag, self.current_version) > 0:
						download_url = None
						for asset in data.get("assets", []):
							if asset["name"].endswith(".nvda-addon"):
								download_url = asset["browser_download_url"]
								break
						if download_url:
							raw_changes = data.get("body", "")

							clean_changes = re.split(r"SHA256|Checklist|---", raw_changes, flags=re.I)[
								0
							].strip()
							clean_changes = clean_markdown(clean_changes)

							wx.CallAfter(self._prompt_update, latest_tag, download_url, clean_changes)
						elif not silent:
							# Translators: Error message when an update is found but the addon file is missing from GitHub.
							msg = _("Update found but no .nvda-addon file in release.")
							show_error_dialog(msg)
					elif not silent:
						# Translators: Status message informing the user they are already on the latest version.
						msg = _("You have the latest version.")
						core.callLater(0, ui.message, msg)
		except Exception as e:
			if not silent:
				# Translators: Error message shown when the add-on fails to check for updates. The {error} placeholder is replaced with specific error details.
				msg = _("Update check failed: {error}").format(error=e)
				show_error_dialog(msg)

	def _compare_versions(self, v1, v2):
		if v1 == v2:
			return 0
		try:
			from packaging.version import parse
			pv1 = parse(v1)
			pv2 = parse(v2)
			return (pv1 > pv2) - (pv1 < pv2)
		except Exception:
			pass
		try:
			t1 = self._parse_version_tuple(v1)
			t2 = self._parse_version_tuple(v2)
			return (t1 > t2) - (t1 < t2)
		except Exception:
			return 0

	@staticmethod
	def _is_prerelease(v):
		try:
			from packaging.version import parse
			return parse(str(v)).is_prerelease
		except Exception:
			return bool(re.search(r"[.-]?(alpha|beta|rc|dev|a|b)\d*$", str(v), re.I))

	@staticmethod
	def _parse_version_tuple(v):
		v = str(v).lstrip("v").strip()
		match = re.match(r"^(\d+(?:\.\d+)*)(?:[.-]?(alpha|beta|rc|dev|a|b|post)?(\d+)?)?$", v, re.I)
		if not match:
			parts = [int(x) for x in re.findall(r"\d+", v)]
			return (parts, 1, 0, 0)
		num_part, tag, tag_num = match.groups()
		nums = [int(x) for x in num_part.split(".")]
		tag_weights = {"dev": 0, "alpha": 1, "a": 1, "beta": 2, "b": 2, "rc": 3}
		if not tag:
			return (nums, 1, 0, 0)
		t_weight = tag_weights.get(tag.lower(), -1)
		t_num = int(tag_num) if tag_num else 0
		return (nums, 0, t_weight, t_num)

	def _prompt_update(self, version, url, changes):
		gui.mainFrame.prePopup()
		try:
			dlg = UpdateDialog(gui.mainFrame, version, ADDON_NAME, changes)
			if dlg.ShowModal() == wx.ID_YES:
				threading.Thread(target=self._download_install_worker, args=(url,), daemon=True).start()
			dlg.Destroy()
		finally:
			gui.mainFrame.postPopup()

	def _download_install_worker(self, url):
		try:
			# Translators: Message shown while downloading update
			plugin_state.speak_status(_("Downloading update, please wait..."))
			temp_dir = tempfile.gettempdir()
			file_path = os.path.join(temp_dir, "VisionAssistant_Update.nvda-addon")

			opener = get_proxy_opener(url)
			req = request.Request(url, headers={"User-Agent": "NVDA-Addon"})
			with opener.open(req, timeout=300) as response:
				total_size = int(response.headers.get("content-length", 0))
				downloaded = 0
				with open(file_path, "wb") as out_file:
					while True:
						chunk = response.read(1024 * 1024)
						if not chunk:
							break
						out_file.write(chunk)
						downloaded += len(chunk)
						if total_size > 0:
							percent = int((downloaded / total_size) * 100)
							# Translators: Progress message during update download
							status_msg = _("Downloading update: {percent}%").format(percent=percent)
							if downloaded % (5 * 1024 * 1024) < 1024 * 1024:
								plugin_state.speak_status(status_msg)

			wx.CallAfter(os.startfile, file_path)
		except Exception as e:
			# Translators: Error message for download failure
			msg = _("Download failed: {error}").format(error=e)
			wx.CallAfter(show_error_dialog, msg)
