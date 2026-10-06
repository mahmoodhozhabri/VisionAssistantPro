# -*- coding: utf-8 -*-
import os
import json
import ssl
import socket
import struct
import time
import re
import base64
import threading
import tempfile
import ctypes
import logging
import urllib.parse
import wx
from urllib import request, error
from urllib.parse import urlparse, urlencode
from http import cookiejar
import http.client

import subprocess
import sys
import zipfile
import shutil

import config as _real_config


class _ConfigProxy:
	def __getattr__(self, name):
		import sys

		cfg = sys.modules.get("config")
		if cfg is not None and hasattr(cfg, name):
			return getattr(cfg, name)
		return getattr(_real_config, name)


nvda_config = _ConfigProxy()
import gui
import core
import ui

from .. import plugin_state
from .. import vision_config
from .system import show_error_dialog

log = logging.getLogger(__name__)

_ = vision_config._ if hasattr(vision_config, "_") else (lambda x: x)

LIVE_MODEL_38 = "gemini-3.8-live"


def live_thinking_supported(model):
	low = (model or "").lower()
	if low.startswith(LIVE_MODEL_38) and "extended" not in low:
		return False
	return True


def live_thinking_level(model, level):
	low = (model or "").lower()
	chosen = (level or "").strip().lower()
	if chosen not in ("minimal", "low", "medium", "high"):
		chosen = "medium"
	if "extended-thinking" in low and chosen == "minimal":
		return "low"
	return chosen


def live_resumption_supported(model):
	return (model or "").lower().startswith(LIVE_MODEL_38)


def live_thinking_choices(model):
	choices = list(vision_config.LIVE_THINKING_CHOICES)
	if "extended-thinking" in (model or "").lower():
		choices = [choice for choice in choices if choice[1] != "minimal"]
	return choices


def resolve_live_model():
	conf = nvda_config.conf["VisionAssistant"]
	provider = conf.get("active_provider") or "gemini"
	model = ""
	if conf.get("advanced_model_routing", False):
		model = conf.get(f"{provider}_live_model", "").strip()
	if (
		not model
		or model.lower() in ("", "auto", "default")
		or "auto" in model.lower()
		or "default" in model.lower()
	):
		return vision_config.DEFAULT_LIVE_MODEL
	if "live" not in model.lower() and "native" not in model.lower():
		log.warning(
			f"Live: selected model '{model}' is not a Live model; using '{vision_config.DEFAULT_LIVE_MODEL}'.",
		)
		return vision_config.DEFAULT_LIVE_MODEL
	return model


# Proxy / HTTP helpers

_PROBED_PROXIES = {}


def detect_proxy_type(host, port, timeout=1.5):
	key = (host, port)
	if key in _PROBED_PROXIES:
		return _PROBED_PROXIES[key]
	if port in (10808, 1080, 2080, 9050):
		_PROBED_PROXIES[key] = "socks5"
		return "socks5"
	if port in (10809, 2081, 8080, 8888, 3128):
		_PROBED_PROXIES[key] = "http"
		return "http"
	try:
		s = socket.create_connection((host, port), timeout=timeout)
		s.sendall(b"\x05\x01\x00")
		res = s.recv(2)
		s.close()
		if len(res) >= 2 and res[0] == 5:
			_PROBED_PROXIES[key] = "socks5"
			return "socks5"
	except Exception:
		pass
	_PROBED_PROXIES[key] = "http"
	return "http"


def parse_proxy_settings():
	try:
		cfg = sys.modules.get("config", nvda_config)
		conf = getattr(cfg, "conf", None)
		if conf is None:
			return None
		va_conf = conf.get("VisionAssistant") if hasattr(conf, "get") else conf["VisionAssistant"]
	except Exception:
		return None
	if not va_conf:
		return None

	raw_url = va_conf.get("proxy_url", "") if hasattr(va_conf, "get") else ""
	if not isinstance(raw_url, str):
		raw_url = ""
	raw_url = raw_url.strip()

	mode = va_conf.get("proxy_mode", "auto") if hasattr(va_conf, "get") else "auto"
	if not isinstance(mode, str):
		mode = "auto"
	mode = mode.strip().lower()

	cfg_user = va_conf.get("proxy_username", "") if hasattr(va_conf, "get") else ""
	if not isinstance(cfg_user, str):
		cfg_user = ""
	cfg_user = cfg_user.strip()

	cfg_pass = va_conf.get("proxy_password", "") if hasattr(va_conf, "get") else ""
	if not isinstance(cfg_pass, str):
		cfg_pass = ""
	cfg_pass = cfg_pass.strip()

	if not raw_url:
		return None

	scheme = ""
	if "://" in raw_url:
		scheme, rest = raw_url.split("://", 1)
		scheme = scheme.lower()
	else:
		rest = raw_url

	parsed = urlparse("http://" + rest)
	user = parsed.username or cfg_user
	password = parsed.password or cfg_pass
	host = parsed.hostname or ""
	port = parsed.port

	is_reverse = False
	if mode == "reverse":
		is_reverse = True
	elif mode in ("forward", "socks5", "http"):
		is_reverse = False
		if mode == "socks5":
			scheme = "socks5"
		elif mode == "http":
			scheme = "http"
	else:
		if "socks" in scheme:
			is_reverse = False
		elif host.lower() in ["localhost", "127.0.0.1"]:
			is_reverse = False
		elif host and "." in host and not host.replace(".", "").isdigit():
			is_reverse = True
		else:
			is_reverse = False

	if not scheme:
		if is_reverse:
			if host.replace(".", "").isdigit() or host.lower() in ["localhost", "127.0.0.1"]:
				scheme = "https" if port == 443 else "http"
			else:
				scheme = "http" if port == 80 else "https"
		elif port and detect_proxy_type(host, port) == "socks5":
			scheme = "socks5"
		else:
			scheme = "http"

	clean_netloc = host
	if port:
		clean_netloc += f":{port}"

	return {
		"raw_url": raw_url,
		"scheme": scheme,
		"host": host,
		"port": port,
		"user": user,
		"password": password,
		"mode": mode,
		"is_reverse": is_reverse,
		"clean_url": f"{scheme}://{clean_netloc}",
	}


class SOCKS5HTTPConnection(http.client.HTTPConnection):
	def __init__(self, proxy_host, proxy_port, proxy_user, proxy_pass, host, port=None, timeout=30):
		super().__init__(host, port=port, timeout=timeout)
		self.proxy_host = proxy_host
		self.proxy_port = proxy_port
		self.proxy_user = proxy_user
		self.proxy_pass = proxy_pass

	def connect(self):
		s = socket.create_connection((self.proxy_host, self.proxy_port or 1080), timeout=self.timeout)
		if self.proxy_user and self.proxy_pass:
			s.sendall(b"\x05\x02\x00\x02")
			res = s.recv(2)
			if len(res) >= 2 and res[1] == 2:
				u = self.proxy_user.encode("utf-8")
				p = self.proxy_pass.encode("utf-8")
				s.sendall(struct.pack("BB", 1, len(u)) + u + struct.pack("B", len(p)) + p)
				auth_res = s.recv(2)
				if len(auth_res) < 2 or auth_res[1] != 0:
					s.close()
					raise ConnectionError("SOCKS5 authentication failed")
		else:
			s.sendall(b"\x05\x01\x00")
			res = s.recv(2)
		if len(res) < 2 or res[0] != 5:
			s.close()
			raise ConnectionError("SOCKS5 proxy returned invalid response")
		host_b = self.host.encode("idna")
		s.sendall(
			struct.pack(">BBBB", 5, 1, 0, 3)
			+ struct.pack("B", len(host_b))
			+ host_b
			+ struct.pack(">H", self.port or 80),
		)
		resp = s.recv(10)
		if len(resp) < 4 or resp[1] != 0:
			s.close()
			raise ConnectionError(
				f"SOCKS5 proxy connection failed with status code {resp[1] if len(resp) >= 2 else 'unknown'}",
			)
		self.sock = s


