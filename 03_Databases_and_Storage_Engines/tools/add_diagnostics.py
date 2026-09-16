#!/usr/bin/env python3
"""Append hand-authored diagnostic questions to each module's self-assessment in Databases course.

The existing quizzes test **recall** ("what is B+ tree order?").
Recall measures reading. A diagnostic question shows real code plus an observed
symptom and asks for cause, fix, and which test would have caught it - which
measures the skill the course actually claims to teach.

Content lives in `diagnostics_data_{a,b,c,d}.py`, hand-written per module. This
script only handles placement, formatting and idempotency.

Usage::

    python tools/add_diagnostics.py            # apply
    python tools/add_diagnostics.py --check    # report coverage only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add Databases/tools to path
TOOLS_DIR = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases\tools")
sys.path.insert(0, str(TOOLS_DIR))

from diagnostics_data_a import DIAGNOSTICS as BATCH_A  # noqa: E402
from diagnostics_data_b import DIAGNOSTICS as BATCH_B  # noqa: E402
from diagnostics_data_c import DIAGNOSTICS as BATCH_C  # noqa: E402
from diagnostics_data_d import DIAGNOSTICS as BATCH_D  # noqa: E402

ROOT = TOOLS_DIR.parent
QUIZ = "SELF_ASSESSMENT_AND_CHALLENGES.md"
HEADING = "## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause"

ALL: dict[str, list] = {**BATCH_A, **BATCH_B, **BATCH_C, **BATCH_D}


def detect_lang(code: str) -> str:
    s = code.lstrip()
    if s.startswith(("SELECT", "CREATE", "ALTER", "INSERT", "UPDATE", "DELETE", "WITH", "--", "EXPLAIN")):
        return "sql"
    if s.startswith(("MATCH", "//")):
        return "cypher"
    if s.startswith(("{", "[", "POST", "GET", "PUT")):
        return "json"
    if s.startswith(("redis-cli", "nodetool", "psql", "$", "sh.")):
        return "bash"
    if s.startswith(("#", "import ", "from ", "def ", "class ", "try:", "with ", "sds =")):
        return "python"
    return ""


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
        lang = detect_lang(code)
        fence = f"```{lang}" if lang else "```"
        lines += [
            f"### D{index}. {title}",
            "",
            fence,
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
        "Every answer above cites real storage engine behaviors, configuration directives, and production failure modes.",
        "Open your implementation files and verify the behavior — the fix is not hypothetical, it is in the code you have built.",
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
            print(f"  {module_dir.name}: no items in diagnostics data")
            skipped += 1
            continue

        if not args.check:
            quiz.write_text(text.rstrip() + "\n" + render(number, items), encoding="utf-8")
        added += 1

    verb = "would add" if args.check else "added"
    print(f"already present: {have} | {verb}: {added} | skipped: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
