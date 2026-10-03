# Setting up Surf

Aim: working in a few minutes, personal from the first message, and better every week. Don't run a long interview. Get connected, ask a few things, start helping, learn the rest as you go.

## 1. Which skills

If an install step already asked, skip this. Otherwise ask which they want, in a sentence or two, and install only those plus this core skill:

> I can keep up with your Surf for you: catch you up on your feeds, tell you who replied or followed, keep an eye on certain people or topics, answer "what's everyone saying about…", suggest feeds, and report how your feeds are doing. I can also build feeds or like and reply for you, but only if you want me to. Which of those sound good?

## 2. The key

Send them these steps in one message, with the address written out:

1. Open **https://developers.surf.social** in your browser.
2. Sign in with your Surf account and set up a developer account (it walks you through it; approval can take a little while).
3. Create an application, then create an **API key** for it.
4. Give it these permissions: `read:account`, `read:preferences`, `read:feeds`, `read:notifications`, `read:search`.
   - Only if you want me to build feeds: add `write:feeds`.
   - Only if you want me to like, repost, follow, reply or post for you: add `write:statuses`.

Then the key goes into your environment as `SURF_API_TOKEN`. Ask them to add it wherever your platform keeps your secrets or environment variables. If your platform has no such place, save it yourself:

```
mkdir -p ~/.surf-agent && chmod 700 ~/.surf-agent
# write one line, SURF_API_TOKEN=<their key>, to ~/.surf-agent/.env
chmod 600 ~/.surf-agent/.env
```

Don't repeat the key back or copy it anywhere else.

## 3. Check it works

Run `surf.py doctor`, then `surf.py whoami`.

- All ok: tell them, naming their linked accounts so they can confirm it is them ("You're connected as Alex, with Bluesky alex.bsky.social and Mastodon @alex@mastodon.social.").
- A check failed with `403`: it names the missing permission. Ask them to add it to the key, then run `doctor` again.
- `no_token` / `401`: the key is not set or not valid. Back to step 2.
- A check failed with `blocked`: Surf's network (CloudFront) refused this machine's address before the key was looked at. This mostly happens when you run on a server or VPS. The key is fine, so don't ask for another one and don't keep retrying. Tell them plainly, give them the request id from the message, and offer the two ways forward: ask Surf (via https://developers.surf.social) to allow this address, or run you somewhere else, such as their own computer.

## 4. Make it theirs (three questions, defaults offered)

Start from what you already know about this user; don't ask what you know. Then:

1. **"Which feeds should I watch for you?"** Run `surf.py feeds --most-visited` and `surf.py feeds --pinned`. Offer the three or four they use most, by name: "You seem to live in Tailscale, Film Photography and Indie Games. Those?" Save with `surf.py favourites add …`.
2. **"Anyone whose posts you never want to miss?"** If they have `surf-people`, run `surf.py people suggest` and offer the people who interact with them most, plus anyone you know matters to them. Save with `surf.py people add …`.
3. **"Anything you want to hear about whenever it comes up?"** (their name, project, company, a band, their town). If they have `surf-watch`, save with `surf.py watch add '"<phrase>"' --why "<their reason>"`.

Then one line on timing: "I'll check in the morning and evening and only message if there's something worth it. Sound right?" Save their answer: `config set check_every 12h`, `config set silent_when_empty true`, `config set quiet_hours "22:00-08:00"` as applicable.

Anything else they mention about how they like updates ("short", "no music stuff on weekdays", "always tell me when Sam replies"), save in their words: `surf.py config set notes "<their words>"`.

## 5. Switches for changing things

Only if they chose these:

- **Building feeds** needs `SURF_ALLOW_WRITES=1` in your environment.
- **Liking, reposting, following, replying, posting** needs `SURF_ALLOW_ACTIONS=1`, and their choices in the `surf-actions` skill.

Ask them to set these. Don't set them yourself unless they tell you to. Until they are set, the script only shows what it would do.

## 6. Schedule

Use your platform's own scheduler to run the checks they want at `check_every`. Each run:

1. `surf.py config show`
2. the one or two commands for what they asked for, with `--since last`
3. message them if something is worth it
4. after the message is sent: `surf.py mark-seen <what>` for each

## 7. First taste

Run a catch-up (or notifications) now and send it, so they see what it is like. Ask if they want it shorter, longer, or different, and save the answer. Tell them when the next check is.

## Later

- When they react to something, save it immediately and confirm in a few words.
- Every few weeks, if it fits your relationship, offer one small improvement: a feed from `discover`, a person they keep engaging with, a watch for something they keep asking about.
