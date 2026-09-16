#!/usr/bin/env python3
"""Module 09: Threading, Race Conditions & Locks Demonstration.

This script demonstrates thread creation, race condition vulnerabilities,
synchronization via threading.Lock, and rate-limiting with threading.Semaphore.
"""

from __future__ import annotations

import threading
import time


class UnsafeBankVault:
    """Demonstrates lost updates from unsynchronized thread race conditions."""
    def __init__(self) -> None:
        self.balance = 0

    def deposit(self, amount: int) -> None:
        current = self.balance
        # Simulate slight OS thread context switch interruption
        time.sleep(0.00001)
        self.balance = current + amount


class SafeBankVault:
    """Thread-safe vault using threading.Lock."""
    def __init__(self) -> None:
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self, amount: int) -> None:
        with self.lock:
            current = self.balance
            time.sleep(0.00001)
            self.balance = current + amount


def demo_race_conditions() -> None:
    print("=" * 60)
    print("  1. Race Condition vs Thread-Safe Lock Synchronization")
    print("=" * 60)

    # 1. Test Unsafe Vault
    unsafe_vault = UnsafeBankVault()
    threads = [threading.Thread(target=unsafe_vault.deposit, args=(10,)) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Unsafe Vault Balance (Expected 1000) : {unsafe_vault.balance}  <-- Data Corruption!")

    # 2. Test Safe Vault
    safe_vault = SafeBankVault()
    threads = [threading.Thread(target=safe_vault.deposit, args=(10,)) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Safe Vault Balance   (Expected 1000) : {safe_vault.balance}  <-- Thread-Safe!")


def demo_semaphore_rate_limiting() -> None:
    print("\n" + "=" * 60)
    print("  2. Concurrency Rate-Limiting with threading.Semaphore")
    print("=" * 60)

    # Allow at most 2 threads to access database connection pool simultaneously
    db_semaphore = threading.Semaphore(2)

    def access_database(thread_id: int) -> None:
        with db_semaphore:
            print(f"  [Thread #{thread_id}] Acquired DB connection. Querying...")
            time.sleep(0.05)
            print(f"  [Thread #{thread_id}] Released DB connection.")

    threads = [threading.Thread(target=access_database, args=(i,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def main() -> None:
    demo_race_conditions()
    demo_semaphore_rate_limiting()


if __name__ == "__main__":
    main()
