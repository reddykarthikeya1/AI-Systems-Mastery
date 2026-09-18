# Debug Lab Incident Report: "Frozen" Pretrained Layer Keeps Changing

- **Severity:** P1 Model Integrity
- **Affected Subsystem:** Module_04_TensorFlow_Fundamentals
- **Reported Impact:** A transfer-learning setup marks the pretrained encoder as
  `trainable=False` so only the new classifier head should adapt during fine-tuning.
  After a short fine-tuning run, the "frozen" encoder's weight has moved anyway.

---

## Observable Symptoms & Logs
```text
Weights before fine-tuning:
  pretrained_encoder: 1.0000 (trainable=False)
  classifier_head: 0.5000 (trainable=True)
Weights after 3 fine-tuning steps:
  pretrained_encoder: 0.9700 (trainable=False)
  classifier_head: 0.4700 (trainable=True)
```
`pretrained_encoder` is printed with `trainable=False` both before and after, yet its
weight value visibly changed from `1.0000` to `0.9700`.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_04_TensorFlow_Fundamentals/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_frozen_layer.py
   ```
3. Compare the encoder's weight before and after fine-tuning.

---

## Your Objective
1. Inspect `broken_frozen_layer.py`'s `apply_gradients()` function.
2. Check whether it consults each layer's `trainable` flag at all.
3. Formulate a hypothesis for why a frozen layer still moves, then check `ANSWERS.md`.
