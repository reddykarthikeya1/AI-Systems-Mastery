# 🐣 Interactive Foundations Playground: Files, Data Formats & Serialization

> *"Reliable systems serialize structured state without data loss or corruption."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import csv
import io
import json
```

---

## 1. JSON Serialization and Deserialization

`json` converts nested dictionaries to standards-compliant string payloads and back.

```python
payload = {"service": "gateway", "ports": [80, 443], "active": True}
serialized = json.dumps(payload, sort_keys=True)
deserialized = json.loads(serialized)
assert deserialized == payload
assert deserialized["ports"] == [80, 443]
print(f"Serialized JSON payload length: {len(serialized)} bytes")
```

---

## 2. CSV Parsing with DictReader

In-memory string buffers (`io.StringIO`) allow testing CSV pipelines without disk I/O.

```python
csv_content = "id,name,score\n1,Alice,95\n2,Bob,88\n"
buffer = io.StringIO(csv_content)
reader = csv.DictReader(buffer)
rows = list(reader)
assert len(rows) == 2
assert rows[0]["name"] == "Alice"
assert int(rows[1]["score"]) == 88
print(f"Parsed {len(rows)} CSV records from stream.")
```

---

## 3. Binary Data Streaming with BytesIO

`io.BytesIO` provides binary streaming buffers for handling raw serialized bytes.

```python
raw_stream = io.BytesIO()
raw_stream.write(b"HEADER_V1")
raw_stream.write(b"PAYLOAD_DATA")
raw_stream.seek(0)
data = raw_stream.read()
assert data == b"HEADER_V1PAYLOAD_DATA"
assert len(data) == 21
print(f"Read {len(data)} bytes from binary stream.")
```

---
