# Troubleshooting & Production Edge Cases

### 1. Clock Skew in Distributed Tracing
- **Symptom**: Child span duration appears negative or ends before parent span starts.
- **Root Cause**: Desynchronized system clocks across worker nodes.
- **Fix**: Use monotonic time (`time.monotonic()`) for span durations and synchronize server clocks via PTP/NTP.

### 2. Memory Leaks from Unclosed Spans
- **Symptom**: Application RAM consumption grows monotonically over days.
- **Root Cause**: Spans created without `with` context manager failed to close on unhandled exceptions.
- **Fix**: Always use context managers or `try...finally` to ensure `span.finish()` executes.
