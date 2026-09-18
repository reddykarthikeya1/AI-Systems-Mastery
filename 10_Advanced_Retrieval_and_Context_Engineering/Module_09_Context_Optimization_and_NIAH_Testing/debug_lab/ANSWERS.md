# Debug Lab Solution & Forensic Post-Mortem

## Incident: NIAH Depth-vs-Accuracy Chart Is Mislabeled Across the Board

---

### Forensic Root Cause Analysis
`insert_needle_at_depth()` computes the insertion point by subtracting the
depth-scaled offset from the *end* of the document instead of measuring it
from the *start*:

```python
insertion_index = len(haystack) - int(depth_percent * len(haystack))
```

Walk the two extremes: at `depth_percent = 0.0`, `insertion_index =
len(haystack) - 0 = len(haystack)` -- the very END of the document. At
`depth_percent = 1.0`, `insertion_index = len(haystack) - len(haystack) = 0`
-- the very START. That is exactly backwards from the documented convention
(`0.0 = very start, 1.0 = very end`) stated in the function's own docstring.
Every requested depth `d` actually lands at measured depth `1 - d`, which is
why a needle requested at a shallow 10% depth is measured landing at 88-90%
(not landing at exactly 90% only because the needle string itself shifts the
measurement slightly). Since NIAH benchmarks specifically chart "accuracy vs.
depth" to find where a model's recall degrades, this single sign inversion
silently flips the entire chart left-to-right -- any real weakness at, say,
90% depth gets reported and investigated as a weakness at 10% depth instead.

---

### Production Corrective Action & Code Fix

```python
def insert_needle_at_depth(haystack, needle, depth_percent):
    insertion_index = int(depth_percent * len(haystack))
    return haystack[:insertion_index] + needle + haystack[insertion_index:]
```

Measuring the offset directly from the start (`depth_percent * len(haystack)`,
with no subtraction from the total length) means `depth_percent = 0.0` lands
at the start, `depth_percent = 1.0` lands at the end, and a requested 10%
depth now measures at approximately 10% after insertion.

---

### Production Prevention Invariants
1. **Verify Both Endpoints of a Percentage Mapping:** Any function taking a
   `0.0-1.0` "depth" or "position" parameter should be sanity-checked at both
   `0.0` and `1.0` explicitly -- an inverted formula is often only obvious at
   the extremes, not at a middle value like `0.5`.
2. **Round-Trip the Test Harness Against Itself:** After inserting a needle
   at a requested depth, immediately measure where it landed and assert the
   two values match within tolerance, exactly as this lab's `measured_depth()`
   does -- and fail the benchmark run loudly if they don't, rather than
   silently mislabeling results.
3. **Cross-Check Against Known-Good Reference Charts:** When a NIAH-style
   benchmark produces a result that contradicts other published or historical
   runs (e.g. "the model does uniquely badly at shallow depth"), treat the
   test harness itself as a prime suspect before concluding the model
   regressed.
