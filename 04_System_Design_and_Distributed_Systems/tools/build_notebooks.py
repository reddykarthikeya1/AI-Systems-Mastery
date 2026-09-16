#!/usr/bin/env python3
"""Rebuild every module notebook so its cells execute the module's real code.

Why this exists
---------------
The previous notebooks were theatre. The template's "verification" cell was::

    print('Verifying architecture invariants under simulated load...')
    print('Status: 100% healthy, zero data corruption detected.')

It verified nothing. It printed a claim. And the "interactive challenge" cell
was::

    test_metric = 100
    assert test_metric == 100, 'Invariant check failed'

A tautology. Those notebooks executed cleanly *precisely because they did
nothing* - which is the worst possible reason for a green result, and exactly
the class of defect this course teaches learners to distrust.

Where the real code comes from
------------------------------
Each module's ``project_solution/test_*.py`` is guaranteed-correct usage of that
module's API: it instantiates the real classes with real arguments and asserts
real properties. Lifting those bodies into cells produces notebooks that cannot
drift from the implementation, because if the API changes the tests break first.

Cell plan (12 cells, all substantive)
-------------------------------------
  0  md    what you will discover
  1  md    setup
  2  code  import + INTROSPECT the real exports (not a hardcoded list)
  3  md    baseline header, naming the property being shown
  4  code  first test body - real instantiation, real assertions
  5  md    prediction prompt tied to the next cell's actual property
  6  code  second test body - confirms or corrects the prediction
  7  md    measurement header
  8  code  third test body, or a timed run of the primary operation
  9  md    fix-in-place challenge
 10  code  DELIBERATELY BROKEN - one wrong expected value to correct
 11  md    takeaways + links to the module's other files

Usage::

    python tools/build_notebooks.py            # rebuild all
    python tools/build_notebooks.py --module 09
    python tools/build_notebooks.py --check    # report, write nothing
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Per-module prediction questions. Hand-written: a real question must be about
# that module's actual mechanism, and no template can produce one.
# ---------------------------------------------------------------------------
PREDICTIONS: dict[str, str] = {
    "00": "You are asked to size a system for 10 million daily active users. Before running "
          "the next cell, write down your estimate for peak QPS. What multiplier over the "
          "daily average did you apply, and why is a flat 1x wrong?",
    "01": "A single server handles 1,000 QPS at 40% CPU. Predict the QPS at which latency "
          "starts climbing sharply - and note it is *not* 2,500. What does queueing theory "
          "say happens as utilisation approaches 1?",
    "02": "Predict which is larger: the byte overhead of 1,000 JSON-over-HTTP/1.1 requests, "
          "or 1,000 gRPC-over-HTTP/2 calls carrying the same fields. By roughly what factor?",
    "03": "A reverse proxy sits in front of 3 origins. If one origin starts returning 500s "
          "but keeps accepting TCP connections, will a naive TCP health probe notice? "
          "Write down yes or no before running.",
    "04": "Round-robin sends equal request *counts* to every backend. Predict what happens "
          "to p99 latency when one backend is 5x slower but still healthy.",
    "05": "The checkout flow needs a new payment provider. Predict how many existing files "
          "must change under the clean architecture below - and what that number would be "
          "if the provider were called directly from the domain layer.",
    "06": "Predict what happens when two subscribers to the same event both raise an "
          "exception. Does the third subscriber still receive the event?",
    "07": "An elevator is at floor 5 going up. Requests arrive for floor 2 and floor 8. "
          "Predict the service order under SCAN scheduling, then under naive FIFO.",
    "08": "Three people split an expense unevenly. Predict whether the sum of all pairwise "
          "balances is exactly zero, and what floating-point issue could break that.",
    "09": "Adding one node to a 3-node ring: predict what fraction of 1,000 keys get "
          "remapped. Compare your guess against 1/4 (naive modulo) and against 1/N.",
    "10": "Two Snowflake generators on the same machine, same millisecond. Predict whether "
          "they can emit the same ID, and which field prevents it.",
    "11": "50 concurrent requests arrive for a key that just expired. Predict how many "
          "reach the database. Write the number down before running the next cell.",
    "12": "A Bloom filter reports an item is present. Predict whether it might be absent, "
          "and whether the reverse (reports absent but is present) is also possible.",
    "13": "A consumer crashes after processing a message but before acknowledging it. "
          "Predict whether that message is lost, redelivered, or silently dropped.",
    "14": "Predict how many characters a base62 short code needs to address 100 billion "
          "URLs. Then predict the collision probability if codes were random rather than "
          "sequential.",
    "15": "A user is connected to server A. Their friend on server B sends a message. "
          "Predict what infrastructure is required for delivery, and why a plain in-memory "
          "socket map is insufficient.",
    "16": "Predict whether fan-out-on-write or fan-out-on-read is cheaper for a user with "
          "50 million followers - and whether the answer flips for a user with 12.",
    "17": "Predict how many geohash cells a 5 km radius search must query, and why a single "
          "cell lookup misses drivers that are 100 m away.",
    "18": "A 4K video is uploaded once and watched a million times. Predict where the "
          "dominant cost sits: ingestion, transcoding, storage, or egress.",
    "19": "Predict what happens to a crawler with no URL frontier deduplication when it "
          "encounters two pages that link to each other.",
    "20": "1,000 users race for 50 items. Predict how many succeed under a naive "
          "read-then-write, and how many under an atomic reservation.",
    "21": "An HNSW index returns 10 nearest neighbours. Predict whether they are guaranteed "
          "to be the true 10 nearest, and what knob trades recall for latency.",
    "22": "Predict the KV-cache memory for 100 concurrent sequences of 2,000 tokens each, "
          "and what fraction PagedAttention reclaims from internal fragmentation.",
    "23": "A saga's third step fails. Predict what the orchestrator must do about steps 1 "
          "and 2, and why a database rollback is unavailable to it.",
    "24": "A 5-node Raft cluster partitions 3-2. Predict which side can still commit "
          "entries, and what the minority side does with incoming writes.",
    "25": "A request touches 6 services and one is slow. Predict what a trace shows that "
          "6 separate service dashboards cannot.",
    "26": "A payment is authorised but the capture call times out. Predict whether the "
          "customer was charged, and what mechanism lets you find out safely.",
}

TAKEAWAYS: dict[str, list[str]] = {
    "00": ["Capacity estimates are decisions, not trivia - state your assumptions out loud.",
           "Peak is a multiple of average; the multiplier is the interesting number.",
           "An interview answer with no numbers in it is not an answer."],
    "01": ["Latency does not degrade linearly - it degrades at a knee, near saturation.",
           "Little's Law connects concurrency, throughput and latency; memorise it.",
           "Vertical scaling has a ceiling you can compute in advance."],
    "02": ["Protocol choice is a latency and bandwidth decision, not a style preference.",
           "Binary framing plus multiplexing removes head-of-line blocking at the HTTP layer.",
           "REST for public APIs, gRPC for internal service-to-service - and know why."],
    "03": ["A health probe that only checks TCP tells you the process is alive, not correct.",
           "The edge is where you terminate TLS, cache, rate-limit and shed load.",
           "Every hop you add is a hop that can fail independently."],
    "04": ["Equal request counts do not mean equal load - least-connections beats round-robin "
           "under heterogeneous latency.",
           "Passive health checks react faster than active ones but need traffic to work.",
           "Sticky sessions trade balance for locality; know which you are buying."],
    "05": ["Dependencies point inward. The domain layer knows nothing about HTTP or SQL.",
           "An interface at the boundary is what makes a provider swap a one-file change.",
           "SOLID is a means to changeability, not a checklist to satisfy."],
    "06": ["Patterns are names for shapes you already needed - not a menu to shop from.",
           "One subscriber's failure must not deny the event to the others.",
           "The right pattern makes the next change small; the wrong one makes it large."],
    "07": ["State machines make illegal transitions impossible rather than merely unlikely.",
           "SCAN beats FIFO on total travel because it exploits direction locality.",
           "Model the states first; the scheduling policy then has somewhere to live."],
    "08": ["Money is not a float. Use integer minor units or Decimal, always.",
           "Balances must sum to zero - assert it, because a rounding drift is silent.",
           "Simplifying debts is a graph problem, not an accounting one."],
    "09": ["Consistent hashing remaps ~1/N of keys on a node change, not ~all of them.",
           "Virtual nodes exist to fix variance, not to fix correctness.",
           "A preference list must contain distinct *physical* nodes to survive a failure."],
    "10": ["Coordination-free unique IDs need time, machine identity, and a sequence field.",
           "Clock skew is the failure mode; a monotonic guard is not optional.",
           "Sortable IDs give you index locality for free - a real database benefit."],
    "11": ["Single-flight turns N concurrent misses into one load. Measure it, do not assume it.",
           "Probabilistic early expiry removes the synchronised expiry cliff entirely.",
           "Negative caching is what stops a nonexistent key from becoming a DDoS."],
    "12": ["Bloom filters trade a bounded false-positive rate for enormous space savings.",
           "False negatives are impossible - that asymmetry is what makes them useful.",
           "Sizing is a formula, not a guess: pick m and k from n and your target error rate."],
    "13": ["At-least-once plus idempotent consumers is the achievable guarantee.",
           "A commit log is a replayable ordered fact stream, not a work queue.",
           "Consumer groups partition work; offsets are what make crash recovery possible."],
    "14": ["Key length is a capacity calculation: log_62(address space).",
           "Sequential-plus-encode avoids collision handling that random codes require.",
           "The read:write ratio decides your entire caching strategy."],
    "15": ["Presence is soft state with a TTL, not a database row.",
           "Cross-server delivery needs a shared bus - an in-memory map cannot span nodes.",
           "Fan-out on a shared channel is where the cost actually lands."],
    "16": ["Fan-out on write is cheap to read and expensive for celebrities.",
           "Hybrid fan-out exists because neither pure strategy survives the tail.",
           "Two-tower retrieval separates candidate generation from ranking for a reason."],
    "17": ["Geospatial indexing turns a 2-D range query into a 1-D prefix scan.",
           "Cell boundaries mean neighbour cells must be queried too - always.",
           "Dispatch is a matching problem under a moving supply distribution."],
    "18": ["Egress dominates cost at scale, which is why CDNs exist.",
           "Transcode once into a ladder; serve the rung the client can actually play.",
           "Chunked delivery plus adaptive bitrate is what makes seeking feel instant."],
    "19": ["A frontier without dedup revisits forever - politeness and dedup are the same concern.",
           "Content hashing catches near-duplicates that URL comparison misses.",
           "robots.txt and per-host rate limits are correctness requirements, not etiquette."],
    "20": ["Read-then-write under contention oversells. Atomicity is the whole fix.",
           "A reservation with a TTL converts a race into a queue.",
           "Assert the conservation invariant: sold + reserved + available never changes."],
    "21": ["ANN indexes trade recall for latency - and recall must be measured, not assumed.",
           "HNSW's layered graph is what turns a linear scan into a logarithmic walk.",
           "Filtered vector search is a different problem from pure similarity search."],
    "22": ["KV cache, not model weights, is what limits concurrent sequences.",
           "Paged allocation reclaims the internal fragmentation that naive caching wastes.",
           "Continuous batching keeps the GPU busy across requests of different lengths."],
    "23": ["A saga has no rollback - it has compensating actions you must write.",
           "The outbox pattern makes 'update DB and publish event' a single local transaction.",
           "Two-phase commit is unavailable across heterogeneous stores; stop reaching for it."],
    "24": ["Consensus needs a majority; a minority partition must refuse writes.",
           "Raft's terms and log matching are what make leader election safe.",
           "Vector clocks detect concurrent updates; they do not resolve them for you."],
    "25": ["A trace shows causality and latency attribution that per-service dashboards cannot.",
           "Context propagation is the whole mechanism - break it and you have unrelated spans.",
           "SLOs and error budgets turn reliability into a number you can spend."],
    "26": ["Idempotency keys are what make a timed-out payment safe to retry.",
           "Authorise and capture are separate steps for a reason - model both.",
           "A fraud score is an input to a decision, never the decision itself."],
}


# ---------------------------------------------------------------------------
# Test-body extraction
# ---------------------------------------------------------------------------


def module_number(module_dir: Path) -> str:
    return module_dir.name.split("_")[1]


def solution_module(module_dir: Path) -> str | None:
    sols = [
        f
        for f in (module_dir / "project_solution").glob("*.py")
        if not f.name.startswith("test_") and f.name != "__init__.py"
    ]
    return sols[0].stem if sols else None


def _fixture_defs(tree, lines):
    """name -> (source with the @fixture decorator stripped, is_async)."""
    out = {}
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        is_fixture = any(
            (isinstance(d, ast.Attribute) and d.attr == "fixture")
            or (
                isinstance(d, ast.Call)
                and isinstance(d.func, ast.Attribute)
                and d.func.attr == "fixture"
            )
            for d in node.decorator_list
        )
        if not is_fixture:
            continue
        src = chr(10).join(lines[node.lineno - 1 : node.end_lineno])
        out[node.name] = (textwrap.dedent(src).rstrip(), isinstance(node, ast.AsyncFunctionDef))
    return out


def usable_tests(module_dir: Path):
    """Return (import lines, [(test_name, runnable notebook source)]).

    Three test shapes a naive lift cannot handle, and how each is resolved:

    * **fixture parameters** - the fixture function is emitted with its
      ``@pytest.fixture`` decorator stripped, aliased, and called, so the cell
      builds the very object the test would have received.
    * **async tests** - ipykernel permits top-level ``await``, so an async body
      is emitted verbatim and an async fixture is awaited.
    * **``pytest.raises`` / ``pytest.approx``** - both work perfectly well
      outside a test session, so the notebook simply imports pytest.
    """
    tests = sorted((module_dir / "project_solution").glob("test_*.py"))
    if not tests:
        return [], []

    imports = []
    bodies = []

    for test_file in tests:
        text = test_file.read_text(encoding="utf-8")
        lines = text.splitlines()
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                seg = chr(10).join(lines[node.lineno - 1 : node.end_lineno])
                if "__future__" not in seg:
                    imports.append(textwrap.dedent(seg))

        fixtures = _fixture_defs(tree, lines)

        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not node.name.startswith("test_"):
                continue

            params = [a.arg for a in node.args.args] + [a.arg for a in node.args.kwonlyargs]
            if any(p not in fixtures for p in params):
                continue

            first = node.body[0]
            start_line = first.lineno - 1
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                if len(node.body) == 1:
                    continue
                start_line = node.body[1].lineno - 1
            body = textwrap.dedent(chr(10).join(lines[start_line : node.end_lineno])).rstrip()

            preamble = []
            for name in params:
                fsrc, fasync = fixtures[name]
                preamble.append(fsrc)
                preamble.append("_make_" + name + " = " + name)
                call = "await _make_" + name + "()" if fasync else "_make_" + name + "()"
                preamble.append(name + " = " + call)

            sep = chr(10) + chr(10)
            source = (sep.join(preamble) + sep + body) if preamble else body
            bodies.append((node.name, source))

    seen = set()
    uniq = [i for i in imports if not (i in seen or seen.add(i))]
    if not any("import pytest" in i for i in uniq):
        uniq.append("import pytest")
    return uniq, bodies


def humanise(test_name: str) -> str:
    return test_name.removeprefix("test_").replace("_", " ").strip().capitalize()


# ---------------------------------------------------------------------------
# Notebook assembly
# ---------------------------------------------------------------------------


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def build(module_dir: Path) -> dict | None:
    num = module_number(module_dir)
    topic = module_dir.name.split("_", 2)[2].replace("_", " ")
    sol = solution_module(module_dir)
    if sol is None:
        return None

    imports, bodies = usable_tests(module_dir)
    if len(bodies) < 2:
        return None

    prediction = PREDICTIONS.get(num, "Predict the outcome of the next cell before running it.")
    takeaways = TAKEAWAYS.get(num, ["Measure, do not assume."])
    import_block = "\n".join(imports)

    cells: list[dict] = []

    # 0 -----------------------------------------------------------------
    cells.append(md(f"""# Module {num}: {topic} — Interactive Laboratory

