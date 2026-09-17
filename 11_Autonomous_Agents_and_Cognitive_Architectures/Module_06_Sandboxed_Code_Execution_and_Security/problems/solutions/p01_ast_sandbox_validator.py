"""Reference Solution — Problem 01: Ast Sandbox Validator

Topic: 06 Sandboxed Code Execution and Security
"""

from __future__ import annotations


def ast_sandbox_validator(code_snippet: str, banned_modules: set[str] | None = None) -> tuple[bool, str | None]:
    import ast
    if banned_modules is None:
        banned_modules = {'os', 'sys', 'subprocess', 'shutil'}
    try:
        tree = ast.parse(code_snippet)
    except Exception as e:
        return (False, f"SyntaxError: {e}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in banned_modules:
                    return (False, f"Banned import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module in banned_modules:
                return (False, f"Banned import from: {node.module}")
    return (True, None)
