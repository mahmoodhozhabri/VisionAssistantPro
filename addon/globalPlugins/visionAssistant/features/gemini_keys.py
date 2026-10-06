# -*- coding: utf-8 -*-
import base64
import csv
import hashlib
import http.server
import json
import logging
import os
import secrets
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

import addonHandler
import config as nvda_config

from .. import vision_config

log = logging.getLogger(__name__)
addonHandler.initTranslation()

CRM = "https://cloudresourcemanager.googleapis.com/v3"
CRM_V1 = "https://cloudresourcemanager.googleapis.com/v1"
SU = "https://serviceusage.googleapis.com/v1"
AK = "https://apikeys.googleapis.com/v2"
IAM = "https://iam.googleapis.com/v1"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
GEMINI_SERVICE = "generativelanguage.googleapis.com"
APIKEYS_SERVICE = "apikeys.googleapis.com"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_REVOKE_URL = "https://oauth2.googleapis.com/revoke"
CLIENT_ID = "764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com"
CLIENT_SECRET = "d-FL95Q19q7MQmFpd7hHD0Ty"
SCOPES = (
	"openid",
	"https://www.googleapis.com/auth/userinfo.email",
	"https://www.googleapis.com/auth/cloud-platform",
)

_ADDON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GeminiKeysError(Exception):
	def __init__(self, message, status=0):
		self.status = status
		super().__init__(message)


def _notify(callback, message):
	if callback is None:
		return
	try:
		callback(message)
	except Exception as e:
		log.debug(f"Status callback failed: {e}")


def _data_dir():
	data_dir = getattr(vision_config, "DATA_DIR", None)
	if not data_dir:
		try:
			import globalVars

			data_dir = os.path.join(globalVars.appArgs.configPath, "VisionAssistant")
		except Exception as e:
			log.debug(f"Could not use the NVDA configuration folder for the key store: {e}")
			data_dir = os.path.join(_ADDON_DIR, "data")
	os.makedirs(data_dir, exist_ok=True)
	return data_dir


def keys_file():
	return os.path.join(_data_dir(), "gemini_keys.txt")


def csv_file():
	return os.path.join(_data_dir(), "gemini_keys.csv")


def _get_opener(target_url=None):
	try:
		from ..utils.media_capture import get_proxy_opener

		return get_proxy_opener(target_url)
	except Exception as e:
		log.debug(f"Proxy opener unavailable, using the default one: {e}")
		return urllib.request.build_opener()


def _format_api_error(status, detail):
	message = ""
	if isinstance(detail, dict):
		value = detail.get("error", {})
		if isinstance(value, dict):
			value = value.get("message", "")
		if not value:
			value = detail.get("message", "")
		message = str(value or "")
	elif detail:
		message = str(detail)
	# Translators: Error message shown when a Google API call fails, {status} is the HTTP status code and {detail} is Google's own message.
	return _("Google API error (HTTP {status}): {detail}").format(status=status, detail=message)


def http_json(method, url, token=None, body=None, quota_project=None, timeout=90):
	headers = {}
	data = None
	if token:
		headers["Authorization"] = "Bearer " + token
	if quota_project:
		headers["x-goog-user-project"] = quota_project
	if body is not None:
		data = json.dumps(body).encode("utf-8")
		headers["Content-Type"] = "application/json"

	request = urllib.request.Request(url, data=data, method=method)
	for name, value in headers.items():
		request.add_header(name, value)

	opener = _get_opener(url)
	try:
		with opener.open(request, timeout=timeout) as response:
			raw = response.read()
			return json.loads(raw) if raw else None
	except urllib.error.HTTPError as error:
		raw = error.read()
		try:
			detail = json.loads(raw)
		except Exception:
			detail = raw.decode("utf-8", "replace")
		raise GeminiKeysError(_format_api_error(error.code, detail), status=error.code)
	except urllib.error.URLError as error:
		raise GeminiKeysError(str(error.reason))


def _check_cancel(cancel_check):
	if cancel_check is not None and cancel_check():
		# Translators: Error message shown when the user cancels a running Gemini key operation.
		raise GeminiKeysError(_("Operation cancelled."))