class SOCKS5HTTPSConnection(http.client.HTTPSConnection):
	def __init__(
		self, proxy_host, proxy_port, proxy_user, proxy_pass, host, port=None, timeout=30, context=None
	):
		super().__init__(host, port=port, timeout=timeout, context=context)
		self.proxy_host = proxy_host
		self.proxy_port = proxy_port
		self.proxy_user = proxy_user
		self.proxy_pass = proxy_pass

	def connect(self):
		s = socket.create_connection((self.proxy_host, self.proxy_port or 1080), timeout=self.timeout)
		if self.proxy_user and self.proxy_pass:
			s.sendall(b"\x05\x02\x00\x02")
			res = s.recv(2)
			if len(res) >= 2 and res[1] == 2:
				u = self.proxy_user.encode("utf-8")
				p = self.proxy_pass.encode("utf-8")
				s.sendall(struct.pack("BB", 1, len(u)) + u + struct.pack("B", len(p)) + p)
				auth_res = s.recv(2)
				if len(auth_res) < 2 or auth_res[1] != 0:
					s.close()
					raise ConnectionError("SOCKS5 authentication failed")
		else:
			s.sendall(b"\x05\x01\x00")
			res = s.recv(2)
		if len(res) < 2 or res[0] != 5:
			s.close()
			raise ConnectionError("SOCKS5 proxy returned invalid response")
		host_b = self.host.encode("idna")
		s.sendall(
			struct.pack(">BBBB", 5, 1, 0, 3)
			+ struct.pack("B", len(host_b))
			+ host_b
			+ struct.pack(">H", self.port or 443),
		)
		resp = s.recv(10)
		if len(resp) < 4 or resp[1] != 0:
			s.close()
			raise ConnectionError(
				f"SOCKS5 proxy connection failed with status code {resp[1] if len(resp) >= 2 else 'unknown'}",
			)
		ctx = self._context or ssl.create_default_context()
		self.sock = ctx.wrap_socket(s, server_hostname=self.host)


class _SOCKS5Handler(request.HTTPHandler, request.HTTPSHandler):
	def __init__(self, proxy_host, proxy_port, proxy_user=None, proxy_pass=None):
		self.proxy_host = proxy_host
		self.proxy_port = proxy_port
		self.proxy_user = proxy_user
		self.proxy_pass = proxy_pass
		super().__init__()

	def http_open(self, req):
		return self.do_open(
			lambda host, **kwargs: SOCKS5HTTPConnection(
				self.proxy_host,
				self.proxy_port,
				self.proxy_user,
				self.proxy_pass,
				host,
				**kwargs,
			),
			req,
		)

	def https_open(self, req):
		return self.do_open(
			lambda host, **kwargs: SOCKS5HTTPSConnection(
				self.proxy_host,
				self.proxy_port,
				self.proxy_user,
				self.proxy_pass,
				host,
				**kwargs,
			),
			req,
		)


def get_proxy_opener(target_url=None):
	is_local = False
	if target_url:
		parsed_target = urlparse(target_url)
		hostname = parsed_target.hostname or ""
		if hostname.lower() in ["localhost", "127.0.0.1"]:
			is_local = True

	p = parse_proxy_settings()
	if is_local or (p and p["is_reverse"]):
		opener = request.build_opener(request.ProxyHandler({}))
	elif p:
		try:
			if "socks" in p["scheme"]:
				opener = request.build_opener(
					_SOCKS5Handler(p["host"], p["port"] or 1080, p["user"], p["password"]),
				)
			else:
				clean_url = f"http://{p['host']}" + (f":{p['port']}" if p["port"] else "")
				handler = request.ProxyHandler({"http": clean_url, "https": clean_url})
				opener = request.build_opener(handler)
				if p["user"]:
					auth_str = f"{p['user']}:{p['password'] or ''}"
					encoded_auth = base64.b64encode(auth_str.encode()).decode()
					opener.addheaders.append(("Proxy-Authorization", f"Basic {encoded_auth}"))
		except Exception as e:
			log.error(f"Proxy Setup Failed: {e}")
			opener = request.build_opener()
	else:
		opener = request.build_opener()
		try:
			sys_proxies = request.getproxies()
			if sys_proxies:
				opener = request.build_opener(request.ProxyHandler(sys_proxies))
		except Exception:
			pass

	opener.addheaders = [h for h in opener.addheaders if h[0].lower() != "user-agent"]
	opener.addheaders.append(
		(
			"User-Agent",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
		),
	)
	return opener


