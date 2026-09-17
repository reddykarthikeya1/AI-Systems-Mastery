"""Beginner playground for Module 08 - Production Agent Evaluation.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Task Completion Success Rate
tasks_evaluated = 50
tasks_successful = 44
success_rate = tasks_successful / tasks_evaluated

assert success_rate == 0.88
assert success_rate > 0.80
print(f"Agent benchmark accuracy: {success_rate:.1%} ({tasks_successful}/{tasks_evaluated})")

# -------------------------------------------- 2. Average Steps to Resolution
steps_per_task = [3, 4, 2, 5, 3]
avg_steps = sum(steps_per_task) / len(steps_per_task)

assert avg_steps == 3.4
assert avg_steps < 5.0
print(f"Average steps per completed task: {avg_steps:.1f}")

# -------------------------------------------- 3. Tool Calling F1 Accuracy
gold_tools = {"search", "calculator"}
called_tools = {"search", "calculator", "browse"}

tp = len(gold_tools & called_tools)
fp = len(called_tools - gold_tools)
precision = tp / (tp + fp)

assert precision == 2 / 3
assert tp == 2
print(f"Tool invocation precision: {precision:.2f}")

print()
print("All checks passed.")
