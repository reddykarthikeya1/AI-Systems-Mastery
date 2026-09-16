#!/usr/bin/env python3
"""Generate learner `starter/` scaffolds from each module's reference solution.

Why generate rather than hand-write every stub? Because the starter must match
the reference solution's API *exactly* - every signature, every class name -
or the shipped test suite cannot grade the learner's work. Deriving the skeleton
from the solution's own AST guarantees that invariant and keeps it true when the
solution changes.

What is preserved verbatim (the learner needs these):
  * module docstring (rewritten to a task brief), imports, __future__
  * module-level constants and type aliases
  * class declarations, base classes, decorators
  * every function/method signature, including type annotations and defaults
  * every docstring - the docstring IS the specification

What is replaced:
  * every function/method BODY -> `raise NotImplementedError(...)` plus a hint

Usage::

    python tools/make_starters.py                # all modules
    python tools/make_starters.py --module 07    # one module
    python tools/make_starters.py --dry-run
"""

from __future__ import annotations

import argparse
import ast
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Modules whose starter is hand-written and must never be overwritten.
HAND_WRITTEN = {"Module_22_CPython_Internals_Rust_PyO3_Extensions"}

SOLUTION_DIRS = ("project_solution", "capstone_platform", "modern_project_template")


@dataclass
class Stub:
    text: str
    n_functions: int
    n_classes: int


def _segment(lines: list[str], node: ast.AST) -> str:
    """Source text for a node, using its own line range."""
    start = node.lineno - 1
    end = getattr(node, "end_lineno", node.lineno)
    return "\n".join(lines[start:end])


