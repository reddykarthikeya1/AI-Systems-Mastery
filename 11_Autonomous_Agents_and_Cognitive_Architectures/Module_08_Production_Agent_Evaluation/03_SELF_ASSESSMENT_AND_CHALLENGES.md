# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is BLEU or ROUGE completely useless for evaluating an autonomous coding agent?
   - *Answer*: Coding agents must be evaluated on functional execution (e.g. passing unit tests), not textual similarity to a reference solution.
2. What is "Trajectory Wandering"?
   - *Answer*: When an agent takes superfluous exploration steps (e.g. reading unrelated files or repeating searches) before eventually finding the solution.
3. How does SWE-bench verify whether a generated patch is valid?
   - *Answer*: It checks out the exact GitHub commit prior to the fix, applies the agent's git diff, and executes `pytest` asserting that fail-to-pass tests now pass and pass-to-pass tests remain unbroken.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Offline Regression Testing for Agent Release Pipeline
**Context**: A team ships bi-weekly updates to their internal developer agent. An update improved Python debugging pass rate by 5%, but introduced subtle tool loops on SQL tasks.
**Question**: Design an automated CI/CD evaluation gate that catches trajectory regressions before deployment.
**Solution**:
1. Run a golden suite of 100 representative tasks in Dockerized containers on every PR.
2. Enforce hard gating thresholds: Overall `pass@1 >= 85%`, `Tool Accuracy >= 95%`, and maximum allowed step count per task $\le 1.5 \times \text{baseline}$.
3. Block merge if any individual domain experiences a $> 3\%$ regression.
