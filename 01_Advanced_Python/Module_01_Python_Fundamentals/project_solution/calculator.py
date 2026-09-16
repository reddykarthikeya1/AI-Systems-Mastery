#!/usr/bin/env python3
"""CLI Financial Compound Interest & Loan Amortization Calculator.

Module 01 Turnkey Project Implementation.
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
    if principal < 0 or annual_rate_percent < 0 or years < 0 or compounds_per_year <= 0:
        raise ValueError("Inputs must be non-negative, and compounding frequency must be > 0.")

    rate_decimal = annual_rate_percent / 100.0
    total_compounds = compounds_per_year * years

    final_balance = principal * ((1.0 + (rate_decimal / compounds_per_year)) ** total_compounds)
    interest_earned = final_balance - principal

    return round(final_balance, 2), round(interest_earned, 2)


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
    if principal <= 0 or years <= 0:
        raise ValueError("Principal and loan term must be greater than zero.")
    if annual_rate_percent < 0:
        raise ValueError("Interest rate cannot be negative.")

    total_months = years * 12

    # Zero interest loan edge case:
    if annual_rate_percent == 0.0:
        return round(principal / total_months, 2)

    monthly_rate = (annual_rate_percent / 100.0) / 12.0
    factor = (1.0 + monthly_rate) ** total_months
    monthly_payment = principal * (monthly_rate * factor) / (factor - 1.0)

    return round(monthly_payment, 2)


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
    monthly_payment = calculate_monthly_loan_payment(principal, annual_rate_percent, years)
    monthly_rate = (annual_rate_percent / 100.0) / 12.0
    total_months = years * 12

    remaining_balance = principal
    schedule: list[dict[str, float]] = []

    for month in range(1, total_months + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment

        # Handle final month rounding adjustments
        if remaining_balance <= principal_payment or month == total_months:
            principal_payment = remaining_balance
            monthly_payment = principal_payment + interest_payment
            remaining_balance = 0.0
        else:
            remaining_balance -= principal_payment

        schedule.append({
            "month": float(month),
            "payment": round(monthly_payment, 2),
            "principal": round(principal_payment, 2),
            "interest": round(interest_payment, 2),
            "remaining": round(max(0.0, remaining_balance), 2),
        })

    return schedule


def prompt_positive_float(prompt_text: str) -> float:
    """Safely prompt the user for a positive float number with continuous validation."""
    while True:
        raw_input = input(prompt_text).strip()
        try:
            val = float(raw_input)
            if val < 0:
                print("  [Error] Value cannot be negative. Please try again.")
                continue
            return val
        except ValueError:
            print("  [Error] Invalid number! Please enter valid digits.")


def prompt_positive_int(prompt_text: str) -> int:
    """Safely prompt the user for a positive integer with continuous validation."""
    while True:
        raw_input = input(prompt_text).strip()
        try:
            val = int(raw_input)
            if val <= 0:
                print("  [Error] Value must be at least 1. Please try again.")
                continue
            return val
        except ValueError:
            print("  [Error] Invalid integer! Please enter a whole number.")


def print_table(schedule: list[dict[str, float]], max_rows: int = 12) -> None:
    """Print an amortization table neatly formatted with f-strings."""
    print(f"\n{'Month':<6} | {'Payment':>12} | {'Principal':>12} | {'Interest':>12} | {'Remaining Balance':>18}")
    print("-" * 72)
    for row in schedule[:max_rows]:
        print(
            f"{int(row['month']):<6} | "
            f"${row['payment']:>11.2f} | "
            f"${row['principal']:>11.2f} | "
            f"${row['interest']:>11.2f} | "
            f"${row['remaining']:>17.2f}"
        )
    if len(schedule) > max_rows:
        print(f"... and {len(schedule) - max_rows} more months (Total term: {len(schedule)} months)")


def main() -> int:
    print("=" * 68)
    print("       FINANCIAL COMPOUND INTEREST & LOAN CALCULATOR")
    print("=" * 68)

    while True:
        print("\nMain Menu:")
        print("  [1] Calculate Compound Savings Interest")
        print("  [2] Calculate Loan Monthly Payment & Amortization Schedule")
        print("  [3] Exit Application")

        choice = input("\nEnter choice (1, 2, or 3): ").strip()

        match choice:
            case "1":
                print("\n--- Compound Savings Calculator ---")
                p = prompt_positive_float("Enter Initial Principal Amount ($): ")
                r = prompt_positive_float("Enter Annual Interest Rate (%): ")
                t = prompt_positive_int("Enter Investment Duration (Years): ")
                freq = prompt_positive_int("Compounding frequency per year (12=monthly, 4=quarterly, 1=annual): ")

                balance, interest = calculate_compound_interest(p, r, t, freq)
                print("\n" + "=" * 48)
                print(f"  Initial Investment  : ${p:,.2f}")
                print(f"  Total Interest Gain : ${interest:,.2f}")
                print(f"  Final Total Balance : ${balance:,.2f}")
                print("=" * 48)

            case "2":
                print("\n--- Loan Amortization Calculator ---")
                p = prompt_positive_float("Enter Loan Amount Borrowed ($): ")
                if p == 0:
                    print("Loan amount cannot be zero.")
                    continue
                r = prompt_positive_float("Enter Annual Interest Rate (%): ")
                t = prompt_positive_int("Enter Loan Term (Years): ")

                payment = calculate_monthly_loan_payment(p, r, t)
                total_paid = payment * (t * 12)
                total_interest = total_paid - p

                print("\n" + "=" * 48)
                print(f"  Monthly Fixed Payment : ${payment:,.2f}")
                print(f"  Total Principal Paid  : ${p:,.2f}")
                print(f"  Total Interest Paid   : ${total_interest:,.2f}")
                print(f"  Total Overall Cost    : ${total_paid:,.2f}")
                print("=" * 48)

                view_table = input("\nDisplay amortization table preview? (y/n): ").strip().lower()
                if view_table == "y":
                    schedule = generate_amortization_schedule(p, r, t)
                    print_table(schedule, max_rows=12)

            case "3" | "exit" | "quit":
                print("\nThank you for using the Financial Calculator. Goodbye!")
                break

            case _:
                print("  [Error] Unrecognized option. Please select 1, 2, or 3.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
