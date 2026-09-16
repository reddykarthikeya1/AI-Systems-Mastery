"""Human-in-the-Loop (HITL) State Machine and Time-Travel Engine."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set


@dataclass
class SuspendedExecution:
    checkpoint_id: int
    paused_at_node: str
    state_snapshot: Dict[str, Any]
    pending_action: Dict[str, Any]


class HITLEngine:
    """Production HITL State Machine with Interrupts and Time Travel."""

    def __init__(
        self,
        nodes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]],
        edges: Dict[str, str],
        interrupt_before: Optional[Set[str]] = None,
    ) -> None:
        self.nodes = nodes
        self.edges = edges
        self.interrupt_before = interrupt_before or set()
        self.checkpoints: List[Dict[str, Any]] = []
        self.suspended_execution: Optional[SuspendedExecution] = None

    def run_until_interrupt(
        self,
        initial_state: Dict[str, Any],
        start_node: str,
        max_steps: int = 10,
    ) -> Dict[str, Any]:
        """Runs graph execution until END or an interrupt_before breakpoint is encountered."""
        state = copy.deepcopy(initial_state)
        curr = start_node
        self.checkpoints.clear()
        self.suspended_execution = None

        for step in range(1, max_steps + 1):
            if curr == "END":
                return {"status": "COMPLETED", "state": state}

            # Check if this node requires human approval
            if curr in self.interrupt_before:
                cp_id = len(self.checkpoints)
                self.suspended_execution = SuspendedExecution(
                    checkpoint_id=cp_id,
                    paused_at_node=curr,
                    state_snapshot=copy.deepcopy(state),
                    pending_action={"target_node": curr, "state": copy.deepcopy(state)},
                )
                return {
                    "status": "SUSPENDED",
                    "paused_at": curr,
                    "checkpoint_id": cp_id,
                    "state": state,
                }

            # Execute node
            update = self.nodes[curr](copy.deepcopy(state))
            state.update(update)

            self.checkpoints.append({
                "step": step,
                "node": curr,
                "state": copy.deepcopy(state),
            })

            curr = self.edges.get(curr, "END")

        return {"status": "MAX_STEPS_REACHED", "state": state}

    def resume(
        self,
        approved: bool,
        state_overrides: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resumes suspended execution after human approval/modification."""
        if not self.suspended_execution:
            raise RuntimeError("No suspended execution to resume.")

        if not approved:
            rejected_state = copy.deepcopy(self.suspended_execution.state_snapshot)
            rejected_state["approval_status"] = "REJECTED"
            self.suspended_execution = None
            return {"status": "REJECTED", "state": rejected_state}

        # Apply human state edits
        state = copy.deepcopy(self.suspended_execution.state_snapshot)
        if state_overrides:
            state.update(state_overrides)
        state["approval_status"] = "APPROVED"

        resume_node = self.suspended_execution.paused_at_node
        self.suspended_execution = None

        # Execute the paused node now that it is approved
        update = self.nodes[resume_node](copy.deepcopy(state))
        state.update(update)

        self.checkpoints.append({
            "step": len(self.checkpoints) + 1,
            "node": resume_node,
            "state": copy.deepcopy(state),
        })

        next_node = self.edges.get(resume_node, "END")
        if next_node == "END":
            return {"status": "COMPLETED", "state": state}

        # Continue remaining nodes
        return self.run_until_interrupt(state, start_node=next_node)

    def time_travel_rewind(self, step_idx: int) -> Dict[str, Any]:
        """Rewinds state to a specific checkpoint index."""
        if 0 <= step_idx < len(self.checkpoints):
            return copy.deepcopy(self.checkpoints[step_idx]["state"])
        raise IndexError(f"Checkpoint index {step_idx} out of range.")
