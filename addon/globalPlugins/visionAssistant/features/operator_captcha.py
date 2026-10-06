# -*- coding: utf-8 -*-
import wx
import json
import logging
import time
import re
import random
import ast
import threading
import ctypes

import addonHandler
import ui
import speech
import core
import api
import tones
import scriptHandler
import gui
import config as nvda_config
import controlTypes
import winUser
import keyboardHandler
import mouseHandler

from .. import vision_config
from ..vision_config import ADDON_NAME
from ..prompt_utils import apply_prompt_template, get_prompt_text
from ..ai.core import AIHandler, is_ai_error, ai_error_message
from ..utils.system import (
	clean_markdown,
	show_error_dialog,
	_generate_object_signature,
	check_screen_curtain_active,
	desktop_protection_reason,
	clean_json_fence,
)
from ..utils.mouse_keyboard import MouseSimulator
from ..dialogs.chat_dialog import VisionQADialog

log = logging.getLogger(__name__)

addonHandler.initTranslation()


_UI_ELEMENT_FILLER_STATES = frozenset(
	{
		"enabled",
		"focused",
		"available",
		"normal",
		"visible",
		"active",
		"valid",
		"ready",
		"default",
	},
)


def _read_ui_element_label(raw_label):
	text = (raw_label or "").strip()
	if not text:
		return ""
	type_match = re.match(r"^\[([^\[\]]{1,40})\]\s*(.*)$", text, re.DOTALL)
	element_type = type_match.group(1).strip() if type_match else ""
	rest = type_match.group(2).strip() if type_match else text
	state = ""
	state_match = re.search(r"\(([^()]{1,40})\)\s*$", rest, re.DOTALL)
	if state_match:
		state = state_match.group(1).strip()
		rest = rest[: state_match.start()].strip()
	if state and state.casefold() in _UI_ELEMENT_FILLER_STATES:
		state = ""
	head = ("[%s] %s" % (element_type, rest)) if element_type else rest
	head = head.strip()
	if not head:
		return text
	if not state:
		return head
	return "%s (%s)" % (head, state)


