# Beginner Playground: Agent Trajectory Evaluation

Welcome to Agent Evaluation! Evaluating an LLM agent is vastly harder than evaluating single-turn QA because an agent takes multi-step exploratory paths.

---

## 1. The Core Mental Model: Trajectory Scoring

To evaluate an agent, we score three core pillars:
1. **Goal Success (Pass/Fail)**: Did the agent resolve the user's issue (e.g. passing unit tests)?
2. **Step Efficiency**: Did the agent take the optimal path, or wander aimlessly for 20 tool calls?
3. **Tool Call Accuracy**: Did the agent call tools with valid arguments without hallucinating parameters?

```
 Optimal Path:   [ Search ] ---------------------> [ Edit ] -> (Pass)
 Wandering Path: [ Search ] -> [ Error ] -> [ Search ] -> [ Read ] -> [ Edit ] -> (Pass)
```

---

## 2. Interactive Pure-Python Experiment: Trajectory Metrics Calculator

```python
def calculate_step_efficiency(optimal_steps: int, actual_steps: int) -> float:
    """Calculates efficiency ratio bounded in [0.0, 1.0]."""
    if actual_steps <= 0:
        return 0.0
    return min(1.0, optimal_steps / actual_steps)

def calculate_tool_precision(total_calls: int, invalid_or_error_calls: int) -> float:
    if total_calls == 0:
        return 1.0
    return max(0.0, (total_calls - invalid_or_error_calls) / total_calls)

print(f"Optimal Trajectory Efficiency: {calculate_step_efficiency(3, 3):.2f}")
print(f"Wandering Trajectory Efficiency: {calculate_step_efficiency(3, 9):.2f}")
print(f"Tool Precision (1 error in 5 calls): {calculate_tool_precision(5, 1):.2f}")
```
