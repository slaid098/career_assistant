from src.core.services import JobService


def get_job_service() -> JobService:
    """
    Dependency provider for JobService.

    Returns:
        JobService: An instance of the JobService.
    """
    return JobService()
