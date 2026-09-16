#!/usr/bin/env python3
"""Unified Enterprise Distributed Microservice Platform Gateway.

Module 24 (Master Capstone Project) Turnkey Implementation.
Unites FastAPI, Pydantic V2, Bcrypt, PyJWT, SQLAlchemy 2.0 Async,
Distributed Task Queue, Polars/DuckDB Analytics, and Prometheus Telemetry.
"""

from __future__ import annotations

import time
import uuid
from collections import defaultdict
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from capstone_platform.analytics import CapstoneAnalytics
from capstone_platform.auth import (
    RoleUpdateSchema,
    TokenResponse,
    UserRegisterSchema,
    create_access_token,
    get_current_user_claims,
    hash_password,
    verify_password,
)
from capstone_platform.models import Base, ProjectModel, UserModel
from capstone_platform.tasks import CapstoneTaskBroker

# ==========================================
# 1. Database & Broker Initialization
# ==========================================

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
session_factory = async_sessionmaker(engine, expire_on_commit=False)
task_broker = CapstoneTaskBroker()

# Telemetry metrics storage
metrics_counter: dict[str, int] = defaultdict(int)


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]:
    # Setup tables on boot
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="Enterprise Distributed Microservice Platform",
    version="1.0.0",
    lifespan=lifespan,
)


# ==========================================
# 2. Telemetry & Correlation ID Middleware
# ==========================================

@app.middleware("http")
async def telemetry_middleware(request: Request, call_next) -> Response:
    corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    start = time.perf_counter()

    response: Response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Correlation-ID"] = corr_id
    response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"

    key = f'path="{request.url.path}",status="{response.status_code}"'
    metrics_counter[key] += 1
    return response


# ==========================================
# 3. Database Dependency
# ==========================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


# ==========================================
# 4. Pydantic Schemas
# ==========================================

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    budget: float = Field(..., gt=0.0)


class ProjectResponse(ProjectCreate):
    id: int
    owner_id: int


# ==========================================
# 5. Core Platform Endpoints
# ==========================================

@app.get("/healthz/live")
def liveness() -> dict[str, object]:
    return {"status": "LIVE", "timestamp": time.time()}


@app.get("/healthz/ready")
def readiness() -> dict[str, object]:
    return {"status": "READY", "db": "CONNECTED", "broker": "ACTIVE"}


@app.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics() -> str:
    lines = ["# TYPE http_requests_total counter"]
    for key, val in metrics_counter.items():
        lines.append(f"http_requests_total{{{key}}} {val}")
    return "\n".join(lines) + "\n"


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterSchema, db: AsyncSession = Depends(get_db)) -> dict[str, object]:
    stmt = select(UserModel).where(UserModel.username == payload.username)
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    new_user = UserModel(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="viewer",   # server-assigned; never client-supplied
    )
    db.add(new_user)
    await db.commit()
    return {"id": new_user.id, "username": new_user.username, "role": new_user.role}


@app.post("/auth/login", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)) -> TokenResponse:
    stmt = select(UserModel).where(UserModel.username == form_data.username)
    user = (await db.execute(stmt)).scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token(user.id, user.username, user.role)
    return TokenResponse(access_token=token)


@app.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    claims: dict = Depends(get_current_user_claims),
    db: AsyncSession = Depends(get_db),
) -> ProjectResponse:
    user_id = int(claims["sub"])
    project = ProjectModel(name=payload.name, budget=payload.budget, owner_id=user_id)
    db.add(project)
    await db.commit()
    return ProjectResponse(id=project.id, name=project.name, budget=project.budget, owner_id=project.owner_id)


@app.post("/tasks/enqueue")
def enqueue_task(task_name: str, payload: dict, claims: dict = Depends(get_current_user_claims)) -> dict[str, str]:
    task = task_broker.enqueue(task_name, payload)
    return {"task_id": task.task_id, "status": task.status}


@app.get("/analytics/summary")
def get_analytics_summary() -> list[dict]:
    # In-memory analytics mock dataset
    data = [
        {"owner": "alice", "name": "App Redesign", "budget": 50000.0},
        {"owner": "bob", "name": "Cloud Migration", "budget": 120000.0},
        {"owner": "alice", "name": "Security Audit", "budget": 30000.0},
    ]
    summary_df = CapstoneAnalytics.aggregate_project_budgets(data)
    return summary_df.to_dicts()


# ---------------------------------------------------------------------------
# Admin-only role management
# ---------------------------------------------------------------------------
# Privilege changes live behind an explicit authorisation check on a separate
# endpoint with its own input model. Registration cannot reach this code path,
# which is what makes self-promotion impossible rather than merely discouraged.


def require_role(*allowed: str):
    """Dependency factory enforcing role-based access control.

    Authentication (`get_current_user_claims`) proves *who* you are. This proves
    *what you may do*. Conflating the two is the IDOR / broken-object-level-
    authorisation family of bugs (Module 16, diagnostic D4).
    """

    def _check(claims: dict = Depends(get_current_user_claims)) -> dict:
        if claims.get("role") not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"requires one of: {', '.join(sorted(allowed))}",
            )
        return claims

    return _check


@app.patch("/admin/users/{user_id}/role", status_code=status.HTTP_200_OK)
async def set_user_role(
    user_id: int,
    payload: RoleUpdateSchema,
    claims: dict = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
) -> dict[str, object]:
    """Promote or demote a user. Admin only."""
    user = (
        await db.execute(select(UserModel).where(UserModel.id == user_id))
    ).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    user.role = payload.role
    await db.commit()
    return {"id": user.id, "username": user.username, "role": user.role}