def test_proxy_connection(
	proxy_url,
	proxy_mode="auto",
	proxy_user="",
	proxy_pass="",
	provider="gemini",
	api_key="",
):
	raw_url = (proxy_url or "").strip()
	if not raw_url:
		# Translators: Announcement when testing proxy connection without entering a URL
		return False, _("Please enter a proxy URL first."), 0

	scheme = ""
	if "://" in raw_url:
		scheme, rest = raw_url.split("://", 1)
		scheme = scheme.lower()
	else:
		rest = raw_url

	parsed = urlparse("http://" + rest)
	user = parsed.username or (proxy_user or "").strip()
	password = parsed.password or (proxy_pass or "").strip()
	host = parsed.hostname or ""
	port = parsed.port

	mode = (proxy_mode or "auto").strip().lower()
	is_reverse = False
	if mode == "reverse":
		is_reverse = True
	elif mode in ("forward", "socks5", "http"):
		is_reverse = False
		if mode == "socks5":
			scheme = "socks5"
		elif mode == "http":
			scheme = "http"
	else:
		if "socks" in scheme:
			is_reverse = False
		elif host.lower() in ["localhost", "127.0.0.1"]:
			is_reverse = False
		elif host and "." in host and not host.replace(".", "").isdigit():
			is_reverse = True
		else:
			is_reverse = False

	if not scheme:
		if is_reverse:
			if host.replace(".", "").isdigit() or host.lower() in ["localhost", "127.0.0.1"]:
				scheme = "https" if port == 443 else "http"
			else:
				scheme = "http" if port == 80 else "https"
		elif port and detect_proxy_type(host, port) == "socks5":
			scheme = "socks5"
		else:
			scheme = "http"

	if is_reverse:
		api_key = (api_key or "").strip()
		if not api_key:
			# Translators: Announcement when testing reverse proxy without an API key
			return False, _("Please enter an API key for the selected provider to test the reverse proxy."), 0

		clean_netloc = host
		if port:
			clean_netloc += f":{port}"
		base_url = f"{scheme}://{clean_netloc}".rstrip("/")

		p_lower = (provider or "gemini").lower()
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
		}
		if p_lower == "gemini":
			probe_url = f"{base_url}/v1beta/models?key={api_key}"
		elif p_lower in ("openai", "mistral", "groq", "minimax", "custom"):
			probe_url = f"{base_url}/v1/models"
			headers["Authorization"] = f"Bearer {api_key}"
		else:
			probe_url = f"{base_url}/v1beta/models?key={api_key}"

		req = request.Request(probe_url, headers=headers, method="GET")
		direct_opener = request.build_opener(request.ProxyHandler({}))
		t0 = time.perf_counter()
		try:
			with direct_opener.open(req, timeout=8):
				latency = int((time.perf_counter() - t0) * 1000)
				# Translators: Announcement when reverse proxy connection test succeeds with latency in ms and provider name
				msg = _("Reverse proxy connected successfully to {provider}. Latency: {latency} ms").format(
					provider=provider.capitalize(),
					latency=latency,
				)
				return True, msg, latency
		except error.HTTPError as e:
			latency = int((time.perf_counter() - t0) * 1000)
			msg = _(
				# Translators: Announcement when reverse proxy responds with an HTTP error status code
				"Reverse proxy reachable ({provider} returned HTTP {code}). Latency: {latency} ms"
			).format(
				provider=provider.capitalize(),
				code=e.code,
				latency=latency,
			)
			return True, msg, latency
		except Exception as e:
			# Translators: Announcement when proxy connection test fails with error details
			msg = _("Proxy connection failed: {error}").format(error=str(e))
			return False, msg, 0
	else:
		t0 = time.perf_counter()
		try:
			if "socks" in scheme:
				opener = request.build_opener(
					_SOCKS5Handler(host, port or 1080, user, password),
				)
			else:
				clean_netloc = host
				if port:
					clean_netloc += f":{port}"
				clean_proxy = f"http://{clean_netloc}"
				handler = request.ProxyHandler({"http": clean_proxy, "https": clean_proxy})
				opener = request.build_opener(handler)
				if user:
					auth_str = f"{user}:{password}"
					encoded_auth = base64.b64encode(auth_str.encode()).decode()
					opener.addheaders.append(("Proxy-Authorization", f"Basic {encoded_auth}"))

			probe_url = "https://www.google.com/generate_204"
			req = request.Request(
				probe_url,
				headers={
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
				},
				method="GET",
			)
			with opener.open(req, timeout=8):
				latency = int((time.perf_counter() - t0) * 1000)
				proto_name = "SOCKS5" if "socks" in scheme else "HTTP"
				# Translators: Announcement when forward proxy connection test succeeds with protocol name and latency in ms
				msg = _("{protocol} proxy connected successfully. Latency: {latency} ms").format(
					protocol=proto_name,
					latency=latency,
				)
				return True, msg, latency
		except Exception as e:
			# Translators: Announcement when proxy connection test fails with error details
			msg = _("Proxy connection failed: {error}").format(error=str(e))
			return False, msg, 0


# FFmpeg utilities


