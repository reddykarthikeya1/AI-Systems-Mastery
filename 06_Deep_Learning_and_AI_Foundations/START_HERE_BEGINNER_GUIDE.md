# Start Here — AI Research Archive

> **Status: 🔴 Scaffold.** This course has structure but no lesson content yet.
> If you are looking for something to learn from today, this is not it — check
> back when the roadmap shows 🟢 markers.

---

## What this course assumes

<!-- Be specific and be honest. "Some programming experience" is not a
     prerequisite, it is a way of avoiding one. -->

- TODO
- TODO

## What this course does not assume

- TODO

## What this course will not teach you

<!-- A course that claims to cover everything is lying about at least one
     thing. Name the boundaries here. -->

- TODO

---

## Setup

```bash
cd "AI Research Archive"
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"

python -m pytest -q                 # currently: no tests yet
python tools/check_links.py         # must pass now and stay passing
```

## Your first hour

1. Read [ROADMAP_AI_RESEARCH.md](ROADMAP_AI_RESEARCH.md) end to end. Do not skip it — knowing the shape of the
   108 lessons ahead is what makes the first module make sense.
2. Open [Module 01 — Math Fundamentals](Module_01_Math_Fundamentals/README.md).
3. Start at [What Math You Actually Need, and What You Do Not](Module_01_Math_Fundamentals/lessons/01_What_Math_You_Actually_Need_and_What_You_Do_Not.md).

## How to actually work through a lesson

- **Predict before you run.** Every lesson asks you to commit to an answer
  before executing the code. Skipping this turns a lesson into a reading.
- **Type the code.** Do not copy it.
- **Read the common-mistake section even when your code works.** That section
  is the difference between a lesson and a reference page.
- **Do the debug lab.** Write a diagnosis for every symptom *before* opening
  `ANSWERS.md`. The diagnostic reasoning is the transferable skill.

## Pacing

See [STUDY_PLANS_AND_PACING_GUIDE.md](STUDY_PLANS_AND_PACING_GUIDE.md).

---

[Course README](README.md) · [Roadmap](ROADMAP_AI_RESEARCH.md)
