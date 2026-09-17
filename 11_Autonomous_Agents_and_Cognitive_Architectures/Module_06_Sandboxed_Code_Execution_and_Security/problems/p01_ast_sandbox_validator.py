"""Problem 01 — Ast Sandbox Validator

Topic: 06 Sandboxed Code Execution and Security
Target: Production-grade implementation

Inspect Python code AST to block dangerous imports and system calls.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def ast_sandbox_validator(code_snippet: str, banned_modules: set[str] | None = None) -> tuple[bool, str | None]:
    """Parse code_snippet with ast.
    Disallow import of banned_modules (defaults to {'os', 'sys', 'subprocess', 'shutil'}).
    Returns (is_safe, violation_reason).
    """
    raise NotImplementedError("Implement ast_sandbox_validator")
