#!/usr/bin/env python3
"""Rebuild every module notebook from that module's own problem-bank tests.

Why this exists
---------------
The course shipped with one notebook, of three cells and zero assertions. A
notebook that executes cleanly *because it does nothing* is the worst kind of
green result, and exactly the defect this course teaches learners to distrust.

Where the content comes from
----------------------------
Each module's ``problems/tests/test_mNN_problems.py`` is guaranteed-correct
usage of that module's problems: it calls the real functions with real arguments
and asserts real properties, and most of its cases cross-check against a brute
force. Lifting those bodies into cells produces notebooks that cannot drift from
the implementations, because if a signature changes the tests break first.

Cell plan (12 cells, all substantive)
-------------------------------------
  0  md    what you will discover in this module
  1  md    setup
  2  code  import and INTROSPECT the real solutions (not a hardcoded list)
  3  md    baseline header naming the property being shown
  4  code  first problem's test body - real assertions
  5  md    prediction prompt, hand-written per module
  6  code  second problem's test body
  7  md    measurement header
  8  code  third problem's test body, timed
  9  md    fix-in-place challenge
 10  code  DELIBERATELY BROKEN - one wrong expected value to correct
 11  md    takeaways and links

Usage::

    python tools/build_notebooks.py
    python tools/build_notebooks.py --module 07
    python tools/build_notebooks.py --check
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Hand-written per module. A real prediction question has to be about that
# module's actual mechanism, and no template can produce one.
PREDICTIONS: dict[int, str] = {
    1: "An algorithm is measured at 1000, 2000 and 4000 elements and the elapsed "
       "times are 1ms, 4ms and 16ms. Before running the next cell, write down the "
       "growth class — then write down what the ratio would be for a *linear* "
       "algorithm over the same three sizes. Which of those two numbers does a "
       "first-to-last comparison actually produce?",
    2: "You need every contiguous subarray summing to exactly k, and the array "
       "contains negative numbers. Predict whether a sliding window works. If you "
       "think it does, write down which direction you would shrink when the sum "
       "overshoots — and then ask what happens when a later negative brings it "
       "back.",
    3: "A list of 5,000 nodes is reversed. Predict whether a recursive solution "
       "returns an answer or raises. Then predict what a three-pointer loop "
       "returns if the `next` pointer is saved *after* the reassignment rather "
       "than before.",
    4: "`next_greater([2, 2, 2])` — predict the output. Now predict "
       "`next_greater([1, 1, 2])`. The difference between the two tells you "
       "whether the stack comparison should be `<` or `<=`.",
    5: "You insert 100,000 consecutive integers and ask for the longest "
       "consecutive run. Predict the number of set-membership tests performed "
       "with, and without, the 'only start from a run start' guard. One of those "
       "numbers is about 100,000 and the other is about 5,000,000,000.",
    6: "A tree has root 5, left child 1, right child 4, and node 4 has children 3 "
       "and 6. Predict whether it is a valid BST. Then predict what a check that "
       "only compares each node against its immediate children would say.",
    7: "You want the 3rd largest of a million numbers. Predict which heap you "
       "need and what its maximum size should be. Most people answer 'max-heap' "
       "and it is the wrong one — work out why before running the cell.",
    8: "A directed graph has edges 0→1, 0→2, 1→3, 2→3. Predict whether it "
       "contains a cycle. Then predict what a DFS that flags any already-visited "
       "node would report.",
    9: "A graph has edges 0→1 costing 4, 0→2 costing 1, and 2→1 costing -2. "
       "Predict the shortest distance from 0 to 1. Then predict what Dijkstra "
       "returns. Those two numbers differ, and nothing raises.",
    10: "For maximum subarray *sum* a single running best suffices. Predict "
        "whether the same is true for maximum subarray *product* on "
        "`[-2, 3, -4]`, and if not, write down what the second piece of state "
        "must be.",
    11: "0/1 knapsack with one item of weight 1 and value 10, and a capacity of "
        "3. Predict the answer. Then predict what a single-row implementation "
        "that iterates capacity upward returns instead.",
    12: "Four meetings: (1,10), (2,3), (4,5), (6,7). Predict how many "
        "non-overlapping meetings fit. Then predict what a greedy that sorts by "
        "START time selects first, and how many it ends up with.",
    13: "Predict how many subsets `subsets([1, 2, 3])` returns, and predict what "
        "each of them contains if the code records `path` instead of `path[:]`. "
        "The count is right in both cases.",
    14: "You union 100,000 elements into one chain and then query connectivity "
        "from the deep end 10,000 times. Predict the total work with path "
        "compression, and without it. The two answers differ by about five "
        "orders of magnitude.",
    15: "A Bloom filter holds 800 items in 8192 bits using 3 hashes. Predict the "
        "false-positive rate when membership requires ALL three bits, and when "
        "it requires ANY one. Then predict the false-*negative* rate in each "
        "case.",
    16: "Searching for 'aa' inside 'aaaa'. Write down how many matches you expect "
        "before running anything. Then decide which answer a search-and-replace "
        "tool should give, and which a security filter should give - they are not "
        "the same, and the difference is one line of code.",
    17: "Five workers, five jobs, and a greedy assignment that takes each pair if "
        "both ends are free. Predict whether greedy can ever be beaten when every "
        "worker is qualified for exactly two jobs. Then predict what happens to "
        "the *count* of assignments if the source capacity is set to 2 by mistake "
        "- does it go up, down, or stay the same?",
}

TAKEAWAYS: dict[int, list[str]] = {
    1: [
        "The constraint on n tells you the complexity you are allowed, and that tells you the "
        "technique.",
        "An exact integer answer needs integer arithmetic - `bit_length()`, not `math.log2`.",
        "A correct answer computed the wrong way is still a defect; assert the scale, not just "
        "the value."],
    2: ["Two pointers, sliding window and prefix sums look alike and are not interchangeable.",
        "A sliding window needs the window's validity to be monotone in its width.",
        "'Minimise the maximum' plus a large answer range means binary search on the answer."],
    3: ["Save the next pointer before overwriting it. That ordering is the whole technique.",
        "Fast and slow pointers must move at different speeds or the gap never closes.",
        "A dummy head removes the 'is it the head?' special case entirely."],
    4: ["'Next greater', 'previous smaller' and 'span' all mean monotonic stack.",
        "A while inside a for is still O(n) when each index is pushed once and popped at most "
        "once.",
        "A monotonic deque needs two evictions per step, answering two different questions."],
    5: ["A hash map answers 'have I seen this?' in O(1) and nothing about order or range.",
        "A canonical key must be equal exactly when two inputs are equivalent - no more, no less.",
        "Walking only from run starts is what turns an O(n^2) scan into O(n)."],
    6: ["A BST invariant is global; a parent/child comparison is local and accepts non-BSTs.",
        "Python recursion dies at ~1000 frames - use an explicit stack for deep trees.",
        "Returning the verdict through the height computes balance in one pass instead of n."],
    7: ["To keep the k largest, use a MIN-heap of size k. The root is what you evict.",
        "Two heaps give a streaming median, and the size invariant is the algorithm.",
        "A heap is the wrong tool when counting or bucketing gets you O(n)."],
    8: ["Unweighted shortest path means BFS. DFS's first arrival is not optimal.",
        "Directed cycle detection needs three states; two produce false positives on any diamond.",
        "Kahn's algorithm detects cycles for free - check the output length."],
    9: ["The edge weights choose the algorithm: BFS, Dijkstra, or Bellman-Ford.",
        "Dijkstra on a negative edge does not error. It returns a larger number, confidently.",
        "Bellman-Ford's extra round is what makes the answer meaningful rather than arbitrary."],
    10: ["State, transition, base case, order - in that order, on paper, before any code.",
         "When a transition can reverse the ordering, one extreme is not enough state.",
         "An 'impossible' sentinel must be a value the valid range can never take."],
    11: [
        "The 0/1 knapsack rolling row must iterate capacity downward. Upward is unbounded "
        "knapsack.",
         "A rolling array carries an ordering contract that nothing in the code enforces.",
         "Label the three neighbours before writing a 2D sequence recurrence."],
    12: ["Sort by start to merge. Sort by end to schedule. Getting it backwards is silent.",
         "If you cannot prove the greedy choice is safe, use DP - slower and always correct.",
         "A greedy scan's precondition is a check you owe the caller."],
    13: ["Record `path[:]`, not `path`. The list you are appending is about to be mutated.",
         "Every change on the way down needs its undo on the way back up - all of them.",
         "`i` versus `i + 1` in the recursive call is with- versus without-replacement."],
    14: ["A trie answers prefix questions a hash map cannot; union-find cannot delete an edge.",
         "Path compression and union by size are not tuning - they are the data structure.",
         "Any cached derived value owes an invalidation path."],
    15: [
        "A Bloom filter's guarantee is one-sided, and `any` destroys its usefulness without "
        "breaking it.",
         "An LRU needs a hash map for lookup and a linked list for ordering; neither alone works.",
         "A performance-shaped bug with no functional symptom is the hardest kind to find."],
    16: [
        "The prefix function is the whole of KMP; the rest is it applied elsewhere.",
        "A hash match is a candidate, not a match - verifying is what makes it correct.",
        "Aho-Corasick costs the same whether you search for 5 patterns or 5,000."],
    17: [
        "The residual edge is an accounting entry, not a road - it is what lets the algorithm "
        "change its mind.",
        "Max flow equals min cut exactly - a free correctness check on your own code.",
        "Almost every flow problem is a reduction; the work is building the graph."],
}


def module_dirs(only: str | None) -> list[Path]:
    found = sorted(p for p in ROOT.glob("Module_*") if p.is_dir())
    if only:
        want = only.zfill(2)
        found = [p for p in found if p.name.split("_")[1] == want]
    return found


def usable_tests(test_file: Path, limit: int = 3) -> list[tuple[str, str]]:
    """Return (test_name, dedented body) for the first `limit` usable tests.

    Bodies using ``pytest.raises`` are kept - the notebook imports pytest, so
    an expected-exception assertion reads perfectly well in a cell and is often
    the most interesting property in the file.
    """
    source = test_file.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    out: list[tuple[str, str]] = []

    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
            continue
        body_lines = lines[node.body[0].lineno - 1 : node.end_lineno]
        # Drop the docstring line if the body opens with one.
        if body_lines and body_lines[0].lstrip().startswith('"""'):
            body_lines = body_lines[1:]
        text = "\n".join(ln[4:] if ln.startswith("    ") else ln for ln in body_lines)
        if not text.strip():
            continue
        out.append((node.name, text.strip()))
        if len(out) == limit:
            break
    return out


