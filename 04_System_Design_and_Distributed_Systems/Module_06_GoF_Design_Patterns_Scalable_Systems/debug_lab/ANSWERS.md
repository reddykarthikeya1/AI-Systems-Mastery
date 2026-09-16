# Debug Lab Solution & Forensic Post-Mortem

## Incident: Decorator Retry Storm Exhausts Downstream Third-Party SMS API

---

### 🔍 Forensic Root Cause Analysis
The retry decorator executed retries in a tight loop with zero delay, amplifying traffic against a struggling upstream provider by 500%.

---

### 🛠️ Production Corrective Action & Code Fix

```python
import time, random

def send_with_exponential_backoff_and_jitter(fn, max_retries: int = 5, base_delay: float = 0.1):
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception:
            if attempt == max_retries - 1:
                raise
            # Exponential backoff + Full Jitter:
            delay = random.uniform(0, base_delay * (2 ** attempt))
            time.sleep(delay)

```

---

### 🛡️ Production Prevention Invariants
1. **Automated Stress Testing:** Ensure regression tests assert behavior under high concurrency and failure injection.
2. **Defensive Telemetry:** Export real-time metrics tracking this specific failure mode before thresholds are breached.
3. **Fail-Safe Defaults:** Systems should fail closed or degrade gracefully rather than corrupting state.
