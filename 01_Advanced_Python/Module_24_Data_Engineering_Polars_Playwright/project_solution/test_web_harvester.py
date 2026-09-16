"""Tests for Module 24 - Playwright harvesting and the Polars hand-off.

Structured in two halves so the suite is useful whether or not a browser is
installed:

* **Parsing and Polars tests** always run - they need no browser at all.
* **Browser tests** carry ``@pytest.mark.requires_browser`` and skip with a
  clear setup hint when Chromium has not been downloaded.

That split is deliberate. A test suite that fails wholesale because an optional
120 MB binary is absent trains people to ignore red output.
"""

from __future__ import annotations

import pytest
from web_harvester import (
    SETUP_HINT,
    Product,
    WebHarvester,
    _parse_bool,
    _parse_price,
    browser_installed,
    browser_page,
    category_summary,
    fixture_server,
    fixture_url,
    playwright_installed,
    to_polars,
)

requires_browser = pytest.mark.skipif(not browser_installed(), reason=SETUP_HINT)

SAMPLE = [
    Product("SKU-1", "Keyboard", "peripherals", 189.99, 4.6, True),
    Product("SKU-2", "Monitor", "displays", 649.00, 4.4, True),
    Product("SKU-3", "Headset", "audio", 299.50, 4.8, True),
    Product("SKU-4", "Dock", "peripherals", 249.00, 4.1, False),
]


# ===========================================================================
# 1. Price parsing - the string soup the DOM hands you
# ===========================================================================


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("$1,299.00", 1299.00),
        ("1299", 1299.0),
        ("1,299.50", 1299.50),
        ("£49.99", 49.99),
        ("€1.000", 1.000),
        ("  $89.95  ", 89.95),
        ("1\xa0299.00", 1299.00),  # non-breaking space, very common in HTML
        (1299, 1299.0),
        (1299.5, 1299.5),
    ],
)
def test_parse_price_normalises_presentation_strings(raw: object, expected: float) -> None:
    assert _parse_price(raw) == pytest.approx(expected)


@pytest.mark.parametrize("bad", ["", "   ", "N/A", "call us", "$"])
def test_parse_price_rejects_non_numeric(bad: str) -> None:
    with pytest.raises(ValueError):
        _parse_price(bad)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("in stock", True),
        ("In Stock", True),
        ("true", True),
        ("yes", True),
        ("1", True),
        ("available", True),
        ("out of stock", False),
        ("no", False),
        ("", False),
        (None, False),
        (True, True),
        (False, False),
    ],
)
def test_parse_bool_handles_real_world_phrasing(raw: object, expected: bool) -> None:
    assert _parse_bool(raw) is expected


# ===========================================================================
# 2. Product construction
# ===========================================================================


def test_product_from_dict_normalises_everything() -> None:
    product = Product.from_dict(
        {
            "sku": "  SKU-99 ",
            "name": "  Widget  ",
            "category": "  PERIPHERALS ",
            "price": "$1,499.00",
            "rating": "4.5",
            "in_stock": "in stock",
        }
    )
    assert product.sku == "SKU-99"
    assert product.name == "Widget"
    assert product.category == "peripherals"  # lower-cased for grouping
    assert product.price == 1499.00
    assert product.rating == 4.5
    assert product.in_stock is True


def test_product_defaults_missing_optional_fields() -> None:
    product = Product.from_dict({"sku": "S", "name": "N", "price": "10"})
    assert product.category == "uncategorised"
    assert product.rating == 0.0
    assert product.in_stock is False


def test_product_missing_required_field_raises() -> None:
    with pytest.raises(KeyError):
        Product.from_dict({"name": "no sku", "price": "10"})


def test_product_is_immutable() -> None:
    """A scraped record should not be mutable in place."""
    with pytest.raises((AttributeError, TypeError)):
        SAMPLE[0].price = 0.0  # type: ignore[misc]


# ===========================================================================
# 3. Polars hand-off
# ===========================================================================


def test_to_polars_shape_and_columns() -> None:
    frame = to_polars(SAMPLE)
    assert frame.shape == (4, 6)
    assert frame.columns == ["sku", "name", "category", "price", "rating", "in_stock"]


def test_to_polars_enforces_explicit_dtypes() -> None:
    """Inferred dtypes are how a Float64 column silently becomes Utf8."""
    import polars as pl

    frame = to_polars(SAMPLE)
    dtypes = dict(zip(frame.columns, frame.dtypes, strict=True))
    assert dtypes["price"] == pl.Float64
    assert dtypes["rating"] == pl.Float64
    assert dtypes["in_stock"] == pl.Boolean
    assert dtypes["sku"] == pl.Utf8


def test_to_polars_empty_input_keeps_the_schema() -> None:
    """An empty harvest must still produce a correctly-typed frame."""
    import polars as pl

    frame = to_polars([])
    assert frame.shape == (0, 6)
    assert dict(zip(frame.columns, frame.dtypes, strict=True))["price"] == pl.Float64


def test_category_summary_excludes_out_of_stock() -> None:
    summary = category_summary(to_polars(SAMPLE))
    peripherals = summary.filter(summary["category"] == "peripherals")
    # SKU-4 (Dock, out of stock) must be excluded, leaving only the keyboard.
    assert peripherals["n"][0] == 1
    assert peripherals["avg_price"][0] == pytest.approx(189.99)


def test_category_summary_is_sorted_by_avg_price_descending() -> None:
    prices = category_summary(to_polars(SAMPLE))["avg_price"].to_list()
    assert prices == sorted(prices, reverse=True)


def test_category_summary_on_empty_frame_is_empty_not_an_error() -> None:
    assert category_summary(to_polars([])).height == 0


