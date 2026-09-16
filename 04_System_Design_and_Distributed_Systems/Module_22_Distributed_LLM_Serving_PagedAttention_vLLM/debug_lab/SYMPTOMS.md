# Debug Lab Incident Report: GPU Out-of-Memory Crash Caused by KV-Cache Internal Fragmentation

- **Severity:** P0 LLM Serving Cluster Crash
- **Affected Subsystem:** Module_22_Distributed_LLM_Serving_PagedAttention_vLLM
- **Reported Impact:** An A100 80GB GPU ran out of memory when serving only 12 concurrent requests due to static memory pre-allocation for max-seq-length (4,096 tokens).

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in llm_inference_engine.
Traceback (most recent call last):
  ...
RuntimeError: GPU Out-of-Memory Crash Caused by KV-Cache Internal Fragmentation
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_22_Distributed_LLM_Serving_PagedAttention_vLLM/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_llm_inference_engine.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_llm_inference_engine.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
