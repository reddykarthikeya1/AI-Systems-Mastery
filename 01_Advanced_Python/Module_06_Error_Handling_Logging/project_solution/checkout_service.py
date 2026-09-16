#!/usr/bin/env python3
"""Enterprise E-Commerce Checkout Service.

Module 06 Turnkey Project Implementation.
Demonstrates Custom Exceptions, Exception Chaining, and Structured JSON Logging.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

# ==========================================
# 1. Custom Domain Exception Hierarchy
# ==========================================

class CheckoutError(Exception):
    """Base exception for all checkout-related failures."""
    def __init__(self, message: str, trace_id: str) -> None:
        super().__init__(message)
        self.message = message
        self.trace_id = trace_id


class OutOfStockError(CheckoutError):
    """Raised when an item does not have sufficient inventory."""
    def __init__(self, item_id: str, requested: int, available: int, trace_id: str) -> None:
        msg = f"Item '{item_id}' out of stock (Requested: {requested}, Available: {available})"
        super().__init__(msg, trace_id)
        self.item_id = item_id
        self.requested = requested
        self.available = available


class PaymentGatewayError(CheckoutError):
    """Raised when the third-party payment gateway fails."""
    pass


class PaymentDeclinedError(CheckoutError):
    """Raised when card authorization is rejected."""
    pass


# ==========================================
# 2. Structured JSON Logging Architecture
# ==========================================

class JSONTraceFormatter(logging.Formatter):
    """Formats LogRecords into structured JSON payloads with trace correlation."""

    def format(self, record: logging.LogRecord) -> str:
        trace_id = getattr(record, "trace_id", "NO_TRACE")
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "trace_id": trace_id,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_checkout_logger(log_file: Path | None = None) -> logging.Logger:
    """Configures structured logger with console and optional rotating file handler."""
    logger = logging.getLogger("checkout_service")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] (%(name)s) %(message)s"))
    logger.addHandler(console_handler)

    # Optional Rotating File Handler
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=2, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(JSONTraceFormatter())
        logger.addHandler(file_handler)

    return logger


# ==========================================
# 3. Checkout Service Engine
# ==========================================

class CheckoutService:
    """Handles end-to-end order processing with inventory reservation and payments."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self._inventory: dict[str, int] = {
            "LAPTOP-01": 10,
            "MOUSE-02": 2,
            "DESK-03": 0,
        }

    def process_order(
        self,
        customer_id: str,
        item_id: str,
        quantity: int,
        payment_token: str,
    ) -> dict[str, Any]:
        """Executes full order workflow, logging all steps and catching domain errors."""
        trace_id = f"tr_{uuid.uuid4().hex[:8]}"
        extra_ctx = {"trace_id": trace_id}

        self.logger.info(
            f"Initiating checkout for customer '{customer_id}': item={item_id}, qty={quantity}",
            extra=extra_ctx,
        )

        # Stage 1: Inventory Check & Deduction
        available = self._inventory.get(item_id, 0)
        if available < quantity:
            self.logger.warning(
                f"Inventory check failed for item '{item_id}'. Required: {quantity}, Available: {available}",
                extra=extra_ctx,
            )
            raise OutOfStockError(item_id, requested=quantity, available=available, trace_id=trace_id)

        # Stage 2: Payment Authorization Simulation
        try:
            self._authorize_payment(payment_token, amount=quantity * 99.99, trace_id=trace_id)
        except TimeoutError as timeout_err:
            self.logger.error("Payment gateway timed out during processing", extra=extra_ctx)
            raise PaymentGatewayError("Payment provider unreachable", trace_id=trace_id) from timeout_err
        except PermissionError as decl_err:
            self.logger.warning("Card issuer declined transaction", extra=extra_ctx)
            raise PaymentDeclinedError("Card declined: Insufficient credit", trace_id=trace_id) from decl_err

        # Stage 3: Deduct Inventory and Finalize
        self._inventory[item_id] -= quantity
        self.logger.info(
            f"Checkout completed successfully for customer '{customer_id}'. Order placed!",
            extra=extra_ctx,
        )

        return {
            "status": "SUCCESS",
            "order_id": f"ORD-{int(time.time())}",
            "trace_id": trace_id,
            "item_id": item_id,
            "quantity": quantity,
        }

    def _authorize_payment(self, token: str, amount: float, trace_id: str) -> bool:
        """Simulates external payment gateway communication."""
        if token == "tok_timeout":
            raise TimeoutError("Gateway socket connection hung")
        if token == "tok_declined":
            raise PermissionError("Issuer rejected charge")
        return True


def main() -> None:
    print("=" * 65)
    print("      ENTERPRISE CHECKOUT SERVICE SIMULATION")
    print("=" * 65)

    log_path = Path("checkout_audit.log")
    logger = configure_checkout_logger(log_path)
    service = CheckoutService(logger)

    print("\n1. Successful Checkout:")
    order = service.process_order("CUST-101", "LAPTOP-01", 1, "tok_valid")
    print(f"Result: {order}")

    print("\n2. Out-of-Stock Checkout:")
    try:
        service.process_order("CUST-102", "DESK-03", 1, "tok_valid")
    except OutOfStockError as e:
        print(f"[CAUGHT DOMAIN ERROR]: {e} (Trace ID: {e.trace_id})")

    print("\n3. Payment Timeout with Exception Chaining:")
    try:
        service.process_order("CUST-103", "LAPTOP-01", 1, "tok_timeout")
    except PaymentGatewayError as e:
        print(f"[CAUGHT DOMAIN ERROR]: {e} (Root cause: {e.__cause__})")

    if log_path.exists():
        log_path.unlink()  # Clean up test log


if __name__ == "__main__":
    main()
