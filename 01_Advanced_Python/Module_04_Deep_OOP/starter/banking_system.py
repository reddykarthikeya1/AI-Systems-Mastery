"""STARTER - Module 04: Deep OOP

Multi-Tier Banking & Investment System.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_banking_system.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/banking_system.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
from abc import ABC, abstractmethod

class Currency:
    """Represents a monetary amount with currency enforcement and operator overloading."""

    def __init__(self, amount: float | int, code: str = "USD") -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 04: implement Currency.__init__()")


    def __repr__(self) -> str:
        # [Tier 2] Algorithm: Implement Currency.__repr__ adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_repr_and_equality
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Currency.__repr__()")


    def __str__(self) -> str:
        # [Tier 2] Algorithm: Implement Currency.__str__ adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Currency.__str__()")


    def __eq__(self, other: object) -> bool:
        # [Tier 2] Algorithm: Implement Currency.__eq__ adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_repr_and_equality
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Currency.__eq__()")


    def __lt__(self, other: Currency) -> bool:
        # [Tier 2] Algorithm: Implement Currency.__lt__ adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_invalid_multiplier_type
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Currency.__lt__()")


    def __le__(self, other: Currency) -> bool:
        # [Tier 2] Algorithm: Implement Currency.__le__ adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Currency.__le__()")


    def __add__(self, other: Currency) -> Currency:
        # [Tier 2] Algorithm: Implement Currency.__add__ adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Currency.__add__()")


    def __sub__(self, other: Currency) -> Currency:
        # [Tier 2] Algorithm: Implement Currency.__sub__ adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Currency.__sub__()")


    def __mul__(self, multiplier: float) -> Currency:
        # [Tier 2] Algorithm: Implement Currency.__mul__ adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_invalid_multiplier_type
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Currency.__mul__()")



class Account(ABC):
    """Abstract Base Class defining the contract for all bank accounts."""

    def __init__(self, account_number: str, owner_name: str, initial_balance: Currency) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 04: implement Account.__init__()")


    @property
    def balance(self) -> Currency:
        """Read-only property for account balance."""
        # [Tier 2] Algorithm: Implement Account.balance adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Account.balance()")


    def deposit(self, amount: Currency) -> None:
        """Deposit funds into account."""
        # [Tier 2] Algorithm: Implement Account.deposit adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_savings_account_deposit_and_interest
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Account.deposit()")


    @abstractmethod
    def withdraw(self, amount: Currency) -> None:
        """Abstract withdrawal method enforcing account-specific overdraft/rules."""
        # [Tier 2] Algorithm: Implement Account.withdraw adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_savings_account_deposit_and_interest
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Account.withdraw()")


    @abstractmethod
    def apply_monthly_process(self) -> None:
        """Abstract monthly calculation (e.g. interest compounding or fees)."""
        # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs
        #   and aggregating results.
        # HINTS:
        #  - Process items sequentially or in batches, applying transformations.
        #  - Track successes and errors separately for a clean summary.
        # GRADES: test_savings_account_deposit_and_interest
        # WARNING: Ensure exceptions from individual items do not crash the
        #   entire batch.
        raise NotImplementedError("Module 04: implement Account.apply_monthly_process()")


    def get_transaction_history(self) -> list[str]:
        # [Tier 1] Algorithm: Implement Account.get_transaction_history adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_account_transaction_history_tracking
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Account.get_transaction_history()")



class SavingsAccount(Account):
    """Savings account featuring annual compound yield and withdrawal limits."""

    def __init__(
        self,
        account_number: str,
        owner_name: str,
        initial_balance: Currency,
        annual_rate_percent: float = 4.5,
    ) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 04: implement SavingsAccount.__init__()")


    def withdraw(self, amount: Currency) -> None:
        # [Tier 2] Algorithm: Implement SavingsAccount.withdraw adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_savings_account_deposit_and_interest
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement SavingsAccount.withdraw()")


    def apply_monthly_process(self) -> None:
        # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs
        #   and aggregating results.
        # HINTS:
        #  - Process items sequentially or in batches, applying transformations.
        #  - Track successes and errors separately for a clean summary.
        # GRADES: test_savings_account_deposit_and_interest
        # WARNING: Ensure exceptions from individual items do not crash the
        #   entire batch.
        raise NotImplementedError("Module 04: implement SavingsAccount.apply_monthly_process()")



class CheckingAccount(Account):
    """Checking account supporting overdraft protection and transaction fees."""

    def __init__(
        self,
        account_number: str,
        owner_name: str,
        initial_balance: Currency,
        overdraft_limit: Currency | None = None,
        transaction_fee: Currency | None = None,
    ) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 04: implement CheckingAccount.__init__()")


    def withdraw(self, amount: Currency) -> None:
        # [Tier 2] Algorithm: Implement CheckingAccount.withdraw adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_savings_account_deposit_and_interest
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement CheckingAccount.withdraw()")


    def apply_monthly_process(self) -> None:
        # [Tier 2] Algorithm: Coordinate execution pipeline, processing inputs
        #   and aggregating results.
        # HINTS:
        #  - Process items sequentially or in batches, applying transformations.
        #  - Track successes and errors separately for a clean summary.
        # GRADES: test_savings_account_deposit_and_interest
        # WARNING: Ensure exceptions from individual items do not crash the
        #   entire batch.
        raise NotImplementedError("Module 04: implement CheckingAccount.apply_monthly_process()")



class Bank:
    """Manages bank accounts and executes multi-account transactions."""

    def __init__(self, bank_name: str = "Apex National Bank") -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_currency_arithmetic_and_comparison
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 04: implement Bank.__init__()")


    def add_account(self, account: Account) -> None:
        # [Tier 2] Algorithm: Implement Bank.add_account adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_bank_transfers_and_aggregations
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Bank.add_account()")


    def get_account(self, account_number: str) -> Account | None:
        # [Tier 1] Algorithm: Implement Bank.get_account adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_bank_get_account_retrieval
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Bank.get_account()")


    def transfer(self, from_acc_num: str, to_acc_num: str, amount: Currency) -> bool:
        # [Tier 2] Algorithm: Implement Bank.transfer adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_bank_transfers_and_aggregations
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Bank.transfer()")


    def calculate_total_deposits(self, currency_code: str = "USD") -> Currency:
        # [Tier 2] Algorithm: Implement Bank.calculate_total_deposits adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_bank_transfers_and_aggregations
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 04: implement Bank.calculate_total_deposits()")



def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_currency_arithmetic_and_comparison
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 04: implement main()")


if __name__ == "__main__":
    main()
