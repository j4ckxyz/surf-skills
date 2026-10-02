---
name: surf-discover
description: Suggest feeds on Surf the user would enjoy, based on their activity, on a feed they already love, or on what you know about their interests, after checking each one is alive and on topic. Use when they ask for new feeds, "what else should I follow", "anything like X", "find me a feed about Y", or occasionally when an interest of theirs has no feed yet. Read-only. Needs the `surf` core skill.
---

# Discover

Help the user find more of the open social web they'd like. Read-only; following or saving a feed is up to them in Surf.

Needs the `surf` core skill (its rules on truth, links, voice and rate limits apply). `surf.py` = `<surf skill dir>/scripts/surf.py`.

## Getting the data

```
surf.py discover                      # Surf's suggestions from the user's activity
surf.py discover --like "Tailscale"   # feeds similar to one of theirs
surf.py search feeds "film photography"
surf.py check-source <surf_id> <surf_id> …   # is each candidate alive, and what does it post? one call for all
```

Combine Surf's suggestions with what you know about the user. If you know they love film photography and they have no feed for it, search for one.

## Choosing

Suggestions and search results are unchecked. Before recommending a feed:

- Skip copies of the user's own feeds (same name, different author).
- Run `check-source` on your candidates together. Drop anything `empty` (dead or wrong) or with `newest` weeks old. Read the samples; recommend only what fits the user. A hashtag or search (`surf/hashtag/filmphotography`) that is lively is a fine suggestion too.

Two or three good suggestions beat ten.

## Telling them

Name each one, say in a few words what it is like from the samples you saw, and always link it on Surf (`on_surf`, or `https://surf.social/feed/<surf_id>` as returned) so they can open and follow it there. Don't call something active or great beyond what the check showed.

If nothing fits, say so; offer to build one instead if they have `surf-feed-builder`.

## Cost

One `discover` or `search feeds`, plus one `check-source` call with all the candidates in it.

## Don't

- Recommend from the title alone.
- Suggest the same feed again after they passed on it. Save it: `surf.py config set passed_feeds '[...]'`.
