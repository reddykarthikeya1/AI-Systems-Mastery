# Module 16: Troubleshooting, Security Traps & JWT Vulnerabilities

This reference guide details critical security vulnerabilities and best practices when designing authentication and authorization systems in Python.

---

## 1. Storing Sensitive Secrets Inside JWT Payloads

### The Mistake
```python
# ❌ DANGEROUS! Storing plaintext credit cards, passwords, or SSNs in JWT:
payload = {
    "sub": "123",
    "credit_card": "4111-2222-3333-4444" # 🚨 CATASTROPHIC!
}
```

### Why It Happens
A JWT is **signed**, not **encrypted**. Anyone who intercepts a JWT can paste it into `jwt.io` and read the JSON payload in clear text!

### The Rule
Only store non-sensitive identifiers and claims in a JWT (e.g. `user_id`, `role`, `exp`, `tenant_id`).

---

## 2. Timing Attacks on Secret Verification

### The Bug
```python
# ❌ VULNERABLE to Timing Attacks:
def verify_api_key(client_key: str, real_key: str) -> bool:
    return client_key == real_key # Standard '==' returns early on first mismatched char!
```

### Why It Happens
Standard string comparison `==` terminates the moment it encounters a mismatched character. Attackers measure microsecond execution latency differences to guess the secret key character-by-character.

### The Fix
Always use constant-time comparison via **`secrets.compare_digest()`**:
```python
import secrets

def verify_api_key(client_key: str, real_key: str) -> bool:
    return secrets.compare_digest(client_key, real_key) # ✅ Constant-time comparison!
```
