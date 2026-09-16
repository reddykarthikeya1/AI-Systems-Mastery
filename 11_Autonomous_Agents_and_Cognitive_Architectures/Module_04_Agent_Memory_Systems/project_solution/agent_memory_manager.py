"""Multi-Tiered Agent Memory Manager with Episodic Multi-Factor Retrieval and Reflection."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class MemoryRecord:
    memory_id: str
    content: str
    timestamp: float
    importance: float  # 1.0 to 10.0
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot / (norm1 * norm2)


class AgentMemoryManager:
    """Production Agent Memory Manager with Working, Episodic, and Reflection tiers."""

    def __init__(
        self,
        working_memory_capacity: int = 5,
        recency_decay_rate: float = 0.995,
        weight_recency: float = 0.3,
        weight_importance: float = 0.3,
        weight_relevance: float = 0.4,
    ) -> None:
        self.working_memory_capacity = working_memory_capacity
        self.recency_decay_rate = recency_decay_rate
        self.weight_recency = weight_recency
        self.weight_importance = weight_importance
        self.weight_relevance = weight_relevance

        self.working_memory: List[Dict[str, str]] = []
        self.episodic_store: List[MemoryRecord] = []
        self.semantic_store: Dict[str, str] = {}

    def add_working_interaction(self, role: str, message: str) -> None:
        """Adds a turn to working memory buffer, maintaining sliding window."""
        self.working_memory.append({"role": role, "content": message})
        if len(self.working_memory) > self.working_memory_capacity:
            self.working_memory.pop(0)

    def add_episodic_memory(
        self,
        memory_id: str,
        content: str,
        importance: float,
        embedding: List[float],
        timestamp: Optional[float] = None,
    ) -> None:
        """Stores a new episodic memory record."""
        t = timestamp if timestamp is not None else time.time()
        record = MemoryRecord(
            memory_id=memory_id,
            content=content,
            timestamp=t,
            importance=min(max(importance, 1.0), 10.0),
            embedding=embedding,
        )
        self.episodic_store.append(record)

    def retrieve_episodic(
        self,
        query_embedding: List[float],
        top_k: int = 3,
        current_time: Optional[float] = None,
    ) -> List[MemoryRecord]:
        """Scores and retrieves top_k episodic memories via multi-factor evaluation."""
        now = current_time if current_time is not None else time.time()
        scored_records = []

        for record in self.episodic_store:
            # Hours elapsed
            hours_elapsed = max(0.0, (now - record.timestamp) / 3600.0)
            recency_score = math.pow(self.recency_decay_rate, hours_elapsed)
            importance_score = record.importance / 10.0
            relevance_score = max(0.0, cosine_similarity(record.embedding, query_embedding))

            total_score = (
                self.weight_recency * recency_score
                + self.weight_importance * importance_score
                + self.weight_relevance * relevance_score
            )
            scored_records.append((total_score, record))

        scored_records.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scored_records[:top_k]]

    def consolidate_reflection(
        self,
        summarizer_fn: Callable[[List[MemoryRecord]], Dict[str, str]],
    ) -> None:
        """Consolidates episodic memories into semantic knowledge facts."""
        if not self.episodic_store:
            return
        extracted_facts = summarizer_fn(self.episodic_store)
        self.semantic_store.update(extracted_facts)
