"""STARTER - Module 12: Python Internals Bytecode Memory

CPython Bytecode & Memory Optimization Profiler.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_internals_profiler.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/internals_profiler.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import ast
import dis
import sys
from collections import Counter
from collections.abc import Callable
from typing import Any

class InternalsProfiler:
    """Introspection and static analysis engine for CPython execution."""

    @staticmethod
    def analyze_bytecode(func: Callable[..., Any]) -> dict[str, Any]:
        """Disassembles a callable into opcodes and aggregates instruction metrics."""
        # [Tier 2] Algorithm: Implement InternalsProfiler.analyze_bytecode
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_bytecode_analysis
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 12: implement InternalsProfiler.analyze_bytecode()")


    @staticmethod
    def compare_instance_memory(std_instance: Any, slotted_instance: Any) -> dict[str, Any]:
        """Compares RAM footprint between standard __dict__ instance and slotted instance."""
        # [Tier 2] Algorithm: Implement
        #   InternalsProfiler.compare_instance_memory adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_compare_instance_memory
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 12: implement InternalsProfiler.compare_instance_memory()")


    @staticmethod
    def audit_ast_security(source_code: str) -> list[str]:
        """Performs static AST security checks for dangerous function calls and mutable defaults."""
        # [Tier 2] Algorithm: Implement InternalsProfiler.audit_ast_security
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_audit_ast_security_catches_eval_and_mutable_defaults
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 12: implement InternalsProfiler.audit_ast_security()")



def sample_calculation(x: int, y: int) -> int:
    # [Tier 2] Algorithm: Implement sample_calculation adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_bytecode_analysis
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 12: implement sample_calculation()")


class RegularUser:

    def __init__(self, uid: int, name: str) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_bytecode_analysis
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 12: implement RegularUser.__init__()")



class SlottedUser:
    __slots__ = ("name", "uid")

    def __init__(self, uid: int, name: str) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_bytecode_analysis
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 12: implement SlottedUser.__init__()")



def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_bytecode_analysis
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 12: implement main()")


if __name__ == "__main__":
    main()
