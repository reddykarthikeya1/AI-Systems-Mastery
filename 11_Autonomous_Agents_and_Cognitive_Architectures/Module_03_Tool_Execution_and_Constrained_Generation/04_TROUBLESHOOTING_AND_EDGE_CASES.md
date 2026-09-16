# Troubleshooting & Production Edge Cases

### 1. Parameter Name Mismatch in Schema Dispatch
- **Symptom**: `TypeError: got unexpected keyword argument 'query_text'`.
- **Root Cause**: LLM renamed the parameter from `query` to `query_text` based on vague docstring instructions.
- **Fix**: Align docstring argument descriptions precisely with parameter identifiers.

### 2. Thread Leak on Timeout Tool Cancellation
- **Symptom**: High memory usage and thread count growth after tool timeouts.
- **Root Cause**: Python threads cannot be forcefully killed in `ThreadPoolExecutor`.
- **Fix**: Use subprocess-based isolation (`multiprocessing.Process` or dedicated worker pools) for tools that might hang indefinitely.
