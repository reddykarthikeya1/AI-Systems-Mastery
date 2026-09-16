#!/usr/bin/env python3
"""Module 14: Cryptographic Password Hashing Demonstration.

This script demonstrates secure password storage using bcrypt and salted hashes.
"""

from __future__ import annotations

import bcrypt


def hash_password(password: str) -> str:
    """Hashes a password with a fresh random cryptographic salt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies candidate password against stored hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def main() -> None:
    print("=" * 60)
    print("  Bcrypt Salted Password Hashing Demonstration")
    print("=" * 60)

    password = "MySecurePasscode2026!"
    stored_hash = hash_password(password)

    print(f"Original Password : {password}")
    print(f"Stored Hash (DB)  : {stored_hash}\n")

    print("Attempting authentication with correct password:")
    print("  Result:", verify_password(password, stored_hash))

    print("\nAttempting authentication with incorrect password:")
    print("  Result:", verify_password("WrongPassword", stored_hash))


if __name__ == "__main__":
    main()
