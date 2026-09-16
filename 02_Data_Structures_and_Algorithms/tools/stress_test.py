#!/usr/bin/env python3
"""Differential fuzzing: run YOUR solution and the reference on random inputs
until they disagree, then shrink the disagreement to the smallest case.

Why this exists
---------------
Passing the shipped tests means you handle the cases somebody thought of. Most
wrong answers on a judge are inputs nobody thought of: an empty list, all equal
values, a single element, a duplicate at the boundary. Generating thousands of
random cases and comparing against a known-correct implementation finds those
in seconds.

The second half matters as much as the first. A failing input of 40 random
integers tells you nothing; the same bug shrunk to `[2, 1]` tells you exactly
what you got wrong. This tool shrinks automatically.

Usage::

    python tools/stress_test.py --module 16 --problem 05
    python tools/stress_test.py --module 02 --problem 01 --trials 50000
    python tools/stress_test.py --module 17 --problem 03 --seed 7
    python tools/stress_test.py --module 16 --list

Exit status is 1 if a disagreement is found, so it can be used in a script.

What it compares
----------------
`problems/pNN_*.py`            <- your implementation
`problems/solutions/pNN_*.py`  <- the reference

An unimplemented stub raises `NotImplementedError`, which is reported as "not
implemented yet" rather than as a disagreement.
"""

from __future__ import annotations

import argparse
import importlib.util
import inspect
import random
import sys
import typing
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# input generation
# ---------------------------------------------------------------------------

def _gen_int(rng: random.Random, size: int) -> int:
    return rng.randint(-size, size)


def _gen_str(rng: random.Random, size: int) -> str:
    alphabet = rng.choice(["ab", "abc", "abcdef"])
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, size)))


def _gen_list_int(rng: random.Random, size: int) -> list[int]:
    span = max(1, size // 2)
    return [rng.randint(-span, span) for _ in range(rng.randint(0, size))]


def _gen_list_str(rng: random.Random, size: int) -> list[str]:
    return [_gen_str(rng, max(1, size // 3)) for _ in range(rng.randint(0, size // 2))]


def _gen_bool(rng: random.Random, size: int) -> bool:
    return rng.random() < 0.5


BY_ANNOTATION: dict[str, Callable[[random.Random, int], Any]] = {
    "int": _gen_int,
    "str": _gen_str,
    "bool": _gen_bool,
    "list[int]": _gen_list_int,
    "list[str]": _gen_list_str,
}


def annotation_name(annotation: Any) -> str:
    if annotation is inspect.Parameter.empty:
        return ""
    if isinstance(annotation, str):
        return annotation.replace(" ", "")
    origin = typing.get_origin(annotation)
    if origin is list:
        (inner,) = typing.get_args(annotation)
        return f"list[{annotation_name(inner)}]"
    return getattr(annotation, "__name__", str(annotation)).replace(" ", "")


# Problems whose arguments must satisfy a relationship no type annotation can
# express - a query index must be inside the array, a graph's edges must name
# real nodes. Keyed "module/problem".
CUSTOM: dict[str, Callable[[random.Random, int], tuple]] = {}


def custom(key: str) -> Callable:
    def register(fn: Callable[[random.Random, int], tuple]) -> Callable:
        CUSTOM[key] = fn
        return fn
    return register


# A shrunk input must still be a LEGAL input. Without this, shrinking happily
# reduces "3 workers, 3 jobs, edge (0,0)" to "0 workers, 0 jobs, edge (0,0)",
# where the two implementations disagree only because the input is nonsense.
# Reporting that as the bug sends you hunting for a defect that is not there.
VALID: dict[str, Callable[[tuple], bool]] = {}


def validator(key: str) -> Callable:
    def register(fn: Callable[[tuple], bool]) -> Callable:
        VALID[key] = fn
        return fn
    return register


def _graph_is_valid(case: tuple) -> bool:
    nodes, edges, source, sink = case
    if nodes < 2 or not (0 <= source < nodes) or not (0 <= sink < nodes):
        return False
    return all(0 <= edge[0] < nodes and 0 <= edge[1] < nodes for edge in edges)


def _bipartite_is_valid(case: tuple) -> bool:
    left, right, pairs = case
    if left < 1 or right < 1:
        return False
    return all(0 <= a < left and 0 <= b < right for a, b in pairs)


for _key in ("17/01", "17/02", "17/04", "17/05"):
    VALID[_key] = _graph_is_valid
VALID["17/03"] = _bipartite_is_valid
VALID["17/06"] = lambda case: (
    _bipartite_is_valid(case[:3]) and case[3] >= 1)


@custom("16/05")
def _gen_text_and_pattern(rng: random.Random, size: int) -> tuple:
    alphabet = rng.choice(["ab", "abc"])
    text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, size)))
    pattern = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 4)))
    return (text, pattern)


