import os
from functools import lru_cache
from typing import Any

import yaml
from dotenv import load_dotenv

from .config import MainConfig, get_config_path


@lru_cache
def get_main_config() -> MainConfig:
    """
    Returns a cached instance of the MainConfig settings.

    It manually loads settings in a controlled order of priority:
    1. Values from the YAML file.
    2. Values from the .env file and other environment variables, which override YAML.

    Returns:
        MainConfig: The application's configuration settings.
    """
    yaml_config = _load_yaml_config()
    _override_from_env_file()
    _override_from_env_variables(yaml_config)

    return MainConfig.model_validate(yaml_config)


def _load_yaml_config() -> dict[str, Any]:
    """
    Load the configuration from the YAML file.
    """
    yaml_path = get_config_path("config.yaml")
    if not yaml_path.exists():
        msg = f"Configuration file not found: {yaml_path}"
        raise FileNotFoundError(msg)

    with yaml_path.open(encoding="utf-8") as f:
        config_data: dict[str, Any] = yaml.safe_load(f) or {}
    return config_data


def _override_from_env_file() -> None:
    """
    Override the config with environment variables from the .env file.
    """
    env_path = get_config_path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)


def _override_from_env_variables(yaml_config: dict[str, Any]) -> None:
    """
    Override the config with environment variables.

    Args:
        yaml_config (dict[str, Any]): The base configuration dictionary.
    """
    for key, value in os.environ.items():
        # Traverse the config dict using the '__' delimiter
        keys = key.lower().split("__")
        d = yaml_config
        for k in keys[:-1]:
            if k in d and isinstance(d.get(k), dict):
                d = d[k]
            else:
                d = None
                break
        if d and keys[-1] in d:
            d[keys[-1]] = value


__all__ = ["get_main_config"]
