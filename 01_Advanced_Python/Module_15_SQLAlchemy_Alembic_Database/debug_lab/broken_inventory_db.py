#!/usr/bin/env python3
"""Broken Async Inventory System demonstrating missing commit and N+1 query traps."""

import asyncio
from sqlalchemy import Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(30))

async def faulty_database_ops():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        session.add(Product(sku="SKU-999"))
        # Forgot: await session.commit()

    # Query in new session
    async with session_factory() as session:
        stmt = select(Product)
        res = await session.execute(stmt)
        products = res.scalars().all()
        print(f"Products in DB: {len(products)} (Expected 1, got 0 because commit was missing!)")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(faulty_database_ops())
