"""Unit tests for Agent Memory Manager."""

from __future__ import annotations

import pytest
from agent_memory_manager import AgentMemoryManager, MemoryRecord


@pytest.fixture
def memory_manager() -> AgentMemoryManager:
    return AgentMemoryManager(
        working_memory_capacity=3,
        recency_decay_rate=0.9,
        weight_recency=0.3,
        weight_importance=0.3,
        weight_relevance=0.4,
    )


def test_working_memory_sliding_window(memory_manager: AgentMemoryManager):
    memory_manager.add_working_interaction("user", "msg1")
    memory_manager.add_working_interaction("assistant", "msg2")
    memory_manager.add_working_interaction("user", "msg3")
    memory_manager.add_working_interaction("assistant", "msg4")

    assert len(memory_manager.working_memory) == 3
    assert memory_manager.working_memory[0]["content"] == "msg2"
    assert memory_manager.working_memory[-1]["content"] == "msg4"


def test_episodic_multi_factor_retrieval(memory_manager: AgentMemoryManager):
    now = 100000.0
    # Mem 1: Recent, high relevance, low importance
    memory_manager.add_episodic_memory(
        memory_id="m1",
        content="I like green apples",
        importance=2.0,
        embedding=[1.0, 0.0],
        timestamp=now - 3600.0,  # 1 hour ago
    )
    # Mem 2: Old, high importance, high relevance
    memory_manager.add_episodic_memory(
        memory_id="m2",
        content="I am severely allergic to peanuts",
        importance=10.0,
        embedding=[1.0, 0.0],
        timestamp=now - (3600.0 * 24.0),  # 24 hours ago
    )
    # Mem 3: Irrelevant
    memory_manager.add_episodic_memory(
        memory_id="m3",
        content="The moon orbits earth",
        importance=5.0,
        embedding=[0.0, 1.0],
        timestamp=now,
    )

    # Query matching [1.0, 0.0]
    results = memory_manager.retrieve_episodic(query_embedding=[1.0, 0.0], top_k=2, current_time=now)
    assert len(results) == 2
    # Memory 2 should be in top results due to importance rating
    ids = [r.memory_id for r in results]
    assert "m1" in ids
    assert "m2" in ids
    assert "m3" not in ids


def test_memory_reflection_consolidation(memory_manager: AgentMemoryManager):
    memory_manager.add_episodic_memory("e1", "User asked about PyTorch", 5.0, [1.0, 0.0])
    memory_manager.add_episodic_memory("e2", "User asked about CUDA kernels", 8.0, [1.0, 0.0])

    def mock_summarizer(memories: list[MemoryRecord]) -> dict[str, str]:
        return {"user_domain": "GPU and Deep Learning Engineer"}

    memory_manager.consolidate_reflection(mock_summarizer)
    assert memory_manager.semantic_store["user_domain"] == "GPU and Deep Learning Engineer"
