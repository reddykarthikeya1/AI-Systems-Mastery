"""Unit tests for the Async E-Commerce Inventory Database."""

from __future__ import annotations

import pytest
import pytest_asyncio
from inventory_db import Base, Customer, InventoryService, Product
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload


@pytest_asyncio.fixture
async def svc():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield InventoryService(session_factory)
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_customer_and_products(svc: InventoryService) -> None:
    cust = await svc.create_customer("test@user.com", "Test User")
    assert cust.id is not None
    assert cust.email == "test@user.com"

    prod = await svc.add_product("SKU-1", "Headphones", 80.0, 10)
    assert prod.id is not None
    assert prod.stock == 10


@pytest.mark.asyncio
async def test_place_order_decrements_inventory_and_totals(svc: InventoryService) -> None:
    cust = await svc.create_customer("buyer@user.com", "Buyer User")
    p1 = await svc.add_product("SKU-A", "Monitor", 300.0, 5)
    p2 = await svc.add_product("SKU-B", "Stand", 50.0, 10)

    order = await svc.place_order(cust.id, [(p1.id, 2), (p2.id, 1)])
    assert order.id is not None
    assert order.total_amount == 650.0
    assert len(order.items) == 2


@pytest.mark.asyncio
async def test_place_order_insufficient_stock_raises_error(svc: InventoryService) -> None:
    cust = await svc.create_customer("buyer2@user.com", "Buyer Two")
    p1 = await svc.add_product("SKU-C", "GPU", 999.0, 1)

    with pytest.raises(ValueError, match="Insufficient stock"):
        await svc.place_order(cust.id, [(p1.id, 5)])


@pytest.mark.asyncio
async def test_get_customer_by_id_via_session(svc: InventoryService) -> None:
    """Test querying customer by ID from database session."""
    cust = await svc.create_customer("lookup@user.com", "Lookup Name")
    async with svc.session_factory() as session:
        fetched = await session.get(Customer, cust.id)
        assert fetched is not None
        assert fetched.email == "lookup@user.com"


@pytest.mark.asyncio
async def test_get_nonexistent_customer_returns_none(svc: InventoryService) -> None:
    """Test lookup of non-existent customer returns None."""
    async with svc.session_factory() as session:
        fetched = await session.get(Customer, 99999)
        assert fetched is None


@pytest.mark.asyncio
async def test_add_product_and_lookup_by_sku(svc: InventoryService) -> None:
    """Test looking up created product by SKU."""
    await svc.add_product("SKU-FIND", "Keyboard", 120.0, 15)
    async with svc.session_factory() as session:
        stmt = select(Product).where(Product.sku == "SKU-FIND")
        res = await session.execute(stmt)
        prod = res.scalar_one_or_none()
        assert prod is not None
        assert prod.name == "Keyboard"
        assert prod.price == 120.0


@pytest.mark.asyncio
async def test_place_order_with_multiple_items_and_quantities(svc: InventoryService) -> None:
    """Test placing order across multiple different products."""
    cust = await svc.create_customer("multi@order.com", "Multi Buyer")
    p1 = await svc.add_product("SKU-M1", "Mouse", 25.0, 10)
    p2 = await svc.add_product("SKU-M2", "Pad", 15.0, 20)

    order = await svc.place_order(cust.id, [(p1.id, 2), (p2.id, 3)])
    expected_total = (2 * 25.0) + (3 * 15.0)
    assert order.total_amount == expected_total

    # Verify inventory was decremented
    async with svc.session_factory() as session:
        updated_p1 = await session.get(Product, p1.id)
        assert updated_p1 is not None
        assert updated_p1.stock == 8
        updated_p2 = await session.get(Product, p2.id)
        assert updated_p2 is not None
        assert updated_p2.stock == 17


@pytest.mark.asyncio
async def test_place_order_zero_stock_raises_value_error(svc: InventoryService) -> None:
    """Test ordering item with zero available stock raises ValueError."""
    cust = await svc.create_customer("zero@stock.com", "Zero Stock")
    p = await svc.add_product("SKU-EMPTY", "Out of stock item", 50.0, 0)

    with pytest.raises(ValueError, match="Insufficient stock"):
        await svc.place_order(cust.id, [(p.id, 1)])


@pytest.mark.asyncio
async def test_place_order_missing_product_raises_value_error(svc: InventoryService) -> None:
    """Test placing order for nonexistent product ID raises ValueError."""
    cust = await svc.create_customer("ghost@buyer.com", "Ghost")
    with pytest.raises(ValueError, match="not found"):
        await svc.place_order(cust.id, [(99999, 1)])


@pytest.mark.asyncio
async def test_customer_orders_relationship(svc: InventoryService) -> None:
    """Test customer relationship loads placed orders."""
    cust = await svc.create_customer("history@user.com", "History User")
    p = await svc.add_product("SKU-H1", "Cable", 10.0, 100)

    await svc.place_order(cust.id, [(p.id, 1)])
    await svc.place_order(cust.id, [(p.id, 2)])

    async with svc.session_factory() as session:
        stmt = select(Customer).options(selectinload(Customer.orders)).where(Customer.id == cust.id)
        res = await session.execute(stmt)
        c = res.scalar_one()
        assert len(c.orders) == 2
