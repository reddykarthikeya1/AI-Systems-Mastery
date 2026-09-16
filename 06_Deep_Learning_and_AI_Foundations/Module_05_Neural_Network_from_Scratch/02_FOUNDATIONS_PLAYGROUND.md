# 🐣 Interactive Foundations Playground: Autograd from Scratch (Micrograd)

> *"Underneath billion-parameter transformers and trillion-FLOP supercomputers lies a tiny 50-line recursive function: topological sorting and the chain rule."*

---

## 1. The Value Object: Wrapping Numbers with History

In regular Python, `a = 2.0; b = -3.0; c = a * b` gives `-6.0`, but forgets that `c` came from `a` and `b`.
In our custom Autograd engine:
- Every number is wrapped in a `Value` class.
- When you do `c = a * b`, `c` stores its numerical `.data = -6.0` **AND** a pointer to its parents `._prev = {a, b}` and operation `._op = '*'`.
- It also registers a local gradient lambda `_backward()`:
  $$\frac{\partial L}{\partial a} += b \cdot \frac{\partial L}{\partial c}, \quad \frac{\partial L}{\partial b} += a \cdot \frac{\partial L}{\partial c}$$

---

## 2. Topological Sort: The Unwinding Order

To backpropagate correctly without corrupting gradients:
1. You must process nodes in **reverse topological order** (from Loss back to inputs).
2. A node can only calculate its total gradient after **all downstream nodes that depend on it have finished**!
3. We build this topological order using a recursive depth-first search (DFS).
