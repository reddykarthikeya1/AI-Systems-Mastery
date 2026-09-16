# Module 26: Troubleshooting & Enterprise Architecture Edge Cases

This reference guide details failure modes and mitigation patterns in production microservice platforms.

---

## 1. Connection Pool Exhaustion

### The Problem
When traffic spikes from 100 req/s to 5,000 req/s, database connections exceed max pool size (`pool_size=20`), throwing `TimeoutError: QueuePool limit of size 20 overflow 10 reached`.

### The Fix
Configure appropriate pool sizing and connection recycling:
```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=50,
    max_overflow=20,
    pool_timeout=10,
    pool_recycle=1800,
)
```

---

## 2. Circuit Breakers for Resilient Microservices

### The Pattern
If a downstream payment service or external API fails 5 consecutive times, open the circuit breaker to fail fast for 30 seconds rather than hanging customer requests.
