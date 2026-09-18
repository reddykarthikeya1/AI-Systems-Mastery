# Debug Lab Solution & Forensic Post-Mortem

## Incident: Tool Dispatcher Crashes the Agent Process on Bad Arguments and Hangs Forever on Slow Tools

---

### 🔍 Forensic Root Cause Analysis
`dispatch()` is a single unguarded line:

```python
def dispatch(self, name, args):
    return self.tools[name](**args)
```

It never checks that `name` exists in `self.tools` before indexing into it, so an unregistered tool name raises a raw `KeyError` straight out of the dispatcher instead of a recoverable "unknown tool" result. It never validates that `args` supplies every parameter the target tool requires before calling it, so a missing argument raises a raw `TypeError` from deep inside the tool's own signature. And it never wraps the call in any kind of watchdog or timeout, so a slow or hung tool blocks the calling thread for exactly as long as the tool takes -- unbounded. All three failure modes trace back to the same missing layer: there is no boundary between "untrusted tool call as requested by the LLM" and "the process's own execution," so any way that request can go wrong takes the whole process down with it.

---

### 🛠️ Production Corrective Action & Code Fix

```python
import concurrent.futures

class FixedToolDispatcher:
    def __init__(self, timeout_seconds=10):
        self.tools = {}
        self.timeout_seconds = timeout_seconds

    def dispatch(self, name, args):
        if name not in self.tools:
            return {"error": f"Unknown tool: {name}"}
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(self.tools[name], **args)
                return {"result": future.result(timeout=self.timeout_seconds)}
        except TypeError as e:
            return {"error": f"Invalid arguments for {name}: {e}"}
        except concurrent.futures.TimeoutError:
            return {"error": f"{name} timed out after {self.timeout_seconds}s"}
```

Unknown tool names and invalid arguments now return a structured `{"error": ...}` result the agent loop can feed back to the model, instead of an unhandled exception that kills the process. The `ThreadPoolExecutor` with an explicit `timeout` bounds how long any single tool call is allowed to block the caller.

---

### 🛡️ Production Prevention Invariants
1. **No Tool-Call Error Should Escape as an Unhandled Exception:** Always translate a failed tool call into a structured error result the agent loop can act on, never let it propagate as a raw exception.
2. **Every Tool Call Must Have an Enforced Timeout:** A tool that never returns must not be able to block the dispatcher indefinitely.
3. **Validate Arguments Against the Tool's Declared Schema First:** Check required parameters before invoking the tool, so malformed calls are reported clearly instead of surfacing as whatever exception the tool's own signature happens to raise.
