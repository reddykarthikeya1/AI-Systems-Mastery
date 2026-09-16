"""Module 08: Mocking and Patching Demonstration.

Run with: pytest 02_mocking_and_patching_demo.py -v
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest


class NotificationClient:
    """Simulates third-party email/SMS provider."""
    def send_sms(self, phone_number: str, message: str) -> bool:
        # In real life, connects to Twilio API
        raise ConnectionError("Live Twilio endpoint cannot be reached in unit tests!")


def notify_user_of_order(client: NotificationClient, phone: str, order_id: str) -> bool:
    """Business logic sending order notification."""
    return client.send_sms(phone, f"Your order #{order_id} has shipped!")


def test_notify_user_with_mock() -> None:
    """Test notification workflow using a MagicMock stunt double."""
    mock_client = MagicMock(spec=NotificationClient)
    mock_client.send_sms.return_value = True

    result = notify_user_of_order(mock_client, "+15550199", "ORD-101")
    assert result is True
    mock_client.send_sms.assert_called_once_with("+15550199", "Your order #ORD-101 has shipped!")


def test_notify_user_failure_handling() -> None:
    """Test how service handles third-party provider failure using side_effect."""
    mock_client = MagicMock(spec=NotificationClient)
    mock_client.send_sms.side_effect = TimeoutError("Twilio API timeout")

    with pytest.raises(TimeoutError):
        notify_user_of_order(mock_client, "+15550199", "ORD-101")
