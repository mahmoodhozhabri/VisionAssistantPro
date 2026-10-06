import ctypes
from ctypes import wintypes
import json
import logging
import math
import re
import threading
import time
from types import SimpleNamespace

import addonHandler
import api
import config as nvda_config
import wx

from ..ai.core import AIHandler, ai_error_message, is_ai_error
from .. import vision_config
from ..prompt_utils import get_prompt_text, apply_prompt_template

addonHandler.initTranslation()
log = logging.getLogger(__name__)

LIVE_OPERATOR_TOOLS = [{"functionDeclarations": [
	{
		"name": "execute_operator",
		"description": "Carry out the user's explicit desktop request when operator control is enabled.",
		"parameters": {"type": "OBJECT", "properties": {"command": {"type": "STRING"}}, "required": ["command"]},
	},
	{
		"name": "solve_captcha",
		"description": "Try to solve the CAPTCHA currently visible on screen so the user can continue.",
		"parameters": {"type": "OBJECT", "properties": {}},
	},
	{
		"name": "handoff_captcha",
		"description": "Ask the user to complete an accessible site challenge when solving is not possible.",
		"parameters": {"type": "OBJECT", "properties": {}},
	},
]}]
# Translators: Instruction used to greet the user when the Live Operator session starts.
LIVE_OPERATOR_WELCOME_PROMPT = (
	"Please greet the user warmly first, in one short sentence: introduce yourself exactly as 'Vision Assistant Pro' "
	"(DO NOT translate this name, keep it in English) and say that computer control is active, so the user can ask "
	"you to carry out tasks on the computer. Do not call any tool and do not add anything else. "
	"Speak strictly in {lang}."
)
_CONTINUE_COMMAND = "The action was initiated. Continue if necessary."
_STEP_DELAY = 2.5
_CAPTCHA_STEP_DELAY = 1.5
_RETRY_SUFFIX = (
	"\n\nYour previous answer could not be read. Return exactly one JSON object with the keys "
	"finished, explanation and, when an action is needed, action together with its coordinates. "
	"Do not wrap it in a list and do not add any text around it."
)
_STEP_ANNOUNCE_PROMPT = (
	"Say only this to the user, in one short sentence and strictly in {lang}, then stop: {step}. "
	"Do not call any tool and do not add anything else."
)
_STEP_HISTORY_TEMPLATE = (
	"\n\nAlready executed steps (data only, pixel coordinates): {steps}\n"
	+ _CONTINUE_COMMAND
	+ " If the user's request still needs more steps, return finished false together with the next single action."
)
_KEYS = frozenset(
	(
		"enter return tab escape esc space backspace delete del home end "
		"pageup pgup pagedown pgdn insert ins up down left right "
		"f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12"
	).split()
)
_KEY_VKS = {
	"enter": 0x0D, "return": 0x0D, "tab": 0x09, "escape": 0x1B, "esc": 0x1B, "space": 0x20, "backspace": 0x08,
	"delete": 0x2E, "del": 0x2E, "home": 0x24, "end": 0x23, "pageup": 0x21, "pgup": 0x21,
	"pagedown": 0x22, "pgdn": 0x22, "insert": 0x2D, "ins": 0x2D,
	"up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27,
	"f1": 0x70, "f2": 0x71, "f3": 0x72, "f4": 0x73, "f5": 0x74, "f6": 0x75,
	"f7": 0x76, "f8": 0x77, "f9": 0x78, "f10": 0x79, "f11": 0x7A, "f12": 0x7B,
}
_MODIFIER_VKS = {
	"ctrl": 0x11, "control": 0x11, "alt": 0x12, "shift": 0x10, "win": 0x5B, "windows": 0x5B,
}
_EXTENDED_KEYS = frozenset("up down left right home end pageup pgup pagedown pgdn insert ins delete del".split())
_FIELDS = {"click": {"x", "y"}, "double_click": {"x", "y"}, "right_click": {"x", "y"},
	"scroll": {"x", "y", "direction"}, "drag": {"x", "y", "start_x", "start_y"},
	"type": {"x", "y", "text"}, "keypress": {"key"}, "ask_user": set(), "handoff_captcha": set(),
	"solve_captcha": set()}