Every cell below runs the module's **real** implementation from
`project_solution/{sol}.py`. Nothing here prints a claim it has not verified.

What you will do:

1. Load the engine and inspect what it actually exports.
2. Run its primary workflow and check the assertions that define correctness.
3. **Commit to a prediction**, then run the cell that tests it.
4. Measure a property rather than asserting one.
5. Fix a deliberately broken cell in place.

> The code in cells 4, 6 and 8 is lifted from this module's own test suite, so it
> cannot drift from the implementation. If the API changes, those tests fail
> first and this notebook is regenerated from them.
"""))

    # 1 -----------------------------------------------------------------
    cells.append(md("""## 1. Load the engine and introspect it

Rather than trusting a hardcoded list of class names, ask the module what it
actually contains.
"""))

    # 2 -----------------------------------------------------------------
    cells.append(code(f"""import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path('.').resolve() / 'project_solution'))
import {sol}

classes = [n for n, o in inspect.getmembers({sol}, inspect.isclass)
           if o.__module__ == '{sol}']
functions = [n for n, o in inspect.getmembers({sol}, inspect.isfunction)
             if o.__module__ == '{sol}']

print(f'module   : {sol}')
print(f'classes  : {{classes}}')
print(f'functions: {{functions}}')
print()
for name in classes:
    obj = getattr({sol}, name)
    try:
        sig = inspect.signature(obj.__init__)
        params = [p for p in sig.parameters if p != 'self']
    except (TypeError, ValueError):
        params = ['<builtin>']
    print(f'  {{name}}({{", ".join(params)}})')"""))

    # 3, 4 --------------------------------------------------------------
    name0, body0 = bodies[0]
    cells.append(md(f"""## 2. Baseline: {humanise(name0)}

