# -*- coding: utf-8 -*-
import ctypes
import time
import random
import logging
import threading
import winUser
import api

log = logging.getLogger(__name__)

CLIPBOARD_RESTORE_DELAY = 2.5


class _MOUSEINPUT(ctypes.Structure):
	_fields_ = [
		("dx", ctypes.c_long),
		("dy", ctypes.c_long),
		("mouseData", ctypes.c_ulong),
		("dwFlags", ctypes.c_ulong),
		("time", ctypes.c_ulong),
		("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
	]


class _KEYBDINPUT(ctypes.Structure):
	_fields_ = [
		("wVk", ctypes.c_ushort),
		("wScan", ctypes.c_ushort),
		("dwFlags", ctypes.c_ulong),
		("time", ctypes.c_ulong),
		("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
	]


class _HARDWAREINPUT(ctypes.Structure):
	_fields_ = [
		("uMsg", ctypes.c_ulong),
		("wParamL", ctypes.c_short),
		("wParamH", ctypes.c_ushort),
	]


class _INPUT_UNION(ctypes.Union):
	_fields_ = [
		("mi", _MOUSEINPUT),
		("ki", _KEYBDINPUT),
		("hi", _HARDWAREINPUT),
	]


class _INPUT(ctypes.Structure):
	_fields_ = [
		("type", ctypes.c_ulong),
		("union", _INPUT_UNION),
	]


INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_EXTENDEDKEY = 0x0001
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x1000
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_VIRTUALDESK = 0x4000
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79


def send_ctrl_v():
	try:
		winUser.keybd_event(0x11, 0, 0, 0)
		winUser.keybd_event(0x56, 0, 0, 0)
		winUser.keybd_event(0x56, 0, 2, 0)
		winUser.keybd_event(0x11, 0, 2, 0)
	except Exception as e:
		log.warning(f"send_ctrl_v failed: {e}")


class MouseSimulator:
	_user32 = ctypes.windll.user32

	@staticmethod
	def _make_mouse_input(flags, dx=0, dy=0, data=0):
		inp = _INPUT()
		inp.type = INPUT_MOUSE
		inp.union.mi.dx = dx
		inp.union.mi.dy = dy
		inp.union.mi.mouseData = data
		inp.union.mi.dwFlags = flags
		inp.union.mi.time = 0
		inp.union.mi.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))
		return inp

	@staticmethod
	def _make_keyboard_input(vk, flags=0):
		inp = _INPUT()
		inp.type = INPUT_KEYBOARD
		inp.union.ki.wVk = vk
		inp.union.ki.wScan = 0
		inp.union.ki.dwFlags = flags
		inp.union.ki.time = 0
		inp.union.ki.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))
		return inp

	@staticmethod
	def _send_inputs(*inputs):
		n = len(inputs)
		arr = (_INPUT * n)(*inputs)
		result = ctypes.windll.user32.SendInput(n, ctypes.pointer(arr), ctypes.sizeof(_INPUT))
		if result != n:
			log.warning(f"SendInput injected {result}/{n} events")
		if log.isEnabledFor(logging.DEBUG):
			try:
				log.debug(
					"SendInput: sent=%s requested=%s cursor=%s foreground=%s",
					result,
					n,
					winUser.getCursorPos(),
					ctypes.windll.user32.GetForegroundWindow(),
				)
			except Exception:
				log.debug("SendInput diagnostics unavailable", exc_info=True)
		return result == n

	@staticmethod
	def move_to(x, y, smooth=False, steps=15, step_delay=0.01):
		if smooth:
			try:
				curr_x, curr_y = winUser.getCursorPos()
			except Exception:
				curr_x, curr_y = 0, 0
			for i in range(1, steps + 1):
				progress = i / steps
				eased = 1 - (1 - progress) ** 2
				cx = int(curr_x + (x - curr_x) * eased)
				cy = int(curr_y + (y - curr_y) * eased)
				ctypes.windll.user32.SetCursorPos(cx, cy)
				time.sleep(step_delay)
		else:
			ctypes.windll.user32.SetCursorPos(int(x), int(y))
			time.sleep(0.02)

	@staticmethod
	def click(x, y, button="left", double=False):
		MouseSimulator.move_to(x, y)
		time.sleep(0.05)
		if button == "left":
			down_flag = MOUSEEVENTF_LEFTDOWN
			up_flag = MOUSEEVENTF_LEFTUP
		elif button == "right":
			down_flag = MOUSEEVENTF_RIGHTDOWN
			up_flag = MOUSEEVENTF_RIGHTUP
		elif button == "middle":
			down_flag = MOUSEEVENTF_MIDDLEDOWN
			up_flag = MOUSEEVENTF_MIDDLEUP
		else:
			down_flag = MOUSEEVENTF_LEFTDOWN
			up_flag = MOUSEEVENTF_LEFTUP
		count = 2 if double else 1
		for _i in range(count):
			inputs = [
				MouseSimulator._make_mouse_input(down_flag),
				MouseSimulator._make_mouse_input(up_flag),
			]
			MouseSimulator._send_inputs(*inputs)
			if double:
				time.sleep(0.05)
		time.sleep(0.1)

	@staticmethod
	def _get_virtual_rect():
		u = ctypes.windll.user32
		vx = u.GetSystemMetrics(SM_XVIRTUALSCREEN)
		vy = u.GetSystemMetrics(SM_YVIRTUALSCREEN)
		vw = u.GetSystemMetrics(SM_CXVIRTUALSCREEN)
		vh = u.GetSystemMetrics(SM_CYVIRTUALSCREEN)
		if vw <= 0:
			vw = u.GetSystemMetrics(0)
		if vh <= 0:
			vh = u.GetSystemMetrics(1)
		return vx, vy, vw, vh

	@staticmethod
	def _abs_move(x, y, rect):
		vx, vy, vw, vh = rect
		nx = int((x - vx) * 65535 / max(vw - 1, 1))
		ny = int((y - vy) * 65535 / max(vh - 1, 1))
		move = MouseSimulator._make_mouse_input(
			MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK,
			dx=nx,
			dy=ny,
		)
		MouseSimulator._send_inputs(move)

	@staticmethod
	def drag(start_x, start_y, end_x, end_y, duration=1.2, steps=60):
		start_x, start_y = int(start_x), int(start_y)
		end_x, end_y = int(end_x), int(end_y)
		rect = MouseSimulator._get_virtual_rect()

		MouseSimulator._abs_move(start_x, start_y, rect)
		time.sleep(random.uniform(0.15, 0.3))

		down_input = MouseSimulator._make_mouse_input(MOUSEEVENTF_LEFTDOWN)
		MouseSimulator._send_inputs(down_input)
		time.sleep(random.uniform(0.2, 0.4))

		for i in range(1, steps + 1):
			t = i / steps
			if t < 0.5:
				progress = 4 * t * t * t
			else:
				p = 2 * t - 2
				progress = 0.5 * p * p * p + 1

			cx = int(start_x + (end_x - start_x) * progress)
			jitter_y = random.randint(-2, 2)
			cy = int(start_y + (end_y - start_y) * progress) + jitter_y

			MouseSimulator._abs_move(cx, cy, rect)

			base_sleep = duration / steps
			time.sleep(base_sleep * random.uniform(0.6, 1.4))

		if random.random() > 0.3:
			overshoot_x = end_x + random.randint(3, 7) * (1 if end_x > start_x else -1)
			MouseSimulator._abs_move(overshoot_x, end_y, rect)
			time.sleep(random.uniform(0.1, 0.2))
			MouseSimulator._abs_move(end_x, end_y, rect)
			time.sleep(random.uniform(0.1, 0.2))

		time.sleep(random.uniform(0.2, 0.4))

		up_input = MouseSimulator._make_mouse_input(MOUSEEVENTF_LEFTUP)
		MouseSimulator._send_inputs(up_input)
		time.sleep(random.uniform(0.1, 0.3))

	@staticmethod
	def scroll(x, y, direction="down", clicks=3):
		MouseSimulator.move_to(x, y)
		time.sleep(0.05)
		if direction in ("left", "right"):
			delta = 120 if direction == "right" else -120
			flags = MOUSEEVENTF_HWHEEL
		else:
			delta = 120 if direction == "up" else -120
			flags = MOUSEEVENTF_WHEEL
		total_delta = delta * clicks
		scroll_input = MouseSimulator._make_mouse_input(flags, data=total_delta & 0xFFFFFFFF)
		MouseSimulator._send_inputs(scroll_input)
		time.sleep(0.1)

	@staticmethod
	def key_press(vk_code, extended=False):
		flags_down = KEYEVENTF_EXTENDEDKEY if extended else 0
		flags_up = KEYEVENTF_KEYUP | (KEYEVENTF_EXTENDEDKEY if extended else 0)
		inputs = [
			MouseSimulator._make_keyboard_input(vk_code, flags_down),
			MouseSimulator._make_keyboard_input(vk_code, flags_up),
		]
		MouseSimulator._send_inputs(*inputs)

	@staticmethod
	def type_text(text, press_enter=False):
		old_clip = None
		try:
			old_clip = api.getClipData()
		except Exception:
			pass
		clean_text = text.replace("\n", "").strip()
		try:
			api.copyToClip(clean_text)
			time.sleep(0.2)
			VK_CONTROL = 0x11
			VK_V = 0x56
			inputs = [
				MouseSimulator._make_keyboard_input(VK_CONTROL, 0),
				MouseSimulator._make_keyboard_input(VK_V, 0),
				MouseSimulator._make_keyboard_input(VK_V, KEYEVENTF_KEYUP),
				MouseSimulator._make_keyboard_input(VK_CONTROL, KEYEVENTF_KEYUP),
			]
			MouseSimulator._send_inputs(*inputs)
			time.sleep(0.3)
		finally:
			if old_clip is not None and old_clip != clean_text:
				threading.Thread(
					target=MouseSimulator._restore_clipboard,
					args=(old_clip, clean_text),
					daemon=True,
				).start()
		if press_enter:
			time.sleep(0.2)
			MouseSimulator.key_press(0x0D)

	@staticmethod
	def _restore_clipboard(old_clip, pasted_text):
		time.sleep(CLIPBOARD_RESTORE_DELAY)
		try:
			if api.getClipData() != pasted_text:
				return
			api.copyToClip(old_clip)
		except Exception as e:
			log.debug(f"Clipboard restore skipped: {e}")
