# Module 13: Self-Assessment Quiz & Mastery Challenges

Test your understanding of FastAPI, ASGI, and API Routing before moving to **Module 12**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Gateway Interfaces:** What is the technical difference between WSGI (Web Server Gateway Interface) and ASGI (Asynchronous Server Gateway Interface)?
2. **ASGI Servers:** What role does Uvicorn play in a FastAPI production deployment?
3. **Type Hint Integration:** How does FastAPI utilize standard Python type hints (`int`, `str`, Pydantic models) to perform automatic request parsing?
4. **ASGI Low-Level Protocol:** What do the 3 parameters `(scope, receive, send)` represent in the ASGI specification?
5. **OpenAPI Generation:** How does FastAPI generate Swagger UI (`/docs`) and ReDoc (`/redoc`) without external documentation files?
6. **Parameter Resolution:** How does FastAPI distinguish between a **Path Parameter**, a **Query Parameter**, and a **Request Body** in an endpoint signature?
7. **HTTP 422:** What causes an HTTP `422 Unprocessable Entity` error response in FastAPI?
8. **Route Ordering:** Why must `/items/summary` be declared before `/items/{item_id}` in code?
9. **Concurrency Dispatch:** What does FastAPI do differently under the hood when you declare an endpoint with `def` vs `async def`?
10. **Automated Testing:** How does Starlette's `TestClient` allow testing FastAPI routes without binding to an open network port?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- **WSGI:** Synchronous, single-request-per-thread model (Flask/Django).
- **ASGI:** Asynchronous, event-driven model supporting non-blocking HTTP requests and WebSockets (FastAPI/Starlette).

#### Answer 2:
Uvicorn is a lightning-fast ASGI web server implementation that binds to OS network sockets and passes incoming HTTP packets to FastAPI's ASGI application.

#### Answer 3:
FastAPI inspects function type signatures via reflection at startup and generates Pydantic validation schemas to parse, cast, and validate incoming query/path parameters and JSON payloads.

#### Answer 4:
- `scope`: Dictionary containing connection metadata (HTTP method, headers, path, client IP).
- `receive`: Async callable to receive incoming request body byte chunks.
- `send`: Async callable to emit response headers and body byte chunks back to the client.

#### Answer 5:
FastAPI compiles its route definitions and Pydantic models into an OpenAPI 3.1 JSON schema, which Swagger UI and ReDoc render dynamically in the browser.

#### Answer 6:
- If declared in the URL path string (e.g. `/{id}`), it's a **Path Parameter**.
- If a primitive type not in the path (e.g. `limit: int = 10`), it's a **Query Parameter**.
- If a Pydantic model (e.g. `item: ItemSchema`), it's parsed from the **JSON Request Body**.

#### Answer 7:
When incoming client request data fails validation against the endpoint's declared Pydantic schema or type constraints (e.g. string sent where integer required).

#### Answer 8:
Routes are matched sequentially top-to-bottom. If `/items/{item_id}` is placed first, it matches the string `"summary"` as `item_id`, preventing `/items/summary` from ever executing.

#### Answer 9:
- `async def`: Runs directly on the main event loop.
- `def`: Offloaded to an external thread pool (`anyio.to_thread`) to safely execute synchronous blocking code without starving the event loop.

#### Answer 10:
`TestClient` uses HTTPX/Requests transport adapters to route requests directly into the ASGI application memory pipeline without opening a physical OS TCP port.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Calculator API Endpoint

**Goal:** Write a FastAPI endpoint `@app.get("/math/divide")` accepting two query parameters `a: float` and `b: float`, returning the quotient, and returning HTTP 400 if `b == 0`.

<details>
<summary><b>Solution Code</b></summary>

```python
from fastapi import FastAPI, HTTPException, status
from starlette.testclient import TestClient

app = FastAPI()

@app.get("/math/divide")
def divide_numbers(a: float, b: float):
    if b == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Division by zero is undefined!"
        )
    return {"a": a, "b": b, "result": a / b}

# Verification:
client = TestClient(app)
res = client.get("/math/divide?a=10&b=2")
print("10 / 2 Result:", res.json())
res_zero = client.get("/math/divide?a=10&b=0")
print("Division by zero status:", res_zero.status_code)
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Blocking call in an async route

```python
import time
from fastapi import FastAPI

app = FastAPI()

@app.get("/report")
async def report() -> dict:
    time.sleep(2)              # a slow, synchronous library call
    return {"ok": True}
