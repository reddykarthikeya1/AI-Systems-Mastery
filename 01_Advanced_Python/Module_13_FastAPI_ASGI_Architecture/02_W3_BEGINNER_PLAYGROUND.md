# W3Schools-Style Playground: FastAPI & ASGI Architecture

> *"An API is a restaurant menu; FastAPI is the ultra-fast kitchen that cooks and serves your responses."*

Welcome to the **Module 13 FastAPI ASGI Architecture** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

An API (Application Programming Interface) lets frontend apps and other servers communicate via HTTP. FastAPI uses ASGI (Asynchronous Server Gateway Interface) to handle requests concurrently with automatic JSON documentation.

---

## 2. Micro-Code Example (3-5 Lines)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "available": True}
```

### Line-by-Line Breakdown:
- `app = FastAPI()`: Initializes your web application instance.
- `@app.get("/")`: Route decorator mapping HTTP `GET` requests on path `/` to the `home()` function.
- `{item_id}`: Path parameter extracted directly from the URL.
- `item_id: int`: Type hint that instructs FastAPI to validate that `item_id` is a valid integer automatically.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What HTTP method is used to read data vs submit new data?

<details><summary><b>Show Answer</b></summary>

`GET` is used to retrieve data; `POST` is used to submit new data.
</details>

---

### Drill 2: Quick Check
What does ASGI stand for?

<details><summary><b>Show Answer</b></summary>

Asynchronous Server Gateway Interface.
</details>

---
