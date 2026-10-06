# Practice Lab: How to Use Everything

> The chapters teach; this section is where you check yourself. Nothing here needs a network or an API key. Run commands from the repository root (the folder that contains `README.md`).

## What is in the lab

| Area | What you get | Where in this portal |
| :--- | :--- | :--- |
| Python exercises | 23 chapters, each with 2 coding and 1 debugging exercise, 105 hidden tests, 3-level hints, written walkthroughs | Python Exercises pages |
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
