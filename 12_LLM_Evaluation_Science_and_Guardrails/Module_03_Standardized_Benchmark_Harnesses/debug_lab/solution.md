# Debug Lab Solution: Pass@k Boundary Overflow Bug

### The Defect
`BrokenBenchmark` crashes when $n - c < k$ because `math.comb(n - c, k)` raises or produces invalid values.

### The Fix
Guard with `if n - c < k: return 1.0` as shown in `project_solution/benchmark_harness_sim.py`.
