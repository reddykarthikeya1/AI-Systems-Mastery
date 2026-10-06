"""Chapter 09 - Testing with fakes, injected clocks and idempotency.

1. retry: retry with exponential backoff, with `sleep` injected so tests need no real waiting.
2. RateLimiter: sliding-window limiter with an injected clock.
3. charge_once (debugging): a failed payment can never be retried.
"""

BUGGY = {
    "charge_once": '''def charge_once(ledger, order_id, amount, gateway):
    """Idempotent payment. `ledger` is a dict order_id -> receipt. Charge via gateway(amount) at most once per order_id,
    return the receipt. If the gateway raises, nothing is recorded, so a later call with the same order_id tries again."""
    if order_id in ledger:
        return ledger[order_id]
    ledger[order_id] = "pending"
    ledger[order_id] = gateway(amount)
    return ledger[order_id]''',
}


def retry(fn, attempts, sleep, base=1.0):
    """Call fn() up to `attempts` times. After failure number k (1-based) that is not the last, call sleep(base * 2**(k-1)).
    Return fn's first successful result; re-raise the LAST exception when all attempts fail. attempts < 1 raises ValueError.
    Only Exception subclasses are retried (KeyboardInterrupt must pass through)."""
    if attempts < 1:
        raise ValueError("attempts must be >= 1")
    for k in range(1, attempts + 1):
        try:
            return fn()
        except Exception:
            if k == attempts:
                raise
            sleep(base * 2 ** (k - 1))


class RateLimiter:
    """Allow at most `limit` calls per key within any sliding window of `window` seconds.
    allow(key) returns True (and records the call) or False. `clock` is a zero-argument callable returning seconds.
    A call exactly `window` seconds after an earlier one no longer counts against it."""

    def __init__(self, limit, window, clock):
        self.limit, self.window, self.clock = limit, window, clock
        self._calls = {}

    def allow(self, key):
        now = self.clock()
        q = self._calls.setdefault(key, [])
        q[:] = [t for t in q if now - t < self.window]
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True


def charge_once(ledger, order_id, amount, gateway):
    """Idempotent payment. `ledger` is a dict order_id -> receipt. Charge via gateway(amount) at most once per order_id,
    return the receipt. If the gateway raises, nothing is recorded, so a later call with the same order_id tries again."""
    if order_id in ledger:
        return ledger[order_id]
    receipt = gateway(amount)
    ledger[order_id] = receipt
    return receipt


def t_retry_backoff_schedule(m):
    sleeps, calls = [], []

    def flaky():
        calls.append(1)
        if len(calls) < 4:
            raise ConnectionError("down")
        return "ok"

    assert m.retry(flaky, 5, sleeps.append, base=0.5) == "ok" and sleeps == [0.5, 1.0, 2.0]


def t_retry_gives_up_with_last_error(m):
    sleeps, n = [], [0]

    def always():
        n[0] += 1
        raise ValueError(f"fail {n[0]}")

    try:
        m.retry(always, 3, sleeps.append)
    except ValueError as e:
        assert str(e) == "fail 3" and sleeps == [1.0, 2.0]
    else:
        raise AssertionError("must re-raise")
    try:
        m.retry(always, 0, sleeps.append)
    except ValueError:
        return
    raise AssertionError("attempts=0 must raise ValueError")


def t_ratelimiter_window(m):
    now = [0.0]
    rl = m.RateLimiter(2, 10, lambda: now[0])
    assert rl.allow("a") and rl.allow("a") and not rl.allow("a")
    assert rl.allow("b")
    now[0] = 9.9
    assert not rl.allow("a")
    now[0] = 10.0
    assert rl.allow("a")


def t_ratelimiter_rejected_calls_do_not_count(m):
    now = [0.0]
    rl = m.RateLimiter(1, 5, lambda: now[0])
    assert rl.allow("k")
    now[0] = 4
    assert not rl.allow("k")
    now[0] = 5
    assert rl.allow("k")


def t_charge_once_retry_after_failure(m):
    ledger, attempts = {}, []

    def gateway(amount):
        attempts.append(amount)
        if len(attempts) == 1:
            raise ConnectionError("timeout")
        return f"rcpt-{amount}"

    try:
        m.charge_once(ledger, "o1", 10, gateway)
    except ConnectionError:
        pass
    assert m.charge_once(ledger, "o1", 10, gateway) == "rcpt-10"
    assert m.charge_once(ledger, "o1", 10, gateway) == "rcpt-10" and len(attempts) == 2
