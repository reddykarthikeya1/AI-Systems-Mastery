# Debug Lab Incident Report: Fine-Tuning Learning Rate Spikes to Maximum on the First Step

- **Severity:** P1 Training Stability
- **Affected Subsystem:** Module_10_How_to_FineTune_Models
- **Reported Impact:** A LoRA fine-tuning run uses a linear warmup schedule so the learning rate ramps gradually from near zero up to `base_lr` over the first 10 steps, protecting the pretrained weights from a destructive first update. Instead the very first optimizer step fires at full `base_lr`, then the rate drops back down before ramping up a second time.

---

## 🚨 Observable Symptoms & Logs
```text
Learning rate warmup schedule (should ramp smoothly from ~0 up to base_lr):
  step  0: lr = 0.001000
  step  1: lr = 0.000100
  step  2: lr = 0.000200
  step  3: lr = 0.000300
  step  4: lr = 0.000400
  step  5: lr = 0.000500
  step  6: lr = 0.000600
  step  7: lr = 0.000700
  step  8: lr = 0.000800
  step  9: lr = 0.000900
  step 10: lr = 0.001000
  step 11: lr = 0.001000
  step 12: lr = 0.001000
  step 13: lr = 0.001000
  step 14: lr = 0.001000
```
A correct warmup schedule should be non-decreasing: `lr` at step 0 should be the smallest value in the table, climbing steadily to `base_lr` by step 10. Instead step 0 is already at `0.001000` (the maximum), then step 1 drops to `0.000100` before climbing again.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_10_How_to_FineTune_Models/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_warmup_schedule.py
   ```
3. Compare the lr value at step 0 against the values at steps 1 through 9.

---

## 🎯 Your Objective
1. Inspect `broken_warmup_schedule.py`'s `warmup_lr()` function.
2. Work out what `fraction` and `scale` evaluate to when `step` is `0`, and trace the `try`/`except` path that gets taken.
3. Formulate a hypothesis for the step-0 spike and the step-1 dip, then check `ANSWERS.md`.
