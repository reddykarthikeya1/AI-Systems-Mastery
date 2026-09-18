"""Problem 01 — Ast Sandbox Validator

Topic: 06 Sandboxed Code Execution and Security
Target: Production-grade implementation

Inspect Python code AST to block dangerous imports and system calls.

Example:
    >>> ast_sandbox_validator('x = 10 + 20')
    (True, None)
    >>> ast_sandbox_validator("import os\nos.system('rm -rf /')")
    (False, 'Banned import: os')

Hints:
    Hint 1: You need to look at the code's structure, not its text — a
        banned module name could appear inside a string literal or
        variable name, so only real import statements should count.
    Hint 2: Parse the snippet with ast.parse, then ast.walk the tree
        looking for ast.Import and ast.ImportFrom nodes, checking each
        imported name against the banned set.
    Hint 3: ast.Import and ast.ImportFrom expose the module name
        differently — Import nodes carry a list of aliases
        (node.names[i].name) for "import os, sys", while ImportFrom
        carries a single node.module for "from os import path"; also
        treat a syntax error in the snippet as unsafe rather than letting
        the parse exception propagate.
"""

from __future__ import annotations


def ast_sandbox_validator(code_snippet: str, banned_modules: set[str] | None = None) -> tuple[bool, str | None]:
    """Parse code_snippet with ast.
    Disallow import of banned_modules (defaults to {'os', 'sys', 'subprocess', 'shutil'}).
    Returns (is_safe, violation_reason).
    """
    raise NotImplementedError("Implement ast_sandbox_validator")
