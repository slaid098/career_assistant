from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise  # type: ignore[reportUnknownReturnType]

from src.api.v1.endpoints import jobs
from src.config import get_main_config
from src.db.config import get_tortoise_orm_config
from src.utils.notify_logger.logger import NotifyLogger

settings = get_main_config()


# Определяем список файлов моделей для Tortoise ORM
_MODELS_FILES = [
    "src.db.models.job",
]

# Получаем конфигурацию Tortoise ORM
TORTOISE_ORM_CONFIG = get_tortoise_orm_config(
    db_config=settings.backend.database,
    models_files=_MODELS_FILES,
)

logger = NotifyLogger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Контекстный менеджер для управления жизненным циклом приложения.
    Инициализирует подключение к базе данных при старте и закрывает при завершении.
    """
    logger.info("Starting up application...")
    register_tortoise(
        app,
        config=TORTOISE_ORM_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    logger.info("Database connection established.")
    yield
    logger.info("Shutting down application...")
    # Tortoise-ORM автоматически закроет соединение при выключении приложения
    logger.info("Database connection closed.")


def create_app() -> FastAPI:
    """
    Создает и настраивает приложение FastAPI.

    Returns:
        FastAPI: Экземпляр приложения FastAPI.
    """
    app = FastAPI(
        title="Career Assistant API",
        description="API для проекта Career Assistant, предоставляющий информацию о вакансиях.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.backend.api.host, port=settings.backend.api.port)
