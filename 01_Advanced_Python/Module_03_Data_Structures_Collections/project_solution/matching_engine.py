#!/usr/bin/env python3
"""In-Memory High-Frequency Order Matching Engine Simulator.

Module 03 Turnkey Project Implementation.
Demonstrates heapq, collections.deque, collections.Counter, and defaultdict.
"""

from __future__ import annotations

import heapq
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Literal


@dataclass
class Order:
    """Represents a limit order in the order book."""
    order_id: int
    trader: str
    side: Literal["BUY", "SELL"]
    price: float
    quantity: int
    timestamp: float


@dataclass
class Trade:
    """Represents an executed trade between buyer and seller."""
    trade_id: int
    buy_order_id: int
    sell_order_id: int
    buyer: str
    seller: str
    price: float
    quantity: int
    timestamp: float


class OrderMatchingEngine:
    """In-memory order matching engine implementing Price-Time Priority."""

    def __init__(self) -> None:
        # Min-heap for Sell orders (Lowest price first)
        self._sell_heap: list[tuple[float, float, int]] = []
        # Max-heap for Buy orders (Highest price first, simulated with -price)
        self._buy_heap: list[tuple[float, float, int]] = []

        # Fast order lookup by ID: id -> Order
        self._orders: dict[int, Order] = {}

        # Trades history
        self._trades: list[Trade] = []
        self._trade_counter: int = 1
        self._order_sequence: int = 1

        # Execution stats using Counter and defaultdict
        self.volume_by_trader: Counter[str] = Counter()
        self.trades_by_price: defaultdict[float, int] = defaultdict(int)

    def place_order(
        self,
        trader: str,
        side: Literal["BUY", "SELL"],
        price: float,
        quantity: int,
    ) -> tuple[Order, list[Trade]]:
        """Submit a new limit order and immediately execute matches if spread crosses."""
        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive numbers.")

        order = Order(
            order_id=self._order_sequence,
            trader=trader,
            side=side,
            price=round(price, 2),
            quantity=quantity,
            timestamp=time.perf_counter(),
        )
        self._order_sequence += 1
        self._orders[order.order_id] = order

        executed_trades = self._match_order(order)
        return order, executed_trades

    def _match_order(self, incoming: Order) -> list[Trade]:
        """Match incoming order against resting orders in the opposite heap."""
        executed: list[Trade] = []

        if incoming.side == "BUY":
            while incoming.quantity > 0 and self._sell_heap:
                best_ask_price, _ask_timestamp, sell_order_id = self._sell_heap[0]

                # Check if buyer is willing to pay seller's asking price
                if incoming.price >= best_ask_price:
                    resting_sell = self._orders.get(sell_order_id)
                    if not resting_sell or resting_sell.quantity == 0:
                        heapq.heappop(self._sell_heap)
                        continue

                    # Determine trade match volume
                    trade_qty = min(incoming.quantity, resting_sell.quantity)
                    trade = Trade(
                        trade_id=self._trade_counter,
                        buy_order_id=incoming.order_id,
                        sell_order_id=resting_sell.order_id,
                        buyer=incoming.trader,
                        seller=resting_sell.trader,
                        price=best_ask_price,  # Resting order price takes priority
                        quantity=trade_qty,
                        timestamp=time.perf_counter(),
                    )
                    self._trade_counter += 1
                    executed.append(trade)
                    self._trades.append(trade)

                    # Update stats
                    self.volume_by_trader[incoming.trader] += trade_qty
                    self.volume_by_trader[resting_sell.trader] += trade_qty
                    self.trades_by_price[best_ask_price] += trade_qty

                    # Deduct quantities
                    incoming.quantity -= trade_qty
                    resting_sell.quantity -= trade_qty

                    if resting_sell.quantity == 0:
                        heapq.heappop(self._sell_heap)
                else:
                    break  # Spread not crossed

            # If incoming order still has remaining volume, place on Buy heap
            if incoming.quantity > 0:
                heapq.heappush(self._buy_heap, (-incoming.price, incoming.timestamp, incoming.order_id))

        else:  # incoming.side == "SELL"
            while incoming.quantity > 0 and self._buy_heap:
                neg_bid_price, _bid_timestamp, buy_order_id = self._buy_heap[0]
                best_bid_price = -neg_bid_price

                # Check if seller is willing to sell at or below buyer's bid price
                if incoming.price <= best_bid_price:
                    resting_buy = self._orders.get(buy_order_id)
                    if not resting_buy or resting_buy.quantity == 0:
                        heapq.heappop(self._buy_heap)
                        continue

                    trade_qty = min(incoming.quantity, resting_buy.quantity)
                    trade = Trade(
                        trade_id=self._trade_counter,
                        buy_order_id=resting_buy.order_id,
                        sell_order_id=incoming.order_id,
                        buyer=resting_buy.trader,
                        seller=incoming.trader,
                        price=best_bid_price,
                        quantity=trade_qty,
                        timestamp=time.perf_counter(),
                    )
                    self._trade_counter += 1
                    executed.append(trade)
                    self._trades.append(trade)

                    self.volume_by_trader[incoming.trader] += trade_qty
                    self.volume_by_trader[resting_buy.trader] += trade_qty
                    self.trades_by_price[best_bid_price] += trade_qty

                    incoming.quantity -= trade_qty
                    resting_buy.quantity -= trade_qty

                    if resting_buy.quantity == 0:
                        heapq.heappop(self._buy_heap)
                else:
                    break

            if incoming.quantity > 0:
                heapq.heappush(self._sell_heap, (incoming.price, incoming.timestamp, incoming.order_id))

        return executed

    def get_order_book_depth(self) -> dict[str, list[tuple[float, int]]]:
        """Return current resting order book depth for bids and asks."""
        bids = [(-p, self._orders[oid].quantity) for p, _, oid in self._buy_heap if self._orders[oid].quantity > 0]
        asks = [(p, self._orders[oid].quantity) for p, _, oid in self._sell_heap if self._orders[oid].quantity > 0]
        return {
            "bids": sorted(bids, key=lambda x: x[0], reverse=True),
            "asks": sorted(asks, key=lambda x: x[0]),
        }


def main() -> None:
    print("=" * 65)
    print("       HIGH-FREQUENCY IN-MEMORY MATCHING ENGINE DEMO")
    print("=" * 65)

    engine = OrderMatchingEngine()

    print("\n1. Submitting resting SELL orders into the order book:")
    engine.place_order("Seller_A", "SELL", price=102.50, quantity=50)
    engine.place_order("Seller_B", "SELL", price=101.00, quantity=100)
    engine.place_order("Seller_C", "SELL", price=103.00, quantity=75)

    depth = engine.get_order_book_depth()
    print(f"Current Asks (Best price first): {depth['asks']}")

    print("\n2. Submitting aggressive BUY order (crosses spread):")
    order, trades = engine.place_order("Buyer_Z", "BUY", price=102.50, quantity=120)

    print(f"Incoming Order: {order.trader} {order.side} {order.price} -> Executed {len(trades)} trade(s):")
    for t in trades:
        print(f"  [TRADE #{t.trade_id}] {t.quantity} units @ ${t.price:.2f} (Buyer: {t.buyer}, Seller: {t.seller})")

    print("\n3. Trading Volume Leaderboard (collections.Counter):")
    for trader, vol in engine.volume_by_trader.most_common():
        print(f"  {trader:<12}: {vol} units traded")


if __name__ == "__main__":
    main()
