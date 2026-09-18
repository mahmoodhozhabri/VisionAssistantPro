# -*- coding: utf-8 -*-
import os
import json
import logging
import re
import time
import datetime
import base64
from urllib import request, error

import addonHandler
import config as nvda_config
import core
import ui

from ... import plugin_state
from ... import vision_config
from ...utils import error_contract
from ...utils.media_capture import get_proxy_opener, ProgressFileReader
from ...prompt_utils import get_prompt_text, apply_prompt_template
from ..core import _apply_gemma_thinking_patch, _extract_text_from_parts

log = logging.getLogger(__name__)


def _request_with_api_key(url, key, **kwargs):
    """Build a Gemini request using auth-key headers for Google's API.

    Custom Gemini-compatible endpoints retain the legacy query parameter
    because not all third-party servers implement Google's auth header.
    """
    headers = dict(kwargs.pop("headers", {}) or {})
    if nvda_config.conf["VisionAssistant"]["active_provider"] == "gemini":
        headers["x-goog-api-key"] = key
    else:
        connector = "&" if "?" in url else "?"
        url = f"{url}{connector}key={key}"
    return request.Request(url, headers=headers, **kwargs)

addonHandler.initTranslation()


def _pacific_utc_offset(now):
    dt = datetime.datetime.fromtimestamp(now, datetime.timezone.utc)
    year = dt.year
    march1 = datetime.date(year, 3, 1)
    march_second_sunday = march1 + datetime.timedelta(days=(6 - march1.weekday()) % 7 + 7)
    nov1 = datetime.date(year, 11, 1)
    nov_first_sunday = nov1 + datetime.timedelta(days=(6 - nov1.weekday()) % 7)
    if march_second_sunday <= dt.date() < nov_first_sunday:
        return 7 * 3600
    return 8 * 3600


