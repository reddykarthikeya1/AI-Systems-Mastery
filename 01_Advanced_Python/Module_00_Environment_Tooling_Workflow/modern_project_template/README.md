# Design Rationale: Modern Python Project Template & Tooling

## Architectural Overview
This solution provides a production-grade Python project scaffold adhering to modern packaging standards (PEP 517/621), uncompromising linting and formatting via Ruff, type safety via strict Mypy, and atomic virtual environment reproducibility.

## Key Design Decisions
1. **Unified `pyproject.toml` Configuration:** All tool configurations (Ruff, Mypy, Pytest, coverage) reside in a single standardized file rather than proliferating legacy config files (`setup.cfg`, `.flake8`, `pytest.ini`).
2. **`src/` Layout Architecture:** Placing application code inside `src/modern_app` prevents the common "import parity trap" where tests accidentally import from local directory files instead of the installed wheel.
3. **Fail-Fast Typing & Linting:** Formatting and linting are unified in Ruff, executing in milliseconds in Rust, removing the historical friction of running 4 separate linters (flake8, isort, black, pyupgrade).

## Rejected Alternatives
1. **Legacy `setup.py` / `requirements.txt` Workflow:**
   - *Reason for Rejection:* Executing arbitrary Python during builds in `setup.py` creates security vulnerabilities, non-deterministic builds, and breaks static wheel distribution.
2. **Flat Layout (`modern_app/` at project root):**
   - *Reason for Rejection:* Flat layouts allow test runners to import local development source without testing that the package installs cleanly as an editable or distributed wheel.

## Invariants & Guarantees
- Zero configuration drift across development and CI.
- All dependencies declare strict lower and upper version bounds.

## Verification
```bash
pytest tests/ -v
ruff check .
mypy src/
```

---

## 🗺️ Recommended Step-by-Step Project Study Path

Follow this sequence to analyze and master the project architecture:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Architecture Review** | Read the specification and design breakdown in this `README.md`. |
| **2** | **Examine Implementation** | Study modular design patterns and invariant safeguards across source files. |
| **3** | **Run Test Suite** | Execute `pytest tests/` to see all production test cases pass green. |
| **4** | **Independent Re-Build** | Re-implement the solution from scratch in `[../starter/](../starter/)` until all tests pass. |

