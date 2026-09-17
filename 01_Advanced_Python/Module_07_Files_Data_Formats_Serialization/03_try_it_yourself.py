"""Beginner playground for Module 07 - Files, Data Formats & Serialization.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import csv
import io
import json

# -------------------------------------------- 1. JSON Serialization and Deserialization
payload = {"service": "gateway", "ports": [80, 443], "active": True}
serialized = json.dumps(payload, sort_keys=True)
deserialized = json.loads(serialized)
assert deserialized == payload
assert deserialized["ports"] == [80, 443]
print(f"Serialized JSON payload length: {len(serialized)} bytes")

# -------------------------------------------- 2. CSV Parsing with DictReader
csv_content = "id,name,score\n1,Alice,95\n2,Bob,88\n"
buffer = io.StringIO(csv_content)
reader = csv.DictReader(buffer)
rows = list(reader)
assert len(rows) == 2
assert rows[0]["name"] == "Alice"
assert int(rows[1]["score"]) == 88
print(f"Parsed {len(rows)} CSV records from stream.")

# -------------------------------------------- 3. Binary Data Streaming with BytesIO
raw_stream = io.BytesIO()
raw_stream.write(b"HEADER_V1")
raw_stream.write(b"PAYLOAD_DATA")
raw_stream.seek(0)
data = raw_stream.read()
assert data == b"HEADER_V1PAYLOAD_DATA"
assert len(data) == 21
print(f"Read {len(data)} bytes from binary stream.")

print()
print("All checks passed.")
