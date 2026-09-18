# Debug Lab Solution & Forensic Post-Mortem

## Incident: Blocked Online-Softmax Attention Output Diverges From Full Softmax

---

### 🔍 Forensic Root Cause Analysis
Online softmax keeps a running max `m`, a running denominator `l`, and a running numerator accumulator `acc`, all expressed relative to the *current* running max. Every time a new block raises the running max from `m_old` to `m_new`, every quantity computed under the old max is stale by a factor of `exp(m_old - m_new) = alpha` and must be rescaled before new contributions are added. `flash_attention_blocked()` correctly rescales `running_sum` (`running_sum = running_sum * alpha + block_sum`), but `acc` is only ever *added to* (`acc = acc + sum(w * v ...)`) and never multiplied by `alpha`. The numerator and denominator drift out of sync: the denominator reflects the correct current scale, while the numerator still carries un-rescaled contributions from earlier blocks computed under a smaller (looser) max, so they are effectively over-weighted relative to later blocks. The final `acc / running_sum` division blends a correctly-scaled denominator with an incorrectly-scaled numerator, producing an output far from the true softmax-weighted average.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def flash_attention_blocked(score_blocks, value_blocks):
    running_max = -math.inf
    running_sum = 0.0
    acc = 0.0
    for scores, values in zip(score_blocks, value_blocks):
        block_max = max(scores)
        new_max = max(running_max, block_max)
        alpha = math.exp(running_max - new_max) if running_max != -math.inf else 0.0

        block_weights = [math.exp(s - new_max) for s in scores]
        block_sum = sum(block_weights)

        running_sum = running_sum * alpha + block_sum
        acc = acc * alpha + sum(w * v for w, v in zip(block_weights, values))  # rescale acc too

        running_max = new_max
    return acc / running_sum
```

---

### 🛡️ Production Prevention Invariants
1. **Rescale Every Running Quantity Together:** Whenever the running max changes, every accumulator expressed relative to it (numerator *and* denominator, and in multi-head kernels each head's output accumulator) must be rescaled by the same `alpha` in the same step.
2. **Cross-Check Against a Single-Pass Reference:** Validate any blocked/online reduction against a full, single-pass softmax over the same data with block boundaries that force at least one max update, since a single block (no max revision) can mask this bug entirely.
3. **Assert Invariants, Not Just Outputs:** In development builds, assert that `running_sum` after each block equals `sum(exp(s - running_max) for s in scores_seen_so_far)` to catch a desynced accumulator before it reaches production.
