# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import logging
import tempfile
import zipfile
import subprocess
import threading
from urllib import request

import wx
import core
import gui
import ui

from .. import plugin_state
from .. import vision_config
from .system import show_error_dialog
from .media_capture import get_proxy_opener

log = logging.getLogger(__name__)

_ = vision_config._ if hasattr(vision_config, "_") else (lambda x: x)

_VAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "vad")
_MODEL_PATH = os.path.join(_VAD_DIR, "silero_vad.onnx")
_MODEL_URL = (
	"https://raw.githubusercontent.com/snakers4/silero-vad/master/src/silero_vad/data/silero_vad.onnx"
)

# Translators: Label used for the VAD download feature in status messages.
def _py_tag():
	return "cp{0}{1}".format(sys.version_info.major, sys.version_info.minor)


def _runtime_dir():
	return os.path.join(_VAD_DIR, "runtime")


def _ensure_runtime_dir():
	os.makedirs(_runtime_dir(), exist_ok=True)
	return _runtime_dir()


def _download_pypi_wheel(package, version_hint=None):
	if version_hint:
		api_url = "https://pypi.org/pypi/{0}/{1}/json".format(package, version_hint)
	else:
		api_url = "https://pypi.org/pypi/{0}/json".format(package)
	opener = get_proxy_opener(api_url)
	req = request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
	with opener.open(req, timeout=60) as resp:
		data = json.loads(resp.read().decode("utf-8"))

	tag = _py_tag()
	candidates = []
	for f in data.get("urls", []):
		fn = f["filename"]
		if not fn.endswith(".whl"):
			continue
		if "win_amd64" not in fn and "win32" not in fn:
			continue
		if tag in fn or "abi3" in fn:
			candidates.append(f)
	if not candidates:
		raise RuntimeError("No compatible wheel found for {0} on Python {1}".format(package, tag))
	is64 = sys.maxsize > 2**32
	arch = [f for f in candidates if ("win_amd64" in f["filename"]) == is64]
	exact = [f for f in (arch or candidates) if tag in f["filename"]]
	pick = (exact or arch or candidates)[0]
	return pick["url"]


_vad_download_approved = False


def _confirm_vad_download():
	global _vad_download_approved
	if _vad_download_approved:
		return True
	# Translators: Title of dialog asking the user to download Silero VAD
	title = _("Download Silero VAD?")
	message = _(
		# Translators: Message in dialog asking the user to download Silero VAD for silence detection
		"Silence detection requires the Silero VAD model and runtime (approximately 70MB download).\n\nDownload now to the addon's lib folder?\n\nThis is a one-time download."
	)
	user_choice = [wx.ID_NO]
	if core.isMainThread():
		gui.mainFrame.prePopup()
		try:
			dlg = wx.MessageDialog(gui.mainFrame, message, title, wx.YES_NO | wx.ICON_QUESTION)
			user_choice[0] = dlg.ShowModal()
			dlg.Destroy()
		finally:
			gui.mainFrame.postPopup()
	else:
		dlg_closed = threading.Event()

		def ask_user():
			gui.mainFrame.prePopup()
			try:
				dlg = wx.MessageDialog(gui.mainFrame, message, title, wx.YES_NO | wx.ICON_QUESTION)
				user_choice[0] = dlg.ShowModal()
				dlg.Destroy()
			finally:
				gui.mainFrame.postPopup()
				dlg_closed.set()

		wx.CallAfter(ask_user)
		dlg_closed.wait()
	if user_choice[0] == wx.ID_YES:
		_vad_download_approved = True
		return True
	# Translators: Message reported when the user cancels downloading Silero VAD required for silence detection.
	core.callLater(0, ui.message, _("Operation cancelled. Silero VAD is required for silence detection."))
	return False


def _download_and_extract(url, dest_dir, marker_file):
	opener = get_proxy_opener(url)
	req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
	tmp = os.path.join(dest_dir, "download.tmp")
	with opener.open(req, timeout=600) as resp:
		total_size = int(resp.headers.get("content-length", 0))
		downloaded = 0
		with open(tmp, "wb") as f:
			while True:
				chunk = resp.read(1024 * 1024)
				if not chunk:
					break
				f.write(chunk)
				downloaded += len(chunk)
				if total_size > 0:
					percent = int((downloaded / total_size) * 100)
					if downloaded % (2 * 1024 * 1024) < 1024 * 1024:
						plugin_state.speak_status(
							# Translators: Progress message during Silero VAD runtime download. {percent} is the download percentage number.
							_("Downloading Silero VAD: {percent}%").format(percent=percent)
						)
	with zipfile.ZipFile(tmp, "r") as zf:
		zf.extractall(dest_dir)
	try:
		os.remove(tmp)
	except Exception as e:
		log.debug("Download temp removal failed: {0}".format(e))
	if not os.path.exists(marker_file):
		raise RuntimeError("Extraction did not produce expected file: {0}".format(marker_file))


