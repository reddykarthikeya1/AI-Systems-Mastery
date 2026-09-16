# Interactive Foundations Playground: SQLAlchemy 2.0 & Database Persistence

> *"An ORM maps Python objects to SQL rows, so you query databases in pure Python."*

Welcome to the **Module 15 SQLAlchemy Alembic Database** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Relational databases store tables and rows. An ORM (Object Relational Mapper) like SQLAlchemy lets you define Python classes that automatically map to SQL tables, allowing you to insert and query data without writing raw SQL strings.

---

## 2. Micro-Code Example (3-5 Lines)

```python
import sqlite3

# Create an in-memory SQLite database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create table & insert row
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Taylor')")
conn.commit()

# Query rows
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())  # [(1, 'Taylor')]
```

### Line-by-Line Breakdown:
- `sqlite3.connect(":memory:")`: Creates a fast, zero-installation SQL database in RAM.
- `cursor.execute(...)`: Sends a SQL command to the database engine.
- `conn.commit()`: Writes changes permanently to the transaction log.
- `cursor.fetchall()`: Retrieves all matching rows as Python tuples.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What does ORM stand for?

<details><summary><b>Show Answer</b></summary>

Object-Relational Mapping.
</details>

---

### Drill 2: Quick Check
Why must you call `commit()` after an INSERT or UPDATE statement?

<details><summary><b>Show Answer</b></summary>

To finalize the transaction; without `commit()`, changes will be rolled back when the connection closes.
</details>

---
