"""Automated render check for the HTML portal, runnable in CI. Needs only Python and a Chrome/Chromium binary.

    python tools/portal_check.py                 # every page in html/
    python tools/portal_check.py --sample 12     # a quick spread of pages
    python tools/portal_check.py html/02-Low-Level-Design/02-UML-Modeling-Class-Sequence-State-Diagrams.html

For each page the script loads it in headless Chrome (so KaTeX and Mermaid actually execute), dumps the rendered DOM and
checks: no KaTeX error nodes, every Mermaid block rendered an SVG without a syntax error, the landmarks and skip link
exist, and the chapter navigation is present. Exit code 1 if any page fails.

Set CHROME_PATH to override the browser location.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "html"
CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome() -> str:
    for c in CANDIDATES:
        if c and Path(c).exists():
            return c
    for name in ("google-chrome", "chromium", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("Chrome not found: set CHROME_PATH")


def render(chrome: str, page: Path) -> str:
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
           "--virtual-time-budget=15000", "--dump-dom", page.resolve().as_uri()]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120).stdout


def check(chrome: str, page: Path) -> list[str]:
    dom = render(chrome, page)
    problems = []
    if len(dom) < 2000:
        return ["page did not render (empty DOM)"]
    n_katex_err = len(re.findall(r'class="katex-error"', dom))
    if n_katex_err:
        problems.append(f"{n_katex_err} KaTeX error node(s)")
    blocks = re.findall(r'<(?:pre|div)[^>]*class="[^"]*\bmermaid\b[^"]*"[^>]*>(.*?)</(?:pre|div)>', dom, re.S)
    unrendered = [b for b in blocks if "<svg" not in b]
    if unrendered:
        problems.append(f"{len(unrendered)} of {len(blocks)} Mermaid block(s) did not render")
    if re.search(r"Syntax error in (text|graph)|Parse error on line", dom):
        problems.append("Mermaid syntax error text present")
    for needle, label in (('id="main-content"', "main landmark"), ('id="chapter-nav"', "chapter navigation"), ('class="skip', "skip link")):
        if needle not in dom:
            problems.append(f"missing {label}")
    return problems


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sample = None
    if "--sample" in sys.argv:
        sample = int(sys.argv[sys.argv.index("--sample") + 1])
        args = [a for a in args if a != str(sample)]
    pages = [Path(a) for a in args] or sorted(p for p in HTML.rglob("*.html") if p.name != "index.html")
    if sample:
        step = max(1, len(pages) // sample)
        pages = pages[::step][:sample]
    chrome = find_chrome()
    failures = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        for page, problems in zip(pages, pool.map(lambda p: check(chrome, p), pages)):
            rel = page.resolve().relative_to(ROOT).as_posix() if page.resolve().is_relative_to(ROOT) else str(page)
            if problems:
                failures += 1
                print(f"FAIL {rel}: {'; '.join(problems)}")
    print(f"checked {len(pages)} pages, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
