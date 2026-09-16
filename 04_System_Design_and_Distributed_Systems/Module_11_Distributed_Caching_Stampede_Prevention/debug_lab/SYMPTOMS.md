# Debug Lab Incident Report: Cache Stampede Crashes Primary Database on Hot Key Expiration

- **Severity:** P0 Full Database Outage
- **Affected Subsystem:** Module_11_Distributed_Caching_Stampede_Prevention
- **Reported Impact:** When the homepage product catalog cache key expired, 5,000 concurrent web workers simultaneously queried MySQL, exhausting all 500 connections and crashing the database.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in distributed_cache_guard.
Traceback (most recent call last):
  ...
RuntimeError: Cache Stampede Crashes Primary Database on Hot Key Expiration
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_11_Distributed_Caching_Stampede_Prevention/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_distributed_cache_guard.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_distributed_cache_guard.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
