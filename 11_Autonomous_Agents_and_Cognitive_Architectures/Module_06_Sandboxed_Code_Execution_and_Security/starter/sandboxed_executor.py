"""Starter stub for Sandboxed Code Executor."""

from __future__ import annotations
from typing import Any


class SandboxedExecutor:
    def __init__(self, timeout_sec: float = 2.0) -> None:
        raise NotImplementedError("SandboxedExecutor is not implemented yet.")

    def execute(self, code_str: str) -> Any:
        raise NotImplementedError
