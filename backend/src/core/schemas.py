from __future__ import annotations

from pydantic import BaseModel, HttpUrl, field_validator


class JobSchema(BaseModel):
    """Represents a job vacancy with its essential details."""

    title: str
    url: HttpUrl
    company: str | None = None
    salary: str | None = None
    location: str | None = None
    description: str | None = None

    @field_validator("title", "company", "location", "description", "salary")
    @classmethod
    def strip_and_clean(cls, value: str | None) -> str | None:
        """Removes leading/trailing whitespace and newlines."""
        if value:
            return " ".join(value.strip().split())
        return value
