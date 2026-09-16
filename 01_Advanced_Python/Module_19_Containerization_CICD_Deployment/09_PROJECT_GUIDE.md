# Module_19_Containerization_CICD_Deployment: Project Implementation Guide

**Deliverable:** a production microservice packaged in a multi-stage Docker container with Prometheus telemetry, health probes, and CI/CD automation.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_app.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Health & Readiness Probes
Implement `GET /healthz/live` (liveness check) and `GET /healthz/ready` (dependency check) returning HTTP 200.

### Step 2 — Prometheus Telemetry Exporter
Implement `GET /metrics` exporting `http_requests_total` counter and `http_request_duration_seconds` summary.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_app.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Multi-Stage Dockerfile
Write a multi-stage `Dockerfile` with build stage installing dependencies and runner stage running as non-root user `10001`.

### Step 4 — Request Latency Middleware
Implement ASGI middleware tracking duration of each request and incrementing path/status metric counters.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/app.py`, change the metrics middleware to omit status code from the metric key (e.g. `path="{path}"`).
Run:
```bash
pytest ../project_solution/test_app.py -k test_metrics_tracks_status_codes -v
```
Watch the test fail when status code is missing from Prometheus output, then restore the label.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_app.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Kubernetes Helm Chart:** Create a production Helm chart with horizontal pod autoscaling (HPA).
2. **Graceful SIGTERM Drain:** Intercept SIGTERM signals and wait up to 10s for active HTTP requests to complete.
3. **Structured JSON Access Logs:** Format stdout logs as single-line JSON records for FluentBit ingestion.
4. **Distroless Base Image:** Build container on Google Distroless Python image for zero-CVE footprint.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_liveness_and_readiness_probes` | Proves liveness and readiness endpoints return valid health payloads |
| `test_prometheus_metrics_endpoint` | Proves /metrics exposes Prometheus formatted counters and summaries |
| `test_metrics_tracks_exact_request_count` | Proves each request increments request counter by 1 |
| `test_metrics_tracks_status_codes_and_404` | Proves 404 responses are tracked with status labels |
| `test_readiness_probe_version_field` | Proves readiness probe reflects APP_VERSION environment variable |

---

## 🎓 You have mastered this module when you can…

- [ ] Write multi-stage Dockerfiles optimizing layer caching and minimizing final image size
- [ ] Always execute containerized applications as an unprivileged non-root user
- [ ] Explain why containers must bind to 0.0.0.0 rather than 127.0.0.1
- [ ] Implement Kubernetes liveness and readiness probe endpoints correctly
- [ ] Instrument ASGI applications with Prometheus counters and latency histograms
- [ ] Configure automated CI/CD pipelines executing linting, typing, and test suites
- [ ] Handle OS signals (SIGTERM, SIGINT) for graceful connection draining
