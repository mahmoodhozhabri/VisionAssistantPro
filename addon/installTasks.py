import addonHandler
import gui
import config
import os.path
import sys
import wx
import shutil
import tempfile
import json
import time
import gc
import logging

addon = addonHandler.getCodeAddon()
addonName = addon.name

log = logging.getLogger("globalPlugins.visionAssistant")


_LIB_MARKERS = (".installed",)


def _long_path(path):
	if os.name != "nt":
		return path
	absolute = os.path.abspath(path)
	if absolute.startswith("\\\\?\\"):
		return absolute
	return "\\\\?\\" + absolute


def _contains_marker(path, max_depth=3):
	if not os.path.isdir(path):
		return False
	base_depth = os.path.abspath(path).rstrip("\\/").count(os.sep)
	try:
		for root, dirs, files in os.walk(path):
			depth = os.path.abspath(root).rstrip("\\/").count(os.sep) - base_depth
			if depth > max_depth:
				dirs[:] = []
				continue
			for marker in _LIB_MARKERS:
				if marker in files:
					return True
	except Exception as e:
		log.warning(f"Marker scan failed for {path}: {e}")
	return False


def _copy_asset(src, dst):
	if os.path.isdir(src):
		shutil.copytree(_long_path(src), _long_path(dst), dirs_exist_ok=True)
	else:
		shutil.copy2(_long_path(src), _long_path(dst))


def _shipped_lib_dir():
	for candidate in (
		os.path.join(os.path.dirname(os.path.abspath(__file__)), "globalPlugins", addonName, "lib"),
		os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"),
	):
		if os.path.isdir(candidate):
			return candidate
	return ""


def _shipped_lib_items():
	shipped = _shipped_lib_dir()
	if not shipped:
		return []
	try:
		return os.listdir(shipped)
	except OSError as e:
		log.warning(f"Could not list the shipped lib items: {e}")
		return []


def _has_extra_content(src, dst, max_files=5000):
	if not os.path.isdir(_long_path(dst)):
		return True
	checked = 0
	try:
		for root, dirs, files in os.walk(src):
			relative = os.path.relpath(root, src)
			for name in files:
				checked += 1
				if checked > max_files:
					return False
				if not os.path.exists(_long_path(os.path.join(dst, relative, name))):
					return True
	except Exception as e:
		log.warning(f"Lib content comparison failed for {src}: {e}")
		return True
	return False


def _backup_lib_assets():
	try:
		current_name = addonName.lower()
		for add in addonHandler.getAvailableAddons():
			if add.path.lower().endswith(".pendinginstall"):
				continue
			if add.name.lower() == current_name or "vision" in add.name.lower():
				old_lib_dir = os.path.join(add.path, "globalPlugins", add.name, "lib")
				if not os.path.exists(old_lib_dir):
					old_lib_dir = os.path.join(add.path, "lib")

				if os.path.exists(old_lib_dir):
					backup_dir = os.path.join(tempfile.gettempdir(), "VisionAssistant_Lib_Backup")
					if os.path.exists(_long_path(backup_dir)):
						try:
							shutil.rmtree(_long_path(backup_dir), ignore_errors=True)
						except Exception as e:
							log.warning(f"Failed to clear previous lib backup: {e}")
					os.makedirs(_long_path(backup_dir), exist_ok=True)

					shipped_items = _shipped_lib_items()
					shipped_dir = _shipped_lib_dir()
					copied = False
					for item in os.listdir(old_lib_dir):
						if item == "google-cloud-sdk":
							continue
						src = os.path.join(old_lib_dir, item)
						if shipped_dir and item in shipped_items:
							if not _contains_marker(src) and not _has_extra_content(
								src,
								os.path.join(shipped_dir, item),
							):
								continue
						dst = os.path.join(backup_dir, item)
						try:
							_copy_asset(src, dst)
							copied = True
						except Exception as e:
							log.warning(f"Lib backup failed for {item}: {e}")

					if copied:
						manifest_file = os.path.join(backup_dir, "backup_manifest.json")
						with open(manifest_file, "w", encoding="utf-8") as f:
							json.dump({"timestamp": time.time()}, f)
						log.info("Lib assets backed up for next startup.")
				break
	except Exception as e:
		log.error(f"Lib backup failed: {e}", exc_info=True)
	finally:
		gc.collect()


def _doPostInstall():
	addonDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "globalPlugins", addonName))
	if addonDir not in sys.path:
		sys.path.append(addonDir)

	try:
		from dialogs.donate import requestDonations

		gui.mainFrame.prePopup()
		try:
			requestDonations(gui.mainFrame)

			conf = config.conf["VisionAssistant"]
			api_keys = [
				conf.get("api_key"),
				conf.get("openai_api_key"),
				conf.get("mistral_api_key"),
				conf.get("groq_api_key"),
				conf.get("minimax_api_key"),
				conf.get("custom_api_key"),
			]

			if not any(key and str(key).strip() for key in api_keys):
				# Translators: Message shown after the add-on is installed.
				msg = _(
					"Installation of Vision Assistant Pro is complete. Please make sure to configure your API keys and preferences in the add-on settings to start using the features.",
				)
				# Translators: Title of the installation complete dialog.
				title = _("Installation Complete")
				gui.messageBox(msg, title, wx.OK | wx.ICON_WARNING)
		finally:
			gui.mainFrame.postPopup()
	finally:
		if addonDir in sys.path:
			sys.path.remove(addonDir)


def onInstall():
	_backup_lib_assets()
	wx.CallAfter(_doPostInstall)
