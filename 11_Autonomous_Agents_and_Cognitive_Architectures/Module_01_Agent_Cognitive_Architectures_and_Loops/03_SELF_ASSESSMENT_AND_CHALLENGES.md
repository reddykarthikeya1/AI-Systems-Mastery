# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. What is the fundamental difference between ReAct and Plan-and-Solve?
   - *Answer*: ReAct dynamically decides the next step based on the immediately preceding observation (dynamic feedback), whereas Plan-and-Solve plans the entire sequence upfront and executes sequentially (static decomposition).
2. Why is pure ReAct vulnerable to high latency in multi-step workflows?
   - *Answer*: Every single action requires a full LLM prefill and generation pass, creating sequential dependency where latency scales as $\sum \text{LLM}_{latency} + \sum \text{Tool}_{latency}$.
3. How does the Reflexion architecture improve upon vanilla ReAct?
   - *Answer*: It introduces episodic memory across multiple trials, allowing an agent that failed a task to read its own past self-critiques and avoid previous dead ends.
4. Explain the "infinite tool oscillation" failure mode.
   - *Answer*: When two complementary tools provide contradictory or mutually dependent partial answers, the LLM alternates endlessly between them.
5. Why is JSON tool calling preferred over free-form regex parsing in production?
   - *Answer*: Free-form parsing breaks easily with formatting drift, while JSON tool calling is backed by constrained decoding at the logits level.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario 1: Preventing Runaway Loops in Autonomous Coding Agents
**Context**: An autonomous agent operating on a Git repository attempts to fix a unit test. It makes an edit, runs `pytest`, sees a failure, and attempts the same syntax fix again in an endless loop, burning $150 of API credits in 10 minutes.
**Question**: Design an automated guardrail system that detects and breaks this loop within 3 iterations without human intervention.
**Solution**:
1. Implement canonicalized AST hashing of source code diffs.
2. If `Hash(Diff_{t}) == Hash(Diff_{t-1})` or test failure signature is identical across 2 attempts, trigger a hard break.
3. Switch the prompt to a Root Cause Analysis mode that forbids code edits until a verifiable explanation of the failure is produced.

### Scenario 2: Context Window Overflow in Long-Running Agents
**Context**: A customer support agent runs for 45 minutes across 30 tool calls. The context length reaches 64k tokens, increasing TTFT to 8 seconds and inflating costs.
**Question**: Propose an active context compaction strategy that preserves essential task state while reducing context length to under 8k tokens.
