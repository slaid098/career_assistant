from __future__ import annotations

import asyncio
import logging
import sys
from typing import TYPE_CHECKING, Any

from loguru import logger

from .formatters import InternalLogFormatter
from .types import LogHandler, LogLevel, LogMessage
from .websocket_manager import WebSocketHandlerManager

if TYPE_CHECKING:
    from loguru import Message, Record

    from .config import (
        FileHandlerConfig,
        TelegramHandlerConfig,
        WebSocketHandlerConfig,
    )

TeleBot: Any
smart_split: Any
try:
    from telebot import TeleBot
    from telebot.util import smart_split
except ImportError:
    TeleBot = None
    smart_split = None

_python_logger = logging.getLogger(__name__)


class ConsoleHandler(LogHandler):
    def __init__(
        self,
        level: LogLevel = "DEBUG",
    ) -> None:
        self.level = level
        self.formatter = InternalLogFormatter()
        self.format = self.formatter.console_format

    def add(self) -> None:
        logger.add(
            sys.stderr,
            format=self.format,
            level=self.level,
            colorize=True,
        )


class FileHandler(LogHandler):
    def __init__(self, config: FileHandlerConfig) -> None:
        self.config = config
        self.formatter = InternalLogFormatter()
        self.format = self.formatter.file_format

    def add(self) -> None:
        logger.add(
            self.config.path,
            level=self.config.level,
            format=self.format,
            rotation=self.config.rotation,
            retention=self.config.retention,
            compression=self.config.compression,
        )


class TelegramHandler(LogHandler):
    """Log handler that sends log entries to Telegram."""

    def __init__(self, config: TelegramHandlerConfig) -> None:
        """
        Initializes the Telegram log handler.

        Args:
            config: Configuration for the Telegram handler.
        """
        if not TeleBot:
            msg = (
                "pytelegrambotapi is not installed. Please install it with "
                "'uv pip install pytelegrambotapi'"
            )
            raise ImportError(msg)

        self.config = config
        self.bot = TeleBot(self.config.bot_token, threaded=False)
        self.formatter = InternalLogFormatter()
        self.format = self.formatter.telegram_format

    def sink(self, message: str) -> None:
        """
        The sink function that actually sends the message.

        Args:
            message: The pre-formatted message from loguru.
        """
        list_messages: list[str] = (
            smart_split(message) if smart_split else [message]
        )

        for admin_id in self.config.admin_ids:
            for msg in list_messages:
                try:
                    self.bot.send_message(
                        admin_id,
                        msg,
                        timeout=self.config.timeout,
                    )
                except Exception as e:
                    log = f"[{self.name}]: failed to send Telegram notification: {e}"
                    _python_logger.exception(log)

    def filter(self, record: Record) -> bool:
        """
        Filter function to decide if a log should be sent.
        Sends only if `extra['notify']` is True.
        """
        return record["extra"].get("notify", False) is True

    def add(self) -> None:
        """Adds the Telegram handler to loguru with the filter and sink."""
        logger.add(
            self.sink,
            format=self.format,
            level=self.config.level,
            filter=self.filter,
        )


class WebSocketHandler(LogHandler):
    """Обработчик для отправки логов через WebSocket"""

    def __init__(self, config: WebSocketHandlerConfig) -> None:
        """
        Инициализирует WebSocket обработчик логов

        Args:
            config: Конфигурация WebSocket обработчика
        """
        self.manager = WebSocketHandlerManager()
        self.formatter = InternalLogFormatter()
        self.level = config.level

    def add(self) -> None:
        """Добавляет обработчик к loguru"""
        logger.add(
            self.process_log,
            level=self.level,
            enqueue=True,
        )
        # Запускаем обработчик очереди
        self.manager.start()

    def process_log(self, message: Message) -> None:
        """
        Обрабатывает сообщение лога

        Args:
            message: Объект Message от loguru, содержащий record
        """
        try:
            record = message.record
            # Формируем LogMessage из record
            log_entry: LogMessage = {
                "level": record["level"].name,
                "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                "message": record["message"],
            }

            # Добавляем в очередь асинхронно, без блокировки
            task = asyncio.create_task(self.manager.add_log(log_entry))
            self.manager.pending_tasks.add(task)
            task.add_done_callback(self.manager.pending_tasks.discard)
        except Exception:
            _python_logger.exception("Ошибка при обработке лога для WebSocket")
