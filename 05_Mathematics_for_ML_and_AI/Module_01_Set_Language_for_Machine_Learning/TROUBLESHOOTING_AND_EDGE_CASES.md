# Module 01 Set Language for Machine Learning: Troubleshooting & Edge Cases

Symptoms first, because that is what you have when it happens.

---

## 1. `{}` is not the empty set

**Symptom**

```
>>> type({})
<class 'dict'>
>>> {}.add(1)
AttributeError: 'dict' object has no attribute 'add'
```

**Cause.** In Python `{}` is an empty dictionary. The empty set is `set()`. Both are falsy and both have length 0, so the mistake survives every truthiness and length check and only surfaces when a set method is called.

**Fix.** Use `set()`. If you want an empty set literal for readability, there is not one - this is a genuine wart in the syntax.

---

## 2. A split passes every check and the model still leaks

**Symptom**

```
assert set(train) & set(test) == set()   # passes
test accuracy 0.98, production accuracy 0.71
```

**Cause.** The assertion is over row indices, which are disjoint by construction for any positional split. The unit of independence - patient, user, document - can still appear on both sides.

**Fix.** Assert over the group ids: `assert units(train) & units(test) == set()`. Defining `units` correctly is a question about the data, not the code.

---

## 3. Per-group totals do not reconstruct the overall total

**Symptom**

```
sum(group_totals) = 961_204
sum(all_rows)     = 1_001_337
```

**Cause.** The grouping key is not inducing a partition. Rows whose key is null or missing fall into no group, so the blocks do not cover the data.

**Fix.** Assert `sum(per group) == sum(all)` before trusting any grouped aggregate, and decide explicitly what a missing key means rather than letting the engine choose.

---

## 4. `np.intersect1d` reordered my rows

**Symptom**

```
ids    = [30, 10, 20]
picked = np.intersect1d(ids, [10, 30])   -> [10, 30]
```

**Cause.** All of NumPy's set routines return sorted, deduplicated arrays. Using the result to index back into the original data reorders rows relative to every parallel array that was not reordered with it.

**Fix.** Select with a boolean mask instead: `mask = np.isin(ids, wanted)`, then apply that same mask to every parallel array. Order and alignment are preserved.

---

## 5. A validation loop reports success on an empty batch

**Symptom**

```
checked 0 rows, all rules satisfied -> PASS
```

**Cause.** `all([])` is True. 'Every element satisfies P' cannot be falsified when there are no elements, so the quantifier reports success vacuously.

**Fix.** Test for emptiness separately if 'no data' and 'data that passed' should be distinguished. The quantifier is behaving correctly and will not do it for you.

---


[Module README](README.md)
