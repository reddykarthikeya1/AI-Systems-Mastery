# Module 01 Set Language for Machine Learning: Self-Assessment & Mastery Challenges

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. Why is `{1, 1, 2}` equal to `{1, 2}` but `[1, 1, 2]` not equal to `[1, 2]`?
2. State De Morgan's laws and say which part people omit.
3. Why is `∅ ⊆ A` true for every A?
4. `|A| = 12`. What is `|P(A)|`, and what does that imply about exhaustive feature selection?
5. Distinguish the codomain from the range, with an ML example.
6. When does a function have a two-sided inverse, and what fails otherwise?
7. Why does the image fail to commute with intersection while the preimage does not?
8. What does convexity of both the feasible set and the objective guarantee?
9. Why does k-NN degrade in high dimensions even with abundant data?
10. Give the three conditions a train/test split must satisfy, and say which is usually violated.

## Part 2: Answer Key & Detailed Explanations

**1.** Set equality is decided by membership alone - each set contains exactly the members of the other. List equality compares element by element in order, so length and repetition both matter.

**2.** `(A ∪ B)ᶜ = Aᶜ ∩ Bᶜ` and `(A ∩ B)ᶜ = Aᶜ ∪ Bᶜ`. The omitted part is that the connective flips: distributing the negation while leaving `and` as `and` computes the other law entirely.

**3.** The definition requires every member of ∅ to be in A. ∅ has no members, so no member can fail the requirement. The statement is vacuously true - there is no possible counterexample.

**4.** 2¹² = 4,096. Each element is an independent in/out decision. With 50 features it is 2⁵⁰ ≈ 10¹⁵, so exhaustive subset search is not slow but infeasible - each extra feature doubles the work.

**5.** The codomain is the declared output type; the range is the set of values actually produced. A softmax has codomain `[0,1]ⁿ` and range the probability simplex - vectors that also sum to 1. Validating only `0 ≤ p ≤ 1` accepts `[0.9, 0.9]`, which is not a distribution.

**6.** Exactly when it is a bijection. If it is not injective, two inputs share an output and the inverse cannot choose between them - information was destroyed. If it is not surjective, some output has no preimage and the inverse is undefined there.

**7.** Distinct elements can collide under f, so `f(S) ∩ f(S')` can contain values arising from different, non-shared inputs. Only `f(S ∩ S') ⊆ f(S) ∩ f(S')` holds, with equality iff f is injective. The preimage pulls sets back without collisions, so it commutes with union, intersection and complement.

**8.** That every local minimum is a global minimum. Both conditions are needed: a convex objective over a non-convex feasible set - for example a cardinality constraint - has no such guarantee.

**9.** Distances concentrate: the ratio of farthest to nearest distance tends to 1, so neighbours are barely nearer than non-neighbours. Volume also flees to the corners - in 10 dimensions under 0.3% of the unit cube lies inside its inscribed ball.

**10.** Exhaustive, pairwise disjoint, and partitioning the correct units. The third is the one usually violated: rows are disjoint while the underlying patient, user or document appears on both sides.

## Part 3: Mastery Challenges

### 🏋️ Challenge 1: Core Implementation

Implement `group_split(rows, key, fractions, time=None)` from
Lesson 01.25 without looking at it. It must:

- partition the groups, then collect rows
- raise `ValueError` on any violated property, naming which one
- report the achieved fractions, which will not equal the requested ones

Then write a deliberately leaking split and confirm your implementation rejects
it. A splitter you have not seen refuse anything is untested.

### 🚀 Challenge 2: Stretch Problem

Extend it to **stratified group splitting**: keep the label
distribution close to the overall distribution across splits, while still never
splitting a group.

These two goals genuinely conflict - a group has one label mix and cannot be
divided to balance another split. Decide which goal wins, implement it, and
write down the maximum distribution skew your implementation can produce.
Reporting that bound is the deliverable, not the code.

## Verification Criteria

- [ ] Your splitter raises on at least three distinct leak modes
- [ ] The group-level assertion is over group ids, never row indices
- [ ] The chronological check is present and tested with a non-chronological input
- [ ] Achieved fractions are reported rather than assumed
- [ ] You can state the maximum skew your stratified version permits

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

These carry more weight than the quiz. Each is a real defect that produces a
plausible wrong answer rather than an error, and the skill being tested is
reading the symptom back to its cause.

### Diagnostic 1

A model scores 0.98 on the test set and 0.71 in production. The split was
verified: the row index sets are disjoint and their union is the full dataset.
Each patient contributes between 1 and 40 records.

<details>
<summary>Cause</summary>

The split partitions **rows**, and rows from one patient are not
independent. With up to 40 records per patient, a positional cut almost
certainly places some patient on both sides, so the model is evaluated on
patients it memorised. The row-level disjointness check passes and cannot
detect this. Compute `patients(train) & patients(test)` and assert it is
empty.

</details>

### Diagnostic 2

A grouped aggregate reports total revenue 4% below the same figure computed
without grouping. Every group total looks individually reasonable.

<details>
<summary>Cause</summary>

The grouping key is not partitioning the data - most commonly it is
null or missing for some rows, which then fall into no group. A partition must
cover every element exactly once; if per-group sums do not reconstruct the
overall sum, the key is not inducing a partition. Decide explicitly what a
missing key means before aggregating.

</details>

### Diagnostic 3

A filter intended to keep rows that are "not (fraudulent or refunded)"
removes noticeably more rows than expected. Spot checks on clearly-good and
clearly-bad rows both look right.

<details>
<summary>Cause</summary>

De Morgan applied without flipping the connective: `not (a or b)`
written as `(not a) and (not b)` is correct, but the same mistake in the other
direction - writing `not (a and b)` as `(not a) and (not b)` - computes a
strictly stronger condition and drops rows. The two forms agree whenever the
conditions agree with each other, which is why both spot checks pass; they
differ only on mixed rows.

</details>

### Diagnostic 4

Predictions decode to the wrong class names after a model is reloaded in a
different process. The model file is unchanged and accuracy on raw logits is
normal.

<details>
<summary>Cause</summary>

The label ordering was derived at load time - typically
`list(set(labels))`, whose iteration order is not guaranteed, or
`sorted(set(training_labels))`, which shifts when the training data changes.
`argmax` returns an index, and an index only means a label under a specific
ordering. The label set and its order must be saved as an artefact alongside
the weights.

</details>

---

[Module README](README.md) · [Project Guide](PROJECT_GUIDE.md)
