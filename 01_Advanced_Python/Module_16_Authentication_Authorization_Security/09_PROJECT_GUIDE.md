# Module_16_Authentication_Authorization_Security: Project Implementation Guide

**Deliverable:** a secure authentication microservice featuring salted Bcrypt password hashing, PyJWT bearer tokens, and role-based access dependencies.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_auth_service.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Bcrypt Hashing Helpers
Implement `hash_password(password)` and `verify_password(plain, hashed)` using `bcrypt` with salt rounds >= 10.

### Step 2 — Cryptographic JWT Issuance
Implement `create_jwt(user)` embedding `sub`, `username`, `role`, and UTC `exp` signed with HS256.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_auth_service.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — User Registration & Login Endpoints
Implement `POST /auth/register` (hashing password before save) and `POST /auth/login` returning bearer access token.

### Step 4 — RBAC Guard Dependency
Implement `require_role(["admin"])` dependency validating bearer token and enforcing role permissions.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/auth_service.py`, change the role check so that non-admin users are allowed to access `/admin/metrics`.
Run:
```bash
pytest ../project_solution/test_auth_service.py -k test_rbac_permission_denied_for_viewer -v
```
Watch the test fail because viewer accessed admin endpoint, then restore the 403 Forbidden check.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_auth_service.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Refresh Token Rotation:** Implement refresh tokens stored in Redis with one-time revocation.
2. **Password Complexity Validator:** Enforce uppercase, lowercase, numbers, and symbols in Pydantic schema.
3. **Rate Limiting Login Attempts:** Lock accounts or add exponential delay after 5 failed password attempts.
4. **OAuth2 Scopes:** Extend RBAC to granular OAuth2 scopes (`users:read`, `users:write`, `reports:export`).

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_user_registration_and_login_flow` | Proves registration, token issuance, and protected endpoint access |
| `test_rbac_permission_denied_for_viewer` | Proves viewers receive 403 Forbidden when requesting admin endpoints |
| `test_login_incorrect_password_returns_401` | Proves invalid password attempts return 401 Unauthorized |
| `test_expired_jwt_token_returns_401` | Proves expired JWT tokens are rejected |
| `test_tampered_jwt_signature_returns_401` | Proves tokens with tampered signatures return 401 Unauthorized |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain password security principles: salting, slow hash work factors, and rainbow table resistance
- [ ] Hash and verify passwords safely using bcrypt
- [ ] Issue and verify signed JSON Web Tokens (JWT) using PyJWT
- [ ] Always use UTC timestamps for expiration verification to avoid clock drift bugs
- [ ] Implement role-based access control (RBAC) using FastAPI dependency injection
- [ ] Prevent timing attacks by using constant-time string comparison
- [ ] Write security test cases asserting token tampering and permission boundaries