def wait_operation(token, base, name, what, timeout=600, quota_project=None, cancel_check=None):
	deadline = time.time() + timeout
	url = base + "/" + name
	while True:
		_check_cancel(cancel_check)
		if time.time() > deadline:
			# Translators: Error message shown when a Google Cloud operation takes too long, {operation} describes the operation.
			raise GeminiKeysError(_("Timed out while waiting for {operation}.").format(operation=what))
		operation = http_json("GET", url, token, quota_project=quota_project)
		if operation.get("done"):
			if operation.get("error"):
				raise GeminiKeysError(_format_api_error(0, operation["error"]))
			return operation
		time.sleep(5)


def _open_browser(url):
	try:
		if not webbrowser.open(url):
			log.debug("The default browser could not open the sign-in page.")
	except Exception as e:
		log.debug(f"Opening the sign-in page failed: {e}")


def credentials_file():
	return os.path.join(_data_dir(), "google_credentials.json")


def _legacy_adc_files():
	files = []
	for variable in ("CLOUDSDK_CONFIG",):
		value = os.environ.get(variable)
		if value:
			files.append(os.path.join(value, "application_default_credentials.json"))
	appdata = os.environ.get("APPDATA")
	if appdata:
		files.append(os.path.join(appdata, "gcloud", "application_default_credentials.json"))
	userprofile = os.environ.get("USERPROFILE") or os.path.expanduser("~")
	files.append(os.path.join(userprofile, ".config", "gcloud", "application_default_credentials.json"))
	return files


def load_credentials():
	primary = credentials_file()
	if os.path.isfile(primary):
		try:
			with open(primary, "r", encoding="utf-8") as f:
				return json.load(f)
		except Exception as e:
			log.debug(f"Could not read credentials from {primary}: {e}")

	for path in _legacy_adc_files():
		if os.path.isfile(path):
			try:
				with open(path, "r", encoding="utf-8") as f:
					data = json.load(f)
					if data.get("refresh_token") or data.get("access_token"):
						return data
			except Exception as e:
				log.debug(f"Could not read legacy credentials from {path}: {e}")
	return {}


def save_credentials(data):
	path = credentials_file()
	try:
		with open(path, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=2)
	except Exception as e:
		log.debug(f"Could not save credentials to {path}: {e}")


def _refresh_access_token(refresh_token):
	payload = urllib.parse.urlencode({
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET,
		"refresh_token": refresh_token,
		"grant_type": "refresh_token",
	}).encode("utf-8")

	request = urllib.request.Request(
		GOOGLE_TOKEN_URL,
		data=payload,
		method="POST",
		headers={"Content-Type": "application/x-www-form-urlencoded"},
	)
	opener = _get_opener(GOOGLE_TOKEN_URL)
	try:
		with opener.open(request, timeout=30) as response:
			raw = response.read()
			return json.loads(raw.decode("utf-8")) if raw else {}
	except urllib.error.HTTPError as error:
		raw = error.read().decode("utf-8", "replace")
		try:
			detail = json.loads(raw)
		except Exception:
			detail = raw
		raise GeminiKeysError(_format_api_error(error.code, detail), status=error.code)
	except urllib.error.URLError as error:
		raise GeminiKeysError(str(error.reason))


def get_access_token():
	creds = load_credentials()
	access_token = creds.get("access_token")
	expires_at = creds.get("expires_at", 0)
	refresh_token = creds.get("refresh_token")

	if creds.get("scope") and "https://www.googleapis.com/auth/cloud-platform" not in creds.get("scope", "").split():
		raise GeminiKeysError(
			# Translators: Error message shown when saved credentials lack Google Cloud permission.
			_("Google Cloud permission was not granted. Please click Sign In again and check the Google Cloud checkbox.")
		)

	if access_token and time.time() < (expires_at - 60):
		return access_token

	if refresh_token:
		try:
			data = _refresh_access_token(refresh_token)
			new_token = data.get("access_token")
			if new_token:
				creds["access_token"] = new_token
				expires_in = data.get("expires_in", 3600)
				creds["expires_at"] = time.time() + expires_in
				if data.get("refresh_token"):
					creds["refresh_token"] = data["refresh_token"]
				save_credentials(creds)
				return new_token
		except Exception as e:
			log.debug(f"Token refresh failed: {e}")

	# Translators: Error message shown when the user is not signed in to Google Cloud.
	raise GeminiKeysError(_("You are not signed in to Google Cloud. Use the Sign In button first."))


