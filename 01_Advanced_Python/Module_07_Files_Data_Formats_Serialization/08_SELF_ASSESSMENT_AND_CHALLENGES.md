# Module 07: Self-Assessment Quiz & Mastery Challenges

Test your understanding of file I/O, `pathlib`, JSON/CSV/TOML serialization, and binary packing before moving to **Module 08**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Stream Modes:** What is the technical difference between opening a file in text mode (`"r"`) versus binary mode (`"rb"`)?
2. **Encoding Traps:** Why does failing to specify `encoding="utf-8"` on Windows frequently result in `UnicodeDecodeError` when emojis or European currency symbols (€) are present?
3. **Path Composition:** In `pathlib.Path`, how do you join directory paths using modern pythonic operator overloading?
4. **JSON Limitations:** Why does `json.dumps({"now": datetime.now()})` raise a `TypeError`, and how do you fix it?
5. **CSV Invariants:** Why must you pass `newline=""` when opening a file for `csv.writer` or `csv.DictWriter` on Windows?
6. **Modern TOML:** Which Python standard library module was introduced in Python 3.11 to natively parse `.toml` configuration files?
7. **Security Vulnerabilities:** Why is loading data with `pickle.loads(untrusted_bytes)` a critical remote code execution vulnerability?
8. **Crash Safety:** How does writing to a temporary file and calling `temp_path.replace(target_path)` guarantee atomic crash-safe persistence?
9. **Binary Packing:** In the `struct` format string `">Id"`, what do the characters `>`, `I`, and `d` represent?
10. **Directory Scanning:** What method on a `pathlib.Path` object allows you to search for all `.py` files recursively inside all subdirectories?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- Text mode (`"r"`) decodes raw bytes into Python `str` characters using an encoding (like UTF-8) and translates OS newline characters (`\r\n` $\rightarrow$ `\n`).
- Binary mode (`"rb"`) reads raw, uninterpreted `bytes` without decoding or altering byte sequences.

#### Answer 2:
Windows historically uses localized legacy code pages (like `cp1252` or `charmap`) as its default encoding rather than UTF-8. UTF-8 multi-byte characters cannot be decoded by legacy single-byte tables, raising `UnicodeDecodeError`.

#### Answer 3:
Using the forward slash `/` operator: `full_path = Path("parent") / "child" / "file.txt"`.

#### Answer 4:
Standard JSON specification does not define a native Date/Time data type. Fix it by subclassing `json.JSONEncoder` and overriding `default(self, obj)` to return `obj.isoformat()`.

#### Answer 5:
The `csv` module manages its own newline termination internally (`\r\n`). If Python's default text file wrapper also translates `\n` to `\r\n`, Windows ends up with double carriage returns (`\r\r\n`), causing blank rows.

#### Answer 6:
**`tomllib`** (read-only TOML parser introduced in Python 3.11).

#### Answer 7:
The `pickle` protocol can serialize and execute arbitrary Python bytecode and callables (such as `os.system("rm -rf /")`) during unpickling.

#### Answer 8:
Filesystem renames are atomic single-step operations in modern operating systems (NTFS, ext4, APFS). The target file is never left half-written; it either remains 100% old version or becomes 100% new version.

#### Answer 9:
- `>`: Big-Endian network byte order.
- `I`: Unsigned 4-byte integer (32-bit).
- `d`: 8-byte floating point double (64-bit IEEE 754).

#### Answer 10:
**`Path.rglob("*.py")`** (or `Path.glob("**/*.py")`).

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Atomic JSON Storage Helper

**Goal:** Write a function `atomic_save_json(filepath: Path, data: dict) -> None` that safely saves a dictionary to a JSON file using atomic replacement.

<details>
<summary><b>Solution Code</b></summary>

```python
import json
from pathlib import Path

def atomic_save_json(filepath: Path, data: dict) -> None:
    temp_file = filepath.with_suffix(f"{filepath.suffix}.tmp")
    
    # 1. Write to temporary file
    temp_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    
    # 2. Atomic replacement
    temp_file.replace(filepath)

# Verification:
target = Path("safe_state.json")
atomic_save_json(target, {"status": "ACTIVE", "port": 8000})
print("Saved content:", target.read_text(encoding="utf-8"))
target.unlink()  # Cleanup
```
</details>

---

### Challenge 2: CSV to JSON Converter CLI

**Goal:** Create a function `csv_to_json_file(csv_path: Path, json_path: Path) -> int` that reads a CSV spreadsheet and exports a JSON array of row objects, returning the total row count.

<details>
<summary><b>Solution Code</b></summary>

```python
import csv
import json
from pathlib import Path

def csv_to_json_file(csv_path: Path, json_path: Path) -> int:
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return len(rows)
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Missing encoding

```python
with open("config.json") as fh:
    data = fh.read()
```

**Observed symptom:** Works on the author's Linux machine. On a colleague's Windows machine: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d`.

**(a)** What encoding is used when you omit the parameter?

**(b)** What is the fix, and what is the belt-and-braces version?

**(c)** Why does the same file work on one machine and not another?

<details>
<summary><b>Show the diagnosis</b></summary>

`locale.getpreferredencoding(False)` — the **platform default**. On most Linux and macOS systems that is UTF-8; on Windows it has historically been a legacy code page such as cp1252.

