# -*- coding: utf-8 -*-
import os
import sys
import logging
import threading
import globalVars
import config as nvda_config

from .secure_credentials import CREDENTIAL_FIELDS, credential_redaction_values, is_protected, redact_text

_LOG_DIR = os.path.join(globalVars.appArgs.configPath, "VisionAssistant", "logs")
_LOG_FILE = os.path.join(_LOG_DIR, "vision_assistant.log")

_file_handler = None
_logger_initialized = False


def _configured_secrets():
    secrets = []
    try:
        configuration = nvda_config.conf["VisionAssistant"]
        for field in CREDENTIAL_FIELDS:
            value = str(configuration.get(field, "") or "")
            if is_protected(value):
                try:
                    secrets.extend(credential_redaction_values(value))
                except Exception:
                    # Even when DPAPI recovery fails, do not expose its protected
                    # envelope through a configuration or exception dump.
                    secrets.append(value)
    except Exception:
        pass
    return secrets


class RedactingFormatter(logging.Formatter):
    def format(self, record):
        rendered = super().format(record)
        return redact_text(rendered, _configured_secrets())

    def formatException(self, exc_info):
        rendered = super().formatException(exc_info)
        return redact_text(rendered, _configured_secrets())


def get_log_file_path():
    return _LOG_FILE


def get_log_dir_path():
    return _LOG_DIR


def cleanup_old_logs(hours=None):
    if hours is None:
        try:
            hours = int(nvda_config.conf["VisionAssistant"].get("log_retention_hours", 168))
        except Exception:
            hours = 168
    if hours <= 0:
        return

    path = get_log_file_path()
    if not os.path.exists(path):
        return

    try:
        import time
        import datetime
        now = time.time()
        cutoff_sec = now - (hours * 3600)

        if os.path.getsize(path) > 0:
            new_lines = []
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

            keep = False
            for line in lines:
                if len(line) >= 19 and line[4] == "-" and line[7] == "-":
                    try:
                        dt = datetime.datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
                        timestamp = dt.timestamp()
                        keep = timestamp >= cutoff_sec
                    except Exception:
                        keep = True
                if keep:
                    new_lines.append(line)

            if len(new_lines) < len(lines):
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
    except Exception as e:
        logging.getLogger(__name__).warning("Log cleanup failed: %s", e)


def setup_file_logging():
    global _file_handler
    try:
        enabled = nvda_config.conf["VisionAssistant"].get("enable_file_logging", False)
        level_str = nvda_config.conf["VisionAssistant"].get("log_level", "DEBUG").upper()
        level = getattr(logging, level_str, logging.DEBUG)
        target_logger = logging.getLogger("globalPlugins.visionAssistant")
        target_logger.setLevel(level)

        for name, logger_obj in list(logging.Logger.manager.loggerDict.items()):
            if name.startswith("globalPlugins.visionAssistant.") and isinstance(logger_obj, logging.Logger):
                logger_obj.setLevel(level)
                logger_obj.propagate = True

        for h in list(target_logger.handlers):
            if isinstance(h, logging.FileHandler):
                target_logger.removeHandler(h)
                try:
                    h.close()
                except Exception:
                    pass

        if _file_handler:
            try:
                _file_handler.close()
            except Exception:
                pass
            _file_handler = None

        if enabled:
            target_logger.propagate = False
            if not os.path.exists(_LOG_DIR):
                os.makedirs(_LOG_DIR, exist_ok=True)

            class ImmediateFlushHandler(logging.FileHandler):
                def emit(self, record):
                    super().emit(record)
                    self.flush()

            _file_handler = ImmediateFlushHandler(_LOG_FILE, mode="a", encoding="utf-8")
            formatter = RedactingFormatter(
                fmt="%(asctime)s [%(levelname)s] [%(name)s:%(threadName)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            _file_handler.setFormatter(formatter)
            _file_handler.setLevel(level)
            target_logger.addHandler(_file_handler)

            cleanup_old_logs()

            target_logger.info(
                "Vision Assistant dedicated logging initialized. Enabled=%s, Level=%s", enabled, level_str
            )
        else:
            target_logger.propagate = True
    except Exception as e:
        logging.getLogger(__name__).warning("Failed to setup file logging: %s", e)


def open_log_file():
    path = get_log_file_path()
    if not os.path.exists(path):
        if not os.path.exists(_LOG_DIR):
            os.makedirs(_LOG_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("--- Vision Assistant Log File Created ---\n")
    try:
        os.startfile(path)
    except Exception as e:
        logging.getLogger("globalPlugins.visionAssistant").error("Failed to open log file: %s", e, exc_info=True)


def open_log_folder():
    d = get_log_dir_path()
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    try:
        os.startfile(d)
    except Exception as e:
        logging.getLogger("globalPlugins.visionAssistant").error("Failed to open log folder: %s", e, exc_info=True)


def clear_log_file():
    global _file_handler
    target_logger = logging.getLogger("globalPlugins.visionAssistant")
    if _file_handler:
        try:
            target_logger.removeHandler(_file_handler)
            _file_handler.close()
        except Exception:
            pass
        _file_handler = None

    path = get_log_file_path()
    try:
        if os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("--- Vision Assistant Log Cleared ---\n")
    except Exception as e:
        target_logger.error("Failed to clear log file: %s", e, exc_info=True)

    setup_file_logging()