def is_signed_in():
	try:
		get_access_token()
		return True
	except Exception:
		return False


def get_account_email():
	creds = load_credentials()
	email = creds.get("account") or creds.get("email") or ""
	if email:
		return email
	try:
		info = http_json("GET", USERINFO_URL, get_access_token())
		email = (info or {}).get("email", "")
		if email:
			creds["account"] = email
			save_credentials(creds)
	except Exception as e:
		log.debug(f"Could not read the signed-in account from the user info: {e}")
		email = ""
	return email


class _OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
	def log_message(self, format, *args):
		pass

	def do_GET(self):
		parsed = urllib.parse.urlparse(self.path)
		query = urllib.parse.parse_qs(parsed.query)
		self.server.auth_code = query.get("code", [None])[0]
		self.server.auth_state = query.get("state", [None])[0]
		self.server.auth_error = query.get("error", [None])[0]

		self.send_response(200)
		self.send_header("Content-Type", "text/html; charset=utf-8")
		self.end_headers()
		if self.server.auth_code:
			# Translators: Title and heading of the web page shown in the browser after successful Google sign-in.
			title = _("Authentication Successful")
			# Translators: Message shown in the browser after successful Google sign-in.
			message = _("Authentication successful! You can now close this browser tab and return to NVDA.")
			html = (
				"<!DOCTYPE html><html dir='auto'><head><meta charset='utf-8'>"
				f"<title>{title}</title>"
				"<style>body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; text-align: center; padding: 40px 20px; line-height: 1.6; background: #fdfdfd; color: #222; } h2 { color: #1a73e8; margin-bottom: 12px; } p { font-size: 16px; color: #555; }</style></head>"
				f"<body><h2>{title}</h2>"
				f"<p>{message}</p>"
				"</body></html>"
			)
		else:
			err = self.server.auth_error or "Unknown error"
			# Translators: Title and heading of the web page shown in the browser when Google sign-in fails.
			fail_title = _("Sign-in Failed")
			html = (
				"<!DOCTYPE html><html dir='auto'><head><meta charset='utf-8'>"
				f"<title>{fail_title}</title>"
				"<style>body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; text-align: center; padding: 40px 20px; line-height: 1.6; background: #fdfdfd; color: #222; } h2 { color: #d93025; margin-bottom: 12px; } p { font-size: 16px; color: #555; }</style></head>"
				f"<body><h2>{fail_title}</h2><p>{err}</p></body></html>"
			)
		self.wfile.write(html.encode("utf-8"))


