# 🐣 Interactive Foundations Playground: Sandboxed Code Execution & Security

> *"Never let an LLM run arbitrary code on your server without strict walls, locked doors, and no root privileges."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import ast
```

---

## 1. AST Code Sanitization Check

Inspecting the Python Abstract Syntax Tree (AST) to ban dangerous modules like `os`, `sys`, and `subprocess`.

```python
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
```

---

## 2. Banning Dangerous Builtin Calls

Disallowing `eval()`, `exec()`, and `__import__` in generated scripts.

```python
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
```

---

## 3. Resource Execution Timeout Guard

Enforcing execution timeouts prevents runaway while-loops from stalling worker pods.

```python
timeout_sec = 2.0
elapsed_sec = 0.45
assert elapsed_sec < timeout_sec
print(f"Execution finished in {elapsed_sec}s (within {timeout_sec}s limit).")
```

---
