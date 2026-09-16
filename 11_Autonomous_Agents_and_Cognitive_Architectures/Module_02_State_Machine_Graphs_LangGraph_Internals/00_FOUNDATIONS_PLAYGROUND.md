# Beginner Playground: State Graphs & Pregel Engine


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to State Graphs! Modern enterprise agent frameworks like **LangGraph** discard simple linear chains in favor of **Cyclic State Graphs** powered by the Pregel computation model.

---

## 1. The Core Mental Model: Pregel State Machines

A state machine graph consists of:
1. **Shared State**: A central dictionary or typed object where all nodes read and write.
2. **Nodes**: Pure or stateful functions that receive the current state and return updates.
3. **Channels & Reducers**: Rules for merging updates into the state (e.g. `append` vs `overwrite`).
4. **Conditional Edges**: Decision functions that inspect state and choose which node executes next.

```
       [ START ]
           |
           v
     +------------+
     | Node: Plan | <----------------+ (Cyclic Loop)
     +------------+                  |
           |                         |
           v                         |
     +------------+                  |
     | Node: Exec |                  |
     +------------+                  |
           |                         |
    [ Condition: Done? ] -- (No) ----+
           |
         (Yes)
           v
        [ END ]
```

---

## 2. Interactive Pure-Python Experiment: Zero-Dependency Graph Engine

```python
from typing import Dict, Any, Callable, List

class MiniStateGraph:
    def __init__(self):
        self.nodes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Callable[[Dict[str, Any]], str]] = {}

    def add_node(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.nodes[name] = func

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, condition_fn: Callable[[Dict[str, Any]], str]):
        self.conditional_edges[from_node] = condition_fn

    def compile_and_run(self, initial_state: Dict[str, Any], start_node: str, max_steps: int = 10):
        state = dict(initial_state)
        curr = start_node
        print(f"Initial State: {state}")

        for step in range(1, max_steps + 1):
            if curr == "END":
                print(f"[Done] Reached END at step {step}")
                break
            print(f"Step {step}: Executing Node '{curr}'")
            node_func = self.nodes[curr]
            update = node_func(state)
            state.update(update)

            # Routing
            if curr in self.conditional_edges:
                router = self.conditional_edges[curr]
                curr = router(state)
            elif curr in self.edges:
                curr = self.edges[curr]
            else:
                curr = "END"
        return state

# Test graph with iteration counter
def increment_counter(state):
    return {"counter": state.get("counter", 0) + 1}

def should_continue(state):
    if state["counter"] >= 3:
        return "END"
    return "loop_node"

graph = MiniStateGraph()
graph.add_node("loop_node", increment_counter)
graph.add_conditional_edge("loop_node", should_continue)

final = graph.compile_and_run({"counter": 0}, start_node="loop_node")
print(f"Final Output State: {final}")
```
