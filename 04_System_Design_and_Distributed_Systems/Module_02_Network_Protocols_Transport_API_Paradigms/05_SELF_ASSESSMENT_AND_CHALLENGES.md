# Module 02: Network Protocols, Transport Layers & API Paradigms: Self-Assessment, Architectural Questions & Challenges

Evaluate your mastery of **TCP/UDP, HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC), gRPC, and WebSockets** through diagnostic interview questions, architectural trade-off evaluations, and hands-on coding challenges.

---

## Part 1: Diagnostic Architectural & Scalability Questions

### Question 1
What is Head-of-Line (HOL) blocking in HTTP/2 multiplexed TCP streams, and how does HTTP/3 (QUIC over UDP) eliminate it?

### Question 2
Why does gRPC with Protocol Buffers outperform REST with JSON by 5x to 10x in internal microservice East-West communication?

### Question 3
When should you choose WebSockets over Server-Sent Events (SSE) or long-polling for real-time applications?

### Question 4
Explain the TCP 3-way handshake and TLS 1.3 1-RTT connection setup overhead on first-byte latency.

### Question 5
How does UDP checksum verification work, and why do multiplayer games and real-time audio accept packet loss over retransmission latency?

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

### Challenge 1: Binary TLV Framing Parser
Implement a binary Type-Length-Value (TLV) frame encoder and decoder for high-throughput RPC protocols.

#### Solution:
```python
import struct

def encode_tlv(msg_type: int, payload: bytes) -> bytes:
    length = len(payload)
    return struct.pack("!HI", msg_type, length) + payload

def decode_tlv(data: bytes) -> tuple[int, bytes]:
    msg_type, length = struct.unpack("!HI", data[:6])
    payload = data[6:6 + length]
    return msg_type, payload

encoded = encode_tlv(0x01, b"PING_FRAME")
m_type, p = decode_tlv(encoded)
assert m_type == 1
assert p == b"PING_FRAME"
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