# Imports the generated setup cell already emits in its own preamble.
TEMPLATE_IMPORTS = {"sys", "time", "pytest", "pathlib"}


def imports_from(test_file: Path, bodies: list[str]) -> str:
    """Only the imports the lifted bodies actually reference.

    Importing all of a module's problems when the notebook exercises three of
    them leaves unused imports, which ruff rightly flags. Intersecting the
    import list against the names the bodies use keeps the setup cell honest
    about what it needs.
    """
    source = test_file.read_text(encoding="utf-8")

    used: set[str] = set()
    for body in bodies:
        try:
            tree = ast.parse(body)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used.add(node.id)
            elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                used.add(node.value.id)

    keep: list[str] = []
    for ln in source.splitlines():
        # Plain `import random` / `import time`: keep it if a lifted body uses
        # the name. Dropping these is how a cell ends up raising NameError on
        # `random.seed(...)` while every import it does have looks fine.
        if ln.startswith("import "):
            module_name = ln[len("import "):].split(" as ")[0].strip()
            root = module_name.split(".")[0]
            # The setup cell's own preamble already imports these; re-emitting
            # one is a redefinition (F811), not a missing import.
            if root in used and root not in TEMPLATE_IMPORTS:
                keep.append(ln)
            continue
        if not ln.startswith("from ") or " import " not in ln:
            continue
        prefix, names = ln.split(" import ", 1)
        wanted = [n.strip() for n in names.split(",") if n.strip() in used]
        if wanted:
            keep.append(f"{prefix} import {', '.join(wanted)}")

    # Module-level constants the lifted bodies reference. Without these the
    # generated cell raises NameError: a test file is free to hoist a shared
    # fixture to module scope, and lifting only the function body loses it.
    fixtures: list[str] = []
    try:
        module = ast.parse(source)
    except SyntaxError:
        module = None
    if module is not None:
        for node in module.body:
            if not isinstance(node, ast.Assign):
                continue
            named = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if any(name in used for name in named):
                fixtures.append(ast.unparse(node))

    blocks = ["\n".join(keep)] if keep else []
    if fixtures:
        blocks.append("\n".join(fixtures))
    return "\n\n".join(blocks)


