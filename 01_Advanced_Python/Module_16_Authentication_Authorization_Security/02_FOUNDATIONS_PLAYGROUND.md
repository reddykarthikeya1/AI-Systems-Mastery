# Interactive Foundations Playground: Authentication, Passwords & Security

> *"Never store raw passwords; hash them with a random salt so even a database leak reveals nothing."*

Welcome to the **Module 16 Authentication Authorization Security** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Security begins with never storing plaintext secrets. When a user creates a password, you combine it with a random **salt** and run it through a cryptographic **one-way hash** function.

---

## 2. Micro-Code Example (3-5 Lines)

```python
import hashlib
import secrets

def hash_password(password: str):
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return salt, hashed

salt, key = hash_password("Secret123!")
print("Random Salt:", salt)
print("SHA256 Hash:", key)
```

### Line-by-Line Breakdown:
- `secrets.token_hex(16)`: Generates cryptographically secure random bytes for salting.
- `password + salt`: Prevents rainbow table dictionary attacks by making identical passwords produce different hashes.
- `hashlib.sha256(...)`: A one-way cryptographic hash: easy to calculate forward, mathematically impossible to reverse.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
Why shouldn't you use `random.randint()` for security tokens or passwords?

<details><summary><b>Show Answer</b></summary>

The `random` module uses the Mersenne Twister algorithm, which is predictable. Always use `secrets` for security.
</details>

---

### Drill 2: Quick Check
Can you decrypt a SHA256 hash back to the original password?

<details><summary><b>Show Answer</b></summary>

**No.** Cryptographic hashes are one-way mathematical functions, not encryptions.
</details>

---
