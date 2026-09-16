#!/usr/bin/env python3
"""Module 24 - Browser automation with Playwright, feeding the Polars pipeline.

The module title promises Playwright and the previous version shipped none. This
file supplies it, and it does so against **local HTML fixtures** rather than
live third-party sites - which is both an ethical and an engineering choice:

* Scraping someone else's site in a test suite is rude, fragile, and often a
  terms-of-service violation.
* A test that depends on a remote page fails when their marketing team ships a
  redesign, which teaches you nothing about your own code.

So the fixtures in ``fixtures/`` are real HTML exercising the hard parts:
JavaScript-rendered content, pagination, lazy loading, and a table that only
appears after a network call. Every technique transfers unchanged to a real
target.

Install
-------
::

    pip install playwright
    playwright install chromium      # ~120 MB browser download, one time

Run:  python web_harvester.py
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

FIXTURE_DIR = Path(__file__).parent / "fixtures"


# ===========================================================================
# Availability probes - a missing browser must be a clear message, not a stack
# ===========================================================================


def playwright_installed() -> bool:
    """True when the `playwright` Python package is importable."""
    import importlib.util

    return importlib.util.find_spec("playwright") is not None


def browser_installed() -> bool:
    """True when a Chromium binary has actually been downloaded.

    ``pip install playwright`` gives you the *library*; the browsers are a
    separate ~120 MB download. Forgetting the second step is the single most
    common Playwright setup failure, so probe for it explicitly.
    """
    if not playwright_installed():
        return False
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
        return True
    except Exception:
        return False


SETUP_HINT = (
    "Chromium is not installed. Run:\n"
    "    pip install playwright\n"
    "    playwright install chromium"
)


# ===========================================================================
# Data model
# ===========================================================================


@dataclass(frozen=True, slots=True)
class Product:
    """One harvested row. Frozen so a scraped record cannot be mutated in place."""

    sku: str
    name: str
    category: str
    price: float
    rating: float
    in_stock: bool

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Product:
        """Parse one raw dict, normalising the string soup the DOM gives you."""
        return cls(
            sku=str(raw["sku"]).strip(),
            name=str(raw["name"]).strip(),
            category=str(raw.get("category", "uncategorised")).strip().lower(),
            price=_parse_price(raw["price"]),
            rating=float(raw.get("rating") or 0.0),
            in_stock=_parse_bool(raw.get("in_stock")),
        )


def _parse_price(value: Any) -> float:
    """Turn '$1,299.00' / '1299' / 1299.0 into a float.

    Scraped numbers arrive as presentation strings: currency symbols, thousands
    separators, non-breaking spaces. Normalise at the boundary so nothing
    downstream has to care.
    """
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = (
        str(value)
        .replace("\xa0", "")
        .replace("$", "")
        .replace("£", "")
        .replace("€", "")
        .replace(",", "")
        .strip()
    )
    if not cleaned:
        raise ValueError("empty price")
    return float(cleaned)


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "in stock", "available"}


# ===========================================================================
# Browser session
# ===========================================================================


@contextmanager
def browser_page(headless: bool = True, timeout_ms: int = 15_000) -> Iterator[Any]:
    """Yield a ready Playwright page, guaranteeing teardown.

    A context manager rather than manual start/stop because a leaked browser
    process survives your test run and slowly eats the machine. Module 05's
    lesson on ``@contextmanager`` exists for exactly this shape of problem.
    """
    if not playwright_installed():
        raise RuntimeError(SETUP_HINT)

    from playwright.sync_api import sync_playwright

    playwright = sync_playwright().start()
    browser = None
    try:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            # Identify your bot honestly. Pretending to be a human browser to
            # evade rate limits is how you get an IP banned - and it is the
            # wrong thing to do.
            user_agent="Module24-CourseHarvester/1.0 (+educational)",
        )
        page = context.new_page()
        page.set_default_timeout(timeout_ms)
        yield page
    finally:
        if browser is not None:
            browser.close()
        playwright.stop()


def fixture_url(name: str) -> str:
    """``file://`` URL for a local fixture.

    Good enough for pages that only need their own inline scripts. A page that
    calls ``fetch()`` needs a real HTTP origin - see ``fixture_server`` - because
    the browser blocks cross-origin requests from ``file://``.
    """
    path = FIXTURE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"fixture not found: {path}")
    return path.resolve().as_uri()


@contextmanager
def fixture_server(port: int = 0) -> Iterator[str]:
    """Serve ``fixtures/`` over real HTTP and yield the base URL.

    Why this exists: a page loaded from ``file://`` has an opaque origin, so the
    browser refuses its ``fetch()`` calls. Any fixture exercising XHR/fetch must
    be served over HTTP - which is also how every real target works, so the
    tests end up closer to production rather than further from it.

    ``port=0`` lets the OS pick a free port, so parallel test runs never collide.
    """
    import threading
    from functools import partial
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

    handler = partial(SimpleHTTPRequestHandler, directory=str(FIXTURE_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


# ===========================================================================
# Harvesting techniques
# ===========================================================================


class WebHarvester:
    """The four extraction techniques that cover most real scraping work."""

    def __init__(self, page: Any) -> None:
        self.page = page

    # -- 1. wait for JS-rendered content ----------------------------------

    def harvest_rendered_table(self, url: str) -> list[Product]:
        """Scrape a table that JavaScript builds after page load.

        The critical line is ``wait_for_selector``. ``requests`` + BeautifulSoup
        would return the empty shell, because they never execute the script.
        This is the entire reason a browser is in the toolchain.

        Note what we do NOT do: ``sleep(3)``. A fixed sleep is either too short
        (flaky) or too long (slow). Wait for the *condition*.
        """
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_selector("#product-table tbody tr", state="attached")

        rows = self.page.query_selector_all("#product-table tbody tr")
        harvested: list[Product] = []
        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) < 6:
                continue  # malformed row: skip rather than crash the whole run
            try:
                harvested.append(
                    Product.from_dict(
                        {
                            "sku": cells[0].inner_text(),
                            "name": cells[1].inner_text(),
                            "category": cells[2].inner_text(),
                            "price": cells[3].inner_text(),
                            "rating": cells[4].inner_text() or 0,
                            "in_stock": cells[5].inner_text(),
                        }
                    )
                )
            except (ValueError, KeyError):
                continue  # one bad row must not lose the other 99
        return harvested

    # -- 2. pagination -----------------------------------------------------

    def harvest_all_pages(self, url: str, max_pages: int = 10) -> list[Product]:
        """Follow the 'next' link until it disappears or the budget is spent.

        ``max_pages`` is not optional politeness - it is a safety bound. A
        pagination bug that loops forever will happily make 100,000 requests.
        """
        self.page.goto(url, wait_until="domcontentloaded")
        collected: list[Product] = []
        seen_skus: set[str] = set()

        for _ in range(max_pages):
            self.page.wait_for_selector("#product-table tbody tr", state="attached")
            for product in self._read_current_page():
                if product.sku not in seen_skus:  # dedupe across page boundaries
                    seen_skus.add(product.sku)
                    collected.append(product)

            next_link = self.page.query_selector("a#next-page:not([disabled])")
            if next_link is None:
                break
            next_link.click()
            self.page.wait_for_load_state("domcontentloaded")

        return collected

    def _read_current_page(self) -> list[Product]:
        out: list[Product] = []
        for row in self.page.query_selector_all("#product-table tbody tr"):
            cells = row.query_selector_all("td")
            if len(cells) < 6:
                continue
            try:
                out.append(
                    Product.from_dict(
                        {
                            "sku": cells[0].inner_text(),
                            "name": cells[1].inner_text(),
                            "category": cells[2].inner_text(),
                            "price": cells[3].inner_text(),
                            "rating": cells[4].inner_text() or 0,
                            "in_stock": cells[5].inner_text(),
                        }
                    )
                )
            except (ValueError, KeyError):
                continue
        return out

    # -- 3. lazy loading / infinite scroll --------------------------------

    def harvest_lazy_loaded(self, url: str, max_scrolls: int = 12) -> list[Product]:
        """Scroll until the item count stops growing.

        Termination is by *observed effect* (the count stopped changing), not by
        a fixed scroll count. That is the only condition that is correct for a
        list whose length you do not know in advance.
        """
        # Imported here, not at module scope: this file must stay importable on
        # a machine with no browser installed, which is what the availability
        # probes above are for.
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_selector(".product-card", state="attached")

        for _ in range(max_scrolls):
            before = len(self.page.query_selector_all(".product-card"))
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            try:
                # Wait for the count to actually GROW, rather than sleeping a
                # fixed interval and hoping the loader finished inside it. A
                # fixed `wait_for_timeout` is the bug this module warns about:
                # on a slow run the loader has not fired yet, the count looks
                # unchanged, and the scroll terminates early with a partial
                # result - no error, just missing rows.
                self.page.wait_for_function(
                    "expected => document.querySelectorAll('.product-card').length > expected",
                    arg=before,
                    timeout=3000,
                )
            except PlaywrightTimeoutError:
                # The count genuinely stopped growing. This is the terminating
                # condition, and it is an observed effect rather than a guess.
                break

        harvested: list[Product] = []
        for card in self.page.query_selector_all(".product-card"):
            raw = card.get_attribute("data-product")
            if not raw:
                continue
            try:
                harvested.append(Product.from_dict(json.loads(raw)))
            except (ValueError, KeyError, json.JSONDecodeError):
                continue
        return harvested

    # -- 4. intercept the API instead of parsing the DOM ------------------

    def harvest_via_api_interception(self, url: str) -> list[Product]:
        """Capture the JSON the page fetches, rather than scraping the rendered DOM.

        **This is usually the right answer.** If a page renders itself from a
        JSON endpoint, read the JSON: it is structured, typed, stable across
        redesigns, and far cheaper than DOM traversal. Reach for CSS selectors
        only when there is no underlying API to observe.
        """
        captured: list[dict[str, Any]] = []

        def on_response(response: Any) -> None:
            # Match the data endpoint, whatever its shape. Against a real target
            # this is where you would put the actual API path you observed in
            # DevTools -> Network.
            if "api_products" not in response.url and "/api/products" not in response.url:
                return
            try:
                body = response.json()
            except Exception:
                return
            captured.extend(body.get("products", []))

        self.page.on("response", on_response)
        self.page.goto(url, wait_until="networkidle")

        harvested: list[Product] = []
        for raw in captured:
            try:
                harvested.append(Product.from_dict(raw))
            except (ValueError, KeyError):
                continue
        return harvested


# ===========================================================================
# Handing off to Polars
# ===========================================================================


def to_polars(products: list[Product]) -> Any:
    """Convert harvested rows into a typed Polars DataFrame.

    Explicit dtypes at the boundary, not inferred ones: a price column that
    silently becomes Utf8 because one row had "N/A" will break every downstream
    aggregation, and it will break it far from the cause.
    """
    import polars as pl

    if not products:
        return pl.DataFrame(
            schema={
                "sku": pl.Utf8,
                "name": pl.Utf8,
                "category": pl.Utf8,
                "price": pl.Float64,
                "rating": pl.Float64,
                "in_stock": pl.Boolean,
            }
        )
    return pl.DataFrame(
        [
            {
                "sku": p.sku,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "rating": p.rating,
                "in_stock": p.in_stock,
            }
            for p in products
        ],
        schema={
            "sku": pl.Utf8,
            "name": pl.Utf8,
            "category": pl.Utf8,
            "price": pl.Float64,
            "rating": pl.Float64,
            "in_stock": pl.Boolean,
        },
    )


def category_summary(frame: Any) -> Any:
    """Aggregate the harvested frame by category."""
    import polars as pl

    return (
        frame.filter(pl.col("in_stock"))
        .group_by("category")
        .agg(
            pl.len().alias("n"),
            pl.col("price").mean().round(2).alias("avg_price"),
            pl.col("price").max().alias("max_price"),
            pl.col("rating").mean().round(2).alias("avg_rating"),
        )
        .sort("avg_price", descending=True)
    )


# ===========================================================================
# Demo
# ===========================================================================


def main() -> None:
    print("=" * 74)
    print("   MODULE 24 - PLAYWRIGHT HARVESTING -> POLARS ANALYTICS")
    print("=" * 74)

    if not browser_installed():
        print(f"\n  {SETUP_HINT}")
        print("\n  The Polars half of this module runs without a browser:")
        print("      python analytics_engine.py")
        return

    with browser_page() as page:
        harvester = WebHarvester(page)

        print("\n" + "-" * 74)
        print(" 1. JS-RENDERED TABLE (requests+BeautifulSoup would see nothing)")
        print("-" * 74)
        rendered = harvester.harvest_rendered_table(fixture_url("rendered_table.html"))
        print(f"\n  harvested {len(rendered)} products")
        for product in rendered[:3]:
            print(f"    {product.sku:<8} {product.name:<26} ${product.price:>9,.2f}")

        print("\n" + "-" * 74)
        print(" 2. PAGINATION (follow 'next' until it disappears)")
        print("-" * 74)
        paged = harvester.harvest_all_pages(fixture_url("paginated_page1.html"))
        print(f"\n  harvested {len(paged)} products across pages")

        print("\n" + "-" * 74)
        print(" 3. LAZY LOADING (scroll until the count stops growing)")
        print("-" * 74)
        lazy = harvester.harvest_lazy_loaded(fixture_url("lazy_load.html"))
        print(f"\n  harvested {len(lazy)} products after scrolling")

        print("\n" + "-" * 74)
        print(" 4. API INTERCEPTION (read the JSON, not the DOM)")
        print("-" * 74)
        intercepted = harvester.harvest_via_api_interception(fixture_url("api_driven.html"))
        print(f"\n  captured {len(intercepted)} products from the network layer")
        print("  -> structured, typed, and immune to a CSS redesign")

    print("\n" + "-" * 74)
    print(" 5. HAND-OFF TO POLARS")
    print("-" * 74)
    frame = to_polars(rendered + lazy)
    print(f"\n  DataFrame shape: {frame.shape}")
    print(f"  dtypes: {dict(zip(frame.columns, [str(d) for d in frame.dtypes], strict=True))}")
    print("\n  category summary (in-stock only):")
    print(category_summary(frame))

    print("\n" + "=" * 74)


if __name__ == "__main__":
    main()
