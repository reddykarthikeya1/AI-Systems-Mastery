# -*- coding: utf-8 -*-
"""
DSA LeetCode Test Execution Engine.
Executes Python solutions against visible and hidden edge testcases
in an isolated sandbox with memory, timeout, and data structure conversion helpers.
"""
import sys
import time
import json
import inspect
import tempfile
import subprocess
from typing import Dict, List, Any, Optional

RUNNER_SANDBOX_TEMPLATE = r'''# -*- coding: utf-8 -*-
import sys
import time
import json
from collections import deque, defaultdict, Counter
import heapq
import bisect
import math
from typing import List, Dict, Tuple, Optional, Any, Set

# Data Structure Helpers
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def list_to_linkedlist(arr):
    if not arr:
        return None
    dummy = ListNode(0)
    curr = dummy
    for x in arr:
        curr.next = ListNode(x)
        curr = curr.next
    return dummy.next

def linkedlist_to_list(head):
    res = []
    curr = head
    visited = set()
    while curr and id(curr) not in visited:
        visited.add(id(curr))
        res.append(curr.val)
        curr = curr.next
    return res

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def list_to_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    q = deque([root])
    i = 1
    while q and i < len(arr):
        curr = q.popleft()
        if i < len(arr) and arr[i] is not None:
            curr.left = TreeNode(arr[i])
            q.append(curr.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            curr.right = TreeNode(arr[i])
            q.append(curr.right)
        i += 1
    return root

def tree_to_list(root):
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        curr = q.popleft()
        if curr:
            res.append(curr.val)
            q.append(curr.left)
            q.append(curr.right)
        else:
            res.append(None)
    while res and res[-1] is None:
        res.pop()
    return res

# ----------------- USER SOLUTION CODE -----------------
{USER_CODE}
# ------------------------------------------------------

testcases = json.loads({TESTCASES_JSON_RAW})
is_design_pattern = {IS_DESIGN}
target_class_name = {TARGET_CLASS_NAME}
is_unordered = {IS_UNORDERED}
has_custom_eval = {CUSTOM_EVAL}

results = []
all_passed = True
start_time = time.perf_counter()

# Resolve Target Callable
target_class = None
target_method = None
sol_instance = None

if is_design_pattern:
    target_class = globals().get(target_class_name)
    if not target_class:
        print(json.dumps({
            "status": "runtime_error",
            "error": f"Class '{target_class_name}' not defined in solution.",
            "all_passed": False,
            "passed_cases": 0,
            "total_cases": len(testcases)
        }))
        sys.exit(0)
else:
    sol_class = globals().get("Solution")
    if not sol_class:
        print(json.dumps({
            "status": "runtime_error",
            "error": "Class 'Solution' not found in your submission.",
            "all_passed": False,
            "passed_cases": 0,
            "total_cases": len(testcases)
        }))
        sys.exit(0)
    sol_instance = sol_class()
    methods = [m for m in dir(sol_instance) if not m.startswith("_") and callable(getattr(sol_instance, m))]
    if not methods:
        print(json.dumps({
            "status": "runtime_error",
            "error": "No public methods found in class 'Solution'.",
            "all_passed": False,
            "passed_cases": 0,
            "total_cases": len(testcases)
        }))
        sys.exit(0)
    target_method = getattr(sol_instance, methods[0])

def compare_results(actual, expected, unordered=False):
    if isinstance(actual, float) and isinstance(expected, (int, float)):
        return abs(actual - expected) < 1e-4
    if unordered:
        if isinstance(expected, list) and isinstance(actual, list):
            try:
                if expected and isinstance(expected[0], list):
                    s_exp = sorted([sorted(x) if isinstance(x, list) else x for x in expected])
                    s_act = sorted([sorted(x) if isinstance(x, list) else x for x in actual])
                    return s_exp == s_act
                else:
                    return sorted(expected) == sorted(actual)
            except Exception:
                pass
    return actual == expected

for idx, tc in enumerate(testcases):
    is_hidden = tc.get("hidden", False)
    inp = tc.get("input")
    expected = tc.get("expected")
    
    try:
        if is_design_pattern:
            cmds = inp.get("commands", [])
            args = inp.get("args", [])
            inst = None
            cmd_results = []
            for cmd, arg in zip(cmds, args):
                if cmd == target_class_name:
                    inst = target_class(*arg)
                    cmd_results.append(None)
                else:
                    fn = getattr(inst, cmd)
                    ret = fn(*arg)
                    cmd_results.append(ret)
            actual = cmd_results
        else:
            if isinstance(inp, dict):
                converted_inp = {}
                for k, v in inp.items():
                    if k in ("head", "list1", "list2") and isinstance(v, list):
                        converted_inp[k] = list_to_linkedlist(v)
                    elif k == "lists" and isinstance(v, list):
                        converted_inp[k] = [list_to_linkedlist(sub) if isinstance(sub, list) else sub for sub in v]
                    elif k in ("root", "root1", "root2") and isinstance(v, list):
                        converted_inp[k] = list_to_tree(v)
                    elif k == "first_bad":
                        fb = v
                        converted_inp["isBadVersion"] = lambda ver, target=fb: ver >= target
                    else:
                        converted_inp[k] = v
                actual = target_method(**converted_inp)
            else:
                actual = target_method(inp)
                
            if isinstance(actual, ListNode):
                actual = linkedlist_to_list(actual)
            elif actual is None and isinstance(expected, list) and isinstance(inp, dict) and any(k in ("head", "list1", "list2", "lists") for k in inp):
                actual = []
            elif isinstance(actual, TreeNode):
                actual = tree_to_list(actual)
            elif actual is None and isinstance(expected, list) and isinstance(inp, dict) and any(k in ("root", "root1", "root2") for k in inp):
                actual = []

        passed = compare_results(actual, expected, unordered=is_unordered)
        if not passed:
            all_passed = False

        results.append({
            "case_index": idx + 1,
            "is_hidden": is_hidden,
            "input": inp if not is_hidden else "[Hidden Edge Test Case]",
            "expected": expected if not is_hidden else "[Hidden]",
            "actual": actual if not is_hidden else ("Match" if passed else "Mismatch"),
            "passed": passed
        })
    except Exception as exc:
        all_passed = False
        results.append({
            "case_index": idx + 1,
            "is_hidden": is_hidden,
            "input": inp if not is_hidden else "[Hidden Edge Test Case]",
            "expected": expected if not is_hidden else "[Hidden]",
            "actual": f"{type(exc).__name__}: {str(exc)}",
            "passed": False
        })

duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
passed_count = sum(1 for r in results if r["passed"])

print("__DSA_RESULT_START__")
print(json.dumps({
    "status": "accepted" if all_passed else "wrong_answer",
    "all_passed": all_passed,
    "total_cases": len(results),
    "passed_cases": passed_count,
    "duration_ms": duration_ms,
    "results": results
}))
'''

