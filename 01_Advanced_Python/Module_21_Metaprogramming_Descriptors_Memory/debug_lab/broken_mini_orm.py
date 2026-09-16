#!/usr/bin/env python3
"""Broken Mini-ORM demonstrating descriptor state storage on descriptor instance."""

class BrokenDescriptor:
    def __init__(self):
        # Because the descriptor is a class attribute, all model instances share this value!
        self.val = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.val

    def __set__(self, instance, value):
        self.val = value

class UserModel:
    name = BrokenDescriptor()

if __name__ == "__main__":
    u1 = UserModel()
    u2 = UserModel()

    u1.name = "Alice"
    print(f"User 1 name: {u1.name}")

    u2.name = "Bob"
    print(f"User 2 name: {u2.name}")
    print(f"User 1 name after User 2 set: {u1.name} (Corrupted! Overwritten by Bob!)")
