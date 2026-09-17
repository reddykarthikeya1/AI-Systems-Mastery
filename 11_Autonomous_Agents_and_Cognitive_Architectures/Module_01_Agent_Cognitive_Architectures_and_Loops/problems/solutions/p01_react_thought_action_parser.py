"""Reference Solution — Problem 01: React Thought Action Parser

Topic: 01 Agent Cognitive Architectures and Loops
"""

from __future__ import annotations


def react_thought_action_parser(output_text: str) -> dict[str, str | None]:
    res = {'thought': None, 'action': None, 'action_input': None, 'final_answer': None}
    lines = output_text.strip().split('\n')
    for line in lines:
        line_s = line.strip()
        if line_s.startswith("Thought:"):
            res['thought'] = line_s.replace("Thought:", "").strip()
        elif line_s.startswith("Action:"):
            res['action'] = line_s.replace("Action:", "").strip()
        elif line_s.startswith("Action Input:"):
            res['action_input'] = line_s.replace("Action Input:", "").strip()
        elif line_s.startswith("Final Answer:"):
            res['final_answer'] = line_s.replace("Final Answer:", "").strip()
    return res
