from datetime import datetime
from typing import TYPE_CHECKING, Any

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from src.api.schemas import JobResponse
from src.db.repository import JobRepository
from src.main import app  # Импортируем наше FastAPI приложение

if TYPE_CHECKING:
    from src.db.models import Job


@pytest.fixture
def job_repository() -> JobRepository:
    """
    Returns a JobRepository instance for test usage.
    """
    return JobRepository()


def test_job_response_pydantic_fails() -> None:
    """
    Test that JobResponse Pydantic model raises ValidationError when required fields are missing.
    """
    with pytest.raises(ValidationError):
        JobResponse()  # type: ignore[reportCallIssue]


def test_job_response_pydantic_succeeds() -> None:
    """
    Test that JobResponse Pydantic model can be successfully created with all required and
    optional fields.
    """
    job_data: dict[str, Any] = {
        "id": 1,
        "title": "Python Developer",
        "company": "Tech Corp",
        "url": "https://example.com/job/1",
        "description": "A great job opportunity.",
        "salary": "100000 USD",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    job_response = JobResponse(**job_data)

    assert job_response.id == job_data["id"]
    assert job_response.title == job_data["title"]
    assert job_response.company == job_data["company"]
    assert str(job_response.url) == job_data["url"]
    assert job_response.description == job_data["description"]
    assert job_response.salary == job_data["salary"]
    assert job_response.created_at == job_data["created_at"]
    assert job_response.updated_at == job_data["updated_at"]


# @pytest.mark.asyncio
def test_get_all_jobs_endpoint_returns_empty_list_initially() -> None:
    """
    Test that GET /api/v1/jobs endpoint returns an empty list if no jobs are in the database.
    This is a 'red' test, as the endpoint is not yet implemented to return actual data.
    """
    client = TestClient(app)
    response = client.get("/api/v1/jobs")
    success_status_code = 200

    assert response.status_code == success_status_code
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_all_jobs_returns_list_of_jobs(job_repository: JobRepository) -> None:
    """
    Test that GET /api/v1/jobs endpoint returns a list of jobs when the database is not empty.
    """
    # Arrange: Create multiple jobs
    await job_repository.add_one(
        title="Python Developer",
        company="Company A",
        url="https://companya.com/job/1",
        description="Desc A",
    )
    await job_repository.add_one(
        title="Data Scientist",
        company="Company B",
        url="https://companyb.com/job/2",
        description="Desc B",
    )
    client = TestClient(app)

    # Act
    response = client.get("/api/v1/jobs")

    # Assert
    success_status_code = 200
    expected_jobs_count = 2
    assert response.status_code == success_status_code

    response_data = response.json()
    assert len(response_data) == expected_jobs_count
    assert response_data[0]["title"] == "Python Developer"
    assert response_data[1]["title"] == "Data Scientist"


def test_get_job_by_id_returns_404_for_nonexistent_job() -> None:
    """
    Test that GET /api/v1/jobs/{job_id} endpoint returns 404 Not Found for a job that does
    not exist.
    """
    client = TestClient(app)
    response = client.get("/api/v1/jobs/999")  # Non-existent job ID
    not_found_status_code = 404

    assert response.status_code == not_found_status_code


@pytest.mark.asyncio
async def test_get_job_by_id_with_existing_job(job_repository: JobRepository) -> None:
    """
    Test that GET /api/v1/jobs/{job_id} endpoint returns the correct job data when the
    job exists in the database.
    """
    # Arrange: Create a job in the database
    test_job: Job = await job_repository.add_one(
        title="Senior Pythonista",
        company="Code Masters",
        url="https://codemasters.com/jobs/1",
        description="Write beautiful code.",
        salary="200000 USD",
    )
    client = TestClient(app)

    # Act: Request the job by its ID
    response = client.get(f"/api/v1/jobs/{test_job.id}")

    # Assert: Check the response
    success_status_code = 200
    assert response.status_code == success_status_code

    response_data = response.json()
    assert response_data["id"] == test_job.id
    assert response_data["title"] == test_job.title
    assert response_data["company"] == test_job.company
    assert response_data["url"] == test_job.url