class _LiveOperatorExit(Exception):
	def __init__(self, status, message):
		self.response = {"status": status, "message": message}


def _strict_object(pairs):
	result = {}
	for key, value in pairs:
		if key in result:
			raise ValueError("Duplicate JSON field")
		result[key] = value
	return result


def _first_object_text(text):
	start, end = text.find("{"), text.rfind("}")
	if start < 0 or end <= start:
		return None
	return text[start:end + 1]


def _load_object(raw):
	text = raw.strip()
	if text.startswith("```"):
		parts = text.split("```")
		body = [part for part in parts[1:] if "{" in part]
		text = (body[0] if body else text).strip()
	decoder = json.JSONDecoder(object_pairs_hook=_strict_object)
	start = text.find("{")
	candidates = [text, text[start:] if start >= 0 else None, _first_object_text(text)]
	for candidate in candidates:
		if not candidate:
			continue
		try:
			data, _end = decoder.raw_decode(candidate)
		except ValueError:
			continue
		if isinstance(data, list):
			if len(data) != 1 or not isinstance(data[0], dict):
				raise ValueError("Expected one JSON object")
			data = data[0]
		if isinstance(data, dict):
			return data
	raise ValueError("Unreadable answer")


_BUSY_MARKERS = ("high demand", "overloaded", "unavailable", "server busy", "try again", "503")
_SLOW_NOTICE_AFTER = 15.0


def _is_busy_error(message):
	text = (message or "").lower()
	return any(marker in text for marker in _BUSY_MARKERS)


def _parse_shortcut(value):
	parts = [part.strip().lower() for part in value.split("+") if part.strip()]
	if len(parts) < 2 or len(parts) > 3:
		return None
	key = parts[-1]
	if key not in _KEY_VKS and not (len(key) == 1 and key.isalnum()):
		return None
	modifiers = parts[:-1]
	if not modifiers or any(modifier not in _MODIFIER_VKS for modifier in modifiers) or len(set(modifiers)) != len(modifiers):
		return None
	return {"modifiers": modifiers, "key": key}


def _parse_action(raw, width, height):
	if not isinstance(raw, str) or len(raw) > 16000 or width <= 0 or height <= 0:
		raise ValueError("Invalid planner response")
	data = _load_object(raw)
	allowed = {"action", "finished", "explanation", "x", "y", "start_x", "start_y", "text",
		"key", "keys", "direction", "scroll_direction"}
	if not isinstance(data, dict) or set(data) - allowed or type(data.get("finished")) is not bool:
		raise ValueError("Invalid fields")
	explanation = data.get("explanation")
	if not isinstance(explanation, str) or not explanation.strip() or len(explanation) > 4000:
		raise ValueError("Invalid explanation")
	action = data.get("action")
	out = {"finished": data["finished"], "explanation": explanation}
	if not action:
		return out
	if action not in _FIELDS:
		raise ValueError("Unknown action")
	out["action"] = action
	for key in _FIELDS[action] & {"x", "y", "start_x", "start_y"}:
		value = data.get(key)
		if value is None and action == "type":
			continue
		if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
			raise ValueError("Invalid coordinates")
		bound = width if key.endswith("x") else height
		if value <= 1000:
			out[key] = min(bound - 1, int(value * bound / 1000))
		elif value < bound:
			out[key] = int(value)
		else:
			raise ValueError("Invalid coordinates")
	if action == "type" and ("x" in out) != ("y" in out):
		raise ValueError("Invalid coordinates")
	for field, alias in (("key", "keys"), ("direction", "scroll_direction")):
		if field not in _FIELDS[action]:
			continue
		value = data.get(field) or data.get(alias)
		if data.get(field) and data.get(alias) and data[field] != data[alias]:
			raise ValueError("Conflicting parameters")
		valid = _KEYS if field == "key" else {"up", "down", "left", "right"}
		if not isinstance(value, str) or not value:
			raise ValueError("Invalid key or direction")
		if field == "key":
			value = value.strip().lower()
			if value not in valid and "+" not in value:
				raise ValueError("Invalid key or direction")
			if "+" in value and _parse_shortcut(value) is None:
				raise ValueError("Unsupported key combination")
		elif value not in valid:
			raise ValueError("Invalid key or direction")
		out[field] = value
	if action == "type":
		text = data.get("text")
		if not isinstance(text, str):
			raise ValueError("Invalid type text")
		enter = text.endswith("\n")
		text = text.replace("\n", "").strip()
		if not text or len(text) > 4000 or any(ord(c) < 32 or ord(c) == 127 for c in text):
			raise ValueError("Invalid type text")
		if not enter:
			follow = data.get("key") or data.get("keys")
			if isinstance(follow, str) and follow.strip().lower() in ("enter", "return"):
				enter = True
		if not enter:
			enter = "enter" in explanation.lower() or "اینتر" in explanation
		out["text"] = text
		out["enter"] = enter
	return out


