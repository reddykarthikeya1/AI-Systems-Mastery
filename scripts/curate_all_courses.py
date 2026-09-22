#!/usr/bin/env python3
"""Curator and generator for working YouTube video lectures across all 12 courses.
Searches YouTube directly, verifies every video via oEmbed API, and builds CURATED_VIDEO_LECTURES.md.
"""

import urllib.request
import urllib.parse
import json
import re
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent

def search_youtube_video(query: str, preferred_authors: Optional[List[str]] = None) -> Optional[Dict[str, str]]:
    """Searches YouTube and returns the first verified working video matching criteria."""
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  [!] Search error for '{query}': {e}")
        return None

    video_ids = list(dict.fromkeys(re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)))
    
    for vid in video_ids[:8]:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
        try:
            oreq = urllib.request.Request(oembed_url, headers=headers)
            with urllib.request.urlopen(oreq, timeout=6) as oresp:
                if oresp.status == 200:
                    data = json.loads(oresp.read().decode("utf-8"))
                    title = data.get("title", "")
                    author = data.get("author_name", "")
                    
                    if preferred_authors:
                        # If preferred authors given, check match
                        if any(pa.lower() in author.lower() or pa.lower() in title.lower() for pa in preferred_authors):
                            return {
                                "id": vid,
                                "url": f"https://www.youtube.com/watch?v={vid}",
                                "title": title,
                                "author": author
                            }
                    else:
                        return {
                            "id": vid,
                            "url": f"https://www.youtube.com/watch?v={vid}",
                            "title": title,
                            "author": author
                        }
        except Exception:
            continue

    # Fallback to first valid ID if preferred author not strictly matched
    for vid in video_ids[:4]:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
        try:
            oreq = urllib.request.Request(oembed_url, headers=headers)
            with urllib.request.urlopen(oreq, timeout=6) as oresp:
                if oresp.status == 200:
                    data = json.loads(oresp.read().decode("utf-8"))
                    return {
                        "id": vid,
                        "url": f"https://www.youtube.com/watch?v={vid}",
                        "title": data.get("title", ""),
                        "author": data.get("author_name", "")
                    }
        except Exception:
            continue

    return None

if __name__ == "__main__":
    test_res = search_youtube_video("Corey Schafer Python Decorators", ["Corey Schafer"])
    print("Test Search Result:", test_res)
