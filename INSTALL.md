# Installing the Surf skills (for the agent)

The user has asked you to set up the Surf skills from https://github.com/j4ckxyz/surf-skills. Follow these steps in order.

## 1. Get the files

Download the repository somewhere you can read it, for example:

```
git clone https://github.com/j4ckxyz/surf-skills.git
```

If you cannot run git, download https://github.com/j4ckxyz/surf-skills/archive/refs/heads/main.zip and unpack it.

Check Python is available: `python3 --version` must show 3.8 or newer.

## 2. Ask which skills they want

Ask before installing anything. Do not install everything by default and do not choose for them. Offer the skills in plain words, something like:

> I can keep up with your Surf for you. Pick any of these:
> - **Catch-up**: what stood out in your favourite feeds while you were away
> - **Notifications**: who replied, mentioned or followed you
> - **People**: keep an eye on the people who matter to you
> - **Watch**: tell you when anyone posts about things you care about (your project, a band, your town)
> - **Lookup**: "what are people saying about...", trending, threads, links
> - **Discover**: suggest feeds you'd like
> - **Feed insights**: how the feeds you publish are doing
> - **Feed builder**: build new feeds from a description (changes your account; I show you the plan first)
> - **Actions**: like, repost, bookmark, follow, reply or post for you (changes your account; you decide how much I can do without asking)

"All of them" is a fine answer, but it has to be theirs. If they are unsure, suggest catch-up, notifications and people to start with.

## 3. Install

Copy the folders they chose, plus `surf/` always, whole and side by side, into the directory your platform loads skills from:

| Folder | Skill |
|---|---|
| `surf/` | Core, always |
| `surf-catch-up/` | Catch-up |
| `surf-notifications/` | Notifications |
| `surf-people/` | People |
| `surf-watch/` | Watch |
| `surf-lookup/` | Lookup |
| `surf-discover/` | Discover |
| `surf-feed-insights/` | Feed insights |
| `surf-feed-builder/` | Feed builder |
| `surf-actions/` | Actions |

If you do not know where your platform loads skills from, check its documentation or ask the user. Do not guess.

The shared tool is then `python3 <skills directory>/surf/scripts/surf.py`. Wherever the skills say `surf.py <command>`, run it that way.

## 4. Set up

Read `surf/SKILL.md`, then follow `surf/references/setup.md` from step 2. It covers getting the API key from https://developers.surf.social, where to put it, testing it, and three quick questions that make it personal.

## Later

- **Add a skill:** copy its folder in and ask its setup question. Feed builder and actions also need extra permissions on the key and a switch in your environment (setup step 5).
- **Remove a skill:** delete its folder. If it was feed builder or actions, ask the user to remove the switch too.
- **Update:** pull or download the repository again and copy the installed folders over the old ones. Preferences in `~/.surf-agent/` are kept.
- **Remove everything:** delete the folders, the key and `~/.surf-agent/`. The user can revoke the key at https://developers.surf.social.
