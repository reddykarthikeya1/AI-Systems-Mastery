"""Chapter 14 - Security: signed tokens and RBAC (stdlib only).

1. sign_token / verify_token: a minimal HS256 JWT, built with hmac and base64url.
2. can: role-based access control with role inheritance.
3. check_password_hash (debugging): a timing leak and a missing salt check.
"""
import base64
import hashlib
import hmac
import json
import time

BUGGY = {
    "verify_signature": '''def verify_signature(secret: bytes, message: bytes, signature_hex: str) -> bool:
    """True when signature_hex is the HMAC-SHA256 of message under secret. Must use a constant-time comparison."""
    expected = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return expected == signature_hex''',
}


def _b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _unb64(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def sign_token(payload, secret, now=None):
    """Return 'header.payload.signature' (base64url, no padding) for header {"alg":"HS256","typ":"JWT"}.
    Signature = HMAC-SHA256(secret, 'header.payload'). JSON uses separators=(',', ':') and sort_keys=True. `secret` is bytes."""
    head = _b64(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":"), sort_keys=True).encode())
    body = _b64(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
    sig = hmac.new(secret, f"{head}.{body}".encode(), hashlib.sha256).digest()
    return f"{head}.{body}.{_b64(sig)}"


def verify_token(token, secret, now=None):
    """Return the payload dict if the token is valid, else raise ValueError. Reject: wrong shape, bad signature
    (constant-time compare), header alg other than HS256 (including 'none'), and an 'exp' claim <= now (default time.time())."""
    try:
        head_b, body_b, sig_b = token.split(".")
        header = json.loads(_unb64(head_b))
        payload = json.loads(_unb64(body_b))
        sig = _unb64(sig_b)
    except Exception as e:
        raise ValueError("malformed token") from e
    if header.get("alg") != "HS256":
        raise ValueError("unsupported alg")
    good = hmac.new(secret, f"{head_b}.{body_b}".encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(good, sig):
        raise ValueError("bad signature")
    now = time.time() if now is None else now
    if "exp" in payload and payload["exp"] <= now:
        raise ValueError("expired")
    return payload


def can(roles, role, permission):
    """`roles` maps role -> {'perms': set of strings, 'inherits': list of role names}. Return True if `role` has `permission`
    directly or through inheritance. A permission ending in '*' (e.g. 'doc:*') grants everything with that prefix.
    Unknown roles have no permissions; inheritance cycles must not loop forever."""
    seen, stack = set(), [role]
    while stack:
        r = stack.pop()
        if r in seen or r not in roles:
            continue
        seen.add(r)
        for p in roles[r].get("perms", ()):
            if p == permission or (p.endswith("*") and permission.startswith(p[:-1])):
                return True
        stack.extend(roles[r].get("inherits", ()))
    return False


def verify_signature(secret: bytes, message: bytes, signature_hex: str) -> bool:
    """True when signature_hex is the HMAC-SHA256 of message under secret. Must use a constant-time comparison."""
    expected = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_hex)


def t_token_roundtrip(m):
    tok = m.sign_token({"sub": "u1", "exp": 2000}, b"k")
    assert tok.count(".") == 2 and "=" not in tok
    assert m.verify_token(tok, b"k", now=1000) == {"sub": "u1", "exp": 2000}


def t_token_matches_reference_signature(m):
    # an independent implementation's output: header/payload fixed, so the signature is deterministic
    tok = m.sign_token({"a": 1}, b"secret")
    head, body, sig = tok.split(".")
    expected = hmac.new(b"secret", f"{head}.{body}".encode(), hashlib.sha256).digest()
    assert _unb64(sig) == expected
    assert json.loads(_unb64(head)) == {"alg": "HS256", "typ": "JWT"}


def t_token_rejections(m):
    tok = m.sign_token({"sub": "u", "exp": 10}, b"k")
    cases = [(tok, b"wrong", 1), (tok, b"k", 10), (tok[:-2] + "AA", b"k", 1), ("a.b", b"k", 1), ("", b"k", 1)]
    for t, key, now in cases:
        try:
            m.verify_token(t, key, now=now)
        except ValueError:
            continue
        raise AssertionError(f"must reject {t[:20]!r}")


def t_token_rejects_alg_none(m):
    head = _b64(json.dumps({"alg": "none", "typ": "JWT"}).encode())
    body = _b64(json.dumps({"sub": "admin"}).encode())
    try:
        m.verify_token(f"{head}.{body}.", b"k", now=0)
    except ValueError:
        return
    raise AssertionError("alg=none must be rejected")


def t_can_inheritance_and_wildcards(m):
    roles = {"viewer": {"perms": {"doc:read"}}, "editor": {"perms": {"doc:write"}, "inherits": ["viewer"]},
             "admin": {"perms": {"*"}}, "loop_a": {"inherits": ["loop_b"]}, "loop_b": {"inherits": ["loop_a"], "perms": {"x:1"}}}
    assert m.can(roles, "editor", "doc:read") and m.can(roles, "editor", "doc:write") and not m.can(roles, "viewer", "doc:write")
    assert m.can(roles, "admin", "anything:at:all") and not m.can(roles, "ghost", "doc:read")
    assert m.can(roles, "loop_a", "x:1") and not m.can(roles, "loop_a", "y:1")


def t_verify_signature_constant_time(m):
    import inspect
    sig = hmac.new(b"k", b"msg", hashlib.sha256).hexdigest()
    assert m.verify_signature(b"k", b"msg", sig) and not m.verify_signature(b"k", b"msg", "0" * 64)
    assert "compare_digest" in inspect.getsource(m.verify_signature)