def _decorators(lines: list[str], node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> list[str]:
    out = []
    for dec in node.decorator_list:
        raw = _segment(lines, dec).strip()
        out.append("@" + raw.lstrip("@").strip())
    return out


def _signature(lines: list[str], node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Reconstruct the `def ...:` line(s) verbatim from source.

    Taken from source rather than unparsed from the AST so that formatting,
    comments in defaults, and multi-line signatures survive intact.
    """
    body_start = node.body[0].lineno - 1
    if body_start == node.lineno - 1:
        line = lines[node.lineno - 1]
        col = getattr(node.body[0], "col_offset", -1)
        if col != -1:
            line = line[:col]
        idx = line.rfind(":")
        text = line[: idx + 1] if idx != -1 else line
    else:
        sig_lines = lines[node.lineno - 1 : body_start]
        text = "\n".join(sig_lines).rstrip()
        idx = text.rfind(":")
        text = text[: idx + 1] if idx != -1 else text
    return textwrap.dedent(text)


def _is_ellipsis_body(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    body_without_doc = [
        b
        for b in node.body
        if not (
            isinstance(b, ast.Expr)
            and isinstance(b.value, ast.Constant)
            and isinstance(b.value.value, str)
        )
    ]
    if len(body_without_doc) == 1:
        child = body_without_doc[0]
        if (
            isinstance(child, ast.Expr)
            and isinstance(child.value, ast.Constant)
            and child.value.value is Ellipsis
        ):
            return True
    return False


def _docstring_block(node: ast.AST, indent: str) -> list[str]:
    doc = ast.get_docstring(node, clean=False)
    if doc is None:
        return []
    if "\n" in doc:
        body = "\n".join(
            (indent + line.rstrip()) if line.strip() else "" for line in doc.splitlines()
        )
        return [f'{indent}"""' + body.lstrip()[: 0] + doc.splitlines()[0].strip(), *[]] if False else [
            f'{indent}"""{doc.splitlines()[0].strip()}',
            *[(indent + line.strip()) if line.strip() else "" for line in doc.splitlines()[1:]],
            f'{indent}"""',
        ]
    return [f'{indent}"""{doc.strip()}"""']


def _hint_for(name: str, qualname: str) -> str:
    """A short, honest nudge based on the member's name."""
    low = name.lower()
    table = [
        (("__init__", "__post_init__"), "initialise all attributes the other methods rely on"),
        (("get", "read", "fetch", "find", "lookup"), "return the value, or sentinel/None when absent"),
        (("set", "put", "add", "insert", "write", "store"), "validate input first, then mutate; maintain invariants"),
        (("delete", "remove", "pop", "evict"), "return whether something was actually removed"),
        (("clear", "reset", "purge"), "restore object to initial state of fresh instance"),
        (("validate", "check", "verify", "ensure"), "raise a specific exception with actionable message"),
        (("parse", "load", "decode", "from_"), "normalise at the boundary so downstream is clean"),
        (("dump", "encode", "to_", "serialize", "serialise"), "lossless round-trip: to_x(from_x(v)) == v"),
        (("run", "execute", "process", "handle"), "keep happy path readable; handle errors at edges"),
        (("main",), "wire pieces together and print verifiable output"),
        (("test",), "arrange, act, assert - one behaviour per test"),
        (("close", "shutdown", "stop", "cleanup"), "must be safe to call multiple times"),
        (("connect", "open", "start"), "fail fast with clear error if unreachable"),
        (("retry", "backoff"), "cap the delay and bound the attempts"),
        (("hash", "digest", "checksum"), "mask to intended bit width; wrap explicitly"),
    ]
    for keys, hint in table:
        if any(low.startswith(k) or low == k.strip("_") for k in keys):
            return hint
    if low.startswith("_"):
        return "internal helper - the public methods above define what it must do"
    return "implement per the docstring above; the tests define the exact contract"


class StarterBuilder(ast.NodeVisitor):
    """Walks a solution module and emits the stubbed equivalent."""

    def __init__(self, source: str, module_label: str) -> None:
        self.lines = source.splitlines()
        self.tree = ast.parse(source)
        self.module_label = module_label
        self.out: list[str] = []
        self.n_functions = 0
        self.n_classes = 0

    # -- helpers -----------------------------------------------------------

    def _emit_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, indent: str, owner: str = ""
    ) -> None:
        self.n_functions += 1
        for dec in _decorators(self.lines, node):
            self.out.append(indent + dec)
        sig = _signature(self.lines, node)
        # Re-indent a signature lifted from a class body.
        for line in sig.splitlines():
            self.out.append(indent + line if line.strip() else "")
        doc = _docstring_block(node, indent + "    ")
        self.out.extend(doc)

        if _is_ellipsis_body(node):
            self.out.append(f"{indent}    ...")
            self.out.append("")
            return

        qual = f"{owner}.{node.name}" if owner else node.name
        self.out.append(f"{indent}    # TODO: {_hint_for(node.name, qual)}")
        self.out.append(
            f'{indent}    raise NotImplementedError("{self.module_label}: implement {qual}()")'
        )
        self.out.append("")

    def _emit_class(self, node: ast.ClassDef) -> None:
        self.n_classes += 1
        for dec in _decorators(self.lines, node):
            self.out.append(dec)
        header = _segment(self.lines, node).splitlines()[0]
        # A multi-line class header: take everything up to the opening colon.
        if not header.rstrip().endswith(":"):
            body_start = node.body[0].lineno - 1
            header = "\n".join(self.lines[node.lineno - 1 : body_start]).rstrip()
            header = header[: header.rfind(":") + 1]
        self.out.append(header)
        self.out.extend(_docstring_block(node, "    "))

        members = [
            child
            for child in node.body
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.AnnAssign, ast.Assign))
        ]
        if not members:
            self.out.append("    pass")
            self.out.append("")
            return

        for child in node.body:
            if isinstance(child, (ast.AnnAssign, ast.Assign)):
                # Dataclass fields and class constants are part of the spec.
                raw_lines = textwrap.dedent(_segment(self.lines, child).strip()).splitlines()
                for raw_line in raw_lines:
                    self.out.append("    " + raw_line if raw_line.strip() else "")
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.out.append("")
                self._emit_function(child, "    ", owner=node.name)
        self.out.append("")

    # -- entry point -------------------------------------------------------

    def build(self, brief: str) -> Stub:
        self.out.append(brief.rstrip())
        self.out.append("")

        for node in self.tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                continue  # module docstring, replaced by the brief
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.AnnAssign, ast.Assign)):
                self.out.append(_segment(self.lines, node))
            elif isinstance(node, ast.ClassDef):
                self.out.append("")
                self._emit_class(node)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.out.append("")
                self._emit_function(node, "")
            elif isinstance(node, ast.If):
                # `if __name__ == "__main__":` - keep it, it is the run entry point.
                self.out.append("")
                self.out.append(_segment(self.lines, node))

        text = "\n".join(self.out).rstrip() + "\n"
        return Stub(text=text, n_functions=self.n_functions, n_classes=self.n_classes)


