# Project Guide: Building an Enterprise Guardrail Pipeline

In this project, you will build an end-to-end multi-layer guardrail pipeline with PII pseudonymization, toxic keyword blocking, and response fallback handlers.

---

## Three-Tier Implementation Path

### Tier 1: Regex PII Scrubber & Entity Masker (Required)
- Detect SSN, Credit Cards, Emails, and Phone Numbers.
- Replace detected PII with canonical tokens (`[REDACTED_SSN]`).

### Tier 2: Pre-Flight Adversarial & Topic Filter
- Block forbidden conversational domains (e.g. medical diagnosis, legal advice).
- Block known prompt injection trigger words.

### Tier 3: Reversible Anonymization Pipeline (Staff-Level)
- Maintain an encrypted session mapping table: `{"<PERSON_1>": "Alice Smith"}`.
- Re-hydrate tokens back into the final response before returning to user.
