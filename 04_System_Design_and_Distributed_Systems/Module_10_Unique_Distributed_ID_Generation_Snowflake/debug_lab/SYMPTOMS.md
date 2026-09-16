# Debug Lab Incident Report: Duplicate Snowflake IDs Generated During NTP Backward Time Leap

- **Severity:** P0 Data Corruption / Duplicate Primary Key
- **Affected Subsystem:** Module_10_Unique_Distributed_ID_Generation_Snowflake
- **Reported Impact:** Two distinct orders received identical 64-bit Snowflake IDs when the server's NTP daemon adjusted local time backwards by 42 milliseconds.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in snowflake_generator.
Traceback (most recent call last):
  ...
RuntimeError: Duplicate Snowflake IDs Generated During NTP Backward Time Leap
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_10_Unique_Distributed_ID_Generation_Snowflake/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_snowflake_generator.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_snowflake_generator.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
