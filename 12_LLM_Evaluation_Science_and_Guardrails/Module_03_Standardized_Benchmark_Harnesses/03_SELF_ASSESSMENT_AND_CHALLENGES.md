# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why does 5-shot CoT prompting improve GSM8K accuracy over zero-shot direct generation?
   - *Answer*: It forces the transformer to allocate computation steps (intermediate tokens) to work through reasoning before committing to the final numeric token.
2. What is the hazard of using Regex parsing for GSM8K answers?
   - *Answer*: Model might output currency symbols (`$150`), commas (`1,000`), or words (`fifteen`), causing false negatives without normalization.
3. How do you detect if an open-source model was fine-tuned on the HumanEval test set?
   - *Answer*: Test it on HumanEval-Plus (mutated assert variants) or evaluate code generation on problems written after the model's training cutoff.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Continuous Benchmark Gating in Model CI/CD
**Context**: An AI laboratory trains a new 70B parameter model checkpoint every 24 hours. Training runs cost $40,000/day. The team needs an automated early-stopping trigger if reasoning capability degenerates.
**Question**: Design the lightweight evaluation harness that runs every 500 gradient steps without slowing training.
**Solution**:
1. Curate a compressed validation subset (e.g. 100 stratified problems across MMLU, GSM8K, and HumanEval).
2. Run inference asynchronously on 4 dedicated evaluation GPUs while main cluster continues training.
3. If Pass@1 drops $> 2.5\sigma$ below moving average, send a hard interrupt signal to pause training and trigger checkpoint rollback.
