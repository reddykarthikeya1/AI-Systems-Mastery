# Module 08: Production Agent Evaluation

## 1. Theoretical Foundations: Benchmarking Autonomous Trajectories

Autonomous agents solve multi-hop, environment-interactive tasks. Evaluating them requires shifting from token-level perplexity to **Trajectory and Outcome Evaluation**.

### 1.1 Landmark Agent Benchmarks

| Benchmark | Domain | Primary Metrics | Environment Type |
| :--- | :--- | :--- | :--- |
| **SWE-bench** (Jimenez et al., 2024) | Real GitHub issues & PRs | % Resolved (Unit tests pass) | Full Git repo + Pytest |
| **WebArena** (Zhou et al., 2023) | Autonomous web browsing | Task success rate, Cost | Live mock websites |
| **GAIA** (Mialon et al., 2023) | General AI Assistant questions | Exact match answer, Step count | Multimodal web & file tools |
| **AgentBench** (Liu et al., 2023) | OS, DB, Web, Games | Turn completion rate | Multi-environment harness |

---

## 2. Mathematical Formulation of Trajectory Metrics

For an evaluation dataset $\mathcal{D} = \{(q_i, y_i, S_i^*)\}_{i=1}^N$ where $S_i^*$ is the oracle optimal step count:

### 2.1 Pass@k Metric
$$\text{Pass}@k = \mathbb{E}_{i} \left[ 1 - \frac{\binom{n - c_i}{k}}{\binom{n}{k}} \right]$$
where $n$ is sampled trajectories per task, and $c_i$ is number of correct solutions.

### 2.2 Step Efficiency Score (SES)
$$\text{SES}(i) = \frac{|S_i^*|}{\max(|S_i|, |S_i^*|)}$$
Measures how concisely the agent reached the goal without exploratory bloat.

### 2.3 Tool Call Precision (TCP)
$$\text{TCP} = \frac{\sum_{t=1}^{T} \mathbb{I}(\text{status}(a_t) = \text{SUCCESS})}{T}$$
