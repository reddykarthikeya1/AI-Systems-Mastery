"""Unit tests for Multi-Agent Swarm and Consensus Engine."""

from __future__ import annotations

import pytest
from multi_agent_swarm import AgentHandoff, SwarmAgent, SwarmEngine, SwarmMessage


@pytest.fixture
def swarm_setup() -> SwarmEngine:
    triage = SwarmAgent(name="Triage", system_prompt="Route requests.")
    billing = SwarmAgent(name="Billing", system_prompt="Handle refunds.")
    tech = SwarmAgent(name="TechSupport", system_prompt="Handle technical bugs.")
    agents = {"Triage": triage, "Billing": billing, "TechSupport": tech}
    return SwarmEngine(agents=agents, max_handoffs=3)


def test_swarm_handoff_success(swarm_setup: SwarmEngine):
    def mock_decision(agent: SwarmAgent, msgs: list[SwarmMessage]):
        if agent.name == "Triage":
            return AgentHandoff(target_agent_name="Billing", reason="User wants refund")
        return "Refund of $50 processed."

    res = swarm_setup.run_swarm("Triage", "Please refund my subscription", mock_decision)
    assert res["final_agent"] == "Billing"
    assert res["response"] == "Refund of $50 processed."
    assert res["handoff_history"] == ["Triage", "Billing"]


def test_swarm_max_handoffs_exceeded(swarm_setup: SwarmEngine):
    # Oscillating decision function
    def ping_pong(agent: SwarmAgent, msgs: list[SwarmMessage]):
        if agent.name == "Triage":
            return AgentHandoff(target_agent_name="Billing", reason="Looping")
        return AgentHandoff(target_agent_name="Triage", reason="Looping back")

    res = swarm_setup.run_swarm("Triage", "Hello", ping_pong)
    assert "Maximum agent handoffs exceeded" in res["response"]
    assert len(res["handoff_history"]) == 4


def test_consensus_debate():
    agents = {
        "Conservative": SwarmAgent(name="Conservative", system_prompt="Be risk averse"),
        "Aggressive": SwarmAgent(name="Aggressive", system_prompt="Take calculated risks"),
        "Neutral": SwarmAgent(name="Neutral", system_prompt="Balanced"),
    }
    engine = SwarmEngine(agents=agents)

    def mock_debate_fn(agent: SwarmAgent, query: str, peer_opinions: dict[str, str]) -> str:
        if not peer_opinions:
            if agent.name == "Aggressive":
                return "APPROVE"
            return "REJECT"
        # Round 2: Aggressive gives in to majority
        return "REJECT"

    res = engine.run_consensus_debate(["Conservative", "Aggressive", "Neutral"], "Approve $1M loan?", mock_debate_fn)
    assert res["consensus_response"] == "REJECT"
    assert res["vote_distribution"]["REJECT"] == 3
