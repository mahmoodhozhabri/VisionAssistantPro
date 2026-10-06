# -*- coding: utf-8 -*-
import copy
import math
import os
import struct
import threading
import logging
import re
import subprocess
import warnings
import wave
import shutil
import tempfile
import zipfile

with warnings.catch_warnings():
	warnings.simplefilter("ignore")
	try:
		import audioop as _audioop
	except ImportError:
		_audioop = None

import wx

import addonHandler
import config as nvda_config
import ui
import core
import gui
import tones
import synthDriverHandler

import comtypes.client

from .. import vision_config
from .. import plugin_state
from ..utils.storage import SeriesCharacterStore
from ..utils.system import apply_model_filter, show_error_dialog
from ..utils.media_capture import get_proxy_opener, GeminiLiveTTS, LiveTTSAborted, ensure_ffmpeg
from ..utils import vad as vad_utils

log = logging.getLogger(__name__)

addonHandler.initTranslation()

lib_dir = os.path.join(os.path.dirname(__file__), "..", "lib")


class DubbingDialog(wx.Dialog):
	def __init__(self, parent, is_dubbing=True):
		self.is_dubbing = is_dubbing
		if is_dubbing:
			# Translators: Title of the dubbing options dialog
			title = _("Dubbing Options")
		else:
			# Translators: Title of the translation options dialog
			title = _("Translation Options")
		super().__init__(parent, title=title, size=(350, 200) if not is_dubbing else (350, 150))
		sizer = wx.BoxSizer(wx.VERTICAL)

		g_sizer = wx.FlexGridSizer(2, 2, 10, 10)

		if not is_dubbing:
			# Translators: Label for the media translation source language combo box.
			g_sizer.Add(wx.StaticText(self, label=_("Source:")), 0, wx.ALIGN_CENTER_VERTICAL)
			self.cmb_source = wx.Choice(self, choices=vision_config.SOURCE_NAMES)
			curr_s_code = nvda_config.conf["VisionAssistant"]["source_language"]
			s_idx = next((i for i, x in enumerate(vision_config.SOURCE_LIST) if x[1] == curr_s_code), 0)
			self.cmb_source.SetSelection(s_idx)
			g_sizer.Add(self.cmb_source, 1, wx.EXPAND)

		# Translators: Label for the media translation target language combo box.
		g_sizer.Add(wx.StaticText(self, label=_("Target:")), 0, wx.ALIGN_CENTER_VERTICAL)
		self.cmb_target = wx.Choice(self, choices=vision_config.TARGET_NAMES)
		curr_t_code = nvda_config.conf["VisionAssistant"]["target_language"]
		t_idx = next((i for i, x in enumerate(vision_config.TARGET_LIST) if x[1] == curr_t_code), 0)
		self.cmb_target.SetSelection(t_idx)
		g_sizer.Add(self.cmb_target, 1, wx.EXPAND)

		sizer.Add(g_sizer, 1, wx.EXPAND | wx.ALL, 15)

		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		btn_ok = wx.Button(self, wx.ID_OK, label=_("Start"))
		btn_ok.SetDefault()
		# Translators: Button to add a label for the selected element
		btn_cancel = wx.Button(self, wx.ID_CANCEL, label=_("Cancel"))
		btn_sizer.Add(btn_ok, 0, wx.RIGHT, 10)
		btn_sizer.Add(btn_cancel, 0)
		sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		self.SetSizer(sizer)

	def get_settings(self):
		if not getattr(self, "is_dubbing", True):
			s_idx = self.cmb_source.GetSelection()
			source_lang = vision_config.SOURCE_NAMES[s_idx]
		else:
			source_lang = "Auto-detect"

		t_idx = self.cmb_target.GetSelection()
		return source_lang, vision_config.TARGET_NAMES[t_idx]


class AmbientStartDialog(wx.Dialog):
	def __init__(
		self,
		parent,
		modes,
		initial_mode="audio",
		initial_context="general",
		initial_audio_source="system",
		initial_ptt=True,
		initial_style="brief",
	):
		self._modes = list(modes)
		# Translators: Title of the dialog that starts the Ambient Observer.
		super().__init__(parent, title=_("Ambient Observer"), size=(470, 320))
		sizer = wx.BoxSizer(wx.VERTICAL)

		g_sizer = wx.FlexGridSizer(rows=0, cols=2, vgap=10, hgap=10)

		# Translators: Label for choosing the working mode of the Ambient Observer.
		g_sizer.Add(wx.StaticText(self, label=_("Observer Mode:")), 0, wx.ALIGN_CENTER_VERTICAL)
		self.cmb_mode = wx.Choice(self, choices=[self._mode_label(key, label) for key, label in self._modes])
		self.cmb_mode.SetMinSize(wx.Size(240, self.cmb_mode.GetBestSize().height))
		mode_index = next((i for i, entry in enumerate(self._modes) if entry[0] == initial_mode), 0)
		self.cmb_mode.SetSelection(mode_index)
		self.cmb_mode.Bind(wx.EVT_CHOICE, self.on_mode_change)
		g_sizer.Add(self.cmb_mode, 1, wx.EXPAND)

		# Translators: Label for choosing the language that the Ambient Observer translates heard audio into.
		self.lbl_target = wx.StaticText(self, label=_("Target:"))
		g_sizer.Add(self.lbl_target, 0, wx.ALIGN_CENTER_VERTICAL)
		self.cmb_target = wx.Choice(self, choices=vision_config.TARGET_NAMES)
		curr_t_code = nvda_config.conf["VisionAssistant"]["target_language"]
		t_idx = next((i for i, x in enumerate(vision_config.TARGET_LIST) if x[1] == curr_t_code), 0)
		self.cmb_target.SetSelection(t_idx)
		g_sizer.Add(self.cmb_target, 1, wx.EXPAND)

		# Translators: Label for choosing where the Ambient Observer takes the audio it listens to from.
		self.lbl_audio = wx.StaticText(self, label=_("Audio Source:"))
		g_sizer.Add(self.lbl_audio, 0, wx.ALIGN_CENTER_VERTICAL)
		self.cmb_audio = wx.Choice(self, choices=vision_config.AMBIENT_SOURCE_NAMES)
		audio_index = next(
			(i for i, x in enumerate(vision_config.AMBIENT_SOURCE_LIST) if x[0] == initial_audio_source),
			0,
		)
		self.cmb_audio.SetSelection(audio_index)
		g_sizer.Add(self.cmb_audio, 1, wx.EXPAND)

		# Translators: Label for the optional description of what the user is doing while observing the screen or webcam.
		self.lbl_context = wx.StaticText(self, label=_("About what I am doing:"))
		g_sizer.Add(self.lbl_context, 0, wx.ALIGN_CENTER_VERTICAL)
		self.cmb_context = wx.ComboBox(
			self,
			choices=[label for _key, label, _instruction in self._options_for_mode(initial_mode)],
			style=wx.CB_DROPDOWN,
		)
		context_label = next(
			(
				label
				for key, label, _instruction in self._options_for_mode(initial_mode)
				if key == initial_context
			),
			"",
		)
		if context_label:
			self.cmb_context.SetValue(context_label)
		else:
			self.cmb_context.SetValue(initial_context)
		g_sizer.Add(self.cmb_context, 1, wx.EXPAND)

		# Translators: Label for selecting how detailed the Ambient Observer reports are.
		self.lbl_style = wx.StaticText(self, label=_("Reporting Style:"))
		g_sizer.Add(self.lbl_style, 0, wx.ALIGN_CENTER_VERTICAL)
		self.cmb_style = wx.Choice(self, choices=vision_config.AMBIENT_STYLE_NAMES)
		style_index = next(
			(i for i, x in enumerate(vision_config.AMBIENT_STYLE_LIST) if x[0] == initial_style),
			0,
		)
		self.cmb_style.SetSelection(style_index)
		g_sizer.Add(self.cmb_style, 1, wx.EXPAND)

		sizer.Add(g_sizer, 1, wx.EXPAND | wx.ALL, 15)

		# Translators: Checkbox to enable Push to Talk for the webcam Live Assistant session started by the observer.
		self.chk_ptt = wx.CheckBox(self, label=_("Ask questions with Push to Talk"))
		self.chk_ptt.SetValue(bool(initial_ptt))
		sizer.Add(self.chk_ptt, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)

		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button to start the Ambient Observer with the selected options.
		btn_ok = wx.Button(self, wx.ID_OK, label=_("Start"))
		btn_ok.SetDefault()
		# Translators: Button to cancel starting the Ambient Observer.
		btn_cancel = wx.Button(self, wx.ID_CANCEL, label=_("Cancel"))
		btn_sizer.Add(btn_ok, 0, wx.RIGHT, 10)
		btn_sizer.Add(btn_cancel, 0)
		sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		self.SetSizer(sizer)
		self.on_mode_change(None)

	def _options_for_mode(self, mode):
		if mode == "webcam":
			return vision_config.AMBIENT_WEBCAM_CONTEXT_LIST
		return vision_config.AMBIENT_CONTEXT_LIST

	def _context_options(self):
		return self._options_for_mode(self._selected_mode())

	def _selected_mode(self):
		index = self.cmb_mode.GetSelection()
		if index == wx.NOT_FOUND:
			index = 0
		return self._modes[index][0]

	def on_mode_change(self, event):
		mode = self._selected_mode()
		needs_audio = mode == "audio"
		self.lbl_target.Show(needs_audio)
		self.cmb_target.Show(needs_audio)
		self.lbl_audio.Show(needs_audio)
		self.cmb_audio.Show(needs_audio)
		self.lbl_context.Show(not needs_audio)
		self.cmb_context.Show(not needs_audio)
		self.lbl_style.Show(not needs_audio)
		self.cmb_style.Show(not needs_audio)
		self.chk_ptt.Show(mode == "webcam")
		if not needs_audio:
			current = self.cmb_context.GetValue().strip()
			options = self._context_options()
			self.cmb_context.Set([label for _key, label, _instruction in options])
			match = next((label for _key, label, _i in options if label == current), "")
			if match:
				self.cmb_context.SetValue(match)
			elif current:
				self.cmb_context.SetValue(current)
			else:
				self.cmb_context.SetSelection(0)
		self.Layout()

	def _mode_label(self, mode, label):
		hint = self._hint_for_mode(mode)
		return f"{label} - {hint}" if hint else label

	def _hint_for_mode(self, mode):
		if mode == "webcam":
			# Translators: Hint shown in the Ambient Observer start dialog for the webcam mode.
			return _("The Live Assistant window opens with the webcam, so you can ask questions at any time.")
		if mode == "audio":
			# Translators: Hint shown in the Ambient Observer start dialog for the audio translation mode.
			return _("Translates continuously what the selected audio source hears.")
		# Translators: Hint shown in the Ambient Observer start dialog for the screen watching mode.
		return _("Reports screen changes automatically, without you asking.")

	def get_settings(self):
		mode = self._selected_mode()
		target_index = self.cmb_target.GetSelection()
		if target_index == wx.NOT_FOUND:
			target_index = 0
		target_name = vision_config.TARGET_NAMES[target_index]
		target_code = vision_config.TARGET_CODES.get(target_name, "en")
		context = self.cmb_context.GetValue().strip()
		context_key = ""
		for key, label, _instruction in self._context_options():
			if label == context:
				context_key = key
				break
		if not context_key:
			context_key = context or "general"
		source_index = self.cmb_audio.GetSelection()
		if source_index == wx.NOT_FOUND:
			source_index = 0
		audio_source = vision_config.AMBIENT_SOURCE_LIST[source_index][0]
		style_index = self.cmb_style.GetSelection()
		if style_index == wx.NOT_FOUND:
			style_index = 0
		style = vision_config.AMBIENT_STYLE_LIST[style_index][0]
		return mode, target_code, context_key, audio_source, bool(self.chk_ptt.Value), style


