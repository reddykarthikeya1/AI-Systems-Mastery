# Interactive Foundations Playground: WebSockets & Dependency Injection

> *"HTTP is sending letters back and forth; WebSockets is picking up a live telephone call."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to the **Module 17 Advanced FastAPI WebSockets DI** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Standard HTTP requires the client to ask for data each time. **WebSockets** maintain an open, bidirectional connection where server and client can push messages instantly. **Dependency Injection (DI)** is a pattern where external services (like DB sessions) are supplied to your functions automatically.

---

## 2. Micro-Code Example (3-5 Lines)

```python
# Dependency Injection concept in pure Python:
def get_db_connection():
    return "DB-Connection-Pool"

def read_user_profile(user_id: int, db=None):
    # db is injected from outside!
    print(f"Using {db} to find user {user_id}")
    return {"user_id": user_id, "name": "Sam"}

# Injecting the dependency:
db = get_db_connection()
read_user_profile(42, db=db)
```

### Line-by-Line Breakdown:
- Dependency Injection decouples your business logic from service creation, making unit testing trivial.
- In FastAPI, you declare dependencies using `Depends(get_db_connection)`.
- WebSockets use the `ws://` protocol and remain open for real-time multiplayer games, live chat, or stock tickers.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What protocol does WebSocket use for unencrypted vs encrypted connections?

<details><summary><b>Show Answer</b></summary>

`ws://` for unencrypted and `wss://` for encrypted TLS connections.
</details>

---

### Drill 2: Quick Check
Why is Dependency Injection useful for automated tests?

<details><summary><b>Show Answer</b></summary>

You can swap real database connections for lightweight in-memory test doubles without altering business logic.
</details>

---
