# 🐣 Interactive Foundations Playground: 3D Parallelism Integration & Orchestration

> *"3D Parallelism combines Data, Tensor, and Pipeline parallelism into a unified training grid."*

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

## 1. Cluster Grid 3D Dimensions

World size factorizes as $\text{Total GPUs} = DP \times TP \times PP$.

```python
TP, PP, DP = 4, 8, 16
total_gpus = TP * PP * DP

assert total_gpus == 512
assert total_gpus % (TP * PP) == 0
print(f"3D Parallel grid: TP={TP}, PP={PP}, DP={DP} utilizes {total_gpus} GPUs.")
```

---

## 2. Rank Mapping to 3D Coordinates

Mapping global rank to $(tp\_id, pp\_id, dp\_id)$ coordinates via integer division and modulo.

```python
def get_3d_coords(rank, tp, pp, dp):
    tp_id = rank % tp
    pp_id = (rank // tp) % pp
    dp_id = rank // (tp * pp)
    return tp_id, pp_id, dp_id

coords = get_3d_coords(100, 4, 8, 16)
assert coords == (0, 1, 3)
assert get_3d_coords(0, 4, 8, 16) == (0, 0, 0)
print(f"Rank 100 mapped to 3D grid: TP={coords[0]}, PP={coords[1]}, DP={coords[2]}")
```

---

## 3. Total Training Throughput Calculation

Cluster throughput is $T = \text{Total GPUs} \times \text{TFLOP/s per GPU} \times \text{MFU}$.

```python
mfu = 0.45  # Model FLOPs Utilization 45%
tflops_per_gpu = 300.0
effective_pflops = (total_gpus * tflops_per_gpu * mfu) / 1000.0

assert round(effective_pflops, 2) == 69.12
print(f"Effective cluster compute throughput: {effective_pflops:.2f} PFLOP/s")
```

---
