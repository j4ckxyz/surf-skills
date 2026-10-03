# Reaching Surf from a server: a relay in the user's home

Surf's network edge (CloudFront) refuses some server and VPS addresses before the key is looked at, while the same request from a home connection goes through. `surf.py` reports this as `blocked`. The fix is to send your Surf requests through a device in the user's home.

Follow these steps in order.

## 1. Try directly first

Always run `surf.py doctor` on the machine you run on, with no relay, before anything else. Most setups work directly and need none of this.

Only carry on if `doctor` says `blocked`. For any other failure (`401`, `403`, `no_token`, a timeout), a relay will not help: see [setup.md](setup.md) step 3.

## 2. Tell the user, and ask two things

Don't go quiet and don't start installing things. Tell them what happened and what you are going to do about it, then ask. Something like:

> Surf is refusing connections from the server I run on. It does that to a lot of hosting addresses; your key is fine. I'm going to try to get it working by sending my Surf requests through a small relay on a device in your home instead. Two questions:
>
> 1. Do you have a device at home that stays switched on that I could use for this? A Raspberry Pi or a spare computer is plenty.
> 2. Am I allowed to SSH into it over Tailscale to set it up?

Then, from their answers:

- **They don't have Tailscale yet:** recommend it. It is a private network between their own devices, free for personal use, and it means nothing at home has to be opened to the internet. Both the home device and the machine you run on need it, signed in to the same account: https://tailscale.com/download (on Linux: `curl -fsSL https://tailscale.com/install.sh | sh`, then `sudo tailscale up`). Wait for them to say it is done.
- **Yes to both:** tell them what will run there before you touch it: one small Python script, listening only on the device's Tailscale address, able to reach `api.surf.social` and nothing else. Then go to step 3 and do it yourself.
- **They have a device but would rather you didn't SSH in:** fine. Give them step 3 as instructions to run themselves, one command at a time, and ask for the address it prints.
- **No device, or they'd rather not:** don't push. The other ways forward are asking Surf (via https://developers.surf.social) to allow the server's address, giving them the request id from the `blocked` message, or running you somewhere else, such as their own computer.

## 3. Set up the relay on the home device

`scripts/surf_proxy.py` is the relay. It is an example you can run as it is or adapt. Standard library only, Python 3.8+.

What it does, and what it will not do:

- Listens on the device's Tailscale address and passes connections on to `api.surf.social:443`. Nothing else: any other destination is refused, so it cannot be used as an open proxy.
- Accepts clients only from Tailscale addresses and the device itself.
- Carries TLS end to end. The relay never sees the API key or the data.

Copy the script over and try it (use the device's Tailscale name or address, and the user they gave you):

```
scp surf_proxy.py <user>@<device>:~/
ssh <user>@<device> python3 surf_proxy.py
```

It prints `listening on 100.x.y.z port 8459 …`. That address and port are what you need in step 4. If it says no Tailscale address was found, Tailscale is not running on the device: back to step 2.

If SSH fails, tell the user what the error was and ask them to check that both machines are on their Tailscale network and that SSH is allowed on the device.

To keep it running across restarts, as a systemd service (adjust the user and path; this needs `sudo` on the device, so say so before you do it):

```
# /etc/systemd/system/surf-proxy.service
[Unit]
Description=Relay for Surf API requests
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
User=pi
ExecStart=/usr/bin/python3 /home/pi/surf_proxy.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl enable --now surf-proxy
journalctl -u surf-proxy -f     # one line per connection
```

`Restart=on-failure` also covers a boot where Tailscale comes up after the service.

## 4. Point your Surf requests at it

On the machine you run on, add one line next to the key, in your environment or in `~/.surf-agent/.env`:

```
SURF_PROXY=http://100.x.y.z:8459
```

The device's Tailscale name works too, if names resolve where you run: `http://raspberrypi:8459`.

Only Surf requests use it: `surf.py` reads its own `SURF_PROXY` setting, so the rest of your traffic is untouched. Don't set `HTTPS_PROXY` to this relay: your other requests would be refused by it.

## 5. Check, and tell the user

Run `surf.py doctor` again. All checks ok and `through_proxy: true` means it works. Tell the user it is working and what is now running on their device, then carry on with [setup.md](setup.md) where you left off (step 3).

| You see | It means |
|---|---|
| `Network error … Connection refused` or a timeout | The relay is not running, or the address or port in `SURF_PROXY` is wrong, or the two machines cannot reach each other over Tailscale. |
| `Tunnel connection failed: 403` | The relay refused you: your address is outside the ranges it allows. Start it with `--allow-from <your range>`. |
| `blocked` still | The request did not go through the relay (check `through_proxy`), or the home connection is refused too. |
| `401` | The relay works. The key is the problem. |

If it still does not work after a couple of tries, stop and tell the user where it got stuck.

## Options

```
python3 surf_proxy.py --bind 100.x.y.z --port 8459 --allow-from 100.64.0.0/10 --dest api.surf.social:443
```

`--allow-from` and `--dest` can be repeated. Keep both as narrow as they are by default unless the user asks otherwise, and never listen on a public address.

## Removing it

On the device: `sudo systemctl disable --now surf-proxy`, then delete the service file and `surf_proxy.py`. On the machine you run on: remove the `SURF_PROXY` line.
