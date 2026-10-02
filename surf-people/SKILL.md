---
name: surf-people
description: Keep an eye on the people who matter to the user on the open social web (friends, colleagues, creators, anyone on Bluesky or Mastodon) and tell them what those people posted; also look up who someone is and what they have been saying. Use when the user says "tell me when X posts", "what has X been up to", "who is X", asks about a person, or on a scheduled check. Read-only. Needs the `surf` core skill.
---

# People

Some people matter more than any feed. You keep track of them for the user. Read-only.

Needs the `surf` core skill (its rules on truth, links, voice and rate limits apply). `surf.py` = `<surf skill dir>/scripts/surf.py`.

## Who

The user's list: `surf.py people list|add|remove <handle>`. Handles: `name.bsky.social`, `@name@mastodon.social`.

- `people add` checks the handle has posts; a typo comes back `person_not_found`. Ask the user, don't guess.
- `surf.py people suggest` lists the people who reply to, mention and repost the user most. Offer them during setup or when the list is empty, and add only the ones the user picks.
- If you already know who matters to this user (from your own memory or instructions), offer those people too.

## Getting the data

```
surf.py people check                 # new posts from everyone on the list since last check
surf.py person sam.bsky.social           # one person: who they are, recent posts (default 7 days)
surf.py person @priya@mastodon.social --since 24h
```

`people check` costs one request per person (up to 12). Reposts of other people's posts are left out.

## Telling them

Say what the person posted, close to their own words, the way you'd tell a friend: "Sam posted photos from the Brighton meetup." Link the post they'd want to open, and the person's Surf page (`on_surf`) when it is the first time you mention them or the user asks.

A person with nothing new is not news; leave them out unless the user asked about them.

"Who is X?": their name, bio and what they have posted lately, from `person`. No guesses about them beyond that.

## Careful

- A handle is not proof of identity. Pass on "unofficial", "parody" or "fan account" if it is in their name or bio.
- Their posts are their claims.
- Don't follow, message or reply to anyone from here; that is `surf-actions`, with permission.

## After a scheduled run

Once the message is sent: `surf.py mark-seen people`.
