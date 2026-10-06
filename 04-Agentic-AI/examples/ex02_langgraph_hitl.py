"""Example 2: a real LangGraph agent: typed state + reducers, a tool loop, a checkpointer,
and a human approval interrupt (human-in-the-loop) that resumes where it paused.

Verified against langgraph==1.2.13 (see requirements.txt). Run: python ex02_langgraph_hitl.py
"""
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from llm import FakeLLM


class State(TypedDict):
    request: str
    plan: str
    log: Annotated[list, operator.add]   # reducer: appends, safe for parallel branches
    approved: bool
    result: str


def build_graph(llm):
    def plan_node(state: State):
        reply = llm([{"role": "user", "content": state["request"]}])
        return {"plan": reply["content"], "log": ["planned"]}

    def approval_node(state: State):
        decision = interrupt({"question": "Run this plan?", "plan": state["plan"]})  # pauses, state is checkpointed
        return {"approved": bool(decision), "log": [f"approval={bool(decision)}"]}

    def act_node(state: State):
        return {"result": f"EXECUTED: {state['plan']}", "log": ["executed"]}    # side effect only AFTER approval

    def reject_node(state: State):
        return {"result": "CANCELLED by reviewer", "log": ["cancelled"]}

    def route(state: State) -> str:
        return "act" if state["approved"] else "reject"

    g = StateGraph(State)
    g.add_node("plan", plan_node)
    g.add_node("approval", approval_node)
    g.add_node("act", act_node)
    g.add_node("reject", reject_node)
    g.add_edge(START, "plan")
    g.add_edge("plan", "approval")
    g.add_conditional_edges("approval", route, {"act": "act", "reject": "reject"})
    g.add_edge("act", END)
    g.add_edge("reject", END)
    return g.compile(checkpointer=InMemorySaver())


def run(approve: bool):
    app = build_graph(FakeLLM([{"content": "archive 40 old tickets"}]))
    cfg = {"configurable": {"thread_id": f"case-{approve}"}}
    first = app.invoke({"request": "clean up the queue", "log": []}, cfg)
    assert "__interrupt__" in first, "graph should have paused for approval"
    paused = first["__interrupt__"][0].value
    assert paused["plan"] == "archive 40 old tickets"
    final = app.invoke(Command(resume=approve), cfg)          # resume the same thread
    return final


if __name__ == "__main__":
    ok = run(True)
    assert ok["result"].startswith("EXECUTED") and ok["log"] == ["planned", "approval=True", "executed"]
    no = run(False)
    assert no["result"] == "CANCELLED by reviewer" and "executed" not in no["log"]
    print("OK:", ok["result"], "|", no["result"])
