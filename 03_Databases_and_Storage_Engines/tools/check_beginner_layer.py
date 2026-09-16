"""Verify the beginner layer of this course.

The playground pages make claims. This checks them rather than trusting them:

  1. Every module has both beginner files.
  2. Every `00_try_it_yourself.py` runs to completion and prints `All checks passed`.
     A page whose assertions do not hold is a page that is lying to a beginner.
  3. The markdown's python blocks, concatenated in order, ARE the script body.
     This is the "they cannot drift apart" claim, checked line by line.
  4. Every playground actually asserts something.
  5. Standard library only - a beginner must not need `pip install` or Docker.

    python tools/check_beginner_layer.py
"""
from __future__ import annotations

import ast
import pathlib
import re
import subprocess
import sys

COURSE = pathlib.Path(__file__).resolve().parent.parent
MD_NAME = "00_FOUNDATIONS_PLAYGROUND.md"
PY_NAME = "00_try_it_yourself.py"

STDLIB = set(sys.stdlib_module_names)

# The generated banner between sections, e.g. "# -------- 3. Reads search newest
# first". Matched precisely, because playground code contains ordinary comments
# and a bare `print()` of its own that must NOT be stripped.
BANNER = re.compile(r"^# -{4,} \d+\. ")
SIGN_OFF = ["print()", 'print("All checks passed.")']   # in file order


def code_lines(text: str) -> list[str]:
    """Non-blank lines, trailing whitespace removed.

    Blank lines are dropped before comparing: the generated script is padded to
    satisfy PEP 8 spacing that the markdown blocks do not carry. Every line of
    real code must still match, in order.
    """
    return [line.rstrip() for line in text.split("\n") if line.strip()]


def markdown_code(markdown: str) -> list[str]:
    blocks = re.findall(r"```python\n(.*?)```", markdown, re.DOTALL)
    return code_lines("\n".join(b.strip() for b in blocks))


def script_code(source: str) -> list[str]:
    lines = source.split("\n")
    start = next(i for i, line in enumerate(lines)
                 if line.startswith("from __future__")) + 1
    body = code_lines("\n".join(line for line in lines[start:]
                                if not BANNER.match(line)))
    # Remove the closing sign-off only where it belongs: at the very end.
    for expected in reversed(SIGN_OFF):
        if body and body[-1] == expected:
            body.pop()
    return body


def third_party_imports(tree: ast.AST) -> list[str]:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            names = [(node.module or "").split(".")[0]]
        else:
            continue
        found += [n for n in names if n and n not in STDLIB and n != "__future__"]
    return found


def main() -> int:
    modules = sorted(p for p in COURSE.glob("Module_*") if p.is_dir())
    if not modules:
        print(f"no modules found under {COURSE}")
        return 1

    failures: list[str] = []
    checked = 0

    for module in modules:
        md_path, py_path = module / MD_NAME, module / PY_NAME
        name = module.name

        if not md_path.exists() or not py_path.exists():
            failures.append(f"{name}: missing {MD_NAME} or {PY_NAME}")
            continue

        source = py_path.read_text(encoding="utf-8")
        markdown = md_path.read_text(encoding="utf-8")

        if script_code(source) != markdown_code(markdown):
            failures.append(f"{name}: {MD_NAME} and {PY_NAME} have drifted apart")

        tree = ast.parse(source)

        asserts = sum(isinstance(n, ast.Assert) for n in ast.walk(tree))
        if asserts < 3:
            failures.append(f"{name}: only {asserts} assertions - claims go unchecked")

        for module_name in third_party_imports(tree):
            failures.append(f"{name}: imports third-party '{module_name}'")

        result = subprocess.run([sys.executable, PY_NAME], cwd=module,
                                capture_output=True, text=True, timeout=300)
        if result.returncode != 0 or "All checks passed" not in result.stdout:
            tail = (result.stderr or result.stdout).strip().split("\n")[-1:]
            failures.append(f"{name}: playground failed -> {' '.join(tail)}")

        checked += 1

    print(f"beginner layer: {checked}/{len(modules)} modules checked")
    if failures:
        print(f"\n{len(failures)} FAILURE(S):")
        for line in failures:
            print(f"  - {line}")
        return 1
    print("  every playground runs, asserts, stays in sync with its page,")
    print("  and needs nothing but the standard library.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
