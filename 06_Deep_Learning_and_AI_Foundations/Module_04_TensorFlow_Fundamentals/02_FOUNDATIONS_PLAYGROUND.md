# 🐣 Interactive Foundations Playground: TensorFlow Fundamentals & Static Graphs

> *"Static graphs compile the computational blueprint once, optimizing execution before any data flows."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Tensor Shape and Stride Manipulation

A multidimensional tensor is an array with dimensions (shape) stored in contiguous memory layout.

```python
shape = (2, 3)
total_elements = shape[0] * shape[1]
strides = (shape[1], 1)

assert total_elements == 6
assert strides == (3, 1)
print(f"Tensor shape {shape} has {total_elements} elements with strides {strides}")
```

---

## 2. Flattening and Index Coordinate Mapping

Mapping 2D matrix coordinates $(r, c)$ into 1D linear buffer offset via row-major order: $\text{offset} = r \cdot C + c$.

```python
def to_1d(r, c, cols):
    return r * cols + c

assert to_1d(0, 0, 3) == 0
assert to_1d(1, 2, 3) == 5
assert to_1d(1, 0, 3) == 3
print("Row-major coordinate translation verified.")
```

---

## 3. Broadcasting Semantics

Broadcasting stretches singleton dimensions to match larger tensor ranks without physically copying underlying memory.

```python
matrix = [[1, 2, 3], [4, 5, 6]]
bias_vec = [10, 20, 30]

result = [[matrix[r][c] + bias_vec[c] for c in range(3)] for r in range(2)]
assert result[0] == [11, 22, 33]
assert result[1] == [14, 25, 36]
print(f"Broadcasted addition result: {result}")
```

---
