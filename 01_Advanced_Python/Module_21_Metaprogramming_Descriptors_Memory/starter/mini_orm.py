"""STARTER - Module 21: Metaprogramming Descriptors Memory

Zero-Dependency Declarative Mini-ORM Framework.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_mini_orm.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/mini_orm.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
from typing import Any, ClassVar

class Field:
    """Base descriptor representing a database column."""

    def __init__(self, sql_type: str = "TEXT", primary_key: bool = False, nullable: bool = True) -> None:
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.name = ""
        self.storage = ""


    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage = f"_{name}"


    def __get__(self, instance: object, owner: type) -> Any:
        # [Tier 1] Algorithm: Implement Field.__get__ adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_schema_generation
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 21: implement Field.__get__()")


    def __set__(self, instance: object, value: Any) -> None:
        # [Tier 2] Algorithm: Implement Field.__set__ adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_schema_generation
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 21: implement Field.__set__()")


    def validate(self, value: Any) -> None:
        # [Tier 1] Algorithm: Validate input arguments against constraints and
        #   raise specific exception.
        # HINTS:
        #  - Check boundary conditions (e.g. non-empty string, positive integer,
        #   range).
        #  - Raise ValueError or TypeError with actionable descriptive messages.
        # GRADES: test_schema_generation
        # WARNING: Never swallow validation errors or return None instead of
        #   raising.
        raise NotImplementedError("Module 21: implement Field.validate()")



class StringField(Field):

    def __init__(self, max_length: int = 255, **kwargs) -> None:
        super().__init__(sql_type=f"VARCHAR({max_length})", **kwargs)
        self.max_length = max_length


    def validate(self, value: Any) -> None:
        # [Tier 1] Algorithm: Validate input arguments against constraints and
        #   raise specific exception.
        # HINTS:
        #  - Check boundary conditions (e.g. non-empty string, positive integer,
        #   range).
        #  - Raise ValueError or TypeError with actionable descriptive messages.
        # GRADES: test_schema_generation
        # WARNING: Never swallow validation errors or return None instead of
        #   raising.
        raise NotImplementedError("Module 21: implement StringField.validate()")



class IntegerField(Field):

    def __init__(self, **kwargs) -> None:
        super().__init__(sql_type="INTEGER", **kwargs)


    def validate(self, value: Any) -> None:
        # [Tier 1] Algorithm: Validate input arguments against constraints and
        #   raise specific exception.
        # HINTS:
        #  - Check boundary conditions (e.g. non-empty string, positive integer,
        #   range).
        #  - Raise ValueError or TypeError with actionable descriptive messages.
        # GRADES: test_schema_generation
        # WARNING: Never swallow validation errors or return None instead of
        #   raising.
        raise NotImplementedError("Module 21: implement IntegerField.validate()")



class FloatField(Field):

    def __init__(self, **kwargs) -> None:
        super().__init__(sql_type="REAL", **kwargs)


    def validate(self, value: Any) -> None:
        # [Tier 1] Algorithm: Validate input arguments against constraints and
        #   raise specific exception.
        # HINTS:
        #  - Check boundary conditions (e.g. non-empty string, positive integer,
        #   range).
        #  - Raise ValueError or TypeError with actionable descriptive messages.
        # GRADES: test_schema_generation
        # WARNING: Never swallow validation errors or return None instead of
        #   raising.
        raise NotImplementedError("Module 21: implement FloatField.validate()")



class Model:
    """Declarative Base Model utilizing __init_subclass__."""
    _fields: ClassVar[dict[str, Field]] = {}
    _table_name: str = ""

    def __init_subclass__(cls, table_name: str | None = None, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._table_name = table_name or cls.__name__.lower() + "s"
        cls._fields = {}
        for key, val in list(cls.__dict__.items()):
            if isinstance(val, Field):
                cls._fields[key] = val


    def __init__(self, **kwargs) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_schema_generation
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 21: implement Model.__init__()")


    def to_dict(self) -> dict[str, Any]:
        # [Tier 1] Algorithm: Implement Model.to_dict adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_model_to_dict_method
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 21: implement Model.to_dict()")


    def as_insert_sql(self) -> str:
        # [Tier 2] Algorithm: Implement Model.as_insert_sql adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_instance_creation_and_insert_sql
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 21: implement Model.as_insert_sql()")


    @classmethod
    def get_create_table_sql(cls) -> str:
        # [Tier 1] Algorithm: Implement Model.get_create_table_sql adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_schema_generation
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 21: implement Model.get_create_table_sql()")



class User(Model, table_name="users"):
    id = IntegerField(primary_key=True)
    username = StringField(max_length=50, nullable=False)
    score = FloatField(nullable=False)


def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_schema_generation
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 21: implement main()")


if __name__ == "__main__":
    main()
