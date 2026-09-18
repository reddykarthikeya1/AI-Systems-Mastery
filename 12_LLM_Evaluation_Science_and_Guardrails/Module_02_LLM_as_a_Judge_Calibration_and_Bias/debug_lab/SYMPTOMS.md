# Debug Lab Incident Report: LLM-as-Judge Comparison Always Favors Whichever Response Is Placed First

- **Severity:** P1 Evaluation Validity
- **Affected Subsystem:** Module_02_LLM_as_a_Judge_Calibration_and_Bias
- **Reported Impact:** A/B model comparison results were found to correlate almost perfectly with which model's output happened to be placed in the prompt's first slot, not with actual response quality -- swapping the display order of the exact same two responses flipped which one "won."

---

## 🚨 Observable Symptoms & Logs
```text
Response X: 'Paris is the capital of France.'
Response Y: 'The capital of France is Paris.'
evaluate(X, Y, judge_fn) -> winner slot: 'A'
evaluate(Y, X, judge_fn) -> winner slot: 'A'
Slot 'A' wins both times regardless of which response sits there: True
```
Two near-identical, equally correct responses were compared through `BrokenJudge.evaluate()`. When `X` was placed first, slot `A` (`X`) won. When the exact same two responses were compared again with `Y` placed first, slot `A` (now `Y`) won too. The verdict is identical both times -- `A` -- even though the response actually occupying slot `A` changed between the two calls. `evaluate()` itself raises no error and returns a normal-looking result in both cases.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_02_LLM_as_a_Judge_Calibration_and_Bias/debug_lab
   ```
2. `broken_judge.py` only defines `BrokenJudge`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_judge import BrokenJudge

   def position_biased_judge_fn(candidate_a, candidate_b):
       # Simulates a real LLM judge's documented tendency to prefer whichever
       # response occupies the first slot of the prompt, regardless of content.
       return "A"

   judge = BrokenJudge()
   response_x = "Paris is the capital of France."
   response_y = "The capital of France is Paris."

   verdict_xy = judge.evaluate(response_x, response_y, position_biased_judge_fn)
   verdict_yx = judge.evaluate(response_y, response_x, position_biased_judge_fn)

   print(f"Response X: {response_x!r}")
   print(f"Response Y: {response_y!r}")
   print(f"evaluate(X, Y, judge_fn) -> winner slot: {verdict_xy!r}")
   print(f"evaluate(Y, X, judge_fn) -> winner slot: {verdict_yx!r}")
   print(f"Slot 'A' wins both times regardless of which response sits there: {verdict_xy == verdict_yx == 'A'}")
   ```
3. Observe that the reported winner tracks the seat position ("A"), not which actual response text was passed into that seat.

---

## 🎯 Your Objective
1. Inspect `evaluate()` -- how many times does it call `judge_fn`, and with what argument order?
2. Run the same two candidate responses through `evaluate()` twice, swapping their argument order the second time, and compare the verdicts.
3. Formulate a hypothesis for what a bias-resistant comparison should do with the two orderings, then check `ANSWERS.md`.
