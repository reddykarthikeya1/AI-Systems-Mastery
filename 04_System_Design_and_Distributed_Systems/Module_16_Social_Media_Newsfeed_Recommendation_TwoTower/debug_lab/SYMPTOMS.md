# Debug Lab Incident Report: Write Amplification Catastrophe on Celebrity Fan-Out

- **Severity:** P0 Message Queue Backlog
- **Affected Subsystem:** Module_16_Social_Media_Newsfeed_Recommendation_TwoTower
- **Reported Impact:** A celebrity with 50M followers posted a picture, causing the message queue to inject 50M insert tasks, creating a 6-hour backlog for all other users.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in newsfeed_recommendation_engine.
Traceback (most recent call last):
  ...
RuntimeError: Write Amplification Catastrophe on Celebrity Fan-Out
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_16_Social_Media_Newsfeed_Recommendation_TwoTower/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_newsfeed_recommendation_engine.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_newsfeed_recommendation_engine.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
