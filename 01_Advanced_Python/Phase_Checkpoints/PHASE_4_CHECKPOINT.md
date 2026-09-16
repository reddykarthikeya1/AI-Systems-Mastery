# Phase 4 Checkpoint Exam: Enterprise Backend Microservices

> **Phase Scope:** Modules 13–18 (FastAPI, Pydantic V2, SQLAlchemy 2.0, Security, WebSockets, Distributed Systems)  
> **Allocated Time:** 120 Minutes  
> **Format:** Full-stack backend service implementation and verification.

---

## 🎯 The Exam Mission: Multi-Tenant Enterprise Microservice

Architect an enterprise-ready customer order microservice with async database persistence, multi-tenant RBAC token authentication, real-time WebSocket notifications, and an idempotent distributed task consumer.

---

## 📋 Functional Requirements

### 1. API Gateway & Validation (`app.py`, `schemas.py`)
- FastAPI ASGI application with structured error responses.
- Pydantic V2 schemas with `@field_validator`, `@model_validator`, and `@computed_field`.
- Strict type validation: zero `Any` escape hatches.

### 2. Async Persistence & Relational Schema (`models.py`)
- SQLAlchemy 2.0 async engine with `Mapped` and `mapped_column`.
- Relational schema: `Customer` 1-to-N `Order` 1-to-N `OrderItem`.
- Eager loading using `selectinload` to prevent N+1 query traps.

### 3. Security & RBAC Guard
- Password hashing with salted Bcrypt.
- PyJWT token issuance with strict `exp` verification and `sub` subject claims.
- Role-based authorization: `admin`, `manager`, `viewer`.

### 4. Real-Time WebSockets & Idempotent Broker
- Room-based WebSocket channel notifying managers of placed orders.
- Task handler ensuring duplicate deliveries are safely ignored.

---

## 📊 Grading Rubric (100 Points Total)

| Requirement | Criteria | Points |
| :--- | :--- | :--- |
| **REST & Validation** | Clean OpenAPI schema, Pydantic V2 validators, correct HTTP status codes | 25 pts |
| **Async ORM & Transactions** | SQLAlchemy 2.0 async sessions, atomic order placement, eager loading | 25 pts |
| **Security & RBAC** | Bcrypt hashing, JWT expiration validation, role guard dependencies | 25 pts |
| **Real-time & Distributed** | WebSockets connection manager, idempotent message handling | 25 pts |

**Passing Threshold:** 85/100 points required to advance to Phase 5.

---

## 🚦 Pre-Flight Gate

**Do not start this exam until all of the following pass.** Attempting a
checkpoint on a foundation that does not build wastes the exam — you will spend
your time debugging setup instead of demonstrating skill.

```bash
# From the course root. All must be green.
pytest Module_13_FastAPI_ASGI_Architecture \
      Module_14_Pydantic_V2_Validation_Routing \
      Module_15_SQLAlchemy_Alembic_Database \
      Module_16_Authentication_Authorization_Security \
      Module_17_Advanced_FastAPI_WebSockets_DI \
      Module_18_Distributed_Systems_Task_Queues_Streaming \
      -q

python tools/check_links.py --quiet
ruff check .
```

If any of that is red, fix it first. The exam assumes a working environment.

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer. When it ends, stop and submit what you have. |
| **No solution exists** | There is deliberately no reference implementation for this exam. The rubric is the specification. |
| **Modules are open-book** | Re-read any README, demo or troubleshooting guide. That is not cheating; it is what the job looks like. |
| **`project_solution/` is closed-book** | Do not read the module solutions during the exam. Copying them measures nothing. |
| **Write your own tests** | Untested code scores zero on the correctness criteria, however elegant it looks. |
| **Working beats complete** | A subset that runs and is tested outscores a full implementation that does not import. |

---

## 🔬 Self-Verification Harness

Produce this evidence before you score yourself. An unmeasured claim earns no
points.

```bash
# 1. It imports and runs at all
python -m your_solution            # must not traceback

# 2. Your tests pass
pytest your_tests.py -v            # paste the summary line

# 3. It is clean
ruff check .
mypy --strict your_solution.py     # advisory, but note the count

# 4. Coverage of your own code
pytest --cov=your_solution --cov-report=term-missing
```

Record the four outputs. The rubric below is scored against **evidence**, not
against intent.

---

## ⏱️ If You Run Out of Time

Score what exists and be honest about the gap. Partial credit is real:

1. **Submit the working subset.** Delete or clearly comment out anything that
   does not run — a broken import costs you every point in the file.
2. **Write down what is missing**, in one line per requirement. Naming your own
   gap accurately is itself a senior skill and earns the analysis criteria.
3. **Keep your tests.** Tests for the parts you finished are worth more than
   untested code for the parts you did not.

---

## 🔁 If You Score Below the Threshold

This is diagnostic information, not a verdict. Do exactly this:

1. Identify which **rubric row** you lost the most points on.
2. Go back to: **Module 16's authorisation material and Module 15's session lifecycle**.
3. Work that module's `debug_lab/` — it drills the failure modes this exam
   punishes.
4. Re-take the exam with a different data set or a changed requirement so you
   are re-solving rather than remembering.

Re-taking a checkpoint is normal. Advancing past one you failed is not — every
later phase assumes this one.

---

## 🎓 What This Checkpoint Actually Measures

Modules 13–18 taught you a set of tools. This exam tests **whether you can build an API that is correct, validated and safe to expose to the internet**.

That is deliberately different from the module quizzes, which test whether you
understood each piece. Here nobody tells you which tool to reach for. Choosing
correctly, under a time limit, with no solution to check against, is the whole
point — and it is the closest this course gets to the actual job.
