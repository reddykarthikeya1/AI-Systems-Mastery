# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why does high ROUGE-L score not guarantee an accurate LLM answer?
   - *Answer*: ROUGE-L only measures longest common subsequence. An answer with identical phrasing but flipped negation ("is" vs "is NOT") achieves $>90\%$ ROUGE-L while being factually 100% incorrect.
2. How does the RAGAS framework avoid requiring human-annotated ground-truth labels?
   - *Answer*: By using reference-free metrics: comparing the generated answer against the retrieved context (Faithfulness) and generating reverse questions from the answer (Answer Relevance).
3. What is the difference between Context Recall and Context Precision?
   - *Answer*: Context Recall measures whether *all* necessary information was retrieved; Context Precision measures whether the relevant chunks were placed at the *top* ranks.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: High-Volume Production Hallucination Detector
**Context**: An enterprise financial advisory LLM generates 100,000 portfolio analysis answers per day. Legal compliance mandates zero ungrounded financial claims. Running GPT-4 as an LLM judge on all 100k queries would cost $15,000/day and add 2 seconds of latency.
**Question**: Architect a cost-effective, real-time groundedness verification pipeline.
**Solution**:
1. Implement a 2-tier cascaded evaluator.
2. Tier 1: Fast deterministic NLI cross-encoder model (e.g. DeBERTa-v3-small, ~20ms, running on local CPU/GPU) checks claim entailment. 90% of verified answers pass instantly.
3. Tier 2: Only ambiguous claims (NLI confidence between 0.4 and 0.8) are escalated to an asynchronous LLM-as-a-judge queue for verification.