@custom("16/06")
def _gen_text_and_banned(rng: random.Random, size: int) -> tuple:
    alphabet = "abc"
    text = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, size)))
    banned = list({"".join(rng.choice(alphabet) for _ in range(rng.randint(1, 3)))
                   for _ in range(rng.randint(0, 4))})
    return (text, banned)


def _gen_graph(rng: random.Random, size: int, weighted: bool) -> tuple:
    nodes = rng.randint(2, max(3, size // 4))
    edges = []
    for a in range(nodes):
        for b in range(nodes):
            if a != b and rng.random() < 0.4:
                edges.append((a, b, rng.randint(1, 9)) if weighted else (a, b))
    return nodes, edges, 0, nodes - 1


@custom("17/01")
def _gen_flow(rng: random.Random, size: int) -> tuple:
    return _gen_graph(rng, size, weighted=True)


@custom("17/02")
def _gen_cut(rng: random.Random, size: int) -> tuple:
    return _gen_graph(rng, size, weighted=True)


@custom("17/04")
def _gen_edge_paths(rng: random.Random, size: int) -> tuple:
    return _gen_graph(rng, size, weighted=False)


@custom("17/05")
def _gen_vertex_paths(rng: random.Random, size: int) -> tuple:
    return _gen_graph(rng, size, weighted=False)


@custom("17/03")
def _gen_matching(rng: random.Random, size: int) -> tuple:
    left = rng.randint(1, max(2, size // 6))
    right = rng.randint(1, max(2, size // 6))
    pairs = [(a, b) for a in range(left) for b in range(right)
             if rng.random() < 0.5]
    return (left, right, pairs)


@custom("17/06")
def _gen_shifts(rng: random.Random, size: int) -> tuple:
    workers = rng.randint(1, max(2, size // 6))
    shifts = rng.randint(1, max(2, size // 6))
    pairs = [(w, s) for w in range(workers) for s in range(shifts)
             if rng.random() < 0.5]
    return (workers, shifts, pairs, rng.randint(1, 3))


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------

def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def find_problem(module_number: str, problem_number: str) -> tuple[Path, Path, str]:
    matches = sorted(ROOT.glob(f"Module_{module_number}_*"))
    if not matches:
        raise SystemExit(f"no module {module_number}")
    problems = matches[0] / "problems"
    stubs = sorted(problems.glob(f"p{problem_number}_*.py"))
    if not stubs:
        raise SystemExit(f"no problem p{problem_number} in {matches[0].name}")
    stub = stubs[0]
    reference = problems / "solutions" / stub.name
    if not reference.exists():
        raise SystemExit(f"no reference solution for {stub.name}")
    return stub, reference, stub.stem


def public_function(module) -> Callable:
    candidates = [
        value for name, value in vars(module).items()
        if inspect.isfunction(value)
        and not name.startswith("_")
        and value.__module__ == module.__name__
    ]
    if not candidates:
        raise SystemExit("no public function found in the problem file")
    return candidates[-1]


# ---------------------------------------------------------------------------
# running and shrinking
# ---------------------------------------------------------------------------

def call(fn: Callable, args: tuple) -> tuple[str, Any]:
    """Return ("ok", value) or ("raised", ExceptionClassName)."""
    try:
        return "ok", fn(*args)
    except NotImplementedError:
        raise
    except Exception as exc:
        return "raised", type(exc).__name__


def disagree(mine: Callable, reference: Callable, args: tuple) -> bool:
    return call(mine, args) != call(reference, args)


def shrink(mine: Callable, reference: Callable, args: tuple,
           is_valid: Callable[[tuple], bool]) -> tuple:
    """Reduce a failing input while it keeps failing.

    Greedy and deliberately simple: try dropping one element, halving a list,
    and moving integers toward zero. Repeat until nothing helps. That is enough
    to turn 40 random values into the two that actually matter.
    """
    current = list(args)
    improved = True
    while improved:
        improved = False
        for index, value in enumerate(current):
            for smaller in shrink_candidates(value):
                # Strict progress only. `abs(v)` for a positive v, or `v // 2`
                # for -1, yields the value back unchanged - and accepting that
                # as an improvement loops forever.
                if smaller == value:
                    continue
                attempt = list(current)
                attempt[index] = smaller
                if not is_valid(tuple(attempt)):
                    continue
                try:
                    if disagree(mine, reference, tuple(attempt)):
                        current = attempt
                        improved = True
                        break
                except NotImplementedError:
                    raise
                except Exception:
                    continue
    return tuple(current)


def shrink_candidates(value: Any):
    if isinstance(value, str):
        if len(value) > 1:
            yield value[:len(value) // 2]
            yield value[1:]
            yield value[:-1]
    elif isinstance(value, list):
        if len(value) > 1:
            yield value[:len(value) // 2]
            yield value[1:]
            yield value[:-1]
        for i in range(len(value)):
            yield value[:i] + value[i + 1:]
    elif isinstance(value, bool):
        return
    elif isinstance(value, int) and value not in (0, 1):
        yield 0
        yield value // 2
        yield abs(value)


def build_generator(key: str, fn: Callable) -> Callable[[random.Random, int], tuple]:
    if key in CUSTOM:
        return CUSTOM[key]
    signature = inspect.signature(fn)
    makers = []
    for parameter in signature.parameters.values():
        name = annotation_name(parameter.annotation)
        maker = BY_ANNOTATION.get(name)
        if maker is None:
            raise SystemExit(
                f"no generator for parameter {parameter.name!r} of type "
                f"{name or 'unannotated'}.\n"
                f"Add one to CUSTOM under the key {key!r} in tools/stress_test.py.")
        makers.append(maker)
    return lambda rng, size: tuple(make(rng, size) for make in makers)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--module", required=True, help="module number, e.g. 16")
    parser.add_argument("--problem", help="problem number, e.g. 05")
    parser.add_argument("--trials", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--size", type=int, default=12,
                        help="rough upper bound on generated input size")
    parser.add_argument("--list", action="store_true",
                        help="list the problems in this module and exit")
    args = parser.parse_args()

    module_number = args.module.zfill(2)

    if args.list:
        matches = sorted(ROOT.glob(f"Module_{module_number}_*"))
        if not matches:
            raise SystemExit(f"no module {module_number}")
        for stub in sorted((matches[0] / "problems").glob("p*.py")):
            print(" ", stub.stem)
        return 0

    if not args.problem:
        parser.error("--problem is required unless --list is given")

    stub_path, reference_path, stem = find_problem(module_number,
                                                   args.problem.zfill(2))
    mine_module = load(stub_path, f"stress_mine_{stem}")
    reference_module = load(reference_path, f"stress_ref_{stem}")
    mine = public_function(mine_module)
    reference = getattr(reference_module, mine.__name__)

    key = f"{module_number}/{args.problem.zfill(2)}"   # zero-padded, as CUSTOM is keyed
    generate = build_generator(key, reference)
    is_valid = VALID.get(key, lambda _case: True)

    seed = args.seed if args.seed is not None else random.randrange(1 << 30)
    rng = random.Random(seed)
    print(f"stress testing {stem}.{mine.__name__}  "
          f"(trials={args.trials:,}, seed={seed})")

    for trial in range(1, args.trials + 1):
        case = generate(rng, args.size)
        try:
            if disagree(mine, reference, case):
                minimal = shrink(mine, reference, case, is_valid)
                print(f"\n  DISAGREEMENT after {trial:,} trials")
                print(f"  shrunk input : {minimal!r}")
                print(f"  yours        : {call(mine, minimal)[1]!r}")
                print(f"  reference    : {call(reference, minimal)[1]!r}")
                print(f"\n  reproduce with --seed {seed}")
                return 1
        except NotImplementedError:
            print(f"  {stem} is not implemented yet - nothing to compare.")
            print("  Write your version in problems/ and run this again.")
            return 0

    print(f"  {args.trials:,} random cases, no disagreement.")
    print("  That is evidence, not proof - but it is the evidence that finds "
          "real bugs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
