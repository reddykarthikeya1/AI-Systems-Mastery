# Debug Lab Incident Report: Speculative Decoding Emits Text the Target Model Never Verified

- **Severity:** P1 Generation Correctness
- **Affected Subsystem:** Module_07_Speculative_Decoding_Architectures
- **Reported Impact:** Outputs from the speculative-decoding path occasionally
  contain fluent but subtly wrong continuations that neither the draft nor
  the target model would have produced on their own, most visible right after
  a draft/target disagreement.

---

## Observable Symptoms & Logs
```text
Draft model proposed:  ['is', 'a', 'helpful', 'assistant', 'today']
Target model verified: ['is', 'a', 'great', 'helper', '.']
Expected: accept the verified prefix up to and including the first mismatch
position, then discard everything after it (draft tokens past a rejection
were never actually checked against the true continuation).
Actual accepted sequence: ['is', 'a', 'great', 'helper', '.']
Final sentence: 'You ' + 'is a great helper .'
```
The draft and target models disagree starting at position 2 (`helpful` vs.
`great`), yet the accepted sequence still includes tokens 3 and 4
(`helper`, `.`) as if they had been verified, even though the target model's
values there were only ever computed against the draft's rejected
continuation.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_07_Speculative_Decoding_Architectures/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_speculative_verify.py
   ```
3. Observe that the accepted sequence has the same length as the full draft
   proposal, with every mismatched position silently swapped in place, rather
   than stopping at the first mismatch.

---

## Your Objective
1. Inspect `accept_draft_tokens()` and trace what it does the moment
   `draft_tok != target_tok`.
2. Consider how `target_model_verify()` computed its per-position
   predictions -- what context was each one conditioned on?
3. Formulate a hypothesis for why accepting tokens past the first mismatch is
   unsound, then check `ANSWERS.md`.
