"""
================================================================================
LAB 01: Multi-Threaded Race Condition Hunter & Fix
================================================================================
Zero-Prerequisite Intuition:
Imagine two bank clerks trying to update the exact same bank account with $1,000.
Clerk A reads the balance ($1,000), prepares to add $500, but takes a coffee sip.
Meanwhile, Clerk B reads the balance ($1,000) and adds $300, saving $1,300 to disk.
Clerk A wakes up and writes $1,500 over Clerk B's deposit!
$300 has vanished into thin air! This is a Race Condition.

Run this script to reproduce the bug live, and see how a Mutex Lock fixes it!
================================================================================
"""

import threading
import time

# --- PART 1: The Broken Implementation (Race Condition Disaster) ---
class UnsafeBankAccount:
    def __init__(self, initial_balance: int = 0):
        self.balance = initial_balance

    def deposit(self, amount: int):
        # 1. Read current balance
        current = self.balance
        # Simulate slight OS thread scheduling preemption delay
        time.sleep(0.00001)
        # 2. Write back mutated balance
        self.balance = current + amount

def run_broken_simulation():
    print("--- [EXPERIMENT 1] Running Unsafe Multi-Threaded Deposits ---")
    account = UnsafeBankAccount(initial_balance=0)
    threads = []
    
    # Spawn 50 threads, each depositing $10. Expected total = $500
    for _ in range(50):
        t = threading.Thread(target=account.deposit, args=(10,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Expected Final Balance: $500")
    print(f"ACTUAL Final Balance:   ${account.balance}")
    if account.balance < 500:
        print("[ALERT] DISASTER: Race condition occurred! Money was silently corrupted!")
    else:
        print("Got lucky on this OS thread slice (run again to observe corruption).")


# --- PART 2: The Senior Engineer Fix (Mutex Lock) ---
class SafeBankAccount:
    def __init__(self, initial_balance: int = 0):
        self.balance = initial_balance
        self._lock = threading.Lock() # The Mutex (Bathroom Key)

    def deposit(self, amount: int):
        # 'with self._lock' guarantees that ONLY ONE thread can execute this block at a time!
        with self._lock:
            current = self.balance
            time.sleep(0.00001)
            self.balance = current + amount

def run_safe_simulation():
    print("\n--- [EXPERIMENT 2] Running Thread-Safe Deposits with Mutex Lock ---")
    account = SafeBankAccount(initial_balance=0)
    threads = []

    # Spawn 50 threads, each depositing $10. Expected total = $500
    for _ in range(50):
        t = threading.Thread(target=account.deposit, args=(10,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Expected Final Balance: $500")
    print(f"ACTUAL Final Balance:   ${account.balance}")
    assert account.balance == 500, "Math invariant violated!"
    print("[SUCCESS] 100% thread-safe balance guaranteed under extreme concurrency!")

if __name__ == "__main__":
    run_broken_simulation()
    run_safe_simulation()
