"""Multi-Agent Swarm Collaboration and Consensus Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class AgentHandoff:
    target_agent_name: str
    reason: str


@dataclass
class SwarmMessage:
    sender: str
    content: str


@dataclass
class SwarmAgent:
    name: str
    system_prompt: str
    tools: Dict[str, Callable[..., Any]] = field(default_factory=dict)


class SwarmEngine:
    """Production Swarm Engine supporting dynamic handoffs and multi-agent debate."""

    def __init__(self, agents: Dict[str, SwarmAgent], max_handoffs: int = 5) -> None:
        self.agents = agents
        self.max_handoffs = max_handoffs

    def run_swarm(
        self,
        initial_agent_name: str,
        user_message: str,
        llm_decision_fn: Callable[[SwarmAgent, List[SwarmMessage]], Any],
    ) -> Dict[str, Any]:
        """Executes multi-agent swarm with dynamic handoffs."""
        if initial_agent_name not in self.agents:
            raise KeyError(f"Initial agent '{initial_agent_name}' not registered.")

        current_agent = self.agents[initial_agent_name]
        messages: List[SwarmMessage] = [SwarmMessage(sender="user", content=user_message)]
        handoff_history: List[str] = [current_agent.name]

        for _ in range(self.max_handoffs):
            decision = llm_decision_fn(current_agent, messages)

            # Check if decision is a handoff
            if isinstance(decision, AgentHandoff):
                target = decision.target_agent_name
                if target not in self.agents:
                    raise ValueError(f"Handoff target '{target}' does not exist.")
                handoff_history.append(target)
                current_agent = self.agents[target]
                messages.append(SwarmMessage(sender="system", content=f"Transferred to {target}: {decision.reason}"))
                continue

            # Otherwise, decision is final response
            messages.append(SwarmMessage(sender=current_agent.name, content=str(decision)))
            return {
                "final_agent": current_agent.name,
                "response": str(decision),
                "handoff_history": handoff_history,
                "messages": messages,
            }

        return {
            "final_agent": current_agent.name,
            "response": "Error: Maximum agent handoffs exceeded.",
            "handoff_history": handoff_history,
            "messages": messages,
        }

    def run_consensus_debate(
        self,
        agent_names: List[str],
        query: str,
        agent_eval_fn: Callable[[SwarmAgent, str, Dict[str, str]], str],
        rounds: int = 2,
    ) -> Dict[str, Any]:
        """Executes multi-agent consensus debate across personas."""
        active_agents = [self.agents[name] for name in agent_names if name in self.agents]
        if not active_agents:
            raise ValueError("No valid agents found for debate.")

        opinions: Dict[str, str] = {}

        # Round 1: Initial opinions
        for agent in active_agents:
            opinions[agent.name] = agent_eval_fn(agent, query, {})

        # Subsequent debate rounds: agents read peer opinions and critique
        for _ in range(1, rounds):
            new_opinions: Dict[str, str] = {}
            for agent in active_agents:
                new_opinions[agent.name] = agent_eval_fn(agent, query, opinions)
            opinions = new_opinions

        # Majority / Consensus check
        votes: Dict[str, int] = {}
        for op in opinions.values():
            votes[op] = votes.get(op, 0) + 1

        winner = max(votes.items(), key=lambda item: item[1])[0]

        return {
            "consensus_response": winner,
            "all_opinions": opinions,
            "vote_distribution": votes,
        }