def ensure_ffmpeg():
	lib_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib")
	ffmpeg_lib_path = os.path.join(lib_dir, "ffmpeg.exe")

	if os.path.exists(ffmpeg_lib_path):
		return ffmpeg_lib_path

	try:
		result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
		if result.returncode == 0:
			return "ffmpeg"
	except Exception as e:
		log.debug(f"ffmpeg version check failed: {e}")

	# Translators: Title of dialog asking user to download ffmpeg
	title = _("Download ffmpeg?")
	message = _(
		# Translators: Message in dialog asking user to download ffmpeg for video processing
		"Video processing requires ffmpeg (approximately 70MB download).\n\nDownload ffmpeg now to the addon's lib folder?\n\nThis is a one-time download.",
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

		if user_choice[0] != wx.ID_YES:
			# Translators: Message reported when user cancels downloading ffmpeg required for video processing
			core.callLater(0, ui.message, _("Operation cancelled. ffmpeg is required for video processing."))
			return None

		result_holder = [None]
		done = threading.Event()

		def _download():
			try:
				result_holder[0] = download_ffmpeg(ffmpeg_lib_path)
			finally:
				done.set()

		threading.Thread(target=_download, daemon=True).start()
		done.wait()
		return result_holder[0]

	user_choice = [wx.ID_NO]
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

	if user_choice[0] != wx.ID_YES:
		# Translators: Message reported when user cancels downloading ffmpeg required for video processing
		core.callLater(0, ui.message, _("Operation cancelled. ffmpeg is required for video processing."))
		return None

	return download_ffmpeg(ffmpeg_lib_path)


def download_ffmpeg(target_path):
	try:
		# Translators: Status message when downloading ffmpeg
		plugin_state.speak_status(_("Downloading ffmpeg, please wait..."))
		download_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
		from urllib import request

		opener = get_proxy_opener(download_url)
		req = request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
		zip_path = target_path + ".zip"
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
						if downloaded % (10 * 1024 * 1024) < 1024 * 1024:
							plugin_state.speak_status(
								# Translators: Spoken progress message during ffmpeg download. {percent} is the download percentage number.
								_("Downloading ffmpeg: {percent}%").format(percent=percent),
							)

		# Translators: Status message when extracting ffmpeg
		plugin_state.speak_status(_("Extracting ffmpeg..."))
		with zipfile.ZipFile(zip_path, "r") as zip_ref:
			ffmpeg_file = None
			for name in zip_ref.namelist():
				if name.endswith("bin/ffmpeg.exe"):
					ffmpeg_file = name
					break
			if ffmpeg_file:
				temp_extract = os.path.join(tempfile.gettempdir(), "ffmpeg_temp_extract")
				os.makedirs(temp_extract, exist_ok=True)
				zip_ref.extract(ffmpeg_file, temp_extract)
				shutil.move(os.path.join(temp_extract, ffmpeg_file), target_path)
				try:
					shutil.rmtree(temp_extract)
				except Exception as e:
					log.debug(f"Temp extract dir removal failed: {e}")
		try:
			os.remove(zip_path)
		except Exception as e:
			log.debug(f"ffmpeg zip removal failed: {e}")

		if os.path.exists(target_path):
			# Translators: Success message after ffmpeg download completes
			plugin_state.speak_status(_("ffmpeg downloaded successfully!"))
			if plugin_state.plugin_instance:
				plugin_state.plugin_instance.current_status = _("Idle")
			return target_path
		else:
			raise Exception("Failed to extract ffmpeg.exe")
	except Exception as e:
		log.error(f"ffmpeg download failed: {e}", exc_info=True)
		# Translators: Error message when ffmpeg download fails
		wx.CallAfter(show_error_dialog, _("Failed to download ffmpeg: {error}").format(error=str(e)))
		if plugin_state.plugin_instance:
			plugin_state.plugin_instance.current_status = _("Idle")
		return None


def compress_video(input_path):
	ffmpeg_path = ensure_ffmpeg()
	if not ffmpeg_path:
		return None

	fd, temp_path = tempfile.mkstemp(suffix=".mp4", prefix="vision_assistant_comp_")
	os.close(fd)

	cmd = [
		ffmpeg_path,
		"-i",
		input_path,
		"-vf",
		"scale=-2:min(480\\,ih)",
		"-c:v",
		"libx264",
		"-preset",
		"veryfast",
		"-crf",
		"30",
		"-c:a",
		"aac",
		"-b:a",
		"64k",
		"-movflags",
		"+faststart",
		"-y",
		temp_path,
	]

	startupinfo = None
	creationflags = 0
	if sys.platform == "win32":
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		startupinfo.wShowWindow = subprocess.SW_HIDE
		creationflags = 0x08000000

	try:
		subprocess.run(
			cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			startupinfo=startupinfo,
			creationflags=creationflags,
			check=True,
		)
		try:
			if os.path.getsize(temp_path) >= os.path.getsize(input_path):
				os.remove(temp_path)
				return input_path
		except Exception as e:
			log.debug(f"Video compress temp removal failed: {e}")
		return temp_path
	except subprocess.CalledProcessError as e:
		log.error(f"Video compression failed: {e.stderr}")
		try:
			os.remove(temp_path)
		except Exception as ex:
			log.debug(f"Video temp file removal failed: {ex}")
		return None


# Online video download link extractors


def get_twitter_download_link(tweet_url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
	}
	try:
		opener = get_proxy_opener()
		id_match = re.search(r"status/(\d+)", tweet_url)
		if id_match:
			tweet_id = id_match.group(1)
			api_url = f"https://api.fxtwitter.com/status/{tweet_id}"
			req = request.Request(api_url, headers=headers)
			try:
				with opener.open(req, timeout=15) as response:
					res_data = json.loads(response.read().decode("utf-8"))
					tweet = res_data.get("tweet", {})
					media = tweet.get("media", {})
					videos = media.get("videos") or []
					if not videos:
						for item in media.get("all") or []:
							if isinstance(item, dict) and item.get("type") in ("video", "gif"):
								videos.append(item)
					if videos:
						best_video = videos[0]
						variants = best_video.get("variants") or []
						mp4_variants = [
							v
							for v in variants
							if isinstance(v, dict) and v.get("content_type") == "video/mp4"
						]
						if mp4_variants:
							mp4_variants.sort(key=lambda x: x.get("bitrate", 0), reverse=True)
							if mp4_variants[0].get("url"):
								return mp4_variants[0]["url"]
						if best_video.get("url"):
							return best_video["url"]
			except Exception as e:
				log.debug(f"FxTwitter extraction failed, trying fallback: {e}")

		ts_url = f"https://twitsave.com/info?url={urllib.parse.quote(tweet_url)}"
		req_fallback = request.Request(ts_url, headers=headers)
		with opener.open(req_fallback, timeout=15) as res:
			html = res.read().decode("utf-8")
			links = re.findall(r'https?://video\.twimg\.com/[^\s"\'<>]+\.mp4[^\s"\'<>]*', html)
			if not links:
				links = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', html)
			if links:
				return links[0].replace("&amp;", "&")
	except Exception as e:
		log.error(f"Twitter download extraction failed: {e}")
	return None


def get_instagram_download_link(insta_url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Referer": "https://indown.io/en1",
	}
	try:
		cookie_handler = request.HTTPCookieProcessor()
		opener = get_proxy_opener()
		opener.add_handler(cookie_handler)

		req_get = request.Request("https://indown.io/en1", headers=headers)
		with opener.open(req_get, timeout=15) as res:
			html_page = res.read().decode("utf-8")

		token_match = re.search(r'name="_token"\s+value="([^"]+)"|value="([^"]+)"\s+name="_token"', html_page)
		if not token_match:
			log.error("Failed to extract CSRF token from indown.io.")
			return None
		csrf_token = token_match.group(1) if token_match.group(1) else token_match.group(2)

		ref_match = re.search(r'name="referer"\s+value="([^"]+)"', html_page)
		referer_val = ref_match.group(1) if ref_match else "https://indown.io/en1"

		payload = {
			"referer": referer_val,
			"locale": "en",
			"_token": csrf_token,
			"link": insta_url,
			"o": "o",
		}
		data = urlencode(payload).encode("utf-8")

		post_headers = headers.copy()
		post_headers["Content-Type"] = "application/x-www-form-urlencoded"
		post_headers["Origin"] = "https://indown.io"
		post_headers["Referer"] = referer_val

		req_post = request.Request(
			"https://indown.io/download",
			data=data,
			headers=post_headers,
			method="POST",
		)

		with opener.open(req_post, timeout=20) as res:
			result_html = res.read().decode("utf-8")

			links = re.findall(r'href="(https?://[^"\s]+/fetch\?url=[^"\s]+)"', result_html)
			if not links:
				links = re.findall(r'href="(https?://[^\s"]+cdninstagram[^\s"]+\.mp4[^\s"]+)"', result_html)
			if not links:
				links = re.findall(r'href="(https?://[^\s"]+rapidcdn[^\s"]+)"', result_html)
			if not links:
				links = re.findall(r'href="(https?://[^\s"]+\.mp4[^\s"]+)"', result_html)

			if links:
				return links[0].replace("&amp;", "&")
	except Exception as e:
		log.error(f"Instagram download extraction failed: {e}")
	return None


def get_tiktok_download_link(tiktok_url):
	api_url = "https://www.tikwm.com/api/"
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
		"X-Requested-With": "XMLHttpRequest",
	}
	try:
		params = {"url": tiktok_url, "hd": "1"}
		data = urlencode(params).encode("utf-8")
		req = request.Request(api_url, data=data, headers=headers, method="POST")
		opener = get_proxy_opener()
		with opener.open(req, timeout=120) as response:
			res = json.loads(response.read().decode("utf-8"))
			if res.get("code") == 0:
				play_url = res["data"]["play"]
				return play_url if play_url.startswith("http") else "https://www.tikwm.com" + play_url
	except Exception as e:
		log.error(f"TikTok download extraction failed: {e}")
	return None


def _download_temp_video(url, abort_checker=None):
	try:
		req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
		opener = get_proxy_opener(url)
		with opener.open(req, timeout=600) as response:
			fd, path = tempfile.mkstemp(suffix=".mp4")
			os.close(fd)
			try:
				with open(path, "wb") as f:
					while True:
						if abort_checker and abort_checker():
							break
						chunk = response.read(8192)
						if not chunk:
							break
						f.write(chunk)
				if abort_checker and abort_checker():
					try:
						os.remove(path)
					except Exception as e:
						log.debug(f"Download temp file removal failed: {e}")
					return None
				return path
			except Exception as e:
				log.error(f"Error writing temp video: {e}")
				if os.path.exists(path):
					try:
						os.remove(path)
					except Exception as ex:
						log.debug(f"Download temp file removal failed: {ex}")
				return None
	except Exception as e:
		log.error(f"Error downloading temp video: {e}")
	return None


# Video source classes


