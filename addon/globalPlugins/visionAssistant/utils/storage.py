# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import os
import re
import threading
import time
import unicodedata

log = logging.getLogger(__name__)

_HISTORY_MAX_ITEMS = 100
_GEMINI_CACHE_MAX_AGE = 48 * 3600
_OCR_TEXT_MAX_ENTRIES = 20
_OCR_TEXT_MAX_PAGES = 2000


class JsonStore:
	_file_lock = threading.Lock()

	def __init__(self, file_path):
		self._file_path = file_path

	def _read_all(self):
		if not os.path.exists(self._file_path):
			return {}
		try:
			with open(self._file_path, "r", encoding="utf-8") as f:
				data = json.load(f)
			if isinstance(data, dict):
				return data
		except Exception:
			pass
		return {}

	def _write_all(self, data):
		try:
			tmp = self._file_path + ".tmp"
			with open(tmp, "w", encoding="utf-8") as f:
				json.dump(data, f, ensure_ascii=False)
			os.replace(tmp, self._file_path)
		except Exception as e:
			log.warning(f"Failed to write {self._file_path}: {e}")

	def get(self, key):
		with JsonStore._file_lock:
			return self._read_all().get(key)

	def set(self, key, value):
		with JsonStore._file_lock:
			data = self._read_all()
			data[key] = value
			self._write_all(data)

	def delete(self, key):
		with JsonStore._file_lock:
			data = self._read_all()
			if key in data:
				del data[key]
				self._write_all(data)

	def clear(self):
		with JsonStore._file_lock:
			self._write_all({})


class HistoryStore(JsonStore):
	def load_all(self):
		with JsonStore._file_lock:
			items = [i for i in self._read_all().values() if isinstance(i, dict)]
		return sorted(items, key=lambda i: i.get("timestamp", 0), reverse=True)

	def save(self, item):
		if not isinstance(item, dict) or not item.get("id") or not item.get("type"):
			return
		with JsonStore._file_lock:
			data = self._read_all()
			data[item["id"]] = item
			items = sorted(data.values(), key=lambda i: i.get("timestamp", 0), reverse=True)
			data = {i["id"]: i for i in items[:_HISTORY_MAX_ITEMS]}
			self._write_all(data)

	def delete(self, item_id):
		super().delete(item_id)

	def clear(self, item_type=None):
		with JsonStore._file_lock:
			data = self._read_all()
			if item_type:
				data = {k: v for k, v in data.items() if v.get("type") != item_type}
			else:
				data = {}
			self._write_all(data)


class SeriesCharacterStore(JsonStore):
	@staticmethod
	def character_key(name):
		value = unicodedata.normalize("NFKC", str(name or "")).strip().casefold()
		value = value.translate(str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"}))
		value = "".join(c for c in unicodedata.normalize("NFKD", value) if not unicodedata.combining(c))
		value = re.sub(r"[^\w]+", " ", value, flags=re.UNICODE)
		return " ".join(value.split())

	def _get_entry(self, name):
		entry = self.get(name)
		return entry if isinstance(entry, dict) else {}

	def get_series(self, name):
		entry = self._get_entry(name)
		characters = entry.get("characters", [])
		if not isinstance(characters, list):
			return []
		result = []
		for character in characters:
			if not isinstance(character, dict) or not character.get("name"):
				continue
			result.append(dict(character))
		return result

	def save_series(self, name, characters, manual=False):
		clean_characters = []
		for character in characters or []:
			if not isinstance(character, dict) or not character.get("name"):
				continue
			item = dict(character)
			if manual:
				item["manual"] = True
			clean_characters.append(item)
		all_manual = bool(clean_characters) and all(
			character.get("manual", False) for character in clean_characters
		)
		self.set(
			name,
			{
				"characters": clean_characters,
				"updated": time.time(),
				"manual_complete": bool(manual) or all_manual,
			},
		)

	def merge_auto_characters(self, name, characters, limit=50):
		if not name:
			return False
		existing = self.get_series(name)
		existing_by_key = {
			self.character_key(character.get("name")): index
			for index, character in enumerate(existing)
			if self.character_key(character.get("name"))
		}
		changed = False
		for character in characters or []:
			if not isinstance(character, dict) or not character.get("name"):
				continue
			name_value = character.get("name").strip()
			key = self.character_key(name_value)
			if not key:
				continue
			description = (character.get("description") or character.get("Description") or "").strip()
			if key in existing_by_key:
				current = existing[existing_by_key[key]]
				if not current.get("manual") and description and current.get("notes") != description:
					current["notes"] = description
					changed = True
				continue
			if len(existing) >= limit:
				continue
			existing.append({"name": name_value, "notes": description, "manual": False})
			existing_by_key[key] = len(existing) - 1
			changed = True
		if changed:
			self.save_series(name, existing[:limit])
		return changed

	def list_series(self):
		with JsonStore._file_lock:
			data = self._read_all()
		return sorted((k for k, v in data.items() if isinstance(v, dict)), key=str.casefold)


def key_fingerprint(api_key):
	if not api_key:
		return None
	return hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:16]


class GeminiFileCache(JsonStore):
	def get(self, path, api_key):
		entry = super().get(path)
		if not entry:
			return None
		if entry.get("key_fp") != key_fingerprint(api_key):
			return None
		if time.time() - entry.get("uploaded_at", 0) >= _GEMINI_CACHE_MAX_AGE:
			return None
		return entry.get("file_uri")

	def put(self, path, api_key, file_uri):
		self.set(
			path,
			{
				"file_uri": file_uri,
				"uploaded_at": time.time(),
				"key_fp": key_fingerprint(api_key),
			},
		)


def file_signature(path):
	try:
		st = os.stat(path)
		return {"mtime": st.st_mtime, "size": st.st_size}
	except Exception:
		return None


class OCRTextCache(JsonStore):
	def get_valid(self, key):
		entry = self.get(key)
		if not entry:
			return None
		files = entry.get("files") or {}
		for path, sig in files.items():
			if file_signature(path) != sig:
				return None
		return entry

	def delete_matching(self, paths):
		want = sorted(paths)
		prefix = "document|" + "|".join(want)
		with JsonStore._file_lock:
			data = self._read_all()
			changed = False
			for key in list(data):
				entry = data.get(key) or {}
				if sorted(entry.get("paths") or []) == want:
					del data[key]
					changed = True
				elif key == prefix or key.startswith(prefix + "|engine="):
					del data[key]
					changed = True
			if changed:
				self._write_all(data)

	def put(self, key, entry):
		if len(entry.get("pages", {})) > _OCR_TEXT_MAX_PAGES:
			return
		with JsonStore._file_lock:
			data = self._read_all()
			data[key] = entry
			items = sorted(data.items(), key=lambda kv: kv[1].get("timestamp", 0), reverse=True)
			data = dict(items[:_OCR_TEXT_MAX_ENTRIES])
			self._write_all(data)
