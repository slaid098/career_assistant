from typing import ClassVar

from tortoise import fields, models


class Job(models.Model):
    """
    Model for storing job information in the database.

    Attributes:
        id (int): Unique job identifier, primary key.
        title (str): Job title.
        company (str): Company name that posted the job.
        location (str): Job location.
        url (str): Unique job URL, used to prevent duplicates.
        description (str): Full job description.
        salary (str | None): Salary information, can be None.
        posted_date (datetime | None): Job posting date, can be None.
        created_at (datetime): Date and time of record creation.
        updated_at (datetime): Date and time of the last record update.
    """

    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=255)
    company = fields.CharField(max_length=255)
    location = fields.CharField(max_length=255)
    url = fields.CharField(max_length=512, unique=True, db_index=True)
    description = fields.TextField()
    salary = fields.CharField(max_length=255, null=True)
    posted_date = fields.DatetimeField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        table = "jobs"
        ordering: ClassVar[list[str]] = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} at {self.company}"