class GeminiHandler:
    _working_key_idx = 0
    _file_uri_keys = {}
    _file_durations = {}
    _max_retries = 10

    @staticmethod
    def _get_current_model_for_ban(task=None):
        p = nvda_config.conf["VisionAssistant"]["active_provider"]
        if p == "custom":
            return nvda_config.conf["VisionAssistant"].get("custom_model_name", "default").strip()

        model = nvda_config.conf["VisionAssistant"].get("model_name", "gemini-3.6-flash").strip()
        if not model: model = "gemini-3.6-flash"

        adv_routing = nvda_config.conf["VisionAssistant"].get("advanced_model_routing", False)
        if adv_routing and task:
            adv = ""
            if task == "video":
                adv = nvda_config.conf["VisionAssistant"].get("gemini_video_model", "").strip()
            elif task == "ocr":
                adv = nvda_config.conf["VisionAssistant"].get("gemini_ocr_model", "").strip()
            elif task == "stt":
                adv = nvda_config.conf["VisionAssistant"].get("gemini_stt_model", "").strip()
            elif task == "tts":
                adv = nvda_config.conf["VisionAssistant"].get("gemini_tts_model", "").strip()
            elif task == "operator":
                adv = nvda_config.conf["VisionAssistant"].get("gemini_operator_model", "").strip()
            elif task == "live":
                adv = nvda_config.conf["VisionAssistant"].get("gemini_live_model", "").strip()

            if adv and "Default" not in adv and "Auto" not in adv:
                model = adv

        return model

    @staticmethod
    def _is_key_banned(key, model=None, task=None):
        from ...utils.secure_credentials import credential_fingerprint
        banned_str = nvda_config.conf["VisionAssistant"].get("banned_gemini_keys", "{}")
        try:
            banned = json.loads(banned_str)
        except Exception:
            banned = {}

        if model is None:
            model = GeminiHandler._get_current_model_for_ban(task=task)
        key_model = f"{credential_fingerprint(key)}::{model}"

        ban_time = banned.get(key_model)
        if not ban_time: return False

        if time.time() < ban_time:
            return True

        del banned[key_model]

        def update_config(b_str):
            nvda_config.conf["VisionAssistant"]["banned_gemini_keys"] = b_str

        core.callLater(0, update_config, json.dumps(banned))
        return False

    @staticmethod
    def _ban_key(key, minutes=None, model=None):
        from ...utils.secure_credentials import credential_fingerprint
        if isinstance(minutes, bool):
            if minutes:
                minutes = None
            else:
                return

        banned_str = nvda_config.conf["VisionAssistant"].get("banned_gemini_keys", "{}")
        try:
            banned = json.loads(banned_str)
        except Exception:
            banned = {}

        now = time.time()
        if minutes is not None:
            reset_ts = now + (minutes * 60)
        else:
            gm = time.gmtime(now)
            seconds_since_midnight = gm.tm_hour * 3600 + gm.tm_min * 60 + gm.tm_sec
            midnight_utc = now - seconds_since_midnight
            reset_ts = midnight_utc + _pacific_utc_offset(now)
            if now >= reset_ts:
                reset_ts += 24 * 3600

        if model is None:
            model = GeminiHandler._get_current_model_for_ban()
        key_model = f"{credential_fingerprint(key)}::{model}"

        banned[key_model] = reset_ts

        def update_config(b_str):
            nvda_config.conf["VisionAssistant"]["banned_gemini_keys"] = b_str

        core.callLater(0, update_config, json.dumps(banned))

    @staticmethod
    def _get_api_keys(task=None):
        from ..core import AIHandler
        p = nvda_config.conf["VisionAssistant"]["active_provider"]
        keys = AIHandler.get_keys(p)
        if not keys and p == "custom":
            keys = [""]

        available_keys = [k for k in keys if not GeminiHandler._is_key_banned(k, task=task)]
        return available_keys

    @staticmethod
    def is_key_exhausted_error(err_msg):
        return error_contract.is_key_exhausted_error(err_msg)

    @staticmethod
    def _get_opener(url=None):
        return get_proxy_opener(url)

    @staticmethod
    def _upload_file_common(file_path, mime_type, key, report_callback=None, abort_checker=None):
        from ..core import AIHandler
        base_upload_url = AIHandler.get_endpoint("upload")
        file_size = os.path.getsize(file_path)

        def default_progress_callback(percent):
            # Translators: Status message showing the file upload progress percentage.
            msg = _("Uploading: {percent}%").format(percent=percent)
            if report_callback:
                report_callback(msg)
            else:
                if plugin_state.plugin_instance:
                    plugin_state.plugin_instance.report_status(msg)
                else:
                    core.callLater(0, ui.message, msg)

        try:
            headers_init = {
                "X-Goog-Upload-Protocol": "resumable",
                "X-Goog-Upload-Command": "start",
                "X-Goog-Upload-Header-Content-Length": str(file_size),
                "X-Goog-Upload-Header-Content-Type": mime_type,
                "Content-Type": "application/json",
                "x-goog-api-key": key,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            }
            req_init = request.Request(base_upload_url, data=json.dumps({"file": {"display_name": os.path.basename(file_path)}}).encode(), headers=headers_init, method="POST")
            opener = get_proxy_opener()

            with opener.open(req_init, timeout=120) as r:
                upload_url = r.headers.get("x-goog-upload-url")

            if not upload_url or (abort_checker and abort_checker()):
                return None, None

            headers_up = {
                "Content-Length": str(file_size),
                "X-Goog-Upload-Offset": "0",
                "X-Goog-Upload-Command": "upload, finalize",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            }

            reader = ProgressFileReader(file_path, callback=default_progress_callback, abort_checker=abort_checker)
            req_up = request.Request(upload_url, data=reader, headers=headers_up, method="POST")

            with opener.open(req_up, timeout=3600) as r:
                res = json.loads(r.read().decode())
                uri, name = res['file']['uri'], res['file']['name']

            if abort_checker and abort_checker():
                return None, None

            p_active = nvda_config.conf["VisionAssistant"]["active_provider"]
            base_api_url = AIHandler.get_base_url(p_active).rstrip('/')
            clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', base_api_url, flags=re.IGNORECASE)

            for attempt in range(150):
                if abort_checker and abort_checker(): return None, None
                check_url = f"{clean_base}/v1beta/{name}"
                req_check = _request_with_api_key(check_url, key, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"})
                try:
                    with opener.open(req_check, timeout=30) as r:
                        data = json.loads(r.read().decode())
                        if data.get('state') == "ACTIVE":
                            GeminiHandler._register_file_uri(uri, key)
                            duration_sec = None
                            v_meta = data.get('videoMetadata') or data.get('video_metadata') or {}
                            dur_str = v_meta.get('videoDuration') or v_meta.get('video_duration') or v_meta.get('duration') or ''
                            if dur_str:
                                try: duration_sec = float(dur_str.rstrip('s'))
                                except Exception as e: log.debug(f"Duration parse failed: {e}")
                            if duration_sec:
                                if not hasattr(GeminiHandler, '_file_durations'):
                                    GeminiHandler._file_durations = {}
                                GeminiHandler._file_durations[uri] = duration_sec
                            return uri, duration_sec
                        if data.get('state') == "FAILED":
                            break
                except Exception as e: log.debug(f"File state poll failed: {e}")
                for step in range(4):
                    if abort_checker and abort_checker(): return None, None
                    time.sleep(0.5)

            return None, None
        except error.HTTPError as e:
            err_msg = GeminiHandler._handle_error(e)
            if hasattr(e, 'code') and e.code == 429:
                is_daily = getattr(e, 'is_daily', False)
                is_fatal_error = error_contract.is_daily_quota_error(err_msg)
                if is_daily or is_fatal_error:
                    GeminiHandler._ban_key(key)
            raise e

    @staticmethod
    def _handle_error(e):
        server_msg = getattr(e, 'parsed_msg', None)
        retry_delay = getattr(e, 'retry_delay', None)
        is_daily_quota = getattr(e, 'is_daily', False)

        if server_msg is not None:
            return server_msg

        if hasattr(e, 'read'):
            try:
                if not hasattr(e, '_cached_raw_err'):
                    e._cached_raw_err = e.read().decode('utf-8')
                raw_err = e._cached_raw_err

                log.error(f"RAW API ERROR RESPONSE: {raw_err}")
                if raw_err:
                    err_json = json.loads(raw_err)
                    err_val = err_json.get("error")
                    if isinstance(err_val, dict):
                        server_msg = err_val.get("message")

                        details = err_val.get("details", [])
                        for item in details:
                            if not isinstance(item, dict):
                                continue

                            if "RetryInfo" in str(item.get("@type", "")):
                                delay_str = item.get("retryDelay", "")
                                if delay_str and delay_str.endswith("s"):
                                    try:
                                        retry_delay = float(delay_str[:-1])
                                    except Exception:
                                        pass

                            elif "QuotaFailure" in str(item.get("@type", "")):
                                violations = item.get("violations", [])
                                for viol in violations:
                                    if isinstance(viol, dict):
                                        q_id = str(viol.get("quotaId", "")).lower()
                                        if any(x in q_id for x in ["perday", "requestsperday", "daily"]):
                                            is_daily_quota = True
                    else:
                        server_msg = err_val or err_json.get("message")
            except Exception as ex:
                log.error(f"Failed to parse raw error: {ex}")

        if server_msg:
            if is_daily_quota and "requestsperday" not in server_msg.lower():
                # Translators: Note appended to the API error message when the daily RequestsPerDay quota limit is reached.
                server_msg += _(" (RequestsPerDay quota exceeded)")
            e.parsed_msg = server_msg
            e.is_daily = is_daily_quota
            if retry_delay is not None:
                e.retry_delay = retry_delay
            return server_msg

        if hasattr(e, 'code'):
            # Translators: Error message for Bad Request (400)
            if e.code == 400: return _("Error 400: Bad Request (Check API Key)")
            # Translators: Error message for Forbidden (403)
            if e.code == 403: return _("Error 403: Forbidden (Check Region)")
            if e.code == 429: return "QUOTA_EXCEEDED"
            if e.code >= 500: return "SERVER_ERROR"

        return str(e)

    @staticmethod
    def _call_with_retry(func_logic, key, *args, max_retries=None):
        if max_retries is None:
            max_retries = GeminiHandler._max_retries
        last_exc = None
        for attempt in range(max_retries):
            try:
                return func_logic(key, *args)
            except error.HTTPError as e:
                err_msg = GeminiHandler._handle_error(e)
                err_msg_lower = err_msg.lower()
                e.parsed_msg = err_msg

                is_retryable = False
                if hasattr(e, 'code') and e.code >= 500:
                    is_retryable = True

                if hasattr(e, 'code') and e.code == 429:
                    used_model = None
                    if hasattr(e, 'url') and e.url and "/models/" in e.url:
                        used_model = e.url.split("/models/")[-1].split(":")[0].split("?")[0]

                    if error_contract.is_daily_quota_error(err_msg_lower):
                        GeminiHandler._ban_key(key, model=used_model)
                        is_retryable = False
                    else:
                        is_retryable = True
                elif "high demand" in err_msg_lower or "exhausted" in err_msg_lower or "quota" in err_msg_lower:
                    used_model = None
                    if hasattr(e, 'url') and e.url and "/models/" in e.url:
                        used_model = e.url.split("/models/")[-1].split(":")[0].split("?")[0]

                    if not error_contract.is_daily_quota_error(err_msg_lower):
                        is_retryable = True
                    else:
                        GeminiHandler._ban_key(key, model=used_model)

                delay_sec = getattr(e, 'retry_delay', None)
                if delay_sec is None:
                    match = re.search(r"retry in ([\d\.]+)s", err_msg_lower)
                    if match:
                        try: delay_sec = float(match.group(1))
                        except Exception as e: log.debug(f"Retry delay parse failed: {e}")

                if delay_sec is not None and delay_sec > 0 and is_retryable:
                    n_keys = len(GeminiHandler._get_api_keys())
                    if n_keys > 1:
                        is_retryable = False
                    else:
                        if attempt == 0:
                            time.sleep(delay_sec + 0.5)
                            last_exc = e
                            continue
                        else:
                            is_retryable = False

                if not is_retryable:
                    raise e

                last_exc = e
            except error.URLError as e:
                last_exc = e

            if attempt < max_retries - 1:
                log.debug(f"Gemini retry attempt {attempt + 2}/{max_retries} in {1.0 * (attempt + 1):.1f}s")
                time.sleep(1.0 * (attempt + 1))
        raise last_exc

    @staticmethod
    def _register_file_uri(uri, key):
        if uri and key:
            GeminiHandler._file_uri_keys[uri] = key
            while len(GeminiHandler._file_uri_keys) > 200:
                GeminiHandler._file_uri_keys.pop(next(iter(GeminiHandler._file_uri_keys)))

    @staticmethod
    def _get_registered_key(uri):
        if not uri:
            return None
        return GeminiHandler._file_uri_keys.get(uri)

    @staticmethod
    def _call_with_key(func_logic, key, *args, max_retries=None):
        try:
            return GeminiHandler._call_with_retry(func_logic, key, *args, max_retries=max_retries)
        except error.HTTPError as e:
            err_msg = getattr(e, 'parsed_msg', GeminiHandler._handle_error(e))
            if err_msg == "QUOTA_EXCEEDED":
                # Translators: Message of a dialog which may pop up while performing an AI call
                err_msg = _("Error 429: Quota Exceeded (Try later)")
            elif err_msg == "SERVER_ERROR":
                err_msg = _("Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
            return "ERROR:" + err_msg
        except Exception as e:
            log.error(f"Gemini call with key failed: {e}", exc_info=True)
            return "ERROR:" + str(e)

    @staticmethod
    def _logic(key, prompt, attachments, json_mode, task="chat"):
        from ..core import AIHandler
        p_active = nvda_config.conf["VisionAssistant"]["active_provider"]
        model = ""
        if p_active == "custom":
            model = nvda_config.conf["VisionAssistant"]["custom_model_name"].strip()

        base_endpoint = AIHandler.get_endpoint(task, model_override=model if model else None)
        url = base_endpoint

        temp = nvda_config.conf["VisionAssistant"].get("ai_temperature", 0.7)
        if isinstance(prompt, list):
            contents = prompt
        else:
            parts = []
            if attachments:
                for att in attachments:
                    if 'file_uri' in att:
                        fd_part = {
                            "fileData": {
                                "mimeType": att['mime_type'],
                                "fileUri": att['file_uri']
                            }
                        }
                        if att.get('video_metadata'):
                            fd_part['videoMetadata'] = {
                                "startOffset": att['video_metadata'].get('start_offset'),
                                "endOffset": att['video_metadata'].get('end_offset')
                            }
                        parts.append(fd_part)
                    elif 'data' in att:
                        parts.append({"inlineData": {"mimeType": att['mime_type'], "data": att['data']}})
            if prompt: parts.append({"text": prompt})
            contents = [{"parts": parts}]

        payload = {
            "contents": contents,
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }
        if json_mode: payload["generationConfig"] = {"responseMimeType": "application/json"}

        _apply_gemma_thinking_patch(payload, base_endpoint)

        headers = {"Content-Type": "application/json"}

        if task == "video" and ":generateContent" in base_endpoint:
            stream_endpoint = base_endpoint.replace(":generateContent", ":streamGenerateContent")
            s_connector = "&" if "?" in stream_endpoint else "?"
            stream_url = f"{stream_endpoint}{s_connector}alt=sse"
            req = _request_with_api_key(stream_url, key, data=json.dumps(payload).encode('utf-8'), headers=headers)

            collected = []
            block_reason = None
            safety_blocked = False
            with GeminiHandler._get_opener(stream_url).open(req, timeout=600) as r:
                for raw_line in r:
                    line = raw_line.decode('utf-8', 'ignore').strip()
                    if not line or not line.startswith("data:"):
                        continue
                    chunk = line[5:].strip()
                    if not chunk or chunk == "[DONE]":
                        continue
                    try:
                        obj = json.loads(chunk)
                    except Exception:
                        continue
                    pf = obj.get('promptFeedback')
                    if pf and pf.get('blockReason'):
                        block_reason = pf['blockReason']
                    for cand in obj.get('candidates', []):
                        if cand.get('finishReason') == "SAFETY":
                            safety_blocked = True
                        collected.append(_extract_text_from_parts(cand.get('content', {}).get('parts', [])))

            text = "".join(collected)
            if text:
                return text
            if block_reason:
                # Translators: Error prefix shown when the AI response is blocked by safety filters.
                return "ERROR:" + _("Blocked by AI Safety Filters: ") + block_reason
            if safety_blocked:
                # Translators: Error shown when the AI response is blocked during generation.
                return "ERROR:" + _("The response was blocked mid-generation by safety filters.")
            # Translators: Generic error message when Gemini returns an empty response.
            return "ERROR:" + _("AI failed to provide a response. This might be due to safety filters or a temporary server issue.")

        req = _request_with_api_key(url, key, data=json.dumps(payload).encode('utf-8'), headers=headers)

        with GeminiHandler._get_opener(url).open(req, timeout=600) as r:
            res = json.loads(r.read().decode())
            candidates = res.get('candidates')
            if not candidates:
                if 'promptFeedback' in res and 'blockReason' in res['promptFeedback']:
                    return "ERROR:" + _("Blocked by AI Safety Filters: ") + res['promptFeedback']['blockReason']
                return "ERROR:" + _("AI failed to provide a response. This might be due to safety filters or a temporary server issue.")

            first_candidate = candidates[0]
            content = first_candidate.get('content', {})
            parts = content.get('parts', [])
            if not parts:
                if first_candidate.get('finishReason') == "SAFETY":
                    return "ERROR:" + _("The response was blocked mid-generation by safety filters.")
                # Translators: Error shown when the response structure is unexpected or empty.
                return "ERROR:" + _("AI returned an empty response structure.")
            return _extract_text_from_parts(parts)

    @staticmethod
    def _call_with_rotation(func_logic, *args, **kwargs):
        task = kwargs.pop('task', None)
        keys = GeminiHandler._get_api_keys(task=task)
        if not keys:
            # Translators: Error when no API keys are found in settings
            return "ERROR:" + _("No valid API key available or daily quota exhausted for all keys.")

        num_keys = len(keys)
        for i in range(num_keys):
            idx = (GeminiHandler._working_key_idx + i) % num_keys
            key = keys[idx]
            log.debug(f"Gemini rotation: trying key index {idx} (task={task})")
            key_start = time.time()
            try:
                res = GeminiHandler._call_with_retry(func_logic, key, *args)
                GeminiHandler._working_key_idx = idx
                log.debug(f"Gemini rotation: key index {idx} succeeded in {int((time.time() - key_start) * 1000)} ms")
                return res
            except error.HTTPError as e:
                err_msg = getattr(e, 'parsed_msg', GeminiHandler._handle_error(e))

                is_quota_or_server = (
                    err_msg in ["QUOTA_EXCEEDED", "SERVER_ERROR"] or
                    GeminiHandler.is_key_exhausted_error(err_msg) or
                    (hasattr(e, 'code') and e.code == 429) or
                    (hasattr(e, 'code') and e.code >= 500)
                )

                if is_quota_or_server:
                    log.warning(f"Gemini Key index {idx} failed with {err_msg}. Trying next...")
                    if i < num_keys - 1: continue

                    log.error(f"All Gemini API Keys failed. Last error: {err_msg}")
                    if hasattr(e, 'code') and e.code >= 500:
                        err_msg = _("Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
                        return "ERROR:" + err_msg
                    else:
                        # Translators: Error when all available API keys fail
                        return "ERROR:" + _("All API Keys failed (Quota/Server).")

                log.error(f"Gemini API Error with key {idx}: {err_msg}")
                return "ERROR:" + err_msg
            except Exception as e:
                log.error(f"Unexpected error in Gemini rotation with key {idx}: {e}", exc_info=True)
                return "ERROR:" + str(e)
        # Translators: Generic error message when an operation fails for an unknown reason.
        return "ERROR:" + _("Unknown error occurred.")

    @staticmethod
    def translate(text, target_lang):
        def _logic(key, txt, lang):
            from ..core import AIHandler
            p_active = nvda_config.conf["VisionAssistant"]["active_provider"]
            if p_active == "custom":
                base_url = AIHandler.get_base_url("custom")
                model = nvda_config.conf["VisionAssistant"]["custom_model_name"].strip()
            else:
                base_url = AIHandler.get_base_url("gemini")
                model = nvda_config.conf["VisionAssistant"]["model_name"]
            clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', base_url, flags=re.IGNORECASE)
            v_tag = "/v1beta"
            url = f"{clean_base}{v_tag}/models/{model}:generateContent"

            quick_template = get_prompt_text("translate_quick") or "Translate to {target_lang}. Output ONLY translation."
            quick_prompt = apply_prompt_template(quick_template, [("target_lang", lang)])
            payload = {"contents": [{"parts": [{"text": quick_prompt}, {"text": txt}]}]}

            _apply_gemma_thinking_patch(payload, model)

            req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with GeminiHandler._get_opener(url).open(req, timeout=90) as r:
                res = json.loads(r.read().decode())
                parts = res['candidates'][0]['content'].get('parts', [])
                return _extract_text_from_parts(parts)
        return GeminiHandler._call_with_rotation(_logic, text, target_lang)

    @staticmethod
    def ocr_page(image_bytes):
        def _logic(key, img_data):
            from ..core import AIHandler
            url = AIHandler.get_endpoint("ocr")
            full_url = url

            ocr_image_prompt = get_prompt_text("ocr_image_extract")
            payload = {"contents": [{"parts": [{"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(img_data).decode('utf-8')}}, {"text": ocr_image_prompt}]}]}

            _apply_gemma_thinking_patch(payload, url)

            req = _request_with_api_key(full_url, key, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
            with GeminiHandler._get_opener(full_url).open(req, timeout=120) as r:
                res = json.loads(r.read().decode())
                parts = res['candidates'][0]['content'].get('parts', [])
                return _extract_text_from_parts(parts)
        return GeminiHandler._call_with_rotation(_logic, image_bytes)

    @staticmethod
    def upload_and_process_batch(file_path, mime_type, page_count, prompt=None, page_range_text="", abort_checker=None):
        from ..core import AIHandler
        keys = GeminiHandler._get_api_keys(task="ocr")
        if not keys:
            # Translators: Error message for missing API Keys
            return [ "ERROR:" + _("No API Keys.") ]

        p_active = nvda_config.conf["VisionAssistant"]["active_provider"]
        upload_support = True
        if p_active == "custom":
            upload_support = nvda_config.conf["VisionAssistant"].get("custom_upload_support", False)

        model = AIHandler.get_endpoint("ocr").split('/')[-1].split(':')[0]

        if not upload_support:
            try:
                import fitz
                parts = []
                doc = fitz.open(file_path)
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_data = base64.b64encode(pix.tobytes("jpg")).decode('utf-8')
                    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": img_data}})
                doc.close()
                if not prompt:
                    prompt = apply_prompt_template(get_prompt_text("ocr_document_extract"), [("response_lang", nvda_config.conf["VisionAssistant"]["ai_response_language"])])
                parts.append({"text": prompt})
                res_text = GeminiHandler._call_with_rotation(GeminiHandler._logic, [{"parts": parts}], None, False, "ocr", task="ocr")
                if error_contract.is_ai_error(res_text): return [res_text]
                return res_text.split('[[[PAGE_SEP]]]')
            except Exception as e:
                return ["ERROR:" + str(e)]

        upload_url_base = AIHandler.get_endpoint("upload")
        opener = GeminiHandler._get_opener(upload_url_base)

        num_keys = len(keys)
        for i in range(num_keys):
            if abort_checker and abort_checker(): return ["ERROR: Aborted"]

            idx = (GeminiHandler._working_key_idx + i) % num_keys
            key = keys[idx]
            try:
                def local_report(msg):
                    if plugin_state.plugin_instance:
                        plugin_state.plugin_instance.report_status(msg)
                    else:
                        core.callLater(0, ui.message, msg)

                uri, _dur = GeminiHandler._upload_file_common(file_path, mime_type, key, report_callback=local_report, abort_checker=abort_checker)

                if not uri:
                    if i < num_keys - 1:
                        if plugin_state.plugin_instance:
                            # Translators: Message reported when an upload fails and the system automatically switches to the next available API key.
                            msg = _("Upload failed. Rotating key...")
                            plugin_state.plugin_instance.report_status(msg)
                        continue
                    # Translators: Error message for upload failure
                    return [ "ERROR:" + _("Upload failed.") ]

                if not prompt:
                    prompt = apply_prompt_template(get_prompt_text("ocr_document_extract"), [("response_lang", nvda_config.conf["VisionAssistant"]["ai_response_language"])])
                attachments = [{'mime_type': mime_type, 'file_uri': uri}]

                if plugin_state.plugin_instance and page_range_text:
                    rng = page_range_text.split("-", 1)
                    if len(rng) == 2:
                        process_msg = _("Processing pages {start} to {end}...").format(start=rng[0], end=rng[1])
                        plugin_state.plugin_instance.report_status(process_msg)

                for gen_attempt in range(10):
                    res = GeminiHandler._call_with_key(GeminiHandler._logic, key, prompt, attachments, False, "ocr", max_retries=1)

                    if res and not error_contract.is_ai_error(res):
                        GeminiHandler._working_key_idx = idx
                        return res.split('[[[PAGE_SEP]]]')

                    err_msg = error_contract.ai_error_message(res) if error_contract.is_ai_error(res) else "Unknown Error"
                    err_msg_lower = err_msg.lower()

                    is_fatal_error = error_contract.is_daily_quota_error(err_msg_lower)

                    if is_fatal_error:
                        GeminiHandler._ban_key(key, model=model)
                        if i < num_keys - 1:
                            break
                        return [res]

                    if error_contract.is_hard_error(err_msg_lower):
                        return [res]

                    delay_sec = 0
                    match = re.search(r"retry in ([\d\.]+)s", err_msg_lower)
                    if match:
                        try: delay_sec = float(match.group(1))
                        except Exception as e: log.debug(f"Retry delay parse failed: {e}")

                    if delay_sec > 0:
                        if plugin_state.plugin_instance:
                            # Translators: Message shown when an API rate limit is reached. {sec} is the number of seconds to wait.
                            retry_msg = _("Rate limit reached. Waiting {sec}s before retry...").format(sec=int(delay_sec))
                            plugin_state.plugin_instance.report_status(retry_msg)
                        for step in range(int(delay_sec * 2) + 2):
                            if abort_checker and abort_checker(): return ["ERROR: Aborted"]
                            time.sleep(0.5)
                        continue

                    if gen_attempt < 9:
                        if plugin_state.plugin_instance:
                            if page_range_text:
                                # Translators: Status message indicating an API request retry due to a temporary error for specific pages. {error} is replaced with details, {range} is the page range, {current} and {total} are attempts.
                                retry_msg = _("Temporary error ({error}). Retrying API request for pages {range} (Attempt {current}/{total})...").format(error=err_msg, range=page_range_text, current=gen_attempt + 2, total=10)
                            else:
                                retry_msg = _("Temporary error ({error}). Retrying on current key (Attempt {current}/{total})...").format(error=err_msg, current=gen_attempt + 2, total=10)
                            plugin_state.plugin_instance.report_status(retry_msg)
                        time_limit_sleep = 5.0 * (gen_attempt + 1)
                        for step in range(int(time_limit_sleep * 2)):
                            if abort_checker and abort_checker(): return ["ERROR: Aborted"]
                            time.sleep(0.5)
                else:
                    if i == num_keys - 1:
                        return [res] if res else ["ERROR:" + _("All keys failed.")]
                    if error_contract.is_server_busy_error(err_msg_lower):
                        return [res] if res else ["ERROR:" + _("All keys failed.")]

            except Exception as e:
                if abort_checker and abort_checker():
                    return ["ERROR: Aborted"]
                log.error(f"Error in upload_and_process_batch with key index {idx}: {e}", exc_info=True)
                if i == num_keys - 1:
                    return ["ERROR:" + str(e)]

            if i < num_keys - 1:
                if plugin_state.plugin_instance:
                    # Translators: Message reported when API quota is exhausted and the system rotates key.
                    msg = _("Daily quota exhausted or retries failed. Rotating key and re-uploading...")
                    plugin_state.plugin_instance.report_status(msg)

        return ["ERROR:" + _("All keys failed.")]

    @staticmethod
    def chat(history, new_msg, file_uri, mime_type, file_data=None):
        def _logic(key, hist, msg, uri, mime, f_data):
            from ..core import AIHandler
            url = AIHandler.get_endpoint("chat")
            full_url = url

            contents = list(hist)
            user_parts = []
            if uri:
                user_parts.append({"fileData": {"mimeType": mime, "fileUri": uri}})
            elif f_data:
                user_parts.append({"inlineData": {"mimeType": mime, "data": f_data}})
            user_parts.append({"text": msg})
            contents.append({"role": "user", "parts": user_parts})

            payload = {"contents": contents}
            _apply_gemma_thinking_patch(payload, url)

            req = _request_with_api_key(full_url, key, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
            with GeminiHandler._get_opener().open(req, timeout=120) as r:
                res = json.loads(r.read().decode())
                parts = res['candidates'][0]['content'].get('parts', [])
                return _extract_text_from_parts(parts)
        forced_key = GeminiHandler._get_registered_key(file_uri) if file_uri else None
        if forced_key:
            return GeminiHandler._call_with_key(_logic, forced_key, history, new_msg, file_uri, mime_type, file_data)
        return GeminiHandler._call_with_rotation(_logic, history, new_msg, file_uri, mime_type, file_data)

    @staticmethod
    def upload_for_chat(file_path, mime_type):
        p_active = nvda_config.conf["VisionAssistant"]["active_provider"]
        if p_active == "custom" and not nvda_config.conf["VisionAssistant"].get("custom_upload_support", False):
            return None

        keys = GeminiHandler._get_api_keys(task="chat")
        if not keys: return "ERROR:" + _("No valid API key available or daily quota exhausted for all keys.")

        for key in keys:
            try:
                uri, _dur = GeminiHandler._upload_file_common(file_path, mime_type, key)
                if uri:
                    return uri
            except Exception:
                continue
        return None

    @staticmethod
    def generate_speech(text, voice_name):
        def _logic(key, txt, voice):
            from ..core import AIHandler
            p_active = nvda_config.conf["VisionAssistant"]["active_provider"]
            if p_active == "custom":
                main_model = nvda_config.conf["VisionAssistant"]["custom_model_name"].strip()
                adv_tts = nvda_config.conf["VisionAssistant"].get("custom_tts_model", "").strip()
            else:
                main_model = nvda_config.conf["VisionAssistant"]["model_name"]
                adv_tts = nvda_config.conf["VisionAssistant"].get("gemini_tts_model", "").strip()
            if nvda_config.conf["VisionAssistant"].get("advanced_model_routing", False) and adv_tts:
                tts_model = adv_tts
            else:
                if p_active == "custom":
                    tts_model = main_model
                else:
                    if "pro" in main_model.lower():
                        tts_model = "gemini-2.5-pro-preview-tts"
                    else:
                        tts_model = "gemini-3.1-flash-tts-preview"

            if p_active == "custom":
                base_url = AIHandler.get_base_url("custom")
            else:
                proxy_url = nvda_config.conf["VisionAssistant"]["proxy_url"].strip()
                base_url = proxy_url.rstrip('/') if proxy_url else vision_config.DEFAULT_API_URLS["gemini"]

            clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', base_url, flags=re.IGNORECASE)
            v_tag = "/v1beta"
            url = f"{clean_base}{v_tag}/models/{tts_model}:generateContent"

            payload = {
                "contents": [{"parts": [{"text": txt}]}],
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}
                }
            }
            req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with GeminiHandler._get_opener(url).open(req, timeout=600) as r:
                raw_resp = r.read().decode()
                try:
                    res = json.loads(raw_resp)
                except Exception:
                    raise Exception(f"Server returned non-JSON response: {raw_resp[:100]}")
                candidates = res.get('candidates', [])
                if not candidates: raise Exception("No candidates returned")
                content = candidates[0].get('content', {})
                parts = content.get('parts', [])
                if not parts: raise Exception("No parts in response")
                part = parts[0]
                if 'inlineData' in part: return part['inlineData']['data']
                if 'text' in part: raise Exception(f"Model refused audio: {part['text']}")
                raise Exception("Unknown response format")
        return GeminiHandler._call_with_rotation(_logic, text, voice_name, task="tts")

    @staticmethod
    def _upload_video_with_key(file_path, key, abort_checker=None):
        try:
            uri, _dur = GeminiHandler._upload_file_common(file_path, "video/mp4", key, abort_checker=abort_checker)
            return uri
        except Exception as e:
            if abort_checker and abort_checker():
                log.debug("Gemini video upload aborted by user")
                return None
            err_msg = GeminiHandler._handle_error(e) if isinstance(e, error.HTTPError) else str(e)
            log.error(f"Gemini video upload error: {err_msg}")
            return None

    @staticmethod
    def upload_and_get_duration(file_path, report_callback=None, abort_checker=None):
        keys = GeminiHandler._get_api_keys(task="video")
        num_keys = len(keys)
        for i in range(num_keys):
            if abort_checker and abort_checker(): return None, None, None
            idx = (GeminiHandler._working_key_idx + i) % num_keys
            key = keys[idx]
            if report_callback:
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                # Translators: Status message indicating video upload progress with file size in MB.
                report_callback(_("Uploading to AI ({size:.1f} MB)...").format(size=file_size_mb))

            uri = GeminiHandler._upload_video_with_key(file_path, key, abort_checker)
            if uri:
                dur = GeminiHandler._file_durations.get(uri)
                GeminiHandler._working_key_idx = idx
                return uri, dur, key
        return None, None, None

    @staticmethod
    def process_video_task(file_path, prompt, start_offset_sec=None, end_offset_sec=None, json_mode=False, report_callback=None, abort_checker=None, current_uri=None, current_key=None, is_direct=False, validator=None):
        keys = GeminiHandler._get_api_keys(task="video")
        num_keys = len(keys)

        if current_key in keys:
            GeminiHandler._working_key_idx = keys.index(current_key)

        keys_exhausted = 0

        while keys_exhausted < num_keys:
            if abort_checker and abort_checker(): return None, None, None

            idx = GeminiHandler._working_key_idx % num_keys
            key = keys[idx]

            if not is_direct and key != current_key:
                current_uri = None

            try:
                if not current_uri and file_path and not is_direct:
                    if report_callback:
                        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                        # Translators: Status message indicating video upload progress with file size in MB and retry attempt numbers.
                        report_callback(_("Uploading to AI ({size:.1f} MB) (Key {current}/{total})...").format(size=file_size_mb, current=idx+1, total=num_keys))

                    current_uri = GeminiHandler._upload_video_with_key(file_path, key, abort_checker)
                    if not current_uri:
                        if report_callback:
                            # Translators: Message reported when a file upload fails and the system is retrying.
                            report_callback(_("Upload failed. Retrying..."))
                        time.sleep(2.0)
                        keys_exhausted += 1
                        GeminiHandler._working_key_idx = (GeminiHandler._working_key_idx + 1) % num_keys
                        continue
                    current_key = key
                elif is_direct and not current_uri:
                    current_uri = file_path
                    current_key = key

                if not current_uri:
                    keys_exhausted += 1
                    GeminiHandler._working_key_idx = (GeminiHandler._working_key_idx + 1) % num_keys
                    continue

                attachments = [{'mime_type': 'video/mp4', 'file_uri': current_uri}]
                if start_offset_sec is not None and end_offset_sec is not None and end_offset_sec != -1:
                    attachments[0]['video_metadata'] = {
                        "start_offset": f"{int(start_offset_sec)}s",
                        "end_offset": f"{int(end_offset_sec)}s"
                    }

                res = None
                for attempt in range(10):
                    if abort_checker and abort_checker(): return None, None, None

                    res = GeminiHandler._call_with_key(GeminiHandler._logic, key, prompt, attachments, json_mode, "video", max_retries=1)

                    if res and not error_contract.is_ai_error(res):
                        if validator and not validator(res):
                            # Translators: Error shown internally when AI stops early
                            res = "ERROR:" + _("Incomplete description. AI stopped early.")
                        else:
                            return res, current_uri, current_key

                    err_msg = error_contract.ai_error_message(res) if res and error_contract.is_ai_error(res) else "Unknown Error"
                    err_msg_lower = err_msg.lower()

                    is_fatal_error = error_contract.is_daily_quota_error(err_msg_lower)

                    if is_fatal_error:
                        break

                    if error_contract.is_file_access_error(err_msg_lower):
                        if report_callback:
                            # Translators: Status message when an uploaded file is no longer accessible and the video is being re-uploaded with another key.
                            report_callback(_("Uploaded file is no longer accessible. Re-uploading with the next key..."))
                        break

                    if error_contract.is_hard_error(err_msg_lower):
                        return res, current_uri, current_key

                    delay_sec = 0
                    match = re.search(r"retry in ([\d\.]+)s", err_msg_lower)
                    if match:
                        try: delay_sec = float(match.group(1))
                        except Exception as e: log.debug(f"Retry delay parse failed: {e}")

                    if delay_sec > 0:
                        if report_callback:
                            report_callback(_("Rate limit reached. Waiting {sec}s before retry...").format(sec=int(delay_sec)))
                        for step in range(int(delay_sec * 2) + 2):
                            if abort_checker and abort_checker(): return None, None, None
                            time.sleep(0.5)
                        continue

                    if report_callback:
                        # Translators: Status message indicating an API request retry due to a temporary error. {error} is replaced with details, {current} and {total} are attempts.
                        report_callback(_("Temporary error ({error}). Retrying on current key (Attempt {current}/{total})...").format(error=err_msg, current=attempt+1, total=10))

                    time_limit_sleep = 5.0 * (attempt + 1)
                    for step in range(int(time_limit_sleep * 2)):
                        if abort_checker and abort_checker(): return None, None, None
                        time.sleep(0.5)

                if res and not error_contract.is_ai_error(res):
                    return res, current_uri, current_key

                keys_exhausted += 1
                if keys_exhausted < num_keys:
                    GeminiHandler._working_key_idx = (GeminiHandler._working_key_idx + 1) % num_keys
                    if report_callback:
                        report_callback(_("Daily quota exhausted or retries failed. Rotating key and re-uploading..."))
                else:
                    if report_callback:
                        # Translators: Message reported when all available API keys have reached their usage limits.
                        report_callback(_("All API keys exhausted or server unavailable."))
                    break

            except Exception as e:
                log.error(f"Error under key {idx}: {e}")
                keys_exhausted += 1
                GeminiHandler._working_key_idx = (GeminiHandler._working_key_idx + 1) % num_keys
                continue

        # Translators: Error message shown when all API keys run out of quota or fail.
        return "ERROR:" + _("All API keys failed or daily quota exhausted."), None, None
