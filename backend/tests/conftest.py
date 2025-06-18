from collections.abc import AsyncGenerator

import pytest_asyncio

from src.config.config import DatabaseConfig
from src.db.db import close_db, init_db

_MODELS_FILES = [
    "src.db.models.job",
    "aerich.models",
]


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db_init() -> AsyncGenerator[None, None]:
    """
    Fixture to initialize the test database before each test.

    This fixture creates an in-memory SQLite database, initializes
    Tortoise ORM using the centralized `init_db` function, and then closes
    the connection after the test completes.

    Yields:
        None
    """
    db_config = DatabaseConfig(
        url="sqlite://:memory:",
        engine="tortoise.backends.sqlite",
    )
    await init_db(db_config)
    yield
    await close_db()
