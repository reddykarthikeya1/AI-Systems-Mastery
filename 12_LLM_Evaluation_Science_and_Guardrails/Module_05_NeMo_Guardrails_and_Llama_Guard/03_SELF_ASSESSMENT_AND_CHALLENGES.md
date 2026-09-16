# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is a Colang state machine more reliable than prompting the LLM with system prompt rules?
   - *Answer*: System prompts can be bypassed or forgotten through prompt injection; Colang intercepts control at the software logic layer before the LLM is ever invoked.
2. What is the output format of Meta Llama Guard?
   - *Answer*: `safe` or `unsafe\nS{category_code}`.
3. How do NeMo Guardrails handle multi-turn conversational context?
   - *Answer*: By tracking dialogue state as an event sequence: user utterance $\rightarrow$ canonical intent $\rightarrow$ flow step $\rightarrow$ bot action.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Low-Latency Safety Gateway for Banking Voice Bot
**Context**: A retail bank deploys an LLM voice agent with a 300ms total budget for Audio $\rightarrow$ LLM $\rightarrow$ TTS. Running Llama Guard adds 250ms of latency, violating the budget.
**Question**: Architect an ultra-low-latency guardrail pipeline that stays within a 30ms guardrail budget.
**Solution**:
1. Implement Colang intent matching via a compiled Trie / finite state automaton running in $< 2$ ms.
2. Run Llama Guard asynchronously in parallel with audio streaming; if Llama Guard flags a violation mid-sentence, send a cancel packet to the audio stream and play a canned refusal.
