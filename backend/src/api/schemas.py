from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class JobResponse(BaseModel):
    """
    Pydantic model for serializing job data for API responses.

    Attributes:
        id (int): The unique identifier of the job.
        title (str): The title of the job.
        company (str): The company offering the job.
        url (HttpUrl): The URL of the job posting.
        description (str | None): A brief description of the job.
        salary (str | None): The salary information for the job.
        created_at (datetime): The timestamp when the job record was created.
        updated_at (datetime): The timestamp when the job record was last updated.
    """

    id: int
    title: str
    company: str
    url: HttpUrl
    description: str | None = None
    salary: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {"from_attributes": True}
