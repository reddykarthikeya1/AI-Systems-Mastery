#!/usr/bin/env python3
"""Verify that every third-party import in the course is declared in pyproject.toml.

The course used to declare **zero** dependencies while importing fastapi,
sqlalchemy, polars, duckdb, bcrypt, jwt and more. `pip install -e .` produced a
working install of nothing, and the first `pytest` run failed on a fresh machine.

This script closes that gap permanently: it walks every ``.py`` file, collects
top-level imports, subtracts the standard library and the course's own modules,
and asserts the remainder is declared.

Usage::

    python tools/check_deps.py            # fail on an undeclared import
    python tools/check_deps.py --list     # just print what was found
"""

from __future__ import annotations

import argparse
import ast
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".hypothesis",
             "target", ".git", ".venv", "node_modules", "starter", "debug_lab"}

# Import name -> distribution name, where they differ.
IMPORT_TO_DIST = {
    "jwt": "pyjwt",
    "sklearn": "scikit-learn",
    "pyarrow": "pyarrow",
    "pytest_asyncio": "pytest-asyncio",
    "yaml": "pyyaml",
    "psycopg2": "psycopg2-binary",
    "cassandra": "cassandra-driver",
    "clickhouse_connect": "clickhouse-connect",
    "qdrant_client": "qdrant-client",
    "pymysql": "pymysql",
    "mysql": "mysql-connector-python",
    "pymysqlreplication": "mysql-replication",
    "bson": "pymongo",
}

# Compiled or locally-built modules that are intentionally not on PyPI.
LOCAL_MODULES: set[str] = set()


def course_module_names() -> set[str]:
    """Every module name defined inside the course itself."""
    names: set[str] = set()
    for path in ROOT.rglob("*.py"):
        if set(path.parts) & SKIP_DIRS:
            continue
        names.add(path.stem)
        names.add(path.parent.name)
    return names


def declared_distributions() -> set[str]:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]
    raw: list[str] = list(project.get("dependencies", []))
    for extra_deps in project.get("optional-dependencies", {}).values():
        raw.extend(extra_deps)

    out: set[str] = set()
    for spec in raw:
        # "uvicorn[standard]>=0.32" -> "uvicorn"
        name = spec.split(";")[0].strip()
        for sep in (">=", "<=", "==", "!=", "~=", ">", "<", "["):
            name = name.split(sep)[0]
        out.add(name.strip().lower().replace("_", "-"))
    return out


def collect_imports() -> dict[str, set[Path]]:
    """Top-level import name -> the files that import it."""
    found: dict[str, set[Path]] = {}
    for path in sorted(ROOT.rglob("*.py")):
        if set(path.parts) & SKIP_DIRS:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.setdefault(alias.name.split(".")[0], set()).add(path)
            # node.level == 0 excludes relative imports (`from .foo import x`),
            # which are intra-course and never third-party.
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                found.setdefault(node.module.split(".")[0], set()).add(path)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="print findings and exit 0")
    args = parser.parse_args()

    stdlib = set(sys.stdlib_module_names)
    own = course_module_names()
    declared = declared_distributions()
    imports = collect_imports()

    third_party: dict[str, set[Path]] = {
        name: files
        for name, files in imports.items()
        if name not in stdlib
        and name not in own
        and name not in LOCAL_MODULES
        and not name.startswith("_")
    }

    undeclared: dict[str, set[Path]] = {}
    for name, files in third_party.items():
        dist = IMPORT_TO_DIST.get(name, name).lower().replace("_", "-")
        if dist not in declared:
            undeclared[name] = files

    if args.list:
        print(f"declared distributions ({len(declared)}):")
        for dist in sorted(declared):
            print(f"  {dist}")
        print(f"\nthird-party imports found ({len(third_party)}):")
        for name in sorted(third_party):
            marker = " <-- UNDECLARED" if name in undeclared else ""
            print(f"  {name}{marker}")
        return 0

    if undeclared:
        print(f"DEPENDENCY CHECK FAILED: {len(undeclared)} undeclared import(s)\n")
        for name, files in sorted(undeclared.items()):
            dist = IMPORT_TO_DIST.get(name, name)
            print(f"  {name!r} (add {dist!r} to pyproject.toml)")
            for path in sorted(files)[:3]:
                print(f"      used in {path.relative_to(ROOT)}")
        return 1

    print(
        f"DEPENDENCY CHECK PASSED: {len(third_party)} third-party imports, "
        f"all declared in pyproject.toml"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
