# What to extract from each video

Fill one row per watched video. Mark every value as seen, heard or measured; leave a cell empty rather than guess.

| Field | What to write | How to get it |
|---|---|---|
| Views ×median | views divided by the channel median | `scan_channel.py` table |
| Topic | the subject in 3–6 words | title + sheet |
| Title / caption | the first line, its pattern (`X vs Y`, question, number, "POV:") | table `title` |
| Hook: visual | the first frame and the first motion (a face, an object mid-action, a before/after) | sheet, frame 1–2 |
| Hook: text | the on-screen words in the first 3 s, readable without sound? | sheet, frame 1–3 |
| Hook: spoken | the first sentence, and its type from `hook-patterns.md` | whisper first 15 s |
| Thumbnail / first frame | YouTube: the thumbnail; TikTok: the first frame | sheet, frame 1 |
| Structure | one take or cuts, the beats and their times | sheet + cut count |
| Pace | cuts per 10 s and the first cut time (`download_videos.sh`) | script output |
| First payoff | when the promise of the hook is first paid off, in seconds; does the video end soon after? | sheet + whisper |
| Length | seconds | table `dur_s` |
| Voice | none / AI / human, language | whisper first 15 s |
| On-screen text | none / labels / word-by-word captions, readable on a phone? | sheet |
| Sound | trending track name, original audio, or SFX | table `sound` |
| Visual technique | 3D render, live action, AI video, motion graphics, screen recording | sheet |
| Payoff | how it ends: a reveal, a winner, a twist, or nothing | last row of the sheet |
| CTA | in the video, in the caption, or none | sheet + caption |
| Engagement | `eng_lift` and the strongest per-1000 metric (saves = useful, shares = identity or humour, comments = debate) | table |
| Long-form test | would this premise work as a long video title? Strong short premises usually would | judgement |
| Risk | gore, real people, brands, minors, anything a platform may limit | sheet |

## Signals that usually separate outliers from flops

- The matchup or question is clear in the first 2 s without reading the caption.
- A concrete number in the hook ("50 steps", "3 mindsets", "$1 vs $1000").
- One continuous escalation with a visible winner.
- A loopable ending: the last frame leads back into the first.
- A trending sound used near its peak, not weeks later.
- A fresh variant of a proven theme; an exact repeat of last week's video flops.
