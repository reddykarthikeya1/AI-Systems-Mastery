# Debug Lab Incident Report: MD5 Hash Collision and Truncation Inconsistencies

- **Severity:** P1 URL Misdirection
- **Affected Subsystem:** Module_14_Distributed_URL_Shortener_TinyURL
- **Reported Impact:** User Alice shortened a link to her blog, but navigating to the short link redirected to user Bob's malicious site due to MD5 prefix collision.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in url_shortener_service.
Traceback (most recent call last):
  ...
RuntimeError: MD5 Hash Collision and Truncation Inconsistencies
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_14_Distributed_URL_Shortener_TinyURL/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_url_shortener_service.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_url_shortener_service.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
