# Debug Lab Incident Report: Load Balancer Cascading Collapse via Unhealthy Server Flapping

- **Severity:** P0 Full Site Outage
- **Affected Subsystem:** Module_04_Load_Balancing_Algorithms_Health_Probes
- **Reported Impact:** When Server A becomes slightly slow, the load balancer removes it, shifting traffic to Server B and C. This overloads Server B, causing it to fail, which then knocks out Server C in a cascade.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in load_balancer.
Traceback (most recent call last):
  ...
RuntimeError: Load Balancer Cascading Collapse via Unhealthy Server Flapping
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_04_Load_Balancing_Algorithms_Health_Probes/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_load_balancer.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_load_balancer.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
