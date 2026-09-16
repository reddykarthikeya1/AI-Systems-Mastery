# Project Guide: Building an Enterprise Agent Benchmark Harness

In this capstone lab, you will build an automated evaluation harness for AI agent trajectories, scoring task resolution, step efficiency, tool accuracy, and execution cost.

---

## Three-Tier Implementation Path

### Tier 1: Benchmark Dataset & Task Runner
- Define `BenchmarkTask` dataclass with prompt, gold criteria, and optimal step count.
- Implement `AgentBenchmarkHarness.evaluate_task()`.

### Tier 2: Multi-Dimensional Trajectory Scoring
- Compute `pass_rate`, `step_efficiency`, and `tool_accuracy`.
- Calculate total token consumption and compute cost per resolved task.

### Tier 3: Summary Analytics & Regression Reporting
- Aggregate results across the benchmark suite.
- Emit markdown regression reports highlighting wandering steps and tool failure points.
