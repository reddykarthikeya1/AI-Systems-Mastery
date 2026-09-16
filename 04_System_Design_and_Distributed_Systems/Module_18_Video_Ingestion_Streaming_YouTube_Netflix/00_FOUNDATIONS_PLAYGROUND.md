# Beginner Playground - Video Ingestion and Streaming

> *"Nobody posts a film as one enormous file. It is cut into ten-second slices, each slice printed at five different qualities, and your player picks a slice at a time."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 1. Chunks, not files

Streaming works by cutting the video into short **segments**, typically 2 to 10
seconds, and listing them in a manifest. The player fetches segments one at a
time.

Two things fall out of this immediately: seeking is just "fetch a different
segment", and every segment is an ordinary static file a CDN can cache.

```python
VIDEO_SECONDS = 600
SEGMENT_SECONDS = 10

segments = VIDEO_SECONDS // SEGMENT_SECONDS
print(f"a {VIDEO_SECONDS}s video -> {segments} segments of {SEGMENT_SECONDS}s")
assert segments == 60

seek_to = 305
segment_index = seek_to // SEGMENT_SECONDS
print(f"seeking to {seek_to}s means fetching segment {segment_index}, nothing else")
assert segment_index == 30
```

---

## 2. The ladder, and what it costs to build

Each segment is encoded at several qualities - the **bitrate ladder**. A phone on
mobile data takes the 360p rendition; a TV on fibre takes the 4K one.

The cost is multiplication. One upload becomes one file per rung per segment, and
every one of them has to be transcoded, which is CPU-expensive and slow.

```python
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
```

---

## 3. Adaptive bitrate: the player decides, every segment

Before each segment the player measures how fast the last one arrived and picks a
rung it can sustain. Because the decision is per segment, a bandwidth collapse
costs you picture quality rather than a spinning wheel.

The viewer sees the image go soft for a few seconds. That is the whole point: a
worse picture is enormously better than a stall.

```python
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
```

---

## 4. The long tail decides your caching strategy

Video popularity is extremely skewed: a tiny fraction of titles takes the large
majority of views. That shape is what makes a CDN work - cache the small hot set
at the edge and you serve most traffic without ever touching origin.

The tail still matters, though. Those requests are rare *per title* and numerous
in total, and they all miss the cache. Which is why the answer is tiered: hot at
the edge, warm in a regional cache, cold in object storage.

```python
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
```

---

## 5. Predict before you run

A user's bandwidth drops from 5 Mbps to 1 Mbps halfway through a scene.
What does a player with one single-quality file do? What does a player with a
quality ladder do, and what does the viewer actually notice?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

One uploaded video becomes dozens of files. That fan-out - transcoding and
storing every rendition - is the dominant cost of running a video platform,
and it is why a 10-minute upload is not watchable for several minutes.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
