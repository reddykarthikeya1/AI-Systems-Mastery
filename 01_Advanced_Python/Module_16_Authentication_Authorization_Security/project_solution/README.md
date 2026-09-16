# Design Rationale: Multi-Tenant OAuth2 & Role-Based Authorization Guard

## Architectural Overview
An enterprise security subsystem providing password hashing with work factors (`bcrypt`), stateless JWT token minting and validation, and Role-Based Access Control (RBAC).

## Key Design Decisions
1. **Stateless JWT Authorization:** Access tokens encapsulate user identities and role claims cryptographically signed with HMAC-SHA256, eliminating per-request database lookups in microservices.
2. **Constant-Time Digest Comparison:** API key and token checks use `hmac.compare_digest()`, eliminating timing side-channel attacks that leak secret prefixes.
3. **Explicit Algorithm Whitelisting:** JWT decoding requires explicit `algorithms=['HS256']`, completely preventing the notorious `alg: "none"` authentication bypass vulnerability.

## Rejected Alternatives
1. **Fast Cryptographic Hashes (SHA-256 / MD5) for Passwords:**
   - *Reason for Rejection:* SHA-256 can be computed at billions of hashes per second on modern GPUs, making password rainbow-table cracking trivial.
2. **Storing Sensitive Identity Attributes in JWT Payloads:**
   - *Reason for Rejection:* JWT payloads are Base64URL-encoded, not encrypted. Any network observer or client can decode and view plaintext claims.

## Invariants & Guarantees
- Expired or tampered tokens are rejected with HTTP 401.
- Insufficient user role permissions are rejected with HTTP 403.

## Verification
```bash
pytest test_auth_service.py -v
```
