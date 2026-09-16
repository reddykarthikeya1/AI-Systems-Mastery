# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. What is the fundamental root cause of Prompt Injection in LLMs?
   - *Answer*: The conflation of control instructions and user data in a single textual input channel (von Neumann architecture analogy).
2. How does an Indirect Prompt Injection differ from a Direct Prompt Injection?
   - *Answer*: Direct injection comes from the active user chat; Indirect injection comes from external third-party data retrieved by the agent (e.g. search results, email body, PDF text).
3. Why is Base64 decoding mandatory in pre-flight guardrails?
   - *Answer*: LLMs have learned Base64 representations during pretraining; they can understand and follow encoded instructions directly while naive keyword filters are bypassed.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: Defense-in-Depth Against Agentic Excessive Agency (LLM06)
**Context**: An AI database assistant executes SQL commands on behalf of developers. A user uses a jailbreak to generate `DROP TABLE accounts;`.
**Question**: Design an architectural defense that prevents data loss even if the LLM is completely compromised by the jailbreak.
**Solution**:
1. Implement Principle of Least Privilege: bind the agent's database connection to a read-only user role.
2. For write/delete queries, enforce a Human-in-the-Loop breakpoint requiring cryptographic approval from a database administrator.
3. Disallow multi-statement queries (`allow_multi_queries=False`) to prevent stacked SQL injection.
