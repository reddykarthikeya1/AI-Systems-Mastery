# Debug Lab 07 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - none

The singular values are in descending order, which is the convention
`numpy.linalg.svd` uses, and the total energy is the sum of squares - the
squared Frobenius norm. Both correct.

---

## Defect 2 - truncating from the wrong end

**Where:** `energy_kept`.

```python
kept = sum(s * s for s in singular_values[-k:])      # the SMALLEST k
```

`[-k:]` takes the last k of a descending list: the least important directions.
The Eckart-Young theorem says the best rank-k approximation keeps the k
**largest** singular values, so this keeps precisely the ones that should be
discarded.

With `[50, 12, 3, 0.4, 0.05]`, k=1 should retain 50^2 / 2653 = 94.2% of the
energy. Taking the smallest instead retains 0.05^2 / 2653, which is about
0.0001%.

**The fix.**

```python
kept = sum(s * s for s in singular_values[:k])
```

**The general lesson.** `[:k]` and `[-k:]` are both plausible-looking slices
and they are opposites. Whenever an algorithm depends on an ordering
convention, write the convention down next to the slice - and test with values
that are obviously unequal, so taking the wrong end is visible rather than
merely slightly worse.

---

## Defect 3 - a consequence, not a separate bug

`choose_rank` and `compression_ratio` are both correct. They inherit the
inverted energy calculation: because k=1 appears to retain nothing, the search
runs to k=5, and the compression ratio for k=5 is genuinely poor.

Fix defect 2 and this section corrects itself. With the right slice, 99% energy
is reached at k=2, and a 1000x1000 matrix compresses from 1,000,000 parameters
to 4,000 - a 250x reduction, which is the entire argument for LoRA.

**The general lesson.** One wrong slice propagated into a capacity decision and
a cost estimate. When several numbers are wrong together, look for the single
upstream quantity they all derive from rather than fixing them one by one - and
notice that the downstream numbers stayed internally consistent the whole time,
which is why nothing looked alarming.
