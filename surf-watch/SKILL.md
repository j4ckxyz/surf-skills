---
name: surf-watch
description: Standing watches on the open social web. Tell the user when anyone posts about something they care about, such as their own name, project, company, a band, a game, or their town, across Bluesky, Mastodon and RSS. Use when they say "tell me if anyone mentions X", "keep an eye out for X", "let me know when people talk about X", or on a scheduled check. Read-only. Needs the `surf` core skill.
---

# Watch

The user names things they want to hear about; you notice when people post about them. Read-only.

Needs the `surf` core skill (its rules on truth, links, voice and rate limits apply). `surf.py` = `<surf skill dir>/scripts/surf.py`.

## Watches

```
surf.py watch add '"Severance"' --why "favourite show, season 3 news"
surf.py watch add '"Pocket Weather"' --why "my app"
surf.py watch list
surf.py watch remove '"Severance"'
```

- Use the user's own words, in double quotes for an exact phrase. Every word needs 3+ characters. `AND` / `OR` in capitals combine terms.
- Save `--why` in their words. It tells you later what kind of mention they care about (news? people using their app? complaints?).
- Good watches are specific. "AI" will flood; their app's name won't.
- Things they keep asking about are good candidates; offer.

## Getting the data

```
surf.py watch check            # every watch, since last check, most engaged first
surf.py watch check --since 24h
```

One request per watch (up to 10). The user's own posts are left out.

## Telling them

Only the matches that fit the `why`. Search is fuzzy: a watch for "Surf" will catch surfing. Drop what is clearly off topic without comment.

Say who posted and what, briefly. Link the best post and the watch's Surf search (`on_surf`) so they can see the rest in Surf. Nothing relevant: say nothing about that watch.

If a watch keeps catching the wrong thing, suggest a tighter phrase and update it when they agree.

## After a scheduled run

Once the message is sent: `surf.py mark-seen watch`.
