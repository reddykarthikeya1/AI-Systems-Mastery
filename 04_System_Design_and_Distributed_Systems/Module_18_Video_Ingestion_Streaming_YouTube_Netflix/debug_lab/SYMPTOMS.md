# Debug Lab Incident Report: Transcoding Worker OOM Crash on Unbounded Video Resolution Ingestion

- **Severity:** P1 Transcoding Pipeline Failure
- **Affected Subsystem:** Module_18_Video_Ingestion_Streaming_YouTube_Netflix
- **Reported Impact:** Workers crashed when processing an uncompressed 8K 60fps video upload because the entire video frame buffer was read into RAM.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in video_pipeline.
Traceback (most recent call last):
  ...
RuntimeError: Transcoding Worker OOM Crash on Unbounded Video Resolution Ingestion
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_18_Video_Ingestion_Streaming_YouTube_Netflix/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_video_pipeline.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_video_pipeline.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
