# Debug Lab Answers: Module 00

<details>
<summary>Bug 1: Fragile relative sys.path hacking</summary>

### Root Cause
Using `sys.path.append("./src")` relies on whatever current working directory (`os.getcwd()`) happens to be when the command runs. If executed from a parent or sibling folder, `./src` points to a non-existent path.

### Fix
Install the project in editable mode (`pip install -e .` or `uv pip install -e .`) so that standard package imports work everywhere without manual `sys.path` tampering. For standalone script pathing, anchor to `__file__`:
```python
from pathlib import Path
src_path = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(src_path))
```
</details>

<details>
<summary>Bug 2: Relative file opening without anchoring</summary>

### Root Cause
`open("config.toml")` looks in `Path.cwd()`, not the directory where the code lives.

### Fix
Anchor configuration resolution to the package or module root:
```python
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.toml"
def load_config():
    if not CONFIG_PATH.exists():
        return "# Default configuration"
    return CONFIG_PATH.read_text(encoding="utf-8")
```
</details>

<details>
<summary>Bug 3: Unhandled ValueError on user input and missing range constraints</summary>

### Root Cause
Raw `int()` call without `try/except` and without domain validation allows non-integer strings to crash the CLI with raw tracebacks and allows invalid negative priority levels.

### Fix
Use structured argument parsing (`argparse` or `click`) with explicit type validation:
```python
def parse_priority(priority_arg: str) -> int:
    try:
        val = int(priority_arg)
        if not (1 <= val <= 10):
            raise ValueError("Priority must be between 1 and 10.")
        return val
    except ValueError as e:
        print(f"Error: Invalid priority '{priority_arg}' - {e}", file=sys.stderr)
        sys.exit(2)
```
</details>
