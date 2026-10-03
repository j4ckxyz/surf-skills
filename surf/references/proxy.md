# Reaching Surf from a server: a relay in the user's home

Use this when `surf.py doctor` says `blocked`. Surf's network edge (CloudFront) refuses some server and VPS addresses before the key is looked at, while the same request from a home connection goes through. The fix is to send your Surf requests through a machine in the user's home.

`scripts/surf_proxy.py` is that relay. It is an example you can run as it is or adapt. Standard library only, Python 3.8+. A Raspberry Pi is plenty.

## What it does, and what it will not do

- Listens on the home machine's private address and passes connections on to `api.surf.social:443`. Nothing else: any other destination is refused, so it cannot be used as an open proxy.
- Accepts clients only from Tailscale addresses and the machine itself.
- Carries TLS end to end. The relay never sees the API key or the data.
- Only Surf requests use it. `surf.py` reads its own `SURF_PROXY` setting, so the rest of your traffic is untouched. Don't set `HTTPS_PROXY` to this relay: your other requests would be refused by it.

## What you need

Both machines on a private network the user owns. These steps use Tailscale. Ask the user before installing anything on their home machine, and tell them what will run there: one small Python script, listening only on their Tailscale address.

## 1. On the home machine

Copy `surf_proxy.py` there, then try it:

```
python3 surf_proxy.py
```

It prints `listening on 100.x.y.z port 8459 …`. That address and port are what you need in step 2. If it says no Tailscale address was found, start Tailscale there, or pass `--bind <address on the private network>`.

To keep it running across restarts, as a systemd service (adjust the user and path):

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

## 2. On the machine you run on

Add one line next to the key, in your environment or in `~/.surf-agent/.env`:

```
SURF_PROXY=http://100.x.y.z:8459
```

The home machine's Tailscale name works too, if names resolve where you run: `http://raspberrypi:8459`.

## 3. Check

Run `surf.py doctor`. All checks ok and `through_proxy: true` means it works. The relay's log shows a line per request.

| You see | It means |
|---|---|
| `Network error … Connection refused` or a timeout | The relay is not running, or the address or port in `SURF_PROXY` is wrong, or the two machines cannot reach each other on the private network. |
| `Tunnel connection failed: 403` | The relay refused you: your address is outside the ranges it allows. Start it with `--allow-from <your range>`. |
| `blocked` still | The request did not go through the relay (check `through_proxy`), or the home connection is refused too. |
| `401` | The relay works. The key is the problem. |

## Options

```
python3 surf_proxy.py --bind 100.x.y.z --port 8459 --allow-from 100.64.0.0/10 --dest api.surf.social:443
```

`--allow-from` and `--dest` can be repeated. Keep both as narrow as they are by default unless the user asks otherwise, and never listen on a public address.
