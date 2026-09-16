"""
Module 16: Interactive Password Hashing & Verification Sandbox
Run: python try_it_yourself.py
"""

import hashlib
import secrets


def create_hash(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(8)
    h = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    return salt, h


def verify_password(attempt, salt, stored_hash):
    _, test_hash = create_hash(attempt, salt)
    return test_hash == stored_hash


def main():
    print("=" * 60)
    print("  MODULE 16: SECURITY & PASSWORD HASHING PLAYGROUND [*]")
    print("=" * 60)

    password = "CorrectHorseBatteryStaple"
    salt, stored_hash = create_hash(password)
    print(f"Original Password: {password}")
    print(f"Generated Salt:    {salt}")
    print(f"Stored Hash:       {stored_hash}")

    print("\nTesting verification:")
    for test in [password, "WrongGuess", "correcthorsebatterystaple"]:
        is_correct = verify_password(test, salt, stored_hash)
        status = "[OK] Access Granted" if is_correct else "[X] Access Denied"
        print(f"  Attempt: '{test}' --> {status}")

    print("\n[OK] Cryptographic hash verification demonstrated!")


if __name__ == "__main__":
    main()
