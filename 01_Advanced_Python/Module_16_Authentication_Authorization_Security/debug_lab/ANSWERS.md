# Debug Lab Answers: Module 16

<details>
<summary>Bug 1: Disabling verify_exp in JWT decoding</summary>

### Root Cause
Passing `options={"verify_exp": False}` instructs PyJWT to ignore the `exp` claim, allowing replayed expired tokens to authenticate indefinitely.

### Fix
Allow PyJWT to verify `exp` by default (or set `verify_exp: True`):
```python
def secure_token_verify(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=["HS256"])
```
</details>

<details>
<summary>Bug 2: Non-constant time string comparison</summary>

### Root Cause
Python's `==` operator compares strings byte-by-byte and terminates immediately upon finding the first non-matching byte.

### Fix
Use `hmac.compare_digest` for constant-time comparison:
```python
def secure_secret_comparison(user_input: str, actual_secret: str) -> bool:
    return hmac.compare_digest(user_input.encode("utf-8"), actual_secret.encode("utf-8"))
```
</details>