class _LocalVideoSource:
	is_direct = False

	def __init__(self, path):
		self.path = path
		# Translators: Error message shown when processing a local video file fails.
		self.error_message = _("Error processing local video.")
		self.log_label = "Local video"
		self._compressed_path = None

	def prepare(self, report, abort_check):
		return True

	def ensure_local(self, owner, report, abort_check):
		if self._compressed_path and os.path.exists(self._compressed_path):
			return self._compressed_path
		# Translators: Status message when compressing a local video file before uploading.
		report(_("Compressing video (this may take a moment)..."))
		self._compressed_path = compress_video(self.path)
		if not self._compressed_path:
			# Translators: Error message shown when video compression fails or was cancelled by the user.
			report(_("Error: Video compression failed or was cancelled."))
			return None
		return self._compressed_path

	def duration(self, file_uri):
		from ..ai.providers.gemini import GeminiHandler

		return getattr(GeminiHandler, "_file_durations", {}).get(file_uri)

	def cleanup(self):
		cp = self._compressed_path
		if cp and cp != self.path and os.path.exists(cp):
			try:
				os.remove(cp)
			except Exception as e:
				log.debug(f"Compressed temp file removal failed: {e}")


class _DownloadVideoSource:
	is_direct = False

	def __init__(self, url, platform):
		self.url = url
		self.platform = platform
		# Translators: Error message shown when processing an online video fails.
		self.error_message = _("Error processing video.")
		self.log_label = "Online video analysis thread failed"
		self._direct_link = None
		self._temp_path = None

	def prepare(self, report, abort_check):
		# Translators: Message reported when the add-on starts processing an online video link.
		report(_("Processing Video..."))
		return True

	def _extract_link(self, report):
		if self.platform == "instagram":
			link = get_instagram_download_link(self.url)
			# Translators: Error message when the add-on fails to get a direct download link for an Instagram video.
			err = _("Error: Could not extract Instagram video.")
		elif self.platform == "twitter":
			link = get_twitter_download_link(self.url)
			# Translators: Error message when the add-on fails to get a direct download link for a Twitter/X video.
			err = _("Error: Could not extract Twitter video.")
		else:
			link = get_tiktok_download_link(self.url)
			# Translators: Error message when the add-on fails to get a direct download link for a TikTok video.
			err = _("Error: Could not extract TikTok video.")
		if not link:
			log.error(f"Video direct link extraction failed for: {self.url}")
			report(err)
		return link

	def ensure_local(self, owner, report, abort_check):
		if self._temp_path and os.path.exists(self._temp_path):
			return self._temp_path
		if abort_check():
			return None
		if not self._direct_link:
			self._direct_link = self._extract_link(report)
			if not self._direct_link:
				return None
		if abort_check():
			return None
		# Translators: Message reported when the add-on is downloading the video from the extracted link.
		report(_("Downloading Video..."))
		self._temp_path = _download_temp_video(self._direct_link, abort_checker=abort_check)
		if not self._temp_path:
			log.error(f"Video download failed for link: {self._direct_link}")
			# Translators: Error message when downloading the online video fails.
			report(_("Error: Download failed."))
			return None
		return self._temp_path

	@property
	def path(self):
		return self._temp_path

	def duration(self, file_uri):
		from ..ai.providers.gemini import GeminiHandler

		return getattr(GeminiHandler, "_file_durations", {}).get(file_uri)

	def cleanup(self):
		if self._temp_path and os.path.exists(self._temp_path):
			try:
				os.remove(self._temp_path)
			except Exception as e:
				log.debug(f"Temp file removal failed: {e}")


class _YouTubeVideoSource:
	is_direct = True
	path = None

	def __init__(self, url):
		self.url = self._clean_youtube_url(url)
		self.error_message = _("Error processing video.")
		self.log_label = "Online video analysis thread failed"

	def _clean_youtube_url(self, url):
		try:
			parsed = urllib.parse.urlparse(url)
			domain = parsed.netloc.lower()

			if "youtube.com" in domain:
				if parsed.path == "/watch":
					qs = urllib.parse.parse_qs(parsed.query)
					if "v" in qs:
						return f"https://www.youtube.com/watch?v={qs['v'][0]}"
				elif parsed.path.startswith("/shorts/"):
					video_id = parsed.path.split("/shorts/")[1].split("?")[0].split("/")[0]
					return f"https://www.youtube.com/watch?v={video_id}"

			elif "youtu.be" in domain:
				video_id = parsed.path.lstrip("/").split("?")[0].split("/")[0]
				return f"https://www.youtube.com/watch?v={video_id}"

		except Exception as e:
			log.warning(f"YouTube URL cleanup failed: {e}")

		return url

	@property
	def direct_uri(self):
		return self.url

	def prepare(self, report, abort_check):
		report(_("Processing Video..."))
		return True

	def ensure_local(self, owner, report, abort_check):
		return None

	def duration(self, file_uri):
		return None

	def cleanup(self):
		pass


class _InvalidVideoSource:
	is_direct = False
	path = None

	def __init__(self, message):
		self.message = message
		self.error_message = message
		self.log_label = "Online video analysis thread failed"

	def prepare(self, report, abort_check):
		report(self.message)
		return False

	def ensure_local(self, owner, report, abort_check):
		return None

	def duration(self, file_uri):
		return None

	def cleanup(self):
		pass


# Progress file reader


