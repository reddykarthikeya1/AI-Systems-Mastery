# Debug Lab Incident Report: Token Bucket Negative Balance Under High Concurrency Race

- **Severity:** P1 Rate Limiter Bypass
- **Affected Subsystem:** Module_03_Edge_Infrastructure_Reverse_Proxies
- **Reported Impact:** Clients exceed their 100 req/sec rate limit by sending bursts of 2,000 requests in parallel threads, resulting in rate limit bypass.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in api_gateway_proxy.
Traceback (most recent call last):
  ...
RuntimeError: Token Bucket Negative Balance Under High Concurrency Race
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_03_Edge_Infrastructure_Reverse_Proxies/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_api_gateway_proxy.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_api_gateway_proxy.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
