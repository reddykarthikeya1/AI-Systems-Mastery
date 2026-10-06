"""
Automated Verification Script for DSA Core 75
PASS CHECK:
  1. Counts exactly 75 problem sections in 03-The-Core-75-Mastery-Walkthroughs.md
  2. Verifies all 8 required subheadings exist in every problem section
  3. Verifies every dry-run trace in the markdown matches runtime output
  4. Specifically checks Trapping Rain Water (Problem 12) dry-run matches code trace
  5. Runs practice/run_tests.py and verifies all 75 solutions pass asserts
"""
import os
import sys
import re
import subprocess

# Ensure repo root and scripts/ are on path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

from dsa_generator.problems_01_15 import get_problems_01_15
from dsa_generator.problems_16_30 import get_problems_16_30
from dsa_generator.problems_31_45 import get_problems_31_45
from dsa_generator.problems_46_60 import get_problems_46_60
from dsa_generator.problems_61_75 import get_problems_61_75

def main():
    print("==================================================")
    print("STARTING DSA CORE 75 AUTOMATED PASS CHECK")
    print("==================================================")

    md_path = os.path.join(REPO_ROOT, "05-DSA-Interview-Playbook", "03-The-Core-75-Mastery-Walkthroughs.md")
    if not os.path.exists(md_path):
        print(f"FAILED: {md_path} does not exist.")
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Count problem sections
    pattern = r"## Problem (\d+): (.+)"
    matches = list(re.finditer(pattern, content))
    print(f"[CHECK 1] Found {len(matches)} problem sections in markdown.")
    if len(matches) != 75:
        print(f"FAILED: Expected 75 problem sections, found {len(matches)}.")
        sys.exit(1)

    # 2. Check each section has required subheadings
    required_subheadings = [
        "### Problem Statement",
        "### Brute Force Approach & Complexity",
        "### Key Insight (\"Aha!\" Moment)",
        "### Optimal Python Solution",
        "### Edge-Case Asserts",
        "### Dry-Run Execution Trace",
        "### Complexity Analysis",
        "### Follow-Up Interview Variants"
    ]

    all_problems = []
    all_problems.extend(get_problems_01_15())
    all_problems.extend(get_problems_16_30())
    all_problems.extend(get_problems_31_45())
    all_problems.extend(get_problems_46_60())
    all_problems.extend(get_problems_61_75())
    prob_map = {p.id: p for p in all_problems}

    sections = re.split(r"(?=## Problem \d+: )", content)[1:] # Skip preamble
    assert len(sections) == 75, f"Expected 75 split sections, got {len(sections)}"

    print("[CHECK 2 & 3] Verifying subheadings and runtime dry-run trace parity...")
    for idx, sec in enumerate(sections, start=1):
        # Verify subheadings
        for heading in required_subheadings:
            if heading not in sec:
                print(f"FAILED: Problem {idx} is missing heading: '{heading}'")
                sys.exit(1)

        # Extract dry-run text block
        trace_match = re.search(r"### Dry-Run Execution Trace\s+```text\s+(.*?)\s+```", sec, re.DOTALL)
        if not trace_match:
            print(f"FAILED: Problem {idx} missing ```text ... ``` trace block.")
            sys.exit(1)
        
        md_trace = trace_match.group(1).strip()
        expected_trace = prob_map[idx].run_trace().strip()

        if md_trace != expected_trace:
            print(f"FAILED: Problem {idx} ({prob_map[idx].title}) dry-run trace does NOT match actual runtime output!")
            print(f"Markdown trace:\n{md_trace[:200]}...\nExpected trace:\n{expected_trace[:200]}...")
            sys.exit(1)

    print(" [PASS] All 75 problems contain all 8 subheadings and 100% trace parity!")

    # 4. Check Problem 12 (Trapping Rain Water) specifically
    p12_trace = prob_map[12].run_trace()
    if "L-step" in p12_trace or "Left" in p12_trace:
        print(" [PASS] Problem 12 (Trapping Rain Water) verified with exact matching two-pointer code trace!")
    else:
        print("FAILED: Problem 12 trace is invalid.")
        sys.exit(1)

    # 5. Run test runner
    print("[CHECK 5] Running 05-DSA-Interview-Playbook/practice/run_tests.py...")
    test_runner_path = os.path.join(REPO_ROOT, "05-DSA-Interview-Playbook", "practice", "run_tests.py")
    res = subprocess.run([sys.executable, test_runner_path], capture_output=True, text=True)
    if res.returncode != 0:
        print("FAILED: Test runner failed!")
        print(res.stdout)
        print(res.stderr)
        sys.exit(1)

    print(res.stdout.strip())
    print("\n==================================================")
    print("ALL DSA CORE 75 PASS CHECKS COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    main()
