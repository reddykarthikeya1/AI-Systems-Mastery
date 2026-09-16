# Beginner Playground: Sandboxed Code Execution & Security


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to Code Sandboxing! Giving an AI agent the ability to execute generated Python code is superpowers for problem solving, but without sandboxing, it is an open door to Remote Code Execution (RCE).

---

## 1. The Core Mental Model: Defense-in-Depth

```
 [ Untrusted LLM Code ]
           |
           v
 [ Layer 1: AST Static Analysis ]  --> (Rejects banned imports: os, sys, subprocess)
           |
           v
 [ Layer 2: Subprocess Sandbox ]   --> (Enforces memory limits & wall-clock timeouts)
           |
           v
 [ Layer 3: Output Sanitizer ]     --> (Redacts API keys, passwords, and secrets)
           |
           v
 [ Safe Execution Result ]
```

---

## 2. Interactive Pure-Python Experiment: AST Code Inspector

```python
import ast

BANNED_MODULES = {"os", "sys", "subprocess", "shutil", "socket"}

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in BANNED_MODULES:
                self.violations.append(f"Direct import of forbidden module '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in BANNED_MODULES:
            self.violations.append(f"Import from forbidden module '{node.module}'")
        self.generic_visit(node)

def inspect_code_safety(code_str: str):
    tree = ast.parse(code_str)
    visitor = SecurityVisitor()
    visitor.visit(tree)
    return visitor.violations

safe_code = "x = [i**2 for i in range(10)]\nprint(sum(x))"
unsafe_code = "import os\nos.system('rm -rf /')"

print("Safe code check:", inspect_code_safety(safe_code))
print("Unsafe code check:", inspect_code_safety(unsafe_code))
```
