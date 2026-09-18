"""Problem 01 — React Thought Action Parser

Topic: 01 Agent Cognitive Architectures and Loops
Target: Production-grade implementation

Parse model generation into Thought, Action name, Action Input string, or Final Answer.

Example:
    >>> text = "Thought: Need to search temperature\nAction: search_weather\nAction Input: Paris"
    >>> react_thought_action_parser(text)
    {'thought': 'Need to search temperature', 'action': 'search_weather', 'action_input': 'Paris', 'final_answer': None}

Hints:
    Hint 1: This is a line-oriented mini-format — classify each line on its
        own by the marker it starts with; you never need to look across
        line boundaries to find where one field ends and the next begins.
    Hint 2: Split the text into lines, strip each line, then check it
        against the marker prefixes ('Thought:', 'Action:', 'Action
        Input:', 'Final Answer:') with startswith, stripping the marker
        text off the front to get that field's value.
    Hint 3: "Action:" and "Action Input:" both start with the word
        "Action", so matching on the bare word would let one swallow the
        other — match the full prefix, colon included, so the two stay
        distinct.
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
