from functools import lru_cache

from .config import MainConfig


@lru_cache
def get_main_config() -> MainConfig:
    """
    Returns a cached instance of the MainConfig settings.

    Using lru_cache ensures that the settings are loaded from files
    and environment variables only once.

    Returns:
        MainConfig: The application's configuration settings.
    """
    return MainConfig()


__all__ = ["get_main_config"]
