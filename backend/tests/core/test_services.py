from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.parsers.base import BaseParser
from src.core.schemas import JobSchema
from src.core.services import ParserService
from src.db.repository import JobRepository


@pytest.mark.asyncio
async def test_parser_service_processes_and_saves_jobs():
    """Tests that ParserService correctly processes content and saves jobs."""
    # 1. Arrange
    # Create fake job data that the mock parser will return
    fake_jobs = [
        JobSchema(
            title="Python Developer",
            url="https://example.com/job/1",  # type: ignore
            company="Test Corp",
            location="Remote",
        ),
        JobSchema(
            title="Data Scientist",
            url="https://example.com/job/2",  # type: ignore
            company="Data Inc.",
            location="New York",
        ),
    ]

    # Mock the parser, client and repository
    mock_parser = MagicMock(spec=BaseParser)
    mock_parser.parse.return_value = fake_jobs

    mock_response = MagicMock()
    mock_response.text = "<html></html>"
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    mock_repo = AsyncMock(spec=JobRepository)

    # Instantiate the service with mocks
    service = ParserService(
        parser=mock_parser, repo=mock_repo, client=mock_client
    )

    # 2. Act
    test_url = "https://fake-url.com"
    await service.process_url(test_url)

    # 3. Assert
    # Verify that the client and parser were called correctly
    mock_client.get.assert_called_once_with(test_url)
    mock_parser.parse.assert_called_once_with(content=mock_response.text)

    # Verify that the repository's method was called for each job
    assert mock_repo.update_or_create.call_count == len(fake_jobs)
    mock_repo.update_or_create.assert_any_call(fake_jobs[0])
    mock_repo.update_or_create.assert_any_call(fake_jobs[1])
