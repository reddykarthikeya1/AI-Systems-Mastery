"""Chapter 20 - Interview Practice: Leaked closures, concurrency rate limiters, and lock ordering.

1. WeakSubscriberRegistry: thread-safe event bus that uses weak references to avoid memory leaks.
2. TokenBucketRateLimiter: thread-safe token bucket rate limiter with monotonic time replenishment.
3. transfer_funds (debugging): fix lock-order inversion deadlock when transferring between accounts.
"""
import threading
import time
import weakref

BUGGY = {
    "transfer_funds": '''def transfer_funds(acc_a, acc_b, amount):
    """Transfer `amount` from `acc_a` to `acc_b` safely using locking."""
    with acc_a.lock:
        with acc_b.lock:
            if acc_a.balance < amount:
                raise ValueError("insufficient funds")
            acc_a.balance -= amount
            acc_b.balance += amount''',
}


class WeakSubscriberRegistry:
    """Event subscriber registry that prevents circular reference memory leaks using weak references."""
    def __init__(self):
        self._subscribers = weakref.WeakKeyDictionary()

    def register(self, subscriber, callback):
        """Register `callback` for `subscriber`. Drops automatically when `subscriber` is garbage collected."""
        self._subscribers[subscriber] = callback

    def notify(self, message):
        """Invoke callbacks for all currently alive subscribers, returning list of results."""
        results = []
        for sub, cb in list(self._subscribers.items()):
            results.append(cb(message))
        return results

    def active_count(self):
        """Return number of currently active, non-collected subscribers."""
        return len(self._subscribers)


class TokenBucketRateLimiter:
    """Thread-safe Token Bucket Rate Limiter."""
    def __init__(self, rate: float, capacity: float):
        self.rate = float(rate)  # tokens added per second
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.last_update = time.monotonic()
        self._lock = threading.Lock()

    def allow_request(self, tokens: float = 1.0) -> bool:
        """Return True if requested tokens are available and consumed; False otherwise."""
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


class Account:
    def __init__(self, account_id: int, balance: float):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()


def transfer_funds(acc_a, acc_b, amount):
    """Transfer `amount` from `acc_a` to `acc_b` safely avoiding deadlock via canonical lock ordering."""
    if acc_a.account_id == acc_b.account_id:
        return
    # Order locks by account_id to eliminate lock-order inversion
    first, second = (acc_a, acc_b) if acc_a.account_id < acc_b.account_id else (acc_b, acc_a)
    with first.lock:
        with second.lock:
            if acc_a.balance < amount:
                raise ValueError("insufficient funds")
            acc_a.balance -= amount
            acc_b.balance += amount


# --- Tests ---

def t_weak_subscriber_registry(m):
    reg = m.WeakSubscriberRegistry()
    class Sub:
        def __init__(self, name):
            self.name = name
    
    s1 = Sub("alpha")
    s2 = Sub("beta")
    
    reg.register(s1, lambda msg: f"{s1.name}:{msg}")
    reg.register(s2, lambda msg: f"{s2.name}:{msg}")
    
    assert reg.active_count() == 2
    res = reg.notify("ping")
    assert sorted(res) == ["alpha:ping", "beta:ping"]
    
    del s1
    import gc; gc.collect()
    assert reg.active_count() == 1
    assert reg.notify("ping2") == ["beta:ping2"]


def t_rate_limiter_replenishment(m):
    limiter = m.TokenBucketRateLimiter(rate=10.0, capacity=2.0)
    assert limiter.allow_request(1.0) is True
    assert limiter.allow_request(1.0) is True
    assert limiter.allow_request(1.0) is False  # capacity exhausted
    time.sleep(0.12)  # replenished ~1.2 tokens
    assert limiter.allow_request(1.0) is True


def t_rate_limiter_concurrency(m):
    limiter = m.TokenBucketRateLimiter(rate=100.0, capacity=50.0)
    allowed = 0
    lock = threading.Lock()
    
    def worker():
        nonlocal allowed
        for _ in range(10):
            if limiter.allow_request(1.0):
                with lock:
                    allowed += 1

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert allowed <= 60  # initial capacity (50) + modest replenishment during run


def t_transfer_funds_deadlock_free(m):
    acc1 = m.Account(1, 1000.0)
    acc2 = m.Account(2, 1000.0)
    
    def worker1():
        for _ in range(100):
            m.transfer_funds(acc1, acc2, 1.0)
            
    def worker2():
        for _ in range(100):
            m.transfer_funds(acc2, acc1, 1.0)

    t1 = threading.Thread(target=worker1)
    t2 = threading.Thread(target=worker2)
    t1.start()
    t2.start()
    t1.join(timeout=3.0)
    t2.join(timeout=3.0)
    
    assert not t1.is_alive() and not t2.is_alive(), "Deadlock detected during concurrent transfer!"
    assert acc1.balance + acc2.balance == 2000.0
