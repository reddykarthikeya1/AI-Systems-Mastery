# Debug Lab: Module 10 — Asyncio Traps

## How to Run
```bash
python debug_lab/broken_scraper.py
```

## Observed Symptoms
1. **Serial execution instead of concurrency**:
   Two 0.5s requests take 1.0s because `time.sleep()` blocks the OS thread running the single-threaded event loop.
2. **RuntimeWarning / un-executed coroutine**:
   ```
   RuntimeWarning: coroutine 'fetch_url' was never awaited
   ```
   The return value is `<coroutine object fetch_url at ...>` instead of actual data.
3. **Unretrieved task exception warning**:
   ```
   Task exception was never retrieved
   ConnectionResetError: Remote server terminated connection
   ```
