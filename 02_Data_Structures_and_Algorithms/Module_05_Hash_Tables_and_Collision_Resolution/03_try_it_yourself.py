"""Module 05: Interactive Hash Tables CLI Sandbox."""
from __future__ import annotations


def demo_hash_lookup():
    print("\n=== DEMO: Hash Map Instant Lookup vs List Search ===")
    d = {"user_101": "Alice", "user_102": "Bob", "user_103": "Charlie"}
    print("Dictionary entries:", d)
    print("Lookup 'user_102':", d.get("user_102"))


if __name__ == "__main__":
    demo_hash_lookup()
