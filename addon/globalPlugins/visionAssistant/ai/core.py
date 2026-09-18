# -*- coding: utf-8 -*-
import os
import json
import logging
import ssl
import re
import time
from urllib import request, error
from urllib.parse import urlparse

import config as nvda_config
import addonHandler

from .. import vision_config
from ..utils.error_contract import AI_ERROR_PREFIX, is_ai_error, ai_error_message, is_server_busy_error

log = logging.getLogger(__name__)

addonHandler.initTranslation()


def _apply_gemma_thinking_patch(payload, url_or_model):
    model_name = ""
    if url_or_model:
        if "/models/" in url_or_model:
            try:
                model_name = url_or_model.split("/models/")[-1].split(":")[0].split("?")[0]
            except Exception:
                pass
        else:
            model_name = url_or_model

    if model_name and ("gemma-4" in model_name.lower() or "gemma4" in model_name.lower()):
        if "generationConfig" not in payload:
            payload["generationConfig"] = {}
        payload["generationConfig"]["thinkingConfig"] = {"thinkingLevel": "MINIMAL"}
    return payload


def _extract_text_from_parts(parts):
    if not parts:
        return ""
    text_parts = [part.get("text", "") for part in parts if not part.get("thought")]
    if text_parts:
        return "".join(text_parts)
    return parts[0].get("text", "")


