import httpx
from fastapi import HTTPException
from loguru import logger

from src.core.parsers.habr import HabrParser
from src.db.models import Job
from src.db.repository import JobRepository


class JobService:
    """A service for processing jobs and saving them to the database."""

    def __init__(
        self,
        repo: JobRepository | None = None,
    ) -> None:
        """
        Initializes the JobService.

        Args:
            repo: An instance of JobRepository.
        """
        self._repo = repo or JobRepository()

    async def get_all_jobs(self) -> list[Job]:
        """
        Retrieves all job vacancies from the database.

        Returns:
            list[Job]: A list of all job vacancies.
        """
        return await self._repo.get_all_jobs()

    async def process_habr_vacancies(self) -> None:
        """
        Fetches, parses, and saves new job vacancies from Habr Career.
        """
        url = "https://career.habr.com/vacancies/python_developer"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",  # noqa: E501
        }
        logger.info("Starting Habr Career processing...")

        try:
            async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error("HTTP error occurred while fetching Habr vacancies: {error}", error=e)
            return
        except httpx.RequestError as e:
            logger.error("Request error occurred while fetching Habr vacancies: {error}", error=e)
            return

        parser = HabrParser()
        jobs = parser.parse(response.text)

        if not jobs:
            logger.info("No new jobs found on Habr Career.")
            return

        logger.info("Found {count} jobs on the page.", count=len(jobs))

        new_jobs_count = 0
        for job_schema in jobs:
            existing_job = await self._repo.get_job_by_url(job_schema.url)
            if not existing_job:
                await self._repo.create_job(
                    title=job_schema.title,
                    url=job_schema.url,
                    company=job_schema.company,
                    description=job_schema.description,
                    location=job_schema.location,
                    salary=job_schema.salary,
                )
                new_jobs_count += 1
                logger.bind(notify=True).info(
                    "✅ Found new job: {title}", title=job_schema.title,
                )

        logger.info(
            "Habr Career processing finished. Added {count} new jobs.",
            count=new_jobs_count,
        )

    async def get_job_by_id(self, job_id: int) -> Job:
        """
        Retrieves a job by its ID.

        Args:
            job_id: The ID of the job to retrieve.

        Returns:
            The job object.

        Raises:
            HTTPException: If the job with the specified ID is not found.
        """
        job = await self._repo.get_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
