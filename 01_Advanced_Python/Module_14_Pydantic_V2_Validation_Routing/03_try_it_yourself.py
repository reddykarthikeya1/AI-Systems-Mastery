"""
Module 14: Interactive Data Schema & Validation Sandbox
Run: python try_it_yourself.py
"""


class SimpleValidator:
    def __init__(self, username, age_raw):
        self.errors = []
        self.username = str(username).strip()
        if len(self.username) < 3:
            self.errors.append("Username must be at least 3 characters.")

        try:
            self.age = int(age_raw)
            if self.age < 0 or self.age > 120:
                self.errors.append("Age must be between 0 and 120.")
        except (ValueError, TypeError):
            self.errors.append("Age must be a valid integer.")

    def is_valid(self):
        return len(self.errors) == 0


def main():
    print("=" * 60)
    print("  MODULE 14: PYDANTIC-STYLE VALIDATION PLAYGROUND [*]")
    print("=" * 60)

    test_cases = [
        ("alice", "28"),
        ("bob", "invalid_age"),
        ("x", "45"),
        ("charlie", "-10"),
    ]

    for user, age in test_cases:
        v = SimpleValidator(user, age)
        status = "[OK] Valid" if v.is_valid() else f"[X] Error: {v.errors}"
        print(f"  Input: user='{user}', age='{age}' --> {status}")

    print("\n[OK] Validation logic demonstrated cleanly!")


if __name__ == "__main__":
    main()