This is the module's own `{name0}` — real instantiation, real calls, real
assertions. If it runs clean, the property it encodes holds.
"""))
    cells.append(code(
        f"{import_block}\n\n{body0}\n\nprint('PASSED: {name0}')" if import_block
        else f"{body0}\n\nprint('PASSED: {name0}')"
    ))

    # 5, 6 --------------------------------------------------------------
    name1, body1 = bodies[1]
    cells.append(md(f"""## 3. 🔮 Prediction — commit before you run

{prediction}

Write your answer down. An uncommitted guess teaches nothing, because you will
retro-fit it to whatever the next cell prints.

The next cell runs `{name1}`, which tests exactly this property.
"""))
    cells.append(code(f"{body1}\n\nprint('PASSED: {name1}')"))

    # 7, 8 --------------------------------------------------------------
    if len(bodies) >= 3:
        name2, body2 = bodies[2]
        cells.append(md(f"""## 4. Measure it: {humanise(name2)}

An assertion tells you a property holds. A measurement tells you *how much*.
This cell runs `{name2}` and times it.
"""))
        cells.append(code(f"""import time

_t0 = time.perf_counter()

{body2}

_elapsed = (time.perf_counter() - _t0) * 1000
print(f'PASSED: {name2}')
print(f'wall clock: {{_elapsed:.2f}} ms')"""))
    else:
        cells.append(md("""## 4. Measure it

