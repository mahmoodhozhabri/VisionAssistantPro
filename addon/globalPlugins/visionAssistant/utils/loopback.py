# -*- coding: utf-8 -*-
import os
import sys
import array
import time
import logging
import zipfile
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
from .vad import _download_pypi_wheel
from .audio_dsp import _resample, _to_mono

log = logging.getLogger(__name__)

_ = vision_config._ if hasattr(vision_config, "_") else (lambda x: x)

_LOOPBACK_DIR = os.path.join(
	os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "loopback"
)
_PACKAGE = "PyAudioWPatch"
_TARGET_RATE = 16000


def _runtime_dir():
	return os.path.join(_LOOPBACK_DIR, "runtime")


def _ensure_runtime_dir():
	rdir = _runtime_dir()
	os.makedirs(rdir, exist_ok=True)
	return rdir


_download_approved = False


def _confirm_download():
	global _download_approved
	if _download_approved:
		return True
	# Translators: Title of dialog asking the user to download the system audio (loopback) support library.
	title = _("Download system audio support?")
	message = _(
		# Translators: Message in dialog asking the user to download the library used to capture the sound of the system speakers.
		"Capturing the system's sound requires an additional library (approximately 1MB download).\n\nDownload now to the addon's lib folder?\n\nThis is a one-time download."
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
		_download_approved = True
		return True
	# Translators: Message reported when the user cancels downloading the system audio support library.
	core.callLater(0, ui.message, _("Operation cancelled. System audio capture is unavailable."))
	return False


def _download_and_extract(url, dest_dir, marker_file):
	opener = get_proxy_opener(url)
	req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
	tmp = os.path.join(dest_dir, "download.tmp")
	with opener.open(req, timeout=600) as resp:
		total_size = int(resp.headers.get("content-length", 0))
		step = max(1, total_size // 10) if total_size > 0 else 0
		downloaded = 0
		with open(tmp, "wb") as f:
			while True:
				chunk = resp.read(1024 * 256)
				if not chunk:
					break
				f.write(chunk)
				downloaded += len(chunk)
				if step and downloaded % step < len(chunk):
					percent = int((downloaded / total_size) * 100)
					plugin_state.speak_status(
						# Translators: Spoken progress percentage during system audio loopback driver download. {percent} is the progress number.
						_("Downloading system audio support: {percent}%").format(percent=percent)
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
	if not _confirm_download():
		return None
	# Translators: Status message when downloading the system audio support library.
	plugin_state.speak_status(_("Downloading system audio support, please wait..."))
	try:
		url = _download_pypi_wheel(_PACKAGE)
		_download_and_extract(url, rdir, os.path.join(rdir, "pyaudiowpatch", "__init__.py"))
		with open(marker, "w") as mf:
			mf.write("ok")
		# Translators: Success message after the system audio support download completes.
		plugin_state.speak_status(_("System audio support downloaded successfully!"))
		return rdir
	except Exception as e:
		log.error("System audio support download failed: {0}".format(e), exc_info=True)
		wx.CallAfter(
			show_error_dialog,
			# Translators: Error dialog shown when system audio loopback download fails. {error} is the error details.
			_("Failed to download system audio support: {error}").format(error=str(e)),
		)
		return None


def _ensure_installed():
	if "pyaudiowpatch" in sys.modules:
		return True
	rdir = _install_runtime()
	if not rdir:
		return False
	if rdir not in sys.path:
		sys.path.insert(0, rdir)
	try:
		import pyaudiowpatch  # noqa: F401

		return True
	except Exception as e:
		log.warning("System audio runtime import failed: {0}".format(e))
		return False


class SystemAudioCapture:
	def __init__(self, on_data, sample_rate=_TARGET_RATE, block_ms=100):
		self.on_data = on_data
		self.sample_rate = sample_rate
		self.block_size = int(sample_rate * 2 * block_ms / 1000)
		self._pa = None
		self._stream = None
		self._running = False
		self._thread = None
		self._src_rate = 0
		self._channels = 0
		self._frames = 0

	def _default_loopback(self, pyaudio):
		try:
			return pyaudio.get_default_wasapi_loopback()
		except Exception as e:
			log.debug("Default loopback device lookup failed: {0}".format(e))
		try:
			for info in pyaudio.get_loopback_device_info_generator():
				return info
		except Exception as e:
			log.debug("Loopback device enumeration failed: {0}".format(e))
		return None

	def start(self):
		if not _ensure_installed():
			raise OSError("System audio support is not available")
		import pyaudiowpatch as pyaudio

		self._pa = pyaudio.PyAudio()
		device = self._default_loopback(self._pa)
		if not device:
			raise OSError("No WASAPI loopback device found")
		self._src_rate = int(device.get("defaultSampleRate", 48000))
		self._channels = int(device.get("maxInputChannels", 2)) or 1
		self._read_frames = max(240, int(self._src_rate * 0.02))
		self._chunk_frames = max(1, int(self._src_rate * 0.1))
		self._pending = array.array("h")
		self._stream = self._pa.open(
			format=pyaudio.paInt16,
			channels=self._channels,
			rate=self._src_rate,
			input=True,
			input_device_index=device["index"],
			frames_per_buffer=self._read_frames,
		)
		self._running = True
		self._thread = threading.Thread(target=self._loop, daemon=True)
		self._thread.start()

	def _loop(self):
		while self._running:
			try:
				data = self._stream.read(self._read_frames, exception_on_overflow=False)
			except Exception as e:
				log.debug("System audio read failed: {0}".format(e))
				break
			if not self.on_data:
				continue
			try:
				frame_bytes = 2 * self._channels
				if len(data) % frame_bytes:
					data = data[: len(data) - (len(data) % frame_bytes)]
				samples = array.array("h")
				samples.frombytes(data)
				mono = _to_mono(samples, self._channels)
				self._pending.extend(mono)
				while len(self._pending) >= self._chunk_frames:
					block = self._pending[: self._chunk_frames]
					self._pending = array.array("h", self._pending[self._chunk_frames :])
					resampled = _resample(block, self._src_rate, self.sample_rate)
					if resampled:
						self.on_data(resampled.tobytes())
			except Exception as e:
				log.debug("System audio conversion failed: {0}".format(e))

	def stop(self):
		self._running = False
		if self._thread:
			self._thread.join(timeout=2)
		if self._stream:
			try:
				if not self._stream.is_stopped():
					self._stream.stop_stream()
				self._stream.close()
			except Exception as e:
				log.debug("System audio stream close failed: {0}".format(e))
			self._stream = None
		if self._pa:
			try:
				self._pa.terminate()
			except Exception as e:
				log.debug("System audio terminate failed: {0}".format(e))
			self._pa = None


class SilenceCapture:
	def __init__(self, on_data, sample_rate=16000, block_ms=100, interval_s=0.1):
		self.on_data = on_data
		self.block_size = int(sample_rate * 2 * block_ms / 1000)
		self._silence = bytes(self.block_size)
		self.interval_s = max(0.02, float(interval_s))
		self._running = False
		self._thread = None

	def start(self):
		self._running = True
		self._thread = threading.Thread(target=self._loop, daemon=True)
		self._thread.start()

	def _loop(self):
		while self._running:
			if self.on_data:
				try:
					self.on_data(self._silence)
				except Exception as e:
					log.debug("Silence stream callback failed: {0}".format(e))
			deadline = time.time() + self.interval_s
			while self._running and time.time() < deadline:
				time.sleep(0.02)

	def stop(self):
		self._running = False
		if self._thread:
			self._thread.join(timeout=1)


def _create_process_capture(on_data):
	try:
		from .proc_loopback import ProcessLoopbackCapture

		capture = ProcessLoopbackCapture(on_data, exclude=True)
		capture.start()
		log.debug("System audio capture started in process mode with own audio excluded")
		return capture
	except Exception as e:
		log.debug("Process loopback unavailable; falling back to whole-system loopback: {0}".format(e))
		return None


def create_capture(source, on_data, silence_interval_s=0.1):
	if source == "silence":
		return SilenceCapture(on_data, interval_s=silence_interval_s)
	if source == "system":
		capture = _create_process_capture(on_data)
		if capture:
			return capture
		return SystemAudioCapture(on_data)
	from .media_capture import _MicCapture

	return _MicCapture(on_data)