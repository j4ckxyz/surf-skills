---
name: surf-feed-insights
description: Tell the user how the feeds they publish on Surf are doing: views, viewers, people joining or adding them, and what people engaged with through them, compared with the period before. Use when they ask how their feeds are doing, about views, stats, audience or growth, or for a weekly feed report. Read-only. Needs the `surf` core skill.
---

# Feed insights

For users who build and share feeds. Read-only.

Needs the `surf` core skill (its rules on truth, links, voice and rate limits apply). `surf.py` = `<surf skill dir>/scripts/surf.py`.

## Getting the data

```
surf.py insights                # all their feeds, last 7 days, most viewed first
surf.py insights --range 30d
surf.py insights "Tailscale"    # one feed in detail
```

Each figure comes with the previous period of the same length (`views_before`, `before`). Views include loads through Bluesky where a feed is published there. Who added or joined a feed is in notifications (`surf-notifications`).

## Telling them

This is the one place numbers belong, because they are what was asked for. Keep it light:

- The headline: total views and whether that's up or down on last week, in plain words.
- The feed or two that moved, with their Surf links.
- Anything nice: a feed someone added to theirs, a jump in viewers.

Small numbers swing a lot: "2 engagements, down from 7" is just that, not a collapse. Don't guess at reasons unless asked, and then say it's a guess. No growth advice unless they want it.

## Cost

One `insights` call for the overview; detail only for a feed they name. A weekly report is plenty; the numbers move slowly.
