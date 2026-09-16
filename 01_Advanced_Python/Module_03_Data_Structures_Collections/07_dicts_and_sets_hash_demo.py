#!/usr/bin/env python3
"""Module 03: Dictionaries, Hash Tables & Sets Demonstration.

This script demonstrates hash table lookups, dictionary merging,
set algebra operations, and read-only mapping proxies.
"""

from __future__ import annotations

import types


def demo_hash_and_dictionary_operations() -> None:
    print("=" * 60)
    print("  1. Dictionary Operations & Modern Merge Syntax (|)")
    print("=" * 60)

    # Base configuration dictionary
    defaults = {"theme": "light", "font_size": 14, "auto_save": True}
    user_settings = {"theme": "dark", "show_line_numbers": True}

    # Modern merge operator (Python 3.9+)
    active_config = defaults | user_settings
    print(f"Merged Config: {active_config}")

    # Dictionary Comprehension
    names = ["Alice", "Bob", "Charlie", "Diana"]
    name_lengths = {name: len(name) for name in names}
    print(f"Name Lengths Dictionary: {name_lengths}")


def demo_set_algebra() -> None:
    print("\n" + "=" * 60)
    print("  2. Set Operations & Fast Membership Testing")
    print("=" * 60)

    group_a = {"Python", "SQL", "Docker", "AWS"}
    group_b = {"Python", "Rust", "Kubernetes", "Docker"}

    print(f"Group A: {group_a}")
    print(f"Group B: {group_b}\n")

    print(f"Intersection (&) (Common Skills)      : {group_a & group_b}")
    print(f"Union (|) (All Skills Combined)       : {group_a | group_b}")
    print(f"Difference (-) (Unique to Group A)    : {group_a - group_b}")
    print(f"Symmetric Diff (^) (In A or B, not both): {group_a ^ group_b}")


def demo_read_only_mapping_proxy() -> None:
    print("\n" + "=" * 60)
    print("  3. Read-Only Dictionaries (MappingProxyType)")
    print("=" * 60)

    # An internal mutable dictionary
    internal_data = {"admin_role": "superadmin", "port": 443}

    # Expose a read-only view to outside consumers
    read_only_view = types.MappingProxyType(internal_data)
    print(f"Read-Only View: {read_only_view}")

    try:
        # Attempting mutation will raise a TypeError
        read_only_view["port"] = 8080  # type: ignore
    except TypeError as e:
        print(f"[PROTECTED] Mutation blocked successfully: {e}")


def main() -> None:
    demo_hash_and_dictionary_operations()
    demo_set_algebra()
    demo_read_only_mapping_proxy()


if __name__ == "__main__":
    main()
