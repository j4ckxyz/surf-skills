---
name: surf-catch-up
description: Catch the user up on the Surf feeds they care about: what stood out while they were away, with the posts people actually engaged with rather than whatever was posted last. Use when they ask what's new or what they missed on Surf, for a summary of a feed, to change which feeds you watch, or on a scheduled check. Read-only. Needs the `surf` core skill.
---

# Catch-up

They were away; you tell them what was worth seeing in their feeds. Read-only.

Needs the `surf` core skill (its rules on truth, links, voice and rate limits apply). `surf.py` = `<surf skill dir>/scripts/surf.py`.

## Which feeds

The user's favourites (`surf.py favourites list|add|remove`). With none set, their pinned feeds. Use what you know about them: if they mention a feed they love, or keep asking about one, offer to add it.

## Getting the data

```
surf.py catch-up                    # favourites, since your last catch-up
surf.py catch-up --since 24h        # "what did I miss today"
surf.py catch-up --feeds "Tailscale"
surf.py posts "Tailscale" --rank    # one feed, most engaged
surf.py posts "Tailscale"           # one feed, newest first
```

`catch-up` does the work in one command: reads each feed, pulls Surf's top posts for busy feeds, drops posts nobody engaged with, removes repeats, and orders everything most-engaged first.

- `top_posts`: the best across all feeds, at most two per feed.
- `feeds`: busiest first, each with `feed_url` and a few more posts (`also`).
- `new_posts_nothing_standing_out`, `quiet_feeds`, `skipped`.

Too thin or too noisy for this user? Change the bar: `surf.py config set min_engagement 5` (default 2).

## Telling them

Pick what this user would find interesting. Usually two to four things, in your own words, with the one feed that was busiest. Not a list of every section.

- Link the feed it mostly came from (`feed_url`, opens in Surf) and the one or two posts they'd want to open.
- If two posts are one conversation (one quotes or replies to the other), tell it as one story, without picking a side.
- Nothing stood out? A line, or nothing if they asked for silence.
- A feed was skipped or `ranked_over` is present? Mention it briefly if it matters.

**Summarising a feed** means: what its most-engaged posts were about, told through those posts. Don't describe the "mood" of a feed or claim what "everyone" is saying from a handful of posts.

## Cost

One `catch-up` per check. Open a thread (`surf-lookup`) or another feed only if they ask about something specific. Up to 8 feeds per run; tell them if more were left out.

## After a scheduled run

Once the message is sent: `surf.py mark-seen catch-up`.
