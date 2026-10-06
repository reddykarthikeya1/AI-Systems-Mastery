"""Example 1: a ReAct-style tool-calling loop with budgets, error handling and loop detection.

Run: python ex01_tool_loop.py   (offline, uses the scripted FakeLLM)
"""
from llm import FakeLLM

TOOLS = [
    {"name": "get_price", "description": "Return the latest price for a ticker symbol.",
     "parameters": {"type": "object", "properties": {"ticker": {"type": "string"}}, "required": ["ticker"]}},
    {"name": "get_history", "description": "Return closing prices for the last N days.",
     "parameters": {"type": "object", "properties": {"ticker": {"type": "string"}, "days": {"type": "integer"}}, "required": ["ticker", "days"]}},
]

PRICES = {"ACME": [100.0, 101.0, 99.5, 102.0, 103.1, 104.0, 106.2]}


def get_price(ticker: str) -> float:
    return PRICES[ticker][-1]


def get_history(ticker: str, days: int) -> list:
    if days < 1 or days > len(PRICES[ticker]):
        raise ValueError(f"days must be between 1 and {len(PRICES[ticker])}")  # helpful error
    return PRICES[ticker][-days:]


REGISTRY = {"get_price": get_price, "get_history": get_history}


def run_agent(goal: str, llm, max_steps: int = 6) -> dict:
    messages = [{"role": "system", "content": "You are a careful analyst. Use tools; do not guess."},
                {"role": "user", "content": goal}]
    seen_calls = set()
    for step in range(max_steps):                            # hard step budget
        reply = llm(messages, TOOLS)
        messages.append({"role": "assistant", "content": reply["content"], "tool_calls": reply["tool_calls"]})
        if not reply["tool_calls"]:                          # stop condition: model answered
            return {"answer": reply["content"], "steps": step + 1, "messages": messages}
        for call in reply["tool_calls"]:
            key = (call["name"], tuple(sorted(call["args"].items())))
            if key in seen_calls:                            # loop detection
                result = "ERROR: identical call repeated; try a different approach or answer."
            else:
                seen_calls.add(key)
                try:
                    result = str(REGISTRY[call["name"]](**call["args"]))
                except Exception as e:  # errors are observations, not crashes
                    result = f"ERROR: {e}"
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
    return {"answer": None, "steps": max_steps, "messages": messages, "stopped": "step budget exhausted"}


if __name__ == "__main__":
    script = [
        {"tool_calls": [{"id": "1", "name": "get_history", "args": {"ticker": "ACME", "days": 30}}]},   # model over-asks
        {"tool_calls": [{"id": "2", "name": "get_history", "args": {"ticker": "ACME", "days": 7}}]},    # recovers from the error
        {"content": "ACME rose from 100.0 to 106.2 over 7 days (+6.2%)."},
    ]
    out = run_agent("How did ACME move over the last week?", FakeLLM(script))
    tool_msgs = [m["content"] for m in out["messages"] if m["role"] == "tool"]
    assert tool_msgs[0].startswith("ERROR: days must be between")  # first call failed, was fed back
    assert out["steps"] == 3 and "106.2" in out["answer"]
    print("OK:", out["answer"])
