from pydantic import BaseModel, HttpUrl


class JobSchema(BaseModel):
    """Pydantic schema for a job listing."""

    title: str
    url: HttpUrl
    company: str | None = None
    salary: str | None = None
    location: str | None = None
    description: str | None = None
