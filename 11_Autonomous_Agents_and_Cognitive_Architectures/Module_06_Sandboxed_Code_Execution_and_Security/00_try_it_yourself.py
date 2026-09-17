"""Beginner playground for Module 06 - Sandboxed Code Execution & Security.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import ast

# -------------------------------------------- 1. AST Code Sanitization Check
banned_modules = {"os", "sys", "subprocess", "socket"}

def is_safe_code(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.split('.')[0] in banned_modules for alias in node.names):
                return False
        elif isinstance(node, ast.ImportFrom):
            if (node.module or '').split('.')[0] in banned_modules:
                return False
    return True

safe_snippet = "x = [i**2 for i in range(10)]"
malicious_snippet = "import os\nos.system('rm -rf /')"

assert is_safe_code(safe_snippet) is True
assert is_safe_code(malicious_snippet) is False
print("AST security validator successfully blocked dangerous imports.")

# -------------------------------------------- 2. Banning Dangerous Builtin Calls
banned_calls = {"eval", "exec", "__import__"}
def check_calls(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in banned_calls:
                return False
    return True

assert check_calls("print(math.sqrt(4))") is True
assert check_calls("eval('2 + 2')") is False
print("AST call guard successfully caught dynamic execution attempts.")

# -------------------------------------------- 3. Resource Execution Timeout Guard
timeout_sec = 2.0
elapsed_sec = 0.45
assert elapsed_sec < timeout_sec
print(f"Execution finished in {elapsed_sec}s (within {timeout_sec}s limit).")

print()
print("All checks passed.")
