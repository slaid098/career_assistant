from __future__ import annotations

import contextvars
import logging
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from loguru import logger as loguru_logger

from .formatters import ExternalLogFormatter
from .handlers import (
    ConsoleHandler,
    FileHandler,
    TelegramHandler,
    WebSocketHandler,
    WebSocketHandlerManager,
)
from .tools import get_dynamic_func_path, get_emoji_by_level

if TYPE_CHECKING:
    from collections.abc import Generator

    from .config import LoggerConfig
    from .types import LogHandler, LogLevel

_author_context: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "author_context",
    default=None,
)
_details_context: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "details_context",
    default=None,
)


class NotifyLogger:
    """
    Logger with notification capabilities, simplified with loguru filters.
    """

    def __init__(self) -> None:
        self.name = self.__class__.__name__
        self.formatter = ExternalLogFormatter()
        self._original = loguru_logger

        self._remove_loguru_logger()
        self._init_default_handler()

    def setup(
        self,
        handlers: list[LogHandler],
        level: LogLevel = "INFO",
    ) -> None:
        """
        Configures the logger with a list of handlers and a global level.

        Args:
            handlers: A list of configured LogHandler instances.
            level: The minimum log level for the logger.
        """
        # Sync Python's standard logging
        std_level = getattr(logging, level, logging.INFO)
        logging.basicConfig(level=std_level, force=True)
        logging.root.setLevel(std_level)

        self._remove_loguru_logger()

        # Always add a default console handler
        ConsoleHandler(level=level).add()

        for handler in handlers:
            handler.add()

        self._set_global_emoji_for_levels()

    def _remove_loguru_logger(self) -> None:
        self.original.remove()

    def _init_default_handler(self, level: LogLevel = "DEBUG") -> None:
        ConsoleHandler(level).add()

    def _set_global_emoji_for_levels(self) -> None:
        """Sets a global icon for each log level in loguru."""
        log_levels: list[LogLevel] = [
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ]
        for level_name in log_levels:
            self.original.level(
                level_name,
                icon=get_emoji_by_level(level_name),
            )

    @contextmanager
    def contextualize(
        self,
        author: str,
        details: str | None = None,
    ) -> Generator[Any, None, None]:
        author_token = _author_context.set(author)
        details_token = _details_context.set(details)
        try:
            yield self
        finally:
            _author_context.reset(author_token)
            _details_context.reset(details_token)

    async def shutdown_websocket(self) -> None:
        """Correctly shuts down the WebSocket handler."""
        manager = WebSocketHandlerManager()
        await manager.stop()

    def _log(  # noqa: PLR0913
        self,
        level: LogLevel,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        """
        Internal logging function that binds the 'notify' flag to the record.

        Args:
            level: The log level.
            message: The log message.
            exception: An optional exception to log.
            author: The author of the log.
            details: Additional details for the log.
            notify: If True, the Telegram handler will be triggered.
        """
        author = author or _author_context.get()
        details = details or _details_context.get()

        func_path = get_dynamic_func_path()
        formatted_message = self.formatter.format_message(
            message=message,
            func_path=func_path,
            exception=exception,
            author=author,
            details=details,
        )

        # Bind the notify flag to the log record's "extra" dict
        bound_logger = self.original.bind(notify=notify)
        bound_logger.opt(exception=exception, lazy=True).log(
            level,
            formatted_message,
        )

    # --- High-level logging methods ---
    def debug(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self._log(
            "DEBUG",
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def success(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self._log(
            "SUCCESS",
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def info(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self._log(
            "INFO",
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def warning(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self._log(
            "WARNING",
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def error(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self._log(
            "ERROR",
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def critical(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self._log(
            "CRITICAL",
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    # --- Short alias methods ---
    def d(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self.debug(
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def s(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self.success(
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def i(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self.info(
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def w(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self.warning(
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def e(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self.error(
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    def c(
        self,
        message: Any,
        exception: Exception | None = None,
        author: str | None = None,
        details: str | None = None,
        *,
        notify: bool = True,
    ) -> None:
        self.critical(
            message,
            exception=exception,
            author=author,
            details=details,
            notify=notify,
        )

    @property
    def original(self):  # noqa: ANN201
        """Provides access to the original loguru logger instance."""
        return self._original


def create_handlers_from_config(config: LoggerConfig) -> list[LogHandler]:
    """
    Creates a list of log handlers based on the provided configuration.

    This factory function encapsulates the logic for building handlers,
    making the logger setup more modular and testable.

    Args:
        config: The logger configuration object.

    Returns:
        A list of configured LogHandler instances.
    """
    handlers: list[LogHandler] = []

    if config.use_file_handler:
        handlers.append(FileHandler(config.file_handler))

    if config.use_telegram_handler and config.telegram_handler:
        handlers.append(TelegramHandler(config.telegram_handler))

    if config.use_websocket_handler and config.websocket_handler:
        manager = WebSocketHandlerManager()
        log_file_path = (
            str(config.file_handler.path) if config.use_file_handler else None
        )
        manager.configure(config.websocket_handler, log_file_path)
        handlers.append(WebSocketHandler(config.websocket_handler))

    return handlers


# Global logger instance (Singleton)
logger = NotifyLogger()
