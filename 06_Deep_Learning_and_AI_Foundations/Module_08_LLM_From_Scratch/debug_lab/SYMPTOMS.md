# Debug Lab Incident Report: Greedy Decoder Gets Stuck Repeating One Token

- **Severity:** P1 Generation Quality
- **Affected Subsystem:** Module_08_LLM_From_Scratch
- **Reported Impact:** A minimal greedy text generator is supposed to walk forward through a next-token lookup table, feeding each predicted token back in as the new context for the following prediction. Instead, every generated sequence collapses into the same token repeated over and over.

---

## 🚨 Observable Symptoms & Logs
```text
Generated sequence:
the cat cat cat cat cat cat cat
Unique tokens produced: 2 out of 8 generated
```
A greedy decoder over this bigram table starting from "the" should walk `the -> cat -> sat -> on -> the -> ...`, cycling through several distinct tokens. Instead the output is almost entirely one repeated word.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_08_LLM_From_Scratch/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_greedy_decoding.py
   ```
3. Count how many distinct tokens appear in the generated sequence.

---

## 🎯 Your Objective
1. Inspect `broken_greedy_decoding.py`'s `greedy_generate()` loop.
2. Trace what value is looked up in `table` on each iteration of the loop.
3. Formulate a hypothesis for why the same token keeps appearing, then check `ANSWERS.md`.
