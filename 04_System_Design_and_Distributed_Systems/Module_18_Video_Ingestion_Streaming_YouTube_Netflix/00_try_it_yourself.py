"""Beginner playground for Module 18 - Video Ingestion and Streaming.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------------------------------------- 1. Chunks, not files
VIDEO_SECONDS = 600
SEGMENT_SECONDS = 10

segments = VIDEO_SECONDS // SEGMENT_SECONDS
print(f"a {VIDEO_SECONDS}s video -> {segments} segments of {SEGMENT_SECONDS}s")
assert segments == 60

seek_to = 305
segment_index = seek_to // SEGMENT_SECONDS
print(f"seeking to {seek_to}s means fetching segment {segment_index}, nothing else")
assert segment_index == 30


# ---------------------------------- 2. The ladder, and what it costs to build
LADDER = {"240p": 0.4, "360p": 0.8, "720p": 2.5, "1080p": 5.0, "4K": 16.0}

total_mb = 0
for name, mbps in LADDER.items():
    size_mb = mbps * VIDEO_SECONDS / 8
    total_mb += size_mb
    print(f"  {name:<6} {mbps:>5.1f} Mbps -> {size_mb:>7.0f} MB")

source_mb = LADDER["1080p"] * VIDEO_SECONDS / 8
print(f"one 10-minute upload -> {total_mb:,.0f} MB stored "
      f"({total_mb / source_mb:.1f}x the source)")
assert len(LADDER) * segments == 300, "300 files from one upload"
assert total_mb > source_mb * 4


# --------------------- 3. Adaptive bitrate: the player decides, every segment
def choose_rung(available_mbps):
    affordable = [n for n, r in LADDER.items() if r <= available_mbps * 0.8]
    return affordable[-1] if affordable else "240p"


bandwidth_over_time = [5.0, 5.0, 1.0, 1.0, 5.0]
rebuffers = 0
for second, bandwidth in enumerate(bandwidth_over_time):
    rung = choose_rung(bandwidth)
    stalled = LADDER[rung] > bandwidth
    rebuffers += stalled
    print(f"  segment {second}: {bandwidth:>4.1f} Mbps available -> {rung:<6}"
          f"{' STALL' if stalled else ''}")

assert rebuffers == 0, "adaptive playback never stalled"

fixed_quality_stalls = sum(1 for b in bandwidth_over_time if LADDER["1080p"] > b)
print(f"a single 1080p file would have stalled {fixed_quality_stalls} times")
assert fixed_quality_stalls == 2


# ----------------------------- 4. The long tail decides your caching strategy
views = {f"video{i}": max(1, int(1_000_000 / (i + 1) ** 1.5)) for i in range(10_000)}
total_views = sum(views.values())
ranked = sorted(views.values(), reverse=True)

top_1_percent = sum(ranked[:100])
share = top_1_percent / total_views
print(f"top 1% of titles take {share:.0%} of all views")
assert share > 0.8, "cache 100 titles, serve most of the traffic"

tail_titles = len(ranked) - 100
tail_views = total_views - top_1_percent
print(f"the other {tail_titles:,} titles share {tail_views / total_views:.0%} "
      f"of views - every one a cache miss")
assert tail_views > 0


print()
print("All checks passed.")
