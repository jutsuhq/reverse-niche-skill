#!/usr/bin/env python3
"""Scan one channel (TikTok, YouTube, YouTube Shorts, Twitch: anything yt-dlp lists) and rank its videos.

Usage: scan_channel.py <channel-url> <out-dir> [--limit 60]

Writes <out-dir>/<handle>.tsv (all videos, newest first) and <handle>.json (raw yt-dlp output), then prints:
confidence, median and mean, outlier tiers, cadence, fatigue and hit rate, title patterns and the top 10.

Each video is scored against the channel's own median ("x_med"). The baseline excludes videos younger than
7 days (TOO NEW, their views are still growing) and sponsored posts (SPONSORED, paid reach).
Flags: OUTLIER >= 3x median, FLOP <= 0.3x median.
Needs yt-dlp on PATH or uv (runs `uvx yt-dlp`).
"""
import argparse, json, re, shutil, statistics, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("url"); ap.add_argument("out"); ap.add_argument("--limit", type=int, default=60)
a = ap.parse_args()

cmd = ["yt-dlp"] if shutil.which("yt-dlp") else ["uvx", "-q", "yt-dlp"]
raw = subprocess.run(cmd + ["--flat-playlist", "-J", "--playlist-end", str(a.limit),
                            "--extractor-args", "youtubetab:approximate_date", a.url],
                     capture_output=True, text=True)
if raw.returncode:
    sys.exit("FAIL yt-dlp: " + (raw.stderr.strip().splitlines() or ["no output"])[-1])
d = json.loads(raw.stdout)
rows = [e for e in d.get("entries") or [] if e.get("view_count") is not None]
if not rows:
    sys.exit("FAIL no videos with view counts (private account, or the site hid stats from yt-dlp)")

handle = (rows[0].get("uploader") or d.get("uploader") or d.get("channel") or d.get("id") or "channel").lstrip("@")
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
(out / f"{handle}.json").write_text(raw.stdout)

# Newest first by upload time when every row has one: pinned TikTok posts break the list order.
dated = all(e.get("timestamp") for e in rows)
if dated:
    rows.sort(key=lambda e: -e["timestamp"])
now = time.time()
text = lambda e: (e.get("title") or e.get("description") or "").replace("\t", " ").replace("\n", " ")
age = lambda e: (now - e["timestamp"]) / 86400 if e.get("timestamp") else None
day = lambda e: datetime.fromtimestamp(e["timestamp"], timezone.utc).strftime("%Y-%m-%d") if e.get("timestamp") else ""
SPONSORED = re.compile(r"#(ad|sponsored|partner)\b|paid partnership|\bsponsored\b", re.I)

for e in rows:
    e["_sponsored"] = bool(SPONSORED.search(text(e)))
    e["_new"] = age(e) is not None and age(e) < 7
base = [e for e in rows if not e["_sponsored"] and not e["_new"]]
if len(base) < 10:  # too few settled videos: fall back to every non-sponsored one
    base = [e for e in rows if not e["_sponsored"]] or rows
views = [e["view_count"] for e in base]
med = statistics.median(views) or 1
mean = statistics.mean(views)
n = len(base)
ranked = n >= 10


def flag(e):
    if e["_sponsored"]: return "SPONSORED"
    if e["_new"]: return "TOO NEW"
    if not ranked: return ""
    x = e["view_count"] / med
    return "OUTLIER" if x >= 3 else "FLOP" if x <= 0.3 else ""


def eng(e):  # likes + comments + shares + saves per view; None when the site gives none of them
    parts = [e.get(k) for k in ("like_count", "comment_count", "repost_count", "save_count")]
    return sum(p or 0 for p in parts) / e["view_count"] if e["view_count"] and any(parts) else None


rates = [r for r in map(eng, base) if r is not None]
eng_med = statistics.median(rates) if rates else None
permille = lambda e, k: f"{1000 * e[k] / e['view_count']:.1f}" if e.get(k) is not None and e["view_count"] else ""

