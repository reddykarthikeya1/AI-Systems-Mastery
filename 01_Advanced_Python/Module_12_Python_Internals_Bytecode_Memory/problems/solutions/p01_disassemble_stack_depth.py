"""Problem 01 — Bytecode Stack Depth Evaluator

Target: Production-grade implementation
"""

from __future__ import annotations


def calculate_net_stack_effect(opcodes: list[tuple[str, int]]) -> int:
    depth = 0
    for op, arg in opcodes:
        if op in ('LOAD_CONST', 'LOAD_FAST', 'LOAD_GLOBAL'):
            depth += 1
        elif op in ('BINARY_OP', 'COMPARE_OP'):
            depth -= 1
        elif op == 'POP_TOP':
            depth -= 1
        elif op == 'RETURN_VALUE':
            depth -= 1
    return depth
