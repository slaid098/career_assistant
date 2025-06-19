import datetime
import inspect
from typing import Any

from .types import LogLevel, LogMessage


def get_emoji_by_level(level: LogLevel) -> str:
    return _get_emoji_mapping().get(level, "")


def _get_emoji_mapping() -> dict[LogLevel, str]:
    return {
        "DEBUG": "🔵",
        "INFO": "🟢",
        "SUCCESS": "🥳",
        "WARNING": "⚠️",
        "ERROR": "🚨",
        "CRITICAL": "🔥",
    }


def parse_log_message(message: str) -> LogMessage:
    """Парсит сообщение лога"""
    parts = message.split("|")
    level = parts[0].strip()
    date_str = datetime.datetime.now().isoformat()
    time_str = parts[1].strip() if len(parts) > 1 else date_str
    msg = " ".join(parts[2:]).strip() if len(parts) > 2 else message  # noqa: PLR2004

    log_message = {
        "level": level,
        "timestamp": time_str,
        "message": msg,
    }

    return _normalize_log_message(log_message)


def _normalize_log_message(raw_log_message: dict[str, Any]) -> LogMessage:
    """Проверяет сообщение лога"""
    if not hasattr(raw_log_message, "get") or not callable(
        getattr(raw_log_message, "get", None),
    ):
        raw_log_message = {"message": str(raw_log_message)}

    # Убедимся, что поле level всегда есть
    if "level" not in raw_log_message or raw_log_message["level"] is None:
        raw_log_message["level"] = "INFO"

        # Добавляем timestamp, если отсутствует
    if "timestamp" not in raw_log_message:
        raw_log_message["timestamp"] = datetime.datetime.now().isoformat()

    log_message: LogMessage = {
        "level": raw_log_message["level"],
        "timestamp": raw_log_message["timestamp"],
        "message": raw_log_message["message"],
    }
    return log_message


def get_dynamic_func_path() -> str:
    """Get caller info dynamically by skipping logger module frames."""
    frame = inspect.currentframe()
    if not frame or not frame.f_back:
        return ""
    caller = frame.f_back.f_back or frame.f_back
    filename = caller.f_code.co_filename
    func_name = caller.f_code.co_name
    line_no = caller.f_lineno
    return f"{filename}:{func_name}:{line_no}"
