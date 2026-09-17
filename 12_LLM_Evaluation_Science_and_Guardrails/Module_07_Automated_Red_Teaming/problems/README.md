# Problem Bank — Automated Red Teaming

Practice problems for **Automated Red Teaming**, designed to build first-principles engineering competence through hands-on implementation and automated test verification.

**1 problem** · Easy/Medium · Rigorous Pytest Validation

---

## How to work these

```bash
cd problems
python -m pytest tests -q
```

Every problem must **fail** before you start — each stub raises `NotImplementedError`. Fill in `p01_detect_jailbreak_heuristics.py`, not the reference solution file.

---

## Problems

| # | Problem | Focus | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [detect_jailbreak_heuristics](p01_detect_jailbreak_heuristics.py) | Automated Red Teaming | Medium | Production Grade |

---

## 🗺️ Recommended Step-by-Step Problem Solving Path

Follow this sequence to solve the module practice problems:

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Read Requirements** | Review problem docstrings and invariants in `[p01_detect_jailbreak_heuristics.py](p01_detect_jailbreak_heuristics.py)`. |
| **2** | **Implement Solution** | Write your algorithmic solution in `problems/` to satisfy all edge cases. |
| **3** | **Run Pytest Suite** | Execute `pytest tests/` in terminal or the web Practice Arena to verify test assertions. |
| **4** | **Review Reference Code** | Inspect `[solutions/](solutions/)` to compare time/space complexity and idiomatic patterns. |

