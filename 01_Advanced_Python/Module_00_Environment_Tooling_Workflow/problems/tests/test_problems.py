"""Pytest suite for Environment Tooling Workflow problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if Path.cwd().resolve() == PROB_DIR.resolve():
    if str(PROB_DIR) not in sys.path:
        sys.path.insert(0, str(PROB_DIR))
else:
    if str(SOL_DIR) not in sys.path:
        sys.path.insert(0, str(SOL_DIR))

from p01_solve_systems_task import solve_systems_task


def test_solve_systems_task():
    assert solve_systems_task([1, 2, 2, "a", "a", "b"]) == {"1": 1, "2": 2, "a": 2, "b": 1}
    assert solve_systems_task([]) == {}
    assert solve_systems_task(["x"]) == {"x": 1}

