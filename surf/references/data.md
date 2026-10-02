# Output fields

Compact JSON. Empty and zero fields are left out.

## Posts

| Field | Meaning |
|---|---|
| `author.name`, `author.handle` | As the author set them. `author.bot` = declared bot. |
| `text` | Plain text, cut at 220 to 280 characters; `…` means cut. ` / ` is a line break. |
| `url` | The post on its own network. |
| `age` | `35m`, `6h`, `2d`. |
| `link` | The page the post shares: `url`, `title`. |
| `media` | `type` and the author's `alt` text if any. You can't see it. |
| `quotes_post` | A different post, by someone else, that this one quotes. |
| `reposted_by` | This is a repost; `author` wrote it. |
| `is_reply` | Part of someone's conversation. |
| `content_warning` | The author's warning; mention it rather than the text. |
| `flags` | `sensitive`, `explicit`, `suggestive`, `automated`, `podcast`. |
| `feed` | Which of the user's feeds it came from. |
| `engagement` | Only with `--counts`. |
| `id` | Only with `--ids`, and only for Bluesky posts. For `thread` and `act`. |

Lists of posts are ordered most-engaged first unless the output says otherwise (`order`).

## Links

| Field | Opens |
|---|---|
| `feed_url`, `on_surf`, `users_feed_url`, `surf_profile` | That feed, person, search or topic in Surf |
| `url` (post) | The post on Bluesky or Mastodon |
| `profile_url` | A person's profile on their network |

## Catch-up

`top_posts` (best across feeds, at most two per feed) · `feeds[]` with `feed_url`, `new_posts` (`40+` means at least 40), `people_posting`, `also` · `new_posts_nothing_standing_out` · `quiet_feeds` · `skipped` · `ranked_over` (present when ranking covered only the newest posts) · `feeds_from` (favourites, pinned, or named).

## Notifications

`summary` holds the totals; lists are capped. `needs_attention` = mentions, replies and quotes (the post is theirs, addressed to the user; `post.id` opens the thread). `new_followers`. `users_posts_that_got_most_attention` (the user's own posts). `posts_from_watched_accounts` (`status` = new post, `update` = edit). `surf_feed_activity`, grouped: `addedfeed` (someone added the user's feed to one of theirs), `addedfeed_home_timeline`, `favoritedfeed`, `joinedfeed`, `featured_surfshop` (Surf featured it). `counts_are_a_floor` = only the newest 100 were returned.

On Bluesky, replies arrive as `mention` with `post.is_reply`.

## People, watches, discover

`people check`: `people_with_new_posts[]` (`name`, `handle`, `on_surf`, `posts`), `nothing_new_from`. `people suggest`: `interacts_by` says how they interact with the user.

`watch check`: `matches[]` (`watch`, `why` in the user's words, `on_surf`, `posts`), `nothing_new_for`. The user's own posts are excluded.

`discover`: `suggestions[]` (`title`, `type`, `by`, `description`, `on_surf`, `surf_id`).

## surf_id forms

`surf/custom/<id>` feed · `surf/topic/<name>` · `surf/hashtag/<tag>` · `surf/search/<words>` or `surf/search/"phrase"` · `bluesky/user/@handle` · `mastodon/user/@name@host` · `bluesky/customfeed/at://…` · `surf/rss/<hash>` · `youtube/user/<id>` · `surf/podcast/<hash>` · `surf/metatopic/<name>` (mostly for excluding, e.g. politics).
