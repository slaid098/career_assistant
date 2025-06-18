from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.config.config import DatabaseConfig


def get_tortoise_orm_config(
    db_config: DatabaseConfig,
    models_files: list[str],
) -> dict[str, Any]:
    """
    Returns the configuration for Tortoise ORM.

    The configuration is determined by the `db_config` object. If `db_config.url`
    is provided, it's used directly. Otherwise, connection parameters are
    assembled from the other `db_config` attributes.

    Args:
        db_config: The database configuration object.
        models_files: A list of model modules to include.

    Returns:
        The configuration dictionary for Tortoise ORM.
    """
    connection_config: dict[str, Any]
    if db_config.url:
        connection_config = {"default": db_config.url}
    else:
        connection_config = {
            "default": {
                "engine": db_config.engine,
                "credentials": {
                    "host": db_config.host,
                    "port": db_config.port,
                    "user": db_config.user,
                    "password": db_config.password,
                    "database": db_config.name,
                },
            },
        }

    return {
        "connections": connection_config,
        "apps": {
            "models": {
                "models": [*models_files, "aerich.models"],
                "default_connection": "default",
            },
        },
    }
