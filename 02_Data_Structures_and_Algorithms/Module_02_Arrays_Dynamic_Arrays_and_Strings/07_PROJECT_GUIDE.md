# Project Guide: Building a Production Dynamic Array & String Engine

## Architectural Objective
Implement `DynamicArrayEngine`: an industrial-grade, generic dynamic array in Python with explicit capacity tracking, geometric resizing ($2\times$ growth factor), shrinking/compaction on load factor $< 0.25$, and integrated algorithmic transformations (sliding window sums, two-pointer filtering, and in-place reversal).

## Key Acceptance Criteria
1. **Geometric Expansion**: When full, capacity doubles ($1 \to 2 \to 4 \to 8 \to 16 \dots$). Every reallocation event increments an internal `reallocation_count` metric.
2. **Amortized Constant Time**: Maintain $O(1)$ amortized append operations verified across $10^5$ operations.
3. **Compaction on Shrink**: When `size <= capacity // 4` and `capacity > 8`, halve capacity to prevent memory bloat.
4. **Boundary Safety**: Strict bounds checking raising `IndexError` on out-of-range indexing.
5. **Algorithmic Methods**:
   - `two_sum_target(target)`: In-place sorted Two-Pointers complement search.
   - `max_sliding_window_sum(k)`: $O(N)$ sliding window fixed size $k$.
   - `prefix_sums()`: Returns running prefix sum array in $O(N)$.
   - `reverse_in_place()`: Swaps elements in-place with $O(1)$ auxiliary memory.

## Test Verification
Run the comprehensive pytest suite:
```bash
pytest project_solution/test_dynamic_array_engine.py -v
```
