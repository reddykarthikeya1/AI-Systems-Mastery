# Self-Assessment & Staff Interview Challenges

## Part 1: Conceptual Knowledge Quiz
1. Why is post-generation output filtering alone insufficient for data security?
   - *Answer*: Post-generation filtering protects the user from seeing sensitive data, but the prompt containing user PII has already been transmitted to and logged by the upstream model provider. Pre-flight input filtering is required.
2. What is the difference between Redaction and Pseudonymization?
   - *Answer*: Redaction permanently deletes or obscures data (`[REDACTED]`); Pseudonymization replaces data with reversible pseudonyms (`<USER_1>`), allowing the LLM to understand entity relationships.
3. How do streaming guardrails reduce latency compared to buffering the whole response?
   - *Answer*: Streaming guardrails inspect sliding token windows (e.g. 20 tokens) concurrently with generation, terminating the stream immediately if a policy violation occurs.

---

## Part 2: Staff / Principal AI Engineer Scenarios

### Scenario: High-Throughput HIPAA Compliance Gateway
**Context**: A telemedicine platform routes doctor-patient transcripts to an LLM for clinical summarization. The pipeline must redact 18 HIPAA Safe Harbor identifiers at 10,000 requests/sec with $< 15$ ms p99 latency overhead.
**Question**: Architect the high-throughput filtering tier.
**Solution**:
1. Implement a compiled Rust/C++ regex engine (e.g. Hyperscan/Vectorscan) executing all structured PII regexes in a single SIMD pass.
2. Pair with a quantized ONNX distilled token-classification model for NER.
3. Run stateless worker nodes in autoscaling groups behind an internal Load Balancer.
