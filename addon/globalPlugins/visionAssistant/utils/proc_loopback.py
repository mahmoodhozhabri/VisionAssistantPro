# -*- coding: utf-8 -*-
import array
import ctypes
import logging
import os
import threading
from ctypes import POINTER, Structure, byref, c_void_p
from ctypes.wintypes import DWORD

from .audio_dsp import _resample

log = logging.getLogger(__name__)

COINIT_MULTITHREADED = 0x0
VIRTUAL_AUDIO_DEVICE_PROCESS_LOOPBACK = "VAD\\Process_Loopback"

AUDCLNT_SHAREMODE_SHARED = 0
AUDCLNT_STREAMFLAGS_LOOPBACK = 0x00020000
AUDCLNT_STREAMFLAGS_EVENTCALLBACK = 0x00040000
AUDCLNT_BUFFERFLAGS_SILENT = 0x2
WAVE_FORMAT_IEEE_FLOAT = 3

AUDIOCLIENT_ACTIVATION_TYPE_PROCESS_LOOPBACK = 1
PROCESS_LOOPBACK_MODE_INCLUDE_TARGET_PROCESS_TREE = 0
PROCESS_LOOPBACK_MODE_EXCLUDE_TARGET_PROCESS_TREE = 1

INFINITE = 0xFFFFFFFF
_REFERENCE_TIME = ctypes.c_longlong


class GUID(Structure):
	_fields_ = [
		("Data1", ctypes.c_ulong),
		("Data2", ctypes.c_ushort),
		("Data3", ctypes.c_ushort),
		("Data4", ctypes.c_ubyte * 8),
	]


def _guid(text):
	parts = text.strip("{}").split("-")
	data4 = (ctypes.c_ubyte * 8).from_buffer_copy(bytes.fromhex(parts[3] + parts[4]))
	return GUID(int(parts[0], 16), int(parts[1], 16), int(parts[2], 16), data4)


IID_IAudioClient = _guid("{1CB9AD4C-DBFA-4C32-B178-C2F568A703B2}")
IID_IAudioCaptureClient = _guid("{C8ADBD64-E71E-48A0-A4DE-185C395CD317}")
IID_ICompletionHandler = _guid("{41D949AB-9862-444A-80F6-C261334DA5EB}")


class AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS(Structure):
	_fields_ = [("TargetProcessId", DWORD), ("ProcessLoopbackMode", ctypes.c_int)]


class AUDIOCLIENT_ACTIVATION_PARAMS(Structure):
	_fields_ = [
		("ActivationType", ctypes.c_int),
		("ProcessLoopbackParams", AUDIOCLIENT_PROCESS_LOOPBACK_PARAMS),
	]


class WAVEFORMATEX(Structure):
	_fields_ = [
		("wFormatTag", ctypes.c_ushort),
		("nChannels", ctypes.c_ushort),
		("nSamplesPerSec", DWORD),
		("nAvgBytesPerSec", DWORD),
		("nBlockAlign", ctypes.c_ushort),
		("wBitsPerSample", ctypes.c_ushort),
		("cbSize", ctypes.c_ushort),
	]


VT_BLOB = 65


class _PropVariantBlob(Structure):
	_fields_ = [("cbSize", ctypes.c_ulong), ("pBlobData", c_void_p)]


class PROPVARIANT(Structure):
	_fields_ = [
		("vt", ctypes.c_ushort),
		("wReserved1", ctypes.c_ushort),
		("wReserved2", ctypes.c_ushort),
		("wReserved3", ctypes.c_ushort),
		("blob", _PropVariantBlob),
	]

IID_IUnknown = _guid("{00000000-0000-0000-C000-000000000046}")
IID_IMarshal = _guid("{00000003-0000-0000-C000-000000000046}")
IID_IAgileObject = _guid("{94EA2B94-E9CC-49E0-C0FF-EE64CA8F5B90}")


def _vtable(ptr):
	return ctypes.cast(ptr, POINTER(POINTER(c_void_p)))[0]


