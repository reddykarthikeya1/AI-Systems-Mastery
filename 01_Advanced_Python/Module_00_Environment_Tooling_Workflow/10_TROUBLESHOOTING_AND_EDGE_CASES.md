# Module 00: Troubleshooting, Edge Cases & Developer Traps

This reference guide solves the most common development pitfalls and edge cases encountered when configuring Python environments, editors, notebooks, and modern toolchains.

---

## 1. PowerShell: "Running scripts is disabled on this system"

### Symptom
When attempting to activate a virtual environment in PowerShell (`.venv\Scripts\Activate.ps1`), you receive the error:
```
File C:\...\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
+ CategoryInfo          : SecurityError: (:) [], PSSecurityException
+ FullyQualifiedErrorId : UnauthorizedAccess
```

### Cause
Windows sets the default PowerShell execution policy to `Restricted` to prevent arbitrary `.ps1` script execution.

### Solution
Change the execution policy for your user account (does not require Administrator privileges):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then rerun:
```powershell
.venv\Scripts\Activate.ps1
```

---

## 2. `ModuleNotFoundError` with `src-layout`

### Symptom
Running `pytest` or `python src/my_app/core.py` results in:
```
ModuleNotFoundError: No module named 'my_app'
```

### Cause
In a `src-layout`, your package is inside `src/`, which is not in `sys.path` by default when running scripts directly from the project root.

### Solution
1. **With `uv`:** Run via `uv run` which automatically resolves the local package:
   ```powershell
   uv run python -m my_app.cli
   ```
2. **With `pytest`:** Ensure your `pyproject.toml` contains `pythonpath = ["src"]`:
   ```toml
   [tool.pytest.ini_options]
   pythonpath = ["src"]
   testpaths = ["tests"]
   ```
3. **With editable installs:** Install your package in editable mode:
   ```powershell
   uv pip install -e .
   ```

---

## 3. VS Code Shows Yellow Squiggly Lines (Interpreter Desync)

### Symptom
Packages installed with `uv add` (like `pydantic` or `rich`) work in the terminal, but VS Code / Pylance highlights them with `ReportMissingImports`.

### Cause
VS Code is using the global system Python interpreter instead of your project's local `.venv`.

### Solution
1. Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS).
2. Type and select: **`Python: Select Interpreter`**.
3. Choose the interpreter inside your project's `.venv` directory (e.g., `./.venv/Scripts/python.exe`).
4. Ensure `.vscode/settings.json` has:
   ```json
   {
     "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe"
   }
   ```

---

## 4. Git Line Endings: CRLF vs. LF Conflicts

### Symptom
On Windows, Git converts file endings to `CRLF` (`\r\n`), causing shell scripts or Linux Docker containers to fail with errors like:
```
/bin/sh: ./entrypoint.sh: /bin/sh^M: bad interpreter: No such file or directory
```

### Solution
Add a `.gitattributes` file to the root of your project:
```gitattributes
# Auto detect text files and normalize line endings
* text=auto eol=lf

# Force LF for shell scripts and Dockerfiles
*.sh text eol=lf
Dockerfile text eol=lf
*.py text eol=lf
```
Then renormalize the repository:
```powershell
git add --renormalize .
```

---

## 5. Lockfile (`uv.lock`) Out of Sync with `pyproject.toml`

### Symptom
A teammate adds a new package directly into `pyproject.toml` by editing the text file, but running `uv sync` warns of discrepancies or doesn't install the exact version.

### Cause
`pyproject.toml` defines *dependency ranges*, while `uv.lock` contains *exact cryptographic hashes and resolved versions*.

### Solution
Whenever `pyproject.toml` is modified manually, re-lock and sync:
```powershell
# Update the lockfile to match pyproject.toml
uv lock

# Sync the virtual environment
uv sync
```
Or always use `uv add <package>` which automatically updates both files atomically!

---

## 6. The Mutable Default Argument Bug

### Symptom
A function with a default list/dictionary retains data across separate calls:
```python
def append_item(item, storage=[]):
    storage.append(item)
    return storage

print(append_item("A"))  # ['A']
print(append_item("B"))  # ['A', 'B']  <-- Bug! Expected ['B']
```

