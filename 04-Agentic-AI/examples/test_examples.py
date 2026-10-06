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
