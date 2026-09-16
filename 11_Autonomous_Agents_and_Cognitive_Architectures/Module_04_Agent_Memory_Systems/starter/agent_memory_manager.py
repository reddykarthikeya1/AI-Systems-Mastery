"""Starter stub for Agent Memory Manager."""

from __future__ import annotations
from typing import Any, List


class AgentMemoryManager:
    def __init__(self, working_memory_capacity: int = 5) -> None:
        raise NotImplementedError("AgentMemoryManager is not implemented yet.")

    def add_working_interaction(self, role: str, message: str) -> None:
        raise NotImplementedError

    def add_episodic_memory(self, memory_id: str, content: str, importance: float, embedding: List[float]) -> None:
        raise NotImplementedError

    def retrieve_episodic(self, query_embedding: List[float], top_k: int = 3) -> List[Any]:
        raise NotImplementedError
