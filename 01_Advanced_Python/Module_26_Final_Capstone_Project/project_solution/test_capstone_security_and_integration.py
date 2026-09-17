"""Capstone suite, part 2: persistence, RBAC, security, and cross-subsystem flows.

`test_capstone.py` covers each subsystem in isolation. This file covers the two
things a capstone exists to verify and unit tests cannot:

1. **Security properties** — that the platform refuses what it should refuse.
   Two of these tests were written after finding real defects in this codebase:
   client-settable `role` on registration (privilege escalation) and a
   hard-coded JWT signing key.
2. **Integration** — that subsystems compose correctly. A bug that only appears
   when auth, persistence and the task queue interact is exactly what unit
   tests miss by construction.

Run:  pytest -m capstone -v
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator

import jwt
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from capstone_platform.analytics import CapstoneAnalytics
from capstone_platform.app import app, engine
from capstone_platform.auth import (
    JWT_ALGORITHM,
    JWT_SECRET,
    RoleUpdateSchema,
    UserRegisterSchema,
    create_access_token,
    hash_password,
    verify_password,
)
from capstone_platform.models import Base, ProjectModel, UserModel
from capstone_platform.tasks import CapstoneTaskBroker

pytestmark = pytest.mark.capstone

COUNTER = {"n": 0}


def unique(prefix: str) -> str:
    """Unique identifier so tests never collide on the unique username index."""
    COUNTER["n"] += 1
    return f"{prefix}_{COUNTER['n']}"


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as c:
        yield c


def register(client: TestClient, username: str, password: str = "ValidPassw0rd!") -> dict:
    res = client.post(
        "/auth/register",
        json={"username": username, "email": f"{username}@platform.io", "password": password},
    )
    assert res.status_code == 201, res.text
    return res.json()


def login(client: TestClient, username: str, password: str = "ValidPassw0rd!") -> dict[str, str]:
    res = client.post("/auth/login", data={"username": username, "password": password})
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


# ===========================================================================
# 1. SECURITY — the platform must refuse these
# ===========================================================================


def test_registration_rejects_client_supplied_role() -> None:
    """Privilege escalation via mass assignment. This was a real defect here.

    A registration model that accepts `role` lets any anonymous caller create an
    administrator. The field is now absent and `extra="forbid"` rejects it.
    """
    with pytest.raises(ValidationError):
        UserRegisterSchema(
            username="attacker",
            email="a@b.co",
            password="Passw0rd123!",
            role="admin",  # type: ignore[call-arg]
        )


def test_registration_endpoint_ignores_role_field(client: TestClient) -> None:
    """The same defence at the HTTP boundary, not just the model."""
    res = client.post(
        "/auth/register",
        json={
            "username": unique("sneaky"),
            "email": "sneaky@platform.io",
            "password": "ValidPassw0rd!",
            "role": "admin",
        },
    )
    assert res.status_code == 422, "an unexpected field must be rejected, not ignored"


def test_new_accounts_are_always_viewers(client: TestClient) -> None:
    body = register(client, unique("newbie"))
    assert body["role"] == "viewer"


def test_jwt_secret_is_not_hardcoded_for_production() -> None:
    """A signing key in source is in every clone, every CI log and every backup."""
    assert "CAPSTONE_JWT_SECRET" in os.environ or JWT_SECRET.startswith("dev-only"), (
        "the default secret must be an obvious development placeholder"
    )


def test_token_signed_with_another_secret_is_rejected(client: TestClient) -> None:
    """Signature verification must actually happen."""
    forged = jwt.encode(
        {"sub": "1", "username": "attacker", "role": "admin", "exp": 9_999_999_999},
        "a-different-secret-that-is-at-least-32-bytes-long",
        algorithm=JWT_ALGORITHM,
    )
    res = client.post(
        "/projects",
        json={"name": "forged", "budget": 1.0},
        headers={"Authorization": f"Bearer {forged}"},
    )
    assert res.status_code == 401


def test_unsigned_alg_none_token_is_rejected(client: TestClient) -> None:
    """The classic JWT attack: claim `alg: none` and supply no signature."""
    unsigned = jwt.encode(
        {"sub": "1", "username": "attacker", "role": "admin", "exp": 9_999_999_999},
        key="",
        algorithm="none",
    )
    res = client.post(
        "/projects",
        json={"name": "unsigned", "budget": 1.0},
        headers={"Authorization": f"Bearer {unsigned}"},
    )
    assert res.status_code == 401


def test_malformed_authorization_header_is_rejected(client: TestClient) -> None:
    for header in ("Bearer", "Bearer ", "Basic abc123", "not-a-header", "Bearer a.b.c"):
        res = client.post(
            "/projects", json={"name": "x", "budget": 1.0}, headers={"Authorization": header}
        )
        assert res.status_code == 401, f"accepted malformed header: {header!r}"


def test_password_is_never_returned(client: TestClient) -> None:
    """No response may contain the password or its hash."""
    body = register(client, unique("private"))
    serialised = str(body).lower()
    assert "password" not in serialised
    assert "$2b$" not in serialised


def test_bcrypt_hash_is_salted(client: TestClient) -> None:
    """Identical passwords must not produce identical hashes."""
    a = hash_password("SamePassword123!")
    b = hash_password("SamePassword123!")
    assert a != b
    assert verify_password("SamePassword123!", a)
    assert verify_password("SamePassword123!", b)


def test_short_password_rejected(client: TestClient) -> None:
    res = client.post(
        "/auth/register",
        json={"username": unique("weak"), "email": "w@platform.io", "password": "short"},
    )
    assert res.status_code == 422


def test_duplicate_username_conflicts(client: TestClient) -> None:
    name = unique("dup")
    register(client, name)
    res = client.post(
        "/auth/register",
        json={"username": name, "email": "other@platform.io", "password": "ValidPassw0rd!"},
    )
    assert res.status_code == 409


def test_login_with_wrong_password_fails(client: TestClient) -> None:
    name = unique("wrongpw")
    register(client, name)
    res = client.post("/auth/login", data={"username": name, "password": "NotThePassword!"})
    assert res.status_code == 401


def test_login_for_unknown_user_fails(client: TestClient) -> None:
    res = client.post("/auth/login", data={"username": "ghost_user", "password": "whatever123"})
    assert res.status_code == 401


# ===========================================================================
# 2. RBAC — authentication is not authorisation
# ===========================================================================


def test_viewer_cannot_change_roles(client: TestClient) -> None:
    name = unique("viewer")
    body = register(client, name)
    headers = login(client, name)
    res = client.patch(f"/admin/users/{body['id']}/role", json={"role": "admin"}, headers=headers)
    assert res.status_code == 403, "a viewer must not be able to promote anyone, including itself"


def test_admin_can_change_roles(client: TestClient) -> None:
    target = register(client, unique("target"))
    admin_name = unique("admin")
    admin = register(client, admin_name)

    # Promote out-of-band, as a real deployment would seed its first admin.
    async def _promote() -> None:
        maker = async_sessionmaker(engine, expire_on_commit=False)
        async with maker() as session:
            user = (
                await session.execute(select(UserModel).where(UserModel.id == admin["id"]))
            ).scalar_one()
            user.role = "admin"
            await session.commit()

    asyncio.run(_promote())

    headers = login(client, admin_name)
    res = client.patch(f"/admin/users/{target['id']}/role", json={"role": "manager"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["role"] == "manager"


def test_role_update_rejects_invalid_role() -> None:
    with pytest.raises(ValidationError):
        RoleUpdateSchema(role="superuser")


def test_role_update_requires_authentication(client: TestClient) -> None:
    assert client.patch("/admin/users/1/role", json={"role": "admin"}).status_code == 401


# ===========================================================================
# 3. PERSISTENCE — the layer test_capstone.py does not touch
# ===========================================================================


@pytest.fixture
def session_maker() -> async_sessionmaker[AsyncSession]:
    async def _init() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_init())
    return async_sessionmaker(engine, expire_on_commit=False)


def test_username_uniqueness_enforced_by_the_database(
    session_maker: async_sessionmaker[AsyncSession],
) -> None:
    """Application checks can race; the unique index is the real guarantee."""
    name = unique("dbunique")

    async def _run() -> None:
        async with session_maker() as session:
            session.add(
                UserModel(
                    username=name, email=f"{name}@a.co", hashed_password="x", role="viewer"
                )
            )
            await session.commit()
        async with session_maker() as session:
            session.add(
                UserModel(
                    username=name, email=f"{name}_2@a.co", hashed_password="x", role="viewer"
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()

    asyncio.run(_run())


def test_project_requires_a_valid_owner(
    session_maker: async_sessionmaker[AsyncSession],
) -> None:
    """A foreign key that is not enforced is a comment."""

    async def _run() -> None:
        async with session_maker() as session:
            await session.execute(__import__("sqlalchemy").text("PRAGMA foreign_keys=ON"))
            session.add(ProjectModel(name="orphan", budget=1.0, owner_id=999_999))
            with pytest.raises(IntegrityError):
                await session.commit()

    asyncio.run(_run())


def test_deleting_a_user_cascades_to_projects(
    session_maker: async_sessionmaker[AsyncSession],
) -> None:
    """`cascade='all, delete-orphan'` must actually remove the children."""
    name = unique("cascade")

    async def _run() -> None:
        async with session_maker() as session:
            user = UserModel(
                username=name, email=f"{name}@a.co", hashed_password="x", role="viewer"
            )
            user.projects.append(ProjectModel(name="child-a", budget=10.0))
            user.projects.append(ProjectModel(name="child-b", budget=20.0))
            session.add(user)
            await session.commit()
            user_id = user.id

        async with session_maker() as session:
            user = (
                await session.execute(
                    select(UserModel)
                    .where(UserModel.id == user_id)
                    .options(selectinload(UserModel.projects))
                )
            ).scalar_one()
            assert len(user.projects) == 2
            await session.delete(user)
            await session.commit()

        async with session_maker() as session:
            remaining = (
                await session.execute(
                    select(ProjectModel).where(ProjectModel.owner_id == user_id)
                )
            ).scalars().all()
            assert remaining == []

    asyncio.run(_run())


def test_selectinload_avoids_the_n_plus_one(
    session_maker: async_sessionmaker[AsyncSession],
) -> None:
    """Eager loading must make the relationship available outside the session.

    Without `selectinload`, touching `user.projects` after the session closes
    raises — which is the symptom that reveals a lazy load, and in a request
    handler would be an N+1 query instead.
    """
    name = unique("eager")

    async def _run() -> list[str]:
        async with session_maker() as session:
            user = UserModel(
                username=name, email=f"{name}@a.co", hashed_password="x", role="viewer"
            )
            user.projects.append(ProjectModel(name="p1", budget=1.0))
            session.add(user)
            await session.commit()
            user_id = user.id

        async with session_maker() as session:
            loaded = (
                await session.execute(
                    select(UserModel)
                    .where(UserModel.id == user_id)
                    .options(selectinload(UserModel.projects))
                )
            ).scalar_one()
        return [p.name for p in loaded.projects]  # session is closed here

    assert asyncio.run(_run()) == ["p1"]


# ===========================================================================
# 4. TASK QUEUE — properties the isolated tests do not assert
# ===========================================================================


def test_broker_assigns_unique_task_ids() -> None:
    broker = CapstoneTaskBroker()
    ids = {broker.enqueue("report", {"i": i}).task_id for i in range(50)}
    assert len(ids) == 50


def test_broker_preserves_fifo_order() -> None:
    broker = CapstoneTaskBroker()
    for i in range(5):
        broker.enqueue("ordered", {"i": i})
    assert [t.payload["i"] for t in broker.queue] == [0, 1, 2, 3, 4]


def test_dlq_retains_the_failure_reason() -> None:
    """A dead-letter entry with no diagnosis is a lost message."""
    broker = CapstoneTaskBroker()
    broker.enqueue("POISON", {"should_fail": True})
    broker.process_all()
    assert broker.dlq, "a permanently failing task must reach the DLQ"
    dead = broker.dlq[0]
    assert dead.status == "DLQ"
    assert dead.result, "a dead-letter entry with no diagnosis is a lost message"
    assert dead.retries_left == 0, "it must exhaust its retries before being dead-lettered"


# ===========================================================================
# 5. ANALYTICS — edge cases
# ===========================================================================


def test_analytics_handles_a_single_owner() -> None:
    frame = CapstoneAnalytics.aggregate_project_budgets(
        [{"owner": "solo", "name": "only", "budget": 42.0}]
    )
    assert frame.height == 1


def test_analytics_sums_rather_than_counts() -> None:
    frame = CapstoneAnalytics.aggregate_project_budgets(
        [
            {"owner": "ada", "name": "a", "budget": 100.0},
            {"owner": "ada", "name": "b", "budget": 250.0},
        ]
    )
    row = frame.to_dicts()[0]
    assert any(abs(float(v) - 350.0) < 1e-6 for v in row.values() if isinstance(v, (int, float)))


def test_analytics_tolerates_zero_budgets() -> None:
    frame = CapstoneAnalytics.aggregate_project_budgets(
        [{"owner": "ada", "name": "free", "budget": 0.0}]
    )
    assert frame.height == 1


# ===========================================================================
# 6. OBSERVABILITY
# ===========================================================================


def test_liveness_and_readiness_are_distinct_endpoints(client: TestClient) -> None:
    """Liveness says 'restart me'; readiness says 'send me traffic'. Not the same."""
    assert client.get("/healthz/live").status_code == 200
    assert client.get("/healthz/ready").status_code == 200


def test_metrics_exposes_prometheus_text_format(client: TestClient) -> None:
    client.get("/healthz/live")
    body = client.get("/metrics").text
    assert "# HELP" in body or "# TYPE" in body, "must be Prometheus exposition format"


def test_correlation_id_is_echoed_back(client: TestClient) -> None:
    supplied = "trace-capstone-abc123"
    res = client.get("/healthz/live", headers={"X-Correlation-ID": supplied})
    assert res.headers.get("X-Correlation-ID") == supplied


def test_correlation_id_generated_when_absent(client: TestClient) -> None:
    res = client.get("/healthz/live")
    assert res.headers.get("X-Correlation-ID")


# ===========================================================================
# 7. CROSS-SUBSYSTEM INTEGRATION
# ===========================================================================


def test_end_to_end_register_login_create_enqueue_analytics(client: TestClient) -> None:
    """One flow crossing auth, persistence, the task queue and analytics."""
    name = unique("e2e")
    register(client, name)
    headers = login(client, name)

    created = client.post("/projects", json={"name": "E2E Platform", "budget": 90000.0}, headers=headers)
    assert created.status_code == 201

    queued = client.post(
        "/tasks/enqueue?task_name=E2EAudit", json={"format": "pdf"}, headers=headers
    )
    assert queued.status_code == 200
    assert queued.json()["task_id"]

    summary = client.get("/analytics/summary")
    assert summary.status_code == 200
    assert isinstance(summary.json(), list)


def test_project_is_attributed_to_its_creator(client: TestClient) -> None:
    """Two users must not see their projects merged."""
    a, b = unique("owner_a"), unique("owner_b")
    ua, ub = register(client, a), register(client, b)
    client.post("/projects", json={"name": "A-proj", "budget": 1.0}, headers=login(client, a))
    client.post("/projects", json={"name": "B-proj", "budget": 2.0}, headers=login(client, b))

    async def _owners() -> dict[str, int]:
        maker = async_sessionmaker(engine, expire_on_commit=False)
        async with maker() as session:
            rows = (
                await session.execute(
                    select(ProjectModel).where(ProjectModel.name.in_(["A-proj", "B-proj"]))
                )
            ).scalars().all()
            return {p.name: p.owner_id for p in rows}

    owners = asyncio.run(_owners())
    assert owners["A-proj"] == ua["id"]
    assert owners["B-proj"] == ub["id"]


def test_expired_token_rejected_end_to_end(client: TestClient) -> None:
    """A token past its `exp` must not work, however well-formed it is."""
    expired = jwt.encode(
        {"sub": "1", "username": "ghost", "role": "admin", "exp": 1_000_000_000},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    res = client.post(
        "/projects",
        json={"name": "expired", "budget": 1.0},
        headers={"Authorization": f"Bearer {expired}"},
    )
    assert res.status_code == 401


def test_project_validation_rejects_bad_input(client: TestClient) -> None:
    name = unique("validate")
    register(client, name)
    headers = login(client, name)
    for payload in ({"name": "", "budget": 1.0}, {"name": "ok"}, {"budget": "not-a-number"}):
        res = client.post("/projects", json=payload, headers=headers)
        assert res.status_code == 422, f"accepted invalid project payload: {payload}"


def test_token_carries_the_role_claim() -> None:
    token = create_access_token(user_id=7, username="claims", role="manager")
    decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert decoded["role"] == "manager"
    assert decoded["username"] == "claims"
    assert "exp" in decoded
