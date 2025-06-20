from __future__ import annotations

import pytest

from src.db.models.job import Job
from src.db.repository import JobRepository


@pytest.mark.asyncio
async def test_create_job() -> None:
    """
    Tests that the create_job method correctly adds a new job to the database.
    """
    repo = JobRepository()
    job_data = {
        "title": "Senior Python Developer",
        "url": "https://example.com/job/123",
        "company": "Tech Innovations Inc.",
        "description": "A great job opportunity.",
        "location": "Moscow",
        "salary": "300000 RUB",
    }

    created_job = await repo.create_job(**job_data)
    assert created_job.id is not None
    assert created_job.title == job_data["title"]


@pytest.mark.asyncio
async def test_get_job_by_url() -> None:
    """
    Tests that get_job_by_url correctly retrieves a job by its URL.
    """
    repo = JobRepository()
    job_data = {
        "title": "Unique Job",
        "url": "https://example.com/job/unique_url",
        "company": "Unique Corp",
        "description": "A one-of-a-kind job.",
        "location": "Internet",
        "salary": "Not specified",
    }
    await repo.create_job(**job_data)

    retrieved_job = await repo.get_job_by_url(job_data["url"])
    assert retrieved_job is not None
    assert retrieved_job.title == job_data["title"]

    non_existent_job = await repo.get_job_by_url("https://example.com/job/nonexistent")
    assert non_existent_job is None
