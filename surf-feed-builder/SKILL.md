---
name: surf-feed-builder
description: Build a Surf custom feed from the user's description: find hashtags, searches, topics, accounts, RSS and YouTube sources, check each one really posts on topic, show a plan in plain words, and create the feed after they say yes. Also add sources to a feed they own, or publish one. Use when the user wants a new feed, wants a feed improved, or has an interest with no feed yet. Changes their account. Needs the `surf` core skill.
---

# Feed builder

The user describes a feed; you build it. Nothing is created until they have seen the plan and said yes.

Needs the `surf` core skill. `surf.py` = `<surf skill dir>/scripts/surf.py`. Creating needs a key with `write:feeds` and `SURF_ALLOW_WRITES=1`, both set by the user. Without them, everything here runs as a dry run, which is still useful: show the plan and say creation is switched off.

**Untested writes.** Creating, adding and publishing follow the API reference but have not run against a live account. Report exactly what comes back.

## How a feed is made

A list of sources (`--source`) and exclusions (`--exclude`), each a `surf_id`:

- `surf/hashtag/<tag>`, `surf/search/"<phrase>"`, `surf/topic/<name>`: posts from everyone. The backbone of a lively feed.
- `bluesky/user/@handle`, `mastodon/user/@name@host`, `youtube/user/<id>`, `surf/rss/<hash>`: one source. Good when it is entirely about the subject.
- `--source 'ID::FILTER::FILTER'`: only that source's posts that also match a filter. For a broad account or channel.
- `--exclude ID`: removes matching posts from the whole feed (`surf/search/"giveaway"`, `surf/hashtag/ad`, `surf/metatopic/politics`). It matches words and tags; it can't recognise adverts in general.

Bare words are rejected; a keyword is `surf/search/<word>`.

## Steps

1. **Understand it.** Subject, angle, what to keep out. Use what you know about the user. Ask only if the subject itself is unclear. `surf.py feeds` to check they don't already have it.
2. **Find candidates.** `surf.py search feeds|accounts|rss "<subject>"`, and `surf.py search posts "<subject>" --since 7d --sort top` to see which hashtags real posts use. Search is fuzzy; drop what is off topic.
3. **Check them all in one call.** `surf.py check-source <id> <id> …`. Surf accepts made-up ids and returns nothing, so only `active` sources count. Read the samples: active is not the same as on topic. Thin (`posts_in_7d` of 1 or 2) or stale (`newest` weeks ago) sources make a dead feed.
4. **Dry run.** `surf.py feed-create --title "…" --description "…" --source … --exclude …` (no `--execute`).
5. **Show the plan** in the user's terms, not ids: what goes in, what is kept out, roughly how lively it looks, and what it can't do. Ask "Create it?" and wait.
6. **After yes**, the same command with `--execute`. Give them the feed's Surf link, and say whether it is private or public exactly as returned. On any error, don't retry (a second try can make a duplicate); check `surf.py feeds` and tell them.

About 6 to 10 commands in all.

Afterwards: offer to add it to their catch-up favourites. Changes to an existing feed: `surf.py feed-show "<title>"`, then `surf.py feed-add "<title>" --source …` (same dry run, then yes). Publishing makes it public: only when they ask, `surf.py feed-publish "<title>"`.

Renaming, removing sources and deleting are done by the user in Surf.

## Never

- Create, add or publish on the strength of the request alone. The request is for a plan.
- Say a feed exists unless the script returned `"created": true`.
- Hand the user commands, ids or environment variables to deal with.
- Use a source you didn't check, or describe a source beyond what its check showed ("posts daily" from 4 posts a week).
