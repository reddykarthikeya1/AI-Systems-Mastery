"""AeroTrade Core - Limit Order Book

Demonstrates concepts from Chapters 02 and 07:
- Data structure selection: dict for O(1) order lookup, sorted price levels, and FIFO deque for price-time priority.
- Encapsulation and invariant maintenance.
"""
from __future__ import annotations
from collections import deque
from typing import Dict, List, Optional, Tuple
from domain import Order, Side, OrderStatus


class OrderBook:
    """In-memory limit order book maintaining strict Price-Time Priority."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        # price -> deque of Orders at that price level
        self.bids: Dict[float, deque[Order]] = {}  # Buy orders (wants highest price)
        self.asks: Dict[float, deque[Order]] = {}  # Sell orders (wants lowest price)
        # order_id -> Order pointer for O(1) lookups and cancellations
        self.orders: Dict[str, Order] = {}

    def get_best_bid(self) -> Optional[float]:
        return max(self.bids.keys()) if self.bids else None

    def get_best_ask(self) -> Optional[float]:
        return min(self.asks.keys()) if self.asks else None

    def add_order(self, order: Order) -> None:
        """Adds a resting limit order to the appropriate side."""
        if order.symbol != self.symbol:
            raise ValueError(f"Order symbol {order.symbol} does not match order book {self.symbol}")

        book = self.bids if order.side == Side.BUY else self.asks
        if order.price not in book:
            book[order.price] = deque()
        book[order.price].append(order)
        self.orders[order.order_id] = order

    def cancel_order(self, order_id: str) -> Optional[Order]:
        """Cancels a resting order in O(1) by reference."""
        order = self.orders.pop(order_id, None)
        if not order:
            return None

        order.status = OrderStatus.CANCELLED
        book = self.bids if order.side == Side.BUY else self.asks
        if order.price in book:
            queue = book[order.price]
            if order in queue:
                queue.remove(order)
            if not queue:
                del book[order.price]
        return order

    def remove_empty_level(self, side: Side, price: float) -> None:
        book = self.bids if side == Side.BUY else self.asks
        if price in book and len(book[price]) == 0:
            del book[price]

    def get_depth(self, levels: int = 5) -> Tuple[List[Tuple[float, int]], List[Tuple[float, int]]]:
        """Returns top N levels of (price, total_quantity) for bids and asks."""
        sorted_bids = sorted(self.bids.keys(), reverse=True)[:levels]
        bid_depth = [(p, sum(o.remaining_quantity for o in self.bids[p])) for p in sorted_bids]

        sorted_asks = sorted(self.asks.keys())[:levels]
        ask_depth = [(p, sum(o.remaining_quantity for o in self.asks[p])) for p in sorted_asks]

        return bid_depth, ask_depth
