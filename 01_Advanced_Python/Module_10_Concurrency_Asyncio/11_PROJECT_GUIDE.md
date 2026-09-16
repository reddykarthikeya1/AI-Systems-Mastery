# Module_10_Concurrency_Asyncio: Project Implementation Guide

**Deliverable:** a high-throughput async scraping daemon with rate limiting, task timeouts, retry backoff, and concurrent gather execution.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_scraper_daemon.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Basic Coroutine Execution
Implement `fetch_page(url, client)` as an `async def` function using non-blocking asynchronous HTTP calls.

### Step 2 — Rate Limiting with Semaphores
Wrap concurrent fetches with an `asyncio.Semaphore(max_concurrency)` to prevent overwhelming target services.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_scraper_daemon.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Timeout and Cancellation
Implement `asyncio.wait_for` to cancel requests exceeding the allowed deadline cleanly.

### Step 4 — Batch Ingestion with asyncio.gather
Orchestrate batch requests with `asyncio.gather(*tasks, return_exceptions=True)` to ensure partial failures do not abort the entire batch.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/scraper_daemon.py`, replace `await asyncio.gather(...)` with a sequential loop: `for url in urls: await fetch_page(url)`.
Run:
```bash
pytest ../project_solution/test_scraper_daemon.py -k test_perf_gather_beats_sequential -v
```
Watch the test fail as execution time jumps from concurrent to sequential, then restore `asyncio.gather`.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_scraper_daemon.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Token Bucket Async Rate Limiter:** Build a sliding-window token bucket algorithm using `asyncio.Event`.
2. **Dynamic Task Queue Worker Pool:** Implement persistent worker coroutines consuming from an `asyncio.Queue`.
3. **Async Context Manager Client:** Implement `async with ScraperDaemon() as scraper:` managing client session lifespan.
4. **Signal-Aware Graceful Drain:** Trap SIGINT/SIGTERM and drain in-flight tasks before shutting down the event loop.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_scraper_single_fetch_success` | Proves single page fetch returns parsed HTML payload |
| `test_scraper_concurrency_semaphore` | Proves semaphore caps in-flight concurrent requests |
| `test_scraper_timeout_handling` | Proves slow endpoints trigger TimeoutError cleanly |
| `test_perf_gather_beats_sequential` | Proves concurrent gather executes substantially faster than sequential awaits |
| `test_scraper_partial_failures_isolated` | Proves failing URLs do not prevent successful URLs from completing |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain the single-threaded cooperative event loop architecture of asyncio
- [ ] Use await, asyncio.create_task, and asyncio.gather correctly
- [ ] Protect against blocking the event loop with synchronous calls or time.sleep
- [ ] Control concurrent resource access using asyncio.Semaphore and asyncio.Lock
- [ ] Implement timeouts and task cancellations using asyncio.wait_for
- [ ] Handle background task exceptions without triggering unretrieved task warnings
- [ ] Write unit tests for async functions using pytest-asyncio
