# Module 13: Troubleshooting, FastAPI Traps & Route Conflicts

This reference guide details common development pitfalls when developing REST APIs with FastAPI.

---

## 1. Route Precedence Trap (Fixed Path vs Path Parameter)

### The Bug
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/users/me") # ❌ Never reached! Matches /users/{user_id} first with user_id="me"!
def get_current_user():
    return {"username": "current_user"}
```
**Error when calling `/users/me`:** `422 Unprocessable Entity` ("value is not a valid integer").

### Why It Happens
FastAPI evaluates routes **in top-to-bottom order**. Since `/users/{user_id}` comes first, it intercepts `/users/me` and tries to parse `"me"` as an integer.

### The Fix
Always define specific, fixed routes **before** dynamic parameterized routes:
```python
@app.get("/users/me") # ✅ Placed FIRST!
def get_current_user():
    return {"username": "current_user"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

---

## 2. The `def` vs `async def` Endpoint Performance Trap

### How FastAPI Handles Functions
* **`async def endpoint():`** FastAPI executes directly on the single-threaded Event Loop.
  - *Rule:* NEVER call synchronous blocking I/O (like `time.sleep()` or `requests.get()`) inside an `async def` endpoint!
* **`def endpoint():`** FastAPI automatically offloads execution to an internal **thread pool** (using `anyio.to_thread.run_sync`), preventing blocking calls from freezing the API.
