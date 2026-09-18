# Debug Lab Incident Report: Occupancy Calculator Reports 100% for a Register-Bound Kernel

- **Severity:** P2 Performance Modeling Error
- **Affected Subsystem:** Module_11_Profiling_with_Nsight_Compute_and_Systems
- **Reported Impact:** A theoretical-occupancy calculator (meant to reproduce the kind of number Nsight Compute reports as "Achieved Occupancy" / "Theoretical Occupancy") is run against a register-hungry kernel launch (256 threads/block, 96 registers/thread) and reports 100% occupancy, while a per-limiter breakdown computed alongside it shows the kernel can only fit a small fraction of the SM's warps.

---

## 🚨 Observable Symptoms & Logs
```text
threads_per_block=256, regs_per_thread=96
Per-limiter resident blocks/SM -> thread: 8, register: 2, hw: 32
Nsight-style achieved occupancy (binding limiter): 25.00%
Calculator-reported theoretical occupancy:         100.00%
```
The thread-count limiter alone would allow 8 resident blocks per SM (100% occupancy), and the hardware block-count cap allows 32. But the register limiter allows only 2 resident blocks per SM -- far tighter than either. The calculator's reported occupancy matches the loosest limiter, not the tightest one.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_11_Profiling_with_Nsight_Compute_and_Systems/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_occupancy_calculator.py
   ```
3. Compare the three per-limiter resident-block counts (thread, register, hw) against the "Calculator-reported theoretical occupancy" line.

---

## 🎯 Your Objective
1. Inspect `broken_occupancy_calculator.py`'s `theoretical_occupancy()` function and see which of the three values returned by `blocks_per_sm_limits()` it actually uses to compute `resident_blocks`.
2. Work out, on real hardware, how many blocks can actually be resident on one SM simultaneously when three independent resources (threads, registers, and a hardware block-count cap) each impose their own ceiling.
3. Formulate a hypothesis for why a kernel can be far more register-constrained than thread-constrained, and why the reported number is dangerously optimistic here, then check `ANSWERS.md`.
