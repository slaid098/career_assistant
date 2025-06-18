from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import Tortoise
from tortoise.connection import connections

# from src.utils.notify_logger.logger import logger
from .config import get_tortoise_orm_config

if TYPE_CHECKING:
    from src.config.config import DatabaseConfig


_MODELS_FILES = [
    "src.db.models.job",
]


async def init_db(db_config: DatabaseConfig) -> None:
    """
    Initializes the database connection and generates schemas.

    This function should be called once at the start of the application,
    with the appropriate configuration.

    Args:
        db_config: The database configuration object.
    """
    # logger.info("Initializing database connection...")
    tortoise_orm_config = get_tortoise_orm_config(
        db_config=db_config,
        models_files=_MODELS_FILES,
    )
    try:
        await Tortoise.init(config=tortoise_orm_config)
        await Tortoise.generate_schemas()
        # logger.info("Database connection initialized successfully.")
    except Exception as e:
        # logger.error("Database initialization error", exception=e)
        raise e from e


async def close_db() -> None:
    """
    Close all established database connections.

    This function should be called at the end of the application's lifecycle.
    """
    # logger.info("Closing database connections...")
    await connections.close_all()
    # logger.info("All database connections closed.")
