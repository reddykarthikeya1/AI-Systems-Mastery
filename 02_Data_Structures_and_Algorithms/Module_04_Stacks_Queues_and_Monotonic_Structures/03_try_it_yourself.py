"""Module 04: Interactive Stacks & Queues CLI Sandbox."""
from __future__ import annotations


def demo_valid_parentheses():
    print("\n=== DEMO: Valid Parentheses Validator ===")
    test_cases = ["()[]{}", "(]", "([{}])"]
    for s in test_cases:
        stack = []
        pairs = {')': '(', '}': '{', ']': '['}
        valid = True
        for char in s:
            if char in pairs:
                if not stack or stack[-1] != pairs[char]:
                    valid = False
                    break
                stack.pop()
            else:
                stack.append(char)
        if stack:
            valid = False
        print(f"Expression: {s:<10} -> Valid: {valid}")


if __name__ == "__main__":
    demo_valid_parentheses()