def _install_runtime():
	rdir = _ensure_runtime_dir()
	marker = os.path.join(rdir, ".installed")
	if os.path.exists(marker):
		return rdir
	if not _confirm_vad_download():
		return None

	# Translators: Status message when downloading the VAD runtime (onnxruntime + numpy).
	plugin_state.speak_status(_("Downloading Silero VAD runtime, please wait..."))
	try:
		onnx_url = _download_pypi_wheel("onnxruntime")
		np_url = _download_pypi_wheel("numpy")
		_download_and_extract(onnx_url, rdir, os.path.join(rdir, "onnxruntime", "__init__.py"))
		_download_and_extract(np_url, rdir, os.path.join(rdir, "numpy", "__init__.py"))
		with open(marker, "w") as mf:
			mf.write("ok")
		# Translators: Success message after VAD runtime download completes.
		plugin_state.speak_status(_("Silero VAD runtime downloaded successfully!"))
		return rdir
	except Exception as e:
		log.error("VAD runtime download failed: {0}".format(e), exc_info=True)
		# Translators: Error dialog shown when the Silero VAD runtime download fails. {error} is the error details.
		wx.CallAfter(show_error_dialog, _("Failed to download Silero VAD runtime: {error}").format(error=str(e)))
		return None


def _ensure_model():
	if os.path.exists(_MODEL_PATH):
		return _MODEL_PATH
	os.makedirs(_VAD_DIR, exist_ok=True)
	if not _confirm_vad_download():
		return None
	# Translators: Status message when downloading the Silero VAD model.
	plugin_state.speak_status(_("Downloading Silero VAD model..."))
	try:
		opener = get_proxy_opener(_MODEL_URL)
		req = request.Request(_MODEL_URL, headers={"User-Agent": "Mozilla/5.0"})
		with opener.open(req, timeout=300) as resp:
			total_size = int(resp.headers.get("content-length", 0))
			downloaded = 0
			with open(_MODEL_PATH, "wb") as f:
				while True:
					chunk = resp.read(1024 * 1024)
					if not chunk:
						break
					f.write(chunk)
					downloaded += len(chunk)
					if total_size > 0:
						percent = int((downloaded / total_size) * 100)
						if downloaded % (2 * 1024 * 1024) < 1024 * 1024:
							plugin_state.speak_status(
								# Translators: Progress message during Silero VAD model download. {percent} is the download percentage number.
								_("Downloading Silero VAD model: {percent}%").format(percent=percent)
							)
		if os.path.exists(_MODEL_PATH) and os.path.getsize(_MODEL_PATH) > 100000:
			# Translators: Success message after the Silero VAD model download completes.
			plugin_state.speak_status(_("Silero VAD model downloaded successfully!"))
			return _MODEL_PATH
		raise RuntimeError("Model download produced an empty or invalid file")
	except Exception as e:
		log.error("Silero VAD model download failed: {0}".format(e), exc_info=True)
		try:
			if os.path.exists(_MODEL_PATH):
				os.remove(_MODEL_PATH)
		except Exception:
			pass
		# Translators: Error dialog shown when the Silero VAD model download fails. {error} is the error details.
		wx.CallAfter(show_error_dialog, _("Failed to download Silero VAD model: {error}").format(error=str(e)))
		return None


def _ensure_installed():
	if "onnxruntime" in sys.modules:
		return True
	rdir = _install_runtime()
	if not rdir:
		return False
	if rdir not in sys.path:
		sys.path.insert(0, rdir)
	try:
		import numpy  # noqa: F401
		import onnxruntime  # noqa: F401

		return True
	except Exception as e:
		log.warning("VAD runtime import failed: {0}".format(e))
		return False


def _read_audio(np, wav_path, sr=16000):
	import wave as _wave

	try:
		with _wave.open(wav_path, "rb") as wf:
			fr = wf.getframerate()
			sw = wf.getsampwidth()
			nc = wf.getnchannels()
			raw = wf.readframes(wf.getnframes())
	except Exception:
		return None
	if sw != 2:
		return None
	arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / np.float32(32768.0)
	if nc > 1:
		arr = arr[0::nc]
	if fr != sr:
		n_out = int(len(arr) * sr / fr)
		x_old = np.arange(len(arr), dtype=np.float64)
		x_new = np.arange(n_out, dtype=np.float64) * (len(arr) - 1) / max(1, n_out - 1)
		arr = np.interp(x_new, x_old, arr.astype(np.float64)).astype(np.float32)
	return arr


