"""Run every example offline: pytest -q   (uses the scripted FakeLLM, no API keys, no network)."""
import asyncio

import ex01_tool_loop
import ex03_hybrid_rag
import ex05_eval_harness


def test_tool_loop_recovers_from_tool_error():
    from llm import FakeLLM
    out = ex01_tool_loop.run_agent("q", FakeLLM([
        {"tool_calls": [{"id": "1", "name": "get_history", "args": {"ticker": "ACME", "days": 99}}]},
        {"tool_calls": [{"id": "2", "name": "get_history", "args": {"ticker": "ACME", "days": 7}}]},
        {"content": "done 106.2"}]))
    assert out["answer"] == "done 106.2" and out["steps"] == 3


def test_tool_loop_step_budget_stops_runaway_agent():
    from llm import FakeLLM
    looping = FakeLLM([{"tool_calls": [{"id": str(i), "name": "get_price", "args": {"ticker": "ACME"}}]} for i in range(10)])
    out = ex01_tool_loop.run_agent("q", looping, max_steps=4)
    assert out["answer"] is None and out["stopped"] == "step budget exhausted"


def test_langgraph_human_in_the_loop():
    import ex02_langgraph_hitl as ex
    assert ex.run(True)["result"].startswith("EXECUTED")
    assert ex.run(False)["result"] == "CANCELLED by reviewer"


def test_hybrid_beats_each_single_retriever():
    r = ex03_hybrid_rag.evaluate(k=1)
    assert r["hybrid"] >= max(r["bm25"], r["dense"]) and r["hybrid"] > min(r["bm25"], r["dense"])


def test_mcp_server_tools():
    import ex04_mcp_server as ex
    asyncio.run(ex.self_test())


def test_pass_hat_k_is_much_lower_than_single_trial():
    r = ex05_eval_harness.evaluate(0.9, trials=8)
    assert r["pass^k"] < r["single"] - 0.3 and r["pass@k"] > 0.99


def test_wilson_interval_known_value():
    lo, hi = ex05_eval_harness.wilson(80, 100)
    assert (round(lo, 2), round(hi, 2)) == (0.71, 0.87)


# --- provider adapters, tested with stub clients (no network, no keys) ---------------------------------

from types import SimpleNamespace as NS

NEUTRAL = [
    {"role": "system", "content": "be careful"},
    {"role": "user", "content": "price of ACME?"},
    {"role": "assistant", "content": "", "tool_calls": [{"id": "c1", "name": "get_price", "args": {"ticker": "ACME"}},
                                                          {"id": "c2", "name": "get_price", "args": {"ticker": "BETA"}}]},
    {"role": "tool", "tool_call_id": "c1", "content": "106.2"},
    {"role": "tool", "tool_call_id": "c2", "content": "55.0"},
]
TOOLS = [{"name": "get_price", "description": "price", "parameters": {"type": "object", "properties": {}}}]


def test_anthropic_adapter_translates_tool_turns_and_parses_tool_use():
    import llm
    seen = {}

    def create(**kw):
        seen.update(kw)
        return NS(content=[NS(type="text", text="calling"), NS(type="tool_use", id="c3", name="get_price", input={"ticker": "GAMMA"})])

    call = llm.anthropic_llm(client=NS(messages=NS(create=create)), model="any-model")
    out = call(NEUTRAL, TOOLS)
    assert seen["system"] == "be careful" and seen["tools"][0]["input_schema"] == TOOLS[0]["parameters"]
    roles = [m["role"] for m in seen["messages"]]
    assert roles == ["user", "assistant", "user"]                       # both tool results share one user message
    assert [b["type"] for b in seen["messages"][1]["content"]] == ["tool_use", "tool_use"]
    assert [b["tool_use_id"] for b in seen["messages"][2]["content"]] == ["c1", "c2"]
    assert out == {"content": "calling", "tool_calls": [{"id": "c3", "name": "get_price", "args": {"ticker": "GAMMA"}}]}


def test_openai_adapter_translates_tool_turns_and_parses_tool_calls():
    import json
    import llm
    seen = {}

    def create(**kw):
        seen.update(kw)
        fn = NS(name="get_price", arguments=json.dumps({"ticker": "GAMMA"}))
        return NS(choices=[NS(message=NS(content=None, tool_calls=[NS(id="c3", function=fn)]))])

    call = llm.openai_llm(client=NS(chat=NS(completions=NS(create=create))), model="any-model")
    out = call(NEUTRAL, TOOLS)
    assistant = seen["messages"][2]
    assert assistant["content"] is None and assistant["tool_calls"][0]["function"]["arguments"] == json.dumps({"ticker": "ACME"})
    assert seen["messages"][3] == {"role": "tool", "tool_call_id": "c1", "content": "106.2"}
    assert seen["tools"][0]["type"] == "function" and seen["tools"][0]["function"]["name"] == "get_price"
    assert out == {"content": "", "tool_calls": [{"id": "c3", "name": "get_price", "args": {"ticker": "GAMMA"}}]}


def test_adapters_require_an_explicit_model_id():
    import os
    import pytest
    import llm
    os.environ.pop("LLM_MODEL", None)
    with pytest.raises(ValueError):
        llm.openai_llm(client=object())
    with pytest.raises(ValueError):
        llm.anthropic_llm(client=object())
