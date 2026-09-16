# Module 17: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Advanced FastAPI, Dependency Injection, Middleware, and WebSockets before moving to **Module 16**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Dependency Graphs:** How does FastAPI construct and resolve sub-dependencies in a request dependency graph?
2. **Yield Lifecycle:** What exact moments in request execution correspond to code *before* vs *after* the `yield` statement in a dependency?
3. **ASGI Middleware Pipeline:** Describe the journey of an HTTP request through custom ASGI middleware to the route endpoint and back.
4. **Distributed Telemetry:** What is the purpose of injecting an `X-Correlation-ID` header into every request and response?
5. **Protocol Upgrade:** How does an HTTP connection upgrade into a bidirectional persistent WebSocket connection?
6. **Socket Disconnections:** What exception is raised when a WebSocket client closes its connection, and why must you catch it?
7. **Connection Managers:** How does an in-memory `ConnectionManager` broadcast JSON messages to thousands of connected browser tabs?
8. **Background Execution:** When should you use FastAPI's built-in `BackgroundTasks` vs a distributed worker queue like Celery or ARQ?
9. **Streaming File Uploads:** What is the difference between `bytes` and `UploadFile` when receiving large file uploads in FastAPI?
10. **WebSocket Testing:** How does Starlette's `TestClient.websocket_connect` simulate real-time WebSocket communication in unit tests?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
FastAPI builds a Directed Acyclic Graph (DAG) of dependencies, evaluating shared sub-dependencies once per request (unless `use_cache=False` is set) and injecting resolved values into dependent functions.

#### Answer 2:
- Code **before** `yield`: Executes during request setup before the route handler is invoked.
- Code **after** `yield`: Executes during response teardown after the route handler finishes, even if an unhandled error occurred.

#### Answer 3:
Incoming bytes pass through each middleware layer in outer-to-inner order, execute the endpoint, and the resulting `Response` flows back through the layers in reverse (inner-to-outer) order.

#### Answer 4:
It provides a single unique trace ID that follows a request across multiple microservices, message queues, and logs, making distributed debugging possible.

#### Answer 5:
The client sends an HTTP `GET` request with `Upgrade: websocket` and `Connection: Upgrade` headers. If accepted (`101 Switching Protocols`), the socket switches from HTTP request-response mode to raw bidirectional framing.

#### Answer 6:
**`starlette.websockets.WebSocketDisconnect`**. Catching it allows removing the dead socket from active broadcast lists, preventing memory leaks and closed-socket write errors.

#### Answer 7:
It maintains a list or set of active `WebSocket` objects and iterates through them with `await ws.send_json(data)` inside an async loop.

#### Answer 8:
- `BackgroundTasks`: In-process background tasks that run after response return (ideal for simple emails or audit logs).
- `Celery / ARQ`: Distributed out-of-process queues backed by Redis/RabbitMQ (essential for heavy CPU tasks, video processing, or guaranteed retry jobs).

#### Answer 9:
- `bytes`: Reads the entire file into RAM at once (crashes server on 1 GB files).
- `UploadFile`: Streams data into a temporary spool file on disk using minimal RAM.

#### Answer 10:
`client.websocket_connect("/path")` returns a context manager that connects to the ASGI WebSocket handler and allows calling `.send_text()` and `.receive_text()`.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Custom Server Timing Header Middleware

**Goal:** Create a FastAPI middleware that measures endpoint execution time and appends a `Server-Timing: app;dur=12.5` HTTP header.

<details>
<summary><b>Solution Code</b></summary>

```python
import time
from fastapi import FastAPI, Request, Response
from starlette.testclient import TestClient

app = FastAPI()

@app.middleware("http")
async def server_timing_middleware(request: Request, call_next) -> Response:
    start = time.perf_counter()
    response: Response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["Server-Timing"] = f"app;dur={elapsed_ms:.2f}"
    return response

@app.get("/hello")
def hello(): return {"message": "world"}

# Verification:
client = TestClient(app)
res = client.get("/hello")
print("Server-Timing Header:", res.headers.get("Server-Timing"))
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. WebSocket disconnect leaks the connection

```python
active: list[WebSocket] = []

@app.websocket("/ws")
async def endpoint(ws: WebSocket) -> None:
    await ws.accept()
    active.append(ws)
    while True:
        msg = await ws.receive_text()
        for peer in active:
            await peer.send_text(msg)
```

**Observed symptom:** After clients disconnect, `active` keeps growing and every broadcast raises `RuntimeError: Cannot call "send" once a close message has been sent`.

**(a)** Why is the socket never removed from `active`?

**(b)** What is the correct structure?

**(c)** Why is iterating `active` while sending also unsafe?

<details>
<summary><b>Show the diagnosis</b></summary>

When the client disconnects, `receive_text()` raises `WebSocketDisconnect`, which propagates out of the handler — so the `active.remove(ws)` that should follow never runs.

**Correct:**

```python
try:
    while True:
        msg = await ws.receive_text()
        await manager.broadcast(msg)
