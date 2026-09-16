# Module 02 Logic for Precise Reasoning: Project Guide

## Project overview

Build a toolkit that takes an informal claim, states it precisely,
and settles it - reporting *which kind of evidence* settled it.

The requirement that shapes everything: **a clean run over a domain you have not
exhausted proves nothing.** The API must make that impossible to report as a
proof by accident, which is why there are three verdicts and not two.

## 🎯 3-Tier Progressive Learning Paths

| Tier | Audience | Scope | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Foundational** | New to proof notation | Connectives, quantifiers, and truth-table classification | 2-3 hours |
| **Tier 2 — Practitioner** | Comfortable with logic, new to formalising claims | The three-verdict checker, with counterexample extraction | 4-5 hours |
| **Tier 3 — Architect** | Wants to apply it to real papers | Parse five published claims and produce a verdict report for each | 8+ hours |

Tier 1 is a coherent stopping point: a working truth-table classifier already lets you settle any
propositional question mechanically, which is the single most useful thing in
this module.

## 1. Architectural blueprint

```
  informal claim
        │
        ▼
  state precisely  ──►  variables, domain, quantifier order
        │
        ▼
  decide what settles it  ──►  proof / counterexample / neither
        │
        ▼
  search or enumerate
        │
        ▼
  verdict + evidence type
   PROVED · REFUTED · UNSETTLED
```

The third verdict is the design decision. Two-valued APIs force a clean search
to be reported as success, which is the error this whole module exists to
prevent.

## 2. Directory structure & key files

```
Module_02_Logic_for_Precise_Reasoning/
├── lessons/                  19 lessons, read in order
├── starter/                  YOUR implementation goes here
│   └── claim_verifier.py
├── project_solution/         reference implementation + its tests
│   ├── claim_verifier.py
│   └── test_claim_verifier.py
└── debug_lab/                planted defects to diagnose
    ├── broken_logic_checks.py
    ├── SYMPTOMS.md
    └── ANSWERS.md
```

## 3. Step-by-step implementation roadmap

### Phase 1: Environment & setup

```bash
cd Module_02_Logic_for_Precise_Reasoning/starter
python -m pytest ../project_solution -q      # must FAIL before you start
```

If those tests pass on an untouched starter, the grading loop is broken - report
it rather than continuing, because it will certify work you have not done.

### Phase 2: Building core capabilities (Tier 1 & 2)

1. **`implies` and `iff`** - one line each, and the truth tables
   are the specification.
2. **`for_all` / `there_exists`** - note the loop shapes differ: exit on the
   first failure versus the first success.
3. **`check_universal` / `check_existential`** - return a `Result` carrying the
   counterexample and the number of cases checked, not a bare boolean.
4. **The `exhaustive` flag** - when False, a clean run returns `UNSETTLED`.

### Phase 3: Architect stretch (Tier 3)

5. **`counterexample_shape`** - given a hypothesis and a
   conclusion, produce the predicate a refutation must satisfy. Most failed
   refutations search for the pattern where the hypothesis also fails, which
   refutes nothing.
6. **Five real claims.** Take them from papers you have read. For each, produce
   a precise statement, a verdict, and the evidence.
7. **Report the readings.** Where a claim has a true reading and a false one,
   give both rather than picking.

## 4. Verification & self-check checklist

- [ ] All shipped tests pass from `project_solution/`
- [ ] An untouched `starter/` **fails** every shipped test
- [ ] A clean run over a non-exhausted domain returns UNSETTLED, never PROVED
- [ ] A refuted universal carries the actual counterexample, not just `False`
- [ ] `equivalent` compares every assignment, not a sample
- [ ] `counterexample_shape` requires the hypothesis to hold
- [ ] Your report distinguishes the three verdicts explicitly

## 5. You Have Mastered This Module When You Can…

1. State when an implication is false, and why the other three rows are true.
2. Negate a nested quantified statement mechanically.
3. Say what a counterexample to a universal implication must look like.
4. Explain why the existential-first order is strictly stronger.
5. Choose between direct, contrapositive and contradiction, and justify it.
6. Report 'no counterexample found' without calling it a proof.

---

[Module README](README.md) · [Course Roadmap](../ROADMAP_ML_MATH.md)
