"""Pregel Cyclic State Graph Engine with Checkpointing and Reducers."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


class RecursionLimitExceeded(RuntimeError):
    """Raised when graph execution exceeds the maximum allowed supersteps."""


@dataclass
class Checkpoint:
    step_id: int
    node_executed: str
    state: Dict[str, Any]


class PregelGraphEngine:
    """Production Pregel State Machine Graph Engine."""

    def __init__(self, reducers: Optional[Dict[str, Callable[[Any, Any], Any]]] = None) -> None:
        self.nodes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Callable[[Dict[str, Any]], str]] = {}
        self.reducers = reducers or {}
        self.checkpoints: List[Checkpoint] = []

    def add_node(self, name: str, fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already registered.")
        self.nodes[name] = fn

    def add_edge(self, from_node: str, to_node: str) -> None:
        self.edges[from_node] = to_node

    def add_conditional_edge(
        self, from_node: str, router_fn: Callable[[Dict[str, Any]], str]
    ) -> None:
        self.conditional_edges[from_node] = router_fn

    def _apply_reducers(self, current_state: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        new_state = copy.deepcopy(current_state)
        for key, val in updates.items():
            if key in self.reducers and key in new_state:
                new_state[key] = self.reducers[key](new_state[key], val)
            else:
                new_state[key] = val
        return new_state

    def run(
        self,
        initial_state: Dict[str, Any],
        start_node: str,
        max_supersteps: int = 25,
    ) -> Dict[str, Any]:
        """Executes graph state machine until END is reached or max_supersteps exceeded."""
        state = copy.deepcopy(initial_state)
        curr_node = start_node
        self.checkpoints.clear()

        # Save initial checkpoint
        self.checkpoints.append(Checkpoint(step_id=0, node_executed="__START__", state=copy.deepcopy(state)))

        for step in range(1, max_supersteps + 1):
            if curr_node == "END":
                return state

            if curr_node not in self.nodes:
                raise KeyError(f"Target node '{curr_node}' does not exist in graph.")

            # Compute step on immutable snapshot
            node_fn = self.nodes[curr_node]
            node_updates = node_fn(copy.deepcopy(state))

            # Channel reduction phase
            state = self._apply_reducers(state, node_updates)

            # Checkpoint recording
            self.checkpoints.append(Checkpoint(step_id=step, node_executed=curr_node, state=copy.deepcopy(state)))

            # Routing phase
            if curr_node in self.conditional_edges:
                next_node = self.conditional_edges[curr_node](state)
            elif curr_node in self.edges:
                next_node = self.edges[curr_node]
            else:
                next_node = "END"

            curr_node = next_node

        raise RecursionLimitExceeded(
            f"Graph exceeded max_supersteps ({max_supersteps}) without reaching 'END'."
        )

    def rewind_to_step(self, step_id: int) -> Dict[str, Any]:
        """Time travel: returns state at a historical step_id."""
        for cp in self.checkpoints:
            if cp.step_id == step_id:
                return copy.deepcopy(cp.state)
        raise IndexError(f"Checkpoint step {step_id} not found.")
