from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import get_job_service
from src.api.schemas import JobResponse
from src.core.services import JobService

router = APIRouter()


@router.get("/jobs")
async def get_all_jobs(
    job_service: Annotated[JobService, Depends(get_job_service)],
) -> list[JobResponse]:
    """
    Возвращает список всех вакансий.
    """
    jobs = await job_service.get_all_jobs()
    # Явно преобразуем объекты Job ORM в объекты JobResponse Pydantic
    return [JobResponse.model_validate(job) for job in jobs]


@router.get("/jobs/{job_id}")
async def get_job_by_id(
    job_id: int,
    job_service: Annotated[JobService, Depends(get_job_service)],
) -> JobResponse:
    """
    Возвращает детали конкретной вакансии по её ID.
    """
    job = await job_service.get_job_by_id(job_id)
    return JobResponse.model_validate(job)