class AIHandler:
    @staticmethod
    def is_tts_supported(provider=None):
        p = provider if provider else nvda_config.conf["VisionAssistant"]["active_provider"]
        return p in ["gemini", "openai", "minimax", "custom"]

    @staticmethod
    def get_voices(provider):
        if provider == "minimax":
            return MinimaxHandler.get_voices()
        if provider == "gemini":
            return vision_config.GEMINI_VOICES
        if provider in ["openai", "custom"]:
            return vision_config.OPENAI_VOICES
        return []

    @staticmethod
    def filter_models(provider, models_info, task="main"):
        if task != "main":
            return models_info
        filtered = []
        for mid_orig, mname_orig in models_info:
            mid = mid_orig.lower()
            mname = mname_orig.lower()
            if provider == "gemini":
                excluded = ["nano", "banana", "robotic", "vo3", "v03", "veo", "tts", "native", "audio", "image", "aqa", "lyria", "embedding", "bison", "gecko", "deep", "antigravity", "computer", "live", "omni", "video", "customtools"]
                if any(x in mid or x in mname for x in excluded):
                    continue
            elif provider == "groq":
                excluded = ["whisper", "audio", "vision-preview", "embedding"]
                if any(x in mid or x in mname for x in excluded):
                    continue
            elif provider == "openai":
                excluded = ["whisper", "tts", "dall-e", "embedding", "moderation", "audio", "realtime", "babbage"]
                if any(x in mid or x in mname for x in excluded):
                    continue
            elif provider == "mistral":
                excluded = ["embed", "moderation"]
                if any(x in mid or x in mname for x in excluded):
                    continue
            filtered.append((mid_orig, mname_orig))
        return filtered

    @staticmethod
    def is_gemini():
        p = nvda_config.conf["VisionAssistant"]["active_provider"]
        if p == "gemini": return True
        if p == "custom":
            return nvda_config.conf["VisionAssistant"]["custom_api_type"] == "gemini"
        return False

    @staticmethod
    def get_base_url(provider):
        if provider == "custom":
            return nvda_config.conf["VisionAssistant"].get("custom_api_url", "").strip().rstrip('/')
        
        proxy_url = nvda_config.conf["VisionAssistant"]["proxy_url"].strip()
        
        if proxy_url:
            if not (proxy_url.startswith("http://") or proxy_url.startswith("https://")):
                proxy_url = "http://" + proxy_url
            try:
                parsed = urlparse(proxy_url)
                if parsed.hostname in ["127.0.0.1", "localhost"] or parsed.username:
                    proxy_url = ""
                else:
                    netloc = parsed.hostname
                    if parsed.port: netloc += f":{parsed.port}"
                    proxy_url = f"{parsed.scheme}://{netloc}"
            except Exception as e:
                log.warning(f"Proxy url parsing failed: {e}")

        if provider == "gemini":
            return proxy_url.rstrip('/') if proxy_url else vision_config.DEFAULT_API_URLS["gemini"]
        elif provider == "openai":
            return proxy_url.rstrip('/') if proxy_url else "https://api.openai.com"
        elif provider == "mistral":
            return proxy_url.rstrip('/') if proxy_url else "https://api.mistral.ai"
        elif provider == "groq":
            return proxy_url.rstrip('/') if proxy_url else "https://api.groq.com/openai"
        elif provider == "minimax":
            return proxy_url.rstrip('/') if proxy_url else nvda_config.conf["VisionAssistant"].get("minimax_api_host", "https://api.minimax.io/v1").strip() or "https://api.minimax.io/v1"
        return ""

    @staticmethod
    def get_endpoint(task_type, model_override=None):
        p = nvda_config.conf["VisionAssistant"]["active_provider"]
        adv = nvda_config.conf["VisionAssistant"]["use_advanced_endpoints"]
        base = AIHandler.get_base_url(p)
        
        model = model_override or ""
        if not model:
            if p == "custom":
                target_model_map = {
                    "vision": "custom_ocr_model",
                    "ocr": "custom_ocr_model",
                    "stt": "custom_stt_model",
                    "tts": "custom_tts_model",
                    "operator": "custom_operator_model",
                    "video": "custom_video_model"
                }
                if task_type in target_model_map:
                    model = nvda_config.conf["VisionAssistant"].get(target_model_map[task_type], "").strip()
                
                if not model:
                    model = nvda_config.conf["VisionAssistant"]["custom_model_name"].strip()
            
            if not model and nvda_config.conf["VisionAssistant"].get("advanced_model_routing", False):
                model = nvda_config.conf["VisionAssistant"].get(f"{p}_{task_type}_model", "").strip()
            
            if not model:
                m_key = "model_name" if p == "gemini" else f"{p}_model_name"
                model = nvda_config.conf["VisionAssistant"].get(m_key, "")

        if task_type == "tts" and AIHandler.is_gemini() and "gemini" in model.lower():
            if "pro" in model.lower(): model = "gemini-2.5-pro-preview-tts"
            else: model = "gemini-3.1-flash-tts-preview"

        if not base:
            base_map = vision_config.DEFAULT_API_URLS
            base = base_map.get(p, "")
            
        if p == "custom" and adv:
            target_map = {"models": "custom_models_url", "vision": "custom_ocr_url", "ocr": "custom_ocr_url", "stt": "custom_stt_url", "tts": "custom_tts_url", "operator": "custom_operator_url"}
            target_key = target_map.get(task_type)
            if target_key:
                target = nvda_config.conf["VisionAssistant"].get(target_key, "").strip()
                if target.lower().startswith("http"): return target

        base = base.rstrip('/')
        if AIHandler.is_gemini():
            if ":generateContent" in base: return base
            clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', base, flags=re.IGNORECASE)
            v_tag = "/v1beta"
            if task_type == "models": return f"{clean_base}{v_tag}/models"
            if task_type == "upload":
                return f"{clean_base}/upload{v_tag}/files"
            return f"{clean_base}{v_tag}/models/{model}:generateContent"
            
        v1_base = base if "/v1" in base.lower() else f"{base}/v1"
        if task_type == "models": return f"{v1_base}/models"
        if task_type in ["chat", "vision", "ocr", "operator"]: return f"{v1_base}/chat/completions"
        if task_type == "upload": return f"{v1_base}/files"
        if task_type == "stt": return f"{v1_base}/audio/transcriptions"
        if task_type == "tts": return f"{v1_base}/audio/speech"
        return v1_base

    @staticmethod
    def get_keys(provider):
        from ..utils.secure_credentials import get_credential
        if provider == "gemini": key_name = "api_key"
        elif provider == "custom": key_name = "custom_api_key"
        else: key_name = f"{provider}_api_key"
        raw = get_credential(nvda_config.conf["VisionAssistant"], key_name)
        return [k.strip() for k in str(raw).replace('\r\n', ',').replace('\n', ',').split(',') if k.strip()]

    @staticmethod
    def get_models(task="main"):
        p = nvda_config.conf["VisionAssistant"]["active_provider"]
        keys = AIHandler.get_keys(p)
        key = keys[0] if keys else ""
        
        custom_type = nvda_config.conf["VisionAssistant"].get("custom_api_type", "openai")
        is_gemini_logic = (p == "gemini" or (p == "custom" and custom_type == "gemini"))
        
        url = AIHandler.get_endpoint("models")
        
        if not url:
            return []
            
        if is_gemini_logic:
            url += ("&" if "?" in url else "?") + "pageSize=1000"
        # Native Gemini authorization keys must be sent in the documented
        # x-goog-api-key header. Keep query authentication for third-party
        # Gemini-compatible custom endpoints for backwards compatibility.
        if p == "custom" and is_gemini_logic and key and "key=" not in url:
            url += ("&" if "?" in url else "?") + f"key={key}"
            
        try:
            ssl_context = ssl.create_default_context()
            from ..utils.media_capture import get_proxy_opener
            proxy_opener = get_proxy_opener(url)
            proxy_opener.add_handler(request.HTTPSHandler(context=ssl_context))
            
            req = request.Request(url, method="GET")
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            req.add_header("Accept", "application/json")

            if p == "gemini" and key:
                req.add_header("x-goog-api-key", key)
            elif not is_gemini_logic and key:
                req.add_header("Authorization", f"Bearer {key}")
                
            with proxy_opener.open(req, timeout=15) as r:
                res_body = r.read().decode('utf-8')
                data = json.loads(res_body)
                models_info = []

                if "data" in data and isinstance(data["data"], list):
                    for m in data["data"]:
                        m_id = m.get("id")
                        if m_id: models_info.append((m_id, m_id))
                elif "models" in data and isinstance(data["models"], list):
                    for m in data["models"]:
                        full_name = m.get("name", "")
                        m_id = full_name.split("/")[-1] if "/" in full_name else full_name
                        if m_id: models_info.append((m_id, m.get("displayName", m_id)))
                elif isinstance(data, list):
                    for m in data:
                        m_id = m.get("id") or m.get("name")
                        if m_id: models_info.append((m_id, m_id))

                return AIHandler.filter_models(p, models_info, task=task)
        except error.HTTPError as e:
            try:
                raw_err = e.read().decode('utf-8')
                err_json = json.loads(raw_err)
                err_val = err_json.get("error")
                if isinstance(err_val, dict):
                    server_msg = err_val.get("message")
                else:
                    server_msg = err_val or err_json.get("message")
                if server_msg:
                    log.error(f"Fetch models failed for {p}: {server_msg}")
                    return []
            except Exception as ex:
                log.warning(f"Fetch models JSON error parsing: {ex}")
            log.error(f"Fetch models failed for {p}: {e}")
            return []
        except Exception as e:
            log.error(f"Fetch models failed for {p}: {e}")
            return []

    @staticmethod
    def call(prompt, attachments=None, json_mode=False, task="chat"):
        p_name = nvda_config.conf["VisionAssistant"]["active_provider"]
        endpoint = AIHandler.get_endpoint(task)
        att_count = len(attachments) if attachments else 0
        start_time = time.time()
        log.info(f"AI call started: provider={p_name}, task={task}, endpoint={endpoint}, prompt_len={len(prompt or '')}, attachments={att_count}")
        log.debug(f"AI call PROMPT:\n{prompt}")

        if AIHandler.is_gemini():
            forced_key = None
            if attachments:
                for att in attachments:
                    if isinstance(att, dict) and 'file_uri' in att:
                        forced_key = GeminiHandler._get_registered_key(att['file_uri'])
                        if forced_key:
                            break
            if forced_key:
                res = GeminiHandler._call_with_key(GeminiHandler._logic, forced_key, prompt, attachments, json_mode, task)
            else:
                res = GeminiHandler._call_with_rotation(GeminiHandler._logic, prompt, attachments, json_mode, task, task=task)
        else:
            res = OpenAIHandler.call(prompt, attachments, json_mode, task)

        elapsed_ms = int((time.time() - start_time) * 1000)
        if is_ai_error(res):
            log.warning(f"AI call error ({elapsed_ms} ms): {res}")
        else:
            log.info(f"AI call finished: {len(res) if res else 0} chars, {elapsed_ms} ms")
            log.debug(f"AI call RESPONSE:\n{res}")
        return res

    @staticmethod
    def ocr(img_or_pdf_base64, mime_type="image/jpeg"):
        p = nvda_config.conf["VisionAssistant"]["active_provider"]
        if p == "mistral":
            return MistralHandler.ocr(img_or_pdf_base64, mime_type)
        return AIHandler.call(vision_config.get_prompt_text("ocr_image_extract"), attachments=[{'mime_type': mime_type, 'data': img_or_pdf_base64}], task="ocr")

    @staticmethod
    def _transcribe_helper(key, audio_att, url, model_name):
        return OpenAIHandler._transcribe_helper(key, audio_att, url, model_name)

    @staticmethod
    def generate_speech(text, voice_name, model_override=None):
        if not AIHandler.is_tts_supported():
            # Translators: Error message when TTS is not supported by the provider
            return "ERROR:" + _("TTS is not supported by this provider."), False
            
        p = nvda_config.conf["VisionAssistant"]["active_provider"]
        if AIHandler.is_gemini(): 
            return GeminiHandler.generate_speech(text, voice_name), True
        if p == "minimax":
            return MinimaxHandler.generate_speech(text, voice_name, model_override)
        return OpenAIHandler.generate_speech(text, voice_name, model_override)

    @staticmethod
    def upload_to_mistral_for_chat(file_path):
        return MistralHandler.upload_to_mistral_for_chat(file_path)

    @staticmethod
    def delete_mistral_file(file_id):
        return MistralHandler.delete_mistral_file(file_id)


from .providers.gemini import GeminiHandler
from .providers.openai import OpenAIHandler
from .providers.mistral import MistralHandler
from .providers.minimax import MinimaxHandler
