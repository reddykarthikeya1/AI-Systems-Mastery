# Troubleshooting & Production Edge Cases

### 1. Tool Call Parsing Failures Due to Hallucinated Markdown
- **Symptom**: `parse_agent_output` raises `ParseError: Could not find Action/Action Input block`.
- **Root Cause**: LLM wrapped JSON inside ````markdown ```` code blocks with conversational preamble.
- **Fix**: Use regex with optional markdown block stripping: `r"```(?:json)?\s*({.*?})\s*```"`.

### 2. Zombie Agent Processes During Tool Timeouts
- **Symptom**: Agent worker threads hang indefinitely on external HTTP or database queries.
- **Root Cause**: Tool implementation lacks socket timeouts (`timeout=None`).
- **Fix**: Wrap all tool invocations inside `concurrent.futures.ThreadPoolExecutor` with strict `future.result(timeout=10.0)`.

### 3. State Poisoning from Oversized Tool Observations
- **Symptom**: LLM produces garbled output or crashes with `ContextWindowExceededError` after a `ReadFile` or `WebSearch` call.
- **Root Cause**: Tool returned a 2 MB HTML file or raw minified JavaScript dump.
- **Fix**: Truncate all tool observations to a strict maximum token/character ceiling (e.g., 2,000 characters) with a clear notification: `[Observation truncated: 24,500 characters omitted]`.
