# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is single-answer rating (e.g., score 1 to 5) less reliable than pairwise comparison?
   - *Answer*: LLMs suffer from severe score calibration drift: a "4" from GPT-4 on Tuesday may correspond to a "3" or "5" on Wednesday. Pairwise comparison converts evaluation into a relative ranking tournament (Elo).
2. What happens if an LLM judge always votes for Candidate B regardless of order?
   - *Answer*: In swap-pair evaluation, Candidate B wins Trial 1, and Candidate A wins Trial 2; the system detects the contradiction and correctly registers a TIE.
3. How does verbosity bias corrupt benchmark leaderboards?
   - *Answer*: Smaller models learn to generate rambling, repetitive markdown lists to trick LLM judges into awarding higher scores despite lower factual density.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: High-Throughput Chatbot Arena Architecture
**Context**: An organization maintains an internal model tournament evaluating 50 fine-tuned models on 10,000 prompts. Full $O(N^2)$ pairwise matches require 2.5 million LLM judge calls.
**Question**: Architect an active learning tournament that computes accurate Elo ratings with $<5\%$ of the compute budget.
**Solution**:
1. Implement Swiss-system or Bayesian Bradley-Terry active matchmaking (e.g. TrueSkill).
2. Instead of all pairs, only match models with overlapping posterior skill distributions (models of similar strength).
3. Use swap-pair verification only on closely contested matches where score difference is $<0.15$.
