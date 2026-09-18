# Debug Lab Incident Report: Blocked Online-Softmax Attention Output Diverges From Full Softmax

- **Severity:** P1 Numerical Correctness
- **Affected Subsystem:** Module_08_FlashAttention_1_and_2_Internals
- **Reported Impact:** A FlashAttention-style blocked online-softmax reduction over three score/value blocks is checked against a plain full-softmax reference computed over the same six scores and values in one shot. The blocked version's weighted output is nowhere close to the reference.

---

## 🚨 Observable Symptoms & Logs
```text
Scores: [1.0, 2.0, 3.0, 0.5, 4.0, 1.5]
Full-softmax reference output:  33.401639
Blocked online-softmax output:  57.239777
Absolute difference: 23.838137
```
Both functions compute a softmax-weighted average of the same `values` under the same `scores`; mathematically they should agree to within floating-point tolerance. Instead the blocked version overshoots by more than 70%.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_08_FlashAttention_1_and_2_Internals/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_online_softmax.py
   ```
3. Compare the reference output line against the blocked online-softmax output line.

---

## 🎯 Your Objective
1. Inspect `broken_online_softmax.py`'s `flash_attention_blocked()` function, specifically what happens to `running_max`, `running_sum`, and `acc` each time a new block raises the running max (`alpha = exp(running_max - new_max)`).
2. Work out which of `running_sum` and `acc` gets multiplied by `alpha` when the max is revised, and which one does not.
3. Formulate a hypothesis for why every earlier block's contribution to `acc` becomes stale once a later block raises the max, then check `ANSWERS.md`.