with open(out / f"{handle}.tsv", "w") as f:
    f.write("date\tage_d\tviews\tx_med\tflag\tlikes_pm\tcomments_pm\tshares_pm\tsaves_pm\teng_lift\tdur_s\tsound\ttitle\turl\n")
    for e in rows:
        lift = f"{eng(e) / eng_med:.2f}" if eng_med and eng(e) is not None else ""
        f.write("\t".join(str(c) for c in (
            day(e), f"{age(e):.0f}" if age(e) is not None else "", e["view_count"], f"{e['view_count'] / med:.2f}", flag(e),
            permille(e, "like_count"), permille(e, "comment_count"), permille(e, "repost_count"), permille(e, "save_count"),
            lift, e.get("duration") or "", e.get("track") or "", text(e), e.get("url") or "")) + "\n")

conf = "exploratory" if n < 5 else "low" if n < 10 else "moderate" if n < 20 else "high"
print(f"{handle}: {len(rows)} videos, {sum(e['view_count'] for e in rows):,} views, baseline {n} videos, "
      f"median {med:,.0f}, mean {mean:,.0f}, confidence {conf}")
if not ranked:
    print("sample too small (<10 settled videos): no OUTLIER/FLOP flags, treat every number as anecdotal")
if mean / med >= 5:
    print(f"mean is {mean / med:.0f}x the median: one or two hits dominate this channel, judge the rest without them")
top = max(rows, key=lambda e: e["view_count"])
print(f"top video holds {top['view_count'] / sum(e['view_count'] for e in rows):.0%} of all views")
xs = [v / med for v in views]
print("tiers: " + "  ".join(f">={t}x: {sum(x >= t for x in xs)}" for t in (1.5, 3, 5, 20))
      + f"  flops <=0.3x: {sum(x <= 0.3 for x in xs)}")
print(f"skipped from baseline: {sum(e['_new'] for e in rows)} too new (<7 days), {sum(e['_sponsored'] for e in rows)} sponsored")

stamps = sorted(e["timestamp"] for e in rows if e.get("timestamp"))
span = (stamps[-1] - stamps[0]) / 86400 if len(stamps) > 1 else 0
if span:
    print(f"cadence: {len(stamps) / span:.1f} videos/day over {span:.0f} days, channel listing covers {age(rows[-1]) or 0:.0f} days")
elif not dated:
    print("cadence: unknown (this listing has no upload dates, e.g. YouTube Shorts); order = the site's listing order")

settled = [e for e in rows if not e["_new"] and not e["_sponsored"]]
if len(settled) >= 20:
    new10, prev10 = [e["view_count"] for e in settled[:10]], [e["view_count"] for e in settled[10:20]]
    hit = lambda vs: sum(v >= med for v in vs) / len(vs)
    r = statistics.median(new10) / med
    verdict = "tiring" if r < 0.5 else "growing" if r > 1.5 else "steady"
    print(f"fatigue: newest 10 median = {r:.2f}x channel median, {statistics.median(new10) / (statistics.median(prev10) or 1):.2f}x "
          f"the previous 10; hit rate (>=1x median) {hit(new10):.0%} now vs {hit(prev10):.0%} before -> {verdict}")
else:
    print("fatigue: needs 20+ settled videos, not enough here")

PATTERNS = {"vs": r"\bvs\.?\b|\bversus\b", "number": r"\d|\$", "question": r"\?", "pov": r"\bpov\b",
            "first person": r"^\s*(i|i'm|my|we)\b", "how/why": r"\b(how|why)\b", "list": r"\b(top|\d+ (ways|things|signs|reasons))\b"}
lines = []
for name, rx in PATTERNS.items():
    hits = [e["view_count"] / med for e in base if re.search(rx, text(e), re.I)]
    if len(hits) >= 3:
        lines.append(f"{name} n={len(hits)} median {statistics.median(hits):.2f}x")
if lines:
    print("title patterns: " + " | ".join(lines))

print("top 10 (x = views / channel median):")
for e in sorted(rows, key=lambda e: -e["view_count"])[:10]:
    print(f"  {e['view_count']:>12,}  {e['view_count'] / med:>6.1f}x  {e.get('duration') or '?':>4}s  {flag(e):9} {text(e)[:60]}  {e.get('url')}")
print(f"table: {out / (handle + '.tsv')}")
