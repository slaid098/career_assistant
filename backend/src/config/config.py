from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings

# from src.utils.notify_logger.config import LoggerConfig


def get_base_dir() -> Path:
    """
    Get the base directory of the project.

    Returns:
        Path: The base directory of the project.
    """

    current_dir = Path(__file__).resolve()
    while (
        current_dir.parent != current_dir
        and not (current_dir / "config.yaml").exists()
    ):
        current_dir = current_dir.parent
    return current_dir


BASE_DIR = get_base_dir()


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

    # logger: LoggerConfig = Field(default_factory=LoggerConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)


class MainConfig(YamlBaseSettings):
    """
    Main application configuration.

    This class loads application settings from `config.yaml` and `.env` files.
    It uses Pydantic-settings to manage hierarchical configuration.

    Attributes:
        frontend (FrontendConfig): Frontend specific settings.
        backend (BackendConfig): Backend specific settings, including logger,
        database, and API.
    """

    model_config = SettingsConfigDict(
        # Загружаем статический YAML из корня проекта
        yaml_file=BASE_DIR / "config.yaml",
        yaml_file_encoding="utf-8",
        # Затем загружаем .env из корня проекта (для секретов)
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        # Общий префикс для переменных окружения приложения
        env_prefix="APP_",
        env_nested_delimiter="__",
    )

    frontend: FrontendConfig = Field(default_factory=FrontendConfig)
    backend: BackendConfig = Field(default_factory=BackendConfig)