def _query_interface(ptr, iid):
	if not ptr:
		return None
	out = c_void_p()
	fn = ctypes.WINFUNCTYPE(ctypes.c_long, c_void_p, POINTER(GUID), POINTER(c_void_p))(_vtable(ptr)[0])
	hr = fn(ptr, byref(iid), byref(out))
	if hr != 0 or not out:
		raise OSError("QueryInterface failed: 0x{0:08X}".format(hr & 0xFFFFFFFF))
	return out


class _ComInterface:
	def __init__(self, ptr):
		self.ptr = ptr
		self._cache = {}

	def _fn(self, index, *argtypes):
		fn = self._cache.get(index)
		if fn is None:
			fn = ctypes.WINFUNCTYPE(ctypes.c_long, c_void_p, *argtypes)(_vtable(self.ptr)[index])
			self._cache[index] = fn
		return fn

	def Release(self):
		try:
			fn = ctypes.WINFUNCTYPE(ctypes.c_ulong, c_void_p)(_vtable(self.ptr)[2])
			fn(self.ptr)
		except Exception as e:
			log.debug("COM release failed: {0}".format(e))


class IAudioClient(_ComInterface):
	def Initialize(self, flags, duration, fmt):
		fn = self._fn(
			3,
			ctypes.c_int,
			DWORD,
			_REFERENCE_TIME,
			_REFERENCE_TIME,
			POINTER(WAVEFORMATEX),
			c_void_p,
		)
		return fn(self.ptr, AUDCLNT_SHAREMODE_SHARED, flags, duration, 0, byref(fmt), None)

	def GetBufferSize(self):
		size = DWORD()
		self._fn(4, POINTER(DWORD))(self.ptr, byref(size))
		return size.value

	def SetEventHandle(self, handle):
		return self._fn(13, c_void_p)(self.ptr, handle)

	def GetService(self, iid):
		ptr = c_void_p()
		hr = self._fn(14, POINTER(GUID), POINTER(c_void_p))(self.ptr, byref(iid), byref(ptr))
		if hr != 0 or not ptr:
			raise OSError("GetService failed: 0x{0:08X}".format(hr & 0xFFFFFFFF))
		return ptr

	def Start(self):
		return self._fn(10)(self.ptr)

	def Stop(self):
		return self._fn(11)(self.ptr)


class IAudioCaptureClient(_ComInterface):
	def GetBuffer(self):
		data = c_void_p()
		frames = ctypes.c_uint32()
		flags = DWORD()
		fn = self._fn(
			3,
			POINTER(c_void_p),
			POINTER(ctypes.c_uint32),
			POINTER(DWORD),
			c_void_p,
			c_void_p,
		)
		hr = fn(self.ptr, byref(data), byref(frames), byref(flags), None, None)
		return hr, data, frames.value, flags.value

	def ReleaseBuffer(self, frames):
		return self._fn(4, ctypes.c_uint32)(self.ptr, frames)

	def GetNextPacketSize(self):
		size = ctypes.c_uint32()
		self._fn(5, POINTER(ctypes.c_uint32))(self.ptr, byref(size))
		return size.value


class _ActivateOperation(_ComInterface):
	def GetActivateResult(self, activate_result, activated_interface):
		fn = self._fn(3, POINTER(ctypes.c_long), POINTER(c_void_p))
		return fn(self.ptr, activate_result, activated_interface)


_CompletionCallback = ctypes.WINFUNCTYPE(ctypes.c_long, c_void_p, c_void_p)
E_NOINTERFACE = 0x80004002


class _HandlerVtbl(Structure):
	_fields_ = [
		("QueryInterface", ctypes.WINFUNCTYPE(ctypes.c_long, c_void_p, POINTER(GUID), POINTER(c_void_p))),
		("AddRef", ctypes.WINFUNCTYPE(ctypes.c_ulong, c_void_p)),
		("Release", ctypes.WINFUNCTYPE(ctypes.c_ulong, c_void_p)),
		("ActivateCompleted", _CompletionCallback),
	]


class _HandlerStruct(Structure):
	_fields_ = [("vtbl", POINTER(_HandlerVtbl))]


def _same_guid(a, b):
	return ctypes.string_at(byref(a), ctypes.sizeof(GUID)) == ctypes.string_at(byref(b), ctypes.sizeof(GUID))


