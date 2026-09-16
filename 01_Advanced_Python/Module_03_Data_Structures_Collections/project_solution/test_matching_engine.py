"""Unit tests for the High-Frequency Order Matching Engine."""

from __future__ import annotations

import pytest
from matching_engine import OrderMatchingEngine


def test_order_placement_and_spread() -> None:
    """Test non-crossing orders rest on order book without generating trades."""
    engine = OrderMatchingEngine()
    _, trades_sell = engine.place_order("Seller_1", "SELL", price=100.0, quantity=10)
    _, trades_buy = engine.place_order("Buyer_1", "BUY", price=95.0, quantity=10)

    assert len(trades_sell) == 0
    assert len(trades_buy) == 0

    depth = engine.get_order_book_depth()
    assert len(depth["bids"]) == 1
    assert len(depth["asks"]) == 1
    assert depth["bids"][0] == (95.0, 10)
    assert depth["asks"][0] == (100.0, 10)


def test_exact_price_and_volume_match() -> None:
    """Test exact volume match clears orders completely."""
    engine = OrderMatchingEngine()
    engine.place_order("Seller_1", "SELL", price=50.0, quantity=20)
    _, trades = engine.place_order("Buyer_1", "BUY", price=50.0, quantity=20)

    assert len(trades) == 1
    trade = trades[0]
    assert trade.price == 50.0
    assert trade.quantity == 20
    assert trade.buyer == "Buyer_1"
    assert trade.seller == "Seller_1"

    # Both books should now be empty
    depth = engine.get_order_book_depth()
    assert len(depth["bids"]) == 0
    assert len(depth["asks"]) == 0


def test_multi_level_partial_sweep() -> None:
    """Test aggressive buy order sweeping through multiple ask levels."""
    engine = OrderMatchingEngine()
    engine.place_order("Seller_A", "SELL", price=10.0, quantity=5)
    engine.place_order("Seller_B", "SELL", price=11.0, quantity=10)
    engine.place_order("Seller_C", "SELL", price=12.0, quantity=15)

    # Buy 20 units at limit 11.50 (should fill 5 @ 10, 10 @ 11, and rest remaining 5 @ 11.50)
    order, trades = engine.place_order("Whale_Buyer", "BUY", price=11.50, quantity=20)

    assert len(trades) == 2
    assert trades[0].price == 10.0
    assert trades[0].quantity == 5
    assert trades[1].price == 11.0
    assert trades[1].quantity == 10

    # 5 units remaining in buy order
    assert order.quantity == 5
    depth = engine.get_order_book_depth()
    assert depth["bids"][0] == (11.50, 5)
    assert depth["asks"][0] == (12.0, 15)


def test_invalid_order_parameters_raise_error() -> None:
    """Test validation errors on negative prices or zero quantities."""
    engine = OrderMatchingEngine()
    with pytest.raises(ValueError):
        engine.place_order("Trader", "BUY", price=-10.0, quantity=5)
    with pytest.raises(ValueError):
        engine.place_order("Trader", "SELL", price=10.0, quantity=0)
def test_empty_order_book_depth() -> None:
    """Test depth on freshly instantiated matching engine returns empty bids and asks."""
    engine = OrderMatchingEngine()
    depth = engine.get_order_book_depth()
    assert depth["bids"] == []
    assert depth["asks"] == []


def test_time_priority_at_identical_prices() -> None:
    """Test price-time priority: earlier order at same price executes first."""
    engine = OrderMatchingEngine()
    # First seller at 100
    engine.place_order("Seller_Early", "SELL", price=100.0, quantity=10)
    # Second seller at 100
    engine.place_order("Seller_Late", "SELL", price=100.0, quantity=10)

    # Buyer buys 10 at 100 -> should match Seller_Early
    _, trades = engine.place_order("Buyer_1", "BUY", price=100.0, quantity=10)
    assert len(trades) == 1
    assert trades[0].seller == "Seller_Early"
    assert trades[0].quantity == 10

    # Remaining in asks should be Seller_Late
    depth = engine.get_order_book_depth()
    assert depth["asks"] == [(100.0, 10)]


def test_volume_by_trader_and_price_stats() -> None:
    """Test execution stats tracking across multiple trades."""
    engine = OrderMatchingEngine()
    engine.place_order("Alice", "SELL", price=50.0, quantity=15)
    engine.place_order("Bob", "BUY", price=50.0, quantity=10)

    assert engine.volume_by_trader["Alice"] == 10
    assert engine.volume_by_trader["Bob"] == 10
    assert engine.trades_by_price[50.0] == 10


def test_multiple_bids_sorted_descending() -> None:
    """Test bids depth ordering maintains highest bid first."""
    engine = OrderMatchingEngine()
    engine.place_order("Buyer_A", "BUY", price=90.0, quantity=5)
    engine.place_order("Buyer_B", "BUY", price=95.0, quantity=10)
    engine.place_order("Buyer_C", "BUY", price=92.0, quantity=8)

    depth = engine.get_order_book_depth()
    prices = [p for p, _ in depth["bids"]]
    assert prices == [95.0, 92.0, 90.0]


def test_multiple_asks_sorted_ascending() -> None:
    """Test asks depth ordering maintains lowest ask first."""
    engine = OrderMatchingEngine()
    engine.place_order("Seller_A", "SELL", price=110.0, quantity=5)
    engine.place_order("Seller_B", "SELL", price=105.0, quantity=10)
    engine.place_order("Seller_C", "SELL", price=108.0, quantity=8)

    depth = engine.get_order_book_depth()
    prices = [p for p, _ in depth["asks"]]
    assert prices == [105.0, 108.0, 110.0]


def test_aggressive_seller_sweeps_multiple_bids() -> None:
    """Test aggressive sell order sweeping downward through multiple bid levels."""
    engine = OrderMatchingEngine()
    engine.place_order("Buyer_1", "BUY", price=100.0, quantity=10)
    engine.place_order("Buyer_2", "BUY", price=98.0, quantity=10)

    # Sell 15 at limit 95 -> fills 10 @ 100, 5 @ 98
    order, trades = engine.place_order("Seller_Whale", "SELL", price=95.0, quantity=15)
    assert len(trades) == 2
    assert trades[0].price == 100.0
    assert trades[0].quantity == 10
    assert trades[1].price == 98.0
    assert trades[1].quantity == 5
    assert order.quantity == 0

    depth = engine.get_order_book_depth()
    assert depth["bids"] == [(98.0, 5)]
