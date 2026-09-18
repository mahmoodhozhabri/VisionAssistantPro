# -*- coding: utf-8 -*-
"""Windows DPAPI-backed storage for Vision Assistant credentials."""

import base64
import ctypes
from ctypes import wintypes
import hashlib
import json
import re


DPAPI_PREFIX = "!!dpapi:v1:"
CREDENTIAL_FIELDS = (
	"api_key",
	"openai_api_key",
	"mistral_api_key",
	"groq_api_key",
	"minimax_api_key",
	"custom_api_key",
)
_ENTROPY = b"VisionAssistantPro:credentials:v1"
_CRYPTPROTECT_UI_FORBIDDEN = 0x1


class CredentialProtectionError(RuntimeError):
	"""Raised when a credential cannot be protected or recovered safely."""


class _DATA_BLOB(ctypes.Structure):
	_fields_ = (("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte)))


def _blob(data):
	buffer = ctypes.create_string_buffer(data)
	return _DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte))), buffer


def _dpapi(operation, data):
	if not hasattr(ctypes, "windll"):
		raise CredentialProtectionError("Windows DPAPI is unavailable")
	input_blob, input_buffer = _blob(data)
	entropy_blob, entropy_buffer = _blob(_ENTROPY)
	output_blob = _DATA_BLOB()
	function = getattr(ctypes.windll.crypt32, operation)
	if operation == "CryptProtectData":
		ok = function(
			ctypes.byref(input_blob),
			"Vision Assistant API credential",
			ctypes.byref(entropy_blob),
			None,
			None,
			_CRYPTPROTECT_UI_FORBIDDEN,
			ctypes.byref(output_blob),
		)
	else:
		description = wintypes.LPWSTR()
		ok = function(
			ctypes.byref(input_blob),
			ctypes.byref(description),
			ctypes.byref(entropy_blob),
			None,
			None,
			_CRYPTPROTECT_UI_FORBIDDEN,
			ctypes.byref(output_blob),
		)
		if description:
			ctypes.windll.kernel32.LocalFree(description)
	# Keep the backing buffers alive until the native call has completed.
	_ = input_buffer, entropy_buffer
	if not ok:
		raise CredentialProtectionError("Windows DPAPI operation failed")
	try:
		return ctypes.string_at(output_blob.pbData, output_blob.cbData)
	finally:
		ctypes.windll.kernel32.LocalFree(output_blob.pbData)


def _protect_bytes(data):
	return _dpapi("CryptProtectData", data)


def _unprotect_bytes(data):
	return _dpapi("CryptUnprotectData", data)


def is_protected(value):
	return isinstance(value, str) and value.startswith(DPAPI_PREFIX)


def protect_credential(value):
	value = "" if value is None else str(value).strip()
	if not value:
		return ""
	if is_protected(value):
		# Validate existing ciphertext rather than wrapping it a second time.
		unprotect_credential(value)
		return value
	try:
		ciphertext = _protect_bytes(value.encode("utf-8"))
		return DPAPI_PREFIX + base64.b64encode(ciphertext).decode("ascii")
	except CredentialProtectionError:
		raise
	except Exception as error:
		raise CredentialProtectionError("Could not protect the credential") from error


def unprotect_credential(value):
	value = "" if value is None else str(value)
	if not value:
		return ""
	if not is_protected(value):
		raise CredentialProtectionError("Refusing to use a plaintext credential")
	try:
		encoded = value[len(DPAPI_PREFIX):]
		return _unprotect_bytes(base64.b64decode(encoded, validate=True)).decode("utf-8")
	except CredentialProtectionError:
		raise
	except Exception as error:
		raise CredentialProtectionError("Could not recover the credential") from error


def get_credential(configuration, field):
	"""Read a credential, migrating legacy plaintext before returning it."""
	value = str(configuration.get(field, "") or "")
	if not value:
		return ""
	if not is_protected(value):
		protected = protect_credential(value)
		configuration[field] = protected
		return value.strip()
	return unprotect_credential(value)


