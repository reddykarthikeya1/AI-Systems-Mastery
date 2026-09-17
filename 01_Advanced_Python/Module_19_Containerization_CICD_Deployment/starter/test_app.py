"""Unit tests for the Containerized Production Microservice."""

from __future__ import annotations

import os
import time

from app import app, request_counts
from fastapi.testclient import TestClient

client = TestClient(app)


def test_liveness_and_readiness_probes() -> None:
    res_live = client.get("/healthz/live")
    assert res_live.status_code == 200
    assert res_live.json()["status"] == "LIVE"

    res_ready = client.get("/healthz/ready")
    assert res_ready.status_code == 200
    assert res_ready.json()["status"] == "READY"


def test_prometheus_metrics_endpoint() -> None:
    client.get("/healthz/live")
    client.get("/healthz/ready")

    res_metrics = client.get("/metrics")
    assert res_metrics.status_code == 200
    body = res_metrics.text
    assert "# TYPE http_requests_total counter" in body
    assert "http_requests_total{" in body
    assert "# TYPE http_request_duration_seconds summary" in body


def test_liveness_probe_timestamp_is_recent() -> None:
    """Test timestamp reported by liveness probe is within 5 seconds of system time."""
    now = time.time()
    res = client.get("/healthz/live")
    assert res.status_code == 200
    probe_time = res.json()["timestamp"]
    assert abs(now - probe_time) < 5.0


def test_readiness_probe_version_field() -> None:
    """Test readiness probe contains version string matching environment."""
    expected_ver = os.getenv("APP_VERSION", "1.0.0")
    res = client.get("/healthz/ready")
    assert res.status_code == 200
    assert res.json()["version"] == expected_ver


def test_metrics_tracks_exact_request_count() -> None:
    """Test each HTTP request increments metric counter by 1."""
    key = 'path="/healthz/live",status="200"'
    initial_count = request_counts.get(key, 0)

    for _ in range(5):
        client.get("/healthz/live")

    assert request_counts[key] == initial_count + 5


def test_metrics_tracks_status_codes_and_404() -> None:
    """Test 404 Not Found requests are tracked in metrics counter."""
    client.get("/nonexistent/route")
    res = client.get("/metrics")
    assert res.status_code == 200
    assert 'status="404"' in res.text


def test_metrics_content_type_plain_text() -> None:
    """Test /metrics endpoint returns text/plain content type."""
    res = client.get("/metrics")
    assert "text/plain" in res.headers["content-type"]


def test_metrics_latency_duration_counters() -> None:
    """Test duration metrics summary contains both count and sum lines."""
    client.get("/healthz/live")
    res = client.get("/metrics")
    assert 'http_request_duration_seconds_count{path="/healthz/live"}' in res.text
    assert 'http_request_duration_seconds_sum{path="/healthz/live"}' in res.text


def test_app_title_metadata() -> None:
    """Test application title metadata is correctly configured."""
    assert app.title == "Cloud-Native Production Microservice"


def test_metrics_endpoint_itself_is_tracked() -> None:
    """Test requesting /metrics records a counter for /metrics."""
    client.get("/metrics")
    assert any('path="/metrics"' in k for k in request_counts)
