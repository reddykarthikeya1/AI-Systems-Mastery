"""
Module 12: Bytecode Disassembler and Memory Inspector
Run: python try_it_yourself.py
"""

import dis
import sys


def compute_tax(amount, rate):
    return amount * rate


def main():
    print("=" * 60)
    print("  MODULE 12: CPYTHON INTERNALS PLAYGROUND [*]")
    print("=" * 60)

    print("\n1. Memory Addresses & Reference Counts:")
    item = {"name": "Laptop", "price": 999}
    print(f"  Object: {item}")
    print(f"  Memory Address: {hex(id(item))}")
    print(f"  Reference Count: {sys.getrefcount(item)}")

    print("\n2. Disassembling compute_tax into Bytecode:")
    print("-" * 50)
    dis.dis(compute_tax)
    print("-" * 50)
    print("[OK] Real CPython Virtual Machine opcodes displayed!")


if __name__ == "__main__":
    main()
