from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import HttpUrl

from src.core.parsers.habr import HabrParser


@pytest.fixture
def habr_html_content() -> str:
    """Provides the HTML content of a test page from career.habr.com."""
    path = Path(__file__).parent.parent / "test_data" / "habr_vacancies.html"
    with path.open(encoding="utf-8") as f:
        return f.read()


def test_habr_parser_returns_correct_job_list(habr_html_content: str) -> None:
    """
    Tests that the HabrParser correctly parses a list of jobs from HTML.

    Args:
        habr_html_content: HTML content of the job listing page.
    """
    # 1. Arrange
    parser = HabrParser()

    # 2. Act
    jobs = parser.parse(habr_html_content)

    # 3. Assert
    # The test HTML has 3 vacancy cards, but one is malformed (no title link).
    # The parser should gracefully skip it and return 2 valid jobs.
    expected_jobs_count = 2
    assert len(jobs) == expected_jobs_count

    # Check the first job in detail
    first_job = jobs[0]
    assert first_job.title == "Python Developer"
    assert first_job.company == "Test Corp"
    assert first_job.salary == "$5000 - $7000"
    assert first_job.location == "Remote"
    assert first_job.description == "We are looking for a skilled Python developer."
    assert first_job.url == HttpUrl("https://career.habr.com/vacancies/10001")

    # Check the second job's title to ensure it was also parsed
    second_job = jobs[1]
    assert second_job.title == "Data Scientist"
