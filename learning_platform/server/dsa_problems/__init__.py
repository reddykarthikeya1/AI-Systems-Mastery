# -*- coding: utf-8 -*-
"""
Unified DSA LeetCode Problem Bank & Execution Interface.
Provides access to 100+ curated LeetCode problems covering all 17 DSA modules.
"""
from typing import Dict, List, Any, Optional
import copy

from .runner import run_dsa_solution as _execute_solution
from .mod01_to_03 import PROBLEMS_MOD01_03
from .mod04_to_06 import PROBLEMS_MOD04_06
from .mod07_to_09 import PROBLEMS_MOD07_09
from .mod10_to_12 import PROBLEMS_MOD10_12
from .mod13_to_15 import PROBLEMS_MOD13_15
from .mod16_to_17 import PROBLEMS_MOD16_17

ALL_PROBLEMS: List[Dict[str, Any]] = (
    PROBLEMS_MOD01_03 +
    PROBLEMS_MOD04_06 +
    PROBLEMS_MOD07_09 +
    PROBLEMS_MOD10_12 +
    PROBLEMS_MOD13_15 +
    PROBLEMS_MOD16_17
)

PROBLEMS_BY_ID: Dict[str, Dict[str, Any]] = {p["id"]: p for p in ALL_PROBLEMS}
PROBLEMS_BY_MOD_NUM: Dict[int, List[Dict[str, Any]]] = {}

for p in ALL_PROBLEMS:
    mod = p.get("module_num", 1)
    if mod not in PROBLEMS_BY_MOD_NUM:
        PROBLEMS_BY_MOD_NUM[mod] = []
    PROBLEMS_BY_MOD_NUM[mod].append(p)

def _sanitize_problem_for_client(p: Dict[str, Any]) -> Dict[str, Any]:
    """Return problem metadata and visible test cases, omitting hidden cases and solution."""
    return {
        "id": p["id"],
        "module_num": p.get("module_num", 1),
        "title": p["title"],
        "difficulty": p["difficulty"],
        "pattern": p.get("pattern", "Algorithmic"),
        "time_complexity": p.get("time_complexity", ""),
        "space_complexity": p.get("space_complexity", ""),
        "description": p["description"],
        "starter_code": p["starter_code"],
        "visible_testcases": p.get("visible_testcases", []),
        "hidden_testcase_count": len(p.get("hidden_testcases", [])),
        "is_design": p.get("is_design", False),
        "target_class": p.get("target_class", "Solution"),
    }

def get_dsa_problems(module: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve problems filtered by module (e.g. '1', 'Module_01', 'Module_01_Complexity...') or all."""
    if not module:
        return [_sanitize_problem_for_client(p) for p in ALL_PROBLEMS]
    
    # Extract numeric module index
    mod_num = None
    import re
    m = re.search(r"(\d+)", module)
    if m:
        try:
            mod_num = int(m.group(1))
        except ValueError:
            pass
            
    if mod_num is not None and mod_num in PROBLEMS_BY_MOD_NUM:
        return [_sanitize_problem_for_client(p) for p in PROBLEMS_BY_MOD_NUM[mod_num]]
    
    return [_sanitize_problem_for_client(p) for p in ALL_PROBLEMS]

def get_dsa_problem_by_id(prob_id: str) -> Optional[Dict[str, Any]]:
    """Get internal problem dict including testcases."""
    return PROBLEMS_BY_ID.get(prob_id)

def run_dsa_solution(prob_id: str, user_code: str, submit: bool = False) -> Dict[str, Any]:
    """Run user code against a given problem's testcases."""
    prob = get_dsa_problem_by_id(prob_id)
    if not prob:
        return {
            "status": "error",
            "error": f"Problem with ID '{prob_id}' not found.",
            "all_passed": False,
            "passed_cases": 0,
            "total_cases": 0,
            "duration_ms": 0.0,
            "results": []
        }
    return _execute_solution(prob, user_code, submit=submit)
