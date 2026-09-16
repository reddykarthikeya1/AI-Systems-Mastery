# Module 00: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Python environments, runtime mechanics, project layouts, and modern tooling before moving on to **Module 01**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Runtime Introspection:** What is the programmatic difference between `sys.prefix` and `sys.base_prefix` when running inside a virtual environment versus system Python?
2. **Project Architecture:** Why is the `src-layout` (`src/my_app/`) safer than the `flat-layout` (`my_app/` in root) when running test suites with `pytest`?
3. **Packaging Standards:** What is the role of `pyproject.toml` under PEP 621, and what older configuration files does it replace?
4. **Tooling Performance:** What architectural reason makes `uv` and `ruff` 10x–100x faster than traditional Python tools like `pip`, `flake8`, and `black`?
5. **Execution Order:** When Python encounters an `import foo` statement, in what order does it search directories in `sys.path`?
6. **Language Mechanics:** Why does `def add_user(user, user_list=[]):` cause unexpected state sharing across multiple function calls?
7. **Virtual Environment Isolation:** When you execute a command with `uv run pytest`, does `uv` require you to manually activate the virtual environment beforehand? Why or why not?
8. **Deterministic Builds:** What is the key difference between the dependencies listed in `pyproject.toml` and the contents of `uv.lock`?
9. **Git & CI/CD Hygiene:** Why are pre-commit hooks valuable for team development, and why shouldn't you solely rely on GitHub Actions CI?
10. **Linter Mechanics:** How does a static linter like `ruff` identify bugs and anti-patterns without actually running your Python code?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
In system/global Python, `sys.prefix == sys.base_prefix`. When a virtual environment is activated, `sys.prefix` points to the isolated environment directory (where the virtualenv's `site-packages` lives), while `sys.base_prefix` still points to the original parent Python installation.

#### Answer 2:
In a flat layout, running `pytest` automatically adds the current working directory (`.`) to `sys.path[0]`. This allows tests to import the uninstalled local folder directly, masking errors where the package was not properly packaged, built, or installed. The `src-layout` ensures tests only succeed if the package is installed into the environment.

#### Answer 3:
`pyproject.toml` provides a single, standardized configuration format for project metadata, dependencies, build backends, and tool settings. It replaces `setup.py`, `setup.cfg`, `requirements.txt`, `MANIFEST.in`, `.flake8`, `pytest.ini`, and `black.toml`.

#### Answer 4:
`uv` and `ruff` are written in **Rust** and compiled to native machine code. They utilize multi-threaded file parsing, direct AST memory representations, global package caching with copy-on-write/reflinks, and zero-copy data structures, avoiding Python interpreter overhead.

#### Answer 5:
1. `sys.path[0]`: The directory containing the script used to invoke the interpreter (or current directory in interactive mode).
2. Standard library directories.
3. Third-party `site-packages` directories.

#### Answer 6:
Default parameter expressions are evaluated **once at function definition time**, not during each invocation. As a result, the same mutable list instance in memory is reused across all subsequent calls that omit the argument.

#### Answer 7:
No. `uv run` automatically discovers the local `.venv`, sets up the environment variables (`PATH`, `VIRTUAL_ENV`), and executes the target process inside that isolated context without requiring manual terminal activation (`activate.ps1`).

#### Answer 8:
`pyproject.toml` defines *high-level dependency declarations and acceptable version ranges* (e.g., `pydantic>=2.7.0`). `uv.lock` records the *exact pinned versions, sub-dependencies, and cryptographic file hashes* to ensure identical, reproducible installs on any machine.

#### Answer 9:
Pre-commit hooks run locally in milliseconds on your machine before a commit is created. They catch linting errors, formatting inconsistencies, and broken syntax immediately, preventing broken commits from reaching GitHub and wasting CI compute minutes.

#### Answer 10:
`ruff` uses a fast Rust-based parser to transform Python source code into an **Abstract Syntax Tree (AST)** and a token stream. It traverses the syntax tree to detect rule violations (like unused variables, mutable defaults, or deprecated syntax) purely through static structural analysis.

</details>

---

## Part 3: Hands-on Debugging Challenges

### Challenge 1: The Broken Test Runner

**Scenario:** You cloned a project with the following structure:
```
my_service/
├── pyproject.toml
├── src/
│   └── service/
│       ├── __init__.py
│       └── utils.py
└── tests/
    └── test_utils.py
```
When running `pytest tests/test_utils.py`, it fails immediately with:
`ModuleNotFoundError: No module named 'service'`

**Task:**
1. What line needs to be added to `pyproject.toml` to fix this without modifying test files?
2. What CLI command can you run with `uv` to execute the tests cleanly?

<details>
<summary><b>Solution</b></summary>

1. Add `pythonpath = ["src"]` to the `[tool.pytest.ini_options]` section in `pyproject.toml`:
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   pythonpath = ["src"]
   ```
2. Run tests via uv:
   ```powershell
   uv run pytest
   ```
</details>

---

### Challenge 2: The Shared Cache Bug

**Scenario:** A colleague wrote the following function to cache user metrics:

```python
def record_metric(user_id: str, score: float, history: dict[str, list[float]] = {}) -> dict[str, list[float]]:
    if user_id not in history:
        history[user_id] = []
    history[user_id].append(score)
    return history

u1 = record_metric("user_101", 95.0)
u2 = record_metric("user_102", 88.0)
```

**Task:**
1. What will `u2` contain, and why?
2. Rewrite the function with proper type hints and eliminate the state-leak bug.

<details>
<summary><b>Solution</b></summary>

1. `u2` will contain both `'user_101'` and `'user_102'` (`{'user_101': [95.0], 'user_102': [88.0]}`) because the default dictionary `{}` was evaluated once at definition time and shared across all invocations.
2. Corrected implementation:
```python
from __future__ import annotations

def record_metric(
    user_id: str,
    score: float,
    history: dict[str, list[float]] | None = None,
) -> dict[str, list[float]]:
    if history is None:
        history = {}
    if user_id not in history:
        history[user_id] = []
    history[user_id].append(score)
    return history
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Wrong interpreter

```
$ pip install polars
Successfully installed polars-1.12.0

$ python -c "import polars"
ModuleNotFoundError: No module named 'polars'
```

**Observed symptom:** The install succeeded, and the very next command cannot find the package.

**(a)** What is almost certainly different between `pip` and `python` here?

**(b)** What two commands diagnose it in one line each?

**(c)** What invocation makes this impossible?

<details>
<summary><b>Show the diagnosis</b></summary>

`pip` and `python` are resolving to **different interpreters**. A bare `pip` is whichever one appears first on `PATH`, which is often not the `python` you just ran — a common outcome with multiple Pythons, an inactive virtualenv, or a user-site install.

**Diagnose:**
```bash
python -c "import sys; print(sys.executable)"
pip --version        # prints the interpreter it belongs to
```
Compare the two paths.

**Prevent it** by never invoking `pip` directly: `python -m pip install polars`. The `-m` form guarantees the package lands in the interpreter you are about to use. This single habit eliminates the entire class of bug, and it is why every command in this course is written as `python -m pip` and `python -m pytest`.

</details>

---

### D2. Ruff passes locally, fails in CI

```
$ ruff check .
All checks passed!

# ...but CI reports:
# tools/helper.py:14:1: I001 Import block is un-sorted
```

**Observed symptom:** Identical command, opposite result.

**(a)** Name three reasons the same command can disagree between machines.

**(b)** How do you make the two environments agree?

**(c)** Why is pinning the linter version not optional?

<details>
<summary><b>Show the diagnosis</b></summary>

**Three reasons:** (1) **different ruff versions** — rules are added and defaults change between releases, so a newer CI ruff flags what your older local one did not; (2) **different working directory** — ruff discovers `pyproject.toml` by walking upward, so running from a subdirectory can pick up different config; (3) **files excluded locally** — an untracked file, or one matched by a local `.gitignore` that CI does not have.

**Make them agree:** pin the version in `pyproject.toml`, install with `pip install -e ".[dev]"` in both places, and run from the repository root in both. Better still, add a `pre-commit` hook so the same pinned binary runs before every commit.

**Pinning is not optional** because an unpinned linter turns your CI into a moving target: a build that passed yesterday fails today with no change to your code. That trains people to ignore CI, which is far more expensive than the pin.

</details>

---

### D3. Editable install that does not update

```
$ pip install -e .
$ # edit src/mypkg/core.py, add a new function
$ python -c "from mypkg.core import new_function"
ImportError: cannot import name 'new_function'
```

**Observed symptom:** An editable install is supposed to pick up edits immediately.

**(a)** Give two reasons the edit is not visible.

**(b)** How do you verify which file Python actually loaded?

**(c)** What does `src/` layout protect you from that a flat layout does not?

<details>
<summary><b>Show the diagnosis</b></summary>

**Two reasons:** (1) a **stale non-editable copy** shadows it — a previous `pip install .` left a real copy in `site-packages`, which wins over the editable path; (2) you are **importing a different package** — a directory named `mypkg` in your current working directory shadows the installed one, because `''` (the cwd) comes first on `sys.path`.

**Verify:**
```python
import mypkg.core; print(mypkg.core.__file__)
```
That prints the file actually in use. It is the single most useful line in Python packaging debugging.

**`src/` layout protects you** from exactly the second case: because the package is not at the repository root, you *cannot* accidentally import it from the cwd. Any successful import proves the install works — which means your tests exercise the installed package, the way your users will. That is why Module 00's template uses it.

</details>

---

### D4. pytest cannot find the module

```
$ pytest
ImportError while importing test module 'tests/test_core.py'
ModuleNotFoundError: No module named 'mypkg'
```

**Observed symptom:** The tests import the package, and pytest cannot see it.

**(a)** Why does pytest not automatically see your package?

**(b)** Name the three standard fixes and which is best.

**(c)** What does adding an `__init__.py` to `tests/` change?

<details>
<summary><b>Show the diagnosis</b></summary>

pytest inserts the **rootdir of the test file** into `sys.path` (in the default `prepend` import mode), not your source directory. With a `src/` layout the package is nowhere on the path unless it is installed.

**Three fixes, worst to best:** (1) `sys.path` manipulation in `conftest.py` — works, but now tests exercise the source tree rather than the installed artifact; (2) `pythonpath = ["src"]` in `pyproject.toml` — declarative and fine; (3) **`pip install -e .`** — best, because the tests then import exactly what a user would.

**An `__init__.py` in `tests/`** makes the test directory a package, which changes module naming (`tests.test_core` instead of `test_core`). That prevents name collisions between same-named test files in different directories — a real problem in large suites — but it does not fix a missing package. The two issues are often confused.

</details>

---

### D5. Committed virtual environment

```
$ git status
Changes to be committed:
    new file:   .venv/lib/python3.11/site-packages/polars/...
    ... 14,203 more files
```

**Observed symptom:** A one-line code change produced a 14,000-file commit.

**(a)** Why is committing `.venv/` harmful, beyond size?

**(b)** What is the correct way to make the environment reproducible?

**(c)** How do you fix it after it has already been committed?

<details>
<summary><b>Show the diagnosis</b></summary>

**Beyond size:** a virtualenv contains **absolute paths** baked into its scripts and `pyvenv.cfg`, so it does not work on any other machine or even in a different directory. It contains **compiled binaries** for one OS and CPU architecture. And it makes every dependency change an unreviewable diff, so a malicious or accidental package change is invisible in review.

**Correct approach:** commit the *intent* (`pyproject.toml`) and the *resolution* (`uv.lock` or `requirements.txt` with hashes). Anyone can then rebuild an identical environment, on their own platform.

**Fix after committing:** add `.venv/` to `.gitignore`, then `git rm -r --cached .venv` to untrack it while keeping the files on disk. Note the history still contains them — repository size is permanently affected unless you rewrite history, which is why the `.gitignore` should exist from the first commit.

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
