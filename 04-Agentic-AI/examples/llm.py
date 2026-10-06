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


def get_llm(script: list | None = None):
    """Return a callable llm(messages, tools) -> response dict."""
    provider = os.environ.get("LLM_PROVIDER", "fake").lower()
    if provider == "fake":
        return FakeLLM(script or [])
    if provider == "anthropic":  # pragma: no cover - needs network and a key
        import anthropic

        client = anthropic.Anthropic()
        model = os.environ.get("LLM_MODEL", "claude-sonnet-5-5")

        def call(messages, tools=None):
            system = next((m["content"] for m in messages if m["role"] == "system"), None)
            msgs = [m for m in messages if m["role"] != "system"]
            kw = {"model": model, "max_tokens": 1024, "messages": msgs}
            if system:
                kw["system"] = system
            if tools:
                kw["tools"] = [{"name": t["name"], "description": t["description"], "input_schema": t["parameters"]} for t in tools]
            r = client.messages.create(**kw)
            text = "".join(b.text for b in r.content if b.type == "text")
            calls = [{"id": b.id, "name": b.name, "args": b.input} for b in r.content if b.type == "tool_use"]
            return {"content": text, "tool_calls": calls}

        return call
    raise ValueError(f"Unknown LLM_PROVIDER={provider!r}; use fake or anthropic")
