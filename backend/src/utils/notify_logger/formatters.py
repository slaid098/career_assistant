from typing import Any

from .tools import get_emoji_by_level
from .types import LogLevel


class InternalLogFormatter:
    @property
    def console_format(self) -> str:
        time_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
        message_format = "<level>{message}</level>"

        return f"{time_format} | {message_format}"

    @property
    def file_format(self) -> str:
        return "{level} | {time:YYYY-MM-DD HH:mm:ss.SSS} | - {message}"

    @property
    def telegram_format(self) -> str:
        return "{level.icon} {level.name}|{message}"

    @property
    def websocket_format(self) -> str:
        """Формат для WebSocket логов"""
        return self.file_format

class ExternalLogFormatter:
    def format_message(
        self,
        message: Any,
        func_path: str,
        exception: Exception | None,
        author: str | None,
        details: str | None,
    ) -> str:
        author = f" [{author}]:" if author else ""
        details = f"| {details}" if details else ""

        if exception:
            ex_name = exception.__class__.__name__
            ex = exception
            formatted_msg = f"{func_path} -{author} {ex_name}:{ex} | {message} {details}"
        else:
            formatted_msg = f"{func_path}{author} - {message} {details}"

        return formatted_msg.strip()

    def add_emoji(self, level: LogLevel, message: str) -> str:
        emoji = get_emoji_by_level(level)
        return f"{emoji} {message}"

