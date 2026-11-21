#!/usr/bin/env bash
# Download videos and make one contact sheet each: duration, cut count, cuts per 10 s, first cut, 24 frames.
# Usage: download_videos.sh <out-dir> <video-url>...   (take the URLs from scan_channel.py's "top" and flop rows)
set -euo pipefail
out="$1"; shift; mkdir -p "$out"
dl=(yt-dlp); command -v yt-dlp >/dev/null || dl=(uvx -q yt-dlp)
for u in "$@"; do
  f=$("${dl[@]}" -q --no-warnings -f "b[ext=mp4]/b" -o "$out/%(id)s.%(ext)s" --print after_move:filepath "$u")
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  times=$(ffmpeg -hide_banner -nostats -i "$f" -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 \
        | { grep -o 'pts_time:[0-9.]*' || true; } | cut -d: -f2)
  cuts=$(printf '%s' "$times" | grep -c . || true)
  first=$(printf '%s\n' "$times" | head -1); first=${first:+$(printf '%.1f' "$first")}
  ffmpeg -v error -y -i "$f" -vf "fps=24/${dur},scale=160:-1,tile=6x4" -frames:v 1 "${f%.*}-sheet.jpg"
  printf '%s  %.1fs  %s cuts (%.1f per 10 s, first at %ss)  %s\n' "$(basename "$f")" "$dur" "$cuts" \
    "$(echo "$cuts * 10 / $dur" | bc -l)" "${first:--}" "${f%.*}-sheet.jpg"
done
