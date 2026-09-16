#!/usr/bin/env python3
"""Module 07: JSON, CSV & TOML Serialization Demonstration.

This script demonstrates multi-format serialization across JSON, CSV (DictWriter),
and TOML (tomllib in Python 3.11+).
"""

from __future__ import annotations

import csv
import io
import json
import tomllib
from datetime import UTC, datetime
from decimal import Decimal


class CustomJSONEncoder(json.JSONEncoder):
    """Encodes datetime and Decimal types into clean JSON representations."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def demo_json_serialization() -> None:
    print("=" * 60)
    print("  1. Custom JSON Serialization (datetime & Decimal)")
    print("=" * 60)

    dataset = {
        "invoice_id": "INV-2026-001",
        "created_at": datetime.now(UTC),
        "total_amount": Decimal("1450.75"),
        "is_paid": True,
    }
    json_str = json.dumps(dataset, cls=CustomJSONEncoder, indent=2)
    print(f"JSON Result:\n{json_str}")


def demo_csv_dictwriter() -> None:
    print("\n" + "=" * 60)
    print("  2. CSV Tabular Serialization with csv.DictWriter")
    print("=" * 60)

    buffer = io.StringIO()
    fieldnames = ["id", "username", "role", "active"]

    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerow({"id": 1, "username": "alice", "role": "admin", "active": True})
    writer.writerow({"id": 2, "username": "bob", "role": "developer", "active": False})

    print(f"CSV Result:\n{buffer.getvalue()}")


def demo_toml_parsing() -> None:
    print("=" * 60)
    print("  3. TOML Parsing with Standard Library 'tomllib' (Python 3.11+)")
    print("=" * 60)

    toml_content = """
    [server]
    host = "0.0.0.0"
    port = 8080
    workers = 4

    [database]
    url = "postgresql://user:pass@localhost:5432/production"
    max_connections = 25
    """

    parsed_config = tomllib.loads(toml_content)
    print(f"Parsed Config Dict:\n  {parsed_config}")
    print(f"Server Port: {parsed_config['server']['port']}")


def main() -> None:
    demo_json_serialization()
    demo_csv_dictwriter()
    demo_toml_parsing()


if __name__ == "__main__":
    main()