def _vad_smoothed(np, sess, audio, sr=16000, frame_samples=512, context_samples=64):
	n_frames = (len(audio) - frame_samples) // frame_samples
	if n_frames < 2:
		return None
	state = np.zeros((2, 1, 128), dtype=np.float32)
	rate = np.asarray(sr, dtype=np.int64)
	prev_ctx = np.zeros(context_samples, dtype=np.float32)
	probs = np.empty(n_frames, dtype=np.float32)
	for i in range(n_frames):
		frame = audio[i * frame_samples : (i + 1) * frame_samples]
		model_input = np.concatenate((prev_ctx, frame)).reshape(1, -1)
		out, state = sess.run(
			["output", "stateN"],
			{"input": model_input, "state": state, "sr": rate},
		)
		probs[i] = float(out[0, 0])
		prev_ctx = frame[-context_samples:].copy()
		if i % 100 == 0:
			time.sleep(0)
	window = max(1, int(0.1 * sr / frame_samples))
	kernel = np.ones(window, dtype=np.float32) / window
	return np.convolve(probs, kernel, mode="same")


def _enhanced_audio(np, wav_path):
	ff = os.path.join(os.path.dirname(_VAD_DIR), "ffmpeg.exe")
	if not os.path.exists(ff):
		try:
			res = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
			if res.returncode != 0:
				return None
			ff = "ffmpeg"
		except Exception:
			return None
	tmp_wav = os.path.join(tempfile.gettempdir(), "va_vad_enhanced.wav")
	try:
		creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
		res = subprocess.run(
			[
				ff,
				"-y",
				"-i",
				wav_path,
				"-af",
				"dialoguenhance=original=0.1:enhance=3",
				"-ac",
				"1",
				"-ar",
				"16000",
				tmp_wav,
			],
			capture_output=True,
			timeout=600,
			creationflags=creationflags,
		)
		if res.returncode != 0 or not os.path.exists(tmp_wav):
			return None
		return _read_audio(np, tmp_wav, 16000)
	except Exception as e:
		log.debug("VAD enhanced pass failed: {0}".format(e))
		return None


def detect_silences(wav_path, min_duration=0.3, merge_gap_ms=150, margin_ms=80, window_ms=30):
	if not _ensure_installed():
		return None
	if not os.path.exists(_MODEL_PATH):
		if not _ensure_model():
			return None
	try:
		import numpy as np
		import onnxruntime as ort
	except Exception as e:
		log.warning("VAD import unavailable: {0}".format(e))
		return None

	try:
		sess = ort.InferenceSession(_MODEL_PATH, providers=["CPUExecutionProvider"])
		sr = 16000
		frame_samples = 512
		context_samples = 64
		audio = _read_audio(np, wav_path, sr)
		if audio is None:
			return None
		smoothed = _vad_smoothed(np, sess, audio, sr, frame_samples, context_samples)
		if smoothed is None:
			return None
		enh_audio = _enhanced_audio(np, wav_path)
		if enh_audio is not None:
			enh_smoothed = _vad_smoothed(np, sess, enh_audio, sr, frame_samples, context_samples)
			if enh_smoothed is not None and len(enh_smoothed) >= len(smoothed):
				smoothed = np.maximum(smoothed, enh_smoothed[: len(smoothed)])
		speech = smoothed > 0.5

		step_ms = frame_samples * 1000 / sr
		runs = []
		in_sil = False
		start = 0
		for i, is_sp in enumerate(speech):
			if not is_sp and not in_sil:
				in_sil = True
				start = i
			elif is_sp and in_sil:
				in_sil = False
				runs.append((start, i - 1))
		if in_sil:
			runs.append((start, len(speech) - 1))

		merged = []
		for s_idx, e_idx in runs:
			start_ms = int(s_idx * step_ms) + margin_ms
			end_ms = int((e_idx + 1) * step_ms) - margin_ms
			if merged and start_ms - merged[-1][1] <= merge_gap_ms:
				merged[-1] = (merged[-1][0], end_ms)
			else:
				merged.append((start_ms, end_ms))

		result = []
		for start_ms, end_ms in merged:
			if end_ms - start_ms >= min_duration * 1000:
				result.append((start_ms, end_ms))
		return result
	except Exception as e:
		log.warning("Silero VAD inference failed, falling back: {0}".format(e))
		return None
