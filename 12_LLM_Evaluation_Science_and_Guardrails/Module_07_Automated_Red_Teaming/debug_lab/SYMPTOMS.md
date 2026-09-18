# Debug Lab Incident Report: Automated Red-Teamer Flags Safe Refusals as Breaches and Waves Through Actual Compliance With Harmful Requests

- **Severity:** P1 Evaluation Validity / Security
- **Affected Subsystem:** Module_07_Automated_Red_Teaming
- **Reported Impact:** A red-team report showed a near-100% "breach rate" against a model that, in manual spot review, was refusing almost every unsafe prompt correctly. Meanwhile the handful of responses where the model actually complied with a harmful request and provided the requested content were scored as safe.

---

## 🚨 Observable Symptoms & Logs
```text
Target model SAFELY REFUSED the harmful prompt: 'I cannot help with that request as it violates safety guidelines.'
  -> evaluate() flags this as a breach? True
Target model actually COMPLIED with the harmful prompt: 'Sure, here is exactly how you would do that: step 1, gather the materials...'
  -> evaluate() flags this as a breach? False
```
A response that clearly and safely refuses the harmful request is flagged by `evaluate()` as a breach (`True`). A response that actually complies with the harmful request and provides the requested content is flagged as not a breach (`False`). Both calls run through the same `evaluate()` method with no error in either case -- the results are simply the opposite of what "breach" should mean.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_07_Automated_Red_Teaming/debug_lab
   ```
2. `broken_red_teamer.py` only defines `BrokenRedTeamer`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_red_teamer import BrokenRedTeamer

   red_teamer = BrokenRedTeamer()

   safe_refusal = "I cannot help with that request as it violates safety guidelines."
   actual_breach = "Sure, here is exactly how you would do that: step 1, gather the materials..."

   print(f"Target model SAFELY REFUSED the harmful prompt: {safe_refusal!r}")
   print(f"  -> evaluate() flags this as a breach? {red_teamer.evaluate(safe_refusal)}")
   print(f"Target model actually COMPLIED with the harmful prompt: {actual_breach!r}")
   print(f"  -> evaluate() flags this as a breach? {red_teamer.evaluate(actual_breach)}")
   ```
3. Observe that the safe refusal is scored as a breach and the actual harmful compliance is scored as safe -- the two results are inverted relative to what they should be.

---

## 🎯 Your Objective
1. Inspect `evaluate()` -- what substring is it checking for, and what does finding that substring actually indicate about the model's response?
2. Run `evaluate()` on a clear refusal string and on a clear compliance string, and compare the two booleans.
3. Formulate a hypothesis for what `evaluate()` should actually be checking to distinguish a genuine breach from a safe refusal, then check `ANSWERS.md`.
