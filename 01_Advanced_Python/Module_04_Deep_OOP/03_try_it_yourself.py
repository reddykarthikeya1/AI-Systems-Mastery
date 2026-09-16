"""Module 04: Interactive Foundations Interactive OOP Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

class BankAccount:
    """A simple, clean bank account class."""
    def __init__(self, owner: str, initial_balance: float = 0.0):
        self.owner = owner
        self.balance = initial_balance
        self.history = [f"Account opened with ${initial_balance:.2f}"]

    def deposit(self, amount: float) -> str:
        if amount <= 0:
            return "[X] Deposit must be greater than zero."
        self.balance += amount
        self.history.append(f"Deposited ${amount:.2f}")
        return f"[OK] Deposited ${amount:.2f}. New Balance: ${self.balance:.2f}"

    def withdraw(self, amount: float) -> str:
        if amount <= 0:
            return "[X] Withdrawal must be greater than zero."
        if amount > self.balance:
            return f"[X] Insufficient funds! Current balance is only ${self.balance:.2f}."
        self.balance -= amount
        self.history.append(f"Withdrew ${amount:.2f}")
        return f"[OK] Withdrew ${amount:.2f}. New Balance: ${self.balance:.2f}"

def main():
    print("=" * 60)
    print("  MODULE 04: INTERACTIVE OOP BANK ACCOUNT SIMULATOR [BANK]")
    print("=" * 60)

    name = input("Enter account holder name: ").strip() or "Taylor"
    account = BankAccount(name, 100.0)
    print(f"Created BankAccount for {account.owner} with $100.00 initial balance.")

    while True:
        print(f"\nCurrent Balance: ${account.balance:.2f}")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. View Transaction History")
        print("4. Exit")
        cmd = input("Select action (1-4): ").strip()

        if cmd == "1":
            try:
                amt = float(input("Deposit amount: $"))
                print(account.deposit(amt))
            except ValueError:
                print("Invalid number!")
        elif cmd == "2":
            try:
                amt = float(input("Withdrawal amount: $"))
                print(account.withdraw(amt))
            except ValueError:
                print("Invalid number!")
        elif cmd == "3":
            print("\n--- Statement History ---")
            for entry in account.history:
                print(f"  * {entry}")
        elif cmd == "4":
            print("Great job learning OOP! Proceed to Module 05.")
            break

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended. Happy coding!")