**Fix:** always pass it — `open(path, encoding="utf-8")`. Belt-and-braces for files you did not produce: `encoding="utf-8", errors="replace"`, which substitutes a replacement character rather than raising — appropriate for logs, not for data you will write back.

**Machine-dependent** because nothing about the file changed; the *decoder* changed. This is the single most common cross-platform Python bug. PEP 686 makes UTF-8 the default in Python 3.15, and `PYTHONWARNDEFAULTENCODING=1` warns today — but explicit `encoding=` is correct on every version and should be unconditional.

</details>

---

### D2. JSON round-trip loses integer keys

```python
import json

original = {1: "one", 2: "two"}
restored = json.loads(json.dumps(original))
print(restored)
print(original == restored)
```

**Observed symptom:** Prints `{'1': 'one', '2': 'two'}` and `False`.

**(a)** Why did the keys change type?

**(b)** What are the two ways to preserve them?

**(c)** Name two other types that do not survive a JSON round-trip.

<details>
<summary><b>Show the diagnosis</b></summary>

The JSON specification requires object keys to be **strings**. `json.dumps` coerces silently rather than raising, so the information is lost at serialisation, not at parse.

**Two fixes:** convert back explicitly on load with `object_hook=lambda d: {int(k): v for k, v in d.items()}` (only safe if you know every key is an integer); or restructure to a list of `{"id": 1, "value": "one"}` objects, which is more portable and self-describing.

**Two others:** `tuple` becomes `list` (so `(1, 2) != [1, 2]` after a round trip), and `datetime` is not serialisable at all without a custom encoder — and a naive datetime loses its intended timezone regardless. Also: `set` is unsupported, `Decimal` becomes `float` and loses precision, and `NaN`/`Infinity` are emitted as non-standard JSON that other parsers reject.

</details>

---

### D3. Non-atomic file write

```python
import json

def save(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
```

**Observed symptom:** After a crash or a full disk, `config.json` exists but is truncated mid-object and will not parse. The previous good version is gone.

**(a)** Name the two independent failure modes.

**(b)** What is the atomic-write pattern?

**(c)** Why is `os.replace` the critical call rather than `os.rename`?

<details>
<summary><b>Show the diagnosis</b></summary>

**Two failures.** (1) `open(path, "w")` **truncates immediately**, so the old content is destroyed before the new content is written — a crash leaves nothing usable. (2) A reader can observe the file mid-write and read a partial document.

**Atomic write:** serialise to a temporary file *in the same directory*, `fh.flush()` then `os.fsync(fh.fileno())` to force it to disk, close it, then `os.replace(tmp, path)`. A reader sees either the complete old file or the complete new one, never a partial one.

**`os.replace` rather than `os.rename`** because `replace` is guaranteed to overwrite an existing destination atomically on **all** platforms; `os.rename` raises `FileExistsError` on Windows if the target exists. Same directory matters too: a rename across filesystems is a copy-and-delete and therefore not atomic. Module 07's `config_migrator` implements exactly this, and its tests assert the temporary file is cleaned up.

</details>

---

### D4. Pickle from an untrusted source

```python
import pickle, requests

payload = requests.get("https://api.partner.example/state").content
state = pickle.loads(payload)
```

**Observed symptom:** No error. Reviewed and merged. Later, the partner's endpoint is compromised and the server executes arbitrary commands.

**(a)** What does `pickle.loads` actually do?

**(b)** What should be used instead?

**(c)** When is pickle acceptable?

<details>
<summary><b>Show the diagnosis</b></summary>

Unpickling **executes** the byte stream: the format includes opcodes that call arbitrary callables via `__reduce__`. `pickle.loads` on untrusted input is remote code execution, full stop — not a hardening opportunity, not mitigable by validation afterwards, because the code has already run by then.

**Instead:** JSON for plain data, or a schema-validated format — Pydantic (Module 14), MessagePack, Protobuf, or Arrow. Any of these parse into data without invoking code.

**Pickle is acceptable** only for data you produced, that never crossed a trust boundary, and where you control both ends and the Python version — a local cache file, or `multiprocessing`'s internal transport. Even then note that pickle is not a stable format across versions. The rule is short: if you did not write the bytes, do not unpickle them. Module 20's `RedisBackend` defaults to JSON for this reason and documents the risk of its pickle option.

</details>

---

### D5. CSV without newline handling

```python
import csv

with open("out.csv", "w") as fh:
    writer = csv.writer(fh)
    writer.writerows([["a", "b"], ["c", "d"]])
```

**Observed symptom:** On Windows the file has a blank line between every row.

**(a)** Why the extra blank lines?

**(b)** What is the exact fix?

**(c)** What is the equivalent trap when reading?

<details>
<summary><b>Show the diagnosis</b></summary>

The `csv` module writes `\r\n` itself as the line terminator. In text mode with default newline translation, Python then converts the `\n` to `\r\n` again, producing `\r\r\n` — which most readers render as an empty row.

**Fix:** `open(path, "w", newline="", encoding="utf-8")`. The empty string disables newline translation and lets `csv` control line endings, which is exactly what the documentation requires.

**When reading**, the same `newline=""` is needed: without it, a quoted field containing an embedded newline gets translated, and the row is split in the wrong place — corrupting the data silently rather than visibly. So the rule is symmetric: **always** pass `newline=""` to any file handed to the `csv` module, in either direction.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
