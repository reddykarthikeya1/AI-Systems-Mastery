"""STARTER - Module 03: Data Structures Collections

In-Memory High-Frequency Order Matching Engine Simulator.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_matching_engine.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/matching_engine.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import heapq
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Literal

@dataclass
class Order:
    """Represents a limit order in the order book."""
    order_id: int
    trader: str
    side: Literal["BUY", "SELL"]
    price: float
    quantity: int
    timestamp: float


@dataclass
class Trade:
    """Represents an executed trade between buyer and seller."""
    trade_id: int
    buy_order_id: int
    sell_order_id: int
    buyer: str
    seller: str
    price: float
    quantity: int
    timestamp: float


class OrderMatchingEngine:
    """In-memory order matching engine implementing Price-Time Priority."""

    def __init__(self) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_order_placement_and_spread
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 03: implement OrderMatchingEngine.__init__()")


    def place_order(
        self,
        trader: str,
        side: Literal["BUY", "SELL"],
        price: float,
        quantity: int,
    ) -> tuple[Order, list[Trade]]:
        """Submit a new limit order and immediately execute matches if spread crosses."""
        # [Tier 2] Algorithm: Implement OrderMatchingEngine.place_order adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_order_placement_and_spread
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 03: implement OrderMatchingEngine.place_order()")


    def _match_order(self, incoming: Order) -> list[Trade]:
        """Match incoming order against resting orders in the opposite heap."""
        # [Tier 2] Algorithm: Implement OrderMatchingEngine._match_order
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_order_placement_and_spread
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 03: implement OrderMatchingEngine._match_order()")


    def get_order_book_depth(self) -> dict[str, list[tuple[float, int]]]:
        """Return current resting order book depth for bids and asks."""
        # [Tier 1] Algorithm: Implement OrderMatchingEngine.get_order_book_depth
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_order_placement_and_spread
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 03: implement OrderMatchingEngine.get_order_book_depth()")



def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_order_placement_and_spread
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 03: implement main()")


if __name__ == "__main__":
    main()
