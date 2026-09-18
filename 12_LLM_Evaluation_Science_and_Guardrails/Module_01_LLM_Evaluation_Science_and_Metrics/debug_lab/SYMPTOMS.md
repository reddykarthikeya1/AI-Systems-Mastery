# Debug Lab Incident Report: Faithfulness Evaluator Scores a Hallucinated Answer as Fully Grounded and a Correct Paraphrase as Ungrounded

- **Severity:** P1 Evaluation Validity
- **Affected Subsystem:** Module_01_LLM_Evaluation_Science_and_Metrics
- **Reported Impact:** A RAG faithfulness dashboard built on this evaluator reported near-perfect groundedness scores for a batch of answers that manual review later found to contain fabricated facts, while flagging several genuinely accurate, well-paraphrased answers as hallucinations.

---

## 🚨 Observable Symptoms & Logs
```text
Context: 'The Eiffel Tower was completed in 1889 and stands 330 meters tall.'
Hallucinated answer (wrong architect, wrong century): 'The Eiffel Tower was designed by Michelangelo and completed in 1750.'
  -> groundedness score: 1.0
Accurate, paraphrased answer: 'Standing 330 meters tall, the tower was finished in 1889.'
  -> groundedness score: 0.0
```
The answer that gets a perfect `1.0` groundedness score contains two claims the context directly contradicts (a wrong designer, a wrong completion year), yet it is scored as fully grounded. Meanwhile an answer that restates the context's real facts accurately, just in different words, scores `0.0` -- as if it were entirely unsupported. Both results run through the exact same `evaluate(answer, context)` call with no error raised in either case.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_01_LLM_Evaluation_Science_and_Metrics/debug_lab
   ```
2. `broken_evaluator.py` only defines `BrokenEvaluator`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_evaluator import BrokenEvaluator

   evaluator = BrokenEvaluator()
   context = "The Eiffel Tower was completed in 1889 and stands 330 meters tall."

   hallucinated_answer = "The Eiffel Tower was designed by Michelangelo and completed in 1750."
   paraphrased_answer = "Standing 330 meters tall, the tower was finished in 1889."

   score_hallucinated = evaluator.evaluate(hallucinated_answer, context)
   score_paraphrase = evaluator.evaluate(paraphrased_answer, context)

   print(f"Context: {context!r}")
   print(f"Hallucinated answer (wrong architect, wrong century): {hallucinated_answer!r}")
   print(f"  -> groundedness score: {score_hallucinated}")
   print(f"Accurate, paraphrased answer: {paraphrased_answer!r}")
   print(f"  -> groundedness score: {score_paraphrase}")
   ```
3. Observe that the fabricated answer scores higher than the accurate one -- the two scores are exactly backwards from what a faithfulness check should report.

---

## 🎯 Your Objective
1. Inspect `evaluate()` -- what part of `answer` does it actually check against `context`, and how?
2. Compute `evaluate()` by hand for an answer whose first five characters happen to appear in `context` but whose remaining claims are fabricated.
3. Formulate a hypothesis for what a real groundedness check would need to examine instead, then check `ANSWERS.md`.
