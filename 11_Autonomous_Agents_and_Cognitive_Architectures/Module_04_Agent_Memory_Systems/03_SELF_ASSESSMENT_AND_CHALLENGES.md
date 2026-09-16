# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is naive vector retrieval (pure cosine similarity) insufficient for agent memory?
   - *Answer*: Pure cosine similarity ignores time recency and intrinsic importance, often returning stale or irrelevant historical trivia.
2. What is the difference between episodic memory and semantic memory?
   - *Answer*: Episodic memory records specific past events with timestamps (e.g., "User asked for Python code on Tuesday"), while semantic memory stores generalized facts (e.g., "User is a Python developer").
3. How does memory reflection prevent catastrophic forgetting in long-running agents?
   - *Answer*: It condenses thousands of granular conversational turns into compact, high-level behavioral rules that fit permanently within the prompt.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Personal Assistant Agent with Privacy and Retention Controls
**Context**: A healthcare assistant agent stores personal patient history across years of interactions. It must support HIPAA compliance, forget requests (GDPR Right to Be Forgotten), and accurate symptom progression recall.
**Question**: Architect the episodic memory retention and deletion pipeline.
**Solution**:
1. Tag every episodic memory with patient ID, cryptographic signature, and category (e.g. `medical_symptom`, `casual_chatter`).
2. Enforce TTL: casual chatter expires in 30 days; medical facts are consolidated into encrypted semantic graphs.
3. Provide an atomic hard-delete endpoint that purges vector embeddings and graph nodes for a specific patient ID across all tiers.
