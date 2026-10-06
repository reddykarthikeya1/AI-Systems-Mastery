from dataclasses import dataclass
from typing import Callable, List, Optional

@dataclass
class Problem:
    id: int
    slug: str
    title: str
    category: str
    difficulty: str
    statement: str
    brute_force: str
    key_insight: str
    func_name: str
    stub_code: str
    solution_code: str
    tests_code: str
    time_complexity: str
    space_complexity: str
    follow_up: str
    run_trace: Callable[[], str]
