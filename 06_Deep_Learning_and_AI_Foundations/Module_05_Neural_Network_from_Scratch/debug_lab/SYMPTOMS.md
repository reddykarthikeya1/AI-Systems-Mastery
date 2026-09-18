# Debug Lab Incident Report: Hand-Rolled Network Cannot Learn XOR

- **Severity:** P2 Training Failure
- **Affected Subsystem:** Module_05_Neural_Network_from_Scratch
- **Reported Impact:** A from-scratch 2-input, 1-hidden-unit network trained with
  manual backpropagation is supposed to learn the classic non-linear XOR function.
  After 400 epochs, loss has barely moved and every prediction has collapsed toward
  the same uninformative value.

---

## Observable Symptoms & Logs
```text
XOR training loss every 100 epochs:
  epoch 0: loss = 0.2542
  epoch 100: loss = 0.2185
  epoch 200: loss = 0.2027
  epoch 300: loss = 0.1973
Final loss: 0.1948

Predictions after training:
  input=[0, 0] target=0 predicted=0.141
  input=[0, 1] target=1 predicted=0.495
  input=[1, 0] target=1 predicted=0.496
  input=[1, 1] target=0 predicted=0.500
```
Loss plateaus well above zero, and three of the four predictions converge to roughly
the same ~0.5 value regardless of the target -- the network is not separating the
XOR cases at all.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_05_Neural_Network_from_Scratch/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_xor_backprop.py
   ```
3. Observe the flat loss curve and near-identical predictions.

---

## Your Objective
1. Inspect `broken_xor_backprop.py`'s training loop, specifically how `d_hidden` is
   computed and used to update `w1`.
2. Write out the chain rule for `d(loss)/d(w1)` by hand and compare it to what the
   code actually computes.
3. Formulate a hypothesis for why the hidden layer never learns useful features, then
   check `ANSWERS.md`.
