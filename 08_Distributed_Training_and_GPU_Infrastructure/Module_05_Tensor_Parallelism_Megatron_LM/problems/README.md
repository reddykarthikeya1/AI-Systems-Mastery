# Problem Bank — Tensor Parallelism Megatron LM

Practice problems for **Tensor Parallelism Megatron LM**, designed to build first-principles engineering competence through hands-on implementation and automated test verification.

**1 problem** · Easy/Medium · Rigorous Pytest Validation

---

## How to work these

```bash
cd problems
python -m pytest tests -q
```

Every problem must **fail** before you start — each stub raises `NotImplementedError`. Fill in `p01_compute_ring_allreduce_cost.py`, not the reference solution file.

---

## Problems

| # | Problem | Focus | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [compute_ring_allreduce_cost](p01_compute_ring_allreduce_cost.py) | Tensor Parallelism Megatron LM | Medium | Production Grade |