def brief_for(module_dir: Path, filename: str, original_doc: str | None) -> str:
    """The task brief that replaces the solution's module docstring."""
    number = module_dir.name.split("_")[1]
    topic = module_dir.name.split("_", 2)[2].replace("_", " ")
    first_line = (original_doc or "").strip().splitlines()[0].strip() if original_doc else ""
    return f'''"""STARTER - Module {number}: {topic}

{first_line or "Implement this module's project."}

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_{Path(filename).stem}.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/{filename} and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""'''


def generate_for_module(module_dir: Path, dry_run: bool = False) -> list[str]:
    """Generate starter files for one module. Returns a report."""
    report: list[str] = []
    if module_dir.name in HAND_WRITTEN:
        return [f"  {module_dir.name}: skipped (hand-written starter)"]

    solution_dir = next(
        (module_dir / name for name in SOLUTION_DIRS if (module_dir / name).is_dir()), None
    )
    if solution_dir is None:
        return [f"  {module_dir.name}: no solution directory - nothing to derive"]

    sources = [
        path
        for path in sorted(solution_dir.rglob("*.py"))
        if not path.name.startswith("test_")
        and "__pycache__" not in path.parts
        and path.name != "__init__.py"
    ]
    if not sources:
        return [f"  {module_dir.name}: no solution modules found"]

    starter_dir = module_dir / "starter"
    label = f"Module {module_dir.name.split('_')[1]}"

    for source_path in sources:
        text = source_path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            report.append(f"  {source_path.name}: SKIPPED (syntax error: {exc.msg})")
            continue

        builder = StarterBuilder(text, label)
        brief = brief_for(module_dir, source_path.name, ast.get_docstring(tree))
        stub = builder.build(brief)

        # Validate: a starter that does not parse is worse than no starter.
        try:
            ast.parse(stub.text)
        except SyntaxError as exc:
            report.append(f"  {source_path.name}: SKIPPED (generated stub invalid: {exc.msg})")
            continue

        rel = source_path.relative_to(solution_dir)
        target = starter_dir / rel
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(stub.text, encoding="utf-8")
        report.append(
            f"  {rel} -> starter/{rel}  ({stub.n_classes} classes, {stub.n_functions} stubs)"
        )

    # Copy any non-Python assets the learner needs (fixtures, compose files).
    if not dry_run and starter_dir.exists():
        for asset in solution_dir.rglob("*"):
            if asset.is_file() and asset.suffix in {".yml", ".yaml", ".json", ".html", ".toml"}:
                if "__pycache__" in asset.parts:
                    continue
                dest = starter_dir / asset.relative_to(solution_dir)
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(asset.read_bytes())

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="only this module number, e.g. 07")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    modules = sorted(p for p in ROOT.glob("Module_*") if p.is_dir())
    if args.module:
        modules = [m for m in modules if m.name.split("_")[1] == args.module.zfill(2)]
        if not modules:
            print(f"no module matching {args.module!r}", file=sys.stderr)
            return 1

    total = 0
    for module_dir in modules:
        print(f"{module_dir.name}")
        for line in generate_for_module(module_dir, dry_run=args.dry_run):
            print(line)
            total += "->" in line
    print(f"\n{'would generate' if args.dry_run else 'generated'} {total} starter file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
