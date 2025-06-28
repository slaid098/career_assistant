from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.db.models.job import Job

if TYPE_CHECKING:
    from pydantic import HttpUrl

    from src.core.schemas import JobSchema


class JobRepository:
    """A repository for handling job data persistence."""

    async def get_all_jobs(self) -> list[Job]:
        """
        Retrieves all job entries from the database.

        Returns:
            list[Job]: A list of all Job objects.
        """
        return await Job.all()

    async def create_job(
        self,
        title: str,
        url: HttpUrl | str,
        company: str | None,
        description: str | None,
        location: str | None,
        salary: str | None,
        **kwargs: Any,
    ) -> Job:
        """
        Creates and saves a new job entry in the database.

        Args:
            title: The job title.
            url: The unique URL for the job posting.
            company: The name of the company.
            description: A description of the job.
            location: The location of the job.
            salary: The salary for the job.
            **kwargs: Additional fields for the Job model.

        Returns:
            The newly created Job object.
        """
        return await Job.create(
            title=title,
            url=str(url),
            company=company,
            description=description,
            location=location,
            salary=salary,
            **kwargs,
        )

    async def get_job_by_url(self, url: HttpUrl | str) -> Job | None:
        """
        Retrieves a job by its URL.

        Args:
            url: The URL of the job to retrieve.

        Returns:
            The Job object if found, otherwise None.
        """
        return await Job.get_or_none(url=str(url))

    async def update_or_create(self, job_schema: JobSchema) -> Job:
        """
        Updates an existing job or creates a new one based on the URL.
        """
        job_dict = job_schema.model_dump(mode="json", exclude_unset=True)
        job, _ = await Job.update_or_create(
            defaults=job_dict, url=job_dict["url"],
        )
        return job

    async def add_one(self, **kwargs: Any) -> Job:
        """
        Adds a single object to the database.

        Args:
            **kwargs: The data for the object to be created.

        Returns:
            The created object.
        """
        return await Job.create(**kwargs)

    async def get_by_id(self, obj_id: int) -> Job | None:
        """
        Retrieves an object by its ID.

        Args:
            obj_id: The ID of the object to retrieve.

        Returns:
            The retrieved object or None if not found.
        """
        return await Job.get_or_none(id=obj_id)
