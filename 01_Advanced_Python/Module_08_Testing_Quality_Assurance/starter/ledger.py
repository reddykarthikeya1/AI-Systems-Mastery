"""STARTER - Module 08: Testing Quality Assurance

Enterprise Financial Ledger Engine.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_ledger.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/ledger.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

class CurrencyConverterGateway(Protocol):
    """Interface for external currency exchange rate services."""

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        ...



@dataclass
class Entry:
    """Represents an immutable ledger transaction record."""
    entry_id: str
    entry_type: str  # "CREDIT" or "DEBIT"
    amount: float
    currency: str
    timestamp: str


class FinancialLedger:
    """Enterprise double-entry compliant ledger with strict balance invariants."""

    def __init__(self, account_id: str, base_currency: str = "USD", converter: CurrencyConverterGateway | None = None) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_deposit_and_withdraw_math
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 08: implement FinancialLedger.__init__()")


    @property
    def balance(self) -> float:
        # [Tier 2] Algorithm: Implement FinancialLedger.balance adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_balance_invariant_matches_sum_of_deposits
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 08: implement FinancialLedger.balance()")


    def deposit(self, amount: float, currency: str = "USD") -> Entry:
        """Deposits funds into ledger, automatically converting currency if needed."""
        # [Tier 2] Algorithm: Implement FinancialLedger.deposit adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_deposit_and_withdraw_math
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 08: implement FinancialLedger.deposit()")


    def withdraw(self, amount: float) -> Entry:
        """Withdraws funds from ledger, enforcing non-negative balance."""
        # [Tier 2] Algorithm: Implement FinancialLedger.withdraw adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_deposit_and_withdraw_math
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 08: implement FinancialLedger.withdraw()")


    def get_statement(self) -> list[Entry]:
        # [Tier 1] Algorithm: Implement FinancialLedger.get_statement adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_deposit_and_withdraw_math
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 08: implement FinancialLedger.get_statement()")



def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_deposit_and_withdraw_math
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 08: implement main()")


if __name__ == "__main__":
    main()
