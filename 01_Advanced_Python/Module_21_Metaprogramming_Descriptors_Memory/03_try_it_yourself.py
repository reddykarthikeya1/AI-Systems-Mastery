"""
Module 21: Descriptor Validator & Slots Demo
Run: python try_it_yourself.py
"""



class ValidatedAge:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, 0)

    def __set__(self, instance, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{self.name} must be a non-negative integer!")
        instance.__dict__[self.name] = value


class User:
    age = ValidatedAge()

    def __init__(self, age):
        self.age = age


def main():
    print("=" * 60)
    print("  MODULE 21: DESCRIPTORS & SLOTS PLAYGROUND [*]")
    print("=" * 60)

    u = User(25)
    print(f"Created User with age: {u.age}")

    print("\nTesting descriptor boundary enforcement:")
    try:
        u.age = -5
    except ValueError as e:
        print(f"  [OK] Caught illegal value: {e}")

    print("\n[OK] Descriptors guard class attribute access seamlessly!")


if __name__ == "__main__":
    main()
