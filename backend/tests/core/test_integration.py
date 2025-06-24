from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
import pytest

from src.core.tasks import parse_habr_vacancies
from src.db.models.job import Job
from src.scheduler.scheduler import TaskScheduler

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_full_cycle_via_scheduler(
    db_init: None,  # noqa: ARG001
    mocker: MockerFixture,
) -> None:
    """
    Integration test to verify the complete cycle: scheduler -> task -> save.

    This test ensures that the TaskScheduler correctly triggers the parsing
    task, which then fetches, parses, and saves job data into the database.
    It also checks for idempotency to prevent duplicate entries.
    """
    # 1. Prepare mock HTML content from a local file
    base_dir = Path(__file__).parent.parent
    html_path = base_dir / "test_data" / "html" / "habr_python_developer.html"
    html_content = html_path.read_text(encoding="utf-8")

    # 2. Mock the HTTP client's response to avoid real network requests
    mock_response = httpx.Response(
        200,
        content=html_content,
        request=httpx.Request("GET", "https://career.habr.com"),
    )
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    # 3. Patch the scheduler's default job setup to run immediately
    # We prevent the original setup (e.g., 60-minute interval) from running.
    mocker.patch(
        "src.scheduler.scheduler.TaskScheduler.setup_jobs", return_value=None
    )

    # 4. Initialize the scheduler and manually add a fast, repeating job
    scheduler = TaskScheduler()
    scheduler.add_interval_job(parse_habr_vacancies, seconds=1)
    scheduler.start()

    try:
        # 5. Wait for the first job to be created by polling the database
        jobs_in_db = []
        for _ in range(30):  # Wait for a maximum of 3 seconds
            jobs_in_db = await Job.all()
            if jobs_in_db:
                break
            await asyncio.sleep(0.1)

        # 6. Check that one job was created
        assert len(jobs_in_db) == 1
        assert jobs_in_db[0].title == "Python-разработчик"

        # 7. Wait for the scheduler to trigger the task a second time
        await asyncio.sleep(1.5)

        # 8. Check that no new jobs were added (idempotency check)
        jobs_in_db_after_second_run = await Job.all()
        assert len(jobs_in_db_after_second_run) == 1

    finally:
        # 9. Clean up by stopping the scheduler
        scheduler.stop()
