"""Beginner playground for Module 00 - Environment, Tooling & Modern Workflow.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import os
import platform
import sys

# -------------------------------------------- 1. Inspecting System Runtime & Executable
version_info = sys.version_info
assert version_info.major == 3
assert version_info.minor >= 10
print(f"Python major.minor: {version_info.major}.{version_info.minor}")

# -------------------------------------------- 2. Working with the Standard Library Pathlib
from pathlib import Path
cwd = Path.cwd()
assert cwd.is_absolute()
parent = cwd.parent
assert parent != cwd or cwd == Path(cwd.root)
print(f"Verified current working directory: {cwd.name}")

# -------------------------------------------- 3. Virtual Environment Detection
is_venv = sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")
assert isinstance(is_venv, bool)
assert os.path.exists(sys.executable)
print(f"Python environment detected (in virtual environment: {is_venv})")

print()
print("All checks passed.")
