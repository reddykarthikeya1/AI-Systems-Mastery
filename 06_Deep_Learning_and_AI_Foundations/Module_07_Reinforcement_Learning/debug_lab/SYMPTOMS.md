# Debug Lab Incident Report: Trained Bandit Agent Still Acts Almost Entirely at Random

- **Severity:** P2 Policy Convergence Failure
- **Affected Subsystem:** Module_07_Reinforcement_Learning
- **Reported Impact:** A multi-armed bandit agent is trained for 300 episodes so it can settle into exploiting the best-known arm. Instead, its exploration rate keeps climbing throughout training and is pinned at maximum by the end, so the final policy is barely more informed than random guessing.

---

## 🚨 Observable Symptoms & Logs
```text
Learned Q-values per arm: [0.203, 0.499, 0.905, 0.095]
Exploration rate (epsilon) at episode 0:   0.110
Exploration rate (epsilon) at episode 50:  0.610
Exploration rate (epsilon) at episode 150: 1.000
Exploration rate (epsilon) at episode 299: 1.000
Policy's preferred arm after training: 2 (true best arm is 2)
```
The exploration rate should shrink toward a small value like 0.01-0.05 as training progresses. Instead it grows every episode and hits the 1.0 ceiling well before training finishes.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_07_Reinforcement_Learning/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_epsilon_schedule.py
   ```
3. Watch the printed epsilon values increase across episodes instead of decreasing.

---

## 🎯 Your Objective
1. Inspect `broken_epsilon_schedule.py`'s `update_epsilon()` function.
2. Work out what should happen to `epsilon` as training progresses in a standard epsilon-greedy schedule, versus what the function actually does.
3. Formulate a hypothesis for why the agent never settles into exploiting its learned Q-values, then check `ANSWERS.md`.
