"""Starter stub for ReAct Loop Engine."""

from __future__ import annotations
from typing import Any, Callable, Dict, List


class ReActLoopEngine:
    def __init__(self, tools: Dict[str, Callable[..., str]], max_steps: int = 10) -> None:
        raise NotImplementedError("ReActLoopEngine is not implemented yet.")

    def run(self, goal: str, llm_generate_fn: Callable[[str, List[str]], str]) -> Any:
        raise NotImplementedError("ReActLoopEngine.run is not implemented yet.")