class _ActivationHandler:
	def __init__(self, on_completed):
		self._on_completed = on_completed
		self._refs = 1
		self._query_cb = ctypes.WINFUNCTYPE(ctypes.c_long, c_void_p, POINTER(GUID), POINTER(c_void_p))(
			self._query_interface
		)
		self._addref_cb = ctypes.WINFUNCTYPE(ctypes.c_ulong, c_void_p)(self._add_ref)
		self._release_cb = ctypes.WINFUNCTYPE(ctypes.c_ulong, c_void_p)(self._release_ref)
		self._completed_cb = _CompletionCallback(self._activate_completed)
		self._vtbl = _HandlerVtbl(
			self._query_cb, self._addref_cb, self._release_cb, self._completed_cb
		)
		self.struct = _HandlerStruct(ctypes.pointer(self._vtbl))
		self.pointer = ctypes.cast(ctypes.pointer(self.struct), c_void_p)
		self._ftm = None
		try:
			ftm = c_void_p()
			hr = ctypes.windll.ole32.CoCreateFreeThreadedMarshaler(self.pointer, byref(ftm))
			if hr == 0 and ftm:
				self._ftm = ftm
			else:
				log.debug("CoCreateFreeThreadedMarshaler failed: 0x{0:08X}".format(hr & 0xFFFFFFFF))
		except Exception as e:
			log.debug("Free-threaded marshaler creation failed: {0}".format(e))

	def _query_interface(self, this, riid, ppv):
		try:
			if not ppv:
				return 0
			if riid:
				iid = riid[0]
				if _same_guid(iid, IID_IMarshal):
					if self._ftm:
						fn = ctypes.WINFUNCTYPE(
							ctypes.c_long, c_void_p, POINTER(GUID), POINTER(c_void_p)
						)(_vtable(self._ftm)[0])
						return fn(self._ftm, riid, ppv)
					return E_NOINTERFACE
				if not (
					_same_guid(iid, IID_IUnknown)
					or _same_guid(iid, IID_ICompletionHandler)
					or _same_guid(iid, IID_IAgileObject)
				):
					return E_NOINTERFACE
			ppv[0] = self.pointer
		except Exception as e:
			log.debug("Handler QueryInterface failed: {0}".format(e))
		return 0

	def _add_ref(self, this):
		self._refs += 1
		return self._refs

	def _release_ref(self, this):
		self._refs -= 1
		return self._refs

	def _activate_completed(self, this, operation):
		try:
			self._on_completed(operation)
		except Exception as e:
			log.debug("Activation completion callback failed: {0}".format(e))
		return 0