An assertion tells you a property holds. A measurement tells you *how much*.
"""))
        cells.append(code(f"""import time

_t0 = time.perf_counter()
{body0.splitlines()[0]}
_elapsed = (time.perf_counter() - _t0) * 1000
print(f'construction cost: {{_elapsed:.3f}} ms')
print(f'exports measured : {{len([n for n in dir({sol}) if not n.startswith("_")])}}')"""))

    # 9, 10 -------------------------------------------------------------
    cells.append(md("""## 5. 🛠️ Fix this cell — it is deliberately broken

The cell below asserts something **false** about the real object. Read the
failure, work out the true value from the module's actual behaviour, and correct
the expected number.

Do not delete the assertion. The point is to make it pass by knowing the answer.
"""))
    cells.append(code(f"""# DELIBERATELY BROKEN - fix the expected value below.
# Hint: print the real value first, then decide what the assertion should say.

exports = [n for n in dir({sol}) if not n.startswith('_')]
print(f'actual export count: {{len(exports)}}')
print(f'actual exports     : {{exports}}')

EXPECTED_EXPORT_COUNT = 999      # <-- wrong on purpose. Replace it.

assert len(exports) == EXPECTED_EXPORT_COUNT, (
    f'expected {{EXPECTED_EXPORT_COUNT}} exports, found {{len(exports)}}. '
    'Read the printed value above and correct the constant.'
)
print('Fixed - assertion now reflects reality.')"""))

    # 11 ----------------------------------------------------------------
    numbered = "\n".join(f"{i}. {t}" for i, t in enumerate(takeaways, 1))
    cells.append(md(f"""### 🎓 Key takeaways

