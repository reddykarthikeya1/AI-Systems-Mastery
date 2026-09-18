# Debug Lab Incident Report: pass@k Benchmark Crashes With a ZeroDivisionError When k Exceeds the Number of Sampled Completions

- **Severity:** P2 Evaluation Reliability
- **Affected Subsystem:** Module_03_Standardized_Benchmark_Harnesses
- **Reported Impact:** A nightly benchmark run crashed partway through the report. pass@1, pass@3, and pass@5 all computed fine for the same problem, but the moment the sweep reached pass@10 -- a completely ordinary configuration value -- the harness raised an unhandled exception and the whole run had to be restarted from scratch.

---

## 🚨 Observable Symptoms & Logs
```text
pass@1 (n=5, c=2) = 0.4000
pass@3 (n=5, c=2) = 0.9000
pass@5 (n=5, c=2) = 1.0000
pass@10 (n=5, c=2) crashed: ZeroDivisionError: division by zero
```
For the same problem, sampled the same 5 times (`n=5`) with 2 of those completions passing (`c=2`), `pass_at_k()` returns clean, plausible-looking numbers for `k=1`, `k=3`, and `k=5`. Nothing about those results looks suspicious. The exact same function, called with the exact same `n` and `c` and only `k` changed to `10`, raises `ZeroDivisionError` and takes the whole computation down instead of returning a score.

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_03_Standardized_Benchmark_Harnesses/debug_lab
   ```
2. `broken_benchmark.py` only defines `BrokenBenchmark`; it has no demo entry point of its own. Save the snippet below as `repro.py` in the same directory and run `python repro.py`:
   ```python
   from broken_benchmark import BrokenBenchmark

   bench = BrokenBenchmark()

   for k in [1, 3, 5, 10]:
       try:
           val = bench.pass_at_k(n=5, c=2, k=k)
           print(f"pass@{k} (n=5, c=2) = {val:.4f}")
       except ZeroDivisionError as e:
           print(f"pass@{k} (n=5, c=2) crashed: {type(e).__name__}: {e}")
   ```
3. Observe that `k <= n` always works, but `k > n` -- a perfectly ordinary configuration when only a handful of completions were sampled per problem -- crashes instead of returning a defined result.

---

## 🎯 Your Objective
1. Inspect `pass_at_k()` and look up what `math.comb(n, k)` returns when `k` is larger than `n`.
2. Compute the denominator `math.comb(n, k)` by hand for `n=5`, `k=10`.
3. Formulate a hypothesis for what should happen instead when a caller asks for pass@k with more samples requested (`k`) than were actually generated (`n`), then check `ANSWERS.md`.
