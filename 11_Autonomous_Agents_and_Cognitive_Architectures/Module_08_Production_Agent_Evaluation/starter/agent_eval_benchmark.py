"""Starter stub for Agent Benchmark Harness."""

from __future__ import annotations
from typing import Any, Callable, Dict, List


class AgentBenchmarkHarness:
    def __init__(self, tasks: List[Any]) -> None:
        raise NotImplementedError("AgentBenchmarkHarness is not implemented yet.")

    def run_suite(self, agent_runner_fn: Callable) -> Dict[str, Any]:
        raise NotImplementedError