def credential_fingerprint(value):
	return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def credential_redaction_values(protected_value):
	"""Return protected and plaintext forms that must be removed from logs."""
	value = str(protected_value or "")
	if not value:
		return ()
	values = [value]
	if not is_protected(value):
		return tuple(values)
	plaintext = unprotect_credential(value)
	values.append(plaintext)
	# Provider settings may contain several keys separated by commas or lines.
	# Redact each usable key as well as the complete decrypted setting.
	values.extend(part.strip() for part in re.split(r"[\r\n,]+", plaintext) if part.strip())
	return tuple(dict.fromkeys(values))


def migrate_banned_gemini_keys(configuration):
	"""Replace API keys embedded in the quota cache with irreversible fingerprints."""
	raw = configuration.get("banned_gemini_keys", "{}")
	try:
		entries = json.loads(raw)
	except Exception:
		entries = {}
	if not isinstance(entries, dict):
		entries = {}
	changed = False
	migrated = {}
	for key_model, expiry in entries.items():
		key_part, separator, model = str(key_model).partition("::")
		if not key_part.startswith("sha256:"):
			key_part = credential_fingerprint(key_part)
			changed = True
		migrated[key_part + (separator + model if separator else "")] = expiry
	if changed:
		configuration["banned_gemini_keys"] = json.dumps(migrated)
	return changed


def migrate_credentials(configuration):
	updates = {}
	for field in CREDENTIAL_FIELDS:
		value = str(configuration.get(field, "") or "")
		if value and not is_protected(value):
			updates[field] = protect_credential(value)
	# Apply credential changes only after every DPAPI operation succeeds. This
	# prevents a failed migration from leaving a partially updated configuration.
	for field, protected in updates.items():
		configuration[field] = protected
	changed = bool(updates)
	changed = migrate_banned_gemini_keys(configuration) or changed
	return changed


def prepare_restored_credentials(configuration):
	"""Make credentials from a backup safe to install in the current profile.

	Legacy plaintext values are protected for the current Windows user. Existing
	DPAPI values are validated; values protected by another user or computer (or
	otherwise unreadable) are cleared so the remaining settings can still be
	restored. Returns the names of credential fields that were cleared.
	"""
	updates = {}
	unavailable = []
	for field in CREDENTIAL_FIELDS:
		value = str(configuration.get(field, "") or "")
		if not value:
			continue
		if is_protected(value):
			try:
				unprotect_credential(value)
			except CredentialProtectionError:
				updates[field] = ""
				unavailable.append(field)
		else:
			# Protect legacy plaintext before applying any changes. If protection
			# fails, the caller must abort rather than persist plaintext.
			updates[field] = protect_credential(value)
	for field, value in updates.items():
		configuration[field] = value
	migrate_banned_gemini_keys(configuration)
	return tuple(unavailable)


def prepare_backup_credentials(configuration, protect=True):
	"""Prepare credential fields in a copied configuration for JSON export.

	Protected backups retain DPAPI values. Portable backups deliberately contain
	plaintext credentials, but this function never changes the live configuration.
	"""
	for field in CREDENTIAL_FIELDS:
		value = str(configuration.get(field, "") or "")
		if not value:
			continue
		if protect:
			configuration[field] = protect_credential(value)
		elif is_protected(value):
			configuration[field] = unprotect_credential(value)
		else:
			configuration[field] = value.strip()
	return configuration


_AUTH_PATTERNS = (
	re.compile(r"(?i)(authorization\s*[:=]\s*)(?:bearer\s+)?[^\s,;]+"),
	re.compile(r"(?i)((?:x-goog-api-key|api[_-]?key)\s*[:=]\s*)[^\s,;&]+"),
	re.compile(r"(?i)([?&](?:key|api_key|apikey|access_token)=)[^&#\s]+"),
)


def redact_text(value, secrets=()):
	text = str(value)
	for secret in sorted((str(s) for s in secrets if s), key=len, reverse=True):
		text = text.replace(secret, "[REDACTED]")
	for pattern in _AUTH_PATTERNS:
		text = pattern.sub(r"\1[REDACTED]", text)
	return text
