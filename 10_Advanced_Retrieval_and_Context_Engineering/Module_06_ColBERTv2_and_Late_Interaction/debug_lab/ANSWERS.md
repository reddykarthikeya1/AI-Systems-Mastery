# Debug Lab Solution & Forensic Post-Mortem

## Incident: Late-Interaction Scoring Prefers Mediocre-Everywhere Docs Over Exact Matches

---

### Forensic Root Cause Analysis
For each query token, `late_interaction_score()` reduces the list of
per-document-token similarities with a mean, not a max:

```python
for q_emb in query_token_embs:
    sims = [cosine_sim(q_emb, d_emb) for d_emb in doc_token_embs]
    total += sum(sims) / len(sims)
```

This is exactly mean-pooling, the very late-interaction alternative ColBERT's
MaxSim was designed to avoid. Under mean-pooling, `doc_A`'s excellent match
(~0.99 similarity for the "exceptions" token) gets averaged together with its
other, irrelevant token (a strongly *negative* similarity of about -0.70 to
the same query token), dragging the per-query-token contribution down toward
zero. `doc_B`, whose two tokens are both mildly positive matches to
everything, has no single great match but also no bad one to average against,
so its mean stays solidly positive across both query tokens. MaxSim exists
specifically so a document is not punished for having *some* unrelated
tokens, as long as it has a great match for each important query term; mean
pooling reintroduces exactly that punishment.

---

### Production Corrective Action & Code Fix

```python
def late_interaction_score(query_token_embs, doc_token_embs):
    total = 0.0
    for q_emb in query_token_embs:
        sims = [cosine_sim(q_emb, d_emb) for d_emb in doc_token_embs]
        total += max(sims)  # MaxSim: best-matching document token per query token
    return total
```

With `max(sims)` in place of the mean, `doc_A`'s ~0.99 match for
`"exceptions"` and its still-decent match for `"python"` dominate its score,
correctly pushing `score_a` above `score_b`.

---

### Production Prevention Invariants
1. **Name the Reduction After What It Does:** A function or variable called
   `late_interaction_score` / `maxsim_score` should be grep-able back to an
   actual `max()` call; a mean hiding under a MaxSim name is a naming/logic
   mismatch worth flagging in review.
2. **One-Exact-Match Fixture Test:** Cover late-interaction scoring with a
   fixture exactly like this one -- one document with a single excellent
   token match plus noise, versus one document with uniformly mediocre
   matches -- and assert the exact-match document wins.
3. **Compare Against Mean-Pooling Baseline:** When validating a late-
   interaction implementation, deliberately compute the mean-pooled score as
   a negative baseline and assert the two rankings differ on documents with
   exactly this "one great match plus noise" shape.
