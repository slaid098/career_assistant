from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, model_validator

from .types import CompressionType, LogLevel  # noqa: TC001  need for pydantic


class BaseTelegramConfig(BaseModel):
    """Base configuration for Telegram (handlers and notifiers)."""

    bot_token: str
    admin_ids: list[int]
    timeout: int = 2


class FileHandlerConfig(BaseModel):
    """Configuration for the file handler."""

    path: Path = Path("app_data", "log", "log.log")
    level: LogLevel = "INFO"
    rotation: str = "10 MB"
    retention: str = "30 days"
    compression: CompressionType | None = "zip"


class TelegramHandlerConfig(BaseTelegramConfig):
    """Configuration for the Telegram handler."""

    level: LogLevel = "WARNING"


class WebSocketHandlerConfig(BaseModel):
    """Configuration for the WebSocket handler."""

    level: LogLevel = "DEBUG"
    max_history: int = 200


class TelegramNotifierConfig(BaseTelegramConfig):
    """Configuration for the Telegram notifier."""

    name: str = "telegram"

    @model_validator(mode="after")
    def check_telebot_installed(
        self: TelegramNotifierConfig,
    ) -> TelegramNotifierConfig:
        try:
            import telebot  # noqa: F401
        except ImportError as e:
            msg = (
                "pytelegrambotapi is not installed. Please install it with "
                "'uv add pytelegrambotapi'"
            )
            raise ValueError(msg) from e
        return self


class LoggerConfig(BaseModel):
    """Main configuration for the logger."""

    log_level: LogLevel = "DEBUG"
    """Level for Loguru logger"""

    std_log_level: LogLevel | None = Field(
        default=None,
        description=(
            "Optional level for Python standard library logger; if not set, log_level is used"
        ),
    )

    use_file_handler: bool = True
    file_handler: FileHandlerConfig = Field(default_factory=FileHandlerConfig)

    use_telegram_handler: bool = False
    telegram_handler: TelegramHandlerConfig | None = None

    use_websocket_handler: bool = False
    websocket_handler: WebSocketHandlerConfig = Field(
        default_factory=WebSocketHandlerConfig,
    )

    use_telegram_notifier: bool = False
    telegram_notifier: TelegramNotifierConfig | None = None

    @model_validator(mode="after")
    def check_dependencies(self) -> LoggerConfig:
        if self.use_telegram_handler and self.telegram_handler is None:
            msg = "telegram_handler config is required when use_telegram_handler is True"
            raise ValueError(msg)
        if self.use_telegram_notifier and self.telegram_notifier is None:
            msg = "telegram_notifier config is required when use_telegram_notifier is True"
            raise ValueError(msg)
        return self
