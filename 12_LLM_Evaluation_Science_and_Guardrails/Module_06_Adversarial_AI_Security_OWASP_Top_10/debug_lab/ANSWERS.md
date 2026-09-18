# Debug Lab Solution & Forensic Post-Mortem

## Incident: Prompt-Injection Scanner Blocks the Textbook Attack Phrase but Waves Through Case-Swapped and Base64-Smuggled Variants

---

### 🔍 Forensic Root Cause Analysis
`scan()` performs a single, case-sensitive, exact-substring check for one literal phrase:

```python
def scan(self, text):
    if "ignore all previous instructions" in text:
        return False
    return True
```

Any transformation of the attack that doesn't produce that exact lowercase substring evades detection entirely. Changing the capitalization (`"IGNORE ALL PREVIOUS INSTRUCTIONS"`) no longer matches a case-sensitive `in` check. Encoding the phrase as Base64 and asking the model to decode it means the literal attack text never appears in `text` at all, since the scanner only ever inspects the raw string it was handed, not any decoded form of substrings within it. There is no normalization step -- case-folding, decoding common encodings, or fuzzy/semantic matching -- before the comparison, so the scanner only ever catches the one exact phrasing it was written against.

---

### 🛠️ Production Corrective Action & Code Fix

```python
import re, base64

INJECTION_PATTERNS = [re.compile(r"ignore\s+all\s+previous\s+instructions", re.IGNORECASE)]

class FixedScanner:
    def scan(self, text):
        candidates = [text]
        for token in re.findall(r"[A-Za-z0-9+/=]{16,}", text):
            try:
                candidates.append(base64.b64decode(token).decode("utf-8", "ignore"))
            except Exception:
                pass
        return not any(p.search(c) for c in candidates for p in INJECTION_PATTERNS)
```

Matching case-insensitively against a flexible whitespace pattern catches the case-swapped variant, and decoding Base64-looking tokens found inside the text before scanning them too catches the smuggled variant -- both without requiring the exact original phrasing.

---

### 🛡️ Production Prevention Invariants
1. **Normalize Case and Common Encodings Before Matching:** Injection scanners must case-fold and decode likely encodings (Base64, URL-encoding, unicode homoglyphs) before comparing against known attack patterns, never compare raw bytes.
2. **Maintain a Growing Regression Corpus of Obfuscation Techniques:** Every new bypass caught in red-teaming should become a permanent test case so it can never silently regress.
3. **Treat Exact-String Matching as a Floor, Not a Ceiling:** Pair it with a semantic or classifier-based second layer to catch variants no regex will anticipate.
