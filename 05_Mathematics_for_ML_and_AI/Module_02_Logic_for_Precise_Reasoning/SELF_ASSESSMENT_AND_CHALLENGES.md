# Module 02 Logic for Precise Reasoning: Self-Assessment & Mastery Challenges

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. When is `p → q` false, and what does that mean for refuting a claim?
2. State De Morgan for quantifiers.
3. Why is the contrapositive equivalent to the original but the converse is not?
4. Distinguish `∀x ∃y P(x,y)` from `∃y ∀x P(x,y)`.
5. What two obligations does a proof by induction carry, and how does each fail?
6. When do you need more than one base case?
7. What must the cases in a proof by cases satisfy?
8. A search over a million inputs finds no counterexample. What has been established?
9. Distinguish necessary from sufficient, using convexity and gradient descent.
10. What does 'uniformly' signal in a theorem statement?

## Part 2: Answer Key & Detailed Explanations

**1.** Only when p is true and q is false. So a counterexample must satisfy the hypothesis - a case where the hypothesis fails is consistent with the implication and refutes nothing.

**2.** `¬(∀x : P(x)) ≡ ∃x : ¬P(x)` and `¬(∃x : P(x)) ≡ ∀x : ¬P(x)`. Negation swaps the quantifier and negates the body.

**3.** `¬q → ¬p` has the same truth table as `p → q` on all four rows. The converse `q → p` differs on the two mixed rows, and is equivalent to the inverse instead.

**4.** The first lets y depend on x; the second demands one y working for every x, and is strictly stronger. The predicate 'x + y = 0' over the integers holds in the first form and fails in the second.

**5.** A base case and an inductive step. Without a base case a valid step proves nothing - the statement 'n = n+1' has a valid step. A step failing at one k leaves everything past that k unproved, which is where the all-horses argument breaks, at k = 1.

**6.** When the step reaches back further than one. A step using `P(n-3)` needs three base cases, because a single base only reaches every third value.

**7.** Exhaustiveness: their union is the whole domain. Disjointness is convenient but not required; overlap only duplicates work, while a gap invalidates the proof.

**8.** That no counterexample exists in the region searched, and nothing about the rest of the domain. The polynomial `n² + n + 41` is prime for n = 0 to 39 and composite at 40.

**9.** Convexity is sufficient for gradient descent to reach a global minimum; it is not necessary, since descent finds global minima of many non-convex objectives. Its absence removes the guarantee, not the possibility.

**10.** That an existential has been pulled in front of a universal - one constant, delta or bound works for every case rather than a different one per case. It is almost always the substantive content of the claim.

## Part 3: Mastery Challenges

### 🏋️ Challenge 1: Core Implementation

Implement the three-verdict checker from scratch. It must:

- return the actual counterexample, not `False`
- return `UNSETTLED` for a clean run over a non-exhausted domain
- unpack tuple domain items into positional predicate arguments

Then use it on `n² + n + 41` over `range(40)` and over `range(45)`, and confirm
the verdicts differ. A checker that reports the first as PROVED is the bug this
module exists to prevent.

### 🚀 Challenge 2: Stretch Problem

Take five claims from papers or blog posts you have actually
read. For each, produce:

1. the precise statement, with domain and quantifier order
2. the verdict, with evidence
3. any second reading under which the verdict changes

Expect at least one to come out as not a proposition as stated. That is a
finding, not a failure - report it with the term that lacks a definition.

## Verification Criteria

- [ ] Every verdict names its evidence type
- [ ] No clean bounded search is reported as a proof
- [ ] Counterexamples satisfy the hypothesis, not merely fail the conclusion
- [ ] Claims with two readings are reported with both
- [ ] At least one claim is correctly classified as not yet a proposition

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

These carry more weight than the quiz. Each is a real defect that produces a
plausible wrong answer rather than an error, and the skill being tested is
reading the symptom back to its cause.

### Diagnostic 1

A reviewer rejects a claim of the form "if the data is i.i.d. the bound
holds", citing an experiment on time-series data where the bound was violated.

<details>
<summary>Cause</summary>

The experiment violates the hypothesis, so it lies in the row where
the implication is vacuously true. It refutes nothing. A counterexample must be
i.i.d. data on which the bound fails - the hypothesis has to hold.

</details>

### Diagnostic 2

A validation step reports that all checks passed on every run, including
runs where the upstream job produced no rows at all.

<details>
<summary>Cause</summary>

`all([])` is True. A universal over an empty domain is vacuously
satisfied, so the check is correct and uninformative. If "no data" and "good
data" should be distinguished, assert non-emptiness separately - the quantifier
will not do it.

</details>

### Diagnostic 3

A proof that every n ≥ 8 is expressible with 3p and 5p stamps is presented
with one base case, n = 8. Spot checks at 11, 14 and 17 pass; a check at 9
fails.

<details>
<summary>Cause</summary>

The inductive step derives `P(n)` from `P(n-3)`, so a single base
case only reaches 8, 11, 14, 17 - every third value. Three base cases are
needed, for 8, 9 and 10. The passing spot checks all happened to lie on the
chain the single base case reaches.

</details>

### Diagnostic 4

An engineer concludes that because overfitting produces a train-test gap,
the observed gap means the model is overfitting. More regularisation does not
close it.

<details>
<summary>Cause</summary>

A converse error. "Overfitting implies a gap" does not give "a gap
implies overfitting". Distribution shift, a leaking split and a harder test set
all produce the same symptom. The remedy was selected by an invalid inference,
so it addresses a cause that may not be present.

</details>

---

[Module README](README.md) · [Project Guide](PROJECT_GUIDE.md)
