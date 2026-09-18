# Debug Lab Solution & Forensic Post-Mortem

## Incident: Hand-Rolled Network Cannot Learn XOR

---

### Forensic Root Cause Analysis
The chain rule for the hidden layer's gradient is
`d(loss)/d(w1) = d_out * w2 * sigmoid_derivative(h) * x`, i.e. the hidden unit's
local derivative must be multiplied by the *upstream* signal (`d_out * w2`) flowing
back from the output layer. The code instead sets
`d_hidden = sigmoid_derivative(h)` alone, dropping the `d_out * w2` term entirely.
The hidden weights are therefore updated using a "gradient" that carries no
information about the actual prediction error -- it only reflects the hidden unit's
own local slope. Without that error signal reaching the hidden layer, the network
can't discover the non-linear combination of inputs XOR requires, so it collapses
toward predicting close to the same value for every input.

---

### Production Corrective Action & Code Fix

```python
for x, y in data:
    h, o = forward(x, w1, w2)
    error = o - y
    d_out = error * sigmoid_derivative(o)
    d_hidden = d_out * w2 * sigmoid_derivative(h)   # chain rule: include upstream signal
    w2 -= lr * d_out * h
    for i in range(len(w1)):
        w1[i] -= lr * d_hidden * x[i]
```

With the upstream term restored, loss drops toward zero and predictions correctly
separate into ~0 for matching inputs and ~1 for XOR-true inputs.

---

### Production Prevention Invariants
1. **Gradient Checking:** Compare analytic gradients against numerical
   (finite-difference) gradients on a small example before trusting a hand-written
   backprop implementation.
2. **Known-Problem Regression Test:** Keep XOR (or another minimal non-linearly
   separable dataset) as a standing regression test for any from-scratch network.
3. **Chain Rule Review:** Treat every backward-pass line as implementing one factor
   of an explicit chain-rule product; review each local gradient against the full
   expression it is supposed to be one term of.
