import pytest

from src.db.models import Job


@pytest.mark.asyncio
async def test_db_model_operations() -> None:
    """
    Test basic database operations: creating and retrieving Job model.

    This test checks that:
    1. Connection to the test database (configured in conftest.py) is
    established.
    2. The Job model can be successfully created.
    3. The created model can be found and retrieved from the database.
    """

    # Test data
    test_url = "https://example.com/job/123"
    test_title = "Middle Python Developer"

    await Job.create(
        title=test_title,
        company="Tech Corp",
        location="Remote",
        url=test_url,
        description="A great job.",
    )

    created_job = await Job.get(url=test_url)
    assert created_job is not None
    assert created_job.title == test_title
    assert created_job.company == "Tech Corp"

    job_count = await Job.all().count()
    assert job_count == 1


@pytest.mark.asyncio
async def test_create_and_get_job() -> None:
    """
    Tests the creation and retrieval of a Job model instance.

    This test verifies that a Job can be successfully created with specific
    attributes and then retrieved from the database, confirming that the basic
    database operations and model definitions are working correctly.
    """
    job = await Job.create(
        title="Software Engineer",
        company="Tech Corp",
        location="Remote",
        description="Developing cool stuff.",
        url="https://example.com/job/1",
    )
    retrieved_job = await Job.get(id=job.id)
    assert retrieved_job.id == job.id
    assert retrieved_job.title == "Software Engineer"