def md(text: str, cid: str) -> dict:
    return {"cell_type": "markdown", "id": cid, "metadata": {},
            "source": text.strip().splitlines(True)}


def code(text: str, cid: str) -> dict:
    return {"cell_type": "code", "id": cid, "execution_count": None,
            "metadata": {}, "outputs": [], "source": text.strip().splitlines(True)}


def build_notebook(mdir: Path) -> dict | None:
    num = int(mdir.name.split("_")[1])
    test_file = next((mdir / "problems" / "tests").glob("test_m*_problems.py"), None)
    if test_file is None:
        return None

    tests = usable_tests(test_file)
    if len(tests) < 3:
        return None
    imports = imports_from(test_file, [body for _, body in tests])
    title = mdir.name.split("_", 2)[2].replace("_", " ")
    # Only import pytest when a lifted body actually needs it.
    needs_pytest = any("pytest." in body for _, body in tests)
    pytest_line = (
        "import pytest   # some assertions check that an invalid input RAISES\n"
        if needs_pytest
        else ""
    )

    solutions = mdir / "problems" / "solutions"
    fn_names = sorted(
        p.stem for p in solutions.glob("p*.py")
    )

    cells = [
        md(f"""
# Module {num:02d} — {title}

## What you will discover

Every cell below runs this module's **real** problem-bank solutions and asserts
their behaviour. Nothing here prints a claim it has not computed.

The assertions are lifted directly from `problems/tests/`, so they cannot drift
from the implementations — if a signature changes, the tests break first.

**One cell near the end is deliberately broken.** Fixing it is the exercise.
""", f"md{num:02d}0"),
        md("""
## Setup

The solutions directory goes on `sys.path` relative to this notebook's own
location. Never hard-code an absolute path — `tools/check_links.py` fails the
build on them, because a path with a username in it works on exactly one
machine.
""", f"md{num:02d}1"),
        code(f"""
import sys
import time
from pathlib import Path

{pytest_line}sys.path.insert(0, str(Path.cwd() / "problems" / "solutions"))

{imports}

print("module {num:02d}: {title}")
print("problems available:", {len(fn_names)})
for name in {fn_names!r}:
    print(f"  {{name}}")
""", f"cd{num:02d}2"),
        md(f"""
## 1. Baseline — `{tests[0][0].replace('test_', '')}`

The first property, asserted rather than printed. Read the assertions before
running: each one names a specific input class, and most cross-check against an
independent brute force over the same data.
""", f"md{num:02d}3"),
        code(f"""
{tests[0][1]}

print("all assertions held")
""", f"cd{num:02d}4"),
        md(f"""
## 2. Predict before you run

{PREDICTIONS[num]}

Commit to an answer before executing the next cell. Predicting and being wrong
is what makes the correction stick; reading the output first does not.
""", f"md{num:02d}5"),
        code(f"""
{tests[1][1]}

print("all assertions held")
""", f"cd{num:02d}6"),
        md("""
## 3. Measurement

Claims about complexity are claims about wall-clock behaviour at scale, so they
have to be measured rather than asserted from the shape of the code.
""", f"md{num:02d}7"),
        code(f"""
started = time.perf_counter()

{tests[2][1]}

elapsed = (time.perf_counter() - started) * 1000
print(f"all assertions held in {{elapsed:.2f}} ms")
""", f"cd{num:02d}8"),
        md("""
## 4. Fix this cell

The values below are **wrong on purpose**. Run it, read the failure, work out
the right numbers from the cells above, and correct them in place.

Change only the expected values — not the code that computes them.
""", f"md{num:02d}9"),
        code("""
import os

# DELIBERATELY BROKEN - two expected values, both wrong. Fix in place.

expected_problem_count = 99      # how many problems does this module ship?
expected_solution_count = 99     # how many reference solutions are on disk?

problem_files = sorted(
    f for f in os.listdir(Path.cwd() / "problems") if f.startswith("p") and f.endswith(".py")
)
solution_files = sorted(
    f for f in os.listdir(Path.cwd() / "problems" / "solutions")
    if f.startswith("p") and f.endswith(".py")
)

assert expected_problem_count == len(problem_files), (
    f"expected {expected_problem_count} problems, found {len(problem_files)}"
)
assert expected_solution_count == len(solution_files), (
    f"expected {expected_solution_count} solutions, found {len(solution_files)}"
)
print("Both match. Every problem has exactly one reference solution.")
""", f"cd{num:02d}10"),
        md(f"""
## Takeaways

{chr(10).join(f'{i}. {t}' for i, t in enumerate(TAKEAWAYS[num], start=1))}

### Where to go next

- [`01_README.md`](01_README.md) — the concepts in depth
- [`problems/README.md`](problems/README.md) — all {len(fn_names)} problems, with hint ladders
- [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md) — planted defects that exit 0
- [Pattern Recognition Guide](../PATTERN_RECOGNITION_GUIDE.md) — attacking an unseen problem
""", f"md{num:02d}11"),
    ]

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="only this module number, e.g. 07")
    parser.add_argument("--check", action="store_true", help="report, write nothing")
    args = parser.parse_args()

    mods = module_dirs(args.module)
    written = skipped = 0

    for mdir in mods:
        nb = build_notebook(mdir)
        if nb is None:
            print(f"  SKIP  {mdir.name[:56]}  (not enough usable tests)")
            skipped += 1
            continue

        int(mdir.name.split("_")[1])
        slug = re.sub(r"[^a-z0-9]+", "_", mdir.name.split("_", 2)[2].lower()).strip("_")
        target = mdir / f"00_interactive_{slug}.ipynb"

        # Remove any earlier notebook so a rename does not leave two behind.
        for old in mdir.glob("*.ipynb"):
            if old != target and not args.check:
                old.unlink()

        if args.check:
            print(f"  would write {target.name}  ({len(nb['cells'])} cells)")
        else:
            target.write_text(json.dumps(nb, indent=1), encoding="utf-8")
            print(f"  {mdir.name[:52]:<52} {len(nb['cells'])} cells -> {target.name[:34]}")
        written += 1

    print(f"\n{written} notebooks, {skipped} skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
