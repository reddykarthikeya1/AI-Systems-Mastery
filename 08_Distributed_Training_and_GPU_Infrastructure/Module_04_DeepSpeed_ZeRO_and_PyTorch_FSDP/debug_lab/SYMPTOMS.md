# Debug Lab Incident Report: ZeRO Sharding Leaves a Tail of Parameters Permanently Stale

- **Severity:** P1 Silent Training Corruption
- **Affected Subsystem:** Module_04_DeepSpeed_ZeRO_and_PyTorch_FSDP
- **Reported Impact:** A ZeRO-style optimizer-state partitioner splits 10 flattened parameters across 4 ranks so each rank owns and updates exactly one contiguous shard. Every parameter index should be owned by exactly one rank. Two of the ten parameter indices are never assigned to any rank's shard and are therefore never updated by any optimizer step.

---

## 🚨 Observable Symptoms & Logs
```text
num_params=10, world_size=4
Shard ranges per rank: [(0, 2), (2, 4), (4, 6), (6, 8)]
Parameters updated by some rank:  [0, 1, 2, 3, 4, 5, 6, 7]
Parameters that should be updated: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Never-updated (stale) parameter indices: [8, 9]
```
Four ranks each claim a shard of size 2, covering only indices 0 through 7. Parameters 8 and 9 fall outside every rank's `[lo, hi)` range and are never touched by any optimizer update -- their values would silently stay at their initialization forever while training "succeeds" with no error or warning.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_04_DeepSpeed_ZeRO_and_PyTorch_FSDP/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_zero_partition.py
   ```
3. Compare the "Parameters updated by some rank" line against the "Parameters that should be updated" line, and note the never-updated indices.

---

## 🎯 Your Objective
1. Inspect `broken_zero_partition.py`'s `partition_ranges()` function, specifically how `shard_size` is computed from `num_params` and `world_size` when they don't divide evenly.
2. Work out how many parameters `world_size * shard_size` actually covers when `num_params` is not a multiple of `world_size`, and what happens to the rest.
3. Formulate a hypothesis for why exactly the *last* `num_params % world_size` parameter indices are the ones left unassigned, then check `ANSWERS.md`.
