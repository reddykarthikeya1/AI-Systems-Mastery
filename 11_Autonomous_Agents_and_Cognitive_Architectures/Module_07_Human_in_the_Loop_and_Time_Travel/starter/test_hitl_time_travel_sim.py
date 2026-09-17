"""Unit tests for HITL State Machine and Time Travel."""

from __future__ import annotations

import pytest
from hitl_time_travel_sim import HITLEngine


@pytest.fixture
def hitl_engine() -> HITLEngine:
    def draft_payment(state):
        return {"amount": 5000, "drafted": True}

    def execute_payment(state):
        return {"paid": True, "final_amount": state["amount"]}

    nodes = {"draft": draft_payment, "pay": execute_payment}
    edges = {"draft": "pay", "pay": "END"}
    return HITLEngine(nodes=nodes, edges=edges, interrupt_before={"pay"})


def test_interrupt_before_breakpoint(hitl_engine: HITLEngine):
    res = hitl_engine.run_until_interrupt({}, start_node="draft")
    assert res["status"] == "SUSPENDED"
    assert res["paused_at"] == "pay"
    assert res["state"]["amount"] == 5000
    assert hitl_engine.suspended_execution is not None


def test_resume_with_human_payload_edit(hitl_engine: HITLEngine):
    hitl_engine.run_until_interrupt({}, start_node="draft")
    # Human intervenes: edits amount from 5000 to 1000
    res = hitl_engine.resume(approved=True, state_overrides={"amount": 1000})

    assert res["status"] == "COMPLETED"
    assert res["state"]["final_amount"] == 1000
    assert res["state"]["paid"] is True
    assert res["state"]["approval_status"] == "APPROVED"


def test_resume_rejection(hitl_engine: HITLEngine):
    hitl_engine.run_until_interrupt({}, start_node="draft")
    res = hitl_engine.resume(approved=False)

    assert res["status"] == "REJECTED"
    assert res["state"]["approval_status"] == "REJECTED"
    assert "paid" not in res["state"]


def test_time_travel_rewind(hitl_engine: HITLEngine):
    hitl_engine.run_until_interrupt({}, start_node="draft")
    hitl_engine.resume(approved=True)

    past_state = hitl_engine.time_travel_rewind(0)
    assert past_state["drafted"] is True
    assert "paid" not in past_state
