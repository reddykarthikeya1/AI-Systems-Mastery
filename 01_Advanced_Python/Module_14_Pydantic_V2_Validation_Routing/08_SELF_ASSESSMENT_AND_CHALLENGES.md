# Module 14: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Pydantic V2, validation modes, and discriminated unions before moving to **Module 13**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Rust Engine:** What is `pydantic-core`, and what performance advantages does it provide in Pydantic V2?
2. **Validation Modes:** What is the difference between `@field_validator(mode="before")` and `@field_validator(mode="after")`?
3. **Cross-Field Validation:** When should you use `@model_validator` instead of `@field_validator`?
4. **Polymorphic Schemas:** How do Discriminated Unions allow parsing heterogeneous JSON objects with a shared tag?
5. **Dynamic Attributes:** How does `@computed_field` differ from standard Python `@property`?
6. **Serialization:** What is the difference between `model.model_dump()` and `model.model_dump_json()`?
7. **Modular Routing:** Why is `fastapi.APIRouter` essential for structuring large production microservices?
8. **Field Constraints:** Name 4 constraints that can be defined directly inside `pydantic.Field(...)`.
9. **Stand-Alone Parsing:** What class replaced `parse_obj_as()` in Pydantic V2 for validating non-model types (like `list[MyModel]`)?
10. **Custom Error Messages:** How do you customize validation error messages returned to API clients?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
`pydantic-core` is a high-performance validation and serialization engine written in Rust, compiling schema validation into native C-ABI calls for a 5x–20x speedup.

#### Answer 2:
- `mode="before"`: Runs on raw input data *before* Pydantic performs any type coercion.
- `mode="after"`: Runs *after* Pydantic has validated and coerced the field into its target Python type.

#### Answer 3:
Use `@model_validator` when validation logic depends on multiple fields simultaneously (e.g. `end_date > start_date` or `password == confirm_password`).

#### Answer 4:
It uses a single literal tag field (e.g. `type: Literal["email", "sms"]`) to match and deserialize into the exact target subclass in $O(1)$ time without trial-and-error parsing.

#### Answer 5:
`@computed_field` properties are automatically included in JSON serialization (`model_dump()` and `model_dump_json()`) and OpenAPI schemas.

#### Answer 6:
- `model_dump()`: Returns a native Python dictionary.
- `model_dump_json()`: Directly serializes into an optimized JSON string (handled in Rust).

#### Answer 7:
`APIRouter` allows splitting route logic across multiple files (`users.py`, `billing.py`) and mounting them with custom prefixes and tags onto the root FastAPI `app`.

#### Answer 8:
`gt` / `ge` (greater than / equal), `lt` / `le` (less than / equal), `min_length` / `max_length`, and `pattern` (regex).

#### Answer 9:
**`TypeAdapter`** (e.g. `TypeAdapter(list[User]).validate_python(raw_data)`).

#### Answer 10:
By raising `ValueError("Your custom error message")` inside `@field_validator` or `@model_validator`.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Password Strength Validator

**Goal:** Implement a Pydantic model `AccountCreate` where `@field_validator("password")` verifies that password is $\ge 8$ chars and contains at least one digit and one uppercase letter.

<details>
<summary><b>Solution Code</b></summary>

```python
from pydantic import BaseModel, field_validator

class AccountCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

# Verification:
acc = AccountCreate(username="alice", password="SecurePassword1")
print("Valid Account Created:", acc.username)
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Validator that silently does nothing

```python
from pydantic import BaseModel, field_validator

class Order(BaseModel):
    quantity: int

    @field_validator("qty")            # note the name
    @classmethod
    def positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("must be positive")
        return v

print(Order(quantity=-5))
```

**Observed symptom:** In Pydantic v2 this raises at class definition. In some configurations it silently accepts `-5`.

**(a)** What is wrong with the validator?

**(b)** What protects you from this class of typo?

**(c)** What is the difference between `field_validator` and `model_validator` here?

<details>
<summary><b>Show the diagnosis</b></summary>

The validator targets `"qty"`, a field that does not exist. Pydantic v2 raises `PydanticUserError: Decorators defined with incorrect fields` at class-creation time — which is the good outcome.

**Protection:** that startup error *is* the protection, and it is why v2 is stricter than v1 (where a mismatched validator name was silently ignored). Keep `model_config = ConfigDict(extra='forbid')` on input models too, so unexpected *data* keys are rejected as well as unexpected validator targets.

**`model_validator`** runs after all fields are parsed and sees the whole object, so it is the right tool for cross-field rules ('end date must follow start date'). `field_validator` sees one value and cannot express that.

</details>

---

### D2. Validation bypassed by construct

```python
from pydantic import BaseModel, Field

