import httpx

from src.core.parsers.base import BaseParser
from src.core.schemas import JobSchema
from src.db.repository import JobRepository
from src.utils.notify_logger.logger import logger


class ParserService:
    """A service for parsing jobs from a URL and saving them to the database."""

    def __init__(
        self,
        parser: BaseParser,
        repo: JobRepository,
        client: httpx.AsyncClient | None = None,
    ):
        """
        Initializes the ParserService.

        Args:
            parser: An instance of a class that inherits from BaseParser.
            repo: An instance of JobRepository.
            client: An optional httpx.AsyncClient for making web requests.
        """
        self._parser = parser
        self._repo = repo
        self._client = client or httpx.AsyncClient()

    async def process_url(self, url: str) -> None:
        """
        Processes a URL to fetch, parse, and save job listings.

        Args:
            url: The URL to process.
        """
        try:
            response = await self._client.get(url)
            response.raise_for_status()
            content = response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred while fetching {url}: {e}")
            return
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting {url}: {e}")
            return

        jobs: list[JobSchema] = self._parser.parse(content=content)

        for job_data in jobs:
            await self._repo.update_or_create(job_data)
            
        logger.info(f"Processed {len(jobs)} jobs from {url}") 