### Cause
Default parameter values in Python are evaluated **once at function definition time**, not each time the function is called. The list object `[]` persists in memory.

### Solution
Always use `None` as the default value and instantiate the list inside the function:
```python
def append_item(item: str, storage: list[str] | None = None) -> list[str]:
    if storage is None:
        storage = []
    storage.append(item)
    return storage
```
*Note: `ruff` automatically detects this anti-pattern under rule `B006` (flake8-bugbear).*

---

## 7. Jupyter Notebooks: `NameError` from Out-of-Order Execution

### Symptom
Running a cell in a Jupyter notebook throws `NameError: name 'sys' is not defined`, even though you clearly see `import sys` at the top of the notebook!

### Cause
Jupyter notebooks maintain a live execution state in RAM. If you click on Cell 2 before running Cell 1, Cell 1's code has **not yet executed in memory**, so its imported modules and variables do not exist yet!

### Solution
1. Always run notebook cells **sequentially from top to bottom** (or click **"Run All"** in the top toolbar).
2. If state becomes confusing, click **"Restart Kernel"** followed by **"Run All"**.

---

## 8. "Why Did My Script Run Without Printing Anything?" (Function Definitions vs Calls)

### Symptom
You write a python file with several functions containing `print()` statements, run `python my_script.py`, and the terminal returns with **zero output**.

### Cause
Writing `def my_function():` only registers the **recipe/blueprint** in Python's memory. It does not cook the meal (execute the code) until you explicitly **call** the function using parentheses: `my_function()`.

### Solution
Use the standard Python entry point at the bottom of the script:
```python
def check_status():
    print("System is operational!")

# The ignition key:
if __name__ == "__main__":
    check_status()  # <-- Explicit call!
```
*When you run `python my_script.py` directly, Python sets `__name__ = "__main__"`, triggering the call to `check_status()`!*

---

## 9. `UnicodeEncodeError` When You `print()` an Emoji

### Symptom

Your script works fine until you add an emoji to a message, then dies on the
last line that should have been the easy part:

```
File "...\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input, self.errors, encoding_table)[0]
UnicodeEncodeError: 'charmap' codec can't encode character '🚀'
    in position 12: character maps to <undefined>
```

### Cause

The Windows console's default code page is **cp1252**, a 256-character
single-byte encoding with no room for emoji. Python encodes whatever you print
using that code page, so the *string* is fine — it is the act of writing it to
the terminal that fails.

Two consequences worth internalising:

1. **Your program was correct.** The computation finished; only the display
   failed. A script that dies while printing a right answer is still a broken
   script, and this is the most common way that happens on Windows.
2. **It is environment-dependent.** The same file runs fine in VS Code's
   terminal, in Windows Terminal with UTF-8 enabled, and on macOS or Linux. So
   it passes on your machine and fails on someone else's — or the reverse.

Emoji in *comments, docstrings and Markdown* is completely safe. Only the
argument to `print()` (or anything else written to `stdout`) passes through the
console encoder.

### Solution

Pick whichever fits the situation:

```python
# 1. Best for code other people will run: use ASCII markers.
print("[OK] Tests passed")          # instead of "✅ Tests passed"
print("[FAIL] 3 tests failed")      # instead of "❌ 3 tests failed"
```

```python
# 2. Keep the emoji, force the stream to UTF-8. Put this before the first print.
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
print("Blast off! 🚀")
```

```bash
# 3. Per-run, no code change:
PYTHONIOENCODING=utf-8 python my_script.py
```

```powershell
# 4. Per-session, PowerShell:
$env:PYTHONIOENCODING = "utf-8"
```

`errors="replace"` in option 2 is deliberate: it substitutes an unmappable
character rather than raising, so a stray glyph degrades the output instead of
killing the run.

> **Why this module mentions it at all:** this course's own beginner playgrounds
> used emoji inside `print()` until it was caught by running every code block on
> a stock Windows console. It is not an exotic edge case — it is what happens
> the first time you try to make your output friendly.
