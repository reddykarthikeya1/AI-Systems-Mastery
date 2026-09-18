# Debug Lab Solution & Forensic Post-Mortem

## Incident: Colang Safety Router Sends Every Message Straight to the LLM Regardless of Content

---

### 🔍 Forensic Root Cause Analysis
`process()` ignores its `text` argument entirely:

```python
def process(self, text):
    return "DELEGATE_LLM"
```

It returns the literal constant `"DELEGATE_LLM"` on every call, with no intent classification, canonical-form matching, or safety-flow lookup performed on the input at all. Because the routing decision does not depend on the content of the message in any way, there is no code path by which an unsafe, jailbreak, or disallowed request could ever be intercepted, refused, or routed to a stricter flow -- every message, benign or malicious, receives the exact same "hand this straight to the LLM" verdict, since `text` is accepted as a parameter but never actually inspected.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class FixedColang:
    UNSAFE_INTENTS = {"jailbreak", "prompt_extraction", "disallowed_content"}

    def process(self, text):
        intent = classify_intent(text)   # canonical-form / embedding match against defined flows
        if intent in self.UNSAFE_INTENTS:
            return "BLOCKED"
        return "DELEGATE_LLM"
```

Classifying the message's intent before deciding how to route it means the routing decision is now actually a function of what was said, and messages matching a known-unsafe intent are blocked before ever reaching the underlying LLM.

---

### 🛡️ Production Prevention Invariants
1. **A Safety Router's Output Must Be a Function of the Input:** A constant return value defeats every downstream policy that assumes routing reflects the message's content.
2. **Maintain a Red-Team Regression Suite:** Keep a growing set of known jailbreak/unsafe prompts and assert none of them route to `DELEGATE_LLM`.
3. **Log the Classified Intent Alongside Every Routing Decision:** This makes unsafe-but-misrouted traffic visible in monitoring immediately, rather than discoverable only through manual red-teaming.
