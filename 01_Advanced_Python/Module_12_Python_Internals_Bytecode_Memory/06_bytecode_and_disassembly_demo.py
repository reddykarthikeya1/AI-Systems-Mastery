#!/usr/bin/env python3
"""Module 11: Bytecode & Disassembly Demonstration.

This script demonstrates disassembling Python code into low-level PVM opcodes
and understanding bytecode instructions.
"""

from __future__ import annotations

import dis


def add_numbers(a: int, b: int) -> int:
    return a + b


def for_loop_sum(limit: int) -> int:
    total = 0
    for i in range(limit):
        total += i
    return total


def main() -> None:
    print("=" * 60)
    print("  1. Bytecode Disassembly: Simple Function (add_numbers)")
    print("=" * 60)
    dis.dis(add_numbers)

    print("\n" + "=" * 60)
    print("  2. Bytecode Disassembly: For Loop (for_loop_sum)")
    print("=" * 60)
    dis.dis(for_loop_sum)


if __name__ == "__main__":
    main()
