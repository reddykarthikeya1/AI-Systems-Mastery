"""Diagnostic quiz questions, batch B: Modules 13-19 (FastAPI through DevOps)."""

from __future__ import annotations

DIAGNOSTICS: dict[str, list[tuple[str, str, str, list[str], str]]] = {
    "13": [
        (
            "Blocking call in an async route",
            '''import time
from fastapi import FastAPI

app = FastAPI()

@app.get("/report")
async def report() -> dict:
    time.sleep(2)              # a slow, synchronous library call
    return {"ok": True}''',
            "One request takes 2 s. Ten concurrent requests take 20 s, and the `/health` "
            "endpoint stops responding while they run.",
            [
                "Why does a slow call in one route block every other route?",
                "Give two fixes and say when each is appropriate.",
                "What would change if the function were `def` rather than `async def`?",
            ],
            "An `async def` route runs **on the event loop thread**. A synchronous `sleep` (or "
            "any blocking I/O) holds that thread, so no other request — including a health check "
            "— can be serviced.\n\n**Fix 1:** make the route `def` instead of `async def`. "
            "FastAPI then runs it in a threadpool automatically, and blocking is contained. "
            "**Fix 2:** keep it `async` and offload explicitly with `await "
            "asyncio.to_thread(blocking_call)`. Use fix 1 when the whole handler is synchronous; "
            "fix 2 when only part of it is.\n\n**As a plain `def`:** Starlette detects the "
            "non-coroutine and dispatches it to `anyio`'s threadpool (40 threads by default), so "
            "ten requests would take ~2 s total. This is the single most important FastAPI "
            "performance rule: **never** put a blocking call in an `async def`.",
        ),
        (
            "Response model does not filter",
            '''from fastapi import FastAPI
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
    return UserDB(id=1, email="a@b.c", password_hash="$2b$...").model_dump()''',
            "The JSON response includes `password_hash`.",
            [
                "Why did the `UserOut` model not filter the field?",
                "What is the correct declaration?",
                "Why is the return annotation not enough on its own here?",
            ],
            "`UserOut` is never referenced. The route returns a plain `dict` annotated as "
            "`dict`, so FastAPI serialises it verbatim — nothing filters anything.\n\n**Fix:** "
            "declare the output model, either as the return annotation "
            "(`async def me() -> UserOut:`) or explicitly "
            "(`@app.get('/me', response_model=UserOut)`). FastAPI then validates and *filters* "
            "the response to exactly the declared fields.\n\n**`-> dict` is not enough** because "
            "`dict` imposes no shape. The annotation only helps when it names a Pydantic model. "
            "This is a real leak pattern — declare `response_model` on every route that returns "
            "data derived from a database row, and let the framework enforce it rather than "
            "remembering to pop fields by hand.",
        ),
        (
            "Mutable default in a Pydantic model",
            '''from pydantic import BaseModel

class Cart(BaseModel):
    items: list[str] = []

a, b = Cart(), Cart()
a.items.append("book")
print(b.items)''',
            "With plain Python this would print `['book']`. With Pydantic it prints `[]`.",
            [
                "Why is Pydantic safe here when a dataclass would not be?",
                "What does the equivalent dataclass need?",
                "What is the one Pydantic default that *is* still shared?",
            ],
            "Pydantic **deep-copies** mutable defaults for every instance, so each `Cart` gets "
            "its own list. This is a deliberate divergence from stdlib behaviour and one of the "
            "genuine reasons to use it for data models.\n\n**A dataclass** needs "
            "`field(default_factory=list)`; a bare `= []` is the classic shared-state bug (see "
            "Module 04's diagnostic on class attributes). `@dataclass` actually raises "
            "`ValueError` for a mutable default, which is a nice piece of "
            "design.\n\n**Still shared:** a default that Pydantic cannot copy — an open file "
            "handle, a database connection, a `threading.Lock`. For those use "
            "`Field(default_factory=...)` explicitly. Also note `model_config` and class-level "
            "`ClassVar` are genuinely class-scoped by design.",
        ),
        (
            "Dependency evaluated once, not per request",
            '''from fastapi import Depends, FastAPI
import time

app = FastAPI()

def request_time() -> float:
    return time.time()

@app.get("/now")
async def now(t: float = Depends(request_time())) -> dict:
    return {"t": t}''',
            "Every response returns the identical timestamp — the moment the server started.",
            [
                "Spot the bug in the `Depends` call.",
                "What is the correct form?",
                "How would you deliberately get the 'evaluate once' behaviour?",
            ],
            "`Depends(request_time())` **calls** the function immediately at import time and "
            "passes its *result* — a float — as the dependency. FastAPI then treats that float as "
            "a fixed default.\n\n**Correct:** `Depends(request_time)` — pass the callable, not "
            "the call. FastAPI invokes it per request.\n\n**Deliberate single evaluation:** use "
            "`@lru_cache` on a settings provider, which is the documented pattern for "
            "configuration:\n\n```python\n@lru_cache\ndef get_settings() -> Settings:\n    return "
            "Settings()\n```\n\nThen `Depends(get_settings)` returns the same instance every "
            "time. The distinction — callable versus called — is the whole bug, and `ruff`'s "
            "`B008` rule exists to warn about function calls in argument defaults (the course "
            "disables it because FastAPI's `Depends` is the legitimate exception).",
        ),
        (
            "Path parameter order shadows a route",
            '''from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: str) -> dict:
    return {"user": user_id}

@app.get("/users/me")
async def get_me() -> dict:
    return {"user": "current"}''',
            "`GET /users/me` returns `{\"user\": \"me\"}` instead of `{\"user\": \"current\"}`.",
            [
                "Why does the wrong handler win?",
                "What is the fix?",
                "What would happen if `user_id` were annotated `int`?",
            ],
            "Starlette matches routes **in declaration order** and returns the first match. "
            "`/users/{user_id}` matches `/users/me` with `user_id='me'`, so the specific route is "
            "never reached.\n\n**Fix:** declare the literal route **before** the parameterised "
            "one. Order matters, and it is not alphabetical or specificity-based.\n\n**With "
            "`user_id: int`:** the path still matches, but conversion fails and FastAPI returns "
            "**422 Unprocessable Entity** rather than falling through to the next route. That is "
            "arguably worse — a confusing validation error instead of a working endpoint — and it "
            "is why you cannot rely on type annotations for disambiguation.",
        ),
    ],
    "14": [
        (
            "Validator that silently does nothing",
            '''from pydantic import BaseModel, field_validator

class Order(BaseModel):
    quantity: int

    @field_validator("qty")            # note the name
    @classmethod
    def positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("must be positive")
        return v

print(Order(quantity=-5))''',
            "In Pydantic v2 this raises at class definition. In some configurations it silently "
            "accepts `-5`.",
            [
                "What is wrong with the validator?",
                "What protects you from this class of typo?",
                "What is the difference between `field_validator` and `model_validator` here?",
            ],
            "The validator targets `\"qty\"`, a field that does not exist. Pydantic v2 raises "
            "`PydanticUserError: Decorators defined with incorrect fields` at class-creation "
            "time — which is the good outcome.\n\n**Protection:** that startup error *is* the "
            "protection, and it is why v2 is stricter than v1 (where a mismatched validator name "
            "was silently ignored). Keep `model_config = ConfigDict(extra='forbid')` on input "
            "models too, so unexpected *data* keys are rejected as well as unexpected validator "
            "targets.\n\n**`model_validator`** runs after all fields are parsed and sees the whole "
            "object, so it is the right tool for cross-field rules ('end date must follow start "
            "date'). `field_validator` sees one value and cannot express that.",
        ),
        (
            "Validation bypassed by construct",
            '''from pydantic import BaseModel, Field

class Config(BaseModel):
    workers: int = Field(ge=1, le=64)

bad = Config.model_construct(workers=-10)
print(bad.workers)''',
            "Prints `-10`. The `ge=1` constraint did not apply.",
            [
                "What does `model_construct` skip, and why does it exist?",
                "When is using it correct?",
                "How would this value reach production undetected?",
            ],
            "`model_construct` builds the instance **without running validation or coercion**. "
            "It exists as a performance escape hatch for data you have *already* validated — "
            "for example rows coming straight out of your own database, where re-validating "
            "millions of rows is pure cost.\n\n**Correct use:** trusted, already-validated "
            "internal data on a hot path, with a comment saying so. Never for external input."
            "\n\n**How it reaches production:** somebody profiles a slow endpoint, sees Pydantic "
            "in the flame graph, swaps `Config(**row)` for `Config.model_construct(**row)`, and "
            "the tests still pass because the test fixtures are valid. The constraint is now "
            "decoration. Guard it with a test that asserts invalid input is rejected through the "
            "**real** construction path used by the endpoint.",
        ),
        (
            "Optional vs default confusion",
            '''from pydantic import BaseModel

class Profile(BaseModel):
    nickname: str | None

print(Profile())''',
            "`ValidationError: Field required` — but the field is `| None`, so you expected it "
            "to be optional.",
            [
                "Why is a nullable field still required?",
                "What are the three distinct states you might want, and how do you spell each?",
                "Why does this distinction matter for a PATCH endpoint specifically?",
            ],
            "`str | None` describes the **type**, not the presence requirement. A field with no "
            "default is required; it just happens to accept `None` as a value.\n\n**Three "
            "states:**\n- required, may be null: `nickname: str | None`\n- optional, defaults to "
            "null: `nickname: str | None = None`\n- optional, distinguishable 'not supplied': "
            "`nickname: str | None = Field(default=None)` plus "
            "`model_dump(exclude_unset=True)`\n\n**PATCH depends on it:** a partial update must "
            "tell 'set nickname to null' apart from 'do not touch nickname'. Both arrive as "
            "`None` in the model, so you need `exclude_unset=True` (or `model_fields_set`) to "
            "know which keys the client actually sent. Ignoring this is how a PATCH silently "
            "wipes fields the client never mentioned.",
        ),
        (
            "Coercion hides bad data",
            '''from pydantic import BaseModel

class Item(BaseModel):
    count: int

print(Item(count="12").count)
print(Item(count=12.9).count)''',
            "Prints `12`, then `12` — the float was truncated silently.",
            [
                "What is Pydantic's default coercion behaviour called?",
                "How do you make it refuse both of these?",
                "Which mode should an internal service-to-service API use, and why?",
            ],
            "The default is **lax mode**: Pydantic coerces where the conversion is lossless-ish, "
            "so `\"12\"` becomes `12`, and a float with a fractional part... actually raises in "
            "v2 for `12.9` unless the value is integral. The general lesson stands: silent "
            "coercion means the type you declared is not the type you validated.\n\n**Refuse "
            "both:** `model_config = ConfigDict(strict=True)`, or per-field "
            "`Field(strict=True)`. Then a string is not an int and a float is not an "
            "int.\n\n**Internal APIs should use strict mode.** Lax coercion exists to be "
            "forgiving of untyped external input such as form posts and query strings, where "
            "everything arrives as a string. Between your own typed services there is no excuse "
            "for a type mismatch, and accepting one hides a real bug in the caller.",
        ),
        (
            "Model reused for input and output",
            '''from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    is_admin: bool = False

# used for both the request body and the response''',
            "A user POSTs `{\"id\": 1, \"email\": \"x@y.z\", \"is_admin\": true}` and becomes an "
            "administrator.",
            [
                "Name the two separate vulnerabilities in reusing this model.",
                "What is the correct structure?",
                "What is this class of bug called?",
            ],
            "**Two problems.** (1) `is_admin` is client-settable — privilege escalation. (2) `id` "
            "is client-settable, so a caller can choose or overwrite a primary key.\n\n"
            "**Correct structure:** separate models per direction —\n\n```python\nclass "
            "UserCreate(BaseModel):      # input: only what a client may set\n    email: "
            "EmailStr\n    password: SecretStr\n\nclass UserOut(BaseModel):         # output: "
            "only what a client may see\n    id: int\n    email: EmailStr\n```\n\nThe server "
            "assigns `id` and `is_admin`; they appear in neither input model.\n\n**Named:** "
            "**mass assignment** (or over-posting). It is one of the most common API "
            "vulnerabilities precisely because sharing one model feels DRY. Module 16's RBAC "
            "service keeps input and output models strictly separate for this reason.",
        ),
    ],
    "15": [
        (
            "N+1 query",
            '''users = session.execute(select(User)).scalars().all()
for user in users:
    print(user.name, len(user.orders))     # lazy relationship''',
            "Loading 500 users issues 501 queries and the endpoint takes 4 s.",
            [
                "Where does the 501st query come from?",
                "Name two loader strategies that fix it and when each is better.",
                "How would you detect this automatically in CI?",
            ],
            "One query fetches the users; then accessing `user.orders` triggers a **separate "
            "lazy-load query per user** — 1 + 500.\n\n**Two strategies:** "
            "`selectinload(User.orders)` issues a second query with `WHERE user_id IN (...)` — "
            "two queries total, and the best default for one-to-many. `joinedload(User.orders)` "
            "uses a single LEFT JOIN — one query, but it multiplies rows and can be slower for "
            "large collections. Use `joinedload` for many-to-one, `selectinload` for "
            "one-to-many.\n\n**Detect in CI:** count queries in a test. Attach an event listener "
            "to `before_cursor_execute` and assert the count is below a threshold, or use "
            "`sqlalchemy.event` with a fixture that fails the test above N queries. A query-count "
            "assertion is a performance test that never flakes, unlike a timing one.",
        ),
        (
            "Async engine with a sync driver",
            '''from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("sqlite:///app.db")''',
            "`InvalidRequestError: The asyncio extension requires an async driver to be used.`",
            [
                "What is wrong with the URL?",
                "What are the correct URLs for SQLite and PostgreSQL?",
                "Why can't SQLAlchemy just wrap the sync driver for you?",
            ],
            "The URL selects the **default synchronous DBAPI** (`sqlite3`). An async engine needs "
            "an async driver.\n\n**Correct:** `sqlite+aiosqlite:///app.db` and "
            "`postgresql+asyncpg://user:pw@host/db`.\n\n**Why not wrap it:** a sync driver "
            "blocks the calling thread on every network round trip. Wrapping it in a threadpool "
            "*is* possible — that is essentially what `run_in_executor` does — but it gives you "
            "thread-per-query concurrency, not event-loop concurrency, so you lose the entire "
            "scalability benefit while keeping all of `asyncio`'s complexity. SQLAlchemy refuses "
            "explicitly rather than let you build something that looks async and performs "
            "worse than sync code.",
        ),
        (
            "Session shared across requests",
            '''from sqlalchemy.orm import Session

session = Session(engine)          # module level

def get_user(user_id: int):
    return session.get(User, user_id)''',
            "Under concurrent load: `InvalidRequestError: This session is provisionally in a "
            "transaction`, random `DetachedInstanceError`, and occasionally one request seeing "
            "another's uncommitted data.",
            [
                "Why is a module-level Session wrong?",
                "What is the correct lifecycle, and how do you wire it in FastAPI?",
                "What is the difference between the Session and the connection pool here?",
            ],
            "A `Session` is a **unit of work** holding an identity map and a transaction. It is "
            "explicitly *not* thread-safe or task-safe. Sharing one means concurrent requests "
            "interleave in the same transaction.\n\n**Correct lifecycle:** one session per "
            "request, created at the start and closed at the end. In FastAPI:\n\n```python\n"
            "async def get_session():\n    async with AsyncSessionLocal() as session:\n        "
            "yield session\n```\n\nthen `session: AsyncSession = Depends(get_session)`.\n\n"
            "**Session vs pool:** the *engine* owns a connection pool and **is** meant to be "
            "shared and module-level — creating an engine per request would destroy pooling. The "
            "session is the short-lived thing. Confusing the two is the root of this bug: share "
            "the engine, never the session.",
        ),
        (
            "Alembic autogenerate misses a change",
            '''# models.py
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)      # newly added''',
            "`alembic revision --autogenerate` produces an empty migration.",
            [
                "Name three reasons autogenerate produces nothing.",
                "What must `env.py` contain?",
                "Which schema changes can autogenerate *never* detect?",
            ],
            "**Three causes:** (1) `target_metadata` in `env.py` is `None` or points at the wrong "
            "`Base`; (2) the module defining `User` was never imported, so it is not in the "
            "metadata; (3) the database is already at that state, so there is genuinely no "
            "diff.\n\n**`env.py` needs:** `from myapp.models import Base` and "
            "`target_metadata = Base.metadata`, with every model module imported (often via the "
            "package `__init__`).\n\n**Never detected:** server-side defaults changes, "
            "constraint *name* changes, `CHECK` constraints, most index option changes, enum "
            "value additions, and anything requiring data migration. Autogenerate is a **draft**, "
            "not an authority — always read the generated migration and always test the "
            "downgrade path.",
        ),
        (
            "Commit without refresh",
            '''new_user = User(email="a@b.c")
session.add(new_user)
session.commit()
print(new_user.id)''',
            "In some configurations, printing `new_user.id` issues a surprise SELECT; in others "
            "it raises `DetachedInstanceError`.",
            [
                "What does `commit()` do to the instance's attributes?",
                "How do you get the generated id efficiently?",
                "What does `expire_on_commit=False` change, and what is its risk?",
            ],
            "By default `commit()` **expires** every attribute on every instance in the session. "
            "The next attribute access triggers a refresh SELECT — and if the session is already "
            "closed, a `DetachedInstanceError` instead.\n\n**Get the id efficiently:** "
            "`session.flush()` before commit — the INSERT executes and the primary key is "
            "populated without ending the transaction. Or `session.refresh(new_user)` "
            "afterwards, or use `returning()` on the insert.\n\n"
            "**`expire_on_commit=False`** keeps attributes loaded after commit, which is the "
            "usual choice for async sessions (where an implicit lazy refresh cannot happen "
            "inside a sync attribute access). The risk is **staleness**: your in-memory object no "
            "longer reflects concurrent changes by other transactions, and you will not be told.",
        ),
    ],
    "16": [
        (
            "JWT signature not verified",
            '''import jwt

def read_token(token: str) -> dict:
    return jwt.decode(token, options={"verify_signature": False})''',
            "Any attacker can mint a token granting themselves any role.",
            [
                "What exactly does this code fail to check?",
                "What is the correct call?",
                "Name two further claims that must be validated even with a valid signature.",
            ],
            "It decodes the payload without verifying the **signature**, so the token's contents "
            "are entirely attacker-controlled. A JWT is signed base64, not encrypted — anyone can "
            "read *and* forge one if you do not check the signature.\n\n**Correct:**\n\n```python"
            "\njwt.decode(token, key=SECRET, algorithms=['HS256'])\n```\n\nPassing "
            "`algorithms` explicitly is mandatory: omitting it historically allowed the "
            "**`alg: none`** attack, and permitting both HS256 and RS256 enables the "
            "algorithm-confusion attack where the public key is used as an HMAC secret."
            "\n\n**Also validate:** `exp` (expiry — verified by default, do not disable), and "
            "`aud`/`iss` (a token minted for a different service or tenant must be rejected). "
            "Add `nbf` if you issue future-dated tokens.",
        ),
        (
            "Timing attack on token comparison",
            '''def check_api_key(supplied: str, expected: str) -> bool:
    return supplied == expected''',
            "Functionally correct; leaks the key over the network to a patient attacker.",
            [
                "How does `==` leak information?",
                "What is the correct comparison?",
                "Does this apply to bcrypt password checks too?",
            ],
            "String `==` **short-circuits** at the first differing byte. Comparing a wrong key "
            "returns marginally faster the earlier the mismatch occurs. Averaged over enough "
            "requests, an attacker recovers the key one byte at a "
            "time.\n\n**Correct:** `hmac.compare_digest(supplied, expected)`, which is "
            "constant-time with respect to content.\n\n**Not needed for bcrypt:** "
            "`bcrypt.checkpw` is already constant-time internally, and more importantly the "
            "attacker is comparing against a *hash* whose computation dominates any comparison "
            "timing. The rule applies to any direct comparison of a **secret you hold in "
            "plaintext**: API keys, session tokens, HMAC signatures, CSRF tokens, password-reset "
            "tokens.",
        ),
        (
            "Password hashed with SHA-256",
            '''import hashlib

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()''',
            "The database is stolen and 80% of passwords are recovered within a day.",
            [
                "Why is SHA-256 the wrong primitive here?",
                "What should be used, and what property makes it right?",
                "What does a salt protect against, and what does it *not* protect against?",
            ],
            "SHA-256 is designed to be **fast** — billions of hashes per second on a GPU. That is "
            "exactly the wrong property for a password hash, where you want each guess to be "
            "expensive. There is also no salt here, so identical passwords produce identical "
            "hashes.\n\n**Use** bcrypt, scrypt, or Argon2id. Their defining property is a "
            "**tunable work factor** — you raise the cost as hardware improves, and the same "
            "parameter is stored in the hash so old hashes remain verifiable. Module 16 uses "
            "`bcrypt`.\n\n**A salt** prevents precomputation: rainbow tables and the instant "
            "cracking of duplicate passwords across accounts. It does **not** slow down an "
            "attack on a single password — only the work factor does that. You need both.",
        ),
        (
            "Authorisation checked in the wrong place",
            '''@app.get("/documents/{doc_id}")
async def get_document(doc_id: int, user = Depends(current_user)) -> dict:
    doc = await db.get_document(doc_id)
    return doc''',
            "Any authenticated user can read any document by changing the id in the URL.",
            [
                "What is the difference between what this checks and what it needs to check?",
                "What is this vulnerability called?",
                "Where should the check live so it cannot be forgotten on the next endpoint?",
            ],
            "`Depends(current_user)` proves **authentication** — who you are. It says nothing "
            "about **authorisation** — whether *this* user may read *this* document. The "
            "ownership check is simply absent.\n\n**Called:** **IDOR** (Insecure Direct Object "
            "Reference), or broken object-level authorisation — consistently near the top of the "
            "OWASP API Security Top 10.\n\n**Where the check belongs:** in the data-access layer, "
            "not the route. Make the query itself scoped — `WHERE id = :doc_id AND owner_id = "
            ":user_id` — so an unauthorised row is *unfetchable* rather than fetched-then-checked. "
            "A route-level `if doc.owner_id != user.id: raise 403` works but relies on every "
            "future endpoint remembering it. Push the constraint down to where forgetting is "
            "impossible.",
        ),
        (
            "Refresh token that never expires",
            '''ACCESS_TOKEN_TTL = 15 * 60          # 15 minutes
REFRESH_TOKEN_TTL = None            # never expires''',
            "A leaked refresh token grants permanent access, and logging out does not revoke it.",
            [
                "Why does a short access-token TTL not help here?",
                "What two mechanisms make refresh tokens revocable?",
                "Why are JWTs a poor choice for the refresh token specifically?",
            ],
            "The access token expiring in 15 minutes is irrelevant when the holder can mint a "
            "fresh one forever. The refresh token *is* the long-lived credential, so it needs the "
            "strongest handling.\n\n**Two mechanisms:** (1) **server-side storage** — keep refresh "
            "tokens in a table or in Redis so logout can delete them and an admin can revoke a "
            "session; (2) **rotation with reuse detection** — issue a new refresh token on every "
            "use and invalidate the old one; if an old one is ever presented again, that means it "
            "was stolen, so revoke the entire token family.\n\n**JWTs are wrong for refresh "
            "tokens** because their whole appeal is being stateless and self-validating — which "
            "means unrevocable. Use an opaque random token backed by server state. Keep the JWT "
            "for the short-lived access token where statelessness is genuinely worth it.",
        ),
    ],
    "17": [
        (
            "WebSocket disconnect leaks the connection",
            '''active: list[WebSocket] = []

@app.websocket("/ws")
async def endpoint(ws: WebSocket) -> None:
    await ws.accept()
    active.append(ws)
    while True:
        msg = await ws.receive_text()
        for peer in active:
            await peer.send_text(msg)''',
            "After clients disconnect, `active` keeps growing and every broadcast raises "
            "`RuntimeError: Cannot call \"send\" once a close message has been sent`.",
            [
                "Why is the socket never removed from `active`?",
                "What is the correct structure?",
                "Why is iterating `active` while sending also unsafe?",
            ],
            "When the client disconnects, `receive_text()` raises `WebSocketDisconnect`, which "
            "propagates out of the handler — so the `active.remove(ws)` that should follow never "
            "runs.\n\n**Correct:**\n\n```python\ntry:\n    while True:\n        msg = await "
            "ws.receive_text()\n        await manager.broadcast(msg)\nexcept WebSocketDisconnect:"
            "\n    pass\nfinally:\n    manager.disconnect(ws)\n```\n\nA `finally` (or a "
            "connection-manager context manager) is what guarantees removal on **every** exit "
            "path.\n\n**Iterating while sending** is unsafe twice over: a dead peer raises "
            "mid-loop and aborts the broadcast to everyone after it, and a concurrent "
            "connect/disconnect mutates the list during iteration. Iterate over a copy, collect "
            "the failures, and remove them afterwards.",
        ),
        (
            "Dependency with yield and an exception",
            '''async def get_conn():
    conn = await pool.acquire()
    yield conn
    await pool.release(conn)''',
            "Under load the pool is exhausted. Connections are never returned when a route "
            "raises.",
            [
                "Why is the connection not released when the route raises?",
                "What is the fix?",
                "What changed in FastAPI about exceptions in yield-dependencies?",
            ],
            "If the route body raises, the exception is thrown *into* the generator at the "
            "`yield`. Without a `try/finally` the code after `yield` never executes and the "
            "connection is lost.\n\n**Fix:**\n\n```python\nasync def get_conn():\n    conn = "
            "await pool.acquire()\n    try:\n        yield conn\n    finally:\n        await "
            "pool.release(conn)\n```\n\nThis is the same rule as any generator-based context "
            "manager: cleanup belongs in `finally`, never merely after the "
            "`yield`.\n\n**What changed:** FastAPI now runs yield-dependency teardown *after* the "
            "response is sent and re-raises exceptions from the dependency in a way that reaches "
            "your exception handlers. Earlier versions could swallow them. Either way the "
            "`finally` is required — do not depend on framework behaviour for resource safety.",
        ),
        (
            "Middleware that consumes the body",
            '''@app.middleware("http")
async def log_body(request: Request, call_next):
    body = await request.body()
    logger.info("body=%s", body)
    return await call_next(request)''',
            "Every POST route receives an empty body and returns 422.",
            [
                "Why is the body empty by the time the route runs?",
                "What are two ways to log the body safely?",
                "What is the risk in the more convenient of those two?",
            ],
            "The request body is an **async stream** that can be consumed once. `await "
            "request.body()` drains it; the route's attempt to read it finds nothing.\n\n"
            "**Two safe approaches:** (1) re-inject the consumed bytes by replacing the "
            "`receive` callable so downstream sees the stream again; (2) do not read it in "
            "middleware — log inside the route, or use a `route_class` that has already parsed "
            "it.\n\n**The risk in re-injection** is memory: you must buffer the *entire* body, so "
            "a 500 MB upload becomes 500 MB of RAM per concurrent request, and it is a trivial "
            "denial-of-service vector. If you must log bodies, cap the size you buffer and skip "
            "streaming content types entirely.",
        ),
        (
            "Background task holding a request-scoped resource",
            '''@app.post("/orders")
async def create(bg: BackgroundTasks, session = Depends(get_session)) -> dict:
    order = await create_order(session)
    bg.add_task(send_receipt, session, order.id)
    return {"id": order.id}''',
            "The receipt email fails intermittently with `DetachedInstanceError` or 'session is "
            "closed'.",
            [
                "What is the lifetime mismatch here?",
                "What should be passed to the background task instead?",
                "When is `BackgroundTasks` the wrong tool entirely?",
            ],
            "The `session` dependency is torn down when the response is sent. The background "
            "task runs **after** that, so it holds a closed session — a lifetime "
            "mismatch.\n\n**Pass plain data**, never live resources: hand the task `order.id` "
            "and let it open its own session. Anything crossing an async boundary should be "
            "serialisable.\n\n**Wrong tool when** the work must survive a process restart, must "
            "be retried, must be observable, or takes more than a second or two. "
            "`BackgroundTasks` runs in the same process with no persistence and no retry — if "
            "the worker is redeployed mid-task, the work is simply lost. That is what Module "
            "18's Redis Streams queue exists for.",
        ),
        (
            "Dependency cached within a request",
            '''call_count = 0

def get_id() -> int:
    global call_count
    call_count += 1
    return call_count

@app.get("/x")
async def x(a: int = Depends(get_id), b: int = Depends(get_id)) -> dict:
    return {"a": a, "b": b}''',
            "Returns `{\"a\": 1, \"b\": 1}` — the dependency ran once, not twice.",
            [
                "Why did the second `Depends` reuse the first result?",
                "How do you force it to run twice?",
                "Why is this caching behaviour usually what you want?",
            ],
            "FastAPI **caches dependency results per request** by default, keyed on the callable "
            "and its own dependencies. Both `Depends(get_id)` entries resolve to the same cache "
            "entry.\n\n**Force re-execution:** `Depends(get_id, use_cache=False)`.\n\n**Why "
            "caching is right:** dependency graphs are usually diamonds. `get_current_user` "
            "depends on `get_session`; so does `get_permissions`; so does the route. Without "
            "caching you would open three database sessions and decode the JWT three times for "
            "one request. The cache makes a declarative dependency graph efficient. Surprises "
            "only arise when a dependency is deliberately impure — and then `use_cache=False` "
            "documents that intent explicitly.",
        ),
    ],
    "18": [
        (
            "Handler that is not idempotent",
            '''def handle_payment(payload: dict) -> None:
    charge_card(payload["card"], payload["amount"])
    mark_order_paid(payload["order_id"])''',
            "A worker crashes between the charge and the mark. After reclaim, the customer is "
            "charged twice.",
            [
                "Why does at-least-once delivery make this a certainty rather than a risk?",
                "What makes a handler idempotent?",
                "Why is exactly-once delivery not the answer?",
            ],
            "Redis Streams (and SQS, and Kafka) guarantee **at-least-once** delivery: an "
            "unacknowledged message is redelivered. A crash between two side effects means the "
            "first one is replayed. Given enough messages this is not a risk, it is a "
            "scheduled event.\n\n**Idempotent means** the second execution has no additional "
            "effect. Here: pass an **idempotency key** to the payment provider (every real one "
            "supports this), and make `mark_order_paid` a conditional update "
            "(`WHERE status != 'paid'`). Module 18's `Worker._process` also keeps a "
            "consumer-side `_processed_keys` set.\n\n**Exactly-once does not exist** across a "
            "network with independent failure domains — you cannot atomically both acknowledge a "
            "message and commit a side effect in another system. What you can have is "
            "at-least-once delivery plus idempotent handlers, which produces the same *observable "
            "result*. That combination is the real answer, and it is why idempotency is a "
            "requirement rather than a nicety.",
        ),
        (
            "Visibility timeout below processing time",
            '''broker.reclaim_stalled(consumer="worker-a", min_idle_ms=5_000)
# ... while the actual handler routinely takes 30 seconds''',
            "Long jobs run two, three, four times concurrently. Output is duplicated and the "
            "database deadlocks.",
            [
                "What does `min_idle_ms` actually mean?",
                "What is the correct way to size it?",
                "What if the processing time is unpredictable?",
            ],
            "`min_idle_ms` is how long a message may sit **unacknowledged** before another "
            "consumer may claim it. Set to 5 s while jobs take 30 s, every job is stolen roughly "
            "six times over — each thief also failing to finish in 5 s.\n\n**Size it** above your "
            "p99 processing time with headroom: if p99 is 30 s, use 90–120 s. The trade-off is "
            "recovery latency — a genuinely crashed worker's message waits that long before "
            "being retried.\n\n**Unpredictable durations:** extend the claim while working "
            "(a heartbeat that re-claims or touches the message periodically), which is what "
            "SQS's `ChangeMessageVisibility` and Celery's late-ack do. Alternatively split the "
            "job into bounded steps. Never solve it by making the timeout enormous — that "
            "destroys crash recovery.",
        ),
        (
            "Dead-lettered message left pending",
            '''def dead_letter(self, job, error: str) -> None:
    self._client.xadd(self.dlq_stream, {"error": error, **job.to_wire()})
    # no XACK''',
            "The poison message is copied to the DLQ, then reclaimed and dead-lettered again, "
            "forever. The DLQ grows without bound.",
            [
                "What is missing, and why does the loop continue?",
                "Why must the ack come after the DLQ write, not before?",
                "What monitoring would have caught this in minutes?",
            ],
            "There is no `XACK`, so the message remains in the pending-entries list. It is "
            "reclaimed after the visibility timeout, fails again, and is appended to the DLQ "
            "again.\n\n**Order matters:** write to the DLQ **first**, then ack. Acking first "
            "risks a crash in between, which loses the message entirely — and losing a poison "
            "message means losing the evidence of a bug. Duplicate DLQ entries are recoverable; "
            "a silently dropped payload is not.\n\n**Monitoring:** alert on **DLQ depth rate of "
            "change**, not just depth. A DLQ that grows steadily with no new input is this bug "
            "exactly. Also alert on pending-entry age (`XPENDING`) — a message older than a few "
            "visibility timeouts is stuck, not slow.",
        ),
        (
            "Idempotency key from an unsorted dict",
            '''def derive_key(task_type: str, payload: dict) -> str:
    return hashlib.sha256(f"{task_type}:{payload}".encode()).hexdigest()''',
            "The same logical job is occasionally enqueued twice, and it correlates with which "
            "web server handled the request.",
            [
                "Why do two identical payloads produce different keys?",
                "What is the fix?",
                "Why does the bug appear intermittent?",
            ],
            "`f\"{payload}\"` uses `dict.__repr__`, which reflects **insertion order**. "
            "`{'a':1,'b':2}` and `{'b':2,'a':1}` are equal dicts with different reprs, hence "
            "different hashes.\n\n**Fix:** canonical serialisation —\n\n```python\ncanonical = "
            "json.dumps({'t': task_type, 'p': payload}, sort_keys=True, separators=(',', ':'))\n"
            "```\n\n`sort_keys=True` makes the representation independent of construction order; "
            "the explicit `separators` removes whitespace variation.\n\n**Intermittent because** "
            "insertion order depends on the code path that built the payload — a JSON body parsed "
            "by one framework, a form parsed by another, a retry constructing the dict in a "
            "different order. Same logical job, different key, no deduplication. Module 18's "
            "`derive_idempotency_key` and its test "
            "`test_idempotency_key_ignores_dict_ordering` pin this.",
        ),
        (
            "Retry without backoff or jitter",
            '''for attempt in range(10):
    try:
        return call_upstream()
    except ConnectionError:
        continue        # immediate retry''',
            "When the upstream service recovers from an outage, it immediately falls over again.",
            [
                "Name the two distinct problems with this retry loop.",
                "What does jitter add beyond exponential backoff?",
                "What should you *not* retry?",
            ],
            "**Two problems.** (1) No delay — ten retries complete in milliseconds, hammering a "
            "struggling service and turning a blip into an outage. (2) No jitter — every client "
            "retries on the same schedule.\n\n**Jitter** breaks synchronisation. With pure "
            "exponential backoff, a thousand clients that failed at the same instant retry "
            "together at t=1s, t=2s, t=4s — a **thundering herd** that re-breaks the service the "
            "moment it recovers. Randomising each delay (`delay * random.uniform(0.5, 1.5)`, or "
            "full jitter) spreads the load smoothly.\n\n**Do not retry:** anything "
            "non-idempotent without an idempotency key, and any **4xx** client error — a 400 or "
            "403 will fail identically forever, so retrying wastes capacity and delays the real "
            "error reaching the caller. Retry timeouts, connection failures, 429s (respecting "
            "`Retry-After`) and 5xx.",
        ),
    ],
    "19": [
        (
            "Dockerfile layer cache always busted",
            '''FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "app"]''',
            "Every build reinstalls all dependencies, taking 4 minutes even for a one-character "
            "code change.",
            [
                "Which layer invalidates the cache, and why?",
                "Rewrite the relevant lines.",
                "What second problem does `COPY . .` create beyond build time?",
            ],
            "`COPY . .` copies the whole source tree, so **any** file change alters that layer's "
            "hash. Every layer after it — including `pip install` — is rebuilt.\n\n"
            "**Rewrite:**\n\n```dockerfile\nCOPY requirements.txt .\nRUN pip install --no-cache-dir "
            "-r requirements.txt\nCOPY . .\n```\n\nDependencies now reinstall only when "
            "`requirements.txt` changes.\n\n**Second problem:** `COPY . .` also ships your "
            "`.git` directory, `.env` files, test fixtures, and any local secrets into the "
            "image — where `docker history` can retrieve them even if a later layer deletes "
            "them. Always pair it with a `.dockerignore`. Image size and secret leakage are both "
            "fixed by the same file.",
        ),
        (
            "App unreachable from outside the container",
            '''CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]''',
            "`docker run -p 8000:8000 img` starts cleanly, but `curl localhost:8000` from the "
            "host gets connection refused.",
            [
                "Why can the host not reach the app?",
                "What is the fix?",
                "Why is that fix safe here but dangerous on a bare-metal host?",
            ],
            "`127.0.0.1` inside the container is the **container's own** loopback interface. "
            "Docker's port forwarding delivers traffic to the container's external interface, "
            "where nothing is listening.\n\n**Fix:** `--host 0.0.0.0` — listen on all interfaces "
            "within the container.\n\n**Safe in a container** because the network namespace is "
            "the boundary: only the ports you explicitly publish with `-p` are reachable, so "
            "`0.0.0.0` means 'all of my private interfaces', not 'the public internet'. On bare "
            "metal, `0.0.0.0` genuinely exposes the service on every NIC, and you would rely on a "
            "host firewall instead. Same flag, entirely different risk — which is why copying "
            "container advice onto a VM is a common mistake.",
        ),
        (
            "Container runs as root",
            '''FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "app"]''',
            "A container escape or a path-traversal bug gives the attacker root on the host "
            "namespace.",
            [
                "What is the default user, and why does it matter?",
                "Add the lines that fix it.",
                "What breaks if you add `USER` too early in the file?",
            ],
            "The default is **root** (uid 0). Combined with a kernel vulnerability or a "
            "misconfigured bind mount, root in the container is effectively root on the host "
            "— and even without an escape it lets an attacker write to any mounted "
            "volume.\n\n**Fix:**\n\n```dockerfile\nRUN useradd --create-home --uid 1000 appuser"
            "\nUSER appuser\n```\n\nplaced **after** the `pip install`.\n\n**Too early breaks "
            "the build:** `pip install` into system site-packages needs write access to "
            "`/usr/local/lib`, and `COPY` would create files the new user cannot read. The "
            "correct order is: install as root, `chown` what the app needs, then drop privileges "
            "with `USER` as the last step before `CMD`. Also prefer a numeric uid — some "
            "orchestrators enforce `runAsNonRoot` and cannot verify a username.",
        ),
        (
            "Healthcheck that always passes",
            '''HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 0''',
            "The orchestrator never restarts the container, even when the app is hard-down.",
            [
                "Spot the bug in one character.",
                "What is the correct exit code convention?",
                "What makes a good health endpoint, as opposed to a useless one?",
            ],
            "`|| exit 0` — the fallback exits **successfully**, so the healthcheck reports "
            "healthy no matter what. It should be `|| exit 1`.\n\n**Convention:** exit 0 = "
            "healthy, exit 1 = unhealthy. Docker also treats exit 2 as reserved. Add "
            "`--interval`, `--timeout`, `--retries` and especially `--start-period` so a slow "
            "boot is not counted as a failure.\n\n**A good health endpoint** checks that this "
            "instance can do its job — can it reach its database, is its worker pool "
            "responsive — and returns quickly without doing expensive work. A useless one returns "
            "`{\"status\": \"ok\"}` unconditionally, which only proves the process is running, "
            "something the orchestrator already knows. Distinguish **liveness** (restart me) from "
            "**readiness** (send me traffic); conflating them causes restart loops during a "
            "dependency outage.",
        ),
        (
            "Prometheus counter as a gauge",
            '''from prometheus_client import Gauge

requests_total = Gauge("requests_total", "Total requests")

@app.middleware("http")
async def count(request, call_next):
    requests_total.inc()
    return await call_next(request)''',
            "The `rate()` query in Grafana produces nonsense after every deployment.",
            [
                "Why is `Gauge` the wrong metric type here?",
                "What should it be, and what does that change?",
                "Why does a deployment specifically break the graph?",
            ],
            "A **Gauge** is for values that go up *and down* — temperature, queue depth, memory "
            "in use. A monotonically increasing total is a **Counter**, and Prometheus's "
            "`rate()`/`increase()` functions are built specifically around counter "
            "semantics.\n\n**Fix:** `Counter('requests_total', ...)`. The `_total` suffix is also "
            "the naming convention for counters, so the current code contradicts itself.\n\n"
            "**Deployments break it** because a restart resets the value to zero. `rate()` "
            "detects and corrects for counter resets — that logic is why the type exists. Applied "
            "to a gauge, Prometheus interprets the drop to zero as a real, enormous negative "
            "change, and the graph spikes or goes blank. Also add labels (`method`, `status`, "
            "`path` — bounded values only) so the counter is actually queryable; unbounded label "
            "values such as a raw URL with ids cause cardinality explosion.",
        ),
    ],
}
