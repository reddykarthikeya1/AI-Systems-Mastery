# 🐣 Interactive Foundations Playground: Human-in-the-Loop & Time Travel

> *"Human-in-the-loop gives humans an emergency brake: high-stakes actions require human approval before execution."*

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
import json
```

---

## 1. Approval Interrupt Gate

If an agent proposes an irreversible side effect (e.g. deleting a database table or sending payments), pause and require human sign-off.

```python
def requires_human_approval(action_type):
    critical_actions = {"transfer_money", "delete_record", "deploy_production"}
    return action_type in critical_actions

assert requires_human_approval("transfer_money") is True
assert requires_human_approval("search_database") is False
print("Approval gate correctly categorized sensitive actions.")
```

---

## 2. Approval / Rejection State Fork

When human rejects an action, the agent state receives a rejection event with feedback to take an alternate path.

```python
state = {"action": "delete_table", "status": "pending_approval"}
human_approved = False

if not human_approved:
    state["status"] = "rejected"
    state["feedback"] = "User disallowed table deletion. Archive instead."

assert state["status"] == "rejected"
assert "Archive instead" in state["feedback"]
print(f"Handled human feedback: {state['feedback']}")
```

---

## 3. Time Travel State Rewind

Restoring state from checkpoint index $t-1$ rewinds history back before an error occurred.

```python
history = ["state_0", "state_1_bad", "state_2_crashed"]
rewound_state = history[0]
assert rewound_state == "state_0"
print(f"Time travel rewound state back to: {rewound_state}")
```

---