def sign_in(status_callback=None, cancel_check=None):
	# Translators: Status message shown when the Google sign-in process starts and a browser window will open.
	_notify(status_callback, _("Starting Google sign-in. A browser window will open."))

	state = secrets.token_urlsafe(32)
	code_verifier = secrets.token_urlsafe(64)
	code_challenge = (
		base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("ascii")).digest())
		.decode("ascii")
		.rstrip("=")
	)

	server = http.server.HTTPServer(("127.0.0.1", 0), _OAuthCallbackHandler)
	server.timeout = 1.0
	server.auth_code = None
	server.auth_state = None
	server.auth_error = None
	port = server.server_address[1]
	redirect_uri = f"http://127.0.0.1:{port}/"

	params = {
		"client_id": CLIENT_ID,
		"redirect_uri": redirect_uri,
		"response_type": "code",
		"scope": " ".join(SCOPES),
		"state": state,
		"access_type": "offline",
		"prompt": "consent",
		"enable_granular_consent": "false",
		"code_challenge": code_challenge,
		"code_challenge_method": "S256",
	}
	auth_url = GOOGLE_AUTH_URL + "?" + urllib.parse.urlencode(params)

	# Translators: Status message shown when the add-on opens the browser for Google sign-in.
	_notify(status_callback, _("Opening the browser for sign-in... Please check the Google Cloud permission box."))
	threading.Thread(target=_open_browser, args=(auth_url,), daemon=True).start()

	deadline = time.time() + 300
	try:
		while server.auth_code is None and server.auth_error is None:
			_check_cancel(cancel_check)
			if time.time() > deadline:
				# Translators: Error message shown when Google sign-in times out.
				raise GeminiKeysError(_("Google sign-in timed out."))
			server.handle_request()
	finally:
		try:
			server.server_close()
		except Exception:
			pass

	if server.auth_error:
		# Translators: Error message shown when Google sign-in returns an error, {error} is the error code.
		raise GeminiKeysError(_("Google sign-in failed: {error}").format(error=server.auth_error))
	if server.auth_state != state:
		# Translators: Error message shown when Google sign-in fails due to OAuth state mismatch.
		raise GeminiKeysError(_("Google sign-in failed: state mismatch."))
	if not server.auth_code:
		# Translators: Error message shown when Google sign-in was not completed or no auth code was returned.
		raise GeminiKeysError(_("Google sign-in did not complete."))

	# Translators: Status message shown when exchanging the authorization code for tokens.
	_notify(status_callback, _("Exchanging authorization code..."))
	payload = urllib.parse.urlencode({
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET,
		"code": server.auth_code,
		"code_verifier": code_verifier,
		"grant_type": "authorization_code",
		"redirect_uri": redirect_uri,
	}).encode("utf-8")

	request = urllib.request.Request(
		GOOGLE_TOKEN_URL,
		data=payload,
		method="POST",
		headers={"Content-Type": "application/x-www-form-urlencoded"},
	)
	opener = _get_opener(GOOGLE_TOKEN_URL)
	try:
		with opener.open(request, timeout=30) as response:
			raw = response.read()
			token_data = json.loads(raw.decode("utf-8")) if raw else {}
	except urllib.error.HTTPError as error:
		raw = error.read().decode("utf-8", "replace")
		try:
			detail = json.loads(raw)
		except Exception:
			detail = raw
		raise GeminiKeysError(_format_api_error(error.code, detail), status=error.code)
	except urllib.error.URLError as error:
		raise GeminiKeysError(str(error.reason))

	access_token = token_data.get("access_token")
	refresh_token = token_data.get("refresh_token")
	expires_in = token_data.get("expires_in", 3600)
	if not access_token:
		# Translators: Error message shown when Google returns no access token during authentication.
		raise GeminiKeysError(_("No access token returned by Google."))

	granted_scopes = (token_data.get("scope") or "").split()
	if "https://www.googleapis.com/auth/cloud-platform" not in granted_scopes:
		raise GeminiKeysError(
			# Translators: Error message shown when Google Cloud permission was not consented on Google sign-in.
			_("Google Cloud permission was not granted. Please sign in again and ensure the Google Cloud checkbox is ticked on the Google consent page.")
		)

	email = ""
	try:
		info = http_json("GET", USERINFO_URL, access_token)
		email = (info or {}).get("email", "")
	except Exception as e:
		log.debug(f"Could not fetch user email: {e}")

	creds = {
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET,
		"access_token": access_token,
		"refresh_token": refresh_token,
		"scope": token_data.get("scope", ""),
		"expires_at": time.time() + expires_in,
		"account": email,
	}
	save_credentials(creds)

	# Translators: Status message shown when the Google sign-in completed successfully.
	_notify(status_callback, _("Signed in successfully."))
	return True


