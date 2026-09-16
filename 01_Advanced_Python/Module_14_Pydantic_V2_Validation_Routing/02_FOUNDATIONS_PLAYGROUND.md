# Interactive Foundations Playground: Pydantic V2 & Data Validation

> *"Pydantic is the bouncer at your application's door, checking IDs before letting data enter."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to the **Module 14 Pydantic V2 Validation Routing** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Never trust external user input. Pydantic lets you define clean data schemas using standard Python class syntax and type annotations. It automatically parses, coerces, and validates incoming data.

---

## 2. Micro-Code Example (3-5 Lines)

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    username: str
    age: int = Field(ge=0, le=120)  # Must be between 0 and 120
    is_active: bool = True

# Parsing valid data (coerces "42" into integer 42!):
u = UserProfile(username="taylor", age="42")
print(u.age)        # 42 (integer)
print(u.model_dump()) # {'username': 'taylor', 'age': 42, 'is_active': True}
```

### Line-by-Line Breakdown:
- `class UserProfile(BaseModel)`: Inheriting from `BaseModel` equips the class with parsing and validation powers.
- `age: int`: Enforces integer type. Pydantic will coerce string `"42"` to int `42`.
- `Field(ge=0, le=120)`: Declares constraints (`ge`: greater than or equal, `le`: less than or equal).
- `.model_dump()`: Exports the validated model back to a standard Python dictionary.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What happens if you pass `age=-5` to the model above?

<details><summary><b>Show Answer</b></summary>

Pydantic raises a `ValidationError` with details indicating `Input should be greater than or equal to 0`.
</details>

---

### Drill 2: Quick Check
What method exports a Pydantic model to a JSON string?

<details><summary><b>Show Answer</b></summary>

`.model_dump_json()`.
</details>

---