```

**Observed symptom:** One request takes 2 s. Ten concurrent requests take 20 s, and the `/health` endpoint stops responding while they run.

**(a)** Why does a slow call in one route block every other route?

**(b)** Give two fixes and say when each is appropriate.

**(c)** What would change if the function were `def` rather than `async def`?

<details>
<summary><b>Show the diagnosis</b></summary>

An `async def` route runs **on the event loop thread**. A synchronous `sleep` (or any blocking I/O) holds that thread, so no other request — including a health check — can be serviced.

**Fix 1:** make the route `def` instead of `async def`. FastAPI then runs it in a threadpool automatically, and blocking is contained. **Fix 2:** keep it `async` and offload explicitly with `await asyncio.to_thread(blocking_call)`. Use fix 1 when the whole handler is synchronous; fix 2 when only part of it is.

**As a plain `def`:** Starlette detects the non-coroutine and dispatches it to `anyio`'s threadpool (40 threads by default), so ten requests would take ~2 s total. This is the single most important FastAPI performance rule: **never** put a blocking call in an `async def`.

</details>

---

### D2. Response model does not filter

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserOut(BaseModel):
    id: int
    email: str

class UserDB(BaseModel):
    id: int
    email: str
    password_hash: str

@app.get("/me")
async def me() -> dict:
    return UserDB(id=1, email="a@b.c", password_hash="$2b$...").model_dump()
```

**Observed symptom:** The JSON response includes `password_hash`.

**(a)** Why did the `UserOut` model not filter the field?

**(b)** What is the correct declaration?

**(c)** Why is the return annotation not enough on its own here?

<details>
<summary><b>Show the diagnosis</b></summary>

`UserOut` is never referenced. The route returns a plain `dict` annotated as `dict`, so FastAPI serialises it verbatim — nothing filters anything.

**Fix:** declare the output model, either as the return annotation (`async def me() -> UserOut:`) or explicitly (`@app.get('/me', response_model=UserOut)`). FastAPI then validates and *filters* the response to exactly the declared fields.

**`-> dict` is not enough** because `dict` imposes no shape. The annotation only helps when it names a Pydantic model. This is a real leak pattern — declare `response_model` on every route that returns data derived from a database row, and let the framework enforce it rather than remembering to pop fields by hand.

</details>

---

### D3. Mutable default in a Pydantic model

```python
from pydantic import BaseModel

class Cart(BaseModel):
    items: list[str] = []

a, b = Cart(), Cart()
a.items.append("book")
print(b.items)
```

**Observed symptom:** With plain Python this would print `['book']`. With Pydantic it prints `[]`.

**(a)** Why is Pydantic safe here when a dataclass would not be?

**(b)** What does the equivalent dataclass need?

**(c)** What is the one Pydantic default that *is* still shared?

<details>
<summary><b>Show the diagnosis</b></summary>

Pydantic **deep-copies** mutable defaults for every instance, so each `Cart` gets its own list. This is a deliberate divergence from stdlib behaviour and one of the genuine reasons to use it for data models.

**A dataclass** needs `field(default_factory=list)`; a bare `= []` is the classic shared-state bug (see Module 04's diagnostic on class attributes). `@dataclass` actually raises `ValueError` for a mutable default, which is a nice piece of design.

**Still shared:** a default that Pydantic cannot copy — an open file handle, a database connection, a `threading.Lock`. For those use `Field(default_factory=...)` explicitly. Also note `model_config` and class-level `ClassVar` are genuinely class-scoped by design.

</details>

---

### D4. Dependency evaluated once, not per request

```python
from fastapi import Depends, FastAPI
import time

app = FastAPI()

def request_time() -> float:
    return time.time()

@app.get("/now")
async def now(t: float = Depends(request_time())) -> dict:
    return {"t": t}
```

**Observed symptom:** Every response returns the identical timestamp — the moment the server started.

**(a)** Spot the bug in the `Depends` call.

**(b)** What is the correct form?

**(c)** How would you deliberately get the 'evaluate once' behaviour?

<details>
<summary><b>Show the diagnosis</b></summary>

`Depends(request_time())` **calls** the function immediately at import time and passes its *result* — a float — as the dependency. FastAPI then treats that float as a fixed default.

**Correct:** `Depends(request_time)` — pass the callable, not the call. FastAPI invokes it per request.

**Deliberate single evaluation:** use `@lru_cache` on a settings provider, which is the documented pattern for configuration:

```python
@lru_cache
def get_settings() -> Settings:
    return Settings()
```

Then `Depends(get_settings)` returns the same instance every time. The distinction — callable versus called — is the whole bug, and `ruff`'s `B008` rule exists to warn about function calls in argument defaults (the course disables it because FastAPI's `Depends` is the legitimate exception).

</details>

---

### D5. Path parameter order shadows a route

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: str) -> dict:
    return {"user": user_id}

@app.get("/users/me")
async def get_me() -> dict:
    return {"user": "current"}
```

**Observed symptom:** `GET /users/me` returns `{"user": "me"}` instead of `{"user": "current"}`.

**(a)** Why does the wrong handler win?

**(b)** What is the fix?

**(c)** What would happen if `user_id` were annotated `int`?

<details>
<summary><b>Show the diagnosis</b></summary>

Starlette matches routes **in declaration order** and returns the first match. `/users/{user_id}` matches `/users/me` with `user_id='me'`, so the specific route is never reached.

**Fix:** declare the literal route **before** the parameterised one. Order matters, and it is not alphabetical or specificity-based.

**With `user_id: int`:** the path still matches, but conversion fails and FastAPI returns **422 Unprocessable Entity** rather than falling through to the next route. That is arguably worse — a confusing validation error instead of a working endpoint — and it is why you cannot rely on type annotations for disambiguation.

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