def run_dsa_solution(prob: Dict[str, Any], user_code: str, submit: bool = False) -> Dict[str, Any]:
    """Run a user-submitted code against a DSA problem's testcases."""
    testcases = []
    for tc in prob.get("visible_testcases", []):
        tc_copy = dict(tc)
        tc_copy["hidden"] = False
        testcases.append(tc_copy)

    if submit:
        for tc in prob.get("hidden_testcases", []):
            tc_copy = dict(tc)
            tc_copy["hidden"] = True
            testcases.append(tc_copy)

    is_design = prob.get("is_design", False)
    target_class_name = prob.get("target_class", "Solution")
    is_unordered = prob.get("is_unordered", False)
    custom_eval = prob.get("custom_eval", False)

    script_content = RUNNER_SANDBOX_TEMPLATE.replace("{USER_CODE}", user_code)
    script_content = script_content.replace("{TESTCASES_JSON_RAW}", repr(json.dumps(testcases)))
    script_content = script_content.replace("{IS_DESIGN}", str(is_design))
    script_content = script_content.replace("{TARGET_CLASS_NAME}", repr(target_class_name))
    script_content = script_content.replace("{IS_UNORDERED}", str(is_unordered))
    script_content = script_content.replace("{CUSTOM_EVAL}", str(custom_eval))

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(script_content)
        temp_file = tf.name

    try:
        proc = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=4.0
        )
        if proc.returncode != 0:
            return {
                "status": "runtime_error",
                "error": proc.stderr or proc.stdout,
                "all_passed": False,
                "passed_cases": 0,
                "total_cases": len(testcases),
                "duration_ms": 0.0,
                "results": []
            }
        
        stdout = proc.stdout
        marker = "__DSA_RESULT_START__"
        if marker in stdout:
            result_str = stdout.split(marker)[-1].strip()
            data = json.loads(result_str)
            if data["all_passed"]:
                data["reference_solution"] = prob.get("reference_solution")
                data["explanation"] = prob.get("explanation")
            return data
        else:
            return {
                "status": "runtime_error",
                "error": stdout or "Execution finished without output.",
                "all_passed": False,
                "passed_cases": 0,
                "total_cases": len(testcases),
                "duration_ms": 0.0,
                "results": []
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "time_limit_exceeded",
            "error": "Time Limit Exceeded: Your solution exceeded the 4.0-second sandbox limit. Ensure your algorithm avoids infinite loops and matches the expected time complexity.",
            "all_passed": False,
            "passed_cases": 0,
            "total_cases": len(testcases),
            "duration_ms": 4000.0,
            "results": []
        }
    except Exception as exc:
        return {
            "status": "runtime_error",
            "error": f"{type(exc).__name__}: {str(exc)}",
            "all_passed": False,
            "passed_cases": 0,
            "total_cases": len(testcases),
            "duration_ms": 0.0,
            "results": []
        }
