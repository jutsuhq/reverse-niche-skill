# Example: a TikTok "mindsets climbing stairs" channel

**Request:** "Analyse this account in detail and design something better than it."

## 1. Numbers

`scan_channel.py` output, shortened:

```
mindset_channel: 30 videos, 42,992,025 views, baseline 30 videos, median 237,250, mean 1,433,068, confidence high
mean is 6x the median: one or two hits dominate this channel, judge the rest without them
cadence: 1.9 videos/day over 16 days
fatigue: newest 10 median 8,920 = 0.04x channel median  <- format tiring
tiers: >=3x: 9  flops <=0.3x: 10
```

One video holds 56% of all views (24.1M). The account is 16 days old, so the formula is promising but not proven.

| # | Title pattern | Views | Length |
|---|---|---|---|
| 1 | "A bleeds. B walks." | 24.1M | 18 s |
| 2 | "A vs B" | 2.9M | 18 s |
| 3 | "A vs B" | 2.5M | 27 s |
| 4 | "A bleeds. C explodes." | 2.2M | 18 s |
| 5 | "Some ride up. Some climb. Some go down." | 1.8M | 16 s |

## 2. Format

- **Theme:** mindsets as people (Obsession, Discipline, Ego, Adaptation, Motivation) racing up a staircase.
- **Structure:** one take, 16–28 s, 0 cuts (`download_videos.sh`). One figure breaks down, Discipline walks steadily to the top.
- **Technique:** a Blender-style 3D render: dark void, concrete stairs with glowing step edges, white mannequins with small labels.
- **Voice:** none. Whisper on the first 15 s returns only "Thanks for watching", so the audio is music only.
- **Sound:** a trending slowed phonk track.
- **CTA:** "Which one are you?" only in the caption.

## 3–4. What works and what flops

- Works: a two-word matchup, one take, a clear loser and a steady winner, a trending sound, under 20 s.
- Flops: the newest 10 videos repeat the same staircase with weaker matchups and get 3–35k. The format itself is tiring, not one video.

## 5. Weaknesses

1. No on-screen hook: without reading the caption, the race makes no sense.
2. The labels are unreadable on a phone.
3. The ending is ambiguous.
4. The same set every time.
5. Gore (blood, falling limbs) is a moderation and reach risk.
6. No progress meter, so the middle sags.
7. The CTA lives only in the caption.

## 6. Design: LAST STEP

| Weakness | Fix |
|---|---|
| 1 | "3 MINDSETS. 50 STEPS. ONLY ONE MAKES IT" in the first 2.5 s |
| 2 | Big coloured name labels with a step counter |
| 3, 7 | End card "WHICH ONE ARE YOU?" with numbered mindsets and "drop your number" |
| 4 | Each lane leaves its own light trail on the steps (the signature detail) |
| 5 | Obsession burns out (glow, embers, collapse) instead of bleeding |
| 6 | A 0–50 race rail on the left with a dot per climber |

Beat sheet, 19.5 s: the hook at 0–2.9 s · Talent's shortcut lift dies at 5.8 s · Obsession overtakes at 6.4 s, collapses at 9.4 s ·
Discipline passes at 10.3 s · a riser at 12.2–15 s · Discipline reaches the top at 15 s · the camera pulls wide for the end card at 15.6 s.

## 7. Episode ideas

1. Talent vs Discipline: the lift breaks halfway (builds on #5, 1.8M).
2. Ego vs Adaptation on a staircase that changes shape (builds on #3, 2.5M).
3. 4 mindsets, 100 steps: a longer race with two collapses (builds on #1, 24.1M).
4. Motivation vs Habit: Motivation's lane goes dark after the first 10 steps (builds on #1).
5. Luck vs Obsession vs Discipline: a dice step that teleports Luck (builds on #2, 2.9M).
