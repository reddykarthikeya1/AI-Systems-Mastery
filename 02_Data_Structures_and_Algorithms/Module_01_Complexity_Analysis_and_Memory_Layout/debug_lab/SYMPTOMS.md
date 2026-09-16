# Debug Lab 01 — Symptoms

> A capacity-planning tool. It reads measured timings, classifies growth, and
decides whether a proposed algorithm fits inside the request budget. Every
number it reports is used to size production hardware.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_complexity_report.py
echo "exit=$?"
```

There are **5** distinct defects.

---

## Symptom 1 — A noisy measurement flips the growth classification

```
[1] Growth classification from measured timings
      index_lookup     -> O(1)
      linear_scan      -> O(n^2)
      pairwise_join    -> O(n^2)
      noisy_linear     -> O(n^2)
```

**Questions to answer:**

- `noisy_linear` doubles in size three times, and its timings roughly double each step. What was it classified as, and what should it be?
- Which two of the four measurements does `classify_growth` actually look at?
- For `linear_scan` the ratio between the first and last time is 4.0. What would the ratio be for a genuinely quadratic algorithm over the same three doublings? Are those two cases distinguishable by the quantity the function computes?

## Symptom 2 — The amortised-copy calculation cannot finish at scale

```
[2] Amortised append cost
      n=5        total element copies = 7          per-append average = 1.400
      n=1000     total element copies = 1023       per-append average = 1.023
      n=100000   total element copies = 131071     per-append average = 1.311
      (the claim is that the average is bounded by a constant)
```

**Questions to answer:**

- The report ran, so it did finish. How long did the n=100,000 row take compared with the n=5 row? What is the loop's actual cost in n?
- The problem statement allows n up to 10**9. Try changing 100_000 to 10**9 and running it again.
- Resizes happen only log2(n) times. What is the loop iterating over instead?

## Symptom 3 — Binary search comparisons are wrong at large n

```
[3] Binary search worst case
      n=1                    comparisons = 1
      n=8                    comparisons = 4
      n=1024                 comparisons = 11
      n=1000000              comparisons = 20
      n=1000000000000000000  comparisons = 60
```

**Questions to answer:**

- The report says 10**18 elements need 60 comparisons. Compute `2 ** 60` and compare it with 10**18. Is 60 enough?
- Check the smaller rows too: is the value for n=1024 right?
- `math.log2` returns a float. What is `math.log2(10**18)` exactly, and what does `int()` do to it? Compare with `(10**18).bit_length()`.

## Symptom 4 — A comparison count comes back as a float

```
[4] Pairwise comparison counts
      n=4            comparisons = 6.0                      type=float
      n=1000         comparisons = 499500.0                 type=float
      n=1000000000   comparisons = 4.999999995e+17          type=float
```

**Questions to answer:**

- Look at the reported `type` for each row. What is it, and what should a count be?
- For n=10**9 the exact answer is 499999999500000000. Compare it with what was printed. Are they equal?
- Python floats carry 53 bits of mantissa. How large can an integer get before a float can no longer represent it exactly?

## Symptom 5 — An unsupported complexity class is silently reported as 'does not fit'

```
[5] Does the proposed algorithm fit the budget?
      n=100000     O(n log n)   fits = True
      n=100000     O(n^2)       fits = False
      n=1000000000 O(n)         fits = False
      n=10         O(n!)        fits = False
      n=10         O(n^4)       fits = False

====================================================================
Report complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Two of the five checks name complexity classes the function does not handle. What did it report for them?
- `O(n!)` at n=10 is 3,628,800 operations, which is comfortably inside a 10**8 budget. Is `False` the right answer?
- Now suppose someone typos `O(n^4)` when they meant `O(n^2)`. What does the report tell them, and would they notice?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_classify_growth` |
| 2 | `test_p02_amortized_copies` |
| 3 | `test_p03_binary_search_steps` |
| 4 | `test_p04_pair_iterations` |
| 5 | `test_p05_fits_budget` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
