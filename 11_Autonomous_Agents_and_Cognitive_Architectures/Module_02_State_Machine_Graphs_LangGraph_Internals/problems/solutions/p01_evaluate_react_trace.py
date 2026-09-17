"""Reference Solution — Problem 01: evaluate_react_trace

Topic: State Machine Graphs LangGraph Internals
"""

from __future__ import annotations

def evaluate_react_trace(steps: list[dict[str, str]], max_steps: int = 10) -> dict[str, bool | int | str]:
    if len(steps) > max_steps:
        return {"success": False, "status": "BUDGET_EXCEEDED", "step_count": len(steps)}
    valid_transitions = {"thought": "action", "action": "observation", "observation": "thought"}
    prev_type = None
    for s in steps:
        stype = s.get("type")
        if prev_type and valid_transitions.get(prev_type) != stype and stype != "finish":
            return {"success": False, "status": "INVALID_TRANSITION", "step_count": len(steps)}
        prev_type = stype
    last_step = steps[-1].get("type") if steps else None
    success = (last_step == "finish")
    return {"success": success, "status": "COMPLETE" if success else "INCOMPLETE", "step_count": len(steps)}

