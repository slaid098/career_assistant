from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from src.utils.notify_logger.logger import logger

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from datetime import datetime


class TaskScheduler:
    """Class for managing tasks."""

    def __init__(self) -> None:
        """Initialize the scheduler."""
        self.scheduler = AsyncIOScheduler()
        self._is_running = False
        self.name = self.__class__.__name__

    def start(self) -> None:
        """Start the scheduler."""
        if not self._is_running:
            self.scheduler.start()
            self._is_running = True
            logger.info("планировщик запущен", author=self.name)

    def stop(self) -> None:
        """Stop the scheduler."""
        if self._is_running:
            self.scheduler.shutdown()
            self._is_running = False
            logger.info("планировщик остановлен", author=self.name)

    def add_interval_job(  # noqa: PLR0913
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        start_date: datetime | None = None,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
        job_id: str | None = None,
    ) -> None:
        """Add a periodic task."""
        trigger = IntervalTrigger(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            start_date=start_date,
        )

        self.scheduler.add_job(
            func,
            trigger=trigger,
            args=args or (),
            kwargs=kwargs or {},
            id=job_id,
            replace_existing=True,
        )
        log = f"periodic task added: {func.__name__}"
        logger.info(log, author=self.name)

    def remove_job(self, job_id: str) -> None:
        """Remove a task by ID."""
        self.scheduler.remove_job(job_id)
        logger.info(f"task removed: {job_id}", author=self.name)

    def add_onetime_job(
        self,
        func: Callable[..., Coroutine[Any, Any, Any]],
        run_date: datetime,
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
        job_id: str | None = None,
    ) -> None:
        """Add a one-time task.

        If a task with the same job_id already exists, it will be replaced.
        """
        trigger = DateTrigger(run_date=run_date)

        self.scheduler.add_job(
            func,
            trigger=trigger,
            args=args or (),
            kwargs=kwargs or {},
            id=job_id,
            replace_existing=True,
        )
        log = f"one-time task added: {func.__name__} on {run_date}"
        logger.info(log, author=self.name)
