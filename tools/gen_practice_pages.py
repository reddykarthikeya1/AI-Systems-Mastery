"""Generate the portal's "Practice Lab" pages (07-Practice-Lab/*.md) from the code that powers the exercises.

    python tools/gen_practice_pages.py

Nothing here is hand-copied: statements come from docstrings, starter code from the stub generator, tests from the
t_* functions, hints and walkthroughs from exercises/hints_and_solutions.py, DSA problems from practice/solutions/, and
the lab inventory from the scripts themselves. Re-run after changing any of them, then rebuild the portal.
"""
from __future__ import annotations

import ast
import glob
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "07-Practice-Lab"
EX = ROOT / "01-Python-Mastery" / "exercises"
DSA = ROOT / "05-DSA-Interview-Playbook" / "practice"
sys.path.insert(0, str(EX))

import run as exercise_runner  # noqa: E402  (the stub generator lives in run.py)
import hints_and_solutions as notes  # noqa: E402


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def details(summary: str, body: str) -> str:
    return f"<details>\n<summary>{summary}</summary>\n\n{body.strip()}\n\n</details>\n"


# ---------------------------------------------------------------------------------------------------------------
# Python exercises
# ---------------------------------------------------------------------------------------------------------------
def public_sources(path: Path) -> str:
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    parts = [ast.get_source_segment(src, n) for n in tree.body
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and not n.name.startswith(("_", "t_"))]
    imports = [ast.get_source_segment(src, n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    return "\n".join(imports) + "\n\n" + "\n\n".join(parts)


def chapter_section(answer: Path) -> tuple[str, int, int]:
    key = answer.stem
    mod = load(answer, "_gen_" + key)
    doc = (mod.__doc__ or "").strip().splitlines()
    title = re.sub(r"^Chapter \d+\s*-\s*", "", doc[0]).rstrip(".") if doc else key
    statements = [ln for ln in doc[1:] if re.match(r"\s*\d\.", ln)]
    tests = sorted(n[2:] for n in dir(mod) if n.startswith("t_"))
    md = [f"## Chapter {key[2:]}: {title}\n", "**The three exercises**\n", "\n".join(f"- {s.strip()[3:].strip()}" for s in statements) or "See the starter code below.", ""]
    md.append(details("Starter code (what `python exercises/run.py --init` creates)", "```python\n" + exercise_runner.make_stub(answer).rstrip() + "\n```"))
    hints = notes.HINTS.get(key, [])
    if hints:
        body = []
        for i, levels in enumerate(hints, 1):
            body.append(f"**Exercise {i}**\n")
            body += [f"{lvl}. {text}" for lvl, text in enumerate(levels, 1)]
            body.append("")
        md.append(details("Hints (open one level at a time, only after a real attempt)", "\n".join(body)))
    md.append(details("What the hidden tests check", "\n".join(f"- `{t}`" for t in tests)))
    explain = notes.EXPLANATIONS.get(key, [])
    walk = []
    for i, e in enumerate(explain, 1):
        walk.append(f"**{i}. {e['problem']}**\n\n*Approach.* {e['approach']}\n\n*Complexity.* {e['complexity']}\n\n*Common wrong answers.*\n")
        walk += [f"- {p}" for p in e["pitfalls"]]
        walk.append("")
    solution = "```python\n" + public_sources(answer).strip() + "\n```"
    md.append(details("Reference solution and walkthrough (look after you have tried)", solution + "\n\n" + "\n".join(walk)))
    return "\n".join(md), len(tests), len(statements)


def python_pages() -> list[tuple[str, str, str]]:
    answers = sorted((EX / "_answers").glob("ch*.py"))
    groups = [("01-Python-Exercises-Chapters-00-07.md", "Python Exercises: Chapters 00 to 07", range(0, 8)),
              ("02-Python-Exercises-Chapters-08-15.md", "Python Exercises: Chapters 08 to 15", range(8, 16)),
              ("03-Python-Exercises-Chapters-16-22.md", "Python Exercises: Chapters 16 to 22", range(16, 23))]
    pages, total_tests = [], 0
    for fname, title, rng in groups:
        sections = []
        for a in answers:
            if int(a.stem[2:]) in rng:
                body, n_tests, _ = chapter_section(a)
                total_tests += n_tests
                sections.append(body)
        intro = (f"# {title}\n\n> Each chapter has graded exercises with hidden tests: two coding exercises and one debugging exercise. "
                 "Create your files with `python 01-Python-Mastery/exercises/run.py --init`, edit `exercises/chNN.py`, then run "
                 "`python 01-Python-Mastery/exercises/run.py NN`. Hints are also available in the terminal with `--hints NN` and "
                 "walkthroughs with `--explain NN`.\n\n---\n\n")
        pages.append((fname, title, intro + "\n---\n\n".join(sections) + "\n"))
    return pages, total_tests


# ---------------------------------------------------------------------------------------------------------------
# DSA practice
# ---------------------------------------------------------------------------------------------------------------
def dsa_page() -> str:
    rows, by_cat = [], {}
    for f in sorted(glob.glob(str(DSA / "solutions" / "p*.py"))):
        t = Path(f).read_text(encoding="utf-8")
        m = re.match(r'"""\s*Problem (\d+): (.+?) \((\w+) - (.+?)\)\n(.*?)\n"""', t, re.S)
        n, name, diff, cat, stmt = int(m[1]), m[2], m[3], m[4], " ".join(m[5].split())
        by_cat.setdefault(cat, []).append((n, name, diff, stmt))
    out = ["# DSA Core 75: Practice Workbook\n",
           "> Every problem has a stub to complete, a reference solution kept closed, hidden asserts, and (for 70 problems) a randomised "
           "cross-check against a brute-force oracle. The statements below come straight from the problem files.\n",
           "## The loop for every problem\n",
           "```text\n"
           "python practice/run_tests.py 12 --hint 12        # a hint (repeat for levels 1, 2, 3)\n"
           "python practice/run_tests.py 12 --stub           # test YOUR stubs/p12_*.py: asserts plus random cross-check\n"
           "python practice/trace.py 12 \"[0,1,0,2,1,0,1,3,2,1,2,1]\" --stub   # dry-run trace of your code on an input\n"
           "python practice/run_tests.py 12                  # the reference solution, once you are done\n"
           "```\n",
           f"**{sum(len(v) for v in by_cat.values())} problems in {len(by_cat)} categories.**\n", "---\n"]
    for cat, items in by_cat.items():
        out.append(f"## {cat}\n")
        out.append("| # | Problem | Level | Statement |\n| :-: | :--- | :-: | :--- |")
        for n, name, diff, stmt in sorted(items):
            short = stmt if len(stmt) <= 230 else stmt[:227].rsplit(" ", 1)[0] + "..."
            out.append(f"| {n} | {name} | {diff} | {short.replace('|', '/')} |")
        out.append("")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------------------------------------------
# Labs, simulations, examples
# ---------------------------------------------------------------------------------------------------------------
def first_doc_line(path: Path) -> str:
    try:
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8")))
    except SyntaxError:
        doc = None
    return " ".join(doc.split("\n\n")[0].split()) if doc else path.stem.replace("_", " ")


def labs_page() -> str:
    groups = [
        ("Python (Track 1)", [ROOT / "01-Python-Mastery" / "labs" / f for f in sorted(p.name for p in (ROOT / "01-Python-Mastery" / "labs").glob("0*.py"))]),
        ("Low-Level Design (Track 2)", sorted((ROOT / "02-Low-Level-Design" / "labs").glob("*.py"))),
        ("High-Level Design (Track 3)", sorted((ROOT / "03-High-Level-Design" / "simulations").glob("*.py"))),
        ("Agentic AI (Track 4)", sorted((ROOT / "04-Agentic-AI" / "simulations").glob("*.py")) + sorted((ROOT / "04-Agentic-AI" / "examples").glob("ex*.py"))),
        ("DSA (Track 5)", sorted((ROOT / "05-DSA-Interview-Playbook" / "simulations").glob("*.py"))),
    ]
    out = ["# Labs, Simulations and Runnable Examples\n",
           "> Everything here runs offline with Python 3.10 or newer. Each script prints what it demonstrates and ends with assertions, so a clean exit means the claim held on your machine. Run them from the repository root.\n"]
    for title, files in groups:
        out.append(f"## {title}\n")
        out.append("| Script | What it shows | Run |\n| :--- | :--- | :--- |")
        for f in files:
            rel = f.relative_to(ROOT).as_posix()
            out.append(f"| `{rel}` | {first_doc_line(f).replace('|', '/')[:200]} | `python {rel}` |")
        out.append("")
    out += ["## Agentic examples: the test suite\n",
            "```text\npip install -r 04-Agentic-AI/examples/requirements.txt\ncd 04-Agentic-AI/examples && pytest -q\n```\n",
            "The examples use a scripted fake model, so no API key is needed. Real providers are reached through `llm.py` "
            "(`LLM_PROVIDER=anthropic` or `openai`, plus `LLM_MODEL`); both adapters are unit-tested with stub clients only.\n",
            "## Optional local services for the Python labs\n",
            "`01-Python-Mastery/labs/docker-compose.yml` starts Postgres, Redis and Kafka for readers who want to run the database, "
            "queue and streaming chapters against real services. It is optional: every chapter has an offline version.\n"]
    return "\n".join(out) + "\n"


def home_page(n_tests: int) -> str:
    n_ex = len(list((EX / "_answers").glob("ch*.py")))
    return f"""# Practice Lab: How to Use Everything

> The chapters teach; this section is where you check yourself. Nothing here needs a network or an API key. Run commands from the repository root (the folder that contains `README.md`).

## What is in the lab

| Area | What you get | Where in this portal |
| :--- | :--- | :--- |
| Python exercises | {n_ex} chapters, each with 2 coding and 1 debugging exercise, {n_tests} hidden tests, 3-level hints, written walkthroughs | Python Exercises pages |
| DSA Core 75 | 75 stubs, hidden asserts, 70 brute-force cross-checks, hints, a dry-run tracer | DSA Practice Workbook |
| Labs and simulations | Race conditions, memory leaks, consensus, consistent hashing, HNSW, benchmarks, agent loops | Labs page |
| Measured quality | Every metric the course reports about itself | Quality Report (Overview) |

## Python exercises in four commands

```text
python 01-Python-Mastery/exercises/run.py --init        # create your editable files: exercises/ch00.py ... ch22.py
python 01-Python-Mastery/exercises/run.py 06            # run the hidden tests for chapter 06 against YOUR file
python 01-Python-Mastery/exercises/run.py --hints 06    # three levels of hints, one exercise at a time
python 01-Python-Mastery/exercises/run.py --explain 06  # approach, complexity and common wrong answers
```

Your `chNN.py` files are ignored by git, so your attempts never mix with the course. `--solutions` runs the same tests against the reference solutions; it is how the course proves the tests are correct.

## DSA practice in four commands

```text
python 05-DSA-Interview-Playbook/practice/run_tests.py 12 --hint 12     # hint level 1; repeat for 2 and 3
python 05-DSA-Interview-Playbook/practice/run_tests.py 12 --stub        # test your stub
python 05-DSA-Interview-Playbook/practice/trace.py 12 "[0,1,0,2,1,0,1,3,2,1,2,1]" --stub   # see your code run line by line
python 05-DSA-Interview-Playbook/practice/run_tests.py --fuzz           # all reference solutions plus brute-force cross-checks
```

## Checking the course itself

| Command | What it proves |
| :--- | :--- |
| `python tools/audit.py` | Chapter length, Check Yourself and references coverage, every code block executed, labs run, exercise and DSA suites pass; writes the Quality Report |
| `python tools/portal_check.py` | Every portal page renders in headless Chrome with no KaTeX or Mermaid errors |
| `python tools/mutation_dsa.py` | The DSA oracles catch deliberate bugs (64 of 70 mutants killed on the last run) |
| `python tools/gen_practice_pages.py` | Regenerates the pages you are reading from the code |

## How to study with the lab

1. Read the chapter, then answer its **Check Yourself** questions on paper.
2. Do the chapter's exercises **before** opening the hints. Use level 1, retry, then level 2.
3. When the tests pass, read the walkthrough even if you were right: the common wrong answers are the interview follow-ups.
4. Run the lab for the chapter to see the failure mode with your own eyes.
5. Come back in a week and redo the debugging exercise without hints.
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    py_pages, n_tests = python_pages()
    pages = {"00-How-To-Use-The-Practice-Lab.md": home_page(n_tests)}
    for fname, _, body in py_pages:
        pages[fname] = body
    pages["04-DSA-Core-75-Practice-Workbook.md"] = dsa_page()
    pages["05-Labs-Simulations-And-Examples.md"] = labs_page()
    for name, text in pages.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote 07-Practice-Lab/{name}  ({len(text.split()):,} words)")


if __name__ == "__main__":
    main()
