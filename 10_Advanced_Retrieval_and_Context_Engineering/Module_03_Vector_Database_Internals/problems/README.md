# Problem Bank — Vector Database Internals

Practice problems for **Vector Database Internals**, designed to build first-principles engineering competence through hands-on implementation and automated test verification.

**1 problem** · Easy/Medium · Rigorous Pytest Validation

---

## How to work these

```bash
cd problems
python -m pytest tests -q
```

Every problem must **fail** before you start — each stub raises `NotImplementedError`. Fill in `p01_compute_rrf_scores.py`, not the reference solution file.

---

## Problems

| # | Problem | Focus | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [compute_rrf_scores](p01_compute_rrf_scores.py) | Vector Database Internals | Medium | Production Grade |

---

## 🗺️ Recommended Step-by-Step Problem Solving Path

Follow this sequence to solve the module practice problems:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Read Requirements** | Review problem docstrings and invariants in `[p01_compute_rrf_scores.py](p01_compute_rrf_scores.py)`. |
| **2** | **Implement Solution** | Write your algorithmic solution in `problems/` to satisfy all edge cases. |
| **3** | **Run Pytest Suite** | Execute `pytest tests/` in terminal or the web Practice Arena to verify test assertions. |
| **4** | **Review Reference Code** | Inspect `[solutions/](solutions/)` to compare time/space complexity and idiomatic patterns. |

