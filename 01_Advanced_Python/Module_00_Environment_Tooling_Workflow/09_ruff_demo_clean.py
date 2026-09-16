"""Clean, idiomatic, fully Ruff-compliant implementation of the demo.

Features:
- Type annotations across all signatures
- Fixed mutable default argument bug using `list[str] | None = None`
- Proper snake_case naming conventions
- Modern f-strings
- Clean, grouped imports
"""

from __future__ import annotations


class UserAccount:
    """Represents a user account with associated metadata tags."""

    def __init__(self, username: str, tags: list[str] | None = None) -> None:
        self.username = username
        # Correctly avoid the mutable default argument trap
        self.tags = list(tags) if tags is not None else []

    def add_tag(self, new_tag: str) -> None:
        """Add a tag to the user's tag list."""
        self.tags.append(new_tag)


def check_status(value: str | None = None) -> None:
    """Check and print user status using modern f-strings and identity checks."""
    if value is None:
        print(f"Status is empty for: {'Anonymous'}")
    else:
        print(f"Status is active for: {value}")


def calculate_metrics(a: float, b: float, c: float) -> float:
    """Calculate combined metric result with proper PEP 8 spacing."""
    return (a + b) * c


def main() -> None:
    acc1 = UserAccount("alice")
    acc1.add_tag("admin")

    acc2 = UserAccount("bob")
    print(f"Alice's tags: {acc1.tags}")
    print(f"Bob's tags (correctly isolated): {acc2.tags}")

    check_status()
    check_status("Alice")

    metric = calculate_metrics(10.0, 5.0, 2.0)
    print(f"Calculated Metric: {metric}")


if __name__ == "__main__":
    main()