class _CharacterEditDialog(wx.Dialog):
	def __init__(self, parent, name="", notes="", allow_ai=True):
		# Translators: Title of the character name dialog.
		super().__init__(parent, title=_("Character"))
		sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Label for the character name field.
		sizer.Add(wx.StaticText(self, label=_("Name:")), 0, wx.ALL, 10)
		self.name_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
		self.name_input.SetValue(name)
		sizer.Add(self.name_input, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		sizer.Add(
			# Translators: Label for the optional character notes field (e.g., role or relationship).
			wx.StaticText(self, label=_("Notes (optional, e.g. role or relationship):")),
			0,
			wx.LEFT | wx.RIGHT | wx.BOTTOM,
			10,
		)
		self.notes_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
		self.notes_input.SetValue(notes)
		sizer.Add(self.notes_input, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		# Translators: Checkbox to allow the AI to update this character's description automatically in later episodes.
		self.allow_ai_check = wx.CheckBox(self, label=_("Allow AI to update this character later"))
		self.allow_ai_check.SetValue(allow_ai)
		sizer.Add(self.allow_ai_check, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		sizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND | wx.ALL, 10)
		self.SetSizer(sizer)
		self.name_input.SetFocus()

	def get_values(self):
		return (
			self.name_input.GetValue().strip(),
			self.notes_input.GetValue().strip(),
			self.allow_ai_check.GetValue(),
		)


class SeriesCharactersDialog(wx.Dialog):
	def __init__(self, parent, series_name="", characters=None):
		# Translators: Title of the character dictionary dialog.
		title = _("{name} - Character Dictionary").format(name=vision_config.ADDON_NAME)
		super().__init__(parent, title=title, size=(460, 420))
		self.saved_series_name = ""
		self.deleted_series = False
		self._orig_series_name = series_name
		self._store = SeriesCharacterStore(vision_config.SERIES_FILE)
		if characters is None:
			self._characters = copy.deepcopy(self._store.get_series(series_name))
		else:
			self._characters = copy.deepcopy(characters)

		sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Label for the series or movie name field.
		sizer.Add(wx.StaticText(self, label=_("Series / movie name:")), 0, wx.ALL, 10)
		existing = self._store.list_series()
		self.series_cb = wx.ComboBox(self, style=wx.CB_DROPDOWN)
		self.series_cb.SetItems(existing)
		self._loaded_name = series_name
		self.series_cb.Bind(wx.EVT_COMBOBOX, self._on_series_selected)
		self.series_cb.Bind(wx.EVT_TEXT, self._on_series_text)
		self.series_cb.SetValue(series_name)
		sizer.Add(self.series_cb, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		sizer.Add(
			# Translators: Label explaining that only character names are needed; descriptions are generated automatically.
			wx.StaticText(self, label=_("Character names (descriptions are generated automatically by AI):")),
			0,
			wx.LEFT | wx.RIGHT | wx.BOTTOM,
			10,
		)
		self.char_list = wx.ListBox(self, style=wx.LB_SINGLE)
		sizer.Add(self.char_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

		btn_box = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button to edit the selected character.
		self.btn_edit = wx.Button(self, label=_("&Edit..."))
		self.btn_edit.Bind(wx.EVT_BUTTON, self.on_edit)
		# Translators: Button to add a new character to the series dictionary.
		self.btn_add = wx.Button(self, label=_("&Add..."))
		self.btn_add.Bind(wx.EVT_BUTTON, self.on_add)
		# Translators: Button to paste a list of character names into the series dictionary.
		self.btn_import = wx.Button(self, label=_("&Import List..."))
		self.btn_import.Bind(wx.EVT_BUTTON, self.on_import)
		# Translators: Button to remove the selected character from the series dictionary.
		self.btn_remove = wx.Button(self, label=_("&Remove"))
		self.btn_remove.Bind(wx.EVT_BUTTON, self.on_remove)
		# Translators: Button to remove all characters from the series dictionary.
		self.btn_clear = wx.Button(self, label=_("C&lear All"))
		self.btn_clear.Bind(wx.EVT_BUTTON, self.on_clear)
		for b in (self.btn_edit, self.btn_add, self.btn_import, self.btn_remove, self.btn_clear):
			btn_box.Add(b, 0, wx.RIGHT, 5)
		sizer.Add(btn_box, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

		del_box = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button to delete the entire series or movie dictionary.
		self.btn_delete = wx.Button(self, label=_("&Delete Series / Movie..."))
		self.btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
		del_box.Add(self.btn_delete, 0)
		sizer.Add(del_box, 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

		sizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0, wx.EXPAND | wx.ALL, 10)
		self.SetSizer(sizer)
		self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)
		self.char_list.Bind(wx.EVT_CHAR_HOOK, self._on_char_key)
		self._refresh_list()
		self.series_cb.SetFocus()

	def _on_char_key(self, event):
		key = event.GetKeyCode()
		if key == wx.WXK_F2:
			self.on_edit(None)
		elif key in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE):
			self.on_remove(None)
		else:
			event.Skip()

	def _refresh_list(self):
		self.char_list.Clear()
		for c in self._characters:
			if isinstance(c, dict) and c.get("name"):
				label = c["name"]
				if c.get("notes"):
					label += " — " + c["notes"]
				self.char_list.Append(label)

	def _load_series_characters(self, name):
		self._characters = copy.deepcopy(self._store.get_series(name))
		self._loaded_name = name
		self._refresh_list()

	def _on_series_selected(self, event):
		name = self.series_cb.GetValue().strip()
		if not name:
			return
		self._load_series_characters(name)

	def _on_series_text(self, event):
		name = self.series_cb.GetValue().strip()
		if not name or name == self._loaded_name:
			return
		if name in self.series_cb.GetItems():
			self._load_series_characters(name)
		else:
			self._characters = []
			self._loaded_name = name
			self._refresh_list()

	def _selected_index(self):
		return self.char_list.GetSelection()

	def on_add(self, event):
		dlg = _CharacterEditDialog(self, allow_ai=True)
		if dlg.ShowModal() == wx.ID_OK:
			name, notes, allow_ai = dlg.get_values()
			if name:
				key = SeriesCharacterStore.character_key(name)
				existing = {
					SeriesCharacterStore.character_key(c.get("name"))
					for c in self._characters
					if isinstance(c, dict) and c.get("name")
				}
				if key in existing:
					wx.MessageBox(
						# Translators: Warning when adding a character that already exists in the dictionary.
						_("This character already exists in the dictionary."),
						# Translators: Title of warning dialog for a duplicate character.
						_("Duplicate Character"),
						wx.OK | wx.ICON_WARNING,
					)
				else:
					self._characters.append(
						{"name": name, "notes": notes, "manual": not allow_ai, "user_edited": True},
					)
					self._refresh_list()
					self.char_list.SetSelection(self.char_list.GetCount() - 1)
		dlg.Destroy()

	def _parse_import_line(self, line):
		line = line.strip().lstrip("-*•·")
		if not line:
			return "", ""
		for prefix in ("با بازی ", "بازی "):
			if line.startswith(prefix):
				line = line[len(prefix) :].strip()
				break
		m = re.match(r"^(.*?)\s*\(([^()]*)\)\s*:\s*(.*)$", line)
		if m:
			char = m.group(2).strip()
			return (char if char else m.group(1).strip()), m.group(3).strip()
		m = re.match(r"^(.*?)\s+(?:در نقش|as)\s+(.*)$", line, re.IGNORECASE)
		if m:
			char = m.group(2).strip()
			notes = ""
			pm = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", char)
			if pm:
				char = pm.group(1).strip()
				notes = pm.group(2).strip()
			return char, notes
		m = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", line)
		if m:
			inner = m.group(2).strip()
			if inner and ("/" in inner or "،" in inner or "," in inner):
				return m.group(1).strip(), inner
			return inner, ""
		if ":" in line:
			left, right = line.split(":", 1)
			return left.strip(), right.strip()
		m = re.match(r"^(.*?)\s*[–—-]\s*(.*)$", line)
		if m:
			return m.group(1).strip(), ""
		return line, ""

	def on_import(self, event):
		msg = _(
			# Translators: Message asking the user to paste character names, one per line, with format guidance.
			"Paste character names, one per line.\n"
			"When the actor's name differs from the character's name, use this format:\n"
			"Actor Name (Character Name): roles / relationships\n"
			"Names without parentheses are used as-is. Only the character name is sent to the AI, never the actor's name.",
		)
		# Translators: Title of dialog for importing character names.
		import_title = _("Import Character Names")
		dlg = wx.TextEntryDialog(
			self,
			msg,
			import_title,
			style=wx.OK | wx.CANCEL | wx.TE_MULTILINE,
		)
		dlg.SetSize((420, 300))
		if dlg.ShowModal() == wx.ID_OK:
			existing = {
				SeriesCharacterStore.character_key(c.get("name"))
				for c in self._characters
				if isinstance(c, dict) and c.get("name")
			}
			for line in dlg.GetValue().splitlines():
				name, notes = self._parse_import_line(line)
				key = SeriesCharacterStore.character_key(name)
				if name and key not in existing:
					self._characters.append(
						{"name": name, "notes": notes, "manual": True, "user_edited": True},
					)
					existing.add(key)
			self._refresh_list()
		dlg.Destroy()

	def on_edit(self, event):
		idx = self._selected_index()
		if idx == wx.NOT_FOUND:
			return
		current = self._characters[idx]
		dlg = _CharacterEditDialog(
			self,
			name=current.get("name", ""),
			notes=current.get("notes", ""),
			allow_ai=not current.get("manual", False),
		)
		if dlg.ShowModal() == wx.ID_OK:
			name, notes, allow_ai = dlg.get_values()
			if name:
				key = SeriesCharacterStore.character_key(name)
				existing = {
					SeriesCharacterStore.character_key(c.get("name"))
					for i, c in enumerate(self._characters)
					if isinstance(c, dict) and c.get("name") and i != idx
				}
				if key in existing:
					wx.MessageBox(
						# Translators: Warning when renaming a character to a name that already exists in the dictionary.
						_("This character already exists in the dictionary."),
						# Translators: Title of warning dialog for a duplicate character.
						_("Duplicate Character"),
						wx.OK | wx.ICON_WARNING,
					)
				else:
					current["name"] = name
					current["notes"] = notes
					current["manual"] = not allow_ai
					current["user_edited"] = True
					self._refresh_list()
					self.char_list.SetSelection(idx)
		dlg.Destroy()

	def on_remove(self, event):
		idx = self._selected_index()
		if idx == wx.NOT_FOUND:
			return
		self._characters.pop(idx)
		self._refresh_list()

	def on_clear(self, event):
		if not self._characters:
			return
		# Translators: Confirmation prompt before removing all characters from a series.
		clear_msg = _("Remove all characters from this series?")
		# Translators: Title of confirmation dialog for clearing all characters.
		clear_title = _("Clear Characters")
		res = wx.MessageBox(
			clear_msg,
			clear_title,
			wx.YES_NO | wx.ICON_QUESTION,
		)
		if res == wx.YES:
			self._characters = []
			self._refresh_list()

	def on_delete(self, event):
		name = self.series_cb.GetValue().strip()
		if not name:
			return
		# Translators: Confirmation prompt before deleting an entire series or movie dictionary. {name} is the series name.
		del_msg = _('Delete the "{name}" dictionary and all its characters?').format(name=name)
		# Translators: Title of confirmation dialog for deleting a series dictionary.
		del_title = _("Delete Dictionary")
		res = wx.MessageBox(
			del_msg,
			del_title,
			wx.YES_NO | wx.ICON_QUESTION,
		)
		if res == wx.YES:
			self._store.delete(name)
			self.deleted_series = True
			self.saved_series_name = ""
			self.EndModal(wx.ID_CANCEL)

	def on_ok(self, event):
		name = self.series_cb.GetValue().strip()
		if not name:
			# Translators: Error message when the series name is empty.
			err_msg = _("Please enter a series name.")
			# Translators: Title of warning dialog when series name is missing.
			err_title = _("Series Name Required")
			wx.MessageBox(
				err_msg,
				err_title,
				wx.OK | wx.ICON_WARNING,
			)
			return
		self.saved_series_name = name
		self._store.save_series(name, self._characters)
		if self._orig_series_name and self._orig_series_name != name:
			self._store.delete(self._orig_series_name)
		self.EndModal(wx.ID_OK)


class VideoSourceDialog(wx.Dialog):
	def __init__(self, parent, guess_series=None, initial_path=""):
		# Translators: Title of the video analysis dialog
		title = _("{name} - Analyze Video").format(name=vision_config.ADDON_NAME)
		super().__init__(parent, title=title, size=(550, 290))
		self.local_path = None
		self._guess_series = guess_series

		sizer = wx.BoxSizer(wx.VERTICAL)
		lbl = wx.StaticText(
			self,
			# Translators: Label instructing the user to enter a URL or browse for a local video
			label=_("Enter Video URL (YouTube, Instagram, Twitter, TikTok) or Browse for a local video:"),
		)
		sizer.Add(lbl, 0, wx.ALL, 10)

		hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.url_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
		if initial_path:
			self.url_input.SetValue(initial_path)
		hbox.Add(self.url_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

		# Translators: Button to browse for a local video file
		btn_browse = wx.Button(self, label=_("&Browse..."))
		btn_browse.Bind(wx.EVT_BUTTON, self.on_browse)
		hbox.Add(btn_browse, 0, wx.ALIGN_CENTER_VERTICAL)

		sizer.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

		# Translators: Option to generate an Audio Description SRT file.
		choices = [_("General Video Analysis"), _("Generate Audio Description (SRT File)")]
		self.action_choice = wx.RadioBox(
			self,
			# Translators: Label for the video action radio box
			label=_("Action"),
			choices=choices,
			majorDimension=1,
			style=wx.RA_SPECIFY_COLS,
		)
		sizer.Add(self.action_choice, 0, wx.EXPAND | wx.ALL, 10)

		self.action_choice.Bind(wx.EVT_RADIOBOX, self.on_action_change)

		# Translators: Checkbox label to add character list as the first subtitle in video SRT output.
		self.chars_as_sub_check = wx.CheckBox(self, label=_("Add character list as first subtitle"))
		self.chars_as_sub_check.SetValue(
			nvda_config.conf["VisionAssistant"].get("video_chars_as_subtitle", True),
		)
		sizer.Add(self.chars_as_sub_check, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		self.chars_as_sub_check.Show(False)

		# Translators: Checkbox label to add an AI warning disclaimer at the beginning of the video SRT output.
		self.disclaimer_check = wx.CheckBox(self, label=_("Add AI disclaimer at the beginning"))
		self.disclaimer_check.SetValue(nvda_config.conf["VisionAssistant"].get("video_add_disclaimer", True))
		sizer.Add(self.disclaimer_check, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		self.disclaimer_check.Show(False)

		# Translators: Label for the series or movie selection combo box in the video dialog.
		self.series_label = wx.StaticText(self, label=_("Series / Movie:"))
		sizer.Add(self.series_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		self.series_label.Show(False)

		series_box = wx.BoxSizer(wx.HORIZONTAL)
		self.series_combo = wx.ComboBox(self, style=wx.CB_READONLY | wx.TE_PROCESS_ENTER)
		self._refreshing_series = False
		series_box.Add(self.series_combo, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		# Translators: Button to open the character dictionary management dialog.
		self.btn_manage_series = wx.Button(self, label=_("Manage Characters..."))
		self.btn_manage_series.Bind(wx.EVT_BUTTON, self.on_manage_series)
		series_box.Add(self.btn_manage_series, 0, wx.ALIGN_CENTER_VERTICAL)
		sizer.Add(series_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
		self.series_combo.Show(False)
		self.btn_manage_series.Show(False)
		self._refresh_series_combo("")

		btn_sizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 10)

		self.SetSizer(sizer)
		self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)
		self.url_input.SetFocus()

	def _series_store(self):
		return SeriesCharacterStore(vision_config.SERIES_FILE)

	def _refresh_series_combo(self, select=""):
		self._refreshing_series = True
		try:
			self._saved_series = self._series_store().list_series()
			self.series_combo.Clear()
			# Translators: Option in the series combo meaning no series is associated with this video.
			self.series_combo.Append(_("None (no series)"))
			# Translators: Option in the series combo that derives the series name automatically from the video file name.
			self.series_combo.Append(_("Auto (from file name)"))
			for s in self._saved_series:
				self.series_combo.Append(s)
			# Translators: Option in the combo to create a new series or movie.
			self.series_combo.Append(_("New series / movie..."))
			self.series_combo.SetSelection(0)
			if select:
				idx = self.series_combo.FindString(select)
				if idx != wx.NOT_FOUND and idx > 1 and idx < self.series_combo.GetCount() - 1:
					self.series_combo.SetSelection(idx)
		finally:
			self._refreshing_series = False

	def _current_series_selection(self):
		idx = self.series_combo.GetSelection()
		if idx == wx.NOT_FOUND or idx <= 1 or idx >= self.series_combo.GetCount() - 1:
			return ""
		return self.series_combo.GetString(idx).strip()

	def is_auto_series(self):
		return self.series_combo.GetSelection() == 1

	def selected_series(self):
		return self._current_series_selection()

	def _is_new_series_selected(self):
		idx = self.series_combo.GetSelection()
		return idx != wx.NOT_FOUND and idx == self.series_combo.GetCount() - 1

	def _guessed_series(self):
		if self._guess_series is None:
			return ""
		try:
			return self._guess_series(self.url_input.GetValue().strip()) or ""
		except Exception:
			return ""

	def on_manage_series(self, event):
		series_name = self._current_series_selection()
		if not series_name and self.is_auto_series():
			series_name = self._guessed_series()
		self._open_series_editor(series_name)

	def _open_series_editor(self, series_name):
		saved = ""
		gui.mainFrame.prePopup()
		try:
			dlg = SeriesCharactersDialog(self, series_name=series_name)
			if dlg.ShowModal() == wx.ID_OK and dlg.saved_series_name:
				saved = dlg.saved_series_name
				self._refresh_series_combo(saved)
			elif getattr(dlg, "deleted_series", False):
				self._refresh_series_combo("")
			dlg.Destroy()
		finally:
			gui.mainFrame.postPopup()
		return saved

	def on_ok(self, event):
		if self.action_choice.GetSelection() == 1 and self._is_new_series_selected():
			saved = self._open_series_editor("")
			if not saved:
				return
		event.Skip()

	def on_browse(self, event):
		# Translators: Filter for video files in the file dialog
		filter_label = _("Video Files")
		wildcard = (
			filter_label
			+ " (*.mp4;*.avi;*.mkv;*.mov;*.wmv;*.flv;*.webm)|*.mp4;*.avi;*.mkv;*.mov;*.wmv;*.flv;*.webm"
		)
		# Translators: Title of the file dialog for selecting a video
		dlg_title = _("Select Local Video")
		with wx.FileDialog(
			self,
			dlg_title,
			wildcard=wildcard,
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
		) as dlg:
			if dlg.ShowModal() == wx.ID_OK:
				self.local_path = dlg.GetPath()
				self.url_input.SetValue(self.local_path)

	def on_action_change(self, event):
		is_srt = self.action_choice.GetSelection() == 1
		self.chars_as_sub_check.Show(is_srt)
		self.disclaimer_check.Show(is_srt)
		self.series_label.Show(is_srt)
		self.series_combo.Show(is_srt)
		self.btn_manage_series.Show(is_srt)
		self.Layout()


class VideoSRTProgressDialog(wx.Dialog):
	def __init__(self, parent, regenerate_cb=None, original_path=None, series_name=None):
		# Translators: Title of the progress dialog when generating SRT
		title = _("{name} - Generating Audio Description").format(name=vision_config.ADDON_NAME)
		super().__init__(
			parent,
			title=title,
			size=(550, 480),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)
		self.srt_content = None
		self.abort = False
		self.regenerate_cb = regenerate_cb
		self.retry_cb = None
		self.original_path = original_path
		self.series_name = series_name
		self.file_uri = None
		self.is_srt_done = False
		self.cache_dir = tempfile.mkdtemp(prefix="nvda_va_cache_")
		self._gemini_tts_cache = {}

		sizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Label for the status log text box
		lbl = wx.StaticText(self, label=_("Process Status / Subtitle Content:"))
		sizer.Add(lbl, 0, wx.ALL, 10)
		self.txt_status = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
		sizer.Add(self.txt_status, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

		hbox_voice = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Label for selecting the Windows TTS voice
		self.lbl_voice = wx.StaticText(self, label=_("Narration Voice:"))
		hbox_voice.Add(self.lbl_voice, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		self.voice_sel = wx.Choice(self, choices=[])
		self.voice_sel.Bind(wx.EVT_CHOICE, self.on_voice_change)
		hbox_voice.Add(self.voice_sel, 1, wx.EXPAND)
		self.voice_sel.Disable()
		sizer.Add(hbox_voice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

		self.hbox_variant = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Label for selecting the eSpeak voice variant
		self.lbl_variant = wx.StaticText(self, label=_("eSpeak Voice Variant:"))
		self.hbox_variant.Add(self.lbl_variant, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

		self.espeak_variant_sel = wx.ComboBox(self, style=wx.TE_PROCESS_ENTER)
		self.espeak_variant_sel.Bind(wx.EVT_TEXT, self.onModelFilter)
		for vname, vid in self._get_espeak_variants():
			self.espeak_variant_sel.Append(vname, vid)
		if self.espeak_variant_sel.GetCount() > 0:
			self.espeak_variant_sel.SetSelection(0)

		self.hbox_variant.Add(self.espeak_variant_sel, 1, wx.EXPAND)

		# Translators: Button to download missing eSpeak-NG
		self.btn_download_espeak = wx.Button(self, label=_("Download eSpeak-NG"))
		self.btn_download_espeak.Bind(wx.EVT_BUTTON, self.on_download_espeak)
		self.hbox_variant.Add(self.btn_download_espeak, 1, wx.EXPAND)

		sizer.Add(self.hbox_variant, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

		self.lbl_variant.Show(False)
		self.espeak_variant_sel.Show(False)
		self.btn_download_espeak.Show(False)
		self.espeak_variant_sel.Disable()
		self.btn_download_espeak.Disable()

		self.hbox_gemini_voice = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Label for selecting the Gemini Live TTS voice
		self.lbl_gemini_voice = wx.StaticText(self, label=_("Gemini Voice:"))
		self.hbox_gemini_voice.Add(self.lbl_gemini_voice, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

		gemini_choices = [f"{v[0]} ({v[1]})" for v in vision_config.GEMINI_VOICES]
		self.gemini_voice_sel = wx.Choice(self, choices=gemini_choices)
		self.hbox_gemini_voice.Add(self.gemini_voice_sel, 1, wx.EXPAND)

		curr_g_voice = nvda_config.conf["VisionAssistant"].get("tts_voice", "Puck")
		g_idx = next((i for i, v in enumerate(vision_config.GEMINI_VOICES) if v[0] == curr_g_voice), 0)
		if self.gemini_voice_sel.GetCount() > 0:
			self.gemini_voice_sel.SetSelection(g_idx)

		sizer.Add(self.hbox_gemini_voice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

		self.lbl_gemini_voice.Show(False)
		self.gemini_voice_sel.Show(False)
		self.gemini_voice_sel.Disable()

		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button to save the generated SRT file
		self.btn_save = wx.Button(self, label=_("&Save SRT"))
		self.btn_save.Disable()
		self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)

		# Translators: Button to generate a synced MP3 narration using offline TTS
		self.btn_generate_mp3 = wx.Button(self, label=_("&Generate Synced Narration (MP3)"))
		self.btn_generate_mp3.Disable()
		self.btn_generate_mp3.Bind(wx.EVT_BUTTON, self.on_generate_mp3)

		# Translators: Button to regenerate the audio description
		self.btn_regenerate = wx.Button(self, label=_("&Regenerate"))
		self.btn_regenerate.Disable()
		self.btn_regenerate.Bind(wx.EVT_BUTTON, self.on_regenerate)

		# Translators: Button to close the dialog
		self.btn_close = wx.Button(self, wx.ID_CANCEL, label=_("&Close / Cancel"))
		self.btn_close.Bind(wx.EVT_BUTTON, self.on_close)

		# Translators: Button to retry generation after a temporary server error
		self.btn_try_again = wx.Button(self, label=_("&Try Again"))
		self.btn_try_again.Bind(wx.EVT_BUTTON, self.on_try_again)
		self.btn_try_again.Hide()
		self.btn_try_again.Disable()

		btn_sizer.Add(self.btn_save, 0, wx.RIGHT, 5)
		btn_sizer.Add(self.btn_generate_mp3, 0, wx.RIGHT, 5)
		btn_sizer.Add(self.btn_regenerate, 0, wx.RIGHT, 5)
		btn_sizer.Add(self.btn_try_again, 0, wx.RIGHT, 5)
		btn_sizer.Add(self.btn_close, 0)
		sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

		self.SetSizer(sizer)
		self.CenterOnParent()
		self.Bind(wx.EVT_CLOSE, self.on_close)

		# Translators: Initial status message
		self.update_status(_("Initializing..."))
		self.txt_status.SetFocus()

		threading.Thread(target=self._load_offline_voices, daemon=True).start()

	def _get_espeak_variants(self):
		espeak_dir = os.path.join(lib_dir, "espeak-ng", "espeak-ng-data", "voices", "!v")
		variants = []

		if os.path.exists(espeak_dir):
			try:
				for f in sorted(os.listdir(espeak_dir)):
					file_path = os.path.join(espeak_dir, f)
					if os.path.isfile(file_path) and not f.startswith("."):
						vid = f
						vname = vid.capitalize()

						try:
							with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
								for line in file:
									line_clean = line.strip()
									if line_clean.lower().startswith("name "):
										extracted_name = line_clean[5:].strip()
										if extracted_name:
											vname = extracted_name.capitalize()
											break
						except Exception:
							pass

						variants.append((vname, vid))
			except Exception as e:
				log.error(f"Failed to dynamically parse espeak variants: {e}")

		return variants

	def _update_variant_visibility(self):
		try:
			if not getattr(self, "voice_sel", None):
				return
			sel = self.voice_sel.GetSelection()
		except Exception:
			return
		if sel != wx.NOT_FOUND:
			voice_id = self.voice_sel.GetClientData(sel)
			is_espeak = str(voice_id).startswith("espeak")
			is_gemini = str(voice_id) == "gemini_tts"

			self.lbl_gemini_voice.Show(is_gemini)
			self.gemini_voice_sel.Show(is_gemini)
			if is_gemini:
				self.gemini_voice_sel.Enable()
			else:
				self.gemini_voice_sel.Disable()

			if is_espeak:
				exe_path = os.path.join(lib_dir, "espeak-ng", "espeak-ng.exe")
				if os.path.exists(exe_path):
					self.lbl_variant.Show(True)
					self.btn_download_espeak.Show(False)
					self.espeak_variant_sel.Show(True)

					current_vid = None
					variants = self._get_espeak_variants()

					if self.espeak_variant_sel.GetCount() == 0:
						for vname, vid in variants:
							self.espeak_variant_sel.Append(vname, vid)

					is_first_run = not hasattr(self, "_first_variant_run")
					if is_first_run:
						self._first_variant_run = False

					if not is_first_run:
						v_sel = self.espeak_variant_sel.GetSelection()
						if v_sel != wx.NOT_FOUND and v_sel < len(variants):
							current_vid = variants[v_sel][1]

					if not current_vid:
						try:
							synth = synthDriverHandler.getSynth()
							if synth.name == "espeak":
								current_vid = getattr(synth, "variant", "max")
							else:
								current_vid = "max"
						except Exception:
							current_vid = "max"

					match_idx = 0
					for i, (vname, vid) in enumerate(variants):
						if vid == current_vid:
							match_idx = i
							break

					if self.espeak_variant_sel.GetCount() > 0:
						self.espeak_variant_sel.SetSelection(match_idx)

					if self.is_srt_done:
						self.espeak_variant_sel.Enable()
						self.btn_generate_mp3.Enable()
					else:
						self.espeak_variant_sel.Disable()
						self.btn_generate_mp3.Disable()
				else:
					self.lbl_variant.Show(False)
					self.espeak_variant_sel.Show(False)
					self.btn_download_espeak.Show(True)
					self.btn_generate_mp3.Disable()
					if self.is_srt_done:
						self.btn_download_espeak.Enable()
					else:
						self.btn_download_espeak.Disable()
			else:
				self.lbl_variant.Show(False)
				self.espeak_variant_sel.Show(False)
				self.btn_download_espeak.Show(False)
				if self.is_srt_done:
					self.btn_generate_mp3.Enable()
				else:
					self.btn_generate_mp3.Disable()
			self.Layout()

	def onModelFilter(self, event):
		cb = event.GetEventObject()
		if cb.IsFrozen():
			return

		sel = cb.GetSelection()
		if sel != wx.NOT_FOUND:
			return

		filtered = apply_model_filter(cb, cb.GetValue())

		if filtered:
			cb.Popup()

	def _generate_espeak_wav(self, text, voice_id, espeak_variant, output_wav):
		espeak_exe = os.path.join(lib_dir, "espeak-ng", "espeak-ng.exe")
		if not os.path.exists(espeak_exe):
			return False

		espeak_voice = "en"
		if voice_id.startswith("espeak_") and voice_id != "espeak_current":
			espeak_voice = voice_id.split("_")[1]

		espeak_speed = "175"
		espeak_pitch = "50"
		espeak_volume = "100"
		espeak_inflection = "75"

		if voice_id == "espeak_current":
			try:
				synth = synthDriverHandler.getSynth()
				if synth.name == "espeak":
					v = getattr(synth, "voice", "en")
					if "\\" in v:
						v = v.split("\\")[-1]
					espeak_voice = v

					nvda_rate = getattr(synth, "rate", 50)
					espeak_speed = str(int(80 + (nvda_rate / 100.0) * 370))

					nvda_pitch = getattr(synth, "pitch", 50)
					espeak_pitch = str(int(nvda_pitch))

					nvda_volume = getattr(synth, "volume", 100)
					espeak_volume = str(int((nvda_volume / 100.0) * 200))
					nvda_inflection = getattr(synth, "inflection", 75)
					espeak_inflection = str(int(nvda_inflection))
			except Exception:
				pass

		ssml_text = f'<speak><prosody range="{espeak_inflection}">{text}</prosody></speak>'

		if espeak_variant:
			espeak_voice = espeak_voice.split("+")[0]
			espeak_voice += f"+{espeak_variant}"

		try:
			subprocess.run(
				[
					espeak_exe,
					"-v",
					espeak_voice,
					"-s",
					espeak_speed,
					"-p",
					espeak_pitch,
					"-a",
					espeak_volume,
					"-m",
					"--stdin",
					"-w",
					output_wav,
				],
				input=ssml_text.encode("utf-8"),
				capture_output=True,
				creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
			)
			return os.path.exists(output_wav) and os.path.getsize(output_wav) > 44
		except Exception as e:
			log.error(f"eSpeak generation failed: {e}")
			return False

	def on_voice_change(self, event):
		self._update_variant_visibility()

	def on_download_espeak(self, event):
		threading.Thread(target=self._download_espeak_worker, daemon=True).start()

	def _download_espeak_worker(self):
		espeak_dir = os.path.join(lib_dir, "espeak-ng")
		exe_path = os.path.join(espeak_dir, "espeak-ng.exe")
		wx.CallAfter(self.btn_download_espeak.Disable)
		try:
			# Translators: Status message when downloading eSpeak-NG
			core.callLater(0, self.update_status, _("Downloading eSpeak-NG, please wait..."))
			download_url = "https://raw.githubusercontent.com/mahmoodhozhabri/VisionAssistantPro/main/eSpeak-NG-portable.zip"

			opener = get_proxy_opener(download_url)
			from urllib import request

			req = request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
			zip_path = os.path.join(lib_dir, "espeak-temp.zip")

			with opener.open(req, timeout=300) as response:
				total_size = int(response.headers.get("content-length", 0))
				downloaded = 0
				with open(zip_path, "wb") as f:
					while True:
						chunk = response.read(1024 * 1024)
						if not chunk:
							break
						f.write(chunk)
						downloaded += len(chunk)
						if total_size > 0:
							percent = int((downloaded / total_size) * 100)
							# Translators: Progress message during eSpeak-NG download
							status_msg = _("Downloading eSpeak-NG: {percent}%").format(percent=percent)
							wx.CallAfter(self.txt_status.SetValue, status_msg)
							if downloaded % (2 * 1024 * 1024) < 1024 * 1024:
								plugin_state.speak_status(status_msg)

			# Translators: Status message when extracting eSpeak-NG
			core.callLater(0, self.update_status, _("Extracting eSpeak-NG..."))
			os.makedirs(espeak_dir, exist_ok=True)
			with zipfile.ZipFile(zip_path, "r") as zip_ref:
				zip_ref.extractall(espeak_dir)
			try:
				os.remove(zip_path)
			except Exception as e:
				log.debug(f"eSpeak zip removal failed: {e}")

			if os.path.exists(exe_path):
				# Translators: Success message after eSpeak-NG download completes
				core.callLater(0, self.update_status, _("eSpeak-NG downloaded successfully!"))
				if self.is_srt_done:
					core.callLater(0, self.update_status, self.srt_content)
				wx.CallAfter(self._update_variant_visibility)
		except Exception as e:
			log.error(f"eSpeak download failed: {e}", exc_info=True)
			# Translators: Error message when eSpeak-NG download fails
			wx.CallAfter(show_error_dialog, _("Failed to download eSpeak-NG: {error}").format(error=str(e)))
			wx.CallAfter(self.btn_download_espeak.Enable)

	def _load_offline_voices(self):
		try:
			voice_list = []
			target_selection = None

			try:
				synth = synthDriverHandler.getSynth()
				synth_name = getattr(synth, "name", "")
				current_nvda_voice = getattr(synth, "voice", "")
			except Exception:
				synth_name = ""
				current_nvda_voice = ""

			current_voice_item = None

			if synth_name == "espeak":
				# Translators: Option for eSpeak voice matching the user's current NVDA voice settings
				current_voice_item = ("espeak_current", _("eSpeak (Current NVDA Language)"))
				target_selection = "espeak_current"

			sapi5_voices = []
			try:
				engine = comtypes.client.CreateObject("SAPI.SpVoice")
				voices = engine.GetVoices()
				for i in range(voices.Count):
					voice = voices.Item(i)
					desc = voice.GetDescription()
					vid = f"sapi5_{voice.Id}"

					if synth_name == "sapi5" and current_nvda_voice == voice.Id:
						current_voice_item = (vid, f"SAPI5 - {desc} (Current)")
						target_selection = vid
					else:
						sapi5_voices.append((vid, f"SAPI5 - {desc}"))
			except Exception as e:
				log.error(f"SAPI5 load failed: {e}")

			if current_voice_item:
				voice_list.append(current_voice_item)

			# Translators: Option to use Gemini Live API for highly realistic text-to-speech
			voice_list.append(("gemini_tts", _("Gemini Live TTS (Online, High Quality)")))

			if synth_name != "espeak":
				# Translators: Option for default English eSpeak voice
				voice_list.append(("espeak_en", _("eSpeak (English Default)")))

			voice_list.extend(sapi5_voices)

			if not target_selection:
				target_selection = "gemini_tts"

			wx.CallAfter(self._populate_voices, voice_list, target_selection)
		except Exception as e:
			log.error(f"Failed to load offline voices: {e}", exc_info=True)

	def _populate_voices(self, voice_list, target_selection):
		try:
			self.voice_sel.Clear()
			for vid, vname in voice_list:
				self.voice_sel.Append(vname, vid)

			if target_selection:
				for i in range(self.voice_sel.GetCount()):
					if self.voice_sel.GetClientData(i) == target_selection:
						self.voice_sel.SetSelection(i)
						self._update_variant_visibility()
						return

			if self.voice_sel.GetCount() > 0:
				self.voice_sel.SetSelection(0)
				self._update_variant_visibility()
		except Exception:
			pass
		finally:
			if self.is_srt_done:
				self.voice_sel.Enable()

	def update_status(self, msg):
		if self.abort:
			return
		self.txt_status.SetValue(msg)
		self.txt_status.SetFocus()
		if plugin_state.plugin_instance:
			plugin_state.plugin_instance.report_status(msg)
		else:
			ui.message(msg)

	def on_finished(self, srt_content):
		if self.abort:
			return
		self.srt_content = srt_content
		self.is_srt_done = True
		# Translators: Title of the dialog when generation is successfully finished
		success_title = _("{name} - Audio Description Ready").format(name=vision_config.ADDON_NAME)
		self.SetTitle(success_title)
		self.txt_status.SetValue(srt_content)
		self.btn_save.Enable()
		self.btn_regenerate.Enable()
		self.btn_generate_mp3.Enable()
		self.voice_sel.Enable()
		self._update_variant_visibility()
		self.txt_status.SetFocus()
		tones.beep(1000, 100)
		core.callLater(
			0,
			ui.message,
			# Translators: Success announcement when generation is complete
			_("Audio description generated successfully! You can read the subtitle content in the text box."),
		)

	def on_error(self, err_msg):
		if self.abort:
			return
		self.is_srt_done = True
		# Translators: Status message when an error occurs during SRT generation
		self.update_status(_("Error: {err}").format(err=err_msg))
		self.btn_regenerate.Enable()
		self.btn_generate_mp3.Disable()
		self.voice_sel.Enable()
		self._update_variant_visibility()

	def _begin_generation_state(self):
		self.abort = False
		self.is_srt_done = False
		generating_title = _("{name} - Generating Audio Description").format(name=vision_config.ADDON_NAME)
		self.SetTitle(generating_title)
		self.btn_save.Disable()
		self.btn_regenerate.Disable()
		self.btn_generate_mp3.Disable()
		self.voice_sel.Disable()
		self.espeak_variant_sel.Disable()
		self.btn_download_espeak.Disable()

	def on_try_again(self, event):
		self.btn_try_again.Hide()
		self.btn_try_again.Disable()
		self._begin_generation_state()
		# Translators: Status message when retrying generation after a temporary server error
		self.update_status(_("Retrying..."))
		if self.retry_cb:
			self.retry_cb(self)

	def show_try_again(self, err_msg):
		if self.abort:
			return
		self.update_status(
			# Translators: Status message shown when a temporary server error interrupts SRT generation and the user can retry.
			_("Temporary server error: {err}\nPress Try Again to continue from where it stopped.").format(
				err=err_msg,
			),
		)
		self.btn_try_again.Show()
		self.btn_try_again.Enable()
		self.btn_try_again.SetFocus()
		self.Layout()

	def on_regenerate(self, event):
		self.srt_content = None
		self._begin_generation_state()
		# Translators: Status message when restarting generation
		self.update_status(_("Re-initializing..."))
		if self.regenerate_cb:
			self.regenerate_cb(self)

	def on_save(self, event):
		if not self.srt_content:
			return

		default_name = "Audio_Description.srt"
		if getattr(self, "original_path", None):
			if str(self.original_path).startswith("http"):
				default_name = "Online_Video_Description.srt"
			else:
				default_name = os.path.splitext(os.path.basename(self.original_path))[0] + ".srt"

		default_dir = ""
		if getattr(self, "original_path", None) and not str(self.original_path).startswith("http"):
			d = os.path.dirname(self.original_path)
			if os.path.isdir(d):
				default_dir = d

		# Translators: File dialog title for saving the generated SRT file
		save_title = _("Save Audio Description")
		gui.mainFrame.prePopup()
		try:
			with wx.FileDialog(
				gui.mainFrame,
				save_title,
				wildcard="SRT Files (*.srt)|*.srt",
				defaultDir=default_dir,
				defaultFile=default_name,
				style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
			) as dlg:
				if dlg.ShowModal() == wx.ID_OK:
					path = dlg.GetPath()
				else:
					path = None
		finally:
			gui.mainFrame.postPopup()
		if path:
			try:
				with open(path, "w", encoding="utf-8") as f:
					f.write(self.srt_content)
				# Translators: Success message when SRT file is saved
				ui.message(_("SRT file saved successfully."))
			except Exception as e:
				show_error_dialog(str(e))

	def _parse_srt(self, srt_text):
		blocks = []
		parts = re.split(r"\n\s*\n", srt_text.strip())
		for part in parts:
			lines = [line.strip() for line in part.strip().split("\n") if line.strip()]
			if len(lines) < 3:
				continue
			time_line = lines[1]
			if "-->" not in time_line:
				continue
			try:
				start_str, end_str = [t.strip() for t in time_line.split("-->")]
				start_ms = self._time_to_ms(start_str)
				end_ms = self._time_to_ms(end_str)
				text = " ".join(lines[2:]).replace("\\n", " ").replace("\\r", " ")
				blocks.append({"start_ms": start_ms, "end_ms": end_ms, "text": text})
			except Exception:
				continue
		return blocks

	def _time_to_ms(self, t):
		h, m, rest = t.replace(",", ".").split(":")
		s, ms = rest.split(".")
		return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms.ljust(3, "0")[:3])

	def _get_wav_duration(self, wav_path):
		try:
			with wave.open(wav_path, "rb") as wf:
				return wf.getnframes() / wf.getframerate()
		except Exception:
			return 0.0

	def _generate_sapi5_wav(self, text, real_voice_id, output_wav):
		try:
			engine = comtypes.client.CreateObject("SAPI.SpVoice")
			voices = engine.GetVoices()
			for i in range(voices.Count):
				if voices.Item(i).Id == real_voice_id:
					engine.Voice = voices.Item(i)
					break

			stream = comtypes.client.CreateObject("SAPI.SpFileStream")
			stream.Open(output_wav, 3)
			engine.AudioOutputStream = stream
			engine.Speak(text)
			stream.Close()
			return os.path.exists(output_wav) and os.path.getsize(output_wav) > 44
		except Exception as e:
			log.error(f"SAPI5 TTS to WAV failed: {e}")
			return False

	def on_generate_mp3(self, event):
		if not self.srt_content:
			return
		blocks = self._parse_srt(self.srt_content)
		if not blocks:
			# Translators: Error when SRT parsing finds no valid subtitle blocks
			show_error_dialog(_("No valid subtitle blocks found in the SRT content."))
			return

		ffmpeg_path = ensure_ffmpeg()
		if not ffmpeg_path:
			return

		sel = self.voice_sel.GetSelection()
		if sel == wx.NOT_FOUND:
			# Translators: Error when no voice is selected
			show_error_dialog(_("Please select an offline voice from the list."))
			return

		voice_id = self.voice_sel.GetClientData(sel)

		gemini_voice = ""
		if voice_id == "gemini_tts":
			g_sel = self.gemini_voice_sel.GetSelection()
			if g_sel != wx.NOT_FOUND:
				gemini_voice = vision_config.GEMINI_VOICES[g_sel][0]
				nvda_config.conf["VisionAssistant"]["tts_voice"] = gemini_voice

		espeak_variant = ""
		if str(voice_id).startswith("espeak"):
			v_sel = self.espeak_variant_sel.GetSelection()
			if v_sel != wx.NOT_FOUND:
				espeak_variant = self.espeak_variant_sel.GetClientData(v_sel)

		default_name = "Audio_Narration.mp3"
		video_path = None
		if hasattr(self, "local_path") and self.local_path and os.path.exists(self.local_path):
			video_path = self.local_path
		elif hasattr(self, "original_path") and self.original_path and os.path.exists(self.original_path):
			video_path = self.original_path

		has_video = bool(video_path)

		if not has_video:
			default_name = "Online_Video_Narration.mp3"
			is_online = True
		else:
			if getattr(self, "original_path", None) and not str(self.original_path).startswith("http"):
				default_name = os.path.splitext(os.path.basename(self.original_path))[0] + "_narration.mp3"
			else:
				default_name = "Audio_Narration.mp3"
			is_online = False

		mode_selection = 0
		apply_ducking = False

		if is_online:
			gui.mainFrame.prePopup()
			try:
				warn_msg = _(
					# Translators: Warning prompt for online videos indicating that the output will only contain narration.
					"Because the source is an online video, the final file will ONLY contain the AI voice narration (synced to the timestamps) and will NOT include the original background audio of the video. Do you want to proceed?",
				)
				# Translators: Title of the warning dialog when opening an online video link.
				online_title = _("Online Video Mode")
				with wx.MessageDialog(
					self,
					warn_msg,
					online_title,
					wx.YES_NO | wx.ICON_WARNING,
				) as dlg:
					if dlg.ShowModal() != wx.ID_YES:
						return
			finally:
				gui.mainFrame.postPopup()
		else:
			# Translators: Title of the narration mode selection dialog.
			title_dlg = _("Select Narration Mode")
			# Translators: Instruction prompt for narration mode selection.
			msg_dlg = _("Choose how the narration should be mixed with the video audio:")
			choices_dlg = [
				# Translators: Option for mixing voice directly over the video without pausing.
				_("Standard AD (Mix voice directly over audio - No Pausing)"),
				# Translators: Option for pausing the background video audio during descriptions.
				_("Extended AD (Pause background audio during descriptions)"),
			]

			gui.mainFrame.prePopup()
			try:
				with wx.SingleChoiceDialog(self, msg_dlg, title_dlg, choices_dlg) as dlg:
					if dlg.ShowModal() != wx.ID_OK:
						return
					mode_selection = dlg.GetSelection()
			finally:
				gui.mainFrame.postPopup()

			if mode_selection == 0:
				gui.mainFrame.prePopup()
				try:
					duck_msg = _(
						# Translators: Prompt asking whether to lower the background video audio during the descriptions.
						"Do you want to fade/duck the background video audio during the descriptions?",
					)
					# Translators: Title for the audio ducking prompt.
					duck_title = _("Audio Ducking")
					with wx.MessageDialog(self, duck_msg, duck_title, wx.YES_NO | wx.ICON_QUESTION) as dlg:
						if dlg.ShowModal() == wx.ID_YES:
							apply_ducking = True
				finally:
					gui.mainFrame.postPopup()

		default_dir = ""
		if video_path:
			d = os.path.dirname(video_path)
			if os.path.isdir(d):
				default_dir = d

		gui.mainFrame.prePopup()
		try:
			with wx.FileDialog(
				gui.mainFrame,
				# Translators: Button label or menu item to save the generated AI audio narration synced to the video.
				_("Save Synced Narration"),
				wildcard="MP3 Files (*.mp3)|*.mp3",
				defaultDir=default_dir,
				defaultFile=default_name,
				style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
			) as dlg:
				if dlg.ShowModal() == wx.ID_OK:
					output_path = dlg.GetPath()
				else:
					output_path = None
		finally:
			gui.mainFrame.postPopup()

		if not output_path:
			return
		if not output_path.lower().endswith(".mp3"):
			output_path += ".mp3"

		self.btn_generate_mp3.Disable()
		self.btn_regenerate.Disable()
		self.btn_save.Disable()
		self.voice_sel.Disable()
		self.espeak_variant_sel.Disable()
		self.btn_download_espeak.Disable()

		# Translators: Status message when narration generation starts
		ui.message(_("Generating offline synced narration. This may take a few moments..."))
		if hasattr(self, "_tts_thread") and self._tts_thread and self._tts_thread.is_alive():
			self._tts_thread.join(0.5)
		self._tts_thread = threading.Thread(
			target=self._offline_tts_worker,
			args=(
				blocks,
				output_path,
				voice_id,
				espeak_variant,
				ffmpeg_path,
				video_path,
				mode_selection,
				apply_ducking,
				gemini_voice,
			),
			daemon=True,
		)
		self._tts_thread.start()

	def _detect_silences(
		self,
		wav_path,
		min_duration=0.3,
		window_ms=30,
		merge_gap_ms=150,
		margin_ms=80,
		threshold_db=18.0,
		hysteresis_db=6.0,
		hangover_ms=120,
	):
		with wave.open(wav_path, "rb") as wf:
			framerate = wf.getframerate()
			sampwidth = wf.getsampwidth()
			nchannels = wf.getnchannels()
			if sampwidth != 2 or framerate <= 0:
				return []
			win = max(1, int(framerate * window_ms / 1000))
			window_bytes = win * sampwidth * nchannels

			rms_vals = []
			buf = b""
			while True:
				chunk = wf.readframes(262144)
				if not chunk:
					break
				buf += chunk
				n_windows = len(buf) // window_bytes
				for i in range(n_windows):
					frag = buf[i * window_bytes : (i + 1) * window_bytes]
					if _audioop is not None:
						rms_vals.append(_audioop.rms(frag, sampwidth))
					else:
						samples = struct.unpack("<%dh" % (len(frag) // 2), frag)
						rms_vals.append(int((sum(s * s for s in samples) / max(1, len(samples))) ** 0.5))
				buf = buf[n_windows * window_bytes :]

		if len(rms_vals) < 2:
			return []

		if max(rms_vals) <= 0:
			return []

		ref = 32767.0
		db_vals = [20.0 * math.log10(max(r, 1) / ref) for r in rms_vals]
		sorted_db = sorted(db_vals)
		noise_floor_db = sorted_db[int(len(sorted_db) * 0.25)]
		threshold = max(noise_floor_db + threshold_db, -60.0)
		enter_db = threshold - hysteresis_db
		exit_db = threshold + hysteresis_db
		hangover_windows = max(0, int(hangover_ms / window_ms))

		runs = []
		in_silence = False
		run_start = None
		for idx, db in enumerate(db_vals):
			if not in_silence and db < enter_db:
				in_silence = True
				run_start = idx
			elif in_silence and db > exit_db:
				in_silence = False
				runs.append((run_start, idx - 1))
				run_start = None
		if run_start is not None:
			runs.append((run_start, len(db_vals) - 1))

		if hangover_windows:
			runs = [(s, min(e + hangover_windows, len(db_vals) - 1)) for s, e in runs]

		silences = []
		for s_idx, e_idx in runs:
			start_ms = s_idx * window_ms
			end_ms = (e_idx + 1) * window_ms
			if end_ms - start_ms >= min_duration * 1000:
				silences.append((start_ms, end_ms))

		merged = []
		for start, end in silences:
			if merged and start - merged[-1][1] <= merge_gap_ms:
				merged[-1] = (merged[-1][0], end)
			else:
				merged.append((start, end))

		result = []
		for start, end in merged:
			s = start + margin_ms
			e = end - margin_ms
			if e - s >= 150:
				result.append((s, e))
		return result

	def _find_best_pause_time(self, target_ms, silences, max_shift_ms=3000, lead_ms=80):
		if not silences:
			return target_ms

		for start, end in silences:
			if start <= target_ms <= end:
				return target_ms

		best_time = target_ms
		best_score = None

		for start, end in silences:
			if target_ms < start:
				dist = start - target_ms
			elif target_ms > end:
				dist = target_ms - end
			else:
				dist = 0

			if dist > max_shift_ms:
				continue

			dur_sec = (end - start) / 1000.0
			duration_bonus = min(dur_sec * 1000.0, 2500.0)
			score = dist - duration_bonus

			if best_score is None or score < best_score:
				best_score = score
				anchor = start + min(lead_ms, max(0, (end - start) // 2))
				best_time = anchor

		return best_time

	def _offline_tts_worker(
		self,
		blocks,
		output_path,
		voice_id,
		espeak_variant,
		ffmpeg_path,
		video_path,
		mode_selection,
		apply_ducking=False,
		gemini_voice="",
	):
		temp_dir = tempfile.mkdtemp()
		try:
			try:
				comtypes.CoInitialize()
			except Exception:
				pass
		except ImportError:
			pass

		try:
			has_video = False
			if video_path and os.path.exists(video_path):
				has_video = True
			else:
				video_path = None
				mode_selection = 0

			orig_audio_wav = os.path.join(temp_dir, "original_audio.wav")
			orig_bytes = None
			total_orig_ms = 0
			silences = []

			if has_video:
				# Translators: Status message shown when extracting the original video audio tracks.
				core.callLater(0, self.update_status, _("Extracting original video audio..."))

				subprocess.run(
					[
						ffmpeg_path,
						"-y",
						"-i",
						video_path,
						"-vn",
						"-acodec",
						"pcm_s16le",
						"-ar",
						"24000",
						"-ac",
						"1",
						orig_audio_wav,
					],
					capture_output=True,
					creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
				)

				if not os.path.exists(orig_audio_wav):
					# Translators: Error message shown when extraction of the video's original audio fails.
					wx.CallAfter(show_error_dialog, _("Failed to extract video audio."))
					return

				with wave.open(orig_audio_wav, "rb") as wf:
					orig_bytes = wf.readframes(wf.getnframes())
					orig_bytes_per_ms = wf.getframerate() * wf.getsampwidth() * wf.getnchannels() // 1000
					total_orig_ms = int(len(orig_bytes) / orig_bytes_per_ms)

				if mode_selection == 1:
					# Translators: Status message shown when analyzing the video's audio to detect periods of silence.
					core.callLater(0, self.update_status, _("Analyzing video for natural silences..."))
					vad_result = [None]
					vad_done = threading.Event()

					def _run_vad():
						try:
							vad_result[0] = vad_utils.detect_silences(orig_audio_wav)
						finally:
							vad_done.set()

					threading.Thread(target=_run_vad, daemon=True).start()
					while not vad_done.is_set():
						vad_done.wait(0.05)
					silences = vad_result[0]
					if silences is None:
						silences = self._detect_silences(orig_audio_wav)
			else:
				total_orig_ms = blocks[-1]["end_ms"] + 2000

			live_tts = None

			if voice_id == "gemini_tts":
				# Translators: Status message shown when starting connection to Gemini Live API
				core.callLater(0, self.update_status, _("Connecting to Gemini Live API..."))
				live_tts = GeminiLiveTTS(gemini_voice or "Puck")
				if not live_tts.ensure_connection(abort_checker=lambda: self.abort):
					if self.abort:
						return
					# Translators: Error message shown when connection to Gemini Live API fails
					wx.CallAfter(show_error_dialog, _("Failed to connect to Gemini Live API."))
					return

			tts_attempted = 0
			tts_failed = 0

			for i, block in enumerate(blocks):
				if self.abort:
					return
				text = block["text"].replace("*", "").replace("_", "").replace("\\n", " ").replace("\\r", " ")
				if not text.strip():
					continue
				tts_attempted += 1

				cache_key = (
					voice_id,
					gemini_voice
					if voice_id == "gemini_tts"
					else espeak_variant
					if str(voice_id).startswith("espeak")
					else "",
					text,
				)

				wav_path = os.path.join(temp_dir, f"block_{i:04d}.wav")
				success = False

				if cache_key in self._gemini_tts_cache and os.path.exists(self._gemini_tts_cache[cache_key]):
					wav_path = self._gemini_tts_cache[cache_key]
					success = True

				if not success:
					# Translators: Progress message during narration generation. {current} is the current block number, {total} is total blocks.
					progress_msg = _("Generating narration: part {current} of {total}...").format(
						current=i + 1,
						total=len(blocks),
					)
					core.callLater(0, self.update_status, progress_msg)

					if str(voice_id).startswith("espeak_"):
						success = self._generate_espeak_wav(text, voice_id, espeak_variant, wav_path)
					elif str(voice_id).startswith("sapi5_"):
						real_id = voice_id[6:]
						success = self._generate_sapi5_wav(text, real_id, wav_path)
					elif voice_id == "gemini_tts":
						pcm_path = os.path.join(temp_dir, f"block_{i:04d}.pcm")
						try:
							pcm_bytes = live_tts.generate(text, abort_checker=lambda: self.abort)
						except LiveTTSAborted:
							return
						if pcm_bytes:
							with open(pcm_path, "wb") as pf:
								pf.write(pcm_bytes)
							subprocess.run(
								[
									ffmpeg_path,
									"-y",
									"-f",
									"s16le",
									"-ar",
									"24000",
									"-ac",
									"1",
									"-i",
									pcm_path,
									wav_path,
								],
								capture_output=True,
								creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
							)
							if os.path.exists(wav_path):
								success = True

					if success:
						cache_path = os.path.join(self.cache_dir, f"cache_{hash(cache_key)}.wav")
						try:
							if not os.path.isdir(self.cache_dir):
								os.makedirs(self.cache_dir, exist_ok=True)
							if os.path.abspath(wav_path) != os.path.abspath(cache_path):
								shutil.copy2(wav_path, cache_path)
							self._gemini_tts_cache[cache_key] = cache_path
						except Exception as e:
							log.debug(f"TTS cache write skipped: {e}")

				if success:
					resampled_wav = os.path.join(temp_dir, f"block_{i:04d}_r.wav")

					available_ms = block["end_ms"] - block["start_ms"]
					if i + 1 < len(blocks):
						gap = blocks[i + 1]["start_ms"] - block["end_ms"]
						if gap > 0:
							available_ms += gap

					target_dur_sec = available_ms / 1000.0
					actual_dur_sec = self._get_wav_duration(wav_path)

					af_filter = []

					cmd = (
						[ffmpeg_path, "-y", "-i", wav_path]
						+ af_filter
						+ ["-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", resampled_wav]
					)

					subprocess.run(
						cmd,
						capture_output=True,
						creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
					)

					if os.path.exists(resampled_wav):
						block["wav_path"] = resampled_wav
					else:
						block["wav_path"] = wav_path
				else:
					block["wav_path"] = None
					tts_failed += 1

				if tts_attempted > 0 and tts_failed == tts_attempted:
					wx.CallAfter(
						show_error_dialog,
						_(
							# Translators: Error message when the selected narration voice produced no audio for any subtitle block.
							"The selected voice could not generate any narration. Make sure the voice is available (for eSpeak, download eSpeak-NG first) and try again.",
						),
					)
					return
				if tts_failed > 0:
					log.warning(
						"Synced narration: {failed} of {total} subtitle blocks failed TTS and were skipped (voice={voice_id}).".format(
							failed=tts_failed,
							total=tts_attempted,
							voice_id=voice_id,
						),
					)
					core.callLater(
						0,
						self.update_status,
						_(
							# Translators: Status warning when some subtitle blocks could not be narrated. {failed} is the number of failed blocks, {total} is the total number of blocks.
							"Warning: {failed} of {total} subtitle blocks could not be narrated and were skipped.",
						).format(failed=tts_failed, total=tts_attempted),
					)

			final_wav_path = os.path.join(temp_dir, "final_mix.wav")

			if mode_selection == 0:
				# Translators: Status message when combining audio blocks
				core.callLater(0, self.update_status, _("Arranging audio track... Please wait."))

				tts_base_path = os.path.join(temp_dir, "tts_base.wav")
				final_end_s = total_orig_ms / 1000.0
				subprocess.run(
					[
						ffmpeg_path,
						"-y",
						"-f",
						"lavfi",
						"-t",
						str(final_end_s),
						"-i",
						"anullsrc=r=24000:cl=mono",
						"-ar",
						"24000",
						"-ac",
						"1",
						tts_base_path,
					],
					capture_output=True,
					creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
				)

				wav_entries = []
				last_end_ms = 0
				for i, block in enumerate(blocks):
					w_path = block.get("wav_path")
					if w_path and os.path.exists(w_path):
						try:
							with wave.open(w_path, "rb") as wf:
								dur_ms = int((wf.getnframes() / wf.getframerate()) * 1000)
						except Exception:
							dur_ms = 0

						start_ms = int(block["start_ms"])
						if start_ms < last_end_ms:
							start_ms = last_end_ms + 150

						wav_entries.append({"path": w_path, "start_ms": start_ms})
						last_end_ms = start_ms + dur_ms

				current_tts_mix = tts_base_path
				batch_size = 40
				for batch_start in range(0, len(wav_entries), batch_size):
					batch = wav_entries[batch_start : batch_start + batch_size]
					batch_out = os.path.join(temp_dir, f"tts_mix_{batch_start}.wav")

					cmd = [ffmpeg_path, "-y", "-i", current_tts_mix]
					filter_parts = []

					for idx, entry in enumerate(batch):
						cmd.extend(["-i", entry["path"]])
						delay_ms = int(entry["start_ms"])
						filter_parts.append(f"[{idx + 1}:a]adelay={delay_ms}|{delay_ms}[a{idx + 1}]")

					mix_inputs = "[0:a]" + "".join(f"[a{i + 1}]" for i in range(len(batch)))
					filter_parts.append(
						f"{mix_inputs}amix=inputs={len(batch) + 1}:duration=longest:normalize=0[out]",
					)

					cmd.extend(
						[
							"-filter_complex",
							";".join(filter_parts),
							"-map",
							"[out]",
							"-ar",
							"24000",
							"-ac",
							"1",
							batch_out,
						],
					)
					subprocess.run(
						cmd,
						capture_output=True,
						creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
					)
					current_tts_mix = batch_out

				if has_video:
					# Translators: Status message when mixing generated narration with original video audio
					core.callLater(0, self.update_status, _("Mixing narration with original video audio..."))

					filter_complex = "[0:a][1:a]amix=inputs=2:duration=longest:normalize=0"
					if apply_ducking:
						filter_complex = "[1:a]asplit=2[sc][tts];[0:a][sc]sidechaincompress=threshold=0.05:ratio=5:attack=50:release=1000[bg];[bg][tts]amix=inputs=2:duration=longest:normalize=0"

					subprocess.run(
						[
							ffmpeg_path,
							"-y",
							"-i",
							orig_audio_wav,
							"-i",
							current_tts_mix,
							"-filter_complex",
							filter_complex,
							"-ar",
							"24000",
							"-ac",
							"1",
							final_wav_path,
						],
						capture_output=True,
						creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
					)
				else:
					final_wav_path = current_tts_mix

			else:
				# Translators: Status message when slicing and splicing the audio file with natural pauses.
				core.callLater(0, self.update_status, _("Splicing audio based on natural pauses..."))
				output_bytes = bytearray()
				last_copied_ms = 0

				for block in blocks:
					if self.abort:
						return
					if not block.get("wav_path") or not os.path.exists(block["wav_path"]):
						continue

					raw_start_ms = block["start_ms"]

					smart_start_ms = self._find_best_pause_time(raw_start_ms, silences, max_shift_ms=3000)

					if smart_start_ms > total_orig_ms:
						smart_start_ms = total_orig_ms

					if smart_start_ms < last_copied_ms:
						smart_start_ms = last_copied_ms

					if smart_start_ms > last_copied_ms:
						chunk_bytes = orig_bytes[
							last_copied_ms * orig_bytes_per_ms : smart_start_ms * orig_bytes_per_ms
						]
						output_bytes.extend(chunk_bytes)
						last_copied_ms = smart_start_ms

					with wave.open(block["wav_path"], "rb") as wf_block:
						tts_frames = wf_block.readframes(wf_block.getnframes())
						output_bytes.extend(tts_frames)

				if last_copied_ms < total_orig_ms:
					remaining_bytes = orig_bytes[last_copied_ms * orig_bytes_per_ms :]
					output_bytes.extend(remaining_bytes)

				with wave.open(final_wav_path, "wb") as wf_out:
					wf_out.setnchannels(1)
					wf_out.setsampwidth(2)
					wf_out.setframerate(24000)
					wf_out.writeframes(output_bytes)

			# Translators: Status message shown when converting the final raw WAV mix to MP3 format.
			core.callLater(0, self.update_status, _("Converting final audio to MP3..."))
			subprocess.run(
				[
					ffmpeg_path,
					"-y",
					"-i",
					final_wav_path,
					"-ac",
					"2",
					"-codec:a",
					"libmp3lame",
					"-q:a",
					"2",
					output_path,
				],
				capture_output=True,
				creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
			)

			if os.path.exists(output_path):
				core.callLater(0, self.update_status, self.srt_content)
				# Translators: Spoken status message when synced extended audio narration is saved successfully.
				saved_msg = _("Synced extended narration with silence detection saved successfully.")
				plugin_state.speak_status(saved_msg)
				wx.CallAfter(
					wx.MessageBox,
					_(
						# Translators: Message spoken on successful save of the synced narration.
						"Synced extended audio narration file generated successfully with smart silence matching.",
					),
					_("Success"),
					wx.OK | wx.ICON_INFORMATION,
				)
			else:
				# Translators: Error message shown when the final MP3 conversion fails.
				wx.CallAfter(show_error_dialog, _("Failed to generate the final MP3 file."))

		except Exception as e:
			log.error(f"Synced narration insertion failed: {e}", exc_info=True)
			# Translators: Error message shown when narration generation fails.
			wx.CallAfter(show_error_dialog, _("Narration Error: {error}").format(error=e))
		finally:
			if "live_tts" in locals() and live_tts:
				live_tts.close()
			try:
				comtypes.CoUninitialize()
			except Exception:
				pass
			try:
				shutil.rmtree(temp_dir, ignore_errors=True)
			except Exception:
				pass
			wx.CallAfter(self.btn_generate_mp3.Enable)
			wx.CallAfter(self.btn_regenerate.Enable)
			wx.CallAfter(self.btn_save.Enable)
			wx.CallAfter(self.voice_sel.Enable)
			wx.CallAfter(self._update_variant_visibility)

	def on_close(self, event):
		self.abort = True
		t = getattr(self, "_tts_thread", None)
		if t and t.is_alive():
			t.join(3)
		if plugin_state.plugin_instance:
			plugin_state.plugin_instance.current_status = _("Idle")
		# Translators: Message announced when user cancels the process
		ui.message(_("Process cancelled."))
		shutil.rmtree(getattr(self, "cache_dir", ""), ignore_errors=True)
		self.Destroy()
