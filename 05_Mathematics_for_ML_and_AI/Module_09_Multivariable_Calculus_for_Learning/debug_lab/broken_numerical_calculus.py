"""Numerical calculus with three planted defects.

Runs to completion, raises nothing, exits 0.
"""
from __future__ import annotations


def forward_difference(f, x, h):
    return (f(x + h) - f(x)) / h


def central_difference(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


def gradient_descent(gradient, start, learning_rate, steps):
    x = start
    history = [x]
    for _ in range(steps):
        x = x - learning_rate * gradient(x)
        history.append(x)
    return x, history


def main():
    print("=" * 66)
    print("NUMERICAL CALCULUS - accuracy report")
    print("=" * 66)

    def f(x):
        return x ** 3

    true_derivative = 3.0 * 2.0 ** 2      # f'(2) = 12

    print()
    print("[1] Forward vs central difference at a sensible step size")
    for h in (1e-2, 1e-4, 1e-6):
        fwd = forward_difference(f, 2.0, h)
        cen = central_difference(f, 2.0, h)
        print(f"    h={h:<8.0e} forward err={abs(fwd - true_derivative):.3e}"
              f"   central err={abs(cen - true_derivative):.3e}")

    print()
    print("[2] Making the step size smaller still")
    for h in (1e-10, 1e-13, 1e-15, 1e-17):
        cen = central_difference(f, 2.0, h)
        print(f"    h={h:<8.0e} estimate={cen:<22.12f} err={abs(cen - true_derivative):.3e}")

    print()
    print("[3] Gradient descent on f(x) = x^2, minimum at 0")
    for lr in (0.1, 0.9, 1.01):
        final, history = gradient_descent(lambda x: 2 * x, start=1.0,
                                          learning_rate=lr, steps=60)
        print(f"    lr={lr:<5} final x={final:<24.6e} |x| shrank: {abs(final) < 1.0}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()
