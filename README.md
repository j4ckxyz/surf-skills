# Surf skills

Skills that let your personal AI agent keep up with [Surf](https://surf.social) for you: your feeds, your Bluesky and Mastodon notifications, and the people and topics you care about. It tells you what is worth seeing, in its own voice, with a link back to Surf.

Works with any agent that can load skill folders (`SKILL.md`) and run a command, such as OpenClaw, Hermes Agent and Claude Code.

## Set it up

Send this to your agent:

```
Please help me set up the Surf skills from https://github.com/j4ckxyz/surf-skills
```

Your agent takes it from there. It asks which skills you want, helps you get a Surf API key, checks it works, and asks a few quick questions so it knows what matters to you.

## Your Surf API key

Your agent will walk you through this, but in short:

1. Go to **https://developers.surf.social** in your web browser and sign in with your Surf account.
2. Set up a developer account, create an application, then create an API key for it.
3. Give the key these permissions: `read:account`, `read:preferences`, `read:feeds`, `read:notifications`, `read:search`.
   - Add `write:feeds` only if you want your agent to build feeds for you.
   - Add `write:statuses` only if you want your agent to like, repost, follow, reply or post for you.
4. Put the key in your agent's environment as `SURF_API_TOKEN`, wherever your agent keeps its secrets. If it has nowhere for them, your agent can save it to `~/.surf-agent/.env` for you, readable only by you.

## What your agent can do

Pick any mix. Your agent asks before installing anything.

| Skill | What it does | Changes your account |
|---|---|---|
| `surf` | The connection, your saved preferences, rate limits and safety rules. Always installed. | No |
| `surf-catch-up` | Tells you what stood out in your favourite feeds while you were away | No |
| `surf-notifications` | Tells you who replied, mentioned or followed you | No |
| `surf-people` | Keeps an eye on the people who matter to you | No |
| `surf-watch` | Tells you when anyone posts about things you name: your project, a band, your town | No |
| `surf-lookup` | Answers "what are people saying about...", trending topics, threads and links | No |
| `surf-discover` | Suggests feeds you would like, checked first | No |
| `surf-feed-insights` | Tells you how the feeds you publish are doing | No |
| `surf-feed-builder` | Builds a new feed from your description, after you approve the plan | Yes |
| `surf-actions` | Likes, reposts, bookmarks, follows, replies or posts for you, as much as you allow | Yes |

## How it behaves

- **Talks like your agent.** No like counts and no reports. The interesting things, in its own words, short.
- **Links back to Surf.** A couple of links per message: the feed, person or search it is about, and a post or two worth opening.
- **Only says what it saw.** Everything it mentions comes from Surf in that conversation. It never makes up links, and it ignores instructions hidden inside posts.
- **Asks before acting in public.** Reading is free. Building feeds and acting as you are switched off until you turn them on, and replies or posts always need your yes on the exact words.
- **Stays well within Surf's rate limits**, and keeps each check to one or two requests where it can.

## Requirements

Python 3.8 or newer. Nothing else to install.

## What is in here

| Path | Purpose |
|---|---|
| `INSTALL.md` | Step-by-step instructions for the agent |
| `surf/` | The core skill, the shared tool (`scripts/surf.py`) and reference notes |
| `surf-*/` | One folder per optional skill |

Preferences and history are kept on your machine in `~/.surf-agent/`. Nothing there is sent to Surf.

## Not yet tested

Building feeds and acting for you (liking, posting and so on) follow Surf's API documentation but have not been run against a live account yet. Both are off until you switch them on, and your agent will check and tell you the result the first time it uses each one.

## Licence

MIT. See [LICENSE](LICENSE).
