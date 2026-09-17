"""Comprehensive Test Suite for the Master Capstone Platform.

Includes unit tests across all subsystems (Auth, Task Broker, Analytics, Models)
and End-to-End integration tests marked with @pytest.mark.capstone.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
import polars as pl
import pytest
from fastapi.testclient import TestClient

from capstone_platform.analytics import CapstoneAnalytics
from capstone_platform.app import app, engine
from capstone_platform.auth import (
    JWT_ALGORITHM,
    JWT_SECRET,
    create_access_token,
    hash_password,
    verify_password,
)
from capstone_platform.models import Base
from capstone_platform.tasks import BackgroundTask, CapstoneTaskBroker


@pytest.fixture(autouse=True)
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# ===========================================================================
# 1. Authentication & Security Subsystem Unit Tests
# ===========================================================================

def test_auth_hash_and_verify_password() -> None:
    raw = "SuperSecretPassphrase123!"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed)
    assert not verify_password("WrongPassword!", hashed)


def test_auth_create_and_decode_jwt_token() -> None:
    token = create_access_token(user_id=42, username="architect", role="admin")
    claims = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert claims["sub"] == "42"
    assert claims["username"] == "architect"
    assert claims["role"] == "admin"


def test_auth_expired_jwt_token_raises_error() -> None:
    expired_payload = {
        "sub": "99",
        "username": "expired_user",
        "role": "viewer",
        "exp": datetime.now(UTC) - timedelta(minutes=5),
    }
    token = jwt.encode(expired_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def test_auth_tampered_jwt_token_raises_error() -> None:
    token = create_access_token(user_id=1, username="test", role="viewer")
    tampered = token[:-4] + "ABCD"
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(tampered, JWT_SECRET, algorithms=[JWT_ALGORITHM])


# ===========================================================================
# 2. Task Broker & DLQ Subsystem Unit Tests
# ===========================================================================

def test_task_broker_enqueue() -> None:
    broker = CapstoneTaskBroker()
    task = broker.enqueue("GenerateReport", {"format": "json"})
    assert isinstance(task, BackgroundTask)
    assert task.status == "PENDING"
    assert task.retries_left == 2
    assert len(broker.queue) == 1


def test_task_broker_process_all_success() -> None:
    broker = CapstoneTaskBroker()
    t1 = broker.enqueue("Task1", {"data": 1})
    t2 = broker.enqueue("Task2", {"data": 2})

    processed = broker.process_all()
    assert processed == 2
    assert len(broker.queue) == 0
    assert len(broker.completed) == 2
    assert t1.task_id in broker.completed
    assert t2.task_id in broker.completed
    assert broker.completed[t1.task_id].status == "SUCCESS"


def test_task_broker_retries_and_dlq() -> None:
    broker = CapstoneTaskBroker()
    failing_task = broker.enqueue("FragileTask", {"should_fail": True})

    # retries_left starts at 2. Total attempts before DLQ: 1 initial + 2 retries = 3
    processed = broker.process_all()
    assert processed == 3
    assert len(broker.queue) == 0
    assert len(broker.dlq) == 1
    assert broker.dlq[0].task_id == failing_task.task_id
    assert broker.dlq[0].status == "DLQ"
    assert "Simulated transient task failure" in str(broker.dlq[0].result)


def test_task_broker_empty_queue_processing() -> None:
    broker = CapstoneTaskBroker()
    assert broker.process_all() == 0


# ===========================================================================
# 3. Analytics Subsystem Unit Tests
# ===========================================================================

def test_analytics_aggregate_project_budgets() -> None:
    data = [
        {"owner": "alice", "name": "P1", "budget": 2000.0},
        {"owner": "bob", "name": "P2", "budget": 2500.0},
        {"owner": "alice", "name": "P3", "budget": 1500.0},
    ]
    df = CapstoneAnalytics.aggregate_project_budgets(data)
    assert isinstance(df, pl.DataFrame)
    assert len(df) == 2
    assert df["owner"][0] == "alice"
    assert df["total_budget"][0] == 3500.0
    assert df["project_count"][0] == 2


def test_analytics_aggregate_empty_dataset() -> None:
    df = CapstoneAnalytics.aggregate_project_budgets([])
    assert isinstance(df, pl.DataFrame)
    assert len(df) == 0
    assert "owner" in df.columns
    assert "total_budget" in df.columns


def test_analytics_rank_projects_duckdb() -> None:
    data = [
        {"owner": "alice", "name": "P_Small", "budget": 1000.0},
        {"owner": "bob", "name": "P_Large", "budget": 5000.0},
        {"owner": "carol", "name": "P_Medium", "budget": 3000.0},
    ]
    ranked = CapstoneAnalytics.rank_projects_duckdb(data)
    assert isinstance(ranked, pl.DataFrame)
    assert "budget_rank" in ranked.columns
    assert ranked["name"][0] == "P_Large"
    assert ranked["budget_rank"][0] == 1


def test_analytics_rank_empty_dataset_duckdb() -> None:
    ranked = CapstoneAnalytics.rank_projects_duckdb([])
    assert isinstance(ranked, pl.DataFrame)
    assert len(ranked) == 0


# ===========================================================================
# 4. End-to-End Integration Tests (Marked with @pytest.mark.capstone)
# ===========================================================================

@pytest.mark.capstone
def test_platform_health_and_metrics() -> None:
    with TestClient(app) as client:
        res_live = client.get("/healthz/live")
        assert res_live.status_code == 200
        assert res_live.json()["status"] == "LIVE"

        res_ready = client.get("/healthz/ready")
        assert res_ready.status_code == 200
        assert res_ready.json()["status"] == "READY"

        metrics_res = client.get("/metrics")
        assert metrics_res.status_code == 200
        assert "http_requests_total" in metrics_res.text


@pytest.mark.capstone
def test_full_auth_and_project_creation_workflow() -> None:
    with TestClient(app) as client:
        # 1. Register User
        reg_data = {
            "username": "lead_architect",
            "email": "lead@platform.io",
            "password": "MasterCapstonePass123!",
        }
        res_reg = client.post("/auth/register", json=reg_data)
        assert res_reg.status_code == 201
        assert res_reg.json()["username"] == "lead_architect"
        # Registration must NOT let the client choose a role.
        assert res_reg.json()["role"] == "viewer"

        # 2. Login to get JWT
        login_res = client.post("/auth/login", data={"username": "lead_architect", "password": "MasterCapstonePass123!"})
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Create Project with JWT Auth
        proj_data = {"name": "NextGen Distributed Platform", "budget": 250000.0}
        res_proj = client.post("/projects", json=proj_data, headers=headers)
        assert res_proj.status_code == 201
        assert res_proj.json()["name"] == "NextGen Distributed Platform"
        assert res_proj.json()["budget"] == 250000.0

        # 4. Enqueue Background Task
        res_task = client.post("/tasks/enqueue?task_name=GenerateExecutiveAudit", json={"format": "pdf"}, headers=headers)
        assert res_task.status_code == 200
        assert res_task.json()["status"] == "PENDING"

        # 5. Polars Analytics Summary
        res_analytics = client.get("/analytics/summary")
        assert res_analytics.status_code == 200
        data = res_analytics.json()
        assert len(data) >= 2
        assert data[0]["owner"] == "bob"
        assert data[0]["total_budget"] == 120000.0


@pytest.mark.capstone
def test_unauthenticated_project_creation_rejected() -> None:
    """Integration Test: Protected routes reject requests without bearer token."""
    with TestClient(app) as client:
        res = client.post("/projects", json={"name": "Rogue Project", "budget": 1000.0})
        assert res.status_code == 401


@pytest.mark.capstone
def test_unauthenticated_task_enqueue_rejected() -> None:
    """Integration Test: Task queuing requires authenticated token."""
    with TestClient(app) as client:
        res = client.post("/tasks/enqueue?task_name=Test", json={})
        assert res.status_code == 401


@pytest.mark.capstone
def test_telemetry_correlation_id_propagation() -> None:
    """Integration Test: Custom correlation ID flows into response header."""
    custom_id = "capstone-audit-trace-888"
    with TestClient(app) as client:
        res = client.get("/healthz/live", headers={"X-Correlation-ID": custom_id})
        assert res.status_code == 200
        assert res.headers.get("X-Correlation-ID") == custom_id
        assert "X-Process-Time-Ms" in res.headers
