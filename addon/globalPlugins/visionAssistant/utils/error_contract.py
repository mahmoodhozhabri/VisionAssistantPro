# -*- coding: utf-8 -*-

AI_ERROR_PREFIX = "ERROR:"

_KEY_EXHAUSTED_KEYWORDS = ("quota", "exhausted", "429")

_DAILY_QUOTA_KEYWORDS = (
	"daily",
	"per day",
	"per_day",
	"perday",
	"requestsperday",
	"quota_exceeded_daily",
)

_HARD_ERROR_KEYWORDS = ("400", "403", "bad request", "forbidden", "blocked")

_FILE_ACCESS_KEYWORDS = (
	"permission to access the file",
	"permission_denied",
	"permission denied",
	"may not exist",
	"file not found",
	"not found or has been deleted",
)

_REGION_ERROR_KEYWORDS = (
	"user location is not supported",
	"unsupported region",
	"region is not supported",
	"not available in your country",
	"not available in your region",
	"api not enabled for your location",
)

_SERVER_BUSY_KEYWORDS = (
	"high demand",
	"overloaded",
	"server error",
	"temporarily unavailable",
	"internal error",
	"server busy",
	"service is busy",
	"busy",
	"try again",
	"500",
	"502",
	"503",
	"504",
	"timed out",
	"timeout",
)


def is_daily_quota_error(err_msg):
	if not err_msg:
		return False
	err_lower = str(err_msg).lower()
	return any(x in err_lower for x in _DAILY_QUOTA_KEYWORDS)


def is_ai_error(res):
	return isinstance(res, str) and res.startswith(AI_ERROR_PREFIX)


def ai_error_message(res):
	return res[len(AI_ERROR_PREFIX) :] if is_ai_error(res) else res


def is_key_exhausted_error(err_msg):
	if not err_msg:
		return False
	err_lower = str(err_msg).lower()
	return any(x in err_lower for x in _KEY_EXHAUSTED_KEYWORDS)


def is_hard_error(err_msg):
	if not err_msg:
		return False
	err_lower = str(err_msg).lower()
	return any(x in err_lower for x in _HARD_ERROR_KEYWORDS)


def is_file_access_error(err_msg):
	if not err_msg:
		return False
	err_lower = str(err_msg).lower()
	return any(x in err_lower for x in _FILE_ACCESS_KEYWORDS)


def is_region_error(err_msg):
	if not err_msg:
		return False
	err_lower = str(err_msg).lower()
	return any(x in err_lower for x in _REGION_ERROR_KEYWORDS)


def is_server_busy_error(err_msg):
	if not err_msg:
		return False
	err_lower = str(err_msg).lower()
	return any(x in err_lower for x in _SERVER_BUSY_KEYWORDS)


def history_to_openai_messages(history):
	messages = []
	for h in history or []:
		role = "assistant" if h.get("role") == "model" else "user"
		text = h["parts"][0]["text"] if h.get("parts") else ""
		messages.append({"role": role, "content": text})
	return messages
