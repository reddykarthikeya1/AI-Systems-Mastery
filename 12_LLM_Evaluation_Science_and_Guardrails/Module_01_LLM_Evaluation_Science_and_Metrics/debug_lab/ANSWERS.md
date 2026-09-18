# Debug Lab Solution & Forensic Post-Mortem

## Incident: Faithfulness Evaluator Scores a Hallucinated Answer as Fully Grounded and a Correct Paraphrase as Ungrounded

---

### 🔍 Forensic Root Cause Analysis
`evaluate()` reduces "is this answer grounded in the context" to a single, extremely narrow check:

```python
def evaluate(self, answer, context):
    return 1.0 if answer[:5] in context else 0.0
```

Only whether the first five characters of `answer` appear anywhere as a substring of `context` is checked. This has nothing to do with whether the answer's actual claims are supported: an answer can open with a common phrase that trivially matches the context (`"The E..."`) and still contain wholly fabricated facts in the rest of the sentence, so it scores a perfect `1.0`. Conversely, a fully accurate answer phrased differently from the context -- reordered, paraphrased, using synonyms -- fails the five-character prefix check entirely and scores `0.0`, even though every claim in it is true. The check never looks past the first five characters, and it never decomposes or verifies individual claims at all.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class FixedEvaluator:
    def evaluate(self, answer, context):
        claims = decompose_into_claims(answer)                       # NLI/claim extraction
        supported = [c for c in claims if is_entailed(c, context)]   # per-claim entailment check
        return len(supported) / len(claims) if claims else 0.0
```

Decomposing the answer into individual claims and checking each one's entailment against the context, rather than pattern-matching a fixed-length prefix, means the score actually tracks whether the answer's content is supported -- not whether its opening words happen to overlap with the source text.

---

### 🛡️ Production Prevention Invariants
1. **Groundedness Must Operate at the Claim Level:** Decompose the answer and check each claim's entailment against context; never substitute a raw substring match on a fixed prefix.
2. **Build a Labeled Test Set of Known Hallucinations and Paraphrases:** Assert the evaluator scores known-hallucinated and known-correct-but-reworded answers in the right direction before trusting it in production.
3. **Track Evaluator Agreement Against Human-Labeled Judgments:** Treat divergence from human groundedness labels as an ongoing calibration signal, not a one-time validation.
