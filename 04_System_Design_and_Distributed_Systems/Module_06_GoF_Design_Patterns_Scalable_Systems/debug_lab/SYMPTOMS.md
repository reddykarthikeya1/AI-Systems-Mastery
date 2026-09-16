# Debug Lab Incident Report: Decorator Retry Storm Exhausts Downstream Third-Party SMS API

- **Severity:** P1 Downstream API Rate Limit Lockout
- **Affected Subsystem:** Module_06_GoF_Design_Patterns_Scalable_Systems
- **Reported Impact:** When Twilio returned HTTP 503, the notification service retried 5 times immediately without exponential backoff or jitter, resulting in full account suspension.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in notification_engine.
Traceback (most recent call last):
  ...
RuntimeError: Decorator Retry Storm Exhausts Downstream Third-Party SMS API
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_06_GoF_Design_Patterns_Scalable_Systems/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_notification_engine.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_notification_engine.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
