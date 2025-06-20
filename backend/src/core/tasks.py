from __future__ import annotations

import httpx
from loguru import logger

from src.core.parsers.habr import HabrParser
from src.db.repository import JobRepository


async def parse_habr_vacancies() -> None:
    """
    Fetches, parses, and saves new job vacancies from Habr Career.

    This function performs the following steps:
    1.  Makes an HTTP request to the Habr Career vacancies page.
    2.  Uses HabrParser to extract job data from the HTML.
    3.  For each found job, checks if it already exists in the database.
    4.  If the job is new, it saves it to the database.
    """
    url = "https://career.habr.com/vacancies/python_developer"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",  # noqa: E501
    }
    logger.info("Starting Habr Career parsing task...")

    try:
        async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
    except httpx.HTTPStatusError as e:
        logger.error(
            "HTTP error occurred while fetching Habr vacancies: {error}", error=e,
        )
        return
    except httpx.RequestError as e:
        logger.error("Request error occurred while fetching Habr vacancies: {error}", error=e)
        return

    parser = HabrParser()
    jobs = parser.parse(response.text)
    repo = JobRepository()

    if not jobs:
        logger.info("No new jobs found on Habr Career.")
        return

    logger.info("Found {count} jobs on the page.", count=len(jobs))

    new_jobs_count = 0
    for job_schema in jobs:
        existing_job = await repo.get_job_by_url(job_schema.url)
        if not existing_job:
            await repo.create_job(
                title=job_schema.title,
                url=job_schema.url,
                company=job_schema.company,
                description=job_schema.description,
                location=job_schema.location,
                salary=job_schema.salary,
            )
            new_jobs_count += 1
            logger.info("Saved new job: {title}", title=job_schema.title)

    logger.info(
        "Habr Career parsing task finished. Added {count} new jobs.",
        count=new_jobs_count,
    )
