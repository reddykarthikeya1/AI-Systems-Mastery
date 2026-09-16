# Module 07: Troubleshooting, File Traps & Serialization Edge Cases

This reference guide details common errors and security vulnerabilities encountered when handling files and data serialization in Python.

---

## 1. The Windows `UnicodeDecodeError` / `cp1252` Trap

### The Bug
```python
# On Windows, open() defaults to 'cp1252' instead of UTF-8:
with open("readme.txt", "w") as f:
    f.write("Emoji: 🚀 and symbols: €")

with open("readme.txt", "r") as f:
    text = f.read()  # ❌ UnicodeDecodeError: 'charmap' codec can't decode byte...
```

### The Fix
**ALWAYS** explicitly declare `encoding="utf-8"` in both `open()` and `Path.read_text()` / `Path.write_text()`:
```python
with open("readme.txt", "w", encoding="utf-8") as f:
    f.write("Emoji: 🚀 and symbols: €")

with open("readme.txt", "r", encoding="utf-8") as f:
    text = f.read()  # ✅ Works cleanly on every OS!
```

---

## 2. The CSV Extra Blank Lines Bug on Windows

### The Bug
```python
import csv

# Opening without newline='' inserts an extra blank line between every row on Windows!
with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name"])
    writer.writerow([1, "Alice"])
```

### The Fix
Pass `newline=""` to `open()` whenever reading or writing CSV files:
```python
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name"])
    writer.writerow([1, "Alice"])
```

---

## 3. The `pickle` Remote Code Execution Hazard

### The Security Danger
Python's built-in `pickle` module allows arbitrary code execution during deserialization (`pickle.loads()`).
If an attacker sends a malicious pickled payload to your server, `pickle.loads()` will execute malicious shell commands!

### The Rule
* **NEVER** use `pickle` to receive data from untrusted networks, REST APIs, or user input.
* Use safe, standard interchange formats like **JSON**, **MessagePack**, or **Protocol Buffers** instead.

---

## 4. Half-Written Corrupted Files on Crash

### The Problem
If power is lost or your server crashes while writing a 50 MB JSON file, the destination file is left half-written and permanently corrupted.

### The Fix: Atomic Replacement
1. Write the new content to a temporary sibling file: `target.with_suffix(".tmp")`
2. Perform an atomic filesystem rename: `temp_file.replace(target)`
The operating system replaces the old file in a single atomic filesystem transaction.