def sign_out(status_callback=None):
	# Translators: Status message shown when the stored Google credentials are removed.
	_notify(status_callback, _("Removing the stored Google credentials..."))
	creds = load_credentials()
	token = creds.get("refresh_token") or creds.get("access_token")
	if token:
		try:
			revoke_data = urllib.parse.urlencode({"token": token}).encode("utf-8")
			req = urllib.request.Request(
				GOOGLE_REVOKE_URL,
				data=revoke_data,
				method="POST",
				headers={"Content-Type": "application/x-www-form-urlencoded"},
			)
			opener = _get_opener(GOOGLE_REVOKE_URL)
			with opener.open(req, timeout=10):
				pass
		except Exception as e:
			log.debug(f"Token revocation failed: {e}")

	removed = []
	primary = credentials_file()
	if os.path.isfile(primary):
		try:
			os.remove(primary)
			removed.append(primary)
		except Exception as e:
			log.debug(f"Could not remove {primary}: {e}")

	for path in _legacy_adc_files():
		if os.path.isfile(path):
			try:
				os.remove(path)
				removed.append(path)
			except Exception as e:
				log.debug(f"Could not remove {path}: {e}")

	# Translators: Status message shown when signed out successfully.
	_notify(status_callback, _("Signed out successfully."))
	return removed


def stored_keys_by_project():
	mapping = {}
	for project_id, label, key in load_key_records():
		mapping[project_id] = (label, key)
	return mapping


def stored_keys_list_by_project():
	mapping = {}
	for project_id, label, key in load_key_records():
		if project_id not in mapping:
			mapping[project_id] = []
		mapping[project_id].append((label, key))
	return mapping


def make_project_id():
	return "gemini-" + secrets.token_hex(4)


def list_projects(token, cancel_check=None):
	projects = []
	page_token = ""
	while True:
		_check_cancel(cancel_check)
		url = CRM_V1 + "/projects"
		if page_token:
			url += "?pageToken=" + urllib.parse.quote(page_token)
		data = http_json("GET", url, token)
		projects.extend((data or {}).get("projects", []))
		page_token = (data or {}).get("nextPageToken", "")
		if not page_token:
			break
	return projects


def list_keys(token, project_id, cancel_check=None):
	keys = []
	page_token = ""
	while True:
		_check_cancel(cancel_check)
		url = "%s/projects/%s/locations/global/keys" % (AK, project_id)
		if page_token:
			url += "?pageToken=" + urllib.parse.quote(page_token)
		data = http_json("GET", url, token, quota_project=project_id)
		keys.extend((data or {}).get("keys", []))
		page_token = (data or {}).get("nextPageToken", "")
		if not page_token:
			break
	return keys


def get_key_string(token, key_name, quota_project=None, cancel_check=None):
	_check_cancel(cancel_check)
	url = "%s/%s/keyString" % (AK, key_name)
	data = http_json("GET", url, token, quota_project=quota_project)
	return (data or {}).get("keyString", "")


def fetch_keys_for_project(token, project_id, cancel_check=None):
	try:
		keys = list_keys(token, project_id, cancel_check=cancel_check)
	except GeminiKeysError as e:
		err_str = str(e).lower()
		if "not been used" in err_str or "disabled" in err_str or getattr(e, "status", 0) == 403:
			try:
				enable_service(token, project_id, APIKEYS_SERVICE, cancel_check=cancel_check)
				keys = list_keys(token, project_id, cancel_check=cancel_check)
			except Exception as enable_err:
				log.debug(f"Could not enable API Keys API for {project_id}: {enable_err}")
				return []
		else:
			log.debug(f"Could not list keys for project {project_id}: {e}")
			return []
	except Exception as e:
		log.debug(f"Could not list keys for project {project_id}: {e}")
		return []

	results = []
	for k in keys:
		_check_cancel(cancel_check)
		key_name = k.get("name")
		if not key_name:
			continue
		display_name = k.get("displayName") or "Gemini API Key"
		try:
			key_string = get_key_string(token, key_name, quota_project=project_id, cancel_check=cancel_check)
			if key_string:
				results.append((display_name, key_string))
		except Exception as e:
			log.debug(f"Could not fetch key string for {key_name}: {e}")
	return results