{numbered}

---

**Continue with this module:**

- [README.md](README.md) — the mental model and failure modes
- [PROJECT_GUIDE.md](PROJECT_GUIDE.md) — build it yourself, in 3 tiers
- [starter/](starter/) — your stubs; run the tests from there to grade yourself
- [debug_lab/SYMPTOMS.md](debug_lab/SYMPTOMS.md) — diagnose planted bugs from the symptom
- [TROUBLESHOOTING_AND_EDGE_CASES.md](TROUBLESHOOTING_AND_EDGE_CASES.md) — real errors, real causes
- [SELF_ASSESSMENT_AND_CHALLENGES.md](SELF_ASSESSMENT_AND_CHALLENGES.md) — quiz and diagnostics
"""))

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.9"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    mods = sorted(p for p in ROOT.glob("Module_*") if p.is_dir())
    if args.module:
        mods = [m for m in mods if module_number(m) == args.module.zfill(2)]

    built = skipped = 0
    for module_dir in mods:
        nb = build(module_dir)
        if nb is None:
            print(f"  SKIP  {module_dir.name} (fewer than 2 fixture-free tests)")
            skipped += 1
            continue
        target = next(module_dir.glob("*.ipynb"), None)
        if target is None:
            target = module_dir / f"00_interactive_{solution_module(module_dir)}.ipynb"
        if not args.check:
            target.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  {'would build' if args.check else 'built'}  {module_dir.name[:44]:<44} "
              f"{len(nb['cells'])} cells -> {target.name}")
        built += 1

    print(f"\n{built} notebooks {'planned' if args.check else 'written'}, {skipped} skipped")
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
