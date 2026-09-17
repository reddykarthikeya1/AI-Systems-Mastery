# 🐣 Interactive Foundations Playground: State Machine Graphs (LangGraph Internals)

> *"LangGraph is a workflow state machine: nodes compute work, and edges route the state dictionary."*

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
import copy
```

---

## 1. State Dictionary Transition Invariant

Nodes in a graph take an immutable state dictionary and return state updates that are merged into the global state.

```python
state = {"query": "Find books", "results": [], "step": 0}

def search_node(s):
    return {"results": ["Book A", "Book B"], "step": s["step"] + 1}

updates = search_node(state)
new_state = {**state, **updates}

assert new_state["step"] == 1
assert len(new_state["results"]) == 2
assert new_state["query"] == "Find books"
print(f"State transition successful: {new_state}")
```

---

## 2. Conditional Routing Edges

Router functions inspect the current state to dynamically pick the next destination node in the graph.

```python
def route_next(s):
    if len(s["results"]) > 0:
        return "summarize"
    return "retry_search"

next_node = route_next(new_state)
assert next_node == "summarize"
assert route_next({"results": []}) == "retry_search"
print(f"Conditional edge routed to '{next_node}' based on search results.")
```

---

## 3. Cycle and Checkpoint Snapshots

Saving state snapshots at every step allows rewinding execution or resuming after process crashes.

```python
checkpoints = []
checkpoints.append(copy.deepcopy(state))
checkpoints.append(copy.deepcopy(new_state))

assert len(checkpoints) == 2
assert checkpoints[0]["step"] == 0
assert checkpoints[1]["step"] == 1
print("Checkpoint history captured across state transitions.")
```

---
