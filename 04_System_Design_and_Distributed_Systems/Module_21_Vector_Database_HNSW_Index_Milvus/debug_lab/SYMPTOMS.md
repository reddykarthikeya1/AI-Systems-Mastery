# Debug Lab Incident Report: HNSW Graph Disconnection Isolates Vector Subsets from Search

- **Severity:** P1 Search Recall Degradation
- **Affected Subsystem:** Module_21_Vector_Database_HNSW_Index_Milvus
- **Reported Impact:** Vector search recall dropped from 98% to 42% after batch deleting 1,000 vectors because node deletion broke navigable highway links.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in vector_database_engine.
Traceback (most recent call last):
  ...
RuntimeError: HNSW Graph Disconnection Isolates Vector Subsets from Search
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_21_Vector_Database_HNSW_Index_Milvus/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_vector_database_engine.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_vector_database_engine.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
