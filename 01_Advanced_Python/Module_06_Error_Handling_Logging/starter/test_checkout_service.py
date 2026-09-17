"""Unit tests for the Enterprise Checkout Service."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest
from checkout_service import (
    CheckoutError,
    CheckoutService,
    JSONTraceFormatter,
    OutOfStockError,
    PaymentDeclinedError,
    PaymentGatewayError,
    configure_checkout_logger,
)


@pytest.fixture
def checkout_service() -> CheckoutService:
    logger = logging.getLogger("test_checkout")
    logger.setLevel(logging.CRITICAL)  # Silence console during tests
    return CheckoutService(logger)


def test_successful_checkout(checkout_service: CheckoutService) -> None:
    """Test successful order execution."""
    result = checkout_service.process_order(
        customer_id="CUST-1",
        item_id="LAPTOP-01",
        quantity=2,
        payment_token="tok_valid",
    )
    assert result["status"] == "SUCCESS"
    assert result["item_id"] == "LAPTOP-01"
    assert result["quantity"] == 2
    assert "trace_id" in result


def test_out_of_stock_exception(checkout_service: CheckoutService) -> None:
    """Test out of stock error includes trace ID and inventory details."""
    with pytest.raises(OutOfStockError) as exc_info:
        checkout_service.process_order("CUST-2", "DESK-03", 1, "tok_valid")

    err = exc_info.value
    assert err.item_id == "DESK-03"
    assert err.requested == 1
    assert err.available == 0
    assert err.trace_id.startswith("tr_")


def test_payment_timeout_chaining(checkout_service: CheckoutService) -> None:
    """Test that payment gateway timeout properly chains root TimeoutError."""
    with pytest.raises(PaymentGatewayError) as exc_info:
        checkout_service.process_order("CUST-3", "LAPTOP-01", 1, "tok_timeout")

    err = exc_info.value
    assert isinstance(err.__cause__, TimeoutError)


def test_payment_declined_error(checkout_service: CheckoutService) -> None:
    """Test card declined error."""
    with pytest.raises(PaymentDeclinedError):
        checkout_service.process_order("CUST-4", "LAPTOP-01", 1, "tok_declined")


def test_order_inventory_deduction(checkout_service: CheckoutService) -> None:
    """Test successful order deducts stock from inventory."""
    initial_stock = checkout_service._inventory["LAPTOP-01"]
    res = checkout_service.process_order("CUST-DEDUCT", "LAPTOP-01", 2, "tok_valid")
    assert res["status"] == "SUCCESS"
    assert checkout_service._inventory["LAPTOP-01"] == initial_stock - 2


def test_order_trace_id_uniqueness(checkout_service: CheckoutService) -> None:
    """Test each order generates a unique trace ID."""
    r1 = checkout_service.process_order("CUST-A", "LAPTOP-01", 1, "tok_valid")
    r2 = checkout_service.process_order("CUST-B", "LAPTOP-01", 1, "tok_valid")
    assert r1["trace_id"] != r2["trace_id"]


def test_exception_hierarchy_inheritance() -> None:
    """Test all checkout exceptions inherit from CheckoutError base."""
    assert issubclass(OutOfStockError, CheckoutError)
    assert issubclass(PaymentGatewayError, CheckoutError)
    assert issubclass(PaymentDeclinedError, CheckoutError)


def test_json_trace_formatter_structure() -> None:
    """Test JSONTraceFormatter structures record into valid JSON payload."""
    import json
    formatter = JSONTraceFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Transaction confirmed",
        args=(),
        exc_info=None,
    )
    record.trace_id = "tr_abc123"
    formatted = formatter.format(record)
    parsed = json.loads(formatted)
    assert parsed["level"] == "INFO"
    assert parsed["trace_id"] == "tr_abc123"
    assert parsed["message"] == "Transaction confirmed"


def test_configure_checkout_logger_with_file(tmp_path: Path) -> None:
    """Test configure_checkout_logger adds rotating file handler."""
    log_file = tmp_path / "checkout.log"
    logger = configure_checkout_logger(log_file)
    assert len(logger.handlers) >= 2
    logger.info("Test message to file")
    assert log_file.exists()


def test_consecutive_orders_depleting_inventory(checkout_service: CheckoutService) -> None:
    """Test multiple orders depleting stock until OutOfStockError triggers."""
    checkout_service._inventory["MOUSE-02"] = 2
    checkout_service.process_order("CUST-1", "MOUSE-02", 2, "tok_valid")
    with pytest.raises(OutOfStockError):
        checkout_service.process_order("CUST-2", "MOUSE-02", 1, "tok_valid")
