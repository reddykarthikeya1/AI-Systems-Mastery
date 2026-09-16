# Module_07_Files_Data_Formats_Serialization: Project Implementation Guide

**Deliverable:** a high-reliability file processing engine migrating configuration and data between JSON, TOML, CSV, and binary formats with atomic file guarantees.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_config_migrator.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Atomic File Writer
Implement `atomic_write(target_path, content, encoding='utf-8')` writing to a temporary file before renaming via `os.replace`.

### Step 2 — Format Parsers & Exporters
Implement `load_config` and `export_config` supporting JSON and TOML with full UTF-8 encoding support.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_config_migrator.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Tabular CSV Exporter
Implement CSV serialization and deserialization handling quoted fields, commas, and newlines.

### Step 4 — Safe Datetime Serialization
Serialize ISO-8601 UTC timestamps losslessly across format migrations.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/config_migrator.py`, remove the temporary file staging in `atomic_write` and write directly to `target_path`.
Run:
```bash
pytest ../project_solution/test_config_migrator.py -k test_atomic_write_crash_resilience -v
```
Watch the test verify that an aborted write leaves the original file corrupted, then restore atomic staging.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_config_migrator.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Binary Protocol Buffers / MessagePack:** Add support for binary MessagePack serialization.
2. **Schema Validation on Load:** Integrate Pydantic or jsonschema validation before accepting migrated files.
3. **Directory Batch Migrator:** Migrate an entire directory of mixed format files concurrently.
4. **File Locking:** Implement cross-platform advisory file locking (`fcntl` / `msvcrt`) to prevent race conditions.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_atomic_write_creates_file` | Proves atomic file writes produce valid files on disk |
| `test_utf8_encoding_preserves_special_chars` | Proves international characters and emojis round-trip without corruption |
| `test_json_and_toml_migration` | Proves data structures migrate losslessly between JSON and TOML |
| `test_csv_export_and_import` | Proves tabular data exports and re-imports with matching types |
| `test_missing_file_raises_not_found` | Proves non-existent file reads raise FileNotFoundError cleanly |

---

## 🎓 You have mastered this module when you can…

- [ ] Always specify explicit encoding='utf-8' on all file I/O operations
- [ ] Implement atomic file write patterns using staging files and os.replace
- [ ] Parse and serialize JSON, TOML, and CSV formats accurately
- [ ] Handle JSON key stringification traps when serializing integer dictionary keys
- [ ] Round-trip datetime objects cleanly using ISO-8601 formatting
- [ ] Navigate and manipulate directory trees using pathlib.Path
- [ ] Write unit tests verifying file contents and crash resilience
