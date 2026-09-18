# Debug Lab Solution & Forensic Post-Mortem

## Incident: Occupancy Calculator Reports 100% for a Register-Bound Kernel

---

### 🔍 Forensic Root Cause Analysis
The number of thread blocks that can be simultaneously resident on one SM is capped independently by several physical resources: total threads per SM, total registers per SM (divided among however many registers each thread demands), shared memory per SM, and a fixed hardware maximum block count. The true number of resident blocks is the *minimum* across every limiter, because each resource is exhausted independently and a block cannot be scheduled if even one resource is out of budget. `theoretical_occupancy()` calls `blocks_per_sm_limits()`, which correctly computes all three limits (`thread_limit`, `reg_limit`, `hw_limit`), but then computes `resident_blocks = min(thread_limit, hw_limit)`, silently dropping `reg_limit` from the comparison. For this launch, `reg_limit` (2 blocks/SM, driven by 96 registers/thread) is far tighter than `thread_limit` (8 blocks/SM), so the true resident-block count is 2, not 8 -- the calculator reports occupancy as if the kernel's high register usage didn't exist at all.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def theoretical_occupancy(threads_per_block, regs_per_thread):
    thread_limit, reg_limit, hw_limit = blocks_per_sm_limits(threads_per_block, regs_per_thread)
    resident_blocks = min(thread_limit, reg_limit, hw_limit)  # bound by every limiter
    warps_per_block = threads_per_block // WARP_SIZE
    resident_warps = resident_blocks * warps_per_block
    return resident_warps / MAX_WARPS_PER_SM
```

---

### 🛡️ Production Prevention Invariants
1. **Always Take the Minimum Across All Limiters:** Any occupancy model must fold in every independent resource ceiling (threads, registers, shared memory, hardware block cap) via `min()`, never a subset of them.
2. **Cross-Check Against `nvcc --ptxas-options=-v` / Nsight:** Compare the calculator's reported occupancy against the compiler's actual register allocation per kernel and Nsight Compute's own achieved-occupancy metric on real hardware; a register-hungry kernel is exactly the case that exposes a limiter silently dropped from the model.
3. **Regression Test Each Limiter in Isolation:** Keep test cases where each of thread-count, register-count, and shared-memory is individually the binding constraint, so a future edit that drops one limiter from the `min()` is caught immediately.
