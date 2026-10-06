import os
import sys

# Ensure current directory is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa_generator.problems_01_15 import get_problems_01_15
from dsa_generator.problems_16_30 import get_problems_16_30
from dsa_generator.problems_31_45 import get_problems_31_45
from dsa_generator.problems_46_60 import get_problems_46_60
from dsa_generator.problems_61_75 import get_problems_61_75
from dsa_generator.models import Problem

def main():
    problems: list[Problem] = []
    problems.extend(get_problems_01_15())
    problems.extend(get_problems_16_30())
    problems.extend(get_problems_31_45())
    problems.extend(get_problems_46_60())
    problems.extend(get_problems_61_75())

    print(f"Loaded {len(problems)} problems.")
    assert len(problems) == 75, f"Expected 75 problems, got {len(problems)}"

    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dsa_dir = os.path.join(repo_root, "05-DSA-Interview-Playbook")
    practice_dir = os.path.join(dsa_dir, "practice")
    solutions_dir = os.path.join(practice_dir, "solutions")
    stubs_dir = os.path.join(practice_dir, "stubs")
    os.makedirs(solutions_dir, exist_ok=True)
    os.makedirs(stubs_dir, exist_ok=True)

    traces = {}

    print("Verifying solutions, running asserts, and generating runtime traces...")
    for p in problems:
        # Test code execution
        test_env = {}
        # Pre-populate common classes if needed
        exec("""
from typing import Optional, List, Dict, Tuple, Set
import heapq
from collections import deque, defaultdict
import bisect

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
""", test_env)
        
        full_code = p.solution_code + "\n" + p.tests_code
        try:
            exec(full_code, test_env)
        except Exception as e:
            print(f"FAILED on Problem {p.id} ({p.title}): {e}")
            raise e

        # Generate trace
        trace_output = p.run_trace()
        traces[p.id] = trace_output

        # Write solution file
        sol_path = os.path.join(solutions_dir, f"{p.slug}.py")
        sol_content = f'''"""
Problem {p.id}: {p.title} ({p.difficulty} - {p.category})
{p.statement}
"""
from typing import List, Dict, Optional, Tuple, Set
import heapq
from collections import deque, defaultdict
import bisect

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

{p.solution_code}

def run_tests():
{chr(10).join("    " + line for line in p.tests_code.splitlines())}
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for {p.slug}!")
'''
        with open(sol_path, "w", encoding="utf-8") as f:
            f.write(sol_content)

        # Write stub file
        stub_path = os.path.join(stubs_dir, f"{p.slug}.py")
        stub_content = f'"""\nProblem {p.id}: {p.title} ({p.difficulty} - {p.category})\n{p.statement}\n"""\nfrom typing import List, Dict, Optional, Tuple, Set\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\nclass GraphNode:\n    def __init__(self, val=0, neighbors=None):\n        self.val = val\n        self.neighbors = neighbors if neighbors is not None else []\n\n{p.stub_code}\n'
        with open(stub_path, "w", encoding="utf-8") as f:
            f.write(stub_content)

    print(f"Successfully verified all 75 solutions and created stubs/solutions!")

    # Write practice/run_tests.py
    run_tests_py_path = os.path.join(practice_dir, "run_tests.py")
    runner_code = '''"""
Core 75 Automated Test Runner Harness
Usage:
  python run_tests.py            # Runs all 75 problems
  python run_tests.py <problem>  # Runs specific problem (e.g. '1', 'p01_two_sum', 'two_sum')
"""
import sys
import os
import glob
import importlib.util

def run_problem(sol_file):
    spec = importlib.util.spec_from_file_location("sol", sol_file)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        if hasattr(mod, "run_tests"):
            mod.run_tests()
        return True, "PASSED"
    except Exception as e:
        return False, str(e)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sol_dir = os.path.join(script_dir, "solutions")
    files = sorted(glob.glob(os.path.join(sol_dir, "p*.py")))

    if len(sys.argv) > 1:
        query = sys.argv[1].lower().strip()
        filtered = []
        for f in files:
            basename = os.path.basename(f).lower()
            # Match number like '1' or '01'
            if query.isdigit():
                prefix = f"p{int(query):02d}_"
                if basename.startswith(prefix):
                    filtered.append(f)
            elif query in basename:
                filtered.append(f)
        if not filtered:
            print(f"No problem matching '{query}' found.")
            sys.exit(1)
        files = filtered

    passed = 0
    failed = 0
    print(f"Running Core 75 Test Suite ({len(files)} problem(s))...\\n" + "=" * 60)
    for f in files:
        prob_name = os.path.splitext(os.path.basename(f))[0]
        ok, msg = run_problem(f)
        if ok:
            passed += 1
            print(f" [PASS] {prob_name}")
        else:
            failed += 1
            print(f" [FAIL] {prob_name} -> {msg}")
    print("=" * 60)
    print(f"Results: {passed} PASSED, {failed} FAILED out of {len(files)} tests.")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    with open(run_tests_py_path, "w", encoding="utf-8") as f:
        f.write(runner_code)

    # Build 05-DSA-Interview-Playbook/03-The-Core-75-Mastery-Walkthroughs.md
    md_path = os.path.join(dsa_dir, "03-The-Core-75-Mastery-Walkthroughs.md")
    md_lines = [
        "# DSA Playbook Chapter 3: The Complete Core 75 Mastery Walkthroughs",
        "",
        "> **Core Learning Objective:** Master every single archetype among the canonical **Core 75** coding interview questions. Every problem features the precise problem statement, brute force analysis, core algorithmic breakthrough, optimal typed Python solution, edge-case unit assertions, runtime-generated execution trace, Big-O complexity breakdown, and follow-up interviewer variants.",
        "",
        "---",
        "",
        "## Master Core 75 Architecture & Category Blueprint",
        "",
        "| # | Problem Name | Category | Difficulty | Primary Pattern | Time | Space |",
        "| :-: | :--- | :--- | :---: | :--- | :---: | :---: |"
    ]

    for p in problems:
        md_lines.append(f"| {p.id} | [{p.title}](#problem-{p.id}-{p.slug.replace('_', '-')}) | {p.category} | {p.difficulty} | {p.category} | {p.time_complexity.split()[0]} | {p.space_complexity.split()[0]} |")

    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

    for p in problems:
        md_lines.extend([
            f"## Problem {p.id}: {p.title} ({p.difficulty} - {p.category})",
            "",
            "### Problem Statement",
            p.statement,
            "",
            "### Brute Force Approach & Complexity",
            p.brute_force,
            "",
            "### Key Insight (\"Aha!\" Moment)",
            p.key_insight,
            "",
            "### Optimal Python Solution",
            "```python",
            p.solution_code.strip(),
            "```",
            "",
            "### Edge-Case Asserts",
            "```python",
            p.tests_code.strip(),
            "```",
            "",
            "### Dry-Run Execution Trace",
            "```text",
            traces[p.id].strip(),
            "```",
            "",
            "### Complexity Analysis",
            f"- **Time Complexity:** {p.time_complexity}",
            f"- **Space Complexity:** {p.space_complexity}",
            "",
            "### Follow-Up Interview Variants",
            p.follow_up,
            "",
            "---",
            ""
        ])

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Successfully generated markdown at {md_path} ({len(md_lines)} lines).")

if __name__ == "__main__":
    main()
