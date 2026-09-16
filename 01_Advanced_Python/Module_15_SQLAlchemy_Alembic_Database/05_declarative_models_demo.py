#!/usr/bin/env python3
"""Module 13: SQLAlchemy 2.0 Modern Declarative Models Demo.

This script demonstrates defining typed declarative models using Mapped
and mapped_column.
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    employees: Mapped[list[Employee]] = relationship(back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped[Department] = relationship(back_populates="employees")


def main() -> None:
    print("=" * 60)
    print("  SQLAlchemy 2.0 Declarative Model Metadata Inspection")
    print("=" * 60)

    for table_name, table in Base.metadata.tables.items():
        print(f"Table: {table_name}")
        for col in table.columns:
            print(f"  Column: {col.name:<15} | Type: {col.type} | PK: {col.primary_key}")


if __name__ == "__main__":
    main()
