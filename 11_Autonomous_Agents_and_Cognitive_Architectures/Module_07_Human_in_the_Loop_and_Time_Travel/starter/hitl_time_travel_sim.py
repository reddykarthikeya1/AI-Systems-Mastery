"""Starter stub for HITL Engine."""

from __future__ import annotations
from typing import Any, Callable, Dict, Optional, Set


class HITLEngine:
    def __init__(self, nodes: Dict[str, Callable], edges: Dict[str, str], interrupt_before: Optional[Set[str]] = None) -> None:
        raise NotImplementedError("HITLEngine is not implemented yet.")

    def run_until_interrupt(self, initial_state: Dict[str, Any], start_node: str) -> Dict[str, Any]:
        raise NotImplementedError

    def resume(self, approved: bool, state_overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError
