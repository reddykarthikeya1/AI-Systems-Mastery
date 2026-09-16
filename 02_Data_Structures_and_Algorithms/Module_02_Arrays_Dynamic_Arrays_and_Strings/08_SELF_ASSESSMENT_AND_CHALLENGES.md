# Self-Assessment & Staff Interview Challenges: Arrays & Strings

## Conceptual Multiple Choice & Proofs

### Q1: Memory & Cache Hierarchy
Why does an $O(N)$ sequential array scan execute significantly faster than an $O(N)$ linked list traversal?
- [x] **A)** Arrays exhibit high spatial locality, loading 64-byte cache lines into CPU L1/L2 caches, whereas linked lists trigger frequent RAM cache misses due to pointer chasing.
- [ ] **B)** Arrays have lower Big-O asymptotic notation than linked lists.
- [ ] **C)** Python dictionaries optimize array pointers in registers.
- [ ] **D)** CPU arithmetic units can only process integers inside arrays.

### Q2: Dynamic Array Resizing
What is the mathematical consequence of growing a dynamic array by adding a constant $+100$ slots rather than multiplying by $2\times$?
- [ ] **A)** It preserves $O(1)$ amortized append while reducing memory consumption.
- [x] **B)** It degrades the amortized cost per append to $O(N)$, causing total time for $N$ appends to reach $O(N^2)$.
- [ ] **C)** It reduces CPU memory fragmentation.
- [ ] **D)** It prevents OS page fault allocation.

---

## Staff-Level System Design Scenario

*You are designing a high-throughput financial time-series ingestion engine processing 10,000,000 tick quotes per second. How do you store the incoming sliding window of price ticks without triggering memory allocations, garbage collection pauses, or cache misses?*

**Architectural Answer Key**:
1. Pre-allocate a fixed-size **Circular Ring Buffer** on an aligned contiguous memory segment matching CPU cache lines.
2. Maintain `head` and `tail` monotonic integer counters with bitmask modulo index wrapping (`index & (BUFFER_SIZE - 1)` where `BUFFER_SIZE` is a power of 2).
3. Zero heap allocations during hot-path streaming; overwrite expired slots in-place, achieving deterministic sub-microsecond latency.
