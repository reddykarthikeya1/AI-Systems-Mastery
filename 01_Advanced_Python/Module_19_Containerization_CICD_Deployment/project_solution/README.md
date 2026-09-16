# Design Rationale: Hardened Microservice Container & Observability Pipeline

## Architectural Overview
A cloud-native production deployment package featuring multi-stage Docker builds, unprivileged non-root execution, Prometheus telemetry exposition, and automated CI pipelines.

## Key Design Decisions
1. **Multi-Stage Docker Architecture:** Compiles dependencies in a heavy builder image and copies only the resulting virtualenv into a minimal Debian-slim runner, shrinking image size by 90%.
2. **Unprivileged Non-Root User (`UID 10001`):** Dropping root privileges inside the container mitigates container-escape vulnerabilities and host privilege escalation.
3. **Prometheus Latency Histograms:** Exposes request latency distributions with explicit buckets, enabling precise p95 and p99 percentile tracking in Grafana.

## Rejected Alternatives
1. **Alpine Linux (`python:3.11-alpine`) for Heavy Python Apps:**
   - *Reason for Rejection:* Alpine uses `musl` libc rather than `glibc`. Pre-compiled wheels fail to install, requiring prolonged C-compilations that frequently fail in CI.
2. **High-Cardinality Labels in Prometheus Metrics (e.g. `user_id`):**
   - *Reason for Rejection:* Assigning dynamic user IDs as metric labels creates millions of unique time series in memory, crashing the Prometheus time-series database.

## Invariants & Guarantees
- Zero build tools (gcc, git) present in the production runtime container.
- All metric labels are bounded, finite enums.

## Verification
```bash
pytest test_app.py -v
```
