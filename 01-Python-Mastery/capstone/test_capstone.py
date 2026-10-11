"""AeroTrade Core - Comprehensive Test Suite

Demonstrates concepts from Chapter 09:
- Comprehensive automated verification with deterministic assertions.
- Mathematical invariant testing (conservation of funds).
- Concurrency and priority verification.
"""
from __future__ import annotations
import unittest
from domain import Order, Side, OrderStatus
from orderbook import OrderBook
from matching_engine import MatchingEngine
from ledger import DoubleEntryLedger
from persistence import TradeStore
from analytics import MarketAnalytics


class TestAeroTradeCore(unittest.TestCase):

    def test_single_match(self):
        engine = MatchingEngine("AAPL")
        sell = Order("S1", "seller_1", "AAPL", Side.SELL, price=150.0, quantity=100)
        buy = Order("B1", "buyer_1", "AAPL", Side.BUY, price=150.0, quantity=100)

        engine.match_order(sell)
        trades = engine.match_order(buy)

        self.assertEqual(len(trades), 1)
        trade = trades[0]
        self.assertEqual(trade.price, 150.0)
        self.assertEqual(trade.quantity, 100)
        self.assertEqual(trade.buyer_id, "buyer_1")
        self.assertEqual(trade.seller_id, "seller_1")
        self.assertTrue(buy.is_filled)
        self.assertTrue(sell.is_filled)

    def test_partial_fill_and_resting(self):
        engine = MatchingEngine("NVDA")
        sell = Order("S1", "seller_1", "NVDA", Side.SELL, price=120.0, quantity=40)
        buy = Order("B1", "buyer_1", "NVDA", Side.BUY, price=120.0, quantity=100)

        engine.match_order(sell)
        trades = engine.match_order(buy)

        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0].quantity, 40)
        self.assertEqual(buy.remaining_quantity, 60)
        self.assertEqual(buy.status, OrderStatus.PARTIALLY_FILLED)
        # Unfilled buy rests in book
        self.assertEqual(engine.book.get_best_bid(), 120.0)

    def test_price_time_priority(self):
        engine = MatchingEngine("MSFT")
        # Two resting sells: S1 at 200.0, S2 also at 200.0 (later)
        s1 = Order("S1", "seller_1", "MSFT", Side.SELL, price=200.0, quantity=50)
        s2 = Order("S2", "seller_2", "MSFT", Side.SELL, price=200.0, quantity=50)
        engine.match_order(s1)
        engine.match_order(s2)

        # Incoming buy takes first 60 shares
        buy = Order("B1", "buyer_1", "MSFT", Side.BUY, price=205.0, quantity=60)
        trades = engine.match_order(buy)

        self.assertEqual(len(trades), 2)
        # First 50 from S1 (time priority)
        self.assertEqual(trades[0].seller_id, "seller_1")
        self.assertEqual(trades[0].quantity, 50)
        # Remaining 10 from S2
        self.assertEqual(trades[1].seller_id, "seller_2")
        self.assertEqual(trades[1].quantity, 10)
        self.assertEqual(s2.remaining_quantity, 40)

    def test_order_cancellation(self):
        book = OrderBook("GOOG")
        o1 = Order("O1", "trader_1", "GOOG", Side.BUY, price=180.0, quantity=25)
        book.add_order(o1)
        self.assertEqual(book.get_best_bid(), 180.0)

        cancelled = book.cancel_order("O1")
        self.assertIsNotNone(cancelled)
        self.assertEqual(cancelled.status, OrderStatus.CANCELLED)
        self.assertIsNone(book.get_best_bid())

    def test_ledger_conservation_invariant(self):
        ledger = DoubleEntryLedger()
        buyer_account = ledger.get_or_create_account("trader_buyer")
        seller_account = ledger.get_or_create_account("trader_seller")

        buyer_account.deposit_cash(100_000.0)
        seller_account.deposit_shares("TSLA", 500)

        initial_cash = 100_000.0
        initial_shares = 500

        engine = MatchingEngine("TSLA")
        engine.subscribe_trades(ledger.record_trade_settlement)

        sell = Order("S1", "trader_seller", "TSLA", Side.SELL, price=200.0, quantity=300)
        buy = Order("B1", "trader_buyer", "TSLA", Side.BUY, price=200.0, quantity=300)

        engine.match_order(sell)
        trades = engine.match_order(buy)
        self.assertEqual(len(trades), 1)

        # Buyer spent 60,000 cash for 300 shares
        self.assertEqual(buyer_account.cash_balance, 40_000.0)
        self.assertEqual(buyer_account.shares["TSLA"], 300)
        # Seller received 60,000 cash, has 200 shares left
        self.assertEqual(seller_account.cash_balance, 60_000.0)
        self.assertEqual(seller_account.shares["TSLA"], 200)

        # Mathematically verify conservation invariant
        self.assertTrue(ledger.verify_conservation_invariant(initial_cash, initial_shares, "TSLA"))

    def test_persistence_and_analytics(self):
        store = TradeStore(":memory:")
        engine = MatchingEngine("AMD")
        engine.subscribe_trades(store.save_trade)

        sell1 = Order("S1", "seller_1", "AMD", Side.SELL, price=100.0, quantity=10)
        sell2 = Order("S2", "seller_2", "AMD", Side.SELL, price=110.0, quantity=10)
        engine.match_order(sell1)
        engine.match_order(sell2)

        buy = Order("B1", "buyer_1", "AMD", Side.BUY, price=120.0, quantity=20)
        trades = engine.match_order(buy)

        recent = store.get_recent_trades("AMD")
        self.assertEqual(len(recent), 2)

        summary = MarketAnalytics.trade_summary(trades)
        self.assertEqual(summary["total_trades"], 2)
        self.assertEqual(summary["total_volume"], 20)
        # VWAP: (100*10 + 110*10) / 20 = 105.0
        self.assertEqual(summary["vwap"], 105.0)
        store.close()


if __name__ == "__main__":
    unittest.main()
