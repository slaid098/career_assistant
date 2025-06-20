from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest

from src.scheduler.scheduler import TaskScheduler

if TYPE_CHECKING:
    from apscheduler.job import Job
    from pytest_mock import MockerFixture


async def dummy_async_job() -> None:
    """A dummy asynchronous job for testing."""


@pytest.mark.asyncio
async def test_add_and_get_job(mocker: MockerFixture) -> None:  # noqa: ARG001
    """
    Tests that a job can be added to the scheduler and retrieved.

    Args:
        mocker: The pytest-mock fixture.
    """
    # 1. Initialize the scheduler
    scheduler = TaskScheduler()

    # 2. Add a job
    job_id = "test_job_1"
    scheduler.add_interval_job(dummy_async_job, seconds=10, job_id=job_id)

    # 3. Check that the job exists
    retrieved_job = cast("Job", scheduler.scheduler.get_job(job_id))
    assert retrieved_job is not None
    assert retrieved_job.id == job_id

    scheduler.remove_job(job_id)
    assert scheduler.scheduler.get_job(job_id) is None
