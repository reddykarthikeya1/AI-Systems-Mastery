# 🐣 Interactive Foundations Playground: TensorFlow & Graph Execution

> *"Eager execution is cooking a meal by hand, tasting as you go. Graph execution is programming an automated robotic assembly line to cook 100,000 meals an hour."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. Eager vs Graph Execution: The Mental Model

- **Eager Execution (PyTorch / TF Eager)**: Operations are evaluated immediately in Python.
  - *Advantage*: Trivial debugging, standard Python breakpoints (`pdb`), dynamic `for` loops.
  - *Disadvantage*: High Python interpreter overhead. Every matrix multiply round-trips through the Python C-API.
- **Graph Execution (`@tf.function` / TorchDynamo)**: Python code is executed once to trace out a Directed Acyclic Graph (DAG) of C++ / XLA kernels.
  - *Advantage*: Kernel fusion (e.g. combining MatMul + BiasAdd + ReLU into one memory access), constant folding, distributed pipeline optimization.
  - *Disadvantage*: Retracing traps if you pass non-tensor Python objects!

---

## 2. The Retracing Trap

Suppose you write:
```python
@tf.function
def compute(x, step):
    return x * step
```
- If you call `compute(x, 1)` then `compute(x, 2)`, TensorFlow **re-compiles a brand new graph** for every unique Python integer! Your training grinds to a halt.
- **The Rule**: Pass loop counters and hyper-parameters as Tensors (`tf.constant(1)`), or use `tf.Tensor` type signatures in `input_signature`.

---

## 3. Data Ingestion: The Software Assembly Line (`tf.data`)

A fast GPU is useless if it spends 80% of its time waiting for the CPU to read images from disk.
The optimal `tf.data` pipeline uses **software pipelining**:
$$\text{Disk Read} \xrightarrow{\text{parallel}} \text{CPU Transform} \xrightarrow{\text{batch}} \text{Prefetch Buffer} \to \text{GPU Computation}$$
Calling `.prefetch(tf.data.AUTOTUNE)` ensures the next batch is already sitting in RAM before the GPU finishes computing the current batch!
