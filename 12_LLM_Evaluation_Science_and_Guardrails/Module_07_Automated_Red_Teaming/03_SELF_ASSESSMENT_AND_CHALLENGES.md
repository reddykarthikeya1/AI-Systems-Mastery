# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is white-box GCG (Greedy Coordinate Gradient) often ineffective against commercial API models?
   - *Answer*: GCG requires computing gradients with respect to input token embeddings, which are hidden behind black-box commercial APIs.
2. What is the PAIR (Prompt Automatic Iterative Refinement) loop?
   - *Answer*: An attacker LLM generates a candidate jailbreak, sends it to the target LLM, reads the refusal or response, and iteratively refines the prompt based on what triggered the refusal.
3. How do safety teams use red-teaming datasets to harden models?
   - *Answer*: Successful adversarial prompts and desired refusal responses are added to RLHF / DPO preference datasets for safety alignment retraining.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Continuous Automated Red Teaming in CI/CD
**Context**: An enterprise customer support bot releases prompt updates weekly. The security team needs a continuous red-teaming test suite running 5,000 automated jailbreaks per deployment.
**Question**: Design the testing pipeline and release gate criteria.
**Solution**:
1. Run automated red-teaming harness with 5,000 stratified attacks across S1-S6 categories.
2. Enforce zero tolerance: if any S1 (violence) or S4 (child safety) attack succeeds (ASR > 0%), immediately block release.
3. For low-severity categories, enforce $\text{ASR} \le 0.5\%$.
