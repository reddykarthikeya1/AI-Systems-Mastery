"""Problem 01 — React Thought Action Parser

Topic: 01 Agent Cognitive Architectures and Loops
Target: Production-grade implementation

Parse model generation into Thought, Action name, Action Input string, or Final Answer.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def react_thought_action_parser(output_text: str) -> dict[str, str | None]:
    """Parse output text:
    - 'thought': text following 'Thought:' up to 'Action:' or 'Final Answer:'
    - 'action': tool name following 'Action:'
    - 'action_input': parameters following 'Action Input:'
    - 'final_answer': text following 'Final Answer:'
    Returns dict with keys 'thought', 'action', 'action_input', 'final_answer'.
    """
    raise NotImplementedError("Implement react_thought_action_parser")
