# Debug Lab Solution & Forensic Post-Mortem

## Incident: "Frozen" Pretrained Layer Keeps Changing

---

### Forensic Root Cause Analysis
`apply_gradients()` iterates over every layer in `layers` and subtracts
`lr * grads[layer.name]` unconditionally. It never inspects `layer.trainable`, so a
layer marked `trainable=False` receives exactly the same update as a trainable one.
The `trainable` flag is stored on the object but never actually read by the update
step -- it is purely decorative, which is why the "frozen" pretrained encoder keeps
drifting during fine-tuning.

---

### Production Corrective Action & Code Fix

```python
def apply_gradients(layers, grads, lr=0.1):
    for layer in layers:
        if not layer.trainable:
            continue
        layer.weight -= lr * grads[layer.name]
```

With the guard in place, `pretrained_encoder` stays exactly at `1.0000` across all
fine-tuning steps while `classifier_head` continues to adapt normally.

---

### Production Prevention Invariants
1. **Trainable-Flag Tests:** Unit test that frozen parameters are bit-for-bit
   identical before and after a training step.
2. **Parameter Diffing:** Snapshot and diff parameter values across checkpoints in
   CI for any layer configured as frozen.
3. **Optimizer Param Groups:** Prefer building the optimizer's parameter list from
   only the trainable layers, rather than filtering inside the update loop, so a
   frozen layer is structurally impossible to update.
