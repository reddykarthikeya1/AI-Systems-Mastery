#!/usr/bin/env python3
"""Module 13: Async Sessions & Relations Demonstration.

This script demonstrates async database operations using aiosqlite and
SQLAlchemy 2.0 selectinload eager loading.
"""

from __future__ import annotations

import asyncio

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    books: Mapped[list[Book]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[Author] = relationship(back_populates="books")


async def main() -> None:
    print("=" * 60)
    print("  SQLAlchemy 2.0 Async Session & Eager Loading Demo")
    print("=" * 60)

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Insert relational records
    async with session_factory() as session:
        author = Author(name="Luciano Ramalho")
        author.books.append(Book(title="Fluent Python 2nd Edition"))
        session.add(author)
        await session.commit()

    # Query with selectinload
    async with session_factory() as session:
        stmt = select(Author).options(selectinload(Author.books)).where(Author.name == "Luciano Ramalho")
        result = await session.execute(stmt)
        auth = result.scalar_one()

        print(f"Author : {auth.name}")
        print(f"Books  : {[b.title for b in auth.books]}")


if __name__ == "__main__":
    asyncio.run(main())