except WebSocketDisconnect:
    pass
finally:
    manager.disconnect(ws)
```

A `finally` (or a connection-manager context manager) is what guarantees removal on **every** exit path.

**Iterating while sending** is unsafe twice over: a dead peer raises mid-loop and aborts the broadcast to everyone after it, and a concurrent connect/disconnect mutates the list during iteration. Iterate over a copy, collect the failures, and remove them afterwards.

</details>

---

### D2. Dependency with yield and an exception

```python
async def get_conn():
    conn = await pool.acquire()
    yield conn
    await pool.release(conn)
```

**Observed symptom:** Under load the pool is exhausted. Connections are never returned when a route raises.

**(a)** Why is the connection not released when the route raises?

**(b)** What is the fix?

**(c)** What changed in FastAPI about exceptions in yield-dependencies?

<details>
<summary><b>Show the diagnosis</b></summary>

If the route body raises, the exception is thrown *into* the generator at the `yield`. Without a `try/finally` the code after `yield` never executes and the connection is lost.

**Fix:**

```python
async def get_conn():
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)
```

This is the same rule as any generator-based context manager: cleanup belongs in `finally`, never merely after the `yield`.

**What changed:** FastAPI now runs yield-dependency teardown *after* the response is sent and re-raises exceptions from the dependency in a way that reaches your exception handlers. Earlier versions could swallow them. Either way the `finally` is required — do not depend on framework behaviour for resource safety.

</details>

---

### D3. Middleware that consumes the body

```
@app.middleware("http")
async def log_body(request: Request, call_next):
    body = await request.body()
    logger.info("body=%s", body)
    return await call_next(request)
```

**Observed symptom:** Every POST route receives an empty body and returns 422.

**(a)** Why is the body empty by the time the route runs?

**(b)** What are two ways to log the body safely?

**(c)** What is the risk in the more convenient of those two?

<details>
<summary><b>Show the diagnosis</b></summary>

The request body is an **async stream** that can be consumed once. `await request.body()` drains it; the route's attempt to read it finds nothing.

**Two safe approaches:** (1) re-inject the consumed bytes by replacing the `receive` callable so downstream sees the stream again; (2) do not read it in middleware — log inside the route, or use a `route_class` that has already parsed it.

**The risk in re-injection** is memory: you must buffer the *entire* body, so a 500 MB upload becomes 500 MB of RAM per concurrent request, and it is a trivial denial-of-service vector. If you must log bodies, cap the size you buffer and skip streaming content types entirely.

</details>

---

### D4. Background task holding a request-scoped resource

```
@app.post("/orders")
async def create(bg: BackgroundTasks, session = Depends(get_session)) -> dict:
    order = await create_order(session)
    bg.add_task(send_receipt, session, order.id)
    return {"id": order.id}
```

**Observed symptom:** The receipt email fails intermittently with `DetachedInstanceError` or 'session is closed'.

**(a)** What is the lifetime mismatch here?

**(b)** What should be passed to the background task instead?

**(c)** When is `BackgroundTasks` the wrong tool entirely?

<details>
<summary><b>Show the diagnosis</b></summary>

The `session` dependency is torn down when the response is sent. The background task runs **after** that, so it holds a closed session — a lifetime mismatch.

**Pass plain data**, never live resources: hand the task `order.id` and let it open its own session. Anything crossing an async boundary should be serialisable.

**Wrong tool when** the work must survive a process restart, must be retried, must be observable, or takes more than a second or two. `BackgroundTasks` runs in the same process with no persistence and no retry — if the worker is redeployed mid-task, the work is simply lost. That is what Module 18's Redis Streams queue exists for.

</details>

---

### D5. Dependency cached within a request

```python
call_count = 0

def get_id() -> int:
    global call_count
    call_count += 1
    return call_count

@app.get("/x")
async def x(a: int = Depends(get_id), b: int = Depends(get_id)) -> dict:
    return {"a": a, "b": b}
```

**Observed symptom:** Returns `{"a": 1, "b": 1}` — the dependency ran once, not twice.

**(a)** Why did the second `Depends` reuse the first result?

**(b)** How do you force it to run twice?

**(c)** Why is this caching behaviour usually what you want?

<details>
<summary><b>Show the diagnosis</b></summary>

FastAPI **caches dependency results per request** by default, keyed on the callable and its own dependencies. Both `Depends(get_id)` entries resolve to the same cache entry.

**Force re-execution:** `Depends(get_id, use_cache=False)`.

**Why caching is right:** dependency graphs are usually diamonds. `get_current_user` depends on `get_session`; so does `get_permissions`; so does the route. Without caching you would open three database sessions and decode the JWT three times for one request. The cache makes a declarative dependency graph efficient. Surprises only arise when a dependency is deliberately impure — and then `use_cache=False` documents that intent explicitly.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
