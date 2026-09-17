"""Unit tests for Agent Benchmark Harness."""

from __future__ import annotations

import pytest
from agent_eval_benchmark import AgentBenchmarkHarness, BenchmarkTask


@pytest.fixture
def benchmark_harness() -> AgentBenchmarkHarness:
    tasks = [
        BenchmarkTask(
            task_id="t1",
            goal="Calculate H100 power",
            optimal_steps=2,
            evaluator_fn=lambda out: "16800" in str(out.get("answer", "")),
        ),
        BenchmarkTask(
            task_id="t2",
            goal="Fix syntax error",
            optimal_steps=3,
            evaluator_fn=lambda out: out.get("test_passed", False) is True,
        ),
    ]
    return AgentBenchmarkHarness(tasks=tasks)


def test_trajectory_scoring_success(benchmark_harness: AgentBenchmarkHarness):
    rec = benchmark_harness.evaluate_trajectory(
        task_id="t1",
        agent_output={"answer": "16800 Wh"},
        actual_steps=2,
        tool_calls_total=2,
        tool_calls_failed=0,
    )
    assert rec.success is True
    assert rec.step_efficiency == 1.0
    assert rec.tool_accuracy == 1.0


def test_trajectory_scoring_wandering(benchmark_harness: AgentBenchmarkHarness):
    # Task succeeded but took 4 steps instead of optimal 2
    rec = benchmark_harness.evaluate_trajectory(
        task_id="t1",
        agent_output={"answer": "16800 Wh"},
        actual_steps=4,
        tool_calls_total=4,
        tool_calls_failed=1,
    )
    assert rec.success is True
    assert rec.step_efficiency == 0.5
    assert rec.tool_accuracy == 0.75


def test_run_suite(benchmark_harness: AgentBenchmarkHarness):
    def mock_agent_runner(task: BenchmarkTask):
        if task.task_id == "t1":
            return {
                "output": {"answer": "16800 Wh"},
                "actual_steps": 2,
                "tool_calls_total": 2,
                "tool_calls_failed": 0,
            }
        return {
            "output": {"test_passed": False},
            "actual_steps": 5,
            "tool_calls_total": 3,
            "tool_calls_failed": 2,
        }

    summary = benchmark_harness.run_suite(mock_agent_runner)
    assert summary["total_tasks"] == 2
    assert summary["solved_tasks"] == 1
    assert summary["pass_rate"] == 0.5
    assert summary["avg_step_efficiency"] == 1.0
