"""Exercise runner for the Python Mastery track.

    python exercises/run.py --init          # create stub files chNN.py from the answer files (never overwrites yours)
    python exercises/run.py                 # run the hidden tests against your chNN.py files
    python exercises/run.py 06 12           # only those chapters
    python exercises/run.py --solutions     # run the tests against the reference solutions (maintainer check)
    python exercises/run.py --reset 06      # recreate the stub for chapter 06 (overwrites your work)

Each chapter has 2 coding exercises and 1 debugging exercise. The tests live in _answers/ together with the
reference solutions: attempt first, look afterwards.
"""
from __future__ import annotations

import ast
import importlib.util
import pathlib
import sys
import traceback
import unittest

HERE = pathlib.Path(__file__).resolve().parent
ANSWERS = HERE / "_answers"


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _stub_body(node: ast.AST) -> None:
    doc = ast.get_docstring(node)
    body: list[ast.stmt] = []
    if doc:
        body.append(ast.Expr(ast.Constant(doc)))
    body.append(ast.Raise(ast.Call(ast.Name("NotImplementedError", ast.Load()), [], []), None))
    node.body = body


def make_stub(answer_path: pathlib.Path) -> str:
    src = answer_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    mod = load(answer_path, "_ans_" + answer_path.stem)
    buggy: dict[str, str] = getattr(mod, "BUGGY", {})
    head, imports, defs = [], [], []
    doc = ast.get_docstring(tree)
    if doc:
        head.append(f'"""{doc}"""')
    imports = [ast.unparse(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    for n in tree.body:
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) or n.name.startswith(("_", "t_")):
            continue
        if n.name in buggy:
            defs.append(buggy[n.name].strip("\n"))
            continue
        if isinstance(n, ast.ClassDef):
            for m in n.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    _stub_body(m)
        else:
            _stub_body(n)
        defs.append(ast.unparse(n))
    return "\n\n".join(head + (["\n".join(imports)] if imports else []) + defs) + "\n"


def run_chapter(answer_path: pathlib.Path, target) -> tuple[int, int, int]:
    ans = load(answer_path, "_tests_" + answer_path.stem)
    passed = failed = skipped = 0
    for name in sorted(n for n in dir(ans) if n.startswith("t_")):
        fn = getattr(ans, name)
        label = name[2:]
        try:
            fn(target)
            passed += 1
            print(f"  PASS  {label}")
        except unittest.SkipTest as e:
            skipped += 1
            print(f"  SKIP  {label} ({e})")
        except NotImplementedError:
            failed += 1
            print(f"  TODO  {label} (still a stub)")
        except Exception as e:  # AssertionError or any crash in student code
            failed += 1
            tb = traceback.extract_tb(e.__traceback__)[-1]
            print(f"  FAIL  {label}: {type(e).__name__}: {str(e)[:120]} (line {tb.lineno})")
    return passed, failed, skipped


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    answers = sorted(ANSWERS.glob("ch*.py"))
    if args:
        answers = [a for a in answers if a.stem[2:4] in {x.zfill(2) for x in args}]
    if "--init" in flags or "--reset" in flags:
        for a in answers:
            out = HERE / a.name
            if out.exists() and "--reset" not in flags:
                continue
            out.write_text(make_stub(a), encoding="utf-8")
            print("wrote", out.name)
        return 0
    total = [0, 0, 0]
    sys.path.insert(0, str(HERE))
    for a in answers:
        print(a.stem)
        try:
            target = load(a, "_sol_" + a.stem) if "--solutions" in flags else None
        except ImportError as e:
            print(f"  SKIP  chapter ({e})")
            continue
        if target is None:
            student = HERE / a.name
            if not student.exists():
                print("  (no file yet: run --init)")
                continue
            try:
                target = load(student, "student_" + a.stem)
            except ImportError as e:
                print(f"  SKIP  chapter ({e})")
                continue
        r = run_chapter(a, target)
        total = [x + y for x, y in zip(total, r)]
    print(f"\nResults: {total[0]} passed, {total[1]} failed, {total[2]} skipped")
    return 1 if total[1] else 0


if __name__ == "__main__":
    sys.exit(main())
