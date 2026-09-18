# Debug Lab Solution & Forensic Post-Mortem

## Incident: Code Execution Tool Gives LLM-Generated Code Full Access to the Host Process

---

### 🔍 Forensic Root Cause Analysis
`execute()` calls the builtin `exec(code)` with no `globals`/`locals` arguments:

```python
def execute(self, code):
    exec(code)
```

When `exec()` is called without explicit `globals`/`locals`, Python defaults to running the given code inside the *calling* frame's own namespace -- here, that is `execute()`'s own local and global scope, which at the moment of the call already includes `self` (the live `BrokenCodeRunner` instance) bound as a local variable, plus the full builtin/module ecosystem of the host interpreter. The executed code is therefore not sandboxed in any sense: it can read and rewrite attributes on `self`, import arbitrary modules (`os`, `subprocess`, `socket`, ...), and otherwise act with exactly the same privileges and memory access as the process that called `execute()`. There is no process isolation, no restricted namespace, and no resource or API allow-list of any kind.

---

### 🛠️ Production Corrective Action & Code Fix

```python
import subprocess, sys, tempfile

class FixedCodeRunner:
    def execute(self, code, timeout_seconds=5):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(code)
            path = f.name
        result = subprocess.run(
            [sys.executable, "-I", "-S", path],   # isolated mode, no site packages, no shared memory
            capture_output=True, text=True, timeout=timeout_seconds,
        )
        return result.stdout
```

Running the untrusted code in a separate subprocess means it can no longer reach `self` or any other live Python object in the host process by construction -- there is no shared memory to walk into. A production system would harden this further with a dedicated low-privilege OS user or container, no filesystem/network access by default, and CPU/memory limits, but the essential fix is the same: untrusted code must run somewhere it cannot see the caller's own objects.

---

### 🛡️ Production Prevention Invariants
1. **Never `exec()` Untrusted Code In-Process:** Always execute it in an isolated subprocess or container with no shared memory or object references back to the host process.
2. **Deny Network and Filesystem Access by Default:** Allow-list only what a specific tool call actually needs, rather than inheriting the host process's full capabilities.
3. **Treat "Run This LLM-Authored Code" as an Untrusted-Input Security Boundary:** Review and test it with the same rigor as authentication code, since it is exactly as security-critical.
