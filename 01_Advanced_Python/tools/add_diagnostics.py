#!/usr/bin/env python3
"""Append hand-authored diagnostic questions to each module's self-assessment.

The existing quizzes test **recall** ("what is a dense vector embedding?").
Recall measures reading. A diagnostic question shows real code plus an observed
symptom and asks for cause, fix, and which test would have caught it - which
measures the skill the course actually claims to teach.

Content lives in `diagnostics_data_{a,b,c}.py`, hand-written per module. This
script only handles placement, formatting and idempotency.

Usage::

    python tools/add_diagnostics.py            # apply
    python tools/add_diagnostics.py --check    # report coverage only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from diagnostics_data_a import DIAGNOSTICS as BATCH_A
from diagnostics_data_b import DIAGNOSTICS as BATCH_B
from diagnostics_data_c import DIAGNOSTICS as BATCH_C
from diagnostics_data_d import DIAGNOSTICS as BATCH_D

ROOT = Path(__file__).resolve().parent.parent
QUIZ = "SELF_ASSESSMENT_AND_CHALLENGES.md"
HEADING = "## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause"

ALL: dict[str, list] = {**BATCH_A, **BATCH_B, **BATCH_C, **BATCH_D}


def render(number: str, items: list) -> str:
    lines = [
        "",
        "---",
        "",
        HEADING,
        "",
        "Recall questions measure reading. These measure diagnosis, which is the skill",
        "that separates intermediate from senior: given code and an observed symptom,",
        "find the cause, name the fix, and know which test would have caught it.",
        "",
        "Work each one **before** expanding the answer. Write your diagnosis down first —",
        "reading the answer with an un-committed guess teaches nothing.",
        "",
    ]

    for index, (title, code, symptom, questions, answer) in enumerate(items, start=1):
        lines += [
            f"### D{index}. {title}",
            "",
            "```python" if not code.lstrip().startswith(("FROM", "CMD", "HEALTHCHECK", "--", "$", "#!", "@app")) else "```",
            code.rstrip(),
            "```",
            "",
            f"**Observed symptom:** {symptom}",
            "",
        ]
        for letter, question in zip("abcdefg", questions, strict=False):
            lines.append(f"**({letter})** {question}")
            lines.append("")
        lines += [
            "<details>",
            "<summary><b>Show the diagnosis</b></summary>",
            "",
            answer,
            "",
            "</details>",
            "",
            "---",
            "",
        ]

    lines += [
        "### Scoring",
        "",
        "| Diagnosed correctly | Verdict |",
        "| :--- | :--- |",
        "| 5 of 5 | You can debug this module's material unaided. |",
        "| 3–4 | Solid. Re-read the ones you missed and the file they cite. |",
        "| 1–2 | Work the `debug_lab/` for this module before moving on. |",
        "| 0 | Re-read the README and re-run the demos; the material has not landed yet. |",
        "",
        "Every answer above cites a real file or test in this course. Open them —",
        "the fix is not hypothetical, it is in the code you already have.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    modules = sorted(p for p in ROOT.glob("Module_*") if p.is_dir())
    have = added = skipped = 0

    for module_dir in modules:
        number = module_dir.name.split("_")[1]
        quiz = module_dir / QUIZ
        if not quiz.exists():
            print(f"  {module_dir.name}: no {QUIZ}")
            skipped += 1
            continue

        text = quiz.read_text(encoding="utf-8")
        if HEADING in text:
            have += 1
            continue

        items = ALL.get(number)
        if not items:
            skipped += 1
            continue

        if not args.check:
            quiz.write_text(text.rstrip() + "\n" + render(number, items), encoding="utf-8")
        added += 1

    verb = "would add" if args.check else "added"
    print(f"already present: {have} | {verb}: {added} | no data (already diagnostic): {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
