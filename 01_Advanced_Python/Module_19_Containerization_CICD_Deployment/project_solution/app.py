#!/usr/bin/env python3
"""Production Containerized Microservice.

Module 17 (Containerization, CI/CD & Deployment) Turnkey Project Implementation.
Demonstrates Prometheus telemetry exposition, health probes, and cloud-native architecture.
"""

from __future__ import annotations

import os
import time
from collections import defaultdict

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import PlainTextResponse

app = FastAPI(
    title="Cloud-Native Production Microservice",
    version=os.getenv("APP_VERSION", "1.0.0"),
)

# Metrics Storage
request_counts: dict[str, int] = defaultdict(int)
request_durations: dict[str, list[float]] = defaultdict(list)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next) -> Response:
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration = time.perf_counter() - start

    path = request.url.path
    status_code = response.status_code
    metric_key = f'path="{path}",status="{status_code}"'

    request_counts[metric_key] += 1
    request_durations[path].append(duration)
    return response


@app.get("/healthz/live", status_code=status.HTTP_200_OK)
def liveness_probe() -> dict[str, object]:
    return {"status": "LIVE", "timestamp": time.time()}


@app.get("/healthz/ready", status_code=status.HTTP_200_OK)
def readiness_probe() -> dict[str, object]:
    # Check DB or dependent service readiness
    return {"status": "READY", "version": os.getenv("APP_VERSION", "1.0.0")}


@app.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    lines = [
        "# HELP http_requests_total Total number of HTTP requests processed",
        "# TYPE http_requests_total counter",
    ]
    for key, count in request_counts.items():
        lines.append(f"http_requests_total{{{key}}} {count}")

    lines.append("# HELP http_request_duration_seconds Request processing latency")
    lines.append("# TYPE http_request_duration_seconds summary")
    for path, durs in request_durations.items():
        lines.append(f'http_request_duration_seconds_count{{path="{path}"}} {len(durs)}')
        lines.append(f'http_request_duration_seconds_sum{{path="{path}"}} {sum(durs):.4f}')

    return "\n".join(lines) + "\n"
