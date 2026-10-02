---
name: surf-lookup
description: Look things up on the open social web through Surf: what people are saying about a topic right now, what's trending, the replies to a post, where a link goes and what it is. Use when the user asks "what are people saying about X", "any news on X", "what's trending", "what did people reply to this", "what's this link", or wants feeds or accounts about something. Read-only. Needs the `surf` core skill.
---

# Lookup

Questions about what is happening out there, answered from real posts. Read-only.

Needs the `surf` core skill (its rules on truth, links, voice and rate limits apply). `surf.py` = `<surf skill dir>/scripts/surf.py`.

## Getting the data

| They ask | Run |
|---|---|
| what are people saying about X | `surf.py search posts "X" --since 24h --sort top` |
| anything new on X | `surf.py search posts "X" --since 24h --sort recent` |
| what's trending | `surf.py trending` |
| what did people reply | `surf.py thread <post id>` |
| what's this link | `surf.py article <url>` |
| feeds / accounts about X | `surf.py search feeds "X"`, `surf.py search accounts "X"` |
| anything else | `surf.py api …` (see the core skill's `references/api.md`) |

Search: plain words are all required; `"double quotes"` for a phrase; `AND` / `OR` in capitals. Start with the user's words. Off topic? Tighten once. Little in 24h? Try `--since 7d`. Two searches per question at most.

`thread` opens Bluesky posts (add `--ids` to the search to get their ids) and posts from the user's own notifications. Mastodon posts from search can't be opened (`thread_unavailable`); link them instead.

`trending` gives topic names only. To say what a topic is about, search it.

## Telling them

Answer the question in your own words, through what the posts actually say. Credit people by name. If posts disagree, say so and give each side; no verdict. You saw a sample, so say "the posts I'm seeing" rather than "everyone".

Don't fill gaps with background you know as if the posts said it. If they don't explain why something happened, you can say that.

`article` gives title, author, date and the opening only.

Links: the search on Surf (`on_surf`) so they can keep reading, plus the one or two posts that say it best.

## Cost

One search per question, two at most. One `thread` or `article`, only for the thing asked about. With `trending`, ask which topic they want before searching.
