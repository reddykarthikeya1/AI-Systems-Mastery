# Module 03: Edge Infrastructure, DNS, CDNs & Reverse Proxies: Self-Assessment, Architectural Questions & Challenges

Evaluate your mastery of **Anycast BGP Routing, CDN Edge Caching, TLS Offloading, and Reverse Proxy Gateways** through diagnostic interview questions, architectural trade-off evaluations, and hands-on coding challenges.

---

## Part 1: Diagnostic Architectural & Scalability Questions

### Question 1
How does Anycast DNS route a global user's query to the physically nearest PoP (Point of Presence) without stateful routing?

### Question 2
What is the difference between an Edge CDN Cache Hit, Cache Miss, and a Stale-While-Revalidate revalidation cycle?

### Question 3
Why should TLS termination be handled at the Edge Proxy / Reverse Proxy (Nginx / Envoy) rather than in application microservice containers?

### Question 4
Explain the difference between a Forward Proxy (client egress control) and a Reverse Proxy (server ingress shield).

### Question 5
How does a reverse proxy perform active health checking versus passive health checking on upstream backend clusters?

### Question 6: Production Observability
What are the top 3 Golden Signals (Latency, Traffic, Errors, Saturation) you must monitor on Grafana dashboards for this engine?

### Question 7: Architectural Anti-Patterns
Describe a common rookie implementation mistake when deploying this architecture, and explain why it causes catastrophic failure under high load.

### Question 8: Security & Multi-Tenant Isolation
How does this architecture enforce strict tenant isolation, cryptographic integrity, or rate limiting against denial-of-service (DoS) attacks?

### Question 9: Alternative Comparison & Technology Trade-Offs
Compare this approach to an alternative architecture. When would you choose this design over simpler or more traditional approaches, and what complexity cost do you pay?

### Question 10: Evolution & Migration Strategy
How do you upgrade or migrate this component in production with zero downtime, backward-compatible schemas, and immediate rollback capability?

---

## Part 2: Detailed Answer Keys & Production Rationales

### Answers 1-5: Architectural Analysis
1. Mechanical Constraints: Hardware bus speeds, cache line sizes, and network packet roundtrips impose strict physical limits. Designs must prioritize in-memory batching and pipelining over synchronous disk/network hops.
2. Failure Modes: Systems employ heartbeat probes, lease timeouts, and leader election quorums to detect and isolate failures without data loss.
3. Concurrency: Atomic primitives, locks with TTLs, and lock-free data structures eliminate lost updates and starvation.
4. Consistency Models: Trade-offs between linearizable Strong Consistency and High Availability are chosen based on business failure tolerance.
5. Capacity Sizing: Proactive rate-limiting and circuit-breaking protect against cascading exhaustion during unexpected traffic spikes.

### Answers 6-10: SRE & Operational Standards
6. Observability: Monitor p99 latency, error rates, and queue/thread saturation.
7. Anti-Patterns: Never allow unbounded memory queues, missing remote call timeouts, or synchronous cascading dependencies.
8. Security: Enforce principle of least privilege, mutual TLS (mTLS), and cryptographic token verification.
9. Trade-offs: Accept distributed architectural complexity only when vertical scaling limits are fundamentally breached.
10. Migrations: Use canary deployments, feature flags, and expand-contract schema evolution.

---

## Part 3: Practical Design & Coding Challenges

### Challenge 1: Reverse Proxy Path-Based Router
Implement a path-based routing table with prefix matching and upstream round-robin selection.

#### Solution:
```python
class PathRouter:
    def __init__(self):
        self.routes = {}
        self.rr_index = {}

    def add_route(self, prefix: str, upstreams: list[str]):
        self.routes[prefix] = upstreams
        self.rr_index[prefix] = 0

    def route(self, path: str) -> str:
        for prefix in sorted(self.routes.keys(), key=len, reverse=True):
            if path.startswith(prefix):
                servers = self.routes[prefix]
                idx = self.rr_index[prefix]
                selected = servers[idx % len(servers)]
                self.rr_index[prefix] += 1
                return selected
        raise ValueError("No route matched")

router = PathRouter()
router.add_route("/api/v1/users", ["srv-user-1:8000", "srv-user-2:8000"])
assert router.route("/api/v1/users/profile") == "srv-user-1:8000"
assert router.route("/api/v1/users/settings") == "srv-user-2:8000"
print("✅ Challenge 1 Passed!")
```

### Challenge 2: Exponential Backoff with Jitter
Implement a full-jitter exponential backoff calculation to prevent the Thundering Herd problem against downstream services.

#### Solution:
```python
import random

def calculate_backoff(attempt: int, base: float = 0.1, cap: float = 2.0) -> float:
    temp = min(cap, base * (2 ** attempt))
    return random.uniform(0, temp)

delays = [calculate_backoff(i) for i in range(5)]
assert all(0 <= d <= 2.0 for d in delays)
print("✅ Challenge 2 Passed!")
```
