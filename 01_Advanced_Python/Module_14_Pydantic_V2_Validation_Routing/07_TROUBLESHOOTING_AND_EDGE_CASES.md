# Module 14: Troubleshooting, Pydantic V2 Traps & Migration Pitfalls

This reference guide details common errors and architectural changes introduced in Pydantic V2.

---

## 1. Deprecated Pydantic V1 `@validator` and `@root_validator`

### The Bug
```python
from pydantic import BaseModel, validator # ❌ Pydantic V1 syntax

class User(BaseModel):
    name: str

    @validator("name") # ⚠️ DeprecationWarning in V2
    def check_name(cls, v):
        return v
```

### The Fix in Pydantic V2
Use **`@field_validator`** with `@classmethod` and **`@model_validator`**:
```python
from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def check_name(cls, v: str) -> str:
        return v.strip().title()
```

---

## 2. `@model_validator(mode="after")` Must Return `self`

### The Bug
```python
@model_validator(mode="after")
def validate_model(self):
    if self.end_date < self.start_date:
        raise ValueError("Invalid dates")
    # ❌ Forgot to return self!
```
**Crash:** `TypeError: Model validator must return a model instance, got NoneType`

### The Fix
Always return `self`:
```python
@model_validator(mode="after")
def validate_model(self) -> "MyModel":
    if self.end_date < self.start_date:
        raise ValueError("Invalid dates")
    return self
```
