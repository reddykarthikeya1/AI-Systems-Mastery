# 🐣 Interactive Foundations Playground: Reinforcement Learning & Q-Learning

> *"Reinforcement learning is training a dog with treats: reward good actions, ignore bad ones."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Bellman Equation for Q-Value Update

The Bellman equation updates action-value $Q(s, a) \leftarrow Q(s, a) + \alpha [R + \gamma \max_{a'} Q(s', a') - Q(s, a)]$.

```python
q_val = 2.0
reward = 5.0
gamma = 0.9
next_max_q = 3.0
alpha = 0.5

td_target = reward + gamma * next_max_q
td_error = td_target - q_val
new_q = q_val + alpha * td_error

assert td_target == 5.0 + 0.9 * 3.0  # 7.7
assert td_error == 5.7
assert new_q == 2.0 + 0.5 * 5.7      # 4.85
print(f"Updated Q-value from {q_val} to {new_q}")
```

---

## 2. Epsilon-Greedy Exploration vs Exploitation

With probability $\epsilon$ explore a random action; with probability $1 - \epsilon$ exploit the action with highest estimated value.

```python
q_table = {"left": 1.5, "right": 4.2}
def exploit(table):
    return max(table, key=table.get)

best_action = exploit(q_table)
assert best_action == "right"
assert q_table[best_action] == 4.2
print(f"Exploitation picked highest-value action: '{best_action}'")
```

---

## 3. Discounted Cumulative Return Calculation

Future rewards are discounted by factor $\gamma^t$: $G_t = \sum_{k=0}^T \gamma^k R_{t+k+1}$.

```python
rewards = [1.0, 1.0, 1.0]
gamma = 0.9
discounted_return = sum(r * (gamma**t) for t, r in enumerate(rewards))

expected_return = 1.0 + 0.9 + 0.81
assert abs(discounted_return - expected_return) < 1e-6
assert discounted_return == 2.71
print(f"Discounted cumulative return over 3 steps: {discounted_return}")
```

---
