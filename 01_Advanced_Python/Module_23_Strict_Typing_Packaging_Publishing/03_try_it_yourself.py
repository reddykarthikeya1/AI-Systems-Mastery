"""
Module 23: Type Hint & pyproject.toml Validator
Run: python try_it_yourself.py
"""



def find_user_id(names: list[str], target: str) -> int | None:
    try:
        return names.index(target)
    except ValueError:
        return None


def main():
    print("=" * 60)
    print("  MODULE 23: STRICT TYPING PLAYGROUND [*]")
    print("=" * 60)

    roster = ["Alice", "Bob", "Charlie"]
    print(f"Roster: {roster}")

    print("\nTesting typed lookup:")
    for name in ["Bob", "Eve"]:
        idx = find_user_id(roster, name)
        status = f"Found at index {idx}" if idx is not None else "Not found (None)"
        print(f"  Lookup '{name}': {status}")

    print("\n[OK] Type hints validate clean contracts!")


if __name__ == "__main__":
    main()
