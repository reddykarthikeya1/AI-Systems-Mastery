# Phase 2 Checkpoint — Pointers, Stacks and Hashing

- **Curriculum Modules:** Modules 03 - 05 (Linked Lists and Pointer Manipulation, Stacks Queues and Monotonic Structures, Hash Tables and Collision Resolution)

- [Module 03 — Linked Lists and Pointer Manipulation](../Module_03_Linked_Lists_and_Pointer_Manipulation/01_README.md)
- [Module 04 — Stacks Queues and Monotonic Structures](../Module_04_Stacks_Queues_and_Monotonic_Structures/01_README.md)
- [Module 05 — Hash Tables and Collision Resolution](../Module_05_Hash_Tables_and_Collision_Resolution/01_README.md)

---

## What this checkpoint proves

You can manipulate linked structures without losing data, recognise a monotonic
stack from the problem statement, and know what a hash map cannot do.

A checkpoint is not a quiz. It is a task you cannot complete by recognising a
template, and a set of questions you cannot answer by pattern-matching on
keywords.

---

## The task

Implement a function that, in one pass and O(1) extra space, reports whether a
linked list is a palindrome — then explain why the same approach cannot be used
if the list must be left unmodified.

Work it on paper first. Then implement it, and then check it against the
problem-bank tests listed below.

```bash
cd Module_03_*/problems
python -m pytest tests -q
```

## Diagnostic questions

Answer these out loud, as if in an interview. If you need to look one up, that
is the module to revisit — not the whole phase.

1. Name the three pointers in an in-place reversal and the order the assignments must take.
2. Give the phrase in a problem statement that means 'monotonic stack', and explain why the nested while loop is still O(n).
3. State two questions a hash map cannot answer, and name the structure that answers each.
4. Explain why a counter dictionary's len() only tracks distinct elements if you delete on zero.

---

## Passing criteria

- [ ] Every problem in Modules 03–05 passes from `problems/`
- [ ] Every module starter in this phase still **fails** before you start it
      (`make integrity`)
- [ ] You have worked the debug lab for each module in this phase and written a
      diagnosis for every symptom **before** opening `ANSWERS.md`
- [ ] You can answer all 4 diagnostic questions without reference
- [ ] You can state the complexity of every solution you wrote, and check it
      against the stated constraint

## If you cannot pass it

Do not repeat the whole phase. The diagnostic questions map to specific
material:

- Question 1 → revisit the relevant module's README section and the `reverse_list` problem
- Question 2 → revisit the relevant module's README section and the `next_greater` problem
- Question 3 → revisit the relevant module's README section and the `longest_consecutive` problem
- Question 4 → revisit the relevant module's README section and the `longest_consecutive` problem

Re-derive the failed item from scratch a day later rather than re-reading it
now. Reading a solution teaches recognition; re-deriving it teaches recall.

---

[← Phase 1](PHASE_01_CHECKPOINT.md) · [Course README](../README.md) · [Pattern Guide](../PATTERN_RECOGNITION_GUIDE.md) · [Phase 3 →](PHASE_03_CHECKPOINT.md)
