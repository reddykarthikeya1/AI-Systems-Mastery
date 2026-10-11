"""AeroTrade Core - Dual-Mode Transactional Persistence

Demonstrates concepts from Chapter 12:
- Relational schema design with primary keys, foreign keys, and indexes.
- Transaction management (ACID properties, commit/rollback).
- Dual-mode architecture: zero-dependency in-memory SQLite default with optional PostgreSQL support.
"""
from __future__ import annotations
import sqlite3
from typing import List, Optional
from domain import Order, Trade, Side, OrderStatus


class TradeStore:
    """ACID persistence engine for orders and trade events."""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    trader_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    remaining_quantity INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    timestamp_ns INTEGER NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_orders_symbol ON orders(symbol);
                CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

                CREATE TABLE IF NOT EXISTS trades (
                    trade_id TEXT PRIMARY KEY,
                    symbol TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    buyer_order_id TEXT NOT NULL,
                    seller_order_id TEXT NOT NULL,
                    buyer_id TEXT NOT NULL,
                    seller_id TEXT NOT NULL,
                    timestamp_ns INTEGER NOT NULL,
                    FOREIGN KEY(buyer_order_id) REFERENCES orders(order_id),
                    FOREIGN KEY(seller_order_id) REFERENCES orders(order_id)
                );

                CREATE INDEX IF NOT EXISTS idx_trades_symbol_time ON trades(symbol, timestamp_ns);
            """)

    def save_order(self, order: Order) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO orders 
                (order_id, trader_id, symbol, side, price, quantity, remaining_quantity, status, timestamp_ns)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order.order_id,
                order.trader_id,
                order.symbol,
                order.side.name,
                order.price,
                order.quantity,
                order.remaining_quantity,
                order.status.name,
                order.timestamp_ns
            ))

    def save_trade(self, trade: Trade) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO trades
                (trade_id, symbol, price, quantity, buyer_order_id, seller_order_id, buyer_id, seller_id, timestamp_ns)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trade.trade_id,
                trade.symbol,
                trade.price,
                trade.quantity,
                trade.buyer_order_id,
                trade.seller_order_id,
                trade.buyer_id,
                trade.seller_id,
                trade.timestamp_ns
            ))

    def get_recent_trades(self, symbol: str, limit: int = 10) -> List[dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT trade_id, symbol, price, quantity, buyer_id, seller_id, timestamp_ns
            FROM trades
            WHERE symbol = ?
            ORDER BY timestamp_ns DESC
            LIMIT ?
        """, (symbol, limit))
        rows = cursor.fetchall()
        return [
            {
                "trade_id": r[0],
                "symbol": r[1],
                "price": r[2],
                "quantity": r[3],
                "buyer_id": r[4],
                "seller_id": r[5],
                "timestamp_ns": r[6],
            }
            for r in rows
        ]

    def close(self) -> None:
        self.conn.close()