def _activate_client(pid, mode, timeout=10.0):
	mmdevapi = ctypes.WinDLL("Mmdevapi.dll")
	proto = ctypes.WINFUNCTYPE(
		ctypes.c_long,
		ctypes.c_wchar_p,
		POINTER(GUID),
		POINTER(PROPVARIANT),
		c_void_p,
		POINTER(c_void_p),
	)
	activate = proto(("ActivateAudioInterfaceAsync", mmdevapi))

	params = AUDIOCLIENT_ACTIVATION_PARAMS()
	params.ActivationType = AUDIOCLIENT_ACTIVATION_TYPE_PROCESS_LOOPBACK
	params.ProcessLoopbackParams.TargetProcessId = int(pid)
	params.ProcessLoopbackParams.ProcessLoopbackMode = int(mode)

	var = PROPVARIANT()
	var.vt = VT_BLOB
	var.blob.cbSize = ctypes.sizeof(AUDIOCLIENT_ACTIVATION_PARAMS)
	var.blob.pBlobData = ctypes.cast(ctypes.pointer(params), c_void_p)

	result = {}
	kernel32 = ctypes.windll.kernel32
	event = kernel32.CreateEventW(None, False, False, None)
	if not event:
		raise OSError("CreateEventW failed")

	def on_completed(operation_ptr):
		try:
			operation = _ActivateOperation(c_void_p(operation_ptr))
			activate_result = ctypes.c_long()
			unknown = c_void_p()
			hr = operation.GetActivateResult(byref(activate_result), byref(unknown))
			log.debug(
				"Process loopback activation callback: hr=0x{0:08X} result=0x{1:08X}".format(
					hr & 0xFFFFFFFF, activate_result.value & 0xFFFFFFFF
				)
			)
			result["hr"] = hr
			result["activate_result"] = activate_result.value
			result["interface"] = unknown
		except Exception as e:
			log.debug("Activation callback failed: {0}".format(e))
			result["error"] = e
		finally:
			kernel32.SetEvent(event)

	handler = _ActivationHandler(on_completed)
	operation_ptr = c_void_p()
	hr = activate(
		VIRTUAL_AUDIO_DEVICE_PROCESS_LOOPBACK,
		byref(IID_IAudioClient),
		byref(var),
		handler.pointer,
		byref(operation_ptr),
	)
	if hr != 0:
		kernel32.CloseHandle(event)
		raise OSError("ActivateAudioInterfaceAsync failed: 0x{0:08X}".format(hr & 0xFFFFFFFF))
	waited = kernel32.WaitForSingleObject(event, int(timeout * 1000))
	kernel32.CloseHandle(event)
	if waited != 0:
		raise OSError("Timed out waiting for the process loopback activation")
	if "error" in result:
		raise result["error"]
	if result.get("hr", 0) != 0:
		raise OSError("Activation result failed: 0x{0:08X}".format(result["hr"] & 0xFFFFFFFF))
	interface = result.get("interface")
	if not interface:
		raise OSError(
			"Activation returned no audio client: 0x{0:08X}".format(
				result.get("activate_result", 0) & 0xFFFFFFFF
			)
		)
	client_ptr = _query_interface(interface, IID_IAudioClient)
	return IAudioClient(client_ptr)


