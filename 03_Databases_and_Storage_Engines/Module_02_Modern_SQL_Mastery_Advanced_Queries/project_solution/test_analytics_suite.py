"""Automated pytest test suite for Module 02 Analytics Suite."""

import pytest
from analytics_suite import AnalyticsSuite


@pytest.fixture
def suite():
    """Provides a fresh analytics suite populated with seed data."""
    s = AnalyticsSuite(":memory:")
    s.insert_seed_data()
    return s


def test_customer_lifetime_value(suite):
    results = suite.calculate_customer_lifetime_value()
    assert len(results) == 4

    # Alice is top spender: 1 Laptop (1200) + 2 Phones (1600) + 1 Headphones (100) = 2900
    top_customer = results[0]
    assert top_customer["name"] == "Alice"
    assert top_customer["total_spent"] == 2900.0
    assert top_customer["order_count"] == 3

    # Diana has 0 orders
    diana = next(c for c in results if c["name"] == "Diana")
    assert diana["order_count"] == 0
    assert diana["total_spent"] == 0.0


def test_running_revenue_and_moving_avg(suite):
    daily = suite.calculate_running_revenue_and_moving_avg()
    assert len(daily) == 6

    # Verify running cumulative total
    assert daily[0]["cumulative_revenue"] == 1200.0
    assert daily[1]["cumulative_revenue"] == 2800.0  # 1200 + 1600

    # 3-day rolling average on day 3 (indices 0, 1, 2: 1200, 1600, 350 -> sum 3150 / 3 = 1050.0)
    assert daily[2]["rolling_3day_avg"] == 1050.0


def test_rank_products_within_categories(suite):
    ranks = suite.rank_products_within_categories()
    
    # In Electronics: Laptop (1200*2 = 2400), Phone (1600), Headphones (100)
    elec = [p for p in ranks if p["category"] == "Electronics"]
    assert elec[0]["name"] == "Laptop"
    assert elec[0]["rank_in_category"] == 1
    assert elec[1]["name"] == "Phone"
    assert elec[1]["rank_in_category"] == 2


def test_recursive_org_hierarchy(suite):
    hierarchy = suite.get_employee_hierarchy()
    assert len(hierarchy) == 6

    # CEO Elena is Level 1
    assert hierarchy[0]["name"] == "CEO Elena"
    assert hierarchy[0]["level"] == 1
    assert hierarchy[0]["path"] == "CEO Elena"

    # David reports to Marcus who reports to Elena -> Level 3
    david = next(e for e in hierarchy if e["name"] == "Engineer David")
    assert david["level"] == 3
    assert david["path"] == "CEO Elena -> VP Marcus -> Engineer David"
