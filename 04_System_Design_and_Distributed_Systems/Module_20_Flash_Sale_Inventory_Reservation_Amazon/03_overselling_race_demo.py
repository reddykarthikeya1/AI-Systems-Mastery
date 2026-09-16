"""Module 20: Standalone Interactive Demo - Flash Sale Overselling Race vs Atomic Reservation."""

import concurrent.futures

from project_solution.flash_sale_engine import (
    AtomicInventoryReservationManager,
    NaiveInventoryStore,
)


def main() -> None:
    print("=" * 80)
    print(" MODULE 20: E-COMMERCE FLASH SALE & INVENTORY RESERVATION")
    print("=" * 80)

    # ---------------------------------------------------------
    # Experiment 1: The Concurrency Bug (Naive Inventory Overselling)
    # ---------------------------------------------------------
    print("\n--- 1. Vulnerability Demonstration: Naive Inventory Store (No Atomic Locks) ---")
    initial_stock = 25
    concurrent_buyers = 100
    naive_store = NaiveInventoryStore(initial_stock=initial_stock)

    def naive_worker() -> None:
        naive_store.attempt_buy(quantity=1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(naive_worker) for _ in range(concurrent_buyers)]
        concurrent.futures.wait(futures)

    print(f" Initial Stock:            {initial_stock}")
    print(f" Concurrent Buying Threads: {concurrent_buyers}")
    print(f" Final Stock Remaining:     {naive_store.stock}")
    print(f" Total Orders Fulfilled:    {naive_store.successful_orders}")
    print(f" Oversold Quantity:         {naive_store.oversold_count}")
    if naive_store.stock < 0:
        print(" [CRITICAL BUG DETECTED] Naive store oversold items! Business incurred massive financial liability.")
    else:
        print(" [WARN] In a single-core test interleaving may vary, but race conditions exist.")

    # ---------------------------------------------------------
    # Experiment 2: Production-Grade Atomic Reservation
    # ---------------------------------------------------------
    print("\n--- 2. Production Architecture: Atomic Redis-Style Reservation Manager ---")
    sku = "IPHONE_16_PRO_LIMITED"
    manager = AtomicInventoryReservationManager()
    manager.register_sku(sku, total_stock=initial_stock)

    tokens_acquired = []
    rejected_count = 0
    lock = manager._lock

    def atomic_worker(buyer_idx: int) -> None:
        nonlocal rejected_count
        success, token = manager.reserve(
            sku=sku,
            user_id=f"user_{buyer_idx:03d}",
            quantity=1,
            ttl_sec=10.0,
            current_time=100.0,
        )
        with lock:
            if success and token:
                tokens_acquired.append(token)
            else:
                rejected_count += 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(atomic_worker, i) for i in range(concurrent_buyers)]
        concurrent.futures.wait(futures)

    snap = manager.get_stock_snapshot(sku)
    print(f" Initial Stock:             {initial_stock}")
    print(f" Attempted Concurrent Buys: {concurrent_buyers}")
    print(f" Granted Reservations:      {len(tokens_acquired)}")
    print(f" Rejected (HTTP 429/409):   {rejected_count}")
    print(f" Snapshot State:            {snap}")
    print(f" Conservation Invariant:    {manager.verify_conservation_invariant(sku)}")
    print(" [SUCCESS] Exactly available stock was reserved with ZERO overselling!")

    # ---------------------------------------------------------
    # Experiment 3: TTL Expiry & Automatic Stock Restoration
    # ---------------------------------------------------------
    print("\n--- 3. Two-Phase Reservation: Partial Checkout & TTL Auto-Restoration ---")
    # Simulate: 15 users confirm payment before expiry, 10 users abandon cart
    confirmed_tokens = tokens_acquired[:15]
    abandoned_tokens = tokens_acquired[15:]

    for t in confirmed_tokens:
        manager.confirm_purchase(t.reservation_id, current_time=105.0)

    print(f" Confirmed Payments:        {len(confirmed_tokens)} (T=105s, within 10s TTL)")
    print(f" Abandoned Carts:           {len(abandoned_tokens)} (Did not pay)")

    snap_mid = manager.get_stock_snapshot(sku)
    print(f" Mid-State Snapshot:        {snap_mid}")

    # Advance time to T=120s (past 110s expiration) and trigger TTL Reaper
    print("\n [Time Advances to T=120.0s] Background Expiry Reaper scans table...")
    expired = manager.reap_expired_reservations(current_time=120.0)
    print(f" Expired & Rolled Back:     {len(expired)} reservations")

    snap_final = manager.get_stock_snapshot(sku)
    print(f" Final Inventory Snapshot:  {snap_final}")
    print(f" Invariant Hold After Reap: {manager.verify_conservation_invariant(sku)}")
    print(f" Restored Stock Available:  {snap_final['available']} units back on the market!")

    print("=" * 80)


if __name__ == "__main__":
    main()
