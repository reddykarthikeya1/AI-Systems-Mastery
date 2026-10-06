"""
Core 75 practice harness.

  python run_tests.py                 # run all 75 reference solutions (asserts)
  python run_tests.py 12              # one problem (number, or part of the name)
  python run_tests.py --fuzz          # solutions + randomized brute-force cross-checks (34 problems)

Practising (write your answer in stubs/pNN_*.py, leave solutions/ closed):
  python run_tests.py 12 --stub       # test YOUR stub: asserts + random cross-check
  python run_tests.py --hint 12       # hint level 1 (pattern); repeat with 2 and 3 for more
  python run_tests.py --hint 12 3     # hint level 3 (the key insight)
"""
import glob
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOL_DIR = os.path.join(HERE, "solutions")
STUB_DIR = os.path.join(HERE, "stubs")
CHAPTER = os.path.join(HERE, "..", "03-The-Core-75-Mastery-Walkthroughs.md")


def load(path, name="mod"):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def find(files, query):
    q = query.lower().strip()
    out = []
    for f in files:
        base = os.path.basename(f).lower()
        if q.isdigit():
            if base.startswith(f"p{int(q):02d}_"):
                out.append(f)
        elif q in base:
            out.append(f)
    return out


def run_solution(path):
    try:
        mod = load(path, "sol")
        if not hasattr(mod, "run_tests"):
            return False, "no run_tests() defined"
        mod.run_tests()
        return True, "PASSED"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def run_stub(sol_path, stub_path):
    """Run the reference tests against the learner's implementation."""
    try:
        sol = load(sol_path, "sol")
        stub = load(stub_path, "stub")
    except Exception as e:  # noqa: BLE001
        return False, f"could not import your stub: {type(e).__name__}: {e}"
    skip = {"ListNode", "TreeNode", "GraphNode", "to_list", "from_list"}
    replaced = 0
    for name, obj in vars(stub).items():
        if name.startswith("_") or name in skip or not callable(obj):
            continue
        if getattr(obj, "__module__", None) != "stub":
            continue
        if name in vars(sol):
            sol.__dict__[name] = obj
            replaced += 1
    try:
        sol.run_tests()
        return True, "PASSED reference asserts"
    except NotImplementedError:
        return False, "not implemented yet (the stub still raises NotImplementedError)"
    except AssertionError as e:
        return False, f"AssertionError: a reference test failed {e}"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def fuzz(n, source_dir):
    os.environ["DSA_SRC_DIR"] = source_dir
    os.environ["DSA_ONLY"] = str(n) if n else ""
    sys.path.insert(0, HERE)
    sys.modules.pop("fuzz_checks", None)
    import fuzz_checks
    return fuzz_checks.run(only=n)


def hint(n, level):
    text = open(CHAPTER, encoding="utf-8").read()
    secs = re.split(r"\n## Problem (\d+): ", text)[1:]
    for i in range(0, len(secs), 2):
        if int(secs[i]) == n:
            body = secs[i + 1]
            title = body.split("\n", 1)[0]
            def part(name):
                m = re.search(rf"### {name}[^\n]*\n(.*?)(?=\n### |\Z)", body, re.S)
                return m.group(1).strip() if m else ""
            cat = re.search(r"\((.*?)\)", title)
            print(f"Problem {n}: {title.split('(')[0].strip()}")
            if level == 1:
                print("Hint 1 (pattern):", cat.group(1) if cat else "see the chapter header")
                print("Next: python run_tests.py --hint", n, 2)
            elif level == 2:
                print("Hint 2 (the naive approach and why it is too slow):\n" + part("Brute Force"))
                print("Next: python run_tests.py --hint", n, 3)
            else:
                print("Hint 3 (key insight):\n" + part("Key Insight"))
                print("Still stuck? Read the full walkthrough in 03-The-Core-75-Mastery-Walkthroughs.md.")
            return
    print(f"No problem {n}")


def main():
    args = [a for a in sys.argv[1:]]
    if args and args[0] == "--hint":
        hint(int(args[1]), int(args[2]) if len(args) > 2 else 1)
        return
    stub_mode = "--stub" in args
    fuzz_mode = "--fuzz" in args or stub_mode
    args = [a for a in args if not a.startswith("--")]
    query = args[0] if args else None

    sols = sorted(glob.glob(os.path.join(SOL_DIR, "p*.py")))
    if query:
        sols = find(sols, query)
        if not sols:
            print(f"No problem matching '{query}' found.")
            sys.exit(1)
    if stub_mode and not query:
        print("--stub needs a problem: python run_tests.py 12 --stub")
        sys.exit(1)

    passed = failed = 0
    label = "your stubs" if stub_mode else "reference solutions"
    print(f"Core 75: {len(sols)} problem(s), {label}\n" + "=" * 60)
    for sol in sols:
        name = os.path.splitext(os.path.basename(sol))[0]
        if stub_mode:
            stub = os.path.join(STUB_DIR, os.path.basename(sol))
            ok, msg = run_stub(sol, stub)
        else:
            ok, msg = run_solution(sol)
        num = int(name[1:3])
        if ok and fuzz_mode:
            res = fuzz(num, STUB_DIR if stub_mode else SOL_DIR)
            if num in res:
                _, bad, ex = res[num]
                if bad:
                    ok, msg = False, f"random cross-check failed {bad} times, e.g. input={str(ex[0])[:80]} got={str(ex[1])[:60]} expected={str(ex[2])[:60]}"
                else:
                    msg += " + random cross-check OK"
        if ok:
            passed += 1
            print(f" [PASS] {name}  {msg if stub_mode or fuzz_mode else ''}".rstrip())
        else:
            failed += 1
            print(f" [FAIL] {name} -> {msg}")
            if stub_mode:
                print(f"        hint: python run_tests.py --hint {num}")
    print("=" * 60)
    print(f"Results: {passed} PASSED, {failed} FAILED out of {len(sols)} tests.")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
