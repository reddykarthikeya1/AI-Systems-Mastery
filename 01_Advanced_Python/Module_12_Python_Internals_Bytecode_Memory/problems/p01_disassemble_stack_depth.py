"""Problem 01 — Bytecode Stack Depth Evaluator

Target: Production-grade implementation

Example:
    >>> ops = [('LOAD_FAST', 0), ('LOAD_CONST', 1), ('BINARY_OP', 0), ('RETURN_VALUE', 0)]
    >>> calculate_net_stack_effect(ops)
    0

Hints:
    Hint 1: Each opcode has a fixed, known effect on the size of the value
        stack — you don't need to simulate real values, just tally how much
        the stack grows or shrinks as you scan the opcode list in order.
    Hint 2: Keep a running `depth` counter and dispatch on the opcode name:
        the `LOAD_*` family pushes one value, while binary/compare ops and
        `POP_TOP`/`RETURN_VALUE` each consume without replacing more than one.
    Hint 3: `BINARY_OP`/`COMPARE_OP` pop two operands but push one result, so
        their net effect is -1, not -2 — that's the detail the reference
        solution encodes and the test's `LOAD, LOAD, BINARY_OP, RETURN_VALUE`
        sequence (net effect 0) is specifically checking for.
"""

from __future__ import annotations


def calculate_net_stack_effect(opcodes: list[tuple[str, int]]) -> int:
    raise NotImplementedError('Implement calculate_net_stack_effect')
