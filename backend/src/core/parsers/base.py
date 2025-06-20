from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.schemas import JobSchema


class BaseParser(ABC):
    """Abstract base class for all job parsers."""

    @abstractmethod
    def parse(self, content: str) -> list[JobSchema]:
        """
        Parses the source content and returns a list of job objects.

        This method must be implemented by all concrete parser classes.

        Args:
            content: The string content to parse (e.g., HTML).

        Returns:
            A list of JobSchema objects.
        """
        raise NotImplementedError
