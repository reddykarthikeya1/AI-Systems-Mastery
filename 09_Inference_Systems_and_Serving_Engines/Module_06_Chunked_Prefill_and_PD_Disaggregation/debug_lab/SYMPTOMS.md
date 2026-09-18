# Debug Lab Incident Report: Decode Node Generates From a Truncated Prompt

- **Severity:** P1 Generation Correctness
- **Affected Subsystem:** Module_06_Chunked_Prefill_and_PD_Disaggregation
- **Reported Impact:** In the prefill/decode (PD) disaggregated deployment,
  long prompts intermittently produce completions that ignore most of the
  prompt -- as though the model only ever saw the last few sentences instead
  of the full input.

---

## Observable Symptoms & Logs
```text
Original prompt (14 tokens): The quick brown fox jumps over the lazy dog near the river bank .
Chunked into 4 chunks of size 4: [['The', 'quick', 'brown', 'fox'], ['jumps', 'over', 'the', 'lazy'], ['dog', 'near', 'the', 'river'], ['bank', '.']]
Expected: decode worker reassembles all 14 tokens in order before generating.
Actual tokens received by decode worker (6 tokens): dog near the river bank .
```
The prefill node chunked and (presumably) processed all 14 tokens, but the
decode node only ever reassembles 6 of them -- the earliest chunks of the
prompt are simply gone by the time decode starts.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_06_Chunked_Prefill_and_PD_Disaggregation/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_pd_kv_transfer.py
   ```
3. Observe that the decode worker's reassembled token count is smaller than
   the original prompt's token count, and that specific early chunks are
   missing.

---

## Your Objective
1. Inspect `prefill_worker_send()` and trace how `slot` is computed for each
   chunk, and what happens when two different chunks map to the same slot.
2. Compare the number of transfer slots (`NUM_TRANSFER_SLOTS`) against the
   number of chunks the prompt actually produces.
3. Formulate a hypothesis for why later chunks silently erase earlier ones
   before decode ever reads them, then check `ANSWERS.md`.
