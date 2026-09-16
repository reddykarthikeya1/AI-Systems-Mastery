# Project Guide: Building an Adversarial Security Scanner

In this lab, you build an enterprise adversarial security scanner that detects prompt injection, Base64/Hex obfuscation, roleplay hijacking, and system prompt leakage attempts.

---

## Three-Tier Implementation Path

### Tier 1: Pattern-Based Injection Detection (Required)
- Detect classic jailbreak strings (`"DAN"`, `"developer mode"`, `"ignore previous instructions"`).
- Detect system prompt extraction attempts (`"print your initial instructions"`, `"repeat prompt"`).

### Tier 2: Multi-Layer Obfuscation Decoding
- Detect and decode Base64 and Hexadecimal encoded tokens.
- Recursively scan decoded content against injection patterns.

### Tier 3: OWASP Classification & Risk Scoring
- Map detected violations to OWASP LLM01, LLM02, or LLM06 codes.
- Emit structured security alert payloads.
