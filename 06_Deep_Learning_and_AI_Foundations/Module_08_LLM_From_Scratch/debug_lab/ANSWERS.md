# Debug Lab Solution & Forensic Post-Mortem

## Incident: Greedy Decoder Gets Stuck Repeating One Token

---

### 🔍 Forensic Root Cause Analysis
Inside the generation loop, `next_token` is computed from `table.get(current, ...)` and appended to `generated`, but `current` itself is never reassigned to `next_token`. Every iteration therefore looks up the successor of the *original* start token instead of the most recently generated one, so the loop repeatedly produces the same next-token prediction instead of advancing through the chain.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def greedy_generate(start_token, table, max_tokens=8):
    current = start_token
    generated = [current]
    for _ in range(max_tokens - 1):
        next_token = table.get(current, "<end>")
        generated.append(next_token)
        current = next_token   # advance the context before the next lookup
    return generated
```

With `current` advanced each step, the decoder correctly walks the chain `the -> cat -> sat -> on -> the -> cat -> ...`, producing a varied sequence instead of one repeated token.

---

### 🛡️ Production Prevention Invariants
1. **Diversity Metrics:** Track the ratio of unique to total generated tokens in generation tests and flag sequences that collapse toward a single token.
2. **State-Advance Tests:** Unit test that the decoding loop's context variable changes value across at least the first few generation steps.
3. **Golden-Sequence Regression:** Keep a small deterministic lookup table with a known expected output sequence as a standing regression test for the decoder.
