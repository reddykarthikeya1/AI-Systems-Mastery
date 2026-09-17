# 🐣 Interactive Foundations Playground: Environment, Tooling & Modern Workflow

> *"A robust environment is the foundation of modern production Python systems."*

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
import os
import platform
import sys
```

---

## 1. Inspecting System Runtime & Executable

Python exposes system configuration and executable paths through `sys` and `platform`.

```python
version_info = sys.version_info
assert version_info.major == 3
assert version_info.minor >= 10
print(f"Python major.minor: {version_info.major}.{version_info.minor}")
```

---

## 2. Working with the Standard Library Pathlib

The `pathlib` module provides an object-oriented API for interacting with the filesystem safely across OSes.

```python
from pathlib import Path
cwd = Path.cwd()
assert cwd.is_absolute()
parent = cwd.parent
assert parent != cwd or cwd == Path(cwd.root)
print(f"Verified current working directory: {cwd.name}")
```

---

## 3. Virtual Environment Detection

Production scripts check `sys.prefix` against `sys.base_prefix` to verify if they are running inside an isolated virtual environment.

```python
is_venv = sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")
assert isinstance(is_venv, bool)
assert os.path.exists(sys.executable)
print(f"Python environment detected (in virtual environment: {is_venv})")
```

---
