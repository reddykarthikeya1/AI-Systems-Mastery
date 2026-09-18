# Debug Lab Incident Report: Warp Completion Latency Estimator Undercounts Divergent Branches

- **Severity:** P2 Performance Modeling Error
- **Affected Subsystem:** Module_01_GPU_Microarchitecture_and_Execution_Model
- **Reported Impact:** A warp-latency estimator is supposed to account for branch divergence: when threads within the same warp take different paths through an if/else, a real SIMT core must execute both paths (masking the inactive lanes each time), not just the slower of the two. The estimator's reported latency for a divergent warp does not match the sum of the two paths' costs.

---

## 🚨 Observable Symptoms & Logs
```text
Warp of 32 threads: half take the 'if' branch (4 cycles), half take 'else' (6 cycles).
Estimated warp completion latency: 6 cycles
Cycles spent on the 'if' path + cycles spent on the 'else' path: 4 + 6 = 10 cycles
```
Half the warp's 32 threads take the 4-cycle 'if' path and half take the 6-cycle 'else' path. Because both groups belong to the same warp and a warp issues one instruction stream at a time, a real GPU core spends time on *both* paths back to back.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_01_GPU_Microarchitecture_and_Execution_Model/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_warp_divergence.py
   ```
3. Compare the 'Estimated warp completion latency' line against the sum of the two branch costs printed on the next line.

---

## 🎯 Your Objective
1. Inspect `broken_warp_divergence.py`'s `simulate_warp_naive()` function.
2. Work out what assumption it makes about how a warp with two different branch outcomes actually executes on real SIMT hardware.
3. Formulate a hypothesis for why the estimate is lower than the sum of the two paths' costs, then check `ANSWERS.md`.
