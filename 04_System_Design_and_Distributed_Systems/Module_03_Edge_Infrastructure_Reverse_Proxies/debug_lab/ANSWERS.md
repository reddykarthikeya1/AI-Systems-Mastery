# Debug Lab Solution & Forensic Post-Mortem

## Incident: Token Bucket Negative Balance Under High Concurrency Race

---

### 🔍 Forensic Root Cause Analysis
The rate limiter checked `tokens > 0` and decremented `tokens` without synchronization (or without Redis atomic Lua script). Concurrent requests all read tokens=1 before any thread decremented, allowing 5 requests through.

---

### 🛠️ Production Corrective Action & Code Fix

```python
import threading

class ThreadSafeRateLimiter:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.tokens = capacity
        self._lock = threading.Lock()
        
    def allow_request(self) -> bool:
        with self._lock:
            if self.tokens > 0:
                self.tokens -= 1
                return True
            return False

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