class ProcessLoopbackCapture:
	CHANNELS = 2
	RATE = 48000
	BITS_PER_SAMPLE = 32
	BUFFER_DURATION = 200000

	def __init__(self, on_data, target_pid=None, exclude=True, sample_rate=16000, block_ms=100):
		self.on_data = on_data
		self.sample_rate = sample_rate
		self.target_pid = int(target_pid if target_pid is not None else os.getpid())
		self.exclude = bool(exclude)
		self.mode = (
			PROCESS_LOOPBACK_MODE_EXCLUDE_TARGET_PROCESS_TREE
			if self.exclude
			else PROCESS_LOOPBACK_MODE_INCLUDE_TARGET_PROCESS_TREE
		)
		self.chunk_frames = max(1, int(self.RATE * block_ms / 1000))
		self._pending = array.array("h")
		self._running = False
		self._ready = threading.Event()
		self._error = None
		self._thread = None
		self._client = None
		self._capture = None
		self._buffer_event = None
		self._resample = None

	def start(self):
		self._running = True
		self._ready = threading.Event()
		self._error = None
		self._thread = threading.Thread(target=self._run, daemon=True)
		self._thread.start()
		if not self._ready.wait(timeout=12):
			self._running = False
			raise OSError("The process loopback capture did not start in time")
		if self._error:
			raise self._error

	def _build_format(self):
		block_align = self.CHANNELS * (self.BITS_PER_SAMPLE // 8)
		return WAVEFORMATEX(
			wFormatTag=WAVE_FORMAT_IEEE_FLOAT,
			nChannels=self.CHANNELS,
			nSamplesPerSec=self.RATE,
			nAvgBytesPerSec=self.RATE * block_align,
			nBlockAlign=block_align,
			wBitsPerSample=self.BITS_PER_SAMPLE,
			cbSize=0,
		)

	def _run(self):
		ole32 = ctypes.windll.ole32
		kernel32 = ctypes.windll.kernel32
		ole32.CoInitializeEx(None, COINIT_MULTITHREADED)
		try:
			client = _activate_client(self.target_pid, self.mode)
			flags = AUDCLNT_STREAMFLAGS_LOOPBACK | AUDCLNT_STREAMFLAGS_EVENTCALLBACK
			hr = client.Initialize(flags, self.BUFFER_DURATION, self._build_format())
			if hr != 0:
				client.Release()
				raise OSError("Audio client initialize failed: 0x{0:08X}".format(hr & 0xFFFFFFFF))
			self._buffer_event = kernel32.CreateEventW(None, False, False, None)
			if not self._buffer_event:
				client.Release()
				raise OSError("CreateEventW for the audio buffer failed")
			hr = client.SetEventHandle(self._buffer_event)
			if hr != 0:
				client.Release()
				raise OSError("SetEventHandle failed: 0x{0:08X}".format(hr & 0xFFFFFFFF))
			self._capture = IAudioCaptureClient(client.GetService(IID_IAudioCaptureClient))
			self._client = client
			hr = client.Start()
			if hr != 0:
				raise OSError("Audio client start failed: 0x{0:08X}".format(hr & 0xFFFFFFFF))
			self._ready.set()
			self._loop()
		except Exception as e:
			log.debug("Process loopback capture failed: {0}".format(e))
			self._error = e
			self._ready.set()
		finally:
			self._cleanup()
			try:
				ole32.CoUninitialize()
			except Exception as e:
				log.debug("CoUninitialize failed: {0}".format(e))

	def _loop(self):
		kernel32 = ctypes.windll.kernel32
		while self._running:
			if kernel32.WaitForSingleObject(self._buffer_event, 200) != 0:
				continue
			packet = self._capture.GetNextPacketSize()
			while packet and self._running:
				hr, data, frames, flags = self._capture.GetBuffer()
				if hr == 0 and frames:
					self._consume(data, frames, flags)
				self._capture.ReleaseBuffer(frames)
				packet = self._capture.GetNextPacketSize()

	def _consume(self, data, frames, flags):
		if flags & AUDCLNT_BUFFERFLAGS_SILENT or not data:
			self._pending.extend(array.array("h", bytes(frames * 2)))
		else:
			size = frames * self.CHANNELS * (self.BITS_PER_SAMPLE // 8)
			raw = ctypes.string_at(data, size)
			floats = array.array("f")
			floats.frombytes(raw)
			if self.CHANNELS > 1:
				floats = floats[0 :: self.CHANNELS]
			for value in floats:
				sample = int(value * 32767.0)
				if sample > 32767:
					sample = 32767
				elif sample < -32768:
					sample = -32768
				self._pending.append(sample)
		self._flush()

	def _flush(self):
		while len(self._pending) >= self.chunk_frames:
			block = self._pending[: self.chunk_frames]
			self._pending = array.array("h", self._pending[self.chunk_frames :])
			resampled = _resample(block, self.RATE, self.sample_rate)
			if resampled and self.on_data:
				self.on_data(resampled.tobytes())

	def _cleanup(self):
		kernel32 = ctypes.windll.kernel32
		if self._client:
			try:
				self._client.Stop()
			except Exception as e:
				log.debug("Audio client stop failed: {0}".format(e))
		if self._capture:
			self._capture.Release()
			self._capture = None
		if self._client:
			self._client.Release()
			self._client = None
		if self._buffer_event:
			try:
				kernel32.CloseHandle(self._buffer_event)
			except Exception as e:
				log.debug("Audio buffer event close failed: {0}".format(e))
			self._buffer_event = None

	def stop(self):
		self._running = False
		if self._thread:
			self._thread.join(timeout=4)
		self._thread = None


def is_supported(pid=None):
	result = {}

	def worker():
		ole32 = ctypes.windll.ole32
		ole32.CoInitializeEx(None, COINIT_MULTITHREADED)
		try:
			target = os.getpid() if pid is None else int(pid)
			client = _activate_client(target, PROCESS_LOOPBACK_MODE_EXCLUDE_TARGET_PROCESS_TREE)
			client.Release()
			result["ok"] = True
		except Exception as e:
			log.debug("Process loopback is not available: {0}".format(e))
			result["ok"] = False
		finally:
			try:
				ole32.CoUninitialize()
			except Exception as e:
				log.debug("CoUninitialize failed: {0}".format(e))

	thread = threading.Thread(target=worker, daemon=True)
	thread.start()
	thread.join(timeout=15)
	return bool(result.get("ok"))