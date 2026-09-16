# Module_09_Concurrency_Threading_Multiprocessing: Project Implementation Guide

**Deliverable:** a hybrid concurrent pipeline combining thread pools for I/O and process pools for CPU-bound hashing and transcoding.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_pipeline.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Threaded I/O Worker
Implement `download_item` using `concurrent.futures.ThreadPoolExecutor` to execute multiple network/disk I/O operations concurrently.

### Step 2 — CPU-Bound Worker Function
Implement `transcode_and_hash(item)` as a top-level function so it can be pickled and spawned across worker processes on Windows and Linux.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_pipeline.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Process Pool Parallelism
Execute the CPU-bound hashing workload in `concurrent.futures.ProcessPoolExecutor` to bypass the GIL and achieve true multicore parallelism.

### Step 4 — Safe Aggregation & Synchronization
Collect worker results using `as_completed` and update shared metrics using a `threading.Lock()`.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/pipeline.py`, replace the `ProcessPoolExecutor` with a `ThreadPoolExecutor` for the CPU-bound hashing stage.
Run:
```bash
pytest ../project_solution/test_pipeline.py -k test_perf_multiprocessing_beats_threading_cpu -v
```
Watch the test fail because the GIL serializes CPU execution across threads, then restore the process pool.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_pipeline.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Zero-Copy Shared Memory:** Refactor large array transfer between processes using `multiprocessing.shared_memory`.
2. **Dynamic Worker Sizing:** Auto-tune thread pool size based on active queue latency and process pool size based on `os.cpu_count()`.
3. **Graceful Worker Cancellation:** Handle worker termination signals and cancel pending futures cleanly.
4. **IPC Queue Backpressure:** Implement bounded `multiprocessing.Queue` to prevent memory exhaustion under high ingest rates.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_pipeline_e2e_processing` | Proves items pass through download, processing, and hashing successfully |
| `test_perf_multiprocessing_beats_threading_cpu` | Proves multiprocessing executes CPU-bound work faster than threading |
| `test_perf_threading_beats_sequential_io` | Proves thread pools execute I/O-bound tasks faster than sequential calls |
| `test_error_handling_in_worker_pool` | Proves exceptions inside worker futures are surfaced without hanging |
| `test_thread_safe_counter_updates` | Proves locks prevent lost updates in shared progress counters |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain the Global Interpreter Lock (GIL) and why threads do not accelerate CPU-bound Python code
- [ ] Choose correctly between ThreadPoolExecutor, ProcessPoolExecutor, and asyncio for a given workload
- [ ] Write picklable worker functions compatible with Windows spawn process creation
- [ ] Synchronize shared state safely using Locks, Semaphores, and Barriers
- [ ] Prevent deadlocks by establishing consistent lock acquisition hierarchies
- [ ] Handle worker exceptions cleanly using concurrent.futures.as_completed
- [ ] Measure and verify multicore speedups using automated performance assertions
