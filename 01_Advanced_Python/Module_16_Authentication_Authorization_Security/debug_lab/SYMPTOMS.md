# Debug Lab: Module 16 — Authentication & Security Traps

## How to Run
```bash
python debug_lab/broken_auth_service.py
```

## Observed Symptoms
1. **Expired tokens accepted indefinitely**:
   A JWT expired 365 days ago decodes successfully without raising `jwt.ExpiredSignatureError`.
2. **Timing attack vulnerability**:
   Standard string equality returns early on first mismatched character, allowing attackers to measure microsecond latency differences to reconstruct secrets.
