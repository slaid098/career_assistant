from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from src.utils.notify_logger.config import TelegramHandlerConfig
from src.utils.notify_logger.handlers import TelegramHandler
from src.utils.notify_logger.logger import NotifyLogger


@pytest.mark.unittest
def test_logger_initialization() -> None:
    """
    Tests that the logger is initialized correctly.
    """
    logger = NotifyLogger()
    assert logger is not None, "Logger should be a singleton instance"
    assert hasattr(logger, "info"), "Logger should have an info method"


@pytest.mark.unittest
def test_telegram_handler_with_notify_flag(mocker: MockerFixture) -> None:
    """
    Tests that the Telegram handler correctly uses the 'notify' flag.

    It verifies that the Telegram bot's send_message method is called only
    when a log record has `extra['notify']` set to True.

    Args:
        mocker: The pytest-mock fixture.
    """
    # 0. Create a fresh logger instance for the test
    logger = NotifyLogger()

    # 1. Mock the TeleBot class at the point of its usage in handlers.py
    mock_telebot_class = mocker.patch("src.utils.notify_logger.handlers.TeleBot")
    mock_bot_instance = MagicMock()
    mock_telebot_class.return_value = mock_bot_instance

    # 2. Configure and create an instance of our TelegramHandler
    test_config = TelegramHandlerConfig(
        bot_token="fake_token",  # noqa: S106
        admin_ids=[123],
        level="INFO",
    )
    telegram_handler = TelegramHandler(test_config)

    # 3. Setup the logger with our handler
    logger.setup(handlers=[telegram_handler], level="INFO")

    # 4. Log two messages, one with notify=True, one with notify=False
    logger.info("This message should be sent to Telegram.", notify=True)
    logger.warning("This message should NOT be sent.", notify=False)
    logger.error("This one also should be sent.", notify=True)

    # 5. Assert that send_message was called exactly twice
    call_count = 2
    assert mock_bot_instance.send_message.call_count == call_count, (
        "send_message should be called twice for logs with notify=True"
    )

    # 6. Optional: Check the content of the calls
    first_call_args = mock_bot_instance.send_message.call_args_list[0].args
    assert "This message should be sent" in first_call_args[1]

    second_call_args = mock_bot_instance.send_message.call_args_list[1].args
    assert "This one also should be sent" in second_call_args[1]