def sync_cloud_keys(token, projects=None, cancel_check=None):
	saved_mapping = stored_keys_by_project()
	if projects is None:
		projects = list_projects(token, cancel_check=cancel_check)

	synced = []
	for project in projects:
		_check_cancel(cancel_check)
		project_id = project.get("projectId")
		state = project.get("lifecycleState", "ACTIVE")
		if state != "ACTIVE" or not project_id:
			continue
		if project_id in saved_mapping:
			continue

		keys = fetch_keys_for_project(token, project_id, cancel_check=cancel_check)
		for label, key_string in keys:
			save_key_record(project_id, label, key_string)
			saved_mapping[project_id] = (label, key_string)
			synced.append((project_id, label, key_string))
			break
	return synced


def create_project(token, project_id, display_name, cancel_check=None, status_callback=None):
	# Translators: Status message shown while creating a Google Cloud project.
	_notify(status_callback, _("Creating the project..."))
	result = http_json(
		"POST",
		CRM + "/projects",
		token,
		body={"projectId": project_id, "displayName": display_name},
	)
	operation = wait_operation(
		token,
		CRM,
		result["name"],
		# Translators: Name of the Google Cloud operation that creates a project, shown if it times out.
		_("project creation"),
		cancel_check=cancel_check,
	)
	return operation.get("response", {})


def enable_service(token, project_id, service, cancel_check=None, status_callback=None):
	# Translators: Status message shown while enabling a Google API on a project.
	_notify(status_callback, _("Enabling an API..."))
	last_error = None
	for attempt, delay in enumerate((0, 10, 20, 40, 60, 90)):
		if attempt > 0:
			# Translators: Status message shown while retrying to enable a Google API, {seconds} is the delay in seconds.
			_notify(status_callback, _("Retrying in {seconds} seconds...").format(seconds=delay))
			time.sleep(delay)
		_check_cancel(cancel_check)
		try:
			result = http_json(
				"POST",
				"%s/projects/%s/services/%s:enable" % (SU, project_id, service),
				token,
				body={},
			)
			name = str((result or {}).get("name", ""))
			if (result or {}).get("done") or "noop" in name.lower():
				return
			wait_operation(
				token,
				SU,
				result["name"],
				# Translators: Name of the Google Cloud operation that enables an API, shown if it times out.
				_("enabling the API"),
				cancel_check=cancel_check,
			)
			return
		except GeminiKeysError as error:
			last_error = error
			if "not found" not in str(error).lower():
				break
	raise last_error


def _get_or_create_service_account(token, project_id, account_id, display_name):
	email = "%s@%s.iam.gserviceaccount.com" % (account_id, project_id)
	try:
		result = http_json(
			"POST",
			"%s/projects/%s/serviceAccounts" % (IAM, project_id),
			token,
			body={"accountId": account_id, "serviceAccount": {"displayName": display_name}},
		)
		return (result or {}).get("email", email)
	except GeminiKeysError as error:
		if error.status == 409:
			return email
		raise


def create_gemini_key(token, project_id, display_name, cancel_check=None, status_callback=None):
	# Translators: Status message shown while creating a Gemini API key.
	_notify(status_callback, _("Creating the API key..."))
	service_account_email = _get_or_create_service_account(
		token, project_id, "gemini-keys", "Gemini keys"
	)
	body = {
		"displayName": display_name,
		"serviceAccountEmail": service_account_email,
		"restrictions": {"apiTargets": [{"service": GEMINI_SERVICE}]},
	}
	result = http_json(
		"POST",
		"%s/projects/%s/locations/global/keys" % (AK, project_id),
		token,
		body=body,
		quota_project=project_id,
	)
	operation = wait_operation(
		token,
		AK,
		result["name"],
		# Translators: Name of the Google Cloud operation that creates an API key, shown if it times out.
		_("API key creation"),
		quota_project=project_id,
		cancel_check=cancel_check,
	)
	return (operation.get("response") or {}).get("keyString", "")


