"""Beginner playground for Module 16 - Authentication, Authorization & Security.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib
import hmac

# -------------------------------------------- 1. Secure Password Hashing with PBKDF2
salt = b"random_salt_123"
password = b"supersecret"
hash1 = hashlib.pbkdf2_hmac("sha256", password, salt, iterations=10_000)
hash2 = hashlib.pbkdf2_hmac("sha256", password, salt, iterations=10_000)
assert hash1 == hash2
assert len(hash1) == 32
print(f"Derived 256-bit PBKDF2 hash: {hash1.hex()[:16]}...")

# -------------------------------------------- 2. Constant-Time Comparison to Prevent Timing Attacks
sig_expected = b"valid_signature_token"
sig_received = b"valid_signature_token"
sig_tampered = b"fraud_signature_token"

assert hmac.compare_digest(sig_received, sig_expected) is True
assert hmac.compare_digest(sig_tampered, sig_expected) is False
print("Constant-time HMAC comparison validated authenticity.")

# -------------------------------------------- 3. HMAC Message Integrity Verification
secret_key = b"secret_key_xyz"
message = b"action=transfer&amount=500"
mac = hmac.new(secret_key, message, hashlib.sha256).digest()
assert len(mac) == 32
assert hmac.new(secret_key, message, hashlib.sha256).digest() == mac
print("HMAC payload integrity verified.")

print()
print("All checks passed.")
