# Project Guide: Building a Colang State Machine and Llama Guard Classifier

In this project, you will build a dialog guardrail engine implementing Colang-style canonical intent routing, topical diversion flows, and Llama Guard hazard classification.

---

## Three-Tier Implementation Path

### Tier 1: Canonical Intent Classifier & Rule Dispatch (Required)
- Map user text to canonical intents via keyword and regex rules.
- Return deterministic bot responses when diversion rails trigger.

### Tier 2: Llama Guard Safety Classifier
- Implement `LlamaGuardClassifier.audit(prompt)`: checks for S1-S6 violations.
- Output binary classification `safe` / `unsafe` along with the violated category code.

### Tier 3: Integrated NeMo Guardrail Pipeline
- Combine pre-flight Llama Guard check with Colang state machine flow transitions.
