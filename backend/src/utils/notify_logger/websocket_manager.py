from __future__ import annotations

import asyncio
import contextlib
import datetime
import logging
import time
from collections import deque
from pathlib import Path
from typing import TYPE_CHECKING, Self

from src.utils.notify_logger.tools import LogMessage, parse_log_message

if TYPE_CHECKING:
    from src.utils.notify_logger.config import WebSocketHandlerConfig

    from .types import WebSocketClient

_python_logger = logging.getLogger(__name__)


class WebSocketHandlerManager:
    """Менеджер для управления WebSocket клиентами и отправкой логов"""

    _instance = None

    def __new__(cls) -> Self:
        """Реализация паттерна Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Инициализация менеджера WebSocket"""
        if self.initialized:
            return

        self.clients: set[WebSocketClient] = set()
        self.log_queue: asyncio.Queue[LogMessage] = asyncio.Queue(
            maxsize=5000,
        )
        self.log_history: deque[LogMessage] = deque(maxlen=200)
        self.processor_task: asyncio.Task[None] | None = None
        self.initialized = True
        self.name = self.__class__.__name__
        self.pending_tasks: set[asyncio.Task[None]] = set()
        self.config: WebSocketHandlerConfig | None = None
        self.log_file_path: str | None = None

    def configure(
        self,
        config: WebSocketHandlerConfig,
        log_file_path: str | None = None,
    ) -> None:
        """Конфигурирует менеджер. Вызывается один раз."""
        if self.config is not None:
            return
        self.config = config
        self.log_file_path = log_file_path
        self.log_history = deque(maxlen=self.config.max_history)

    def start(self) -> None:
        """Запускает обработчик логов"""
        if self.processor_task is None or self.processor_task.done():
            if self.log_file_path:
                self._add_logs_from_file()
            self.processor_task = asyncio.create_task(self._process_logs())

    async def stop(self) -> None:
        """Останавливает обработчик логов"""
        if self.processor_task and not self.processor_task.done():
            self.processor_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.processor_task

        # Очищаем все ожидающие задачи
        for task in self.pending_tasks:
            if not task.done():
                task.cancel()

        self.pending_tasks.clear()

    def _add_logs_from_file(self) -> None:
        """Загружает логи из файла"""
        if not self.log_file_path or not Path(self.log_file_path).exists():
            return

        timezone = self._get_system_timezone()
        current_time = self._get_current_time(timezone)
        logs = Path(self.log_file_path).read_text()
        for line in logs.splitlines():
            log = parse_log_message(line)
            log_timestamp = self._get_log_timestamp(log, timezone)
            if log_timestamp and log_timestamp < current_time:
                self.log_history.append(log)

    def _get_log_timestamp(
        self,
        log_message: LogMessage,
        timezone: datetime.timezone,
    ) -> datetime.datetime | None:
        """Получает timestamp из лога"""
        try:
            return datetime.datetime.strptime(
                log_message["timestamp"],
                "%Y-%m-%d %H:%M:%S.%f",
            ).replace(tzinfo=timezone)
        except ValueError as e:
            log = f"Ошибка при получении timestamp из лога: {e}"
            _python_logger.exception(log)
            return None

    def _get_system_timezone(self) -> datetime.timezone:
        """Получает смещение системной временной зоны"""
        time_now = time.time()

        # Получаем локальное время как наивный datetime
        local_time = datetime.datetime.fromtimestamp(time_now)
        # Получаем UTC время используя рекомендованный способ
        utc_time = datetime.datetime.fromtimestamp(time_now, tz=datetime.UTC)

        # Приводим локальное время к UTC для корректного сравнения
        local_time_utc = local_time.replace(tzinfo=datetime.UTC)

        # Вычисляем разницу
        offset = local_time_utc - utc_time
        return datetime.timezone(offset)

    def _get_current_time(
        self,
        timezone: datetime.timezone,
    ) -> datetime.datetime:
        """Получает текущее время"""
        return datetime.datetime.now(timezone)

    async def _process_logs(self) -> None:
        """Обрабатывает очередь логов и отправляет их клиентам"""
        while True:
            try:
                log_entry = await self.log_queue.get()

                # Добавляем в историю
                self.log_history.append(log_entry)

                # Если есть подключенные клиенты, отправляем им лог
                if self.clients:
                    # Создаем задачу для отправки логов, чтобы не блокировать
                    # основной цикл
                    send_task = asyncio.create_task(
                        self._send_to_clients(log_entry),
                    )
                    self.pending_tasks.add(send_task)
                    send_task.add_done_callback(self.pending_tasks.discard)

                self.log_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                log = f"Ошибка при обработке логов: {e}"
                _python_logger.exception(log)
                await asyncio.sleep(0.1)  # Небольшая пауза при ошибке

    async def _send_to_clients(self, log_entry: LogMessage) -> None:
        """
        Отправляет лог всем клиентам

        Args:
            log_entry: Запись лога для отправки
        """
        disconnected: set[WebSocketClient] = set()
        clients = set(self.clients)
        for client in clients:
            try:
                await client.send_json(log_entry)
            except Exception as e:
                log = f"Ошибка при отправке логов клиенту: {e}"
                _python_logger.exception(log)
                disconnected.add(client)

        # Удаляем отключенные клиенты
        for client in disconnected:
            self.clients.discard(client)

    def add_client(self, client: WebSocketClient) -> None:
        """
        Добавляет нового клиента для отправки логов.

        Args:
            client: Объект с методом `send_json` для отправки данных.
        """
        self.clients.add(client)

    def remove_client(self, client: WebSocketClient) -> None:
        """
        Удаляет клиента из списка получателей.

        Args:
            client: Ранее добавленный объект клиента.
        """
        self.clients.discard(client)

    async def send_history(
        self,
        client: WebSocketClient,
        limit: int | None = None,
    ) -> None:
        """
        Отправляет историю логов клиенту

        Args:
            client: Объект клиента
            limit: Ограничение количества записей
        """
        if not self.log_history:
            return

        if limit is None:
            limit = self.config.max_history if self.config else 200

        try:
            history = list(self.log_history)[-limit:]
            # Отправляем историю через методом `send_json`
            await client.send_json({"type": "history", "logs": history})
        except Exception as e:
            print(f"Ошибка при отправке истории логов: {e}")
            self.remove_client(client)

    async def add_log(self, log_entry: LogMessage) -> None:
        """
        Добавляет лог в очередь отправки

        Args:
            log_entry: Запись лога
        """
        # Защита от переполнения очереди
        try:
            # Используем non-blocking put с тайм-аутом
            await asyncio.wait_for(self.log_queue.put(log_entry), timeout=0.5)
        except asyncio.TimeoutError:  # noqa: UP041
            # Если очередь переполнена, пропускаем некритичные логи
            if log_entry.get("level") in ["ERROR", "CRITICAL"]:
                # Для критичных логов пробуем еще раз, но уже в
                # блокирующем режиме
                await self.log_queue.put(log_entry)
            else:
                log = f"Очередь логов переполнена, лог пропущен: {log_entry.get('message', '')}"
                _python_logger.exception(log)
