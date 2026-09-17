"""Beginner playground for Module 07 - Reinforcement Learning & Q-Learning.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Bellman Equation for Q-Value Update
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

# -------------------------------------------- 2. Epsilon-Greedy Exploration vs Exploitation
q_table = {"left": 1.5, "right": 4.2}
def exploit(table):
    return max(table, key=table.get)

best_action = exploit(q_table)
assert best_action == "right"
assert q_table[best_action] == 4.2
print(f"Exploitation picked highest-value action: '{best_action}'")

# -------------------------------------------- 3. Discounted Cumulative Return Calculation
rewards = [1.0, 1.0, 1.0]
gamma = 0.9
discounted_return = sum(r * (gamma**t) for t, r in enumerate(rewards))

expected_return = 1.0 + 0.9 + 0.81
assert abs(discounted_return - expected_return) < 1e-6
assert discounted_return == 2.71
print(f"Discounted cumulative return over 3 steps: {discounted_return}")

print()
print("All checks passed.")
