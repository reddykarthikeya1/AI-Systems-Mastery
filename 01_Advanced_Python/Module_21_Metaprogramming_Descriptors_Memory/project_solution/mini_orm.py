#!/usr/bin/env python3
"""Zero-Dependency Declarative Mini-ORM Framework.

Module 19 (Metaprogramming & Descriptors) Turnkey Project Implementation.
Demonstrates Descriptors (__get__, __set__, __set_name__), __init_subclass__,
and declarative SQL schema generation.
"""

from __future__ import annotations

from typing import Any, ClassVar


class Field:
    """Base descriptor representing a database column."""

    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True) -> None:
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.name = ""
        self.storage = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage = f"_{name}"

    def __get__(self, instance: object, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage, None)

    def __set__(self, instance: object, value: Any) -> None:
        if value is None and not self.nullable:
            raise ValueError(f"Field '{self.name}' cannot be NULL")
        self.validate(value)
        setattr(instance, self.storage, value)

    def validate(self, value: Any) -> None:
        pass


class StringField(Field):
    def __init__(self, max_length: int = 255, **kwargs) -> None:
        super().__init__(sql_type=f"VARCHAR({max_length})", **kwargs)
        self.max_length = max_length

    def validate(self, value: Any) -> None:
        if value is not None and (not isinstance(value, str) or len(value) > self.max_length):
            raise TypeError(f"Field '{self.name}' must be a string up to {self.max_length} characters")


class IntegerField(Field):
    def __init__(self, **kwargs) -> None:
        super().__init__(sql_type="INTEGER", **kwargs)

    def validate(self, value: Any) -> None:
        if value is not None and not isinstance(value, int):
            raise TypeError(f"Field '{self.name}' must be an integer (Got: {type(value).__name__})")


class FloatField(Field):
    def __init__(self, **kwargs) -> None:
        super().__init__(sql_type="REAL", **kwargs)

    def validate(self, value: Any) -> None:
        if value is not None and not isinstance(value, (int, float)):
            raise TypeError(f"Field '{self.name}' must be a float (Got: {type(value).__name__})")


class Model:
    """Declarative Base Model utilizing __init_subclass__."""
    _fields: ClassVar[dict[str, Field]] = {}
    _table_name: str = ""

    def __init_subclass__(cls, table_name: str | None = None, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._table_name = table_name or cls.__name__.lower() + "s"
        cls._fields = {}

        # Collect descriptor fields
        for key, val in list(cls.__dict__.items()):
            if isinstance(val, Field):
                cls._fields[key] = val

    def __init__(self, **kwargs) -> None:
        for name, field in self._fields.items():
            if name in kwargs:
                setattr(self, name, kwargs[name])
            elif not field.nullable and not field.primary_key:
                raise ValueError(f"Missing required field: '{name}'")

    def to_dict(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self._fields}

    def as_insert_sql(self) -> str:
        columns = list(self._fields.keys())
        values = [repr(getattr(self, c)) if getattr(self, c) is not None else "NULL" for c in columns]
        return f"INSERT INTO {self._table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"

    @classmethod
    def get_create_table_sql(cls) -> str:
        col_defs = []
        for name, field in cls._fields.items():
            pk = " PRIMARY KEY" if field.primary_key else ""
            null = " NOT NULL" if not field.nullable else ""
            col_defs.append(f"  {name} {field.sql_type}{pk}{null}")
        return f"CREATE TABLE {cls._table_name} (\n" + ",\n".join(col_defs) + "\n);"


# Example Model
class User(Model, table_name="users"):
    id = IntegerField(primary_key=True)
    username = StringField(max_length=50, nullable=False)
    score = FloatField(nullable=False)


def main() -> None:
    print("=" * 65)
    print("      ZERO-DEPENDENCY DECLARATIVE MINI-ORM DEMO")
    print("=" * 65)

    print(User.get_create_table_sql())

    user = User(id=1, username="alice_metaprogrammer", score=98.5)
    print(f"\nUser Instance Dict: {user.to_dict()}")
    print(f"Generated SQL     : {user.as_insert_sql()}")


if __name__ == "__main__":
    main()
