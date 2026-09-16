# Lesson 02.19 — Module Project: Verify or Refute Five Published Claims

> **Module 02:** Logic for Precise Reasoning · Lesson 19 of 19

---

## What you will be able to do after this lesson

- [ ] Take five informal claims, state each as a precise proposition, and verify or refute it.
- [ ] Report each verdict with the evidence type - proof, counterexample, or undecidable as stated.

## Prerequisites

- [Lesson 02.16](16_Counterexamples_and_Disproof.md) - counterexamples.
- [Lesson 02.17](17_Reading_a_Theorem_Statement_in_a_Paper.md) - reading theorems.
- [Lesson 02.18](18_Necessary_versus_Sufficient_Conditions_in_ML_Claims.md) - necessary and sufficient.

---

## 1. The idea

The module project: take claims of the kind that appear in papers, blog posts
and code review, and put each through the full pipeline.

For each claim:

1. **State it precisely** - variables, domain, quantifiers. If it cannot be
   stated, that *is* the finding.
2. **Decide what would settle it** - a proof for a universal, one counterexample
   to refute, one witness for an existential.
3. **Do that.**
4. **Report the verdict with its evidence type**, and say what remains open.

Three verdicts are possible and all are legitimate results:

| Verdict | Evidence |
| :--- | :--- |
| True | proof covering the stated domain |
| False | one explicit counterexample |
| Not a proposition | the term that has no definition |

The third is the most common outcome for informal claims, and reporting it is
more useful than guessing which reading was meant.

The reference implementation is in
[`project_solution/`](../project_solution); this lesson works two of the five.

## 2. Worked example

**Claim 1.** "Adding a layer never increases training error."

Precisely: for a network N and `N'` identical plus one layer, trained to
convergence, `train_error(N') ≤ train_error(N)`.

Verdict: **false as stated**. `N'` can represent everything `N` can - set the
extra layer to identity - so the *minimum achievable* error does not increase.
But "trained to convergence" is about what optimisation finds, not what the
class contains, and deeper networks are harder to optimise. The claim confuses
*representational capacity* with *achieved training error*, and the degradation
result of He et al. is the counterexample.

A true nearby claim: `min over parameters` of training error does not increase.
That is about the hypothesis class and is provable by the identity construction.

**Claim 2.** "If two models have the same accuracy, they make the same
predictions."

Precisely: `accuracy(A) = accuracy(B) → predictions(A) = predictions(B)`.

Verdict: **false**, by counterexample. On four examples with labels
`[1,1,0,0]`, model A predicts `[1,1,1,1]` and B predicts `[0,1,0,1]`. Both score
0.5, and they agree on only two of the four items. Accuracy is a *summary*, and
summaries are not injective - many prediction vectors map to the same number.

This is Lesson 01.12 again: a non-injective map cannot be inverted, so you
cannot recover predictions from a score.

## 3. Verify it in code

```python
# Claim 2: equal accuracy does not imply equal predictions.
labels = [1, 1, 0, 0]
model_a = [1, 1, 1, 1]
model_b = [0, 1, 0, 1]

def accuracy(pred, truth):
    return sum(p == t for p, t in zip(pred, truth)) / len(truth)

assert accuracy(model_a, labels) == 0.5
assert accuracy(model_b, labels) == 0.5
assert model_a != model_b, "same score, different predictions"
agreement = sum(a == b for a, b in zip(model_a, model_b)) / len(labels)
assert agreement == 0.5

# Accuracy is not injective: count prediction vectors scoring exactly 0.5.
from itertools import product
same_score = [p for p in product([0, 1], repeat=4) if accuracy(p, labels) == 0.5]
assert len(same_score) == 6, "six different vectors share one score"

# Claim 1, the TRUE nearby version: an extra identity layer cannot reduce capacity.
def represents(depth, target):
    # A depth-d net can represent anything a depth-(d-1) net can: set the extra
    # layer to the identity.
    return depth >= target

for target in range(1, 6):
    assert represents(target, target)
    assert represents(target + 1, target), "deeper represents everything shallower does"

# But "achieved" error is about optimisation, not representation - a different claim.
achievable_min = {1: 0.30, 2: 0.22, 3: 0.18}
achieved = {1: 0.30, 2: 0.22, 3: 0.26}          # depth 3 optimised worse
assert achievable_min[3] < achievable_min[2], "capacity did not decrease"
assert achieved[3] > achieved[2], "and yet training error rose"
```

## 4. The mistake people actually make

**Refuting a claim the author did not make.**

"Adding a layer never increases training error" has a true reading
(representational capacity) and a false one (error actually achieved). Attacking
the false reading when the author meant the true one wins nothing, and vice
versa.

The discipline that avoids it: state the claim precisely *before* looking for a
counterexample, and if two readings exist, say so and evaluate both. "Under
reading A this is true by the identity construction; under reading B it is false
and here is the counterexample" is a complete and honest answer, and it is more
useful than either half.

The second failure is declaring a claim false because it lacks a proof. Absence
of a proof is not a refutation - it means the claim is *unsettled*, which is a
third verdict and a legitimate one to report.

Keep the three verdicts distinct: proved, refuted by a named counterexample, or
not yet a proposition. Collapsing them is how confident wrong statements get
made.

---

## Check yourself

1. What are the three possible verdicts, and what evidence does each require?
2. Give a counterexample to 'equal accuracy implies equal predictions'.
3. A claim has a true reading and a false one. What should you report?

<details>
<summary>Answers</summary>

1. True, requiring a proof over the stated domain. False, requiring one explicit counterexample. Not a proposition, requiring you to name the undefined term.
2. Labels `[1,1,0,0]`; model A predicts `[1,1,1,1]` and model B predicts `[0,1,0,1]`. Both score 0.5 and they agree on only two of the four items.
3. Both, explicitly: state each reading, give the proof for the true one and the counterexample for the false one. Choosing one reading silently and reporting a single verdict misrepresents the situation.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](18_Necessary_versus_Sufficient_Conditions_in_ML_Claims.md) · [Module README](../README.md)
