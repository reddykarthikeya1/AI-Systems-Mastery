"""A tiny LLM abstraction so every example runs offline in CI.

`FakeLLM` replays a scripted list of responses (deterministic). To use a real
model, set LLM_PROVIDER=anthropic or openai and the matching API key; the
examples call `get_llm()` and never import a provider SDK directly.

A response is a dict: {"content": str, "tool_calls": [{"id", "name", "args"}]}.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class FakeLLM:
    script: list = field(default_factory=list)
    calls: int = 0

    def __call__(self, messages: list, tools: list | None = None) -> dict:
        if self.calls >= len(self.script):
            raise RuntimeError("FakeLLM script exhausted (the agent looped more than the test expected)")
        out = self.script[self.calls]
        self.calls += 1
        return {"content": out.get("content", ""), "tool_calls": out.get("tool_calls", [])}


def anthropic_llm(client=None, model: str | None = None, max_tokens: int = 1024):
    """Adapter for the Anthropic Messages API. `client` is injectable so the translation can be tested offline.

    The agent's neutral format uses role="tool" messages and an assistant `tool_calls` list. Anthropic wants
    tool results as `tool_result` blocks inside a *user* message, and tool calls as `tool_use` blocks inside the
    assistant message, so both directions are translated here.
    """
    if client is None:  # pragma: no cover - needs a key
        import anthropic

        client = anthropic.Anthropic()
    model = model or os.environ.get("LLM_MODEL")
    if not model:
        raise ValueError("set LLM_MODEL to a model id from your provider's current model list")

    def call(messages, tools=None):
        system = next((m["content"] for m in messages if m["role"] == "system"), None)
        out: list = []
        for m in messages:
            if m["role"] == "system":
                continue
            if m["role"] == "tool":
                block = {"type": "tool_result", "tool_use_id": m["tool_call_id"], "content": m["content"]}
                if out and out[-1]["role"] == "user" and isinstance(out[-1]["content"], list) and out[-1]["content"][0]["type"] == "tool_result":
                    out[-1]["content"].append(block)       # several results to one assistant turn share one user message
                else:
                    out.append({"role": "user", "content": [block]})
            elif m["role"] == "assistant":
                blocks = ([{"type": "text", "text": m["content"]}] if m.get("content") else [])
                blocks += [{"type": "tool_use", "id": c["id"], "name": c["name"], "input": c["args"]} for c in m.get("tool_calls", [])]
                out.append({"role": "assistant", "content": blocks or [{"type": "text", "text": ""}]})
            else:
                out.append({"role": "user", "content": m["content"]})
        kw = {"model": model, "max_tokens": max_tokens, "messages": out}
        if system:
            kw["system"] = system
        if tools:
            kw["tools"] = [{"name": t["name"], "description": t["description"], "input_schema": t["parameters"]} for t in tools]
        r = client.messages.create(**kw)
        text = "".join(b.text for b in r.content if b.type == "text")
        calls = [{"id": b.id, "name": b.name, "args": b.input} for b in r.content if b.type == "tool_use"]
        return {"content": text, "tool_calls": calls}

    return call


def openai_llm(client=None, model: str | None = None):
    """Adapter for the OpenAI Chat Completions API (tools/function calling), with an injectable client."""
    import json

    if client is None:  # pragma: no cover - needs a key
        from openai import OpenAI

        client = OpenAI()
    model = model or os.environ.get("LLM_MODEL")
    if not model:
        raise ValueError("set LLM_MODEL to a model id from your provider's current model list")

    def call(messages, tools=None):
        out = []
        for m in messages:
            if m["role"] == "assistant":
                msg = {"role": "assistant", "content": m.get("content") or None}
                if m.get("tool_calls"):
                    msg["tool_calls"] = [{"id": c["id"], "type": "function",
                                          "function": {"name": c["name"], "arguments": json.dumps(c["args"])}} for c in m["tool_calls"]]
                out.append(msg)
            else:
                out.append({k: v for k, v in m.items() if k in ("role", "content", "tool_call_id")})
        kw = {"model": model, "messages": out}
        if tools:
            kw["tools"] = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                             "parameters": t["parameters"]}} for t in tools]
        msg = client.chat.completions.create(**kw).choices[0].message
        calls = [{"id": c.id, "name": c.function.name, "args": json.loads(c.function.arguments or "{}")}
                 for c in (msg.tool_calls or [])]
        return {"content": msg.content or "", "tool_calls": calls}

    return call


def get_llm(script: list | None = None):
    """Return a callable llm(messages, tools) -> response dict. LLM_PROVIDER is fake (default), anthropic or openai."""
    provider = os.environ.get("LLM_PROVIDER", "fake").lower()
    if provider == "fake":
        return FakeLLM(script or [])
    if provider == "anthropic":
        return anthropic_llm()
    if provider == "openai":
        return openai_llm()
    raise ValueError(f"Unknown LLM_PROVIDER={provider!r}; use fake, anthropic or openai")
