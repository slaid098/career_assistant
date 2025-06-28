from __future__ import annotations

from loguru import logger

from src.core.services import JobService


async def parse_habr_vacancies() -> None:
    """
    Runs the job processing logic for Habr Career.

    This function acts as an entry point for the scheduler.
    It initializes the JobService and calls the main processing method.
    """
    logger.info("Starting Habr Career parsing task...")

    service = JobService()
    await service.process_habr_vacancies()

    logger.info("Habr Career parsing task finished.")