def delete_key(token, key_name, project_id=None, cancel_check=None):
	result = http_json("DELETE", AK + "/" + key_name, token, quota_project=project_id)
	if result and result.get("name"):
		wait_operation(
			token,
			AK,
			result["name"],
			# Translators: Name of the Google Cloud operation that deletes an API key, shown if it times out.
			_("API key deletion"),
			quota_project=project_id,
			cancel_check=cancel_check,
		)


def save_key_record(project_id, label, key_string):
	for p_id, _lbl, k_str in load_key_records():
		if p_id == project_id and k_str == key_string:
			return
	line = "%s | %s | %s" % (project_id, label, key_string)
	try:
		with open(keys_file(), "a", encoding="utf-8") as handle:
			handle.write(line + "\n")
	except OSError as error:
		log.debug(f"Could not save the API key to a file: {error}")


def load_key_records():
	records = []
	path = keys_file()
	if not os.path.exists(path):
		return records
	try:
		with open(path, "r", encoding="utf-8") as handle:
			for line in handle:
				line = line.strip()
				if not line:
					continue
				parts = [part.strip() for part in line.split("|")]
				if len(parts) >= 3:
					records.append((parts[0], parts[1], parts[2]))
	except OSError as error:
		log.debug(f"Could not read the saved API keys: {error}")
	return records


def export_keys_csv(target_path=None, keys_only=False):
	records = load_key_records()
	if not records:
		# Translators: Error message shown when trying to export keys but no keys are saved.
		raise GeminiKeysError(_("There are no saved API keys to export."))
	path = target_path or csv_file()
	with open(path, "w", encoding="utf-8-sig", newline="") as handle:
		writer = csv.writer(handle)
		if keys_only:
			# Translators: Column header for API key value in exported Gemini API keys CSV file.
			header_key = _("Key")
			writer.writerow([header_key])
			for record in records:
				writer.writerow([record[2]])
		else:
			# Translators: Column header for project name in exported Gemini API keys CSV file.
			header_proj = _("Project")
			# Translators: Column header for key label in exported Gemini API keys CSV file.
			header_name = _("Name")
			# Translators: Column header for API key value in exported Gemini API keys CSV file.
			header_key = _("Key")
			writer.writerow([header_proj, header_name, header_key])
			for record in records:
				writer.writerow(list(record))
	return path


def export_keys_txt(target_path=None, keys_only=False):
	records = load_key_records()
	if not records:
		# Translators: Error message shown when trying to export keys but no keys are saved.
		raise GeminiKeysError(_("There are no saved API keys to export."))
	path = target_path or os.path.join(_data_dir(), "gemini_api_keys.txt")
	with open(path, "w", encoding="utf-8") as handle:
		if keys_only:
			for record in records:
				handle.write(record[2] + "\n")
		else:
			for record in records:
				handle.write(f"{record[0]} | {record[1]} | {record[2]}\n")
	return path


def current_addon_keys():
	raw = nvda_config.conf["VisionAssistant"].get("api_key", "") or ""
	return [part.strip() for part in raw.replace("\n", ",").split(",") if part.strip()]


def add_keys_to_addon(keys):
	parts = current_addon_keys()
	added = 0
	for key in keys:
		value = (key or "").strip()
		if value and value not in parts:
			parts.append(value)
			added += 1
	if added:
		nvda_config.conf["VisionAssistant"]["api_key"] = ", ".join(parts)
	return added


def remove_keys_from_addon(keys):
	parts = current_addon_keys()
	removed = 0
	for key in keys:
		value = (key or "").strip()
		if value and value in parts:
			parts.remove(value)
			removed += 1
	if removed:
		nvda_config.conf["VisionAssistant"]["api_key"] = ", ".join(parts)
	return removed


def remove_key_record(project_id, key_value):
	records = load_key_records()
	remaining = [
		record
		for record in records
		if not (record[0] == project_id and record[2] == key_value)
	]
	if len(remaining) == len(records):
		return False
	try:
		with open(keys_file(), "w", encoding="utf-8") as handle:
			for project, label, key in remaining:
				handle.write("%s | %s | %s\n" % (project, label, key))
	except OSError as error:
		log.debug(f"Could not update the saved API keys: {error}")
		return False
	return True
