"""AeroTrade Core - Interactive CLI Simulation

Run with:
    python 01-Python-Mastery/capstone/demo.py

Simulates live market order flow, prints real-time order book depth,
settles trades in the double-entry ledger, persists records, and displays
columnar market analytics.
"""
from __future__ import annotations
import random
import time
from domain import Order, Side
from matching_engine import MatchingEngine
from ledger import DoubleEntryLedger
from persistence import TradeStore
from analytics import MarketAnalytics


def run_simulation():
    print("=" * 70)
    print("  AEROTRADE CORE: HIGH-THROUGHPUT MATCHING & LEDGER SIMULATION")
    print("=" * 70)

    symbol = "BTC-USD"
    engine = MatchingEngine(symbol)
    ledger = DoubleEntryLedger()
    store = TradeStore(":memory:")

    # Register persistence and ledger fanout callbacks
    engine.subscribe_trades(ledger.record_trade_settlement)
    engine.subscribe_trades(store.save_trade)

    # Seed traders with initial balances
    traders = [f"TRADER_{i:02d}" for i in range(1, 6)]
    for t in traders:
        acc = ledger.get_or_create_account(t)
        acc.deposit_cash(500_000.0)
        acc.deposit_shares(symbol, 10)

    initial_total_cash = 5 * 500_000.0
    initial_total_shares = 5 * 10

    print(f"\n[INIT] Seeded 5 traders with $500,000 cash and 10 {symbol} each.")
    print(f"       System Initial Cash: ${initial_total_cash:,.2f} | Shares: {initial_total_shares}")

    # Seed resting order book
    base_price = 65000.0
    print("\n[STEP 1] Generating Resting Order Book...")
    resting_orders = [
        Order("BID-01", "TRADER_01", symbol, Side.BUY, base_price - 50.0, 2),
        Order("BID-02", "TRADER_02", symbol, Side.BUY, base_price - 100.0, 5),
        Order("BID-03", "TRADER_03", symbol, Side.BUY, base_price - 150.0, 8),
        Order("ASK-01", "TRADER_04", symbol, Side.SELL, base_price + 50.0, 3),
        Order("ASK-02", "TRADER_05", symbol, Side.SELL, base_price + 100.0, 4),
        Order("ASK-03", "TRADER_01", symbol, Side.SELL, base_price + 150.0, 6),
    ]

    for order in resting_orders:
        engine.match_order(order)
        store.save_order(order)

    bids, asks = engine.book.get_depth(levels=3)
    print("\n  === ORDER BOOK DEPTH ===")
    print("  ASKS (Sellers):")
    for price, qty in reversed(asks):
        print(f"    ${price:,.2f}  |  {qty} units")
    print("  ------------------------- [SPREAD: ${:,.2f}]".format(asks[0][0] - bids[0][0]))
    print("  BIDS (Buyers):")
    for price, qty in bids:
        print(f"    ${price:,.2f}  |  {qty} units")

    # Execute market crossing orders
    print("\n[STEP 2] Executing Aggressive Inbound Orders...")
    aggressive_buy = Order("MKT-BUY-01", "TRADER_02", symbol, Side.BUY, price=base_price + 120.0, quantity=5)
    print(f"\n-> Incoming BUY Order: {aggressive_buy.quantity} {symbol} @ limit ${aggressive_buy.price:,.2f}")
    trades = engine.match_order(aggressive_buy)

    print(f"   Matches Executed: {len(trades)}")
    for t in trades:
        print(f"   * MATCH: {t.quantity} units @ ${t.price:,.2f} | Buyer: {t.buyer_id} <-> Seller: {t.seller_id}")

    # Check conservation invariant
    print("\n[STEP 3] Verifying Conservation Invariant...")
    ledger.verify_conservation_invariant(initial_total_cash, initial_total_shares, symbol)
    print("   [OK] Conservation invariant passed: $0 cash created/destroyed, 0 shares lost.")

    # Columnar Market Analytics
    print("\n[STEP 4] Real-Time Market Analytics:")
    recent_trades = [t for t in ledger.trade_history]
    summary = MarketAnalytics.trade_summary(recent_trades)
    print(f"   Total Volume Executed : {summary['total_volume']} {symbol}")
    print(f"   VWAP                  : ${summary['vwap']:,.2f}")
    print(f"   Min Executed Price    : ${summary['min_price']:,.2f}")
    print(f"   Max Executed Price    : ${summary['max_price']:,.2f}")
    print(f"   Analytics Engine      : {summary['engine_backend']}")

    print("\n" + "=" * 70)
    print("  SIMULATION COMPLETED CLEANLY WITH ZERO ERRORS.")
    print("=" * 70)
    store.close()


if __name__ == "__main__":
    run_simulation()
