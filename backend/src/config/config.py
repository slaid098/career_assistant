from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from src.utils.notify_logger.config import LoggerConfig


def get_config_path(file_name: Literal["config.yaml", ".env"]) -> Path:
    """
    Get the path to the config file.

    Returns:
        Path: The path to the config file.
    """
    current_dir = Path(__file__).resolve()
    while current_dir.parent != current_dir and not (current_dir / file_name).exists():
        current_dir = current_dir.parent
    print(current_dir / file_name)
    return current_dir / file_name


# Добавляем модели для других секций конфига, если они есть в config.yaml
class FrontendServeConfig(BaseModel):
    """
    Configuration settings for serving the frontend application.

    Attributes:
        host (str): The host address for the frontend server.
        port (int): The port number for the frontend server.
    """

    host: str = "localhost"
    port: int = 3000


class FrontendConfig(BaseModel):
    """
    Overall frontend application configuration.

    Attributes:
        serve (FrontendServeConfig): Settings related to serving the frontend.
        static_dir (str): The directory where static frontend build files are
        located.
    """

    serve: FrontendServeConfig = Field(default_factory=FrontendServeConfig)
    static_dir: str = "frontend/build"


class DatabaseConfig(BaseModel):
    """
    Configuration settings for the database connection.

    Can be defined either via a connection URL or by individual parameters.

    Attributes:
        url (Optional[str]): A full database connection URL. If provided,
         other parameters are ignored.
        host (str): The database host address.
        port (int): The database port number.
        user (str): The username for database access.
        password (Optional[str]): The password for database access. Loaded from
         environment variables for security.
        name (str): The name of the database to connect to.
        engine (str): The Tortoise ORM backend engine.
    """

    url: str | None = None
    host: str = "db.example.com"
    port: int = 5432
    user: str = "app_user"
    password: str | None = None
    name: str = "my_database"
    engine: str = "tortoise.backends.asyncpg"


class ApiConfig(BaseModel):
    """
    Configuration settings for the API server.

    Attributes:
        host (str): The host address for the API server.
        port (int): The port number for the API server.
    """

    host: str = "0.0.0.0"  # noqa: S104
    port: int = 8000


class BackendConfig(BaseModel):
    """
    Overall backend application configuration.

    Attributes:
        logger (LoggerConfig): Configuration settings for the application
        logger.
        database (DatabaseConfig): Configuration settings for the database
        connection.
        api (ApiConfig): Configuration settings for the API server.
    """

    logger: LoggerConfig = Field(default_factory=LoggerConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)


class MainConfig(BaseModel):
    """
    Main application configuration model.

    This class defines the structure of the application's configuration.
    It is populated manually from YAML and .env files for full control.

    Attributes:
        frontend (FrontendConfig): Frontend specific settings.
        backend (BackendConfig): Backend specific settings, including logger,
        database, and API.
    """

    frontend: FrontendConfig = Field(default_factory=FrontendConfig)
    backend: BackendConfig = Field(default_factory=BackendConfig)
