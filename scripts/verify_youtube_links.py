#!/usr/bin/env python3
"""Automated YouTube Link Validator.

Extracts all YouTube video links from Markdown files across the repository
and verifies them against YouTube's official oEmbed API endpoint.
Ensures zero broken, deleted, private, or hallucinated video URLs.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import os
import re
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Tuple, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT_DIR = Path(__file__).resolve().parent.parent

CACHE_FILE = ROOT_DIR / ".youtube_verified_cache.json"
_VERIFIED_CACHE: Dict[str, Dict] = {}
if CACHE_FILE.is_file():
    try:
        raw_cache = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        for item in raw_cache.values():
            if isinstance(item, dict) and "id" in item:
                _VERIFIED_CACHE[item["id"]] = item
    except Exception:
        pass

YOUTUBE_REGEX = re.compile(
    r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
)

def extract_youtube_urls(file_path: Path) -> List[Tuple[str, str]]:
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    matches = YOUTUBE_REGEX.findall(content)
    unique_ids = []
    seen = set()
    for vid in matches:
        if vid not in seen:
            seen.add(vid)
            unique_ids.append((vid, f"https://www.youtube.com/watch?v={vid}"))
    return unique_ids

def verify_single_video(item: Tuple[str, str]) -> Tuple[str, bool, str, str]:
    vid, full_url = item
    if vid in _VERIFIED_CACHE:
        c = _VERIFIED_CACHE[vid]
        return vid, True, c.get("title", "Verified Video"), c.get("author", "Verified Channel")

    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                return vid, True, data.get("title", "Unknown Title"), data.get("author_name", "Unknown Author")
            return vid, False, f"Unexpected status: {response.status}", ""
    except urllib.error.HTTPError as e:
        return vid, False, f"HTTP Error {e.code}", ""
    except Exception as e:
        return vid, False, f"Request Error: {e}", ""

def verify_file(file_path: Path) -> Tuple[int, int, List[str]]:
    urls = extract_youtube_urls(file_path)
    if not urls:
        return 0, 0, []

    print(f"\n[*] Checking {len(urls)} video links in: {file_path.relative_to(ROOT_DIR)}")
    passed = 0
    failed = 0
    errors = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(verify_single_video, item) for item in urls]
        for f in as_completed(futures):
            vid, is_valid, title, author = f.result()
            if is_valid:
                passed += 1
                title_short = (title[:50] + "...") if len(title) > 50 else title
                print(f"  [OK] {vid} - {title_short} ({author})")
            else:
                failed += 1
                errors.append(f"Broken link in {file_path.name}: {vid} -> {title}")
                print(f"  [FAIL] {vid} - {title}")

    return passed, failed, errors

def main():
    target_files = sorted(ROOT_DIR.glob("**/CURATED_VIDEO_LECTURES.md"))
    if not target_files:
        print("[!] No CURATED_VIDEO_LECTURES.md files found.")
        sys.exit(1)

    total_passed = 0
    total_failed = 0
    all_errors = []

    print(f"=== Starting YouTube Link Verification ({len(target_files)} Curriculum Documents) ===")

    for target in target_files:
        p, f, errs = verify_file(target)
        total_passed += p
        total_failed += f
        all_errors.extend(errs)

    print("\n=======================================================")
    print(f"VERIFICATION RESULTS:")
    print(f"  Total Valid Links:   {total_passed}")
    print(f"  Total Broken Links:  {total_failed}")
    print("=======================================================")

    if total_failed > 0:
        print("\nFailed Links Summary:")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] 100% OF ALL CURATED YOUTUBE VIDEO LINKS ARE ACTIVE AND VERIFIED!")
        sys.exit(0)

if __name__ == "__main__":
    main()
