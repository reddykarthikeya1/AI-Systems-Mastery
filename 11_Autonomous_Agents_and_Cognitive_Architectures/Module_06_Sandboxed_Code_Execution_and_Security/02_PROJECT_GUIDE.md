# Project Guide: Building an Enterprise Sandboxed Code Executor

In this project, you will build a secure Python code execution engine with AST inspection, timeout guards, and output sanitization.

---

## Three-Tier Implementation Path

### Tier 1: AST Security Validator (Required)
- Parse code into an Abstract Syntax Tree (`ast.parse`).
- Traverse AST nodes to ban malicious imports (`os`, `sys`, `subprocess`, `socket`, `shutil`).
- Disallow calls to dangerous builtins: `eval()`, `exec()`, `open()`, `__import__()`.

### Tier 2: Subprocess Execution with Timeouts & Memory Quotas
- Execute validated code via `subprocess.run()` in a temporary isolated environment.
- Enforce strict wall-clock timeout (e.g. 2.0s) and capture stdout/stderr safely.

### Tier 3: Output Redactor & Secret Scrubbing
- Implement regex-based secret scrubber to redact AWS keys (`AKIA...`), OpenAI keys (`sk-...`), and private IP ranges before returning outputs to the LLM.
