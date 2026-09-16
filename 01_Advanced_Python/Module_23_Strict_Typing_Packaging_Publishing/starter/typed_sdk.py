"""STARTER - Module 23: Strict Typing Packaging Publishing

Production-Grade Fully Typed Python SDK Library.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_typed_sdk.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/typed_sdk.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable
T = TypeVar("T")
R = TypeVar("R")

@dataclass(frozen=True)
class ApiResponse(Generic[T]):
    """Type-safe immutable API response envelope."""
    status_code: int
    data: T | None = None
    error_message: str | None = None

    @property
    def is_success(self) -> bool:
        # [Tier 2] Algorithm: Implement ApiResponse.is_success adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_api_response_is_success_property
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 23: implement ApiResponse.is_success()")



@runtime_checkable
class TransportProtocol(Protocol):
    """Protocol for mockable HTTP transport clients."""

    def send_request(self, method: str, endpoint: str, payload: dict | None = None) -> dict[str, Any]:
        ...



class MockHTTPTransport:
    """Mock implementation satisfying TransportProtocol."""

    def __init__(self, responses: dict[str, dict[str, Any]] | None = None) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_transport_protocol_conformance
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 23: implement MockHTTPTransport.__init__()")


    def send_request(self, method: str, endpoint: str, payload: dict | None = None) -> dict[str, Any]:
        # [Tier 2] Algorithm: Implement MockHTTPTransport.send_request adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_mock_http_transport_custom_responses
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 23: implement MockHTTPTransport.send_request()")



class TypedEnterpriseClient:
    """Fully typed enterprise API client."""

    def __init__(self, transport: TransportProtocol) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_transport_protocol_conformance
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 23: implement TypedEnterpriseClient.__init__()")


    def get_resource(self, endpoint: str, transform: Callable[[dict[str, Any]], T]) -> ApiResponse[T]:
        # [Tier 1] Algorithm: Implement TypedEnterpriseClient.get_resource
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_typed_client_successful_fetch
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 23: implement TypedEnterpriseClient.get_resource()")



@dataclass
class UserDTO:
    id: int
    username: str
    tier: str


def parse_user(payload: dict[str, Any]) -> UserDTO:
    # [Tier 1] Algorithm: Normalize raw input data structure into typed domain
    #   representation.
    # HINTS:
    #  - Handle missing optional keys with sensible defaults (.get() pattern).
    #  - Coerce primitive data types safely and strip surrounding whitespace.
    # GRADES: test_user_dto_parsing_and_field_integrity
    # WARNING: Watch for unexpected null or None values in optional fields.
    raise NotImplementedError("Module 23: implement parse_user()")


def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_transport_protocol_conformance
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 23: implement main()")


if __name__ == "__main__":
    main()
