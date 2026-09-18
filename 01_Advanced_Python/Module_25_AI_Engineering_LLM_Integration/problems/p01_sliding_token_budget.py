"""Problem 01 — LLM Context Window Token Truncator

Target: Production-grade implementation

Example:
    >>> msgs = ['Hello', 'How are you?', 'Tell me a story about algorithms!']
    >>> fit_prompt_budget('System', msgs, 10)
    ['System', 'Tell me a story about algorithms!']

Hints:
    Hint 1: The system message is non-negotiable — it always ships — so the
        real question is how much of the *remaining* budget the most recent
        user messages can fill before older ones get pushed out.
    Hint 2: Approximate token count as `len(text) // 4` (minimum 1), subtract
        the system message's cost from `max_tokens` up front, then walk
        `user_msgs` from newest to oldest, greedily keeping each one that
        still fits in the shrinking remaining budget.
    Hint 3: Stop at the first message (working backwards) that doesn't fit —
        don't skip it to try squeezing in an even older, shorter one — and
        rebuild the kept messages back into chronological order after the
        system message; if the system message alone exceeds `max_tokens`,
        return just `[system_msg]`.
"""

from __future__ import annotations


def fit_prompt_budget(system_msg: str, user_msgs: list[str], max_tokens: int) -> list[str]:
    raise NotImplementedError('Implement fit_prompt_budget')
