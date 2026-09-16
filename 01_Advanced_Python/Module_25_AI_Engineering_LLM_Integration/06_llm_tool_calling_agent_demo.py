#!/usr/bin/env python3
"""Module 23: Autonomous LLM Tool-Calling Agent Demonstration.

This script demonstrates executing autonomous tool calls and returning structured answers.
"""

from __future__ import annotations


def tool_check_server_load(datacenter: str) -> dict:
    """Tool: Returns live CPU load for a specified datacenter."""
    loads = {"us-east": "42%", "eu-west": "78%", "ap-south": "21%"}
    return {"datacenter": datacenter, "cpu_load": loads.get(datacenter, "UNKNOWN")}


def simulate_agent_loop(user_intent: str) -> str:
    print(f"User Request: '{user_intent}'")
    # Step 1: LLM decides to call a tool
    tool_call = {
        "function": "tool_check_server_load",
        "arguments": {"datacenter": "eu-west"},
    }
    print(f"Agent Action: Calling tool '{tool_call['function']}' with args: {tool_call['arguments']}")

    # Step 2: System executes tool
    tool_result = tool_check_server_load(**tool_call["arguments"])
    print(f"Tool Observation: {tool_result}")

    # Step 3: LLM generates final response based on observation
    final_answer = f"The live CPU load in datacenter '{tool_result['datacenter']}' is currently {tool_result['cpu_load']}."
    return final_answer


def main() -> None:
    print("=" * 60)
    print("  Autonomous Agent ReAct Tool Execution Loop Demo")
    print("=" * 60)

    res = simulate_agent_loop("Check health of EU cluster")
    print(f"\nFinal Agent Response:\n  {res}")


if __name__ == "__main__":
    main()
