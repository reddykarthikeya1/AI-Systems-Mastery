# Debug Lab Answers: Module 13

<details>
<summary>Bug 1: Route definition order shadowing</summary>

### Root Cause
FastAPI (Starlette) evaluates routes in the order they are defined. `/items/{item_id}` matches any string including `"special"`.

### Fix
Place specific static routes before dynamic path parameter routes:
```python
@app.get("/items/special")
def get_special_item():
    return {"item_id": "special", "type": "special_offer"}

@app.get("/items/{item_id}")
def get_item(item_id: str):
    return {"item_id": item_id, "type": "dynamic"}
```
</details>

<details>
<summary>Bug 2: Blocking synchronous call in async def</summary>

### Root Cause
When a route is declared `async def`, FastAPI executes it directly on the main event loop thread. Calling blocking I/O or `time.sleep()` blocks the entire event loop.

### Fix
Either declare the route as regular `def` (so FastAPI automatically runs it in an external threadpool) or use `await asyncio.sleep()`:
```python
# Option A (Non-blocking async):
@app.get("/slow-calc")
async def slow_calculation():
    await asyncio.sleep(1.0)
    return {"status": "complete"}

# Option B (Offloaded to worker threadpool):
@app.get("/slow-calc")
def slow_calculation():
    time.sleep(1.0)
    return {"status": "complete"}
```
</details>
