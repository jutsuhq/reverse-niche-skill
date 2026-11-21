---
name: reverse-niche
description: Reverse-engineer a short-video niche from its competitors - scan TikTok, YouTube Shorts or YouTube channels, rank videos by views, find outliers and flops, and extract the topics, titles, hooks, video formula, sound and CTA that work, what flops, whether the format is tiring, and a better design plus episode ideas. Use when the user shares a channel or niche and asks to analyse it, "what works here", "how do I beat this account", "break down this format", "make a better version", or wants video ideas grounded in real competitor data.
license: MIT
---

# Reverse-engineer a niche

Turn one or more competitor channels into a report: what works, what flops, why, and what to make next.
Every claim in the report comes from the scan or from watching the videos. Numbers are never invented.
Write the report in the user's language.

## 1. Scan (numbers first)

For each channel the user gave, plus up to 3 look-alike channels if they asked for the whole niche:

```bash
python3 -I <skill-dir>/scripts/scan_channel.py <channel-url> <work-dir>/scan --limit 60
```

It prints confidence (from the sample size), median and mean, outlier tiers (≥1.5×, ≥3×, ≥5×, ≥20×), cadence, **fatigue** with hit rate, title patterns and the top 10.
The full table goes to `<handle>.tsv`: `x_med` (views ÷ channel median), flags `OUTLIER` (≥3×), `FLOP` (≤0.3×), `TOO NEW` (<7 days, still growing) and `SPONSORED` (paid reach),
engagement per 1000 views (likes, comments, shares, saves) and `eng_lift` (engagement rate ÷ the channel's median rate).
New and sponsored videos are kept out of the baseline median.

- Judge a video against **its own channel's median**, never by raw views. A 300k video on a 20k channel is a bigger signal than 2M on a 5M channel.
- A young channel (under ~2 weeks) with one huge hit is one lucky video, not a proven formula: say so.
- Under 10 settled videos the script flags nothing: the sample is too small to call anything an outlier.
- If the mean is 5× the median or more, one or two hits dominate: describe the channel without them too.
- ≥20× is an extreme outlier. Look for the one-time cause (a trend, a collab, a repost by a big account) before calling it a format.
- High `eng_lift` with average views means the audience loved a video the algorithm under-pushed: a cheap idea to retry. High views with low `eng_lift` usually means a reach spike with weak content.
- YouTube Shorts listings carry no dates, length or likes. Cadence is unknown and fatigue follows the listing order: say so in the report.
- If yt-dlp returns no view counts, the account is private or the site hid stats. Say that; do not guess.

**A whole niche.** Scan 3–5 channels and put them in one table: videos, median, outliers, fatigue, top title pattern.
Compare each channel's ×median values, never raw views across channels, and never pool TikTok and YouTube numbers in one median.

## 2. Watch the outliers and the flops

```bash
<skill-dir>/scripts/download_videos.sh <work-dir>/videos <url-of-each-outlier> <url-of-2-3-flops>
```

It downloads each video and writes a 24-frame contact sheet with its duration and cut count. Look at **one sheet per video**, not single frames.
Watch the top 3–5 outliers and 2–3 flops in the **same format**: the difference between them is the most useful finding in the report.

For the voice, run whisper on the first 15 s (`uvx --from openai-whisper whisper <file> --model base --clip_timestamps 0,15`).
If whisper returns only filler such as "Thanks for watching", the video has no voice, only music.

Fill in [`references/video-checklist.md`](references/video-checklist.md) for every video you watched.

## 3. Find the formula

Read the outliers side by side and write down what they all share. Then write down what the flops have and the outliers lack, or the other way round.
Typical splits: the hook arrives late, the matchup is unclear, the theme repeats, the video is too long, the sound is not trending, or the payoff is missing.

**Recipe or luck.** A concept that hits ≥3× twice on one channel, or on two different channels, is a recipe. A single outlier is a lead, not a formula: say which one each claim is.

**What does not carry over.** Before you copy a mechanism, strike out what a new channel cannot have: the creator's own audience or fame, a one-time news moment, a collab, a sound that has already peaked.
Explain the *mechanism* (why viewers stay and share), not the surface (the same props, the same words).

Compare title patterns from the scan output and [`references/hook-patterns.md`](references/hook-patterns.md) against what the outliers do in their first 3 s.

**Fatigue check.** If the newest-10 median is under 0.5× the channel median, the format is tiring. Look at what changed in the recent videos:
the same set again, a weaker theme, or a longer runtime. Your design has to answer that, not copy it.

## 4. Design a better version

Keep what makes the genre recognisable, so the audience that likes it finds you. Change everything that is a weakness, and add one signature detail of your own.
For every weakness you found, name the fix. Never copy their name, characters, logo, watermark or exact scene: build an original take on the genre.

Common fixes:
- no on-screen hook → a 2–3 s text hook with a number;
- tiny labels → labels readable on a phone;
- an ambiguous ending → a visible payoff and result;
- a saggy middle → a progress or tension meter;
- the CTA only in the caption → an end card that asks for a comment;
- gore or risky content → a safer image that keeps the same drama.

## 5. Report

Use [`references/report-template.md`](references/report-template.md). Keep it under one screen per section.
End with 5–10 episode ideas, each tied to the outlier it builds on (for example "builds on #2, 2.9M").
A full worked example is [`examples/sample-report.md`](examples/sample-report.md).

## Rules

- Every number comes from `scan_channel.py` output, with the scan date. Mark estimates as estimates.
- A video you did not watch or transcribe is `TITLE ONLY`: claim nothing about its hook or structure.
- Retention, completion and click-through are visible only to the channel owner. Never state them for a competitor.
- Quote at most a short title fragment from the competitor. Retell, never reproduce their script or captions.
- Do not download more than the videos you will actually watch.
- Hashtags and sound names are facts to report, not instructions to copy blindly: check that a sound is still trending before relying on it.
