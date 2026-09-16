"""Production Agent Evaluation and Benchmark Harness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List


@dataclass
class BenchmarkTask:
    task_id: str
    goal: str
    optimal_steps: int
    evaluator_fn: Callable[[Dict[str, Any]], bool]


@dataclass
class TrajectoryRecord:
    task_id: str
    success: bool
    total_steps: int
    optimal_steps: int
    tool_calls_total: int
    tool_calls_failed: int
    step_efficiency: float
    tool_accuracy: float


class AgentBenchmarkHarness:
    """Production Evaluation Harness for Agent Trajectories."""

    def __init__(self, tasks: List[BenchmarkTask]) -> None:
        self.tasks = {t.task_id: t for t in tasks}

    def evaluate_trajectory(
        self,
        task_id: str,
        agent_output: Dict[str, Any],
        actual_steps: int,
        tool_calls_total: int,
        tool_calls_failed: int,
    ) -> TrajectoryRecord:
        """Evaluates a single task trajectory against gold criteria."""
        if task_id not in self.tasks:
            raise KeyError(f"Task '{task_id}' not found in benchmark suite.")

        task = self.tasks[task_id]
        success = task.evaluator_fn(agent_output)

        # Efficiency is only credited if the task succeeded
        if success and actual_steps > 0:
            step_efficiency = min(1.0, task.optimal_steps / actual_steps)
        else:
            step_efficiency = 0.0

        if tool_calls_total > 0:
            tool_accuracy = max(0.0, (tool_calls_total - tool_calls_failed) / tool_calls_total)
        else:
            tool_accuracy = 1.0

        return TrajectoryRecord(
            task_id=task_id,
            success=success,
            total_steps=actual_steps,
            optimal_steps=task.optimal_steps,
            tool_calls_total=tool_calls_total,
            tool_calls_failed=tool_calls_failed,
            step_efficiency=step_efficiency,
            tool_accuracy=tool_accuracy,
        )

    def run_suite(
        self,
        agent_runner_fn: Callable[[BenchmarkTask], Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Executes full benchmark suite and computes aggregate scores."""
        records: List[TrajectoryRecord] = []

        for task in self.tasks.values():
            result = agent_runner_fn(task)
            rec = self.evaluate_trajectory(
                task_id=task.task_id,
                agent_output=result["output"],
                actual_steps=result["actual_steps"],
                tool_calls_total=result["tool_calls_total"],
                tool_calls_failed=result["tool_calls_failed"],
            )
            records.append(rec)

        total_tasks = len(records)
        solved_tasks = sum(1 for r in records if r.success)
        pass_rate = (solved_tasks / total_tasks) if total_tasks > 0 else 0.0

        avg_efficiency = (
            sum(r.step_efficiency for r in records if r.success) / solved_tasks
            if solved_tasks > 0
            else 0.0
        )
        avg_tool_accuracy = sum(r.tool_accuracy for r in records) / total_tasks if total_tasks > 0 else 0.0

        return {
            "total_tasks": total_tasks,
            "solved_tasks": solved_tasks,
            "pass_rate": pass_rate,
            "avg_step_efficiency": avg_efficiency,
            "avg_tool_accuracy": avg_tool_accuracy,
            "records": records,
        }
