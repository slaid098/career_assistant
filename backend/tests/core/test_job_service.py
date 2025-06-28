# This file will contain tests for the JobService.

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import HttpUrl

from src.core.schemas import JobSchema
from src.core.services import JobService


@pytest.fixture
def mock_job_repo() -> AsyncMock:
    """Fixture to create a mock JobRepository."""
    mock_repo = AsyncMock()

    # Simulate that one job already exists, and the other doesn't
    async def get_job_by_url(url: HttpUrl | str) -> JobSchema | None:
        if str(url) == "https://example.com/job/existing":
            return JobSchema(
                title="Existing Job",
                url=HttpUrl("https://example.com/job/existing"),
                company="Old Corp",
            )
        return None

    mock_repo.get_job_by_url.side_effect = get_job_by_url
    mock_repo.create_job = AsyncMock()
    return mock_repo


@pytest.fixture
def fake_jobs_from_parser() -> list[JobSchema]:
    """Fixture to provide a list of fake jobs."""
    return [
        JobSchema(
            title="Existing Job",
            url=HttpUrl("https://example.com/job/existing"),
            company="Old Corp",
        ),
        JobSchema(
            title="New Python Developer",
            url=HttpUrl("https://example.com/job/new"),
            company="New Tech Inc.",
            description="A great new job.",
        ),
    ]


@pytest.mark.asyncio
@patch("src.core.services.HabrParser")
@patch("src.core.services.httpx.AsyncClient")
@patch("src.core.services.logger")
async def test_process_habr_vacancies_saves_new_jobs_and_notifies(
    mock_logger: MagicMock,
    mock_client: MagicMock,
    mock_parser: MagicMock,
    mock_job_repo: AsyncMock,
    fake_jobs_from_parser: list[JobSchema],
) -> None:
    """
    Tests that JobService correctly processes vacancies:
    - Fetches data using httpx.
    - Uses the parser to get jobs.
    - Creates only new jobs in the repository.
    - Sends a notification for new jobs only.
    """
    # 1. Arrange
    # Setup mock for httpx response
    mock_response = AsyncMock()
    mock_response.text = "<html></html>"
    mock_client.return_value.__aenter__.return_value = mock_response

    # Setup mock for parser
    mock_parser_instance = MagicMock()
    mock_parser_instance.parse.return_value = fake_jobs_from_parser
    mock_parser.return_value = mock_parser_instance

    mock_notify_logger = MagicMock()
    mock_logger.bind.return_value = mock_notify_logger

    # Instantiate the service with the mocked repository
    service = JobService(repo=mock_job_repo)

    # 2. Act
    await service.process_habr_vacancies()


    # 3. Assert
    # Check that we tried to find both jobs in the DB
    expected_call_count = 2
    assert mock_job_repo.get_job_by_url.call_count == expected_call_count
    mock_job_repo.get_job_by_url.assert_any_call(HttpUrl("https://example.com/job/existing"))
    mock_job_repo.get_job_by_url.assert_any_call(HttpUrl("https://example.com/job/new"))

    # Check that a new job was created ONLY ONCE
    mock_job_repo.create_job.assert_called_once()
    # Check that the created job is the new one
    args, kwargs = mock_job_repo.create_job.call_args
    assert kwargs["title"] == "New Python Developer"
    assert kwargs["url"] == HttpUrl("https://example.com/job/new")

    # Check that the notification was sent ONLY ONCE
    mock_logger.bind.assert_called_once_with(notify=True)
    mock_notify_logger.info.assert_called_once()
    # Check the content of the notification
    args, kwargs = mock_notify_logger.info.call_args
    assert "Found new job" in args[0]
    assert kwargs["title"] == "New Python Developer"

    # Check that the old service is not being used
    del service

    await asyncio.sleep(0)  # Allow other tasks to run
