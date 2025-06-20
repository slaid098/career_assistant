from __future__ import annotations

from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import HttpUrl, ValidationError

from src.core.schemas import JobSchema
from src.utils.notify_logger.logger import logger

from .base import BaseParser


class HabrParser(BaseParser):
    """A parser for job listings from career.habr.com."""

    BASE_URL = "https://career.habr.com"

    def parse(self, content: str) -> list[JobSchema]:
        """
        Parses the HTML content of a habr job listing page.

        Args:
            content: The HTML content of the page.

        Returns:
            A list of JobSchema objects.
        """
        soup = BeautifulSoup(content, "lxml")
        jobs: list[JobSchema] = []
        job_cards = soup.find_all("div", class_="vacancy-card")

        for card in job_cards:
            if isinstance(card, Tag):
                job = self._parse_job_card(card)
                if job:
                    jobs.append(job)

        return jobs

    def _parse_job_card(self, card: Tag) -> JobSchema | None:
        """
        Parses a single job card from the page.

        Args:
            card: A BeautifulSoup Tag object representing a single job card.

        Returns:
            A JobSchema object or None if parsing fails.
        """
        try:
            title_tag = card.find("a", class_="vacancy-card__title-link")
            if not isinstance(title_tag, Tag):
                return None

            title = title_tag.text.strip()
            url = f"https://career.habr.com{title_tag.get('href', '')}"

            company_div = card.find("div", class_="vacancy-card__company-title")
            company = None
            if isinstance(company_div, Tag):
                company_tag = company_div.find("a")
                if isinstance(company_tag, Tag):
                    company = company_tag.text.strip()

            salary_div = card.find("div", class_="vacancy-card__salary-value")
            salary = None
            if isinstance(salary_div, Tag):
                salary = salary_div.text.strip()

            meta_div = card.find("div", class_="vacancy-card__meta")
            location = None
            if isinstance(meta_div, Tag):
                location_tag = meta_div.find("span")
                if isinstance(location_tag, Tag):
                    location = location_tag.text.strip()

            description_div = card.find("div", class_="vacancy-card__description")
            description = None
            if isinstance(description_div, Tag):
                description = description_div.text.strip()

            return JobSchema(
                title=title,
                url=HttpUrl(url),
                company=company,
                salary=salary,
                location=location,
                description=description,
            )
        except (AttributeError, ValidationError) as e:
            logger.debug(
                "Error parsing job card",
                exception=e,
                details=f"Card HTML: {card!s}",
            )
            return None
