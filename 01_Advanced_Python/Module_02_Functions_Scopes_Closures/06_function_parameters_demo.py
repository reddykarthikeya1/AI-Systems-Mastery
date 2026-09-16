#!/usr/bin/env python3
"""Module 02: Function Parameters, Constraints & Unpacking Demonstration.

This script demonstrates positional-only (/), keyword-only (*), variable length
(*args, **kwargs), default arguments, and dictionary/sequence unpacking.
"""

from __future__ import annotations


def calculate_shipping(weight_kg: float, distance_km: float, /) -> float:
    """Calculate base shipping fee using positional-only arguments."""
    base_rate = 5.0
    return round(base_rate + (weight_kg * 1.5) + (distance_km * 0.1), 2)


def create_user_record(
    username: str,
    email: str,
    *,
    is_admin: bool = False,
    notify: bool = True,
) -> dict[str, str | bool]:
    """Create a user record enforcing keyword-only security flags."""
    return {
        "username": username,
        "email": email,
        "is_admin": is_admin,
        "notify": notify,
    }


def aggregate_scores(student_name: str, *scores: float, curve: float = 0.0) -> dict[str, str | float]:
    """Aggregate variable number of test scores with an optional curve."""
    average = 0.0 if not scores else sum(scores) / len(scores) + curve

    return {
        "student": student_name,
        "count": len(scores),
        "average": round(average, 2),
    }


def send_api_request(endpoint: str, method: str = "GET", **headers: str) -> None:
    """Simulate sending an API request with arbitrary HTTP headers via **kwargs."""
    print(f"\n[HTTP REQUEST] {method} {endpoint}")
    if headers:
        print("  Headers:")
        for key, value in headers.items():
            print(f"    {key}: {value}")


def main() -> None:
    print("=" * 60)
    print("  1. Positional-Only Parameters (/)")
    print("=" * 60)
    fee = calculate_shipping(12.5, 150.0)
    print(f"Shipping Fee: ${fee:.2f}")

    print("\n" + "=" * 60)
    print("  2. Keyword-Only Parameters (*)")
    print("=" * 60)
    user = create_user_record("karthik", "karthik@example.com", is_admin=True, notify=False)
    print(f"User Profile: {user}")

    print("\n" + "=" * 60)
    print("  3. Variable Positional Arguments (*args)")
    print("=" * 60)
    grades = [88.5, 92.0, 79.5, 95.0]
    # Unpack list directly using *grades
    result = aggregate_scores("Alice", *grades, curve=2.5)
    print(f"Grade Summary: {result}")

    print("\n" + "=" * 60)
    print("  4. Variable Keyword Arguments (**kwargs)")
    print("=" * 60)
    request_headers = {
        "Authorization": "Bearer secret-token-xyz",
        "Content-Type": "application/json",
        "User-Agent": "PythonClient/2026.1",
    }
    # Unpack dictionary using **request_headers
    send_api_request("/api/v1/users", method="POST", **request_headers)


if __name__ == "__main__":
    main()
