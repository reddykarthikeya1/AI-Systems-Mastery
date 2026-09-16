"""Module 01: Interactive Foundations Interactive Fundamentals Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

import random


def demo_calculator():
    print("\n--- 1. Mini Math Calculator ---")
    try:
        num1 = float(input("Enter first number: "))
        op = input("Enter operator (+, -, *, /, //, %, **): ").strip()
        num2 = float(input("Enter second number: "))

        if op == "+":
            ans = num1 + num2
        elif op == "-":
            ans = num1 - num2
        elif op == "*":
            ans = num1 * num2
        elif op == "/":
            ans = num1 / num2 if num2 != 0 else "Error: Division by Zero"
        elif op == "//":
            ans = num1 // num2 if num2 != 0 else "Error: Division by Zero"
        elif op == "%":
            ans = num1 % num2 if num2 != 0 else "Error: Division by Zero"
        elif op == "**":
            ans = num1 ** num2
        else:
            ans = "Unknown operator!"

        print(f"Result: {num1} {op} {num2} = {ans}")
    except ValueError:
        print("Invalid number entered!")

def demo_number_guessing():
    print("\n--- 2. Guess the Secret Number Game ---")
    secret = random.randint(1, 10)
    attempts = 3
    print("I picked a number between 1 and 10. Can you guess it in 3 tries?")

    while attempts > 0:
        try:
            guess = int(input(f"Your guess ({attempts} attempts left): "))
            if guess == secret:
                print("[*] BINGO! You guessed the secret number!")
                return
            elif guess < secret:
                print("Too low! Aim higher.")
            else:
                print("Too high! Aim lower.")
            attempts -= 1
        except ValueError:
            print("Please enter a valid whole number.")

    print(f"Game over! The secret number was {secret}.")

def main():
    print("=" * 60)
    print("  MODULE 01: INTERACTIVE FUNDAMENTALS PLAYGROUND  ")
    print("=" * 60)
    while True:
        print("\nChoose an activity:")
        print("1. Try the Mini Calculator")
        print("2. Play Guess the Secret Number")
        print("3. Exit")
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            demo_calculator()
        elif choice == "2":
            demo_number_guessing()
        elif choice == "3":
            print("Great job practicing! Now proceed to Module 02.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended. Happy coding!")
