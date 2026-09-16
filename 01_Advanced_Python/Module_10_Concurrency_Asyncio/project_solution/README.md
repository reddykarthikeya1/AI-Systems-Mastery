# Design Rationale: Async Web Scraper Daemon & Ingestion Engine

## Architectural Overview
A cooperative asynchronous scraping daemon capable of querying hundreds of URLs concurrently using `asyncio`, rate-limiting semaphores, and structured task groups (`asyncio.TaskGroup`).

## Key Design Decisions
1. **Structured Concurrency with `TaskGroup`:** Using Python 3.11 `async with asyncio.TaskGroup()` ensures that if one task fails, sibling tasks are cancelled cleanly without leaving orphaned background jobs.
2. **`asyncio.Semaphore` Rate-Limiting:** Enforces bounded concurrency against external hostnames, protecting target servers and preventing local socket exhaustion.
3. **Non-Blocking Execution Guarantee:** All blocking legacy operations are offloaded using `asyncio.to_thread()`, keeping the single-threaded event loop responsive.

## Rejected Alternatives
1. **`asyncio.gather(*tasks)` Without Exception Shields:**
   - *Reason for Rejection:* When one task crashes in `gather()`, remaining tasks continue running unchecked in the background, leaking memory and network connections.
2. **Synchronous `time.sleep()` Inside Coroutines:**
   - *Reason for Rejection:* `time.sleep()` freezes the entire operating system thread, halting all other concurrent coroutines on the server.

## Invariants & Guarantees
- Event loop latency stays under 10 ms under load.
- Maximum concurrent outbound connections strictly respect semaphore bounds.

## Verification
```bash
pytest test_scraper_daemon.py -v
```
