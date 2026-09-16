# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is Python's `eval(code, {"__builtins__": {}})` fundamentally insecure?
   - *Answer*: Python reflection allows traversing object inheritance trees: `().__class__.__base__.__subclasses__()` allows reaching `os._wrap_close` or `subprocess.Popen` without importing them.
2. What is the difference between gVisor and standard Docker container isolation?
   - *Answer*: Standard Docker shares the host Linux kernel directly (a kernel exploit escapes the container); gVisor intercepts and reimplements Linux syscalls in user-space (Go), creating a true sandbox.
3. How does Indirect Prompt Injection compromise a code-executing agent?
   - *Answer*: When the agent parses an untrusted file (e.g. CSV or HTML), malicious text inside the file instructs the LLM to format its next code execution block to exfiltrate database records.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: High-Throughput Safe Code Execution at Scale
**Context**: A coding assistant platform executes 500,000 Python code snippets per day submitted by end users. MicroVM spin-up latency and container cleanup overhead are creating massive CPU load.
**Question**: Architect an execution tier that balances sub-100ms latency with ironclad security.
**Solution**:
1. Maintain a pre-warmed pool of ephemeral Firecracker microVMs or gVisor sandbox workers over Unix Domain Sockets.
2. Assign each request an immutable read-only filesystem snapshot with tmpfs for scratch workspace.
3. Terminate and recreate the microVM worker after each execution to prevent state leakage between tenants.
