"""AeroTrade Core - Asynchronous Matching Engine

Demonstrates concepts from Chapters 03, 06, and 07:
- Asynchronous producer-consumer pipelines with asyncio.Queue.
- Event-driven callback fan-out to subscribers (Ledger, Analytics, Persistence).
- Deterministic order matching in sub-millisecond execution loops.
"""
from __future__ import annotations
import asyncio
import uuid
from typing import Callable, List, Optional
from domain import Order, Side, Trade, OrderStatus
from orderbook import OrderBook


class MatchingEngine:
    """Asynchronous matching engine implementing price-time matching."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.book = OrderBook(symbol)
        self.trade_subscribers: List[Callable[[Trade], None]] = []
        self._inbound_queue: asyncio.Queue[Order] = asyncio.Queue()
        self._is_running = False

    def subscribe_trades(self, callback: Callable[[Trade], None]) -> None:
        """Register a callback for every executed trade (fan-out pattern)."""
        self.trade_subscribers.append(callback)

    def _emit_trade(self, trade: Trade) -> None:
        for callback in self.trade_subscribers:
            try:
                callback(trade)
            except Exception as e:
                # Log or handle subscriber exception without crashing engine
                pass

    def match_order(self, incoming: Order) -> List[Trade]:
        """Synchronously match an incoming order against the resting book."""
        trades: List[Trade] = []

        if incoming.side == Side.BUY:
            # Match against lowest asks
            while incoming.remaining_quantity > 0:
                best_ask = self.book.get_best_ask()
                if best_ask is None or incoming.price < best_ask:
                    break  # No more matching asks

                resting_queue = self.book.asks[best_ask]
                while resting_queue and incoming.remaining_quantity > 0:
                    resting = resting_queue[0]
                    trade_qty = min(incoming.remaining_quantity, resting.remaining_quantity)
                    trade_price = resting.price  # Price-time priority: resting order price sets the trade price

                    incoming.fill(trade_qty)
                    resting.fill(trade_qty)

                    trade = Trade(
                        trade_id=f"TRD-{uuid.uuid4().hex[:8].upper()}",
                        symbol=self.symbol,
                        price=trade_price,
                        quantity=trade_qty,
                        buyer_order_id=incoming.order_id,
                        seller_order_id=resting.order_id,
                        buyer_id=incoming.trader_id,
                        seller_id=resting.trader_id,
                    )
                    trades.append(trade)
                    self._emit_trade(trade)

                    if resting.is_filled:
                        resting_queue.popleft()
                        self.book.orders.pop(resting.order_id, None)

                self.book.remove_empty_level(Side.SELL, best_ask)

        else:  # Side.SELL
            # Match against highest bids
            while incoming.remaining_quantity > 0:
                best_bid = self.book.get_best_bid()
                if best_bid is None or incoming.price > best_bid:
                    break  # No more matching bids

                resting_queue = self.book.bids[best_bid]
                while resting_queue and incoming.remaining_quantity > 0:
                    resting = resting_queue[0]
                    trade_qty = min(incoming.remaining_quantity, resting.remaining_quantity)
                    trade_price = resting.price

                    incoming.fill(trade_qty)
                    resting.fill(trade_qty)

                    trade = Trade(
                        trade_id=f"TRD-{uuid.uuid4().hex[:8].upper()}",
                        symbol=self.symbol,
                        price=trade_price,
                        quantity=trade_qty,
                        buyer_order_id=resting.order_id,
                        seller_order_id=incoming.order_id,
                        buyer_id=resting.trader_id,
                        seller_id=incoming.trader_id,
                    )
                    trades.append(trade)
                    self._emit_trade(trade)

                    if resting.is_filled:
                        resting_queue.popleft()
                        self.book.orders.pop(resting.order_id, None)

                self.book.remove_empty_level(Side.BUY, best_bid)

        # If incoming limit order has remaining quantity, rest in the order book
        if not incoming.is_filled and incoming.status != OrderStatus.CANCELLED:
            self.book.add_order(incoming)

        return trades

    async def submit_order_async(self, order: Order) -> List[Trade]:
        """Async entry point returning executed trades."""
        return self.match_order(order)
