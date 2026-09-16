# Module 02 Logic for Precise Reasoning: Troubleshooting & Edge Cases

Symptoms first, because that is what you have when it happens.

---

## 1. A counterexample that refutes nothing

**Symptom**

```
claim:     for all m, calibrated(m) -> brier(m) < 0.2
proposed:  an UNCALIBRATED model with brier 0.30
verdict:   refutes nothing
```

**Cause.** An implication is only false when the hypothesis holds and the conclusion fails. A case where the hypothesis fails sits in a row where the implication is vacuously true.

**Fix.** Search for the pattern where the hypothesis holds and the conclusion fails. `counterexample_shape(hypothesis, conclusion)` builds that predicate so the hypothesis cannot be dropped by accident.

---

## 2. A bounded search reported as a proof

**Symptom**

```
checked n = 0..39 for primality of n^2+n+41
result:   no counterexample
reported: PROVED
```

**Cause.** The domain was not exhausted. At n = 40 the value is 1681 = 41 squared, so the claim is false and the smallest counterexample is one step past the search.

**Fix.** Pass `exhaustive=False` whenever the domain is infinite or merely sampled. The checker then returns UNSETTLED, which is the honest verdict.

---

## 3. An induction with too few base cases

**Symptom**

```
base case: P(8)
step:      P(n-3) -> P(n)
P(9) fails
```

**Cause.** A step reaching back three values needs three base cases. A single base only establishes 8, 11, 14, ... - every third value.

**Fix.** Count how far back the step reaches and supply that many base cases. The same rule applies to recursive functions with multiple recursive calls.

---

## 4. A for-all loop that implements there-exists

**Symptom**

```
for v in values:
    if predicate(v):
        return True
return False
```

**Cause.** Returning True on the first success is the existential. A universal returns False on the first failure. The two agree on collections that are entirely passing or entirely failing, which is what hand-written test data usually looks like.

**Fix.** Invert it: return False on the first failure, and True after the loop. Or use `all()`, which has the right shape by construction.

---

## 5. Logical equivalence asserted from agreement on a sample

**Symptom**

```
f(1,1) == g(1,1)  ok
f(0,0) == g(0,0)  ok
-> replaced f with g
production differs
```

**Cause.** Equivalence requires agreement on every assignment. The two rows checked were the ones where the expressions happen to coincide; they differ on the mixed rows.

**Fix.** Enumerate all assignments. For up to about 20 variables that is cheap, and it is a genuine proof rather than evidence.

---


[Module README](README.md)
