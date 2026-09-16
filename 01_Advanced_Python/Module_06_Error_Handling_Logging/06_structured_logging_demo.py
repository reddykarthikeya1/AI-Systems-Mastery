#!/usr/bin/env python3
"""Module 06: Structured Logging & Rotating File Handlers Demonstration.

This script demonstrates log levels, structured JSON formatters,
trace correlation IDs, and RotatingFileHandler.
"""

from __future__ import annotations

import json
import logging
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path


class JSONTraceFormatter(logging.Formatter):
    """Custom formatter outputting logs as JSON with trace correlation IDs."""

    def format(self, record: logging.LogRecord) -> str:
        trace_id = getattr(record, "trace_id", "N/A")
        log_payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "trace_id": trace_id,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_payload)


def setup_logger(log_file: Path) -> logging.Logger:
    """Configures a logger with both console and rotating file handlers."""
    logger = logging.getLogger("enterprise_app")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    # 1. Console Handler (Standard Text)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(console)

    # 2. Rotating File Handler (JSON Format, 1 MB max size, 2 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=2, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JSONTraceFormatter())
    logger.addHandler(file_handler)

    return logger


def main() -> None:
    print("=" * 60)
    print("  Enterprise Structured Logging Demonstration")
    print("=" * 60)

    log_path = Path("app_audit.log")
    logger = setup_logger(log_path)

    # Generate a unique distributed trace ID
    request_trace_id = str(uuid.uuid4())[:8]

    print(f"\nEmitting log events with Trace ID: {request_trace_id}")
    logger.info("Incoming HTTP POST /orders/checkout", extra={"trace_id": request_trace_id})
    logger.debug("Validating payload headers and HMAC signature", extra={"trace_id": request_trace_id})
    logger.warning("Database response took 450ms (threshold: 200ms)", extra={"trace_id": request_trace_id})
    logger.error("Payment decline response from gateway", extra={"trace_id": request_trace_id})

    print("\n--- Recent JSON Lines from Log File ---")
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines()[-4:]:
            print(line)
        logging.shutdown()  # Closes open file handles on Windows
        log_path.unlink(missing_ok=True)  # Clean up scratch file


if __name__ == "__main__":
    main()
