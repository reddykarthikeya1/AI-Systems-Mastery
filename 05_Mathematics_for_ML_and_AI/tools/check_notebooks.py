#!/usr/bin/env python3
"""Execute every module notebook and fail if any cell errors.

Why a dedicated gate
--------------------
"Does the notebook open?" is not a useful question. The notebooks this replaced
opened perfectly and contained cells like::

    print('Verifying architecture invariants under simulated load...')
    print('Status: 100% healthy, zero data corruption detected.')

which verified nothing, and::

    test_metric = 100
    assert test_metric == 100, 'Invariant check failed'

which asserted a tautology. They were green because they were empty. Every cell
now runs the module's real implementation — code lifted from that module's own
test suite — so execution is a genuine signal.

The single cell tagged ``DELIBERATELY BROKEN`` is excluded: it exists for the
learner to fix in place and is *supposed* to fail until they do.

Usage::

    python tools/check_notebooks.py
    python tools/check_notebooks.py --module 09
    python tools/check_notebooks.py --timeout 600
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BROKEN_MARKER = "DELIBERATELY BROKEN"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="only this module number, e.g. 09")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    try:
        import nbformat
        from nbclient import NotebookClient
    except ImportError:
        print("nbclient/nbformat not installed. Run: pip install -e '.[notebook]'")
        return 1

    notebooks = sorted(ROOT.glob("Module_*/*.ipynb"))
    if args.module:
        want = args.module.zfill(2)
        notebooks = [n for n in notebooks if n.parts[-2].split("_")[1] == want]
    if not notebooks:
        print("no notebooks matched")
        return 1

    failures: list[tuple[str, str]] = []
    broken_cells_found = 0

    for path in notebooks:
        module_name = path.parent.name
        nb = nbformat.read(path, as_version=4)
        total = len(nb.cells)
        nb.cells = [c for c in nb.cells if BROKEN_MARKER not in "".join(c.get("source", ""))]
        broken_cells_found += total - len(nb.cells)

        try:
            NotebookClient(
                nb,
                timeout=args.timeout,
                kernel_name="python3",
                resources={"metadata": {"path": str(path.parent)}},
                allow_errors=False,
            ).execute()
            print(f"  ok    {module_name[:52]:<52} {total} cells")
        except Exception as exc:
            lines = [ln for ln in str(exc).strip().splitlines() if ln.strip()]
            failures.append((module_name, lines[-1] if lines else "unknown error"))
            print(f"  FAIL  {module_name[:52]:<52} {total} cells")

    print()
    if failures:
        print(f"NOTEBOOK CHECK FAILED: {len(failures)} of {len(notebooks)} notebooks error")
        for module_name, err in failures:
            print(f"  {module_name}: {err[:150]}")
        return 1

    print(
        f"NOTEBOOK CHECK PASSED: {len(notebooks)} notebooks executed, "
        f"{broken_cells_found} fix-in-place cell(s) skipped by design"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