class Config(BaseModel):
    workers: int = Field(ge=1, le=64)

bad = Config.model_construct(workers=-10)
print(bad.workers)
```

**Observed symptom:** Prints `-10`. The `ge=1` constraint did not apply.

**(a)** What does `model_construct` skip, and why does it exist?

**(b)** When is using it correct?

**(c)** How would this value reach production undetected?

<details>
<summary><b>Show the diagnosis</b></summary>

`model_construct` builds the instance **without running validation or coercion**. It exists as a performance escape hatch for data you have *already* validated — for example rows coming straight out of your own database, where re-validating millions of rows is pure cost.

**Correct use:** trusted, already-validated internal data on a hot path, with a comment saying so. Never for external input.

**How it reaches production:** somebody profiles a slow endpoint, sees Pydantic in the flame graph, swaps `Config(**row)` for `Config.model_construct(**row)`, and the tests still pass because the test fixtures are valid. The constraint is now decoration. Guard it with a test that asserts invalid input is rejected through the **real** construction path used by the endpoint.

</details>

---

### D3. Optional vs default confusion

```python
from pydantic import BaseModel

class Profile(BaseModel):
    nickname: str | None

print(Profile())
```

**Observed symptom:** `ValidationError: Field required` — but the field is `| None`, so you expected it to be optional.

**(a)** Why is a nullable field still required?

**(b)** What are the three distinct states you might want, and how do you spell each?

**(c)** Why does this distinction matter for a PATCH endpoint specifically?

<details>
<summary><b>Show the diagnosis</b></summary>

`str | None` describes the **type**, not the presence requirement. A field with no default is required; it just happens to accept `None` as a value.

**Three states:**
- required, may be null: `nickname: str | None`
- optional, defaults to null: `nickname: str | None = None`
- optional, distinguishable 'not supplied': `nickname: str | None = Field(default=None)` plus `model_dump(exclude_unset=True)`

**PATCH depends on it:** a partial update must tell 'set nickname to null' apart from 'do not touch nickname'. Both arrive as `None` in the model, so you need `exclude_unset=True` (or `model_fields_set`) to know which keys the client actually sent. Ignoring this is how a PATCH silently wipes fields the client never mentioned.

</details>

---

### D4. Coercion hides bad data

```python
from pydantic import BaseModel

class Item(BaseModel):
    count: int

print(Item(count="12").count)
print(Item(count=12.9).count)
```

**Observed symptom:** Prints `12`, then `12` — the float was truncated silently.

**(a)** What is Pydantic's default coercion behaviour called?

**(b)** How do you make it refuse both of these?

**(c)** Which mode should an internal service-to-service API use, and why?

<details>
<summary><b>Show the diagnosis</b></summary>

The default is **lax mode**: Pydantic coerces where the conversion is lossless-ish, so `"12"` becomes `12`, and a float with a fractional part... actually raises in v2 for `12.9` unless the value is integral. The general lesson stands: silent coercion means the type you declared is not the type you validated.

**Refuse both:** `model_config = ConfigDict(strict=True)`, or per-field `Field(strict=True)`. Then a string is not an int and a float is not an int.

**Internal APIs should use strict mode.** Lax coercion exists to be forgiving of untyped external input such as form posts and query strings, where everything arrives as a string. Between your own typed services there is no excuse for a type mismatch, and accepting one hides a real bug in the caller.

</details>

---

### D5. Model reused for input and output

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    is_admin: bool = False

# used for both the request body and the response
```

**Observed symptom:** A user POSTs `{"id": 1, "email": "x@y.z", "is_admin": true}` and becomes an administrator.

**(a)** Name the two separate vulnerabilities in reusing this model.

**(b)** What is the correct structure?

**(c)** What is this class of bug called?

<details>
<summary><b>Show the diagnosis</b></summary>

**Two problems.** (1) `is_admin` is client-settable — privilege escalation. (2) `id` is client-settable, so a caller can choose or overwrite a primary key.

**Correct structure:** separate models per direction —

```python
class UserCreate(BaseModel):      # input: only what a client may set
    email: EmailStr
    password: SecretStr

class UserOut(BaseModel):         # output: only what a client may see
    id: int
    email: EmailStr
```

The server assigns `id` and `is_admin`; they appear in neither input model.

**Named:** **mass assignment** (or over-posting). It is one of the most common API vulnerabilities precisely because sharing one model feels DRY. Module 16's RBAC service keeps input and output models strictly separate for this reason.

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
