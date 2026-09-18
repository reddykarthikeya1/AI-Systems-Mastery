# Debug Lab Solution & Forensic Post-Mortem

## Incident: Trained Bandit Agent Still Acts Almost Entirely at Random

---

### 🔍 Forensic Root Cause Analysis
`update_epsilon()` returns `epsilon + decay_rate`, increasing the exploration rate every episode instead of decaying it. A standard epsilon-greedy schedule should shrink `epsilon` toward zero over time (e.g. `epsilon - decay_rate`, or a multiplicative decay) so the agent exploits its learned Q-values more and more often. With the sign flipped, `epsilon` grows until it is clamped at `1.0`, meaning the agent is choosing a uniformly random action almost every single step, even very late in training -- it never converges to a stable, mostly greedy policy.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def update_epsilon(epsilon, decay_rate=0.01):
    return max(0.01, epsilon - decay_rate)
```

With the decay direction corrected, `epsilon` shrinks toward its floor of `0.01` well before training ends, and the agent spends most of its later episodes exploiting the best-known arm.

---

### 🛡️ Production Prevention Invariants
1. **Schedule Assertions:** Assert that any decay schedule is monotonically moving toward its target bound (e.g. `epsilon[t+1] <= epsilon[t]`).
2. **Convergence Metrics:** Log the fraction of greedy (non-random) actions taken in the last N episodes and alert if it never approaches 1.0.
3. **Schedule Unit Tests:** Test the decay function in isolation across many steps and assert it reaches its floor within the expected number of episodes.
