# Surf API: what works, and the quirks

Base: `https://api.surf.social/v1`. `surf.py api <path> key=value …` reads any GET endpoint with the user's key, shrinks the result, and counts it against the budget. Use the ready-made commands first; reach for `api` when they don't answer the question.

Everything below was checked with a real key on 2 October 2026. "Works" means it returned real data. Scopes in brackets are what the key needs.

## Reads that work

| Endpoint | Gives | Ready-made command |
|---|---|---|
| `/account` [read:account] | The user's name, bio, linked accounts. **Also their email: never repeat it.** | `whoami` |
| `/preferences/account` [read:preferences] | Pinned feeds (`feedPins`) and other settings | `feeds` |
| `/custom` [read:feeds] | The user's custom feeds with sources. Large: use `--fields` | `feeds`, `feed-show` |
| `/custom/<id>` | One custom feed. `<id>` with or without `surf/custom/` | `feed-show` |
| `/feed?surf_id=` | Title, type, description of any feed, person, topic or search | |
| `/feed/posts?surf_id=&limit=&since=&sort=` | Posts of any feed, person (`bluesky/user/@handle`, `mastodon/user/@name@host`), topic, hashtag, search | `posts`, `person` |
| `/feed/speeddial?limit=` | Feeds the user opens most | `feeds --most-visited` |
| `/feed/following?surf_id=` | Public custom feeds that include this source | |
| `/notifications` [read:notifications] | Bluesky, Mastodon and Surf notifications, merged | `notifications` |
| `/search/posts?q=&since=&sort=top` [read:search] | Matching posts across networks | `search posts` |
| `/search/maestra/feeds?q=` | Feeds, podcasts, YouTube channels, starter packs | `search feeds` |
| `/search/bluesky/searchActors?q=` | Bluesky accounts | `search accounts` |
| `/search/rss/search?q=` | RSS feeds | `search rss` |
| `/search/publications?q=&count=` | Longform blogs (Leaflet / standard.site) | |
| `/search/discover?type=recommended` | Trending search topics | `trending` |
| `/search/discover?type=interests` | Feed suggestions from the user's activity | `discover` |
| `/search/discover?type=similar&feed_id=` | Feeds similar to one | `discover --like` |
| `/account/lookup?account=` | A Bluesky profile by handle | `person` |
| `/statuses/<id>`, `/statuses/<id>/context?service=` | A post and its thread | `thread` |
| `/post?id=` | A post by id (Bluesky `at://` ids) | |
| `/content/extract?url=` | Title, author, date, opening of a web page | `article` |
| `/content/resolve?url=` | Where a short link goes | |
| `/content/topics?url=` | Tags and language of a page | |
| `/analytics/feeds/summary?range=7d` [read:feeds] | Views and engagement for all the user's feeds | `insights` |
| `/analytics/feed/<id>/overview`, `/top-posts` | One feed in detail | `insights "<feed>"` |
| `/audio/vibes/<vibe>/posts` | Posts matching a mood. Works, but full of spam; avoid | |

## Not available with a read-only key

| Endpoint | Needs | Result without it |
|---|---|---|
| `/ai/feed-summary`, `/ai/thread-summary`, `/ai/ask`, `/ai/fact-check` | `use:ai` (100 a day) | 403 |
| `/audio/briefing/*`, `/audio/quiz/*`, podcast transcripts and show notes | `read:audio` | 401 |
| `/sonars/*` | `read:sonars` | 403 |
| `/playback` | `read:playback` | 403 |

If the user's key has these, they work through `api`; nothing in the skills depends on them.

## Changes (only through `surf-feed-builder` and `surf-actions`)

`POST /custom`, `/custom/<id>/operators`, `/custom/<id>/publish` [write:feeds]; `POST /statuses`, `/statuses/<id>/favourite|reblog|bookmark` (and the `un…` forms), `/accounts/<id>/follow|unfollow` [write:statuses]. **Not tested**: the test key was read-only. `api` never sends these.

## Quirks

1. **`since` takes durations, not timestamps.** `24h`, `7d`, `30m`, `3600s` work. An ISO time fails with `For input string: "2026-…"` despite the docs. The script converts for you.
2. **Surf accepts any id and returns nothing.** `surf/topic/made-up`, a misspelt handle: empty, no error. Empty means "check the id", not "quiet".
3. **`sort=top` on feeds is slow** and sometimes times out at 30 s. The script tries it once, briefly, only for busy feeds.
4. **`surf/trending/dynamic` takes about a minute.** Don't use it; `trending` is instant.
5. **`/notifications` ignores `limit`** and returns about 100 merged items; `include_types` does not filter Surf's own types. Filter client-side (the script does).
6. **Threads open only for Bluesky posts, and for Mastodon posts from the user's own notifications.** Mastodon ids seen in search and feeds belong to other servers and give 404. The same limit applies to actions. For Mastodon, pass `service=mastodon`; the default is Bluesky.
7. **`/account/lookup` returns null for Mastodon handles.** Use the person's feed (`person @name@host`).
8. **Search returns reposts as separate results**, so the same post can appear several times. The script removes duplicates.
9. **Search is fuzzy.** "mechanical keyboards" returned a writing podcast first. Judge every result.
10. **`surf/bookmarks/all`, `surf/timeline/*`, `surf/feeds/followed` are not readable as feeds** (404). They only work as sources inside a custom feed.
11. **`/custom` is about 350 KB for a heavy user.** Always `--fields`.
12. **`/content/extract` gives the opening only**, never the full article.
13. **Analytics "views" include loads through Bluesky** where a feed is published there.
14. **Discover can suggest copies** of the user's own feed under the same name, made by other people.
15. **A request without a User-Agent can be blocked by Cloudflare** (error 1010). The script always sends one.
16. **Single-source feeds ignore `since`.** A person (`bluesky/user/…`, `mastodon/user/…`), YouTube channel or podcast returns its latest posts whatever the window, including ones months old. The script drops posts outside the window; through `api`, check `created_at` yourself.
17. **Action ids must be full.** A Bluesky post id is the whole `at://…/app.bsky.feed.post/…` URI, not the short code at the end of a bsky.app link. Account ids for follow are DIDs (`did:plc:…`).
18. **Rate limit headers**: `X-RateLimit-Remaining` counts down per minute and resets after 60 s. AI endpoints have a separate 100-a-day limit.

## Links that open in Surf

`https://surf.social/feed/<surf_id, URL-encoded>` opens any feed, person, topic or search in Surf:

- feed: `surf/custom/<id>`
- person: `bluesky/user/@handle`, `mastodon/user/@name@host`
- search: `surf/search/<words>`
- topic: `surf/topic/<name>`

The script already returns these as `feed_url` and `on_surf`. Surf has no clean page for a single post; link posts to their own network (`url`).