class OperatorCaptchaMixin:
	# Translators: Script description for 'Shows a list of available commands in the layer.' in Input Gestures dialog.
	@scriptHandler.script(description=_("Toggles the interactive UI elements explorer."), category=ADDON_NAME)
	def script_toggleUIExplorer(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		if not self.is_ui_explorer_active:
			self.is_ui_explorer_active = True
			# Translators: Status message when UI Explorer starts
			self.report_status(_("UI Explorer Active"))
			wx.CallLater(100, lambda: threading.Thread(target=self._thread_ui_explorer, daemon=True).start())
		else:
			self.is_ui_explorer_active = False
			# Translators: Status message when UI Explorer stops
			self.report_status(_("UI Explorer Stopped"))
			tones.beep(200, 100)

	def _thread_ui_explorer(self):
		try:
			if not self.is_ui_explorer_active:
				return
			if check_screen_curtain_active():
				self.is_ui_explorer_active = False
				return
			time.sleep(0.5)
			img, w, h, m = self._capture_fullscreen_sync()
			if not img:
				self.is_ui_explorer_active = False
				return
			tones.beep(800, 50)
			fg_app = self._get_fg_app_name_sync()
			prompt_template = get_prompt_text("ui_explorer_system")
			prompt = apply_prompt_template(prompt_template, [("app_name", fg_app)])
			res = AIHandler.call(
				prompt,
				attachments=[{"mime_type": m, "data": img}],
				json_mode=True,
				task="operator",
			)
			if not self.is_ui_explorer_active:
				return
			if not res or is_ai_error(res):
				self.is_ui_explorer_active = False
				# Translators: Generic error message for AI failures
				err_msg = ai_error_message(res) if res else _("Unknown AI Error")
				wx.CallAfter(show_error_dialog, err_msg)
				return
			try:
				clean_res = clean_json_fence(res)

				clean_res = re.sub(r"\}\s*\{", "}, {", clean_res)
				elements = []
				try:
					elements = json.loads(clean_res)
				except Exception:
					try:
						elements = ast.literal_eval(clean_res)
					except Exception:
						for match in re.finditer(r"\{[^{}]*\}", clean_res):
							obj_str = match.group(0)
							lbl_match = re.search(r'"label"\s*:\s*"([^"]+)"', obj_str)
							x_match = re.search(r'"x"\s*:\s*(\d+)', obj_str)
							y_match = re.search(r'"y"\s*:\s*(\d+)', obj_str)
							if lbl_match and x_match and y_match:
								elements.append(
									{
										"label": lbl_match.group(1),
										"x": int(x_match.group(1)),
										"y": int(y_match.group(1)),
									},
								)
				if not elements:
					raise ValueError("JSON failed")
				tones.beep(1000, 100)
				wx.CallAfter(self._show_elements_selector, elements, w, h)
			except Exception as e:
				log.error(f"UI Explorer parsing failed: {e}")
				if self.is_ui_explorer_active:
					self.is_ui_explorer_active = False
					# Translators: Error shown when AI fails to find UI elements
					wx.CallAfter(show_error_dialog, _("AI failed to identify UI elements."))
		except Exception as e:
			log.error(f"UI Explorer thread failed: {e}")
			self.is_ui_explorer_active = False

	def _show_elements_selector(self, elements, sw, sh):
		if not self.is_ui_explorer_active:
			return
		choices, valid_elements = [], []
		seen = set()
		for el in elements:
			label = el.get("label", "").strip()
			if not label or label in seen:
				continue
			seen.add(label)
			choices.append(_read_ui_element_label(label))
			valid_elements.append(el)
		if not choices:
			self.is_ui_explorer_active = False
			return
		from ..dialogs.ui_elements import UIExplorerDialog

		gui.mainFrame.prePopup()
		try:
			dlg = UIExplorerDialog(gui.mainFrame, choices, valid_elements, sw, sh, self)
			dlg.ShowModal()
			action_taken = dlg.action_taken
		finally:
			gui.mainFrame.postPopup()
		if not action_taken:
			self.is_ui_explorer_active = False
			self.report_status(_("UI Explorer Stopped"))
		dlg.Destroy()

	@scriptHandler.script(
		description=_("Asks the AI Operator to perform an action or describe the screen."),
		category=ADDON_NAME,
	)
	def script_aiOperatorAction(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		if getattr(self, "_is_operator_running", False):
			self._abort_operator = True
			self._operator_thread_token = getattr(self, "_operator_thread_token", 0) + 1
			self._is_operator_running = False
			# Translators: Announcement when the AI Operator is manually stopped
			ui.message(_("AI Operator stopped."))
			tones.beep(300, 150)
			return
		if getattr(self, "_dialog_open", False):
			return
		if check_screen_curtain_active():
			return
		if desktop_protection_reason():
			ui.message(_("Secure mode, locked desktop or screen curtain is active."))
			tones.beep(220, 150)
			return

		def show_cmd_dialog():
			self._dialog_open = True
			try:
				gui.mainFrame.prePopup()
				# Translators: Prompt message asking what the AI Operator should do
				op_prompt = _("What should I do or what is your question?")
				# Translators: Title of the AI Operator command dialog
				op_title = _("AI Operator")
				dlg = wx.TextEntryDialog(
					gui.mainFrame,
					op_prompt,
					op_title,
				)
				if dlg.ShowModal() == wx.ID_OK:
					command = dlg.GetValue()
					dlg.Destroy()
					gui.mainFrame.postPopup()
					self._dialog_open = False
					time.sleep(0.5)
					if command.strip():
						self._operator_history = []
						self._operator_extra_info = {}
						# Translators: Message while processing request of the refine text command
						wx.CallLater(300, self.report_status, _("Processing..."))
						self._operator_thread_token = getattr(self, "_operator_thread_token", 0) + 1
						token = self._operator_thread_token
						wx.CallLater(
							800,
							lambda: threading.Thread(
								target=self._thread_ai_computer_use,
								args=(command, token),
								daemon=True,
							).start(),
						)
					return
				dlg.Destroy()
				gui.mainFrame.postPopup()
			finally:
				self._dialog_open = False

		wx.CallAfter(show_cmd_dialog)

	def _wait_for_operator_speech(self, text, token, min_delay=0.4, extra_buffer=0.25):
		for _ in range(int(min_delay * 10)):
			if self._should_abort(token):
				return
			time.sleep(0.1)

		clean = clean_markdown(text or "")
		max_wait = max(4.0, len(clean) * 0.12 + 2.0)
		start_time = time.time()
		while time.time() - start_time < max_wait:
			if self._should_abort(token):
				return
			try:
				if not speech.isSpeaking():
					break
			except Exception:
				break
			time.sleep(0.1)

		for _ in range(int(extra_buffer * 10)):
			if self._should_abort(token):
				return
			time.sleep(0.1)

	def _thread_ai_computer_use(self, user_command, token):
		self._abort_operator = False
		self._is_operator_running = True
		try:
			max_turns = 10
			current_command = user_command
			if not self._operator_history:
				self._operator_history = []
			resp_lang = vision_config.get_lang_name("ai_response_language")
			fg_app = self._get_fg_app_name_sync()
			is_gemini = AIHandler.is_gemini()
			for turn in range(max_turns):
				if self._should_abort(token):
					break

				if desktop_protection_reason():
					core.callLater(
						0, ui.message, _("Secure mode, locked desktop or screen curtain is active.")
					)
					break

				if turn > 0:
					for i in range(35):
						if self._should_abort(token):
							break
						time.sleep(0.1)
					if self._should_abort(token):
						break

				time.sleep(0.5)
				if self._should_abort(token):
					break

				img, w, h, m = self._capture_fullscreen_sync()
				if not img:
					break
				if self._should_abort(token):
					break

				tones.beep(800, 50)
				system_template = get_prompt_text("ai_operator_system")
				prompt = apply_prompt_template(
					system_template,
					[("user_command", current_command), ("response_lang", resp_lang), ("app_name", fg_app)],
				)

				messages = []
				for item in self._operator_history:
					role = item["role"]
					content = item.get("content") or ""
					if "{" in content and "explanation" in content:
						try:
							exp_match = re.search(r'"explanation":\s*"([^"]*)"', content)
							if exp_match:
								content = exp_match.group(1)
						except Exception as e:
							log.debug(f"Explanation extraction failed: {e}")
					if is_gemini:
						messages.append(
							{"role": "user" if role == "user" else "model", "parts": [{"text": content}]},
						)
					else:
						messages.append(
							{"role": role if role != "model" else "assistant", "content": content},
						)

				if is_gemini:
					messages.append(
						{
							"role": "user",
							"parts": [{"text": prompt}, {"inline_data": {"mime_type": m, "data": img}}],
						},
					)
				else:
					messages.append(
						{
							"role": "user",
							"content": [
								{"type": "text", "text": prompt},
								{"type": "image_url", "image_url": {"url": f"data:{m};base64,{img}"}},
							],
						},
					)

				res = AIHandler.call(messages, task="operator")
				if self._should_abort(token):
					break

				if not res or is_ai_error(res):
					# Translators: Error message shown when the AI returns an unknown error
					wx.CallAfter(show_error_dialog, ai_error_message(res) if res else _("AI Error"))
					break

				display_text, is_finished, action_info = self._process_ai_action_logic(res, w, h)

				# Translators: Internal history label for user actions in operator sessions
				hist_user = current_command if turn == 0 else _("Action performed. Checking result...")
				self._operator_history.append({"role": "user", "content": hist_user})
				self._operator_history.append({"role": "assistant", "content": res})

				if not self._should_abort(token):
					self._last_result_data = (
						self._open_operator_chat_dialog,
						(display_text, {"last_w": w, "last_h": h}),
					)
					core.callLater(0, ui.message, clean_markdown(display_text))

				if action_info:
					self._wait_for_operator_speech(display_text, token)
					if self._should_abort(token):
						break

					act, rx, ry, txt_val, p_ent, scroll_dir, keys_val, rsx, rsy = action_info
					if act == "type" and txt_val:
						self._do_type(rx, ry, txt_val, p_ent)
					elif act == "keypress" and keys_val:
						self._do_keypress(keys_val)
					elif act == "scroll":
						self._do_mouse_action(rx, ry, act, scroll_direction=scroll_dir)
					else:
						self._do_mouse_action(rx, ry, act, start_x=rsx, start_y=rsy)
					tones.beep(1000, 100)

				if is_finished or ("{" not in res and not action_info):
					if self._should_abort(token):
						break
					if nvda_config.conf["VisionAssistant"]["copy_to_clipboard"]:
						core.callLater(0, api.copyToClip, display_text)
					if not nvda_config.conf["VisionAssistant"]["skip_chat_dialog"]:
						self._wait_for_operator_speech(display_text, token)
						if not self._should_abort(token):
							wx.CallAfter(
								self._open_operator_chat_dialog,
								display_text,
								{"last_w": w, "last_h": h},
							)
					break

				if self._should_abort(token):
					break
				time.sleep(2.5)
				current_command = "The action was initiated. Continue if necessary."
		except Exception as e:
			log.error(f"AI Computer Use thread failed: {e}", exc_info=True)
		finally:
			if getattr(self, "_operator_thread_token", 0) == token:
				self._is_operator_running = False
				self._abort_operator = False
			# Translators: Error message shown when uploading a video file fails.
			self.current_status = _("Idle")

	def _open_operator_chat_dialog(self, text, context, force_show=False, is_recall=False):
		self._last_result_data = (self._open_operator_chat_dialog, (text, context))
		if nvda_config.conf["VisionAssistant"]["skip_chat_dialog"] and not force_show:
			return
		if self.vision_dlg:
			try:
				self.vision_dlg.Destroy()
			except Exception as e:
				log.warning(f"Destroy vision dlg failed: {e}")
			self.vision_dlg = None

		def operator_callback(ctx, q, history, extra):
			self._operator_history = []
			for h in history:
				role = "user" if h["role"] == "user" else "assistant"
				text_val = h.get("content") or (
					h.get("parts", [{}])[0].get("text", "") if h.get("parts") else ""
				)
				if text_val and text_val != q:
					self._operator_history.append({"role": role, "content": text_val})

			wx.CallAfter(self.vision_dlg.Close)
			self._operator_thread_token = getattr(self, "_operator_thread_token", 0) + 1
			token = self._operator_thread_token
			threading.Thread(target=self._thread_ai_computer_use, args=(q, token), daemon=True).start()
			return None, None

		if not is_recall:
			tones.beep(1000, 100)

		# Translators: The title of the interactive chat dialog for the AI Operator feature.
		title_text = _("{name} - AI Operator").format(name=vision_config.ADDON_NAME)

		if not isinstance(getattr(self, "_operator_extra_info", None), dict):
			self._operator_extra_info = {}

		self.vision_dlg = VisionQADialog(
			gui.mainFrame,
			title_text,
			text,
			context,
			operator_callback,
			extra_info=self._operator_extra_info,
			status_callback=self.report_status,
		)

		if self._operator_history:
			dialog_history = []
			self.vision_dlg.outputArea.Clear()
			self.vision_dlg._nav_messages = []
			self.vision_dlg._nav_index = -1
			for h in self._operator_history:
				role = "user" if h["role"] == "user" else "model"
				content = h.get("content") or h.get("parts", [{}])[0].get("text", "")
				dialog_history.append({"role": role, "parts": [{"text": content}]})
				# Translators: Label for the AI operator role in chat history
				label_ai = _("Operator")
				# Translators: Label for the user role in chat history
				label_user = _("You")
				role_label = label_ai if h["role"] in ["assistant", "model"] else label_user
				content_only = ""
				try:
					if "{" in content:
						json_match = re.search(r"\{.*\}", content, flags=re.DOTALL)
						if json_match:
							content_only = json.loads(json_match.group(0)).get("explanation", "")
				except Exception as e:
					log.debug(f"Captcha JSON parse failed: {e}")
				if not content_only:
					content_only = re.sub(r"\{.*\}", "", content, flags=re.DOTALL).strip()
				if "Windows operator" not in content and content_only:
					cleaned = clean_markdown(content_only)
					self.vision_dlg.outputArea.AppendText(f"{role_label}: {cleaned}\n\n")
					self.vision_dlg._add_nav_message(cleaned, role)
			self.vision_dlg.chat_history = dialog_history

		self.vision_dlg.Show()
		self.vision_dlg.Raise()
		self.vision_dlg.SetFocus()

	def _process_ai_action_logic(self, res, sw, sh):
		is_finished = False
		action_info = None
		clean_text = res
		exp_match = re.search(r'"explanation":\s*"([^"]*)"', res)
		if exp_match:
			clean_text = exp_match.group(1)
		else:
			clean_text = re.sub(r"\{.*\}", "", res, flags=re.DOTALL).strip()
			if not clean_text:
				clean_text = res

		try:
			start_idx = res.find("{")
			end_idx = res.rfind("}")
			if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
				json_str = res[start_idx : end_idx + 1].replace("\n", " ")
				try:
					data = json.loads(json_str)
					x = data.get("x") if data.get("x") is not None else data.get("end_x")
					y = data.get("y") if data.get("y") is not None else data.get("end_y")
					start_x, start_y = data.get("start_x"), data.get("start_y")
					action = data.get("action", "click")
					is_finished = data.get("finished", False)
					explanation = data.get("explanation", clean_text)
					t_val = data.get("text", "")
					scroll_dir = data.get("scroll_direction", "down")
					keys_val = data.get("keys", "")
				except Exception:
					x_m = re.search(r'"(?:end_)?x":\s*(\d+)', json_str)
					y_m = re.search(r'"(?:end_)?y":\s*(\d+)', json_str)
					sx_m = re.search(r'"start_x":\s*(\d+)', json_str)
					sy_m = re.search(r'"start_y":\s*(\d+)', json_str)
					x = int(x_m.group(1)) if x_m else None
					y = int(y_m.group(1)) if y_m else None
					start_x = int(sx_m.group(1)) if sx_m else None
					start_y = int(sy_m.group(1)) if sy_m else None
					action = "click"
					act_m = re.search(r'"action":\s*"([^"]*)"', json_str)
					if act_m:
						action = act_m.group(1)
					is_finished = bool(re.search(r'"finished":\s*true', json_str.lower()))
					explanation = clean_text
					t_m = re.search(r'"text":\s*"([^"]*)"', json_str)
					t_val = t_m.group(1) if t_m else ""
					scroll_dir = "down"
					keys_val = ""

				if x is not None and y is not None:
					real_x, real_y = int(x * sw / 1000), int(y * sh / 1000)
					real_start_x = int(start_x * sw / 1000) if start_x is not None else None
					real_start_y = int(start_y * sh / 1000) if start_y is not None else None
					p_ent = t_val.endswith("\n") or "اینتر" in explanation or "enter" in explanation.lower()
					action_info = (
						action,
						real_x,
						real_y,
						t_val,
						p_ent,
						scroll_dir,
						keys_val,
						real_start_x,
						real_start_y,
					)

				return explanation, is_finished, action_info
			else:
				return clean_text, True, None
		except Exception:
			return clean_text, True, None

	def _do_mouse_action(self, x, y, action_type, scroll_direction="down", start_x=None, start_y=None):
		try:
			sw, sh = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
			x = max(0, min(sw - 1, int(x)))
			y = max(0, min(sh - 1, int(y)))
			if start_x is not None:
				start_x = max(0, min(sw - 1, int(start_x)))
			if start_y is not None:
				start_y = max(0, min(sh - 1, int(start_y)))
			if action_type == "scroll":
				MouseSimulator.scroll(x, y, direction=scroll_direction, clicks=3)
			elif action_type == "drag":
				if start_x is None or start_y is None:
					start_x, start_y = x, y
				MouseSimulator.drag(start_x, start_y, x, y, duration=0.8, steps=40)
			elif action_type == "right_click":
				MouseSimulator.click(x, y, button="right")
			elif action_type == "double_click":
				MouseSimulator.click(x, y, button="left", double=True)
			else:
				MouseSimulator.click(x, y, button="left")
			time.sleep(0.2)
		except Exception as e:
			log.error(f"Mouse action failed: {e}", exc_info=True)
			try:
				winUser.setCursorPos(int(x), int(y))
				time.sleep(0.1)
				core.callLater(0, mouseHandler.doPrimaryClick)
			except Exception as e2:
				log.error(f"Mouse fallback also failed: {e2}")

	def _do_keypress(self, key_name):
		VK_MAP = {
			"enter": 0x0D,
			"return": 0x0D,
			"tab": 0x09,
			"escape": 0x1B,
			"esc": 0x1B,
			"up": 0x26,
			"down": 0x28,
			"left": 0x25,
			"right": 0x27,
			"space": 0x20,
			"backspace": 0x08,
			"delete": 0x2E,
			"home": 0x24,
			"end": 0x23,
			"pageup": 0x21,
			"pagedown": 0x22,
			"insert": 0x2D,
			"f1": 0x70,
			"f2": 0x71,
			"f3": 0x72,
			"f4": 0x73,
			"f5": 0x74,
			"f6": 0x75,
			"f7": 0x76,
			"f8": 0x77,
			"f9": 0x78,
			"f10": 0x79,
			"f11": 0x7A,
			"f12": 0x7B,
		}
		EXTENDED_KEYS = {
			"up",
			"down",
			"left",
			"right",
			"home",
			"end",
			"pageup",
			"pagedown",
			"insert",
			"delete",
		}
		key_lower = str(key_name).lower()
		vk = VK_MAP.get(key_lower)
		if vk:
			extended = key_lower in EXTENDED_KEYS
			MouseSimulator.key_press(vk, extended=extended)
			time.sleep(0.15)
		else:
			log.warning(f"Unknown key name: {key_name}")

	def _do_type(self, x, y, text, press_enter=False):
		try:
			MouseSimulator.click(x, y, button="left")
			time.sleep(0.3)
			VK_CONTROL, VK_A = 0x11, 0x41
			inputs = [
				MouseSimulator._make_keyboard_input(VK_CONTROL, 0),
				MouseSimulator._make_keyboard_input(VK_A, 0),
				MouseSimulator._make_keyboard_input(VK_A, 2),
				MouseSimulator._make_keyboard_input(VK_CONTROL, 2),
			]
			MouseSimulator._send_inputs(*inputs)
			time.sleep(0.1)
			MouseSimulator.key_press(0x2E)
			time.sleep(0.1)
			MouseSimulator.type_text(text, press_enter=press_enter)
		except Exception as e:
			log.error(f"Type action failed: {e}", exc_info=True)

	def _should_abort(self, token):
		return getattr(self, "_abort_operator", False) or token != getattr(self, "_operator_thread_token", 0)

	# Translators: Script description for 'Labels the current navigator object using AI.' in Input Gestures dialog.
	@scriptHandler.script(description=_("Labels the current navigator object using AI."), category=ADDON_NAME)
	def script_labelObject(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		obj = api.getNavigatorObject()
		if not obj or not obj.location:
			return
		if check_screen_curtain_active():
			return

		uniqueId = self._getAppId(obj)
		if uniqueId in ["chrome", "msedge", "firefox", "opera", "brave"]:
			# Translators: Message shown when a user tries to use AI labeling in a web browser.
			ui.message(_("AI Labeling is currently not supported in web browsers."))
			return

		loc = obj.location
		sig_key = _generate_object_signature(obj)
		old_key = f"{int(obj.role)}:{loc.left},{loc.top}" if loc else None

		is_labeled = False
		found_label = ""
		if uniqueId in self.labels_cache:
			if sig_key and sig_key in self.labels_cache[uniqueId]:
				is_labeled = True
				found_label = self.labels_cache[uniqueId][sig_key]
			elif old_key and old_key in self.labels_cache[uniqueId]:
				is_labeled = True
				found_label = self.labels_cache[uniqueId][old_key]

		if is_labeled:
			# Translators: Message spoken by NVDA when the current object already has a custom or AI-generated label. {name} is replaced with the existing label text.
			ui.message(_("Already labeled as: {name}").format(name=found_label))
			return

		tones.beep(800, 100)
		# Translators: Progress message spoken when the add-on starts taking a screenshot of the current focused object.
		self.current_status = _("Identifying object...")
		ui.message(self.current_status)

		img, w, h, m = self._capture_navigator()

		def worker():
			try:
				if not img:
					self.current_status = _("Idle")
					return
				self.current_status = _("Analyzing...")
				core.callLater(0, ui.message, self.current_status)

				resp_lang = vision_config.get_lang_name("ai_response_language")
				prompt_template = get_prompt_text("label_single_system")
				prompt = apply_prompt_template(
					prompt_template,
					[("app_name", uniqueId), ("response_lang", resp_lang)],
				)

				res = AIHandler.call(prompt, attachments=[{"mime_type": m, "data": img}], task="operator")
				if res and not is_ai_error(res):
					clean_name = clean_markdown(res)

					def save_ui_thread():
						if uniqueId not in self.labels_cache:
							self.labels_cache[uniqueId] = {}
						sig_key2 = _generate_object_signature(obj)
						if sig_key2:
							self.labels_cache[uniqueId][sig_key2] = clean_name
							self._save_all_labels()
							tones.beep(1000, 100)
							# Translators: Success message spoken when the AI successfully assigns a new label to the object. {name} is replaced with the AI-generated label.
							ui.message(_("Labeled as: {name}").format(name=clean_name))

					wx.CallAfter(save_ui_thread)
				elif res and is_ai_error(res):
					wx.CallAfter(show_error_dialog, ai_error_message(res))
			except Exception as e:
				log.error(f"Single label thread failed: {e}")
			finally:
				self.current_status = _("Idle")

		threading.Thread(target=worker, daemon=True).start()

	@scriptHandler.script(
		# Translators: Script description for 'Manages existing labels or scans the entire app to label unnamed elements.' in Input Gestures dialog.
		description=_("Manages existing labels or scans the entire app to label unnamed elements."),
		category=ADDON_NAME,
	)
	def script_manageOrScanApp(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		obj = api.getFocusObject()
		try:
			app_name = obj.appModule.appName.lower()
		except Exception:
			app_name = "unknown"
		if app_name in ["chrome", "msedge", "firefox", "opera", "brave"]:
			ui.message(_("AI Labeling is currently not supported in web browsers."))
			return
		uniqueId = self._getAppId(obj)

		if uniqueId in self.labels_cache and self.labels_cache[uniqueId]:

			def show_manager():
				import gui
				from ..dialogs.ui_elements import LabelManagerDialog

				gui.mainFrame.prePopup()
				try:
					dlg = LabelManagerDialog(gui.mainFrame, uniqueId, self.labels_cache[uniqueId])
					if dlg.ShowModal() == wx.ID_OK:
						if dlg.action_type == "delete":
							for k in dlg.target_keys:
								del self.labels_cache[uniqueId][k]
						elif dlg.action_type == "rename":
							self.labels_cache[uniqueId][dlg.target_keys[0]] = dlg.new_name
						elif dlg.action_type == "rescan":
							wx.CallLater(600, self._batchLabelApp, uniqueId)

						if dlg.action_type in ["delete", "rename"]:
							self._save_all_labels()
							# Translators: Confirmation message shown after labels are deleted or renamed.
							ui.message(_("Labels updated."))
				finally:
					gui.mainFrame.postPopup()
				dlg.Destroy()

			wx.CallAfter(show_manager)
		else:
			wx.CallLater(400, self._batchLabelApp, uniqueId)

	def _save_all_labels(self):
		try:
			with open(vision_config.LABELS_FILE, "w", encoding="utf-8") as f:
				json.dump(self.labels_cache, f, ensure_ascii=False, indent=4)
		except Exception as e:
			log.warning(f"Save labels failed: {e}")

	def _batchLabelApp(self, unique_id):
		if check_screen_curtain_active():
			return
		tones.beep(800, 100)
		# Translators: Progress message spoken when the add-on begins scanning the current application window to find UI elements (like buttons or icons) that do not have accessibility names.
		self.current_status = _("Scanning application UI...")
		ui.message(self.current_status)

		root = api.getForegroundObject()
		candidates = []
		stack = [(root, 0)]
		target_roles = {
			controlTypes.Role.BUTTON,
			controlTypes.Role.TOGGLEBUTTON,
			controlTypes.Role.CHECKBOX,
			controlTypes.Role.RADIOBUTTON,
			controlTypes.Role.MENUITEM,
			controlTypes.Role.LINK,
			controlTypes.Role.TAB,
			controlTypes.Role.DATAITEM,
			controlTypes.Role.LISTITEM,
			controlTypes.Role.COMBOBOX,
			controlTypes.Role.GRAPHIC,
			controlTypes.Role.ICON,
			controlTypes.Role.TABLECELL,
		}

		while stack and len(candidates) < 1500:
			obj, depth = stack.pop()
			if depth > 25:
				continue
			try:
				role = obj.role
				loc = obj.location
				name = obj.name
				if loc and role in target_roles and (not name or not name.strip()):
					candidates.append(obj)
				child = obj.firstChild
				while child:
					stack.append((child, depth + 1))
					child = child.next
			except Exception as e:
				log.debug(f"Object tree traversal skipped: {e}")
				continue

		if not candidates:
			self.current_status = _("Idle")
			# Translators: Message spoken when the add-on finishes the UI scan but finds no unnamed elements to label (everything already has a name).
			ui.message(_("No unnamed elements found."))
			return

		# Translators: Progress message spoken when the add-on has found unnamed elements and is now sending the full application screenshot to AI for batch labeling.
		self.current_status = _("Analyzing application...")
		ui.message(self.current_status)
		img, w, h, m = self._capture_fullscreen()

		def worker():
			try:
				prompt_template = get_prompt_text("label_batch_system")
				prompt = apply_prompt_template(
					prompt_template,
					[
						("app_name", unique_id),
						("response_lang", vision_config.get_lang_name("ai_response_language")),
					],
				)
				res = AIHandler.call(
					prompt,
					attachments=[{"mime_type": m, "data": img}],
					json_mode=True,
					task="operator",
				)

				if res and not is_ai_error(res):
					try:
						raw_res = res.strip()
						start_idx = raw_res.find("[")
						end_idx = raw_res.rfind("]")
						clean_json = (
							raw_res[start_idx : end_idx + 1]
							if (start_idx != -1 and end_idx != -1)
							else raw_res
						)
						clean_json = re.sub(r"\}\s*\{", "}, {", clean_json)
						ai_items = []
						try:
							ai_items = json.loads(clean_json)
						except Exception:
							try:
								ai_items = ast.literal_eval(clean_json)
							except Exception:
								for match in re.finditer(r"\{[^{}]*\}", clean_json):
									obj_str = match.group(0)
									lbl_match, x_match, y_match = (
										re.search(r'"label"\s*:\s*"([^"]+)"', obj_str),
										re.search(r'"x"\s*:\s*(\d+)', obj_str),
										re.search(r'"y"\s*:\s*(\d+)', obj_str),
									)
									if lbl_match and x_match and y_match:
										ai_items.append(
											{
												"label": lbl_match.group(1),
												"x": int(x_match.group(1)),
												"y": int(y_match.group(1)),
											},
										)

						def save_batch_ui_thread():
							if unique_id not in self.labels_cache:
								self.labels_cache[unique_id] = {}
							for item in ai_items:
								if not all(k in item for k in ("x", "y", "label")):
									continue
								try:
									x_val, y_val = float(item["x"]), float(item["y"])
								except Exception as e:
									log.debug(f"Label coordinate parse skipped: {e}")
									continue

								ai_x, ai_y = int(x_val * w / 1000), int(y_val * h / 1000)
								best_match, min_dist = None, 100
								for cand in candidates:
									c_loc = cand.location
									if not c_loc:
										continue
									cx, cy = c_loc.left + c_loc.width / 2, c_loc.top + c_loc.height / 2
									dist = ((cx - ai_x) ** 2 + (cy - ai_y) ** 2) ** 0.5
									if dist < min_dist:
										min_dist = dist
										best_match = cand
								if best_match:
									sig_key = _generate_object_signature(best_match)
									if sig_key:
										self.labels_cache[unique_id][sig_key] = item["label"]
							self._save_all_labels()
							tones.beep(1000, 100)
							# Translators: Success message spoken when the AI finishes analyzing the app and successfully names multiple elements in the background.
							ui.message(_("Application labeling complete."))

						wx.CallAfter(save_batch_ui_thread)
					except Exception as e:
						log.error(f"Batch labeling mapping failed: {e}")
						# Translators: Error message spoken when the add-on fails to parse or map the labels returned by the AI (e.g., due to invalid AI response format).
						core.callLater(0, ui.message, _("Batch labeling failed."))
				elif res and is_ai_error(res):
					wx.CallAfter(show_error_dialog, ai_error_message(res))
			except Exception as e:
				log.error(f"Batch label worker failed: {e}")
			finally:
				self.current_status = _("Idle")

		threading.Thread(target=worker, daemon=True).start()

	@scriptHandler.script(
		# Translators: Script description for 'Attempts to solve a CAPTCHA on the screen or navigator object.' in Input Gestures dialog.
		description=_("Attempts to solve a CAPTCHA on the screen or navigator object."),
		category=ADDON_NAME,
	)
	def script_solveCaptcha(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		if check_screen_curtain_active():
			return
		if getattr(self, "_is_captcha_running", False):
			self._captcha_run_id = getattr(self, "_captcha_run_id", 0) + 1
			self._is_captcha_running = False
			self.current_status = _("Idle")
			# Translators: Announcement when the visual CAPTCHA solver is manually aborted
			ui.message(_("Visual CAPTCHA solver aborted."))
			tones.beep(300, 150)
			return

		mode = nvda_config.conf["VisionAssistant"]["captcha_mode"]
		if mode == "fullscreen":
			d, w, h, m = self._capture_fullscreen()
		else:
			d, w, h, m = self._capture_navigator()

		is_gov = False
		try:
			if api.getForegroundObject() and "پنجره ملی خدمات دولت هوشمند" in api.getForegroundObject().name:
				is_gov = True
		except Exception as e:
			log.debug(f"Gov window check failed: {e}")

		if d:
			log.info(f"CAPTCHA solving started in mode: {mode}, is_gov={is_gov}")
			# Translators: Message reported by NVDA when the user triggers the CAPTCHA solving command.
			self.report_status(_("Solving..."))
			self._captcha_run_id = getattr(self, "_captcha_run_id", 0) + 1
			self._is_captcha_running = True
			threading.Thread(
				target=self._thread_cap,
				args=(d, m, is_gov, self._captcha_run_id),
				daemon=True,
			).start()
		else:
			log.warning("CAPTCHA solve failed: Image capture returned empty.")
			# Translators: Message reported when image capture fails during CAPTCHA solve.
			self.report_status(_("Capture failed."))

	def _captcha_run_stale(self, run_id):
		return run_id != getattr(self, "_captcha_run_id", 0)

	def _report_captcha_solved(self, run_id):
		if self._captcha_run_stale(run_id):
			return
		# Translators: Message reported when a visual CAPTCHA is successfully solved.
		self.report_status(_("Visual CAPTCHA solved!"))

	def _thread_cap(self, d, m, is_gov, run_id):
		start_visual_loop = False
		try:
			cap_template = get_prompt_text("captcha_solver_base")
			cap_extra = (
				" Read 5 Persian digits, convert to English." if is_gov else " Convert to English digits."
			)
			p = apply_prompt_template(cap_template, [("captcha_extra", cap_extra)])

			log.info("Sending CAPTCHA image to AI Handler...")
			r = AIHandler.call(p, attachments=[{"mime_type": m, "data": d}])
			if self._captcha_run_stale(run_id):
				log.info("CAPTCHA solving aborted by user.")
				return

			if r:
				log.debug(f"CAPTCHA raw AI response: {r}")
				if is_ai_error(r):
					wx.CallAfter(show_error_dialog, ai_error_message(r))
					return
				if "[[[NO_CAPTCHA]]]" in r:
					# Translators: Message reported by NVDA when the AI cannot detect any CAPTCHA in the captured image.
					core.callLater(0, self.report_status, _("No CAPTCHA detected."))
				elif "[[[VISUAL_CAPTCHA]]]" in r:
					if nvda_config.conf["VisionAssistant"].get("enable_visual_captcha_solver", True):
						core.callLater(
							0,
							self.report_status,
							_(
								# Translators: Message reported when a visual CAPTCHA (like reCAPTCHA) is detected.
								"Visual CAPTCHA detected. Entering solving mode... This may take a little while.",
							),
						)
						start_visual_loop = True
						threading.Thread(
							target=self._solve_visual_captcha_loop,
							args=(run_id,),
							daemon=True,
						).start()
					else:
						# Translators: Message reported when a visual CAPTCHA is detected but the solver is disabled.
						disabled_msg = _("Visual CAPTCHA detected, but the solver is disabled in settings.")
						core.callLater(0, self.report_status, disabled_msg)
				else:
					wx.CallAfter(self._finish_captcha, r.strip())
			else:
				# Translators: Message reported when image capture fails or AI returns empty.
				core.callLater(0, self.report_status, _("Capture failed or AI returned empty response."))
		except Exception as e:
			log.error(f"Captcha base error: {e}", exc_info=True)
		finally:
			if not start_visual_loop and not self._captcha_run_stale(run_id):
				self._is_captcha_running = False
				self.current_status = _("Idle")

	def _finish_captcha(self, text):
		clean_text = re.sub(r"[^a-zA-Z0-9]", "", text)
		log.info(f"CAPTCHA solved ({len(clean_text)} chars).")
		log.debug(f"CAPTCHA solved result text: {clean_text}")
		for char in clean_text:
			try:
				keyboardHandler.KeyboardInputGesture.fromName(char).send()
			except Exception:
				vk = winUser.user32.VkKeyScanW(ord(char)) & 0xFF
				winUser.keybd_event(vk, 0, 0, 0)
				winUser.keybd_event(vk, 0, 2, 0)
			time.sleep(0.02)
		tones.beep(1000, 100)
		# Translators: Message reported by NVDA after successfully solving a text CAPTCHA, announcing the characters found.
		msg = _("Captcha: {text}").format(text=clean_text)
		self.report_status(msg)

	def _solve_visual_captcha_loop(self, run_id):
		if self._captcha_run_stale(run_id):
			return
		self._is_captcha_running = True
		max_attempts = 15
		sys_prompt = get_prompt_text("captcha_solver_loop")

		try:
			for attempt in range(max_attempts):
				if self._captcha_run_stale(run_id):
					break
				time.sleep(0.5)
				if self._captcha_run_stale(run_id):
					break

				d, w, h, m = self._capture_fullscreen()
				if not d:
					break

				try:
					res = AIHandler.call(
						sys_prompt,
						attachments=[{"mime_type": m, "data": d}],
						json_mode=True,
						task="operator",
					)
					if self._captcha_run_stale(run_id):
						break
					if not res or is_ai_error(res):
						break

					clean_res = res.strip()
					if "```json" in clean_res:
						clean_res = clean_res.split("```json")[1].split("```")[0].strip()
					elif "```" in clean_res:
						clean_res = clean_res.split("```")[1].split("```")[0].strip()

					try:
						clean_res = re.sub(r'(["\]\}\d]|true|false|null)\s+(?=")', r"\1, ", clean_res)
						data = json.loads(clean_res)
					except Exception:
						start_idx = clean_res.find("{")
						end_idx = clean_res.rfind("}")
						parsed = False
						while end_idx > start_idx:
							try:
								data = json.loads(clean_res[start_idx : end_idx + 1])
								parsed = True
								break
							except Exception:
								end_idx = clean_res.rfind("}", start_idx, end_idx)
						if not parsed:
							raise ValueError("JSON Error")

					action = data.get("action", "")
					if self._captcha_run_stale(run_id):
						break

					if action == "solved":
						core.callLater(0, self._report_captcha_solved, run_id)
						tones.beep(1000, 100)
						break
					elif action == "click":
						pos = data.get("coordinates") or data.get("point")
						if pos:
							ry = int(pos[0] * h / 1000) + random.randint(-7, 7)
							rx = int(pos[1] * w / 1000) + random.randint(-7, 7)
							self._do_mouse_action(rx, ry, "click")
							time.sleep(random.uniform(2.5, 3.5))
					elif action == "drag":
						start_pos = data.get("drag_start")
						end_pos = data.get("drag_end")
						if start_pos and end_pos:
							sry = int(start_pos[0] * h / 1000) + random.randint(-5, 5)
							srx = int(start_pos[1] * w / 1000) + random.randint(-5, 5)
							ery = int(end_pos[0] * h / 1000) + random.randint(-5, 5)
							erx = int(end_pos[1] * w / 1000) + random.randint(-5, 5)
							if abs(srx - erx) > 5 or abs(sry - ery) > 5:
								self._do_mouse_action(erx, ery, "drag", start_x=srx, start_y=sry)
								time.sleep(random.uniform(0.4, 0.8))
						btn = data.get("action_button")
						if btn and not (isinstance(btn, list) and len(btn) == 0):
							time.sleep(random.uniform(0.4, 0.8))
							ry = int(btn[0] * h / 1000) + random.randint(-5, 5)
							rx = int(btn[1] * w / 1000) + random.randint(-5, 5)
							self._do_mouse_action(rx, ry, "click")
							time.sleep(random.uniform(1.5, 2.5))
					elif action == "puzzle":
						tiles = data.get("tile_clicks", [])
						btn = data.get("action_button")
						is_fading = data.get("is_fading", False)
						for tile in tiles:
							if self._captcha_run_stale(run_id):
								break
							ry = int(tile[0] * h / 1000) + random.randint(-9, 9)
							rx = int(tile[1] * w / 1000) + random.randint(-9, 9)
							self._do_mouse_action(rx, ry, "click")
							time.sleep(random.uniform(0.4, 0.9))
						if self._captcha_run_stale(run_id):
							break
						if (
							btn
							and not (isinstance(btn, list) and len(btn) == 0)
							and (not is_fading or len(tiles) == 0)
						):
							time.sleep(random.uniform(0.4, 0.8))
							ry = int(btn[0] * h / 1000) + random.randint(-6, 6)
							rx = int(btn[1] * w / 1000) + random.randint(-6, 6)
							self._do_mouse_action(rx, ry, "click")
							time.sleep(random.uniform(1.8, 2.5))
						elif tiles and is_fading:
							time.sleep(random.uniform(1.2, 1.8))
					elif action == "none":
						time.sleep(random.uniform(1.2, 1.8))
						continue
				except Exception as e:
					log.error(f"Visual captcha loop parsing error: {e}", exc_info=True)
					continue
			else:
				if not self._captcha_run_stale(run_id):
					# Translators: Message reported when AI fails to solve the visual CAPTCHA after max attempts.
					fail_msg = _("Failed to solve CAPTCHA after maximum attempts.")
					core.callLater(0, self.report_status, fail_msg)
		except Exception as e:
			log.error(f"Visual captcha loop error: {e}", exc_info=True)
		finally:
			if not self._captcha_run_stale(run_id):
				self._is_captcha_running = False
				self.current_status = _("Idle")
