"""STARTER - Module 01: Python Fundamentals

CLI Financial Compound Interest & Loan Amortization Calculator.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_calculator.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/calculator.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import sys

def calculate_compound_interest(
    principal: float,
    annual_rate_percent: float,
    years: int,
    compounds_per_year: int = 12,
) -> tuple[float, float]:
    """Calculate the final investment balance and total compound interest earned.

    Formula:
    A = P * (1 + r/n)**(n*t)

    Args:
    principal: Initial investment amount in dollars.
    annual_rate_percent: Annual interest rate as a percentage (e.g. 5.0 for 5%).
    years: Investment duration in years.
    compounds_per_year: Times interest is compounded per year (default 12 for monthly).

    Returns:
    tuple[float, float]: (final_balance, total_interest_earned) rounded to 2 decimal places.

    """
    # [Tier 2] Algorithm: Compute compound monthly interest rate and derive
    #   schedule balances.
    # HINTS:
    #  - Use formula M = P * [i*(1+i)**N] / [(1+i)**N - 1] where i = rate / 12 /
    #   100.
    #  - Round financial values with round(val, 2) to match monetary cents.
    # GRADES: test_compound_interest_monthly
    # WARNING: Do not divide annual rate by 12 without dividing by 100 for
    #   percent.
    raise NotImplementedError("Module 01: implement calculate_compound_interest()")


def calculate_monthly_loan_payment(
    principal: float,
    annual_rate_percent: float,
    years: int,
) -> float:
    """Calculate the fixed monthly loan payment (Amortization Payment).

    Formula:
    M = P * [i * (1 + i)**N] / [(1 + i)**N - 1]

    Args:
    principal: Total loan amount borrowed.
    annual_rate_percent: Annual loan interest rate (e.g. 6.5 for 6.5%).
    years: Total term of the loan in years.

    Returns:
    float: Fixed monthly payment rounded to 2 decimal places.

    """
    # [Tier 2] Algorithm: Compute compound monthly interest rate and derive
    #   schedule balances.
    # HINTS:
    #  - Use formula M = P * [i*(1+i)**N] / [(1+i)**N - 1] where i = rate / 12 /
    #   100.
    #  - Round financial values with round(val, 2) to match monetary cents.
    # GRADES: test_loan_monthly_payment_standard
    # WARNING: Do not divide annual rate by 12 without dividing by 100 for
    #   percent.
    raise NotImplementedError("Module 01: implement calculate_monthly_loan_payment()")


def generate_amortization_schedule(
    principal: float,
    annual_rate_percent: float,
    years: int,
) -> list[dict[str, float]]:
    """Generate a complete month-by-month loan amortization schedule.

    Returns:
    list[dict[str, float]]: List of monthly records containing:
    - month
    - payment
    - principal
    - interest
    - remaining

    """
    # [Tier 2] Algorithm: Compute compound monthly interest rate and derive
    #   schedule balances.
    # HINTS:
    #  - Use formula M = P * [i*(1+i)**N] / [(1+i)**N - 1] where i = rate / 12 /
    #   100.
    #  - Round financial values with round(val, 2) to match monetary cents.
    # GRADES: test_amortization_schedule_completes_to_zero
    # WARNING: Do not divide annual rate by 12 without dividing by 100 for
    #   percent.
    raise NotImplementedError("Module 01: implement generate_amortization_schedule()")


def prompt_positive_float(prompt_text: str) -> float:
    """Safely prompt the user for a positive float number with continuous validation."""
    # [Tier 2] Algorithm: Implement prompt_positive_float adhering to the
    #   contract defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_compound_interest_monthly
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 01: implement prompt_positive_float()")


def prompt_positive_int(prompt_text: str) -> int:
    """Safely prompt the user for a positive integer with continuous validation."""
    # [Tier 2] Algorithm: Implement prompt_positive_int adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_compound_interest_monthly
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 01: implement prompt_positive_int()")


def print_table(schedule: list[dict[str, float]], max_rows: int = 12) -> None:
    """Print an amortization table neatly formatted with f-strings."""
    # [Tier 2] Algorithm: Implement print_table adhering to the contract defined
    #   in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_compound_interest_monthly
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 01: implement print_table()")


def main() -> int:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_compound_interest_monthly
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 01: implement main()")


if __name__ == "__main__":
    sys.exit(main())
