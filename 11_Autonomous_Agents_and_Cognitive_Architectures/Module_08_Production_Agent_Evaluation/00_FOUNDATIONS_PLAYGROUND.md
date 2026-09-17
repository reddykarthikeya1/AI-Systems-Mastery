# 🐣 Interactive Foundations Playground: Production Agent Evaluation

> *"Evaluating agents is grading a workflow: did it accomplish the goal efficiently without wandering in circles?"*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Task Completion Success Rate

Success rate is the fraction of user benchmark tasks completed correctly without human intervention.

```python
tasks_evaluated = 50
tasks_successful = 44
success_rate = tasks_successful / tasks_evaluated

assert success_rate == 0.88
assert success_rate > 0.80
print(f"Agent benchmark accuracy: {success_rate:.1%} ({tasks_successful}/{tasks_evaluated})")
```

---

## 2. Average Steps to Resolution

Measuring efficiency: an agent that solves tasks in 3 steps is far cheaper and faster than one taking 15 steps.

```python
steps_per_task = [3, 4, 2, 5, 3]
avg_steps = sum(steps_per_task) / len(steps_per_task)

assert avg_steps == 3.4
assert avg_steps < 5.0
print(f"Average steps per completed task: {avg_steps:.1f}")
```

---

## 3. Tool Calling F1 Accuracy

Evaluating precision and recall of the specific tools called compared against human gold-standard trajectories.

```python
gold_tools = {"search", "calculator"}
called_tools = {"search", "calculator", "browse"}

tp = len(gold_tools & called_tools)
fp = len(called_tools - gold_tools)
precision = tp / (tp + fp)

assert precision == 2 / 3
assert tp == 2
print(f"Tool invocation precision: {precision:.2f}")
```

---
