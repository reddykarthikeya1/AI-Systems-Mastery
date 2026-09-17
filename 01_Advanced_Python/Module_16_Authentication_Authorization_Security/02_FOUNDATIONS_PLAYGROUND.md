# 🐣 Interactive Foundations Playground: Authentication, Authorization & Security

> *"Security relies on cryptographic hashes, constant-time comparisons, and strict token validation."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import hashlib
import hmac
```

---

## 1. Secure Password Hashing with PBKDF2

Salted PBKDF2 hashing protects passwords against precomputed rainbow table attacks.

```python
salt = b"random_salt_123"
password = b"supersecret"
hash1 = hashlib.pbkdf2_hmac("sha256", password, salt, iterations=10_000)
hash2 = hashlib.pbkdf2_hmac("sha256", password, salt, iterations=10_000)
assert hash1 == hash2
assert len(hash1) == 32
print(f"Derived 256-bit PBKDF2 hash: {hash1.hex()[:16]}...")
```

---

## 2. Constant-Time Comparison to Prevent Timing Attacks

`hmac.compare_digest` prevents side-channel timing attacks when validating signatures.

```python
sig_expected = b"valid_signature_token"
sig_received = b"valid_signature_token"
sig_tampered = b"fraud_signature_token"

assert hmac.compare_digest(sig_received, sig_expected) is True
assert hmac.compare_digest(sig_tampered, sig_expected) is False
print("Constant-time HMAC comparison validated authenticity.")
```

---

## 3. HMAC Message Integrity Verification

HMAC binds secret keys to message payloads to detect message tampering.

```python
secret_key = b"secret_key_xyz"
message = b"action=transfer&amount=500"
mac = hmac.new(secret_key, message, hashlib.sha256).digest()
assert len(mac) == 32
assert hmac.new(secret_key, message, hashlib.sha256).digest() == mac
print("HMAC payload integrity verified.")
```

---
