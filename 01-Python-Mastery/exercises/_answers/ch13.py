"""Chapter 13 - FastAPI and Pydantic v2 (needs `pip install "pydantic>=2"`; the runner skips this chapter without it).

1. User: a model with validation rules.
2. parse_or_errors: turn a ValidationError into a simple list of 'field: message' strings.
3. Item (debugging): numeric strings are silently coerced; make the model strict.
"""
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

BUGGY = {
    "Item": '''class Item(BaseModel):
    """Item(name: str, qty: int) that REJECTS qty='3' (a string) instead of coercing it, and rejects qty < 1."""
    name: str
    qty: int''',
}

class User(BaseModel):
    """User(email: str, age: int). email must contain exactly one '@' and be stored lowercased and stripped;
    age must be 0..150."""
    email: str
    age: int = Field(ge=0, le=150)

    @field_validator("email")
    @classmethod
    def _email(cls, v):
        v = v.strip().lower()
        if v.count("@") != 1:
            raise ValueError("must contain exactly one @")
        return v

class Item(BaseModel):
    """Item(name: str, qty: int) that REJECTS qty='3' (a string) instead of coercing it, and rejects qty < 1."""
    model_config = ConfigDict(strict=True)
    name: str
    qty: int = Field(ge=1)


def parse_or_errors(model, data):
    """Return (instance, []) when `data` validates, else (None, sorted list of 'field: message') using the first loc element as field."""
    try:
        return model.model_validate(data), []
    except ValidationError as e:
        return None, sorted(f"{err['loc'][0]}: {err['msg']}" for err in e.errors())


def t_user_normalises_email(m):
    u, errs = m.parse_or_errors(m.User, {"email": "  Bob@Example.COM ", "age": 30})
    assert errs == [] and u.email == "bob@example.com"


def t_user_rejects_bad_values(m):
    _, errs = m.parse_or_errors(m.User, {"email": "a@b@c", "age": 200})
    assert [e.split(":")[0] for e in errs] == ["age", "email"]
    _, errs = m.parse_or_errors(m.User, {"age": 1})
    assert errs == ["email: Field required"]


def t_parse_or_errors_success_shape(m):
    inst, errs = m.parse_or_errors(m.User, {"email": "a@b.c", "age": 1})
    assert isinstance(inst, m.User) and errs == []


def t_item_is_strict(m):
    assert m.Item(name="x", qty=3).qty == 3
    for bad in ({"name": "x", "qty": "3"}, {"name": "x", "qty": 0}):
        try:
            m.Item(**bad)
        except Exception as e:
            assert type(e).__name__ == "ValidationError"
            continue
        raise AssertionError(f"{bad} must be rejected")
