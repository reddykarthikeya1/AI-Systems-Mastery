# Module_00_Environment_Tooling_Workflow: Project Implementation Guide

**Deliverable:** a fully configured, lint-clean, tested Python CLI package using modern pyproject.toml, ruff, and pytest.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_modern_app.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Configure Virtual Environment and Tooling
Inspect `pyproject.toml` and ensure `ruff`, `mypy`, and `pytest` are available. Run `ruff check .` to establish baseline code quality.

### Step 2 — Implement TaskItem Schema
In `starter/src/modern_app/core.py`, implement the Pydantic `TaskItem` model with fields for title, description, and completion status.

### Step 3 — Implement TaskManager Storage
Create an internal dictionary storage for tasks in `TaskManager` ensuring each created task receives a unique auto-incrementing ID.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_modern_app.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 4 — Implement Task CRUD Methods
Implement `add_task`, `get_task`, and `list_tasks` with status filtering (`all`, `pending`, `completed`).

### Step 5 — Wire Rich CLI Presentation
In `cli.py`, build the command-line interface using `argparse` and format output using `rich.table.Table`.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/src/modern_app/core.py`, remove the uniqueness check or auto-incrementing logic for task IDs.
Run:
```bash
pytest ../project_solution/test_modern_app.py -k test_add_task_generates_unique_ids -v
```
Watch the test fail with duplicated IDs, then restore the ID sequence generator and confirm it passes.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_modern_app.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **JSON File Persistence:** Add an atomic file persistence layer that exports the task list to `~/.tasks.json`.
2. **Priority Filtering:** Extend `TaskItem` with an enum `Priority` (LOW, MEDIUM, HIGH, URGENT) and implement sorting.
3. **Async Auto-Sync:** Add an async background watcher that reloads tasks when modified externally.
4. **Custom Pre-commit Hook:** Configure a `.pre-commit-config.yaml` running `ruff check` and `mypy` before git commits.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_add_task` | Proves task creation stores items with unique IDs |
| `test_get_task_found_and_missing` | Proves ID lookup returns matching item or None |
| `test_list_tasks_filter` | Proves status filtering partitions pending and completed tasks |
| `test_cli_execution` | Proves command line entry point functions end-to-end |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain the exact role of pyproject.toml vs requirements.txt without looking it up
- [ ] Configure ruff with custom rule selectors (E, F, I, B, UP, SIM, RUF)
- [ ] Run pytest with strict markers and coverage reporting
- [ ] Structure a package with clean src-layout to prevent import confusion
- [ ] Set up an editable install with pip install -e . or uv pip install -e .
- [ ] Explain why sys.path manipulation in application code is an anti-pattern
- [ ] Diagnose and fix virtual environment path mismatches