def _step_line(step):
	action = step.get("action") or "step"
	location = ",".join(str(step[key]) for key in ("x", "y") if key in step)
	head = " ".join(part for part in (action, "at " + location if location else "") if part)
	detail = step.get("explanation") or step.get("note") or step.get("outcome") or ""
	return "- {0}: {1}".format(head, detail) if detail else "- " + head


class LiveOperatorMixin:
	def _live_operator_on(self):
		return bool(getattr(self, "_live_session_operator", False))

	def _set_live_operator_session(self, enabled):
		self._live_session_operator = bool(enabled)

	def _live_operator_cancel(self, session, ids):
		job = getattr(self, "_live_operator_job", None)
		if job and job.session is session and (ids is None or job.call["id"] in ids):
			job.cancel.set()

	def _stop_live_operator(self):
		job = getattr(self, "_live_operator_job", None)
		if job:
			self._live_operator_cancel(job.session, None)

	def _lo_check(self, job):
		pending = getattr(job.session, "_pending_tool_calls", {})
		if (job.cancel.is_set() or getattr(self, "_live_operator_job", None) is not job
				or self.live_session is not job.session or not self._live_operator_on()
				or not job.session._running or not job.session.ready or job.call["id"] not in pending):
			# Translators: The Live operator task was cancelled.
			raise _LiveOperatorExit("cancelled", _("Operator cancelled."))
		if time.monotonic() >= job.deadline:
			# Translators: The maximum duration of a Live operator task was reached.
			raise _LiveOperatorExit("step_limit", _("Operator time limit reached."))
		if getattr(self, "_is_operator_running", False):
			# Translators: The separate operator is already working.
			raise _LiveOperatorExit("error", _("Standalone operator is busy."))

	def _lo_wait(self, job, event, timeout):
		deadline = min(job.deadline, time.monotonic() + timeout)
		while True:
			self._lo_check(job)
			if event.wait(0.05):
				self._lo_check(job)
				return
			if time.monotonic() >= deadline:
				# Translators: A Live operator request or GUI operation took too long.
				raise _LiveOperatorExit("error", _("Operator wait timed out."))

	def _lo_gui(self, job, callback, timeout=15):
		done, abandoned, result = threading.Event(), threading.Event(), []
		def run():
			try:
				if abandoned.is_set():
					return
				self._lo_check(job)
				result.append(callback())
			except Exception as error:
				result.append(error)
			finally:
				done.set()
		wx.CallAfter(run)
		try:
			self._lo_wait(job, done, timeout)
		except Exception:
			abandoned.set()
			job.cancel.set()
			raise
		if isinstance(result[0], Exception):
			raise result[0]
		return result[0]

	def _lo_environment(self):
		if not wx.IsMainThread():
			raise RuntimeError("Desktop access requires the GUI thread")
		from ..utils.system import check_screen_curtain_active, desktop_protection_reason
		if check_screen_curtain_active() or desktop_protection_reason():
			# Translators: Computer control is blocked on a protected desktop.
			raise _LiveOperatorExit("user_action_required", _("Secure mode, locked desktop or screen curtain is active."))
		user32 = ctypes.windll.user32
		return tuple(user32.GetSystemMetrics(i) for i in (0, 1, 76, 77, 78, 79))

	def _lo_bounds(self, geometry):
		left, top = geometry[2], geometry[3]
		return left, top, left + max(geometry[4], geometry[0]), top + max(geometry[5], geometry[1])

	def _lo_capture(self, job):
		self._lo_check(job)
		geometry = self._lo_environment()
		image = self._capture_fullscreen()
		self._lo_check(job)
		if not image[0] or len(image) < 3 or image[1] <= 0 or image[2] <= 0:
			# Translators: A usable screen image could not be captured.
			raise _LiveOperatorExit("error", _("Invalid screenshot geometry or format."))
		log.debug(
			"Live operator capture: call=%s time=%.3f size=%sx%s",
			job.call["id"], time.monotonic(), image[1], image[2],
		)
		return image, geometry

	def _lo_app_name(self):
		try:
			obj = api.getForegroundObject()
			return obj.appModule.appName if obj and obj.appModule else "unknown"
		except Exception:
			log.debug("Foreground app name lookup failed", exc_info=True)
			return "unknown"

	def _lo_captcha_extra(self):
		try:
			name = api.getForegroundObject().name or ""
		except Exception:
			name = ""
		return (
			" Read 5 Persian digits, convert to English."
			if "پنجره ملی خدمات دولت هوشمند" in name
			else " Convert to English digits."
		)

	def _lo_detect_captcha(self, job, snapshot):
		prompt = apply_prompt_template(
			get_prompt_text("captcha_solver_base"), [("captcha_extra", self._lo_captcha_extra())]
		)
		image = snapshot[0]
		return AIHandler.call(
			prompt, attachments=[{"mime_type": image[3], "data": image[0]}], task="operator"
		)

	def _lo_type_captcha(self, job, answer):
		self._lo_check(job)
		code = re.sub(r"[^a-zA-Z0-9]", "", answer or "")
		if not code:
			# Translators: The CAPTCHA answer returned by the AI did not contain usable characters.
			raise _LiveOperatorExit("error", _("The CAPTCHA answer was empty."))
		self._finish_captcha(code)
		return code

	def _lo_visual_captcha(self, job):
		run_id = getattr(self, "_captcha_run_id", 0) + 1
		self._captcha_run_id = run_id
		self._lo_captcha_run_id = run_id
		done = threading.Event()
		def solve():
			try:
				self._solve_visual_captcha_loop(run_id)
			except Exception:
				log.debug("Visual CAPTCHA loop failed", exc_info=True)
			finally:
				done.set()
		threading.Thread(target=solve, daemon=True).start()
		try:
			self._lo_wait(job, done, 240)
		finally:
			self._lo_captcha_run_id = None
			if job.cancel.is_set():
				self._captcha_run_id = run_id + 1
				self._is_captcha_running = False
				self.current_status = _("Idle")
		snapshot = self._lo_gui(job, lambda: self._lo_capture(job))
		verify = self._lo_detect_captcha(job, snapshot)
		self._lo_check(job)
		if verify and not is_ai_error(verify) and "[[[VISUAL_CAPTCHA]]]" not in verify and "[[[NO_CAPTCHA]]]" not in verify:
			code = self._lo_gui(job, lambda: self._lo_type_captcha(job, verify))
			# Translators: The visual CAPTCHA was solved and its answer typed for the user.
			return {"status": "completed", "message": _("CAPTCHA solved and typed: {text}").format(text=code)}
		# Translators: The visual CAPTCHA could not be solved automatically.
		unsolved_msg = _("The visual CAPTCHA could not be solved. Please complete it yourself.")
		return {
			"status": "user_action_required",
			"message": unsolved_msg,
		}

	def _lo_solve_captcha(self, job):
		snapshot = self._lo_gui(job, lambda: self._lo_capture(job))
		answer = self._lo_detect_captcha(job, snapshot)
		self._lo_check(job)
		if not answer or is_ai_error(answer):
			# Translators: The AI service returned no usable CAPTCHA answer.
			message = ai_error_message(answer) if answer else _("The AI service returned no answer.")
			raise _LiveOperatorExit("error", message)
		if "[[[NO_CAPTCHA]]]" in answer:
			# Translators: No challenge was found on the current screen.
			return {"status": "not_found", "message": _("No CAPTCHA was found on the screen.")}
		if "[[[VISUAL_CAPTCHA]]]" not in answer:
			code = self._lo_gui(job, lambda: self._lo_type_captcha(job, answer))
			# Translators: The text CAPTCHA was solved and its answer typed for the user.
			return {"status": "completed", "message": _("CAPTCHA solved and typed: {text}").format(text=code)}
		if not nvda_config.conf["VisionAssistant"].get("enable_visual_captcha_solver", True):
			# Translators: A visual challenge was found while the solver is switched off in settings.
			disabled_msg = _("A visual CAPTCHA was found, but the solver is disabled in settings.")
			return {
				"status": "user_action_required",
				"message": disabled_msg,
			}
		return self._lo_visual_captcha(job)

	def _lo_announce(self, job, data):
		self._lo_report(job, data.get("explanation"))

	def _lo_report(self, job, text):
		if not text:
			return
		prompt = _STEP_ANNOUNCE_PROMPT.format(
			lang=vision_config.get_lang_name("ai_response_language"), step=text
		)
		try:
			sent = job.session.send_client_text(prompt)
		except Exception:
			log.debug("Live step announcement failed", exc_info=True)
			sent = False
		if not sent:
			wx.CallAfter(self.report_status, text)

	def _lo_trace(self, phase, job, data):
		try:
			point = wintypes.POINT()
			user32 = ctypes.windll.user32
			position = (point.x, point.y) if user32.GetCursorPos(ctypes.byref(point)) else None
			log.debug("Live operator %s: call=%s action=%s target=%s,%s cursor=%s hwnd=%s",
				phase, job.call["id"], data["action"], data.get("x"), data.get("y"), position,
				user32.GetForegroundWindow())
		except Exception:
			log.debug("Live operator diagnostics unavailable", exc_info=True)

	def _lo_type_here(self, text, press_enter=False):
		from ..utils.mouse_keyboard import KEYEVENTF_KEYUP, MouseSimulator

		VK_CONTROL, VK_A, VK_DELETE = 0x11, 0x41, 0x2E
		MouseSimulator._send_inputs(
			MouseSimulator._make_keyboard_input(VK_CONTROL, 0),
			MouseSimulator._make_keyboard_input(VK_A, 0),
			MouseSimulator._make_keyboard_input(VK_A, KEYEVENTF_KEYUP),
			MouseSimulator._make_keyboard_input(VK_CONTROL, KEYEVENTF_KEYUP),
		)
		time.sleep(0.1)
		MouseSimulator.key_press(VK_DELETE)
		time.sleep(0.1)
		MouseSimulator.type_text(text, press_enter=press_enter)

	def _lo_keypress_combo(self, combination):
		from ..utils.mouse_keyboard import KEYEVENTF_EXTENDEDKEY, KEYEVENTF_KEYUP, MouseSimulator

		shortcut = _parse_shortcut(combination)
		if not shortcut:
			raise ValueError("Unsupported key combination")
		modifiers = [_MODIFIER_VKS[name] for name in shortcut["modifiers"]]
		key_name = shortcut["key"]
		if key_name in _KEY_VKS:
			vk = _KEY_VKS[key_name]
			extended = key_name in _EXTENDED_KEYS
		else:
			code = ctypes.windll.user32.VkKeyScanW(ord(key_name)) & 0xFF
			if not code:
				raise ValueError("Unsupported key")
			vk = code
			extended = False
		inputs = [MouseSimulator._make_keyboard_input(modifier, 0) for modifier in modifiers]
		inputs.append(MouseSimulator._make_keyboard_input(vk, KEYEVENTF_EXTENDEDKEY if extended else 0))
		inputs.append(MouseSimulator._make_keyboard_input(vk, (KEYEVENTF_EXTENDEDKEY if extended else 0) | KEYEVENTF_KEYUP))
		inputs.extend(MouseSimulator._make_keyboard_input(modifier, KEYEVENTF_KEYUP) for modifier in reversed(modifiers))
		MouseSimulator._send_inputs(*inputs)
		time.sleep(0.2)

	def _lo_execute(self, job, data, snapshot):
		self._lo_check(job)
		image, geometry = snapshot
		action = data["action"]
		if action not in _FIELDS or action in ("ask_user", "handoff_captcha", "solve_captcha"):
			raise ValueError("Not an executable action")
		if "x" in data:
			sx = geometry[0] / float(image[1]) if image[1] > 0 and image[1] != geometry[0] else 1.0
			sy = geometry[1] / float(image[2]) if image[2] > 0 and image[2] != geometry[1] else 1.0
			if sx != 1.0 or sy != 1.0:
				data["x"] = int(round(data["x"] * sx))
				data["y"] = int(round(data["y"] * sy))
				if action == "drag":
					data["start_x"] = int(round(data["start_x"] * sx))
					data["start_y"] = int(round(data["start_y"] * sy))
			left, top, right, bottom = self._lo_bounds(geometry)
			points = [(data["x"], data["y"])]
			if action == "drag":
				points.append((data["start_x"], data["start_y"]))
			if any(not left <= x < right or not top <= y < bottom for x, y in points):
				# Translators: The proposed click is outside the whole desktop area.
				raise _LiveOperatorExit("user_action_required", _("Action is outside the screen."))
		self._lo_check(job)
		self._lo_trace("before action", job, data)
		if action == "type":
			if "x" in data:
				self._do_type(data["x"], data["y"], data["text"], press_enter=bool(data.get("enter")))
			else:
				self._lo_type_here(data["text"], bool(data.get("enter")))
		elif action == "keypress":
			if "+" in data["key"]:
				self._lo_keypress_combo(data["key"])
			else:
				self._do_keypress(data["key"])
		else:
			kwargs = {"scroll_direction": data["direction"]} if action == "scroll" else {}
			if action == "drag":
				kwargs = {"start_x": data["start_x"], "start_y": data["start_y"]}
			self._do_mouse_action(data["x"], data["y"], action, **kwargs)
		self._lo_trace("after action", job, data)
		self._lo_check(job)

	def _lo_wait_for_answer(self, job, done, notice_after=None):
		notice_after = _SLOW_NOTICE_AFTER if notice_after is None else notice_after
		start = time.monotonic()
		notified = False
		while True:
			self._lo_check(job)
			if done.wait(0.05):
				self._lo_check(job)
				return
			if not notified and time.monotonic() - start >= notice_after:
				notified = True
				self._lo_slow_notice(job)

	def _lo_slow_notice(self, job):
		# Translators: Reassurance spoken by Live when a step takes longer than usual.
		self._lo_report(job, _("This is taking longer than usual. I am still working on it, please wait."))

	def _lo_plan(self, job, prompt, image):
		for attempt in range(2):
			text = prompt if attempt == 0 else prompt + _RETRY_SUFFIX
			done, result = threading.Event(), []
			def request():
				try:
					self._lo_check(job)
					result.append(AIHandler.call(text, attachments=[{"mime_type": image[3], "data": image[0]}],
						json_mode=True, task="operator"))
				except Exception as error:
					result.append(error)
				finally:
					done.set()
			threading.Thread(target=request, daemon=True).start()
			self._lo_wait_for_answer(job, done)
			if isinstance(result[0], Exception):
				raise result[0]
			if not result[0] or is_ai_error(result[0]):
				# Translators: The service failed after its internal retry policy finished.
				message = ai_error_message(result[0]) if result[0] else _("The AI service returned no answer.")
				if _is_busy_error(message):
					# Translators: Message when the AI service stayed overloaded until the end.
					raise _LiveOperatorExit("error", _("The AI service is busy and could not finish this task. Please try again in a moment."))
				raise _LiveOperatorExit("error", message)
			try:
				return _parse_action(result[0], image[1], image[2])
			except ValueError:
				log.debug("Invalid live operator plan", exc_info=True)
		# Translators: Invalid model output was rejected without moving the mouse or typing.
		raise _LiveOperatorExit("error", _("The AI returned an invalid action. Nothing was executed."))

	def _lo_handoff(self, job):
		self._lo_check(job)
		self._live_operator_handoff_session = job.session
		# Translators: Instruction telling the user how to regain control after a site challenge.
		return {
			"status": "user_action_required",
			"message": _("Complete the accessible challenge, toggle operator permission off and on, then ask to continue."),
		}

	def _lo_worker(self, job):
		# Translators: Unexpected failure of the Live operator.
		response = {"status": "error", "message": _("Operator failed. Check the add-on log for details.")}
		try:
			if job.call["name"] == "handoff_captcha":
				response = self._lo_gui(job, lambda: self._lo_handoff(job))
			elif job.call["name"] == "solve_captcha":
				response = self._lo_solve_captcha(job)
			else:
				history = []
				last_signature = None
				strikes = 0
				for step in range(10):
					snapshot = self._lo_gui(job, lambda: self._lo_capture(job))
					app_name = self._lo_gui(job, self._lo_app_name)
					prompt = apply_prompt_template(
						get_prompt_text("ai_operator_system"),
						[
							("user_command", job.call["args"]["command"]),
							("response_lang", vision_config.get_lang_name("ai_response_language")),
							("app_name", app_name),
						],
					)
					if history:
						prompt += _STEP_HISTORY_TEMPLATE.format(steps="\n".join(_step_line(step) for step in history))
					data = self._lo_plan(job, prompt, snapshot[0])
					self._lo_check(job)
					if not data.get("action"):
						response = {
							"status": "completed" if data["finished"] else "user_action_required",
							"message": data["explanation"],
						}
						break
					if data["action"] == "handoff_captcha":
						response = self._lo_gui(job, lambda: self._lo_handoff(job))
						break
					if data["action"] == "solve_captcha":
						outcome = self._lo_solve_captcha(job)
						if outcome["status"] in ("completed", "not_found"):
							history.append({"action": "solve_captcha", "outcome": outcome["status"]})
							job.cancel.wait(_CAPTCHA_STEP_DELAY)
							continue
						response = outcome
						break
					if data["action"] == "ask_user":
						response = {"status": "user_action_required", "message": data["explanation"]}
						break
					if step == 9:
						# Translators: Maximum number of approved steps reached.
						response = {"status": "step_limit", "message": _("Ten-step limit reached; no further action executed.")}
						break
					signature = (
						data["action"], data.get("x"), data.get("y"), data.get("text"),
						data.get("key"), data.get("direction"),
					)
					if signature == last_signature:
						strikes += 1
						if strikes >= 2:
							response = {
								"status": "step_limit",
								# Translators: The operator proposed the same action again although nothing changed on screen.
								"message": _("The same action was proposed again with no visible change, so the task stopped."),
							}
							break
						history.append({
							"action": "repeated",
							"note": "That action was already executed and nothing changed. Choose a different action, or return finished true without an action if the request is complete.",
						})
						job.cancel.wait(_STEP_DELAY)
						continue
					strikes = 0
					last_signature = signature
					self._lo_announce(job, data)
					self._lo_gui(job, lambda: self._lo_execute(job, data, snapshot))
					history.append(data)
					if data["finished"]:
						response = {"status": "completed", "message": data["explanation"]}
						break
					job.cancel.wait(_STEP_DELAY)
		except _LiveOperatorExit as error:
			response = error.response
		except Exception:
			log.exception("Live operator failed")
		finally:
			if job.cancel.is_set():
				# Translators: The user stopped the operation.
				response = {"status": "cancelled", "message": _("Operator cancelled.")}
			self._lo_send(job.session, job.call, response)
			wx.CallAfter(self._lo_complete, job, response)

	def _lo_send(self, session, call, response):
		try:
			session.send_tool_response(call, response)
		except Exception:
			log.debug("Live operator response failed", exc_info=True)

	def _lo_complete(self, job, response):
		if getattr(self, "_live_operator_job", None) is not job:
			return
		self._live_operator_job = None
		if self.live_session is job.session:
			# Translators: User-facing name for a successfully completed task.
			completed = _("Completed")
			# Translators: User-facing name for a cancelled task.
			cancelled = _("Cancelled")
			# Translators: User-facing status when the user needs to take over.
			required = _("Your action is required")
			# Translators: User-facing name for a task limit.
			limited = _("Limit reached")
			# Translators: User-facing name for an unsuccessful task.
			failed = _("Error")
			status = {"completed": completed, "cancelled": cancelled, "user_action_required": required,
				"step_limit": limited}.get(response["status"], failed)
			# Translators: A Live operator result displayed in the conversation.
			line = _("Live operator: {status}: {message}").format(status=status, message=response["message"])
			self._live_append(line)
			if response["status"] in ("error", "step_limit"):
				self._lo_report(job, response["message"])

	def _live_operator_call(self, session, call):
		if not wx.IsMainThread():
			wx.CallAfter(self._live_operator_call, session, call)
			return True
		if not isinstance(call, dict) or not isinstance(call.get("id"), str):
			return False
		if call["id"] not in getattr(session, "_pending_tool_calls", {}):
			return True
		args, name = call.get("args"), call.get("name")
		message = None
		if self.live_session is not session or not session.ready or not session._running:
			# Translators: A tool call belongs to a conversation which has ended.
			message = _("Session is no longer active.")
		elif not self._live_operator_on() or not session.tools:
			# Translators: Computer control is disabled.
			message = _("Operator permission is not enabled for this session.")
		elif getattr(self, "_live_operator_job", None) or getattr(self, "_is_operator_running", False):
			# Translators: Another operator request is still running.
			message = _("Operator is busy.")
		elif getattr(self, "_live_operator_handoff_session", None) is session:
			# Translators: Automatic retries are blocked after a site challenge.
			message = _("Complete the accessible challenge, toggle operator permission off and on, then ask to continue.")
		elif (name not in ("execute_operator", "handoff_captcha", "solve_captcha") or not isinstance(args, dict)
				or (name in ("handoff_captcha", "solve_captcha") and args)
				or (name == "execute_operator" and (set(args) != {"command"}
					or not isinstance(args["command"], str) or not args["command"].strip() or len(args["command"]) > 4000))):
			# Translators: An invalid tool call has been rejected.
			message = _("Invalid tool or arguments.")
		if message:
			response = {
				"status": "user_action_required" if getattr(self, "_live_operator_handoff_session", None) is session else "error",
				"message": message,
			}
			threading.Thread(target=self._lo_send, args=(session, call, response), daemon=True).start()
			return True
		job = SimpleNamespace(session=session, call=dict(call, args=dict(args)), cancel=threading.Event(),
			deadline=time.monotonic() + 900)
		self._live_operator_job = job
		threading.Thread(target=self._lo_worker, args=(job,), daemon=True).start()
		return True
