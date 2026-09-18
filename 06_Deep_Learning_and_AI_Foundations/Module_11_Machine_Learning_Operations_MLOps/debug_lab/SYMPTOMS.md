# Debug Lab Incident Report: Same Feature Value Produces Different Predictions in Training vs Serving

- **Severity:** P1 Train/Serve Skew
- **Affected Subsystem:** Module_11_Machine_Learning_Operations_MLOps
- **Reported Impact:** A model's single numeric feature is standardized before being fed to a linear predictor. Feeding the exact same raw feature value into the exact same trained weights produces a very different prediction at serving time than it did at training/validation time.

---

## 🚨 Observable Symptoms & Logs
```text
Training-time normalization stats: mean=11.500, std=1.500
Prediction using training-time normalization: 0.9333
Prediction using serving-time normalization:  0.1000
Same raw feature value (12.0) fed to the same trained weights in both cases.
```
The raw input (`12.0`) and the model weights are identical in both calls -- only the normalization step differs -- yet the two predictions do not match.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_11_Machine_Learning_Operations_MLOps/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_train_serve_skew.py
   ```
3. Compare the training-time and serving-time predictions for the same input.

---

## 🎯 Your Objective
1. Inspect `broken_train_serve_skew.py`'s `serve_request()` function.
2. Compare where its normalization statistics (`mean`, `std`) come from versus where the training-time statistics come from.
3. Formulate a hypothesis for the mismatched predictions, then check `ANSWERS.md`.
