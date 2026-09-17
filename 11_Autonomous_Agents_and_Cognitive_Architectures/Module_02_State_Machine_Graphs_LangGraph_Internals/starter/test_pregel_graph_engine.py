"""Unit tests for Pregel Graph Engine."""

from __future__ import annotations

import operator
import pytest
from pregel_graph_engine import PregelGraphEngine, RecursionLimitExceeded


def test_linear_graph_execution():
    reducers = {"messages": operator.add}
    engine = PregelGraphEngine(reducers=reducers)

    def step_a(state):
        return {"messages": ["Step A completed"]}

    def step_b(state):
        return {"messages": ["Step B completed"], "status": "DONE"}

    engine.add_node("node_a", step_a)
    engine.add_node("node_b", step_b)
    engine.add_edge("node_a", "node_b")
    engine.add_edge("node_b", "END")

    final = engine.run({"messages": ["Initial"]}, start_node="node_a")
    assert final["status"] == "DONE"
    assert final["messages"] == ["Initial", "Step A completed", "Step B completed"]
    assert len(engine.checkpoints) == 3


def test_cyclic_conditional_loop():
    engine = PregelGraphEngine()

    def worker(state):
        return {"count": state.get("count", 0) + 1}

    def should_continue(state):
        if state["count"] >= 3:
            return "END"
        return "worker"

    engine.add_node("worker", worker)
    engine.add_conditional_edge("worker", should_continue)

    final = engine.run({"count": 0}, start_node="worker", max_supersteps=10)
    assert final["count"] == 3


def test_recursion_limit_enforced():
    engine = PregelGraphEngine()

    def infinite_node(state):
        return {"ping": True}

    engine.add_node("infinite", infinite_node)
    engine.add_edge("infinite", "infinite")

    with pytest.raises(RecursionLimitExceeded):
        engine.run({}, start_node="infinite", max_supersteps=5)


def test_time_travel_rewind():
    reducers = {"history": operator.add}
    engine = PregelGraphEngine(reducers=reducers)

    def step_1(state):
        return {"history": ["v1"]}

    def step_2(state):
        return {"history": ["v2"]}

    engine.add_node("step_1", step_1)
    engine.add_node("step_2", step_2)
    engine.add_edge("step_1", "step_2")
    engine.add_edge("step_2", "END")

    engine.run({"history": []}, start_node="step_1")
    rewound = engine.rewind_to_step(1)
    assert rewound["history"] == ["v1"]
