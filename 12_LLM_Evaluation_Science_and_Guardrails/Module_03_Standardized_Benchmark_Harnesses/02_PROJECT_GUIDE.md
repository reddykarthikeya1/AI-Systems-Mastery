# Project Guide: Building an Enterprise Benchmark Evaluation Harness

In this lab, you implement an automated benchmark test harness executing standardized math reasoning (GSM8K style) and Python code execution (HumanEval style) with Pass@k estimation.

---

## Three-Tier Implementation Path

### Tier 1: Math Reasoning Evaluation (Required)
- Extract numeric answers from Chain-of-Thought solutions (`r"####\s*(-?[0-9]+(?:\.[0-9]+)?)"`).
- Evaluate exact numeric equivalence.

### Tier 2: Code Execution & Pass@k Computation
- Execute generated python code against test assertions.
- Implement `compute_pass_at_k(n, c, k)`.

### Tier 3: Benchmark Contamination Detector
- Implement $n$-gram decontamination scanner: check whether a test question matches any training sample.
