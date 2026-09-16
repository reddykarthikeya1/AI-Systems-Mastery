# Debug Lab Incident Report: Infinite Spider Trap Exhausts Crawler Memory and Storage

- **Severity:** P1 Crawler Resource Starvation
- **Affected Subsystem:** Module_19_Distributed_Web_Crawler_Deduplication_Google
- **Reported Impact:** A crawler spent 48 hours and 50GB downloading dynamic calendar links (`/calendar?day=1`, `/calendar?day=2`...) from a single malicious host.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in web_crawler_frontier.
Traceback (most recent call last):
  ...
RuntimeError: Infinite Spider Trap Exhausts Crawler Memory and Storage
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_19_Distributed_Web_Crawler_Deduplication_Google/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_web_crawler_frontier.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_web_crawler_frontier.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
