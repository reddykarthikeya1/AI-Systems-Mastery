"""Starter stub for Pregel Graph Engine."""

from __future__ import annotations
from typing import Any, Callable, Dict, Optional


class PregelGraphEngine:
    def __init__(self, reducers: Optional[Dict[str, Callable[[Any, Any], Any]]] = None) -> None:
        raise NotImplementedError("PregelGraphEngine is not implemented yet.")

    def add_node(self, name: str, fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        raise NotImplementedError

    def run(self, initial_state: Dict[str, Any], start_node: str, max_supersteps: int = 25) -> Dict[str, Any]:
        raise NotImplementedError
