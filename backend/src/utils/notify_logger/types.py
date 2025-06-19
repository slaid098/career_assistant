from abc import ABC, abstractmethod
from typing import Any, Literal, Protocol, TypedDict

LogLevel = Literal["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]

CompressionType = Literal[
    "zip",
    "tar",
    "gz",
    "bz2",
    "xz",
    "lzma",
    "tar.gz",
    "tar.bz2",
    "tar.xz",
]


class LogHandler(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def add(self) -> None:
        raise NotImplementedError


class LogMessage(TypedDict):
    level: str
    timestamp: str
    message: str


class WebSocketClient(Protocol):
    """Protocol for WebSocket clients used by WebSocketHandlerManager."""

    async def send_json(self, data: Any) -> None:
        """Sends JSON-serializable data to the client"""
        ...
