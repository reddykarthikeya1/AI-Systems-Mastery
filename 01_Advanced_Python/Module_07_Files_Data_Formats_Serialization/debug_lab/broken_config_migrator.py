#!/usr/bin/env python3
"""Broken Serialization Migrator demonstrating encoding, JSON keys, and datetime traps."""

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

def save_and_read_unicode_config(tmp_dir: Path):
    target = tmp_dir / "unicode_config.txt"
    with open(target, "w") as f:
        f.write("Server Name: €_Trading_Node_☂")

    with open(target, "r") as f:
        return f.read()

def roundtrip_portfolio_keys():
    portfolio = {101: "Tech", 102: "Energy"}
    serialized = json.dumps(portfolio)
    deserialized = json.loads(serialized)
    return deserialized

def parse_and_compare_timestamp():
    utc_now = datetime.now(timezone.utc)
    naive_parsed = datetime.fromisoformat("2026-09-01T12:00:00")
    return naive_parsed > utc_now

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        try:
            val = save_and_read_unicode_config(Path(td))
            print(f"Unicode config read: {val}")
        except UnicodeError as err:
            print(f"Unicode encoding crashed: {err}")

    res = roundtrip_portfolio_keys()
    print(f"Key 101 in deserialized: {101 in res} (Expected True, got False because keys became strings!)")

    try:
        parse_and_compare_timestamp()
    except TypeError as err:
        print(f"Datetime comparison crashed: {err}")
