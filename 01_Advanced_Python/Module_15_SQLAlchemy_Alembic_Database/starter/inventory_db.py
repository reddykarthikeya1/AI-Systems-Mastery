"""STARTER - Module 15: SQLAlchemy Alembic Database

Relational E-Commerce Inventory & Order System.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_inventory_db.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/inventory_db.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
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
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_create_customer_and_products
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 15: implement InventoryService.__init__()")


    async def create_customer(self, email: str, full_name: str) -> Customer:
        # [Tier 2] Algorithm: Implement InventoryService.create_customer
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_create_customer_and_products
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 15: implement InventoryService.create_customer()")


    async def add_product(self, sku: str, name: str, price: float, stock: int) -> Product:
        # [Tier 2] Algorithm: Implement InventoryService.add_product adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_add_product_and_lookup_by_sku
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 15: implement InventoryService.add_product()")


    async def place_order(self, customer_id: int, item_requests: list[tuple[int, int]]) -> Order:
        """Places an order atomically, checking stock and decrementing inventory."""
        # [Tier 2] Algorithm: Implement InventoryService.place_order adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_place_order_decrements_inventory_and_totals
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 15: implement InventoryService.place_order()")



async def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_create_customer_and_products
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 15: implement main()")


if __name__ == "__main__":
    asyncio.run(main())
