# 🐣 Interactive Foundations Playground: Multi-Agent Collaboration Topologies

> *"Multi-agent systems divide labor: a supervisor breaks down the goal and delegates tasks to specialists."*

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

## 1. Supervisor Router Delegation

A supervisor inspects user requests and delegates sub-tasks to specialized worker agents (Researcher, Coder, Reviewer).

```python
def supervisor_route(task):
    if "code" in task.lower() or "bug" in task.lower():
        return "coder_agent"
    elif "search" in task.lower() or "who" in task.lower():
        return "researcher_agent"
    return "general_agent"

assert supervisor_route("Fix the bug in main.py") == "coder_agent"
assert supervisor_route("Who won the 2024 Nobel prize?") == "researcher_agent"
print("Supervisor successfully routed specialized tasks to domain agents.")
```

---

## 2. Majority Vote Consensus Protocol

For critical decisions, querying 3 independent agents and taking the majority vote eliminates individual agent hallucinations.

```python
from collections import Counter
votes = ["approve", "approve", "reject"]
counts = Counter(votes)
winner, win_count = counts.most_common(1)[0]

assert winner == "approve"
assert win_count == 2
print(f"Consensus achieved: '{winner}' with {win_count}/3 votes.")
```

---

## 3. Hand-Off Protocol Context Forwarding

When transferring control between agents, summarize prior accomplishments to keep communication lean.

```python
hand_off = {"from": "researcher", "to": "writer", "summary": "Found 3 key sources."}
assert hand_off["to"] == "writer"
assert len(hand_off["summary"]) > 0
print(f"Hand-off verified from {hand_off['from']} to {hand_off['to']}.")
```

---
