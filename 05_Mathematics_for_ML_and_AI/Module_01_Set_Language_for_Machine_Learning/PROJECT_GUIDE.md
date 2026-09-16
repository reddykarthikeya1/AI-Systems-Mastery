# Module 01 Set Language for Machine Learning: Project Guide

## Project overview

Build a dataset splitter that **cannot** leak - not because it is
written carefully, but because it verifies the properties it claims and refuses
to return a split that fails them.

The one requirement that shapes every decision: **the split must partition the
units of independence, not the rows.** Everything else follows from that.

## 🎯 3-Tier Progressive Learning Paths

| Tier | Audience | Scope | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Foundational** | First time with set notation | Row-level split with exhaustiveness and disjointness assertions | 2-3 hours |
| **Tier 2 — Practitioner** | Comfortable with sets, new to leakage | Group-aware split, plus a chronological mode | 4-5 hours |
| **Tier 3 — Architect** | Wants the production version | Stratification, nested splits, and leakage detection for fitted transforms | 8+ hours |

Tier 1 is a coherent stopping point: a row-level splitter that proves it dropped nothing and
duplicated nothing is already better than most hand-written splits, and it is
the foundation the group logic sits on.

## 1. Architectural blueprint

Three layers, and the middle one is where the value is.

```
      rows  ─────────────►  key(row)  ─────────────►  groups
                                                        │
                                          partition the GROUPS
                                                        │
                                                        ▼
                                          collect each group's rows
                                                        │
                                                        ▼
                                             assert the properties
                                        (exhaustive, disjoint, chronological)
```

The order matters. Partitioning groups and then collecting rows makes the
property true by construction; collecting rows and then trying to repair
overlaps does not converge, because repairing one overlap creates another.

The assertions are not a test-suite concern. They live in the splitter and raise,
because a splitter that returns a leaking split quietly is worse than one that
refuses.

## 2. Directory structure & key files

```
Module_01_Set_Language_for_Machine_Learning/
├── lessons/                  25 lessons, read in order
├── starter/                  YOUR implementation goes here
│   └── dataset_partition_validator.py
├── project_solution/         reference implementation + its tests
│   ├── dataset_partition_validator.py
│   └── test_dataset_partition_validator.py
└── debug_lab/                planted defects to diagnose
    ├── broken_dataset_split.py
    ├── SYMPTOMS.md
    └── ANSWERS.md
```

## 3. Step-by-step implementation roadmap

### Phase 1: Environment & setup

```bash
cd Module_01_Set_Language_for_Machine_Learning/starter
python -m pytest ../project_solution -q      # must FAIL before you start
```

If those tests pass on an untouched starter, the grading loop is broken - report
it rather than continuing, because it will certify work you have not done.

### Phase 2: Building core capabilities (Tier 1 & 2)

1. **`split(rows, fractions)`** - positional split. Assert
   exhaustiveness (`train | val | test == rows`) and pairwise disjointness.
2. **`group_split(rows, key, fractions)`** - partition the groups first. The
   assertion that matters is over group ids, not row indices.
3. **Accept the size drift.** A group split cannot hit 70/30 exactly, because
   groups are indivisible. Report the achieved fractions rather than pretending.
4. **`time` parameter** - when given, assert
   `max(train times) < min(test times)`. Disjointness does not imply this.

### Phase 3: Architect stretch (Tier 3)

5. **Stratification** - keep the label distribution roughly equal
   across splits while still partitioning by group. These two goals conflict;
   decide which wins and document it.
6. **Nested splits** for cross-validation, where every fold must satisfy the
   same properties and the union of the test folds must be the whole dataset.
7. **Detect transform leakage** - a scaler fitted before the split leaks the
   test set's statistics without putting any row on both sides. Write a check
   that catches it.

## 4. Verification & self-check checklist

- [ ] All shipped tests pass from `project_solution/`
- [ ] An untouched `starter/` **fails** every shipped test
- [ ] `train ∪ val ∪ test` equals the full row set - nothing was dropped
- [ ] All three pairwise intersections are empty **at the group level**
- [ ] The splitter raises rather than returning a leaking split
- [ ] With a `time` column, every training timestamp precedes every test timestamp
- [ ] A deliberately leaking input is rejected by your own assertions

## 5. You Have Mastered This Module When You Can…

1. Say what the unit of independence is for a given dataset, and justify it.
2. Explain why a row-level disjointness check always passes and proves nothing.
3. Write the three assertions that make a split verifiable, from memory.
4. Explain why a group split cannot hit an exact 70/30 and why that is correct.
5. Name two leaks that a disjointness check cannot catch, and how to catch them.
6. Translate 'no patient appears in both halves' into set notation and into code.

---

[Module README](README.md) · [Course Roadmap](../ROADMAP_ML_MATH.md)
