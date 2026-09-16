"""Reference solution — Problem 07: Evaluate Reverse Polish Notation

Pattern:    Stack
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    operators = {"+", "-", "*", "/"}

    for tok in tokens:
        if tok in operators:
            if len(stack) < 2:
                raise ValueError(f"operator {tok!r} with fewer than two operands")
            b = stack.pop()
            a = stack.pop()      # popped SECOND, so it is the left operand
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            else:
                if b == 0:
                    raise ValueError("division by zero")
                # int() truncates toward zero; // would floor toward -inf and
                # give -4 instead of -3 for -7 / 2.
                stack.append(int(a / b))
        else:
            try:
                stack.append(int(tok))
            except ValueError:
                raise ValueError(f"not an integer or operator: {tok!r}") from None

    if len(stack) != 1:
        raise ValueError("malformed expression: operands left over")
    return stack[0]