# ===========================================================================
# 4. Fixtures & setup probes
# ===========================================================================


def test_playwright_package_is_installed() -> None:
    assert playwright_installed(), "pip install playwright"


@pytest.mark.parametrize(
    "name",
    [
        "rendered_table.html",
        "paginated_page1.html",
        "paginated_page2.html",
        "paginated_page3.html",
        "lazy_load.html",
        "api_driven.html",
        "api_products.json",
    ],
)
def test_fixture_exists(name: str) -> None:
    assert fixture_url(name).startswith("file:///")


def test_missing_fixture_raises_clear_error() -> None:
    with pytest.raises(FileNotFoundError, match="fixture not found"):
        fixture_url("does_not_exist.html")


def test_rendered_table_fixture_body_is_genuinely_empty() -> None:
    """Proves the JS-rendering test is not accidentally testing static HTML.

    If this fixture ever gains static rows, the browser test would pass for the
    wrong reason and the module's central claim would go unverified.
    """
    from pathlib import Path

    html = (Path(__file__).parent / "fixtures" / "rendered_table.html").read_text(
        encoding="utf-8"
    )
    tbody = html.split("<tbody>")[1].split("</tbody>")[0]
    assert "SKU-" not in tbody, "fixture tbody must be empty; rows come from JS"


# ===========================================================================
# 5. Browser tests
# ===========================================================================


@pytest.mark.requires_browser
@requires_browser
def test_browser_page_context_manager_cleans_up() -> None:
    with browser_page() as page:
        page.goto(fixture_url("rendered_table.html"))
        assert page.title() == "Rendered Table"
    # A leaked browser process would keep the suite's memory climbing.


@pytest.mark.requires_browser
@requires_browser
def test_harvest_js_rendered_table() -> None:
    """The module's central claim: a browser sees what requests cannot."""
    with browser_page() as page:
        products = WebHarvester(page).harvest_rendered_table(
            fixture_url("rendered_table.html")
        )
    assert len(products) == 12, f"expected 12 products, got {len(products)}"
    skus = {p.sku for p in products}
    assert "SKU-1001" in skus
    assert "SKU-BAD" not in skus, "the malformed row should have been skipped"


@pytest.mark.requires_browser
@requires_browser
def test_harvested_prices_are_parsed_as_floats() -> None:
    with browser_page() as page:
        products = WebHarvester(page).harvest_rendered_table(
            fixture_url("rendered_table.html")
        )
    keyboard = next(p for p in products if p.sku == "SKU-1001")
    assert keyboard.price == pytest.approx(189.99)
    assert keyboard.in_stock is True
    assert all(isinstance(p.price, float) for p in products)


@pytest.mark.requires_browser
@requires_browser
def test_pagination_collects_every_page() -> None:
    with browser_page() as page:
        products = WebHarvester(page).harvest_all_pages(fixture_url("paginated_page1.html"))
    assert len(products) == 12, f"expected 12 across 3 pages, got {len(products)}"
    assert len({p.sku for p in products}) == 12, "SKUs must be deduplicated"


@pytest.mark.requires_browser
@requires_browser
def test_pagination_respects_max_pages_bound() -> None:
    """The safety bound must actually bound - a runaway crawl is a real hazard."""
    with browser_page() as page:
        products = WebHarvester(page).harvest_all_pages(
            fixture_url("paginated_page1.html"), max_pages=1
        )
    assert len(products) == 4, "only the first page should have been read"


@pytest.mark.requires_browser
@requires_browser
def test_lazy_loading_scrolls_until_exhausted() -> None:
    with browser_page() as page:
        products = WebHarvester(page).harvest_lazy_loaded(fixture_url("lazy_load.html"))
    assert len(products) == 12, f"scrolling should reveal all 12, got {len(products)}"


@pytest.mark.requires_browser
@requires_browser
def test_lazy_loading_first_batch_only_without_scrolling() -> None:
    """Confirms the fixture really does lazy-load rather than render everything."""
    with browser_page() as page:
        page.goto(fixture_url("lazy_load.html"))
        page.wait_for_selector(".product-card")
        initial = len(page.query_selector_all(".product-card"))
    assert initial == 4, f"expected one batch of 4 before scrolling, saw {initial}"


@pytest.mark.requires_browser
@requires_browser
def test_api_interception_captures_structured_json() -> None:
    """Reading the API beats parsing the DOM - structured, typed, redesign-proof.

    Served over real HTTP because a ``file://`` page's ``fetch()`` is blocked by
    the browser's same-origin policy. Real targets are HTTP anyway.
    """
    with fixture_server() as base, browser_page() as page:
        products = WebHarvester(page).harvest_via_api_interception(
            f"{base}/api_driven.html"
        )
    assert len(products) == 12
    assert all(isinstance(p.price, float) for p in products)


@pytest.mark.requires_browser
@requires_browser
def test_fixture_server_serves_over_http() -> None:
    """The local HTTP harness itself must work, or the test above is vacuous."""
    with fixture_server() as base, browser_page() as page:
        page.goto(f"{base}/rendered_table.html")
        assert page.title() == "Rendered Table"
        assert base.startswith("http://127.0.0.1:")


@pytest.mark.requires_browser
@requires_browser
def test_end_to_end_harvest_into_polars_summary() -> None:
    with browser_page() as page:
        products = WebHarvester(page).harvest_rendered_table(
            fixture_url("rendered_table.html")
        )
    frame = to_polars(products)
    summary = category_summary(frame)
    assert frame.height == 12
    assert set(summary["category"].to_list()) <= {"peripherals", "displays", "audio"}
    assert summary["avg_price"].to_list() == sorted(
        summary["avg_price"].to_list(), reverse=True
    )
