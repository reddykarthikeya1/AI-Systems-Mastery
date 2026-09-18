# Debug Lab Incident Report: Beam Search Forks Bleed Tokens Into Each Other

- **Severity:** P1 Generation Correctness
- **Affected Subsystem:** Module_03_PagedAttention_Architecture_vLLM
- **Reported Impact:** Parallel sampling / beam search requests that fork from
  a shared prompt prefix produce garbled completions: one beam's newly
  generated token shows up appended to a *different* beam's sequence.

---

## Observable Symptoms & Logs
```text
Before divergence, parent tokens: ['The', 'capital', 'of']
Before divergence, child tokens:  ['The', 'capital', 'of']

Expected: parent should read 'The capital of France' and child should
independently read 'The capital of Germany'.
Actual parent tokens: ['The', 'capital', 'of', 'France']
Actual child tokens:  ['The', 'capital', 'of', 'France', 'Germany']
```
The child sequence ends up containing both `France` and `Germany`, while the
parent is missing its own independent continuation. The two logical sequences
that were supposed to diverge after the fork are still writing into the same
physical memory.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_03_PagedAttention_Architecture_vLLM/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_paged_attention_cow.py
   ```
3. Observe that appending different tokens to the parent and the child after
   `fork()` does not keep their token lists independent.

---

## Your Objective
1. Inspect `PagedSequence.fork()` and `PagedSequence.append_token()`, and
   trace what happens to a `PhysicalBlock`'s `refcount` and `tokens` list when
   two sequences share it.
2. Compare against how PagedAttention is supposed to handle a block whose
   `refcount > 1`.
3. Formulate a hypothesis for why writes to one sequence appear in the other,
   then check `ANSWERS.md`.
