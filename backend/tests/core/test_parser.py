from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from src.core.parsers.base import BaseParser
from src.core.parsers.habr import HabrParser


@pytest.mark.asyncio
async def test_parser_inheritance_and_interface() -> None:
    """
    Tests that a concrete parser correctly inherits from BaseParser
    and implements the required 'parse' method.
    """
    assert issubclass(HabrParser, BaseParser)
    parser_instance = HabrParser()
    assert hasattr(parser_instance, "parse")
    assert not asyncio.iscoroutinefunction(parser_instance.parse)


@pytest.mark.asyncio
async def test_habr_parser_parses_job_correctly() -> None:
    """
    Tests that HabrParser correctly parses a local HTML file
    and returns a valid Job object.
    """
    base_dir = Path(__file__).parent.parent
    html_path = base_dir / "test_data" / "html" / "habr_python_developer.html"
    html_content = html_path.read_text(encoding="utf-8")

    parser = HabrParser()
    jobs = parser.parse(html_content)

    assert jobs
    job = jobs[0]

    assert "Python" in job.title

    if job.company:
        assert "Best Company Ever" in job.company

    if job.location:
        assert "Москва" in job.location

    if job.salary:
        assert "250 000" in job.salary

    if job.description:
        assert "Python" in job.description
        assert "django" in job.description.lower()
        assert "fastapi" in job.description.lower()
