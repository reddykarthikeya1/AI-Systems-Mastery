# Debug Lab Solution & Forensic Post-Mortem

## Incident: Speculative Decoding Emits Text the Target Model Never Verified

---

### Forensic Root Cause Analysis
`accept_draft_tokens()` keeps iterating over every position regardless of
whether an earlier position mismatched:

```python
for draft_tok, target_tok in zip(draft_tokens, target_tokens):
    if draft_tok == target_tok:
        accepted.append(draft_tok)
    else:
        accepted.append(target_tok)  # correct the mismatch and keep scanning
    return accepted
```

`target_model_verify()` computes its per-position outputs in a *single*
forward pass over `context + draft_tokens` -- i.e. `target_tokens[3]` is the
target model's prediction for "what comes after `context + draft[0:3]`",
where `draft[0:3]` includes the draft model's own (wrong) guess `"helpful"`
at position 2. The instant position 2 mismatches, every target-model
prediction at position 3 onward was conditioned on a prefix that never
actually happened (the real accepted prefix diverges to `"great"`, not
`"helpful"`, at that point). Those later "verified" tokens are therefore
meaningless, but the loop appends them anyway because it never stops after
the first mismatch -- it just keeps substituting in the (already-invalid)
target token at each remaining position.

---

### Production Corrective Action & Code Fix

```python
def accept_draft_tokens(draft_tokens, target_tokens):
    accepted = []
    for draft_tok, target_tok in zip(draft_tokens, target_tokens):
        if draft_tok == target_tok:
            accepted.append(draft_tok)
        else:
            accepted.append(target_tok)  # bonus token: target's true next token
            break  # everything after a mismatch was conditioned on a
                   # rejected draft continuation and cannot be trusted
    return accepted
```

With the fix, verification stops at the first mismatch, accepts `"is"` and
`"a"` from the draft, takes `"great"` as the target model's bonus token, and
then hands control back to the (expensive) target model to generate the next
token for real -- instead of fabricating `"helper"` and `"."` from an
already-invalidated forward pass.

---

### Production Prevention Invariants
1. **Stop at First Divergence:** Speculative-decoding acceptance must be a
   strict prefix match; the moment draft and target disagree, every later
   "verified" token from that same forward pass is invalid and must be
   discarded, not substituted in.
2. **Single Forward Pass, Single Valid Prefix:** Remember that the target
   model's per-position outputs from one batched verification pass are only
   meaningful up to the point where the conditioning context (the draft
   tokens) actually matches what gets accepted.
3. **Regression Test on a Known Divergence Point:** Cover this path with a
   fixture where the draft and target disagree at a fixed position and assert
   `len(accepted) == divergence_index + 1`, not `len(accepted) == len(draft)`.
