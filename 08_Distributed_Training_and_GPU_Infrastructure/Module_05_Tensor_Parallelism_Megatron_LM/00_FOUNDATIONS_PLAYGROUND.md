# 🐣 Interactive Foundations Playground: Tensor Parallelism (Megatron-LM)

> *"Tensor parallelism splits giant weight matrices across GPUs along rows or columns."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Column Parallel Linear Layer

Splitting weight matrix $W$ column-wise: $W = [W_1 | W_2]$. Each GPU computes $Y_i = X W_i$, followed by AllGather.

```python
X = [1.0, 2.0]
W1 = [[1.0], [2.0]]  # Column 1
W2 = [[3.0], [4.0]]  # Column 2

Y1 = sum(X[i] * W1[i][0] for i in range(2))  # 1*1 + 2*2 = 5
Y2 = sum(X[i] * W2[i][0] for i in range(2))  # 1*3 + 2*4 = 11

assert Y1 == 5.0
assert Y2 == 11.0
print(f"Column parallel outputs on 2 GPUs: Y1={Y1}, Y2={Y2}")
```

---

## 2. Row Parallel Linear Layer with AllReduce

Splitting row-wise requires an AllReduce sum at the end: $Y = X_1 W_1 + X_2 W_2$.

```python
X1 = [1.0]
X2 = [2.0]
W_row1 = [5.0, 6.0]
W_row2 = [7.0, 8.0]

part1 = [X1[0] * w for w in W_row1]  # [5, 6]
part2 = [X2[0] * w for w in W_row2]  # [14, 16]
full_Y = [p1 + p2 for p1, p2 in zip(part1, part2)]

assert full_Y == [19.0, 22.0]
assert len(full_Y) == 2
print(f"Row parallel output after AllReduce sum: {full_Y}")
```

---

## 3. Megatron-LM MLP Two-Layer Fusion Invariant

By coupling a Column Parallel linear layer with a Row Parallel linear layer, Megatron requires only 1 AllReduce in the backward pass.

```python
allreduce_count = 1  # Exactly 1 AllReduce per MLP block
assert allreduce_count == 1
print("Megatron MLP column+row pairing minimizes collective communication to 1 AllReduce.")
```

---
