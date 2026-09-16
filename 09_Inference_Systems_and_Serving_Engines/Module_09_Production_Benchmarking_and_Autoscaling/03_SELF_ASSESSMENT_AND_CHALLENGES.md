# Module 09: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Sizing Cluster Instances Using Little's Law
**Question**: An AI platform anticipates 120 QPS peak traffic. Average prompt length is 500 tokens, average response length is 200 tokens. Serving telemetry indicates average request residence time $W = 4.0 \text{ seconds}$. A single 8-GPU node can sustain 64 concurrent requests without violating the $P_{99}$ SLA.
Calculate the minimum number of 8-GPU serving nodes required.

**Solution**:
1. **Calculate Required System Concurrency ($L$) via Little's Law**:
   $$L = \lambda \times W = 120 \text{ req/s} \times 4.0 \text{ s} = 480 \text{ concurrent active requests}$$
2. **Calculate Node Count**:
   $$\text{Nodes} = \left\lceil \frac{480}{64} \right\rceil = \lceil 7.5 \rceil = 8 \text{ nodes}$$
3. **Headroom Buffer**: Add $25\%$ headroom for traffic bursts $\implies 10$ nodes total.