class ProgressFileReader:
	def __init__(self, file_path, callback=None, abort_checker=None):
		self.file_path = file_path
		self.callback = callback
		self.abort_checker = abort_checker
		self.total_size = os.path.getsize(file_path)
		self.bytes_read = 0
		self.last_reported_percent = 0

	def __iter__(self):
		with open(self.file_path, "rb") as f:
			while True:
				if self.abort_checker and self.abort_checker():
					raise Exception("Upload aborted")

				chunk = f.read(1024 * 512)
				if not chunk:
					break

				self.bytes_read += len(chunk)
				if self.total_size > 0:
					percent = int((self.bytes_read / self.total_size) * 100)
					if percent >= self.last_reported_percent + 10:
						self.last_reported_percent = (percent // 10) * 10
						if self.callback:
							self.callback(self.last_reported_percent)

				yield chunk

	def __len__(self):
		return self.total_size


# Minimal WebSocket client (for Live session)


_XOR_TABLES = {}


def _xor_table(key_byte):
	table = _XOR_TABLES.get(key_byte)
	if table is None:
		table = bytes(b ^ key_byte for b in range(256))
		_XOR_TABLES[key_byte] = table
	return table


class _MinimalWebSocket:
	def __init__(self, host, path, port=443, is_ssl=True, timeout=30):
		self.host = host
		self.path = path
		self.port = port
		self.is_ssl = is_ssl
		self.timeout = timeout
		self.sock = None
		self._recv_buf = b""
		self.closed = False
		self.close_reason = None
		self._send_lock = threading.Lock()

	def _get_effective_proxy(self):
		p = parse_proxy_settings()
		if p:
			if p["is_reverse"] or (p["host"] and p["host"].lower() == self.host.lower()):
				return None
			return p
		try:
			sys_proxies = request.getproxies()
			sys_url = sys_proxies.get("https") or sys_proxies.get("http")
			if sys_url:
				if "://" not in sys_url:
					sys_url = "http://" + sys_url
				parsed = urlparse(sys_url)
				if parsed.hostname and parsed.hostname.lower() != self.host.lower():
					return {
						"scheme": (parsed.scheme or "http").lower(),
						"host": parsed.hostname,
						"port": parsed.port or (443 if parsed.scheme == "https" else 80),
						"user": parsed.username or "",
						"password": parsed.password or "",
					}
		except Exception:
			pass
		return None

	def _connect_via_socks5(self, proxy_info, timeout):
		p_host = (
			proxy_info.get("host") if isinstance(proxy_info, dict) else getattr(proxy_info, "hostname", "")
		)
		p_port = proxy_info.get("port") if isinstance(proxy_info, dict) else getattr(proxy_info, "port", None)
		p_port = p_port or 1080
		s = socket.create_connection((p_host, p_port), timeout=timeout)
		u = proxy_info.get("user") if isinstance(proxy_info, dict) else getattr(proxy_info, "username", "")
		p = (
			proxy_info.get("password")
			if isinstance(proxy_info, dict)
			else getattr(proxy_info, "password", "")
		)
		if u and p:
			s.sendall(b"\x05\x02\x00\x02")
			res = s.recv(2)
			if len(res) < 2 or res[0] != 5:
				s.close()
				raise ConnectionError("SOCKS5 proxy invalid response")
			if res[1] == 2:
				u_b = u.encode("utf-8")
				p_b = p.encode("utf-8")
				s.sendall(struct.pack("BB", 1, len(u_b)) + u_b + struct.pack("B", len(p_b)) + p_b)
				auth_res = s.recv(2)
				if len(auth_res) < 2 or auth_res[1] != 0:
					s.close()
					raise ConnectionError("SOCKS5 auth failed")
			elif res[1] != 0:
				s.close()
				raise ConnectionError(f"Unsupported SOCKS5 auth method: {res[1]}")
		else:
			s.sendall(b"\x05\x01\x00")
			res = s.recv(2)
			if len(res) < 2 or res[0] != 5 or res[1] != 0:
				s.close()
				raise ConnectionError(f"SOCKS5 proxy rejected connection: {res!r}")
		host_b = self.host.encode("idna")
		s.sendall(
			struct.pack(">BBBB", 5, 1, 0, 3)
			+ struct.pack("B", len(host_b))
			+ host_b
			+ struct.pack(">H", self.port),
		)
		resp = s.recv(10)
		if len(resp) < 4 or resp[1] != 0:
			s.close()
			raise ConnectionError(
				f"SOCKS5 connection failed with status code: {resp[1] if len(resp) >= 2 else 'unknown'}",
			)
		return s

	def _connect_via_http_proxy(self, proxy_info, timeout):
		p_host = (
			proxy_info.get("host") if isinstance(proxy_info, dict) else getattr(proxy_info, "hostname", "")
		)
		p_port = proxy_info.get("port") if isinstance(proxy_info, dict) else getattr(proxy_info, "port", None)
		p_port = p_port or 80
		s = socket.create_connection((p_host, p_port), timeout=timeout)
		connect_req = f"CONNECT {self.host}:{self.port} HTTP/1.1\r\nHost: {self.host}:{self.port}\r\n"
		u = proxy_info.get("user") if isinstance(proxy_info, dict) else getattr(proxy_info, "username", "")
		p = (
			proxy_info.get("password")
			if isinstance(proxy_info, dict)
			else getattr(proxy_info, "password", "")
		)
		if u:
			auth = base64.b64encode(f"{u}:{p or ''}".encode()).decode()
			connect_req += f"Proxy-Authorization: Basic {auth}\r\n"
		connect_req += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n\r\n"
		s.sendall(connect_req.encode())
		resp = b""
		while b"\r\n\r\n" not in resp:
			chunk = s.recv(4096)
			if not chunk:
				s.close()
				raise ConnectionError("Proxy tunnel closed connection abruptly.")
			resp += chunk
		first_line = resp.split(b"\r\n", 1)[0]
		if b" 200 " not in first_line:
			s.close()
			err_msg = first_line.decode(errors="ignore")
			raise ConnectionError(f"Proxy tunnel failed: {err_msg}")
		return s

	def connect(self):
		proxy_info = self._get_effective_proxy()
		raw = None

		if proxy_info:
			try:
				scheme = (
					proxy_info.get("scheme")
					if isinstance(proxy_info, dict)
					else getattr(proxy_info, "scheme", "http")
				) or "http"
				if "socks" in scheme.lower():
					raw = self._connect_via_socks5(proxy_info, self.timeout)
				else:
					raw = self._connect_via_http_proxy(proxy_info, self.timeout)
			except Exception as e:
				log.error(f"Proxy connection failed: {e}")
				if raw:
					try:
						raw.close()
					except Exception as ex:
						log.debug(f"Socket close failed: {ex}")
				raise
		else:
			raw = socket.create_connection((self.host, self.port), timeout=self.timeout)

		if self.is_ssl:
			ctx = ssl.create_default_context()
			self.sock = ctx.wrap_socket(raw, server_hostname=self.host)
		else:
			self.sock = raw

		key = base64.b64encode(os.urandom(16)).decode()
		handshake = (
			f"GET {self.path} HTTP/1.1\r\n"
			f"Host: {self.host}\r\n"
			"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36\r\n"
			"Origin: https://aistudio.google.com\r\n"
			"Upgrade: websocket\r\n"
			"Connection: Upgrade\r\n"
			f"Sec-WebSocket-Key: {key}\r\n"
			"Sec-WebSocket-Version: 13\r\n\r\n"
		)
		self.sock.sendall(handshake.encode())

		resp = b""
		while b"\r\n\r\n" not in resp:
			chunk = self.sock.recv(4096)
			if not chunk:
				raise ConnectionError("WebSocket handshake closed")
			resp += chunk

		if b" 101 " not in resp.split(b"\r\n", 1)[0]:
			try:
				status_line = resp.split(b"\r\n", 1)[0].decode(errors="ignore")
				body = resp.split(b"\r\n\r\n", 1)[1].decode(errors="ignore")
				err_msg = f"WebSocket handshake failed: {status_line} Body: {body[:500]}"
			except Exception:
				err_msg = f"WebSocket handshake failed: {resp[:120]!r}"
			raise ConnectionError(err_msg)

		self._recv_buf = resp.split(b"\r\n\r\n", 1)[1]
		self.sock.settimeout(1.0)

	def _send_frame(self, opcode, payload):
		if self.closed:
			return
		header = bytearray()
		header.append(0x80 | opcode)
		mask = os.urandom(4)
		length = len(payload)
		if length < 126:
			header.append(0x80 | length)
		elif length < 65536:
			header.append(0x80 | 126)
			header += struct.pack(">H", length)
		else:
			header.append(0x80 | 127)
			header += struct.pack(">Q", length)
		header += mask
		payload = bytes(payload)
		masked = bytearray(len(payload))
		for offset, key_byte in enumerate(mask):
			masked[offset::4] = payload[offset::4].translate(_xor_table(key_byte))
		frame = bytes(header) + bytes(masked)
		with self._send_lock:
			if self.closed or not self.sock:
				return
			try:
				self.sock.settimeout(10.0)
				self.sock.sendall(frame)
			except Exception as e:
				self.close_reason = f"send error: {e}"
				self.closed = True
				try:
					self.sock.close()
				except Exception:
					pass
				raise
			finally:
				if not self.closed and self.sock:
					try:
						self.sock.settimeout(1.0)
					except Exception:
						pass

	def send_text(self, text):
		self._send_frame(0x1, text.encode("utf-8"))

	def _recv_exact(self, n, deadline=None):
		while len(self._recv_buf) < n:
			if self.closed:
				raise ConnectionError("WebSocket closed")
			if deadline is not None and time.time() >= deadline:
				raise socket.timeout("WebSocket receive timed out")
			try:
				chunk = self.sock.recv(65536)
				if not chunk:
					self.close()
					raise ConnectionError("WebSocket connection closed")
				self._recv_buf += chunk
			except (BlockingIOError, ssl.SSLWantReadError, socket.timeout):
				if deadline is not None and time.time() >= deadline:
					raise socket.timeout("WebSocket receive timed out")
				time.sleep(0.05)
				continue
			except ssl.SSLError as e:
				if "timed out" in str(e).lower():
					if deadline is not None and time.time() >= deadline:
						raise socket.timeout("WebSocket receive timed out")
					time.sleep(0.05)
					continue
				self.close()
				raise
			except Exception:
				self.close()
				raise
		data, self._recv_buf = self._recv_buf[:n], self._recv_buf[n:]
		return data

	def _read_frame(self, deadline=None):
		b0, b1 = self._recv_exact(2, deadline)
		opcode = b0 & 0x0F
		fin = (b0 & 0x80) != 0
		length = b1 & 0x7F
		if length == 126:
			length = struct.unpack(">H", self._recv_exact(2, deadline))[0]
		elif length == 127:
			length = struct.unpack(">Q", self._recv_exact(8, deadline))[0]
		payload = self._recv_exact(length, deadline) if length else b""
		return opcode, fin, payload

	def _note_close(self, payload):
		if len(payload) >= 2:
			code = struct.unpack(">H", payload[:2])[0]
			text = payload[2:].decode("utf-8", "replace")
			self.close_reason = f"{code} {text}".strip()
		self.closed = True

	def recv(self, timeout=None):
		deadline = (time.time() + timeout) if timeout is not None else None
		try:
			opcode, fin, payload = self._read_frame(deadline)
			if opcode == 0x8:
				self._note_close(payload)
				return None, None
			if opcode == 0x9:
				return 0x9, payload
			if not fin:
				buf = bytearray(payload)
				frame_count = 1
				while True:
					cont_op, cont_fin, cont_payload = self._read_frame(deadline)
					if cont_op == 0x8:
						self._note_close(cont_payload)
						return None, None
					if cont_op == 0x9:
						try:
							self._send_frame(0xA, cont_payload or b"")
						except Exception:
							pass
						continue
					if cont_op == 0x0:
						buf += cont_payload
						frame_count += 1
					if cont_fin:
						break
				payload = bytes(buf)
				log.debug(f"WebSocket fragmented message reassembled from {frame_count} frames.")
			return opcode, payload
		except socket.timeout:
			raise
		except Exception as e:
			self.close_reason = self.close_reason or f"recv error: {e}"
			self.closed = True
			return None, None

	def close(self):
		if self.closed:
			return
		try:
			self._send_frame(0x8, b"")
		except Exception:
			pass
		self.closed = True
		try:
			if self.sock:
				self.sock.close()
		except Exception:
			pass


# Microphone capture (Windows MCI / waveIn API)


class _WAVEFORMATEX(ctypes.Structure):
	_fields_ = [
		("wFormatTag", ctypes.c_ushort),
		("nChannels", ctypes.c_ushort),
		("nSamplesPerSec", ctypes.c_uint),
		("nAvgBytesPerSec", ctypes.c_uint),
		("nBlockAlign", ctypes.c_ushort),
		("wBitsPerSample", ctypes.c_ushort),
		("cbSize", ctypes.c_ushort),
	]


class _WAVEHDR(ctypes.Structure):
	pass


_WAVEHDR._fields_ = [
	("lpData", ctypes.c_char_p),
	("dwBufferLength", ctypes.c_uint),
	("dwBytesRecorded", ctypes.c_uint),
	("dwUser", ctypes.c_void_p),
	("dwFlags", ctypes.c_uint),
	("dwLoops", ctypes.c_uint),
	("lpNext", ctypes.POINTER(_WAVEHDR)),
	("reserved", ctypes.c_void_p),
]


class _MicCapture:
	_CALLBACK_NULL = 0x00000000
	_WHDR_DONE = 0x00000001

	def __init__(self, on_data, sample_rate=16000, block_ms=100):
		self.on_data = on_data
		self.sample_rate = sample_rate
		self.block_size = int(sample_rate * 2 * block_ms / 1000)
		self.hwi = None
		self._running = False
		self._thread = None
		self._buffers = []

	def start(self):
		winmm = ctypes.windll.winmm
		fmt = _WAVEFORMATEX(
			wFormatTag=1,
			nChannels=1,
			nSamplesPerSec=self.sample_rate,
			nAvgBytesPerSec=self.sample_rate * 2,
			nBlockAlign=2,
			wBitsPerSample=16,
			cbSize=0,
		)
		self.hwi = ctypes.c_void_p()
		res = winmm.waveInOpen(
			ctypes.byref(self.hwi),
			0xFFFFFFFF,
			ctypes.byref(fmt),
			0,
			0,
			self._CALLBACK_NULL,
		)
		if res != 0:
			raise OSError(f"waveInOpen failed: {res}")
		self._running = True
		self._thread = threading.Thread(target=self._loop, daemon=True)
		self._thread.start()

	def _make_header(self):
		buf = ctypes.create_string_buffer(self.block_size)
		hdr = _WAVEHDR()
		hdr.lpData = ctypes.cast(buf, ctypes.c_char_p)
		hdr.dwBufferLength = self.block_size
		hdr.dwFlags = 0
		return buf, hdr

	def _loop(self):
		winmm = ctypes.windll.winmm
		hdr_size = ctypes.sizeof(_WAVEHDR)
		headers = [self._make_header() for _i in range(4)]
		for buf, hdr in headers:
			winmm.waveInPrepareHeader(self.hwi, ctypes.byref(hdr), hdr_size)
			winmm.waveInAddBuffer(self.hwi, ctypes.byref(hdr), hdr_size)
		winmm.waveInStart(self.hwi)
		try:
			while self._running:
				progressed = False
				for buf, hdr in headers:
					if hdr.dwFlags & self._WHDR_DONE:
						recorded = hdr.dwBytesRecorded
						if recorded and self.on_data:
							try:
								self.on_data(buf.raw[:recorded])
							except Exception as e:
								log.debug(f"Mic data callback failed: {e}")
						winmm.waveInUnprepareHeader(self.hwi, ctypes.byref(hdr), hdr_size)
						hdr.dwFlags = 0
						hdr.dwBytesRecorded = 0
						winmm.waveInPrepareHeader(self.hwi, ctypes.byref(hdr), hdr_size)
						winmm.waveInAddBuffer(self.hwi, ctypes.byref(hdr), hdr_size)
						progressed = True
				if not progressed:
					time.sleep(0.05)
		finally:
			try:
				winmm.waveInStop(self.hwi)
			except Exception as e:
				log.debug(f"waveInStop failed: {e}")
			for buf, hdr in headers:
				try:
					winmm.waveInUnprepareHeader(self.hwi, ctypes.byref(hdr), hdr_size)
				except Exception as e:
					log.debug(f"waveInUnprepareHeader failed: {e}")

	def stop(self):
		self._running = False
		if self.hwi:
			try:
				ctypes.windll.winmm.waveInReset(self.hwi)
			except Exception as e:
				log.debug(f"waveInReset failed: {e}")
		if self._thread:
			self._thread.join(timeout=2)
		if self.hwi:
			try:
				ctypes.windll.winmm.waveInClose(self.hwi)
			except Exception as e:
				log.debug(f"waveInClose failed: {e}")
			self.hwi = None


# Live voice session (Gemini Live API)


class LiveTTSAborted(Exception):
	pass


class GeminiLiveTTS:
	def __init__(self, voice=""):
		self.voice = voice or "Puck"
		self.ws = None

	def _system_instruction(self):
		return "You are a strict Text-to-Speech engine. You will receive text segments. Your ONLY job is to read them out loud exactly as written. Do not add any conversational fillers, greetings, or extra words. Do not acknowledge instructions. Just speak the text provided."

	def _resolve_model(self):
		return resolve_live_model()

	def ensure_connection(self, abort_checker=None):
		if self.ws and not getattr(self.ws, "closed", True):
			return True
		if self.ws:
			try:
				self.ws.close()
			except Exception as e:
				log.debug(f"WebSocket close failed: {e}")
			self.ws = None

		from ..ai.core import AIHandler
		from ..ai.providers.gemini import GeminiHandler

		live_model = self._resolve_model()
		self._live_model = live_model
		api_keys = AIHandler.get_keys("gemini")
		if not api_keys:
			return False

		num_keys = len(api_keys)
		start_idx = getattr(GeminiHandler, "_working_key_idx", 0)

		for k_i in range(num_keys):
			if abort_checker and abort_checker():
				return False
			idx = (start_idx + k_i) % num_keys
			api_key = api_keys[idx]
			base_host = vision_config.DEFAULT_API_URLS["gemini"].replace("https://", "")
			base_port = 443
			is_ssl = True
			try:
				base = AIHandler.get_base_url("gemini")
				p_base = urlparse(base)
				if p_base.hostname:
					base_host = p_base.hostname
					base_port = p_base.port or (443 if p_base.scheme == "https" else 80)
					is_ssl = p_base.scheme != "http"
			except Exception:
				pass

			ws_path = (
				f"/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key={api_key}"
			)

			max_retries = getattr(GeminiHandler, "_max_retries", 3)
			attempt = 0
			while attempt < max_retries:
				if abort_checker and abort_checker():
					return False
				try:
					ws_candidate = _MinimalWebSocket(base_host, ws_path, port=base_port, is_ssl=is_ssl)
					ws_candidate.connect()

					setup_msg = {
						"setup": {
							"model": f"models/{live_model}",
							"generationConfig": {
								"responseModalities": ["AUDIO"],
								"speechConfig": {
									"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": self.voice}},
								},
							},
							"systemInstruction": {"parts": [{"text": self._system_instruction()}]},
						},
					}
					ws_candidate.send_text(json.dumps(setup_msg))

					start_wait = time.time()
					setup_success = False
					while time.time() - start_wait < 10:
						setup_res = ws_candidate.recv()
						if setup_res:
							op, pay = setup_res
							if op is None:
								break
							if op in (0x1, 0x2):
								try:
									setup_data = json.loads(pay.decode("utf-8", "replace"))
									if "setupComplete" in setup_data:
										setup_success = True
										break
								except Exception:
									pass
							elif op == 0x9:
								try:
									ws_candidate._send_frame(0xA, pay or b"")
								except Exception:
									pass
							time.sleep(0.05)

					if setup_success:
						self.ws = ws_candidate
						setattr(GeminiHandler, "_working_key_idx", idx)
						return True
					else:
						ws_candidate.close()

				except Exception as e:
					log.error(f"VisionAssistant Offline TTS WebSocket exception: {e}")

				attempt += 1
				time.sleep(1)

		return False

	def generate(self, text, max_attempts=3, timeout=30, abort_checker=None):
		chunks = []
		for tts_attempt in range(max_attempts):
			if abort_checker and abort_checker():
				self.close()
				raise LiveTTSAborted()
			if not self.ensure_connection(abort_checker):
				break

			current_ws = self.ws
			model_name = (getattr(self, "_live_model", "") or "").lower()
			trailing_timeout = 5.0 if "native" in model_name else 1.0
			try:
				req = {
					"clientContent": {
						"turns": [{"role": "user", "parts": [{"text": text}]}],
						"turnComplete": True,
					},
				}
				current_ws.send_text(json.dumps(req))

				received = []
				turn_seen = False
				last_data = time.time()
				start_wait = time.time()
				while time.time() - start_wait < timeout:
					if abort_checker and abort_checker():
						raise LiveTTSAborted()
					if turn_seen:
						remaining = trailing_timeout - (time.time() - last_data)
						if remaining <= 0:
							break
						read_timeout = remaining
					else:
						read_timeout = None
					try:
						opcode, payload = current_ws.recv(read_timeout)
					except socket.timeout:
						break
					if opcode is None:
						if turn_seen:
							break
						raise ConnectionError("WebSocket dropped during receive.")
					if opcode in (0x1, 0x2) and payload:
						last_data = time.time()
						try:
							resp = json.loads(payload.decode("utf-8", "replace"))
							if "serverContent" in resp:
								turn = resp["serverContent"].get("modelTurn") or resp["serverContent"].get(
									"model_turn",
								)
								if turn:
									for part in turn.get("parts", []):
										inline = part.get("inlineData") or part.get("inline_data")
										if inline and inline.get("data"):
											if turn_seen:
												log.debug(
													"Gemini TTS: collected trailing audio chunk after turnComplete.",
												)
											received.append(base64.b64decode(inline["data"]))
								if resp["serverContent"].get("turnComplete") or resp["serverContent"].get(
									"turn_complete",
								):
									turn_seen = True
						except Exception:
							pass
					elif opcode == 0x9:
						try:
							current_ws._send_frame(0xA, payload or b"")
						except Exception:
							pass
					time.sleep(0.01)

				if received:
					chunks = received
					break
			except LiveTTSAborted:
				if self.ws:
					try:
						self.ws.close()
					except Exception as ex:
						log.debug(f"WebSocket close failed: {ex}")
					self.ws = None
				raise
			except Exception as e:
				log.warning(f"Gemini TTS generation failed on attempt {tts_attempt + 1}: {e}")
				if self.ws:
					try:
						self.ws.close()
					except Exception as ex:
						log.debug(f"WebSocket close failed: {ex}")
					self.ws = None
				time.sleep(1)

		if not chunks:
			return None
		return b"".join(chunks)

	def close(self):
		if self.ws:
			try:
				self.ws.close()
			except Exception as e:
				log.debug(f"WebSocket close failed: {e}")
			self.ws = None
