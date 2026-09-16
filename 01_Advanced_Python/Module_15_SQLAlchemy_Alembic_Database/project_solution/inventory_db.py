#!/usr/bin/env python3
"""Relational E-Commerce Inventory & Order System.

Module 13 (Async Databases & SQLAlchemy 2.0) Turnkey Project Implementation.
Demonstrates SQLAlchemy 2.0 Mapped models, async sessions, and selectinload eager loading.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100))
    orders: Mapped[list[Order]] = relationship(back_populates="customer", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(30), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float]
    stock: Mapped[int]


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    total_amount: Mapped[float] = mapped_column(default=0.0)

    customer: Mapped[Customer] = relationship(back_populates="orders")
    items: Mapped[list[OrderItem]] = relationship(back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    unit_price: Mapped[float]

    order: Mapped[Order] = relationship(back_populates="items")
    product: Mapped[Product] = relationship()


class InventoryService:
    """Async database service managing orders and inventory transactions."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def create_customer(self, email: str, full_name: str) -> Customer:
        async with self.session_factory() as session:
            customer = Customer(email=email, full_name=full_name)
            session.add(customer)
            await session.commit()
            return customer

    async def add_product(self, sku: str, name: str, price: float, stock: int) -> Product:
        async with self.session_factory() as session:
            product = Product(sku=sku, name=name, price=price, stock=stock)
            session.add(product)
            await session.commit()
            return product

    async def place_order(self, customer_id: int, item_requests: list[tuple[int, int]]) -> Order:
        """Places an order atomically, checking stock and decrementing inventory."""
        async with self.session_factory() as session:
            async with session.begin():
                order = Order(customer_id=customer_id, total_amount=0.0)
                total = 0.0

                for product_id, qty in item_requests:
                    prod = await session.get(Product, product_id)
                    if not prod:
                        raise ValueError(f"Product #{product_id} not found")
                    if prod.stock < qty:
                        raise ValueError(f"Insufficient stock for '{prod.name}' (Available: {prod.stock}, Requested: {qty})")

                    prod.stock -= qty
                    subtotal = prod.price * qty
                    total += subtotal
                    # Setting order=order automatically links to order.items via relationship
                    OrderItem(order=order, product_id=prod.id, quantity=qty, unit_price=prod.price)

                order.total_amount = round(total, 2)
                session.add(order)

            # Re-fetch with eager loading
            stmt = select(Order).options(selectinload(Order.items).selectinload(OrderItem.product)).where(Order.id == order.id)
            res = await session.execute(stmt)
            return res.scalar_one()


async def main() -> None:
    print("=" * 65)
    print("      ASYNC SQLALCHEMY 2.0 INVENTORY SERVICE DEMO")
    print("=" * 65)

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    svc = InventoryService(session_factory)
    cust = await svc.create_customer("alice@cloud.com", "Alice Walker")
    p1 = await svc.add_product("SKU-100", "Laptop Pro", 1200.0, 5)
    p2 = await svc.add_product("SKU-200", "USB-C Hub", 45.0, 20)

    order = await svc.place_order(cust.id, [(p1.id, 1), (p2.id, 2)])
    print(f"\nOrder Placed Successfully! (Order ID: #{order.id})")
    print(f"Customer  : {cust.full_name} ({cust.email})")
    print(f"Total     : ${order.total_amount:,.2f}")
    for it in order.items:
        print(f"  - {it.product.name} (x{it.quantity} @ ${it.unit_price:,.2f})")


if __name__ == "__main__":
    asyncio.run(main())
