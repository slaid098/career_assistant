from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.config import get_main_config

get_main_config.cache_clear()

TEST_PORT = 8000
ENV_BACKEND_DATABASE_HOST = "BACKEND__DATABASE__HOST"
ENV_BACKEND_API_PORT = "BACKEND__API__PORT"


@pytest.fixture
def mock_config_files(tmp_path: Path, monkeypatch: MonkeyPatch) -> Path:
    """
    Fixture to create temporary config files and mock get_config_path.
    """
    yaml_content = f"""
    backend:
      api:
        host: "0.0.0.0"
        port: {TEST_PORT}
      database:
        host: "yaml_db_host"
        port: 5432
    """
    env_file_content = f'{ENV_BACKEND_DATABASE_HOST}="env_db_host"'

    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text(yaml_content)

    env_file = tmp_path / ".env"
    env_file.write_text(env_file_content)

    def mock_get_path(file_name: str) -> Path:
        return tmp_path / file_name

    monkeypatch.setattr("src.config.get_config_path", mock_get_path)

    get_main_config.cache_clear()
    return tmp_path


def test_load_from_yaml(mock_config_files: Path, monkeypatch: MonkeyPatch) -> None:
    """
    Tests that configuration is correctly loaded from the YAML file.
    """

    # delete system environment variables
    monkeypatch.delenv(ENV_BACKEND_DATABASE_HOST, raising=False)
    monkeypatch.delenv(ENV_BACKEND_API_PORT, raising=False)

    (mock_config_files / ".env").unlink()

    config = get_main_config()

    assert config.backend.api.port == TEST_PORT
    assert config.backend.database.host == "yaml_db_host"


def test_override_from_env_file(mock_config_files: Path, monkeypatch: MonkeyPatch) -> None:  # noqa: ARG001
    """
    Tests that .env variables override YAML configuration.
    """
    monkeypatch.delenv(ENV_BACKEND_DATABASE_HOST, raising=False)
    config = get_main_config()
    assert config.backend.database.host == "env_db_host"


def test_override_from_system_env(mock_config_files: Path, monkeypatch: MonkeyPatch) -> None:  # noqa: ARG001
    """
    Tests that system environment variables override both .env and YAML.
    """
    test_db_host = "system_env_db_host"
    test_port = 9999
    monkeypatch.setenv(ENV_BACKEND_DATABASE_HOST, test_db_host)
    monkeypatch.setenv(ENV_BACKEND_API_PORT, str(test_port))

    config = get_main_config()

    assert config.backend.database.host == test_db_host
    assert config.backend.api.port == test_port


def test_yaml_not_found_raises_error(mock_config_files: Path) -> None:
    """
    Tests that a FileNotFoundError is raised if config.yaml is missing.
    """
    (mock_config_files / "config.yaml").unlink()

    with pytest.raises(FileNotFoundError):
        get_main_config()


@patch("src.config._load_yaml_config")
def test_get_main_config_is_cached(mock_load_yaml: MagicMock) -> None:
    """
    Tests that the get_main_config function is cached.
    """
    with patch("src.config.get_config_path"):
        mock_load_yaml.return_value = {}

        for _ in range(3):
            get_main_config()

        mock_load_yaml.assert_called_once()
