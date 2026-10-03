#!/usr/bin/env python3
"""surf_proxy.py -- lets an agent on a server reach Surf through the user's home connection.

Surf's network edge refuses some server and VPS addresses (surf.py reports this as `blocked`). Run this on a
machine in the user's home (a Raspberry Pi is plenty) that shares a private network with the agent, such as
Tailscale. The agent then sets SURF_PROXY=http://<this machine>:8459 and surf.py sends its requests this way.

Standard library only (Python 3.8+). It is a small CONNECT proxy, deliberately narrow:

  one destination   only api.surf.social:443. Anything else is refused, so this is not an open proxy.
  private clients   only Tailscale addresses and this machine itself, unless --allow-from says otherwise.
  private address   listens on this machine's Tailscale address, never on every interface unless told to.
  sees nothing      the tunnel carries TLS end to end. The API key and the data pass through encrypted.

Run:   python3 surf_proxy.py            (options: --bind, --port, --allow-from, --dest)
Setup: see references/proxy.md
"""

import argparse
import ipaddress
import select
import socket
import socketserver
import subprocess
import sys
import time

DEST = "api.surf.social:443"
PORT = 8459
# Tailscale's address ranges, plus this machine itself.
PRIVATE_CLIENTS = ("100.64.0.0/10", "fd7a:115c:a1e0::/48", "127.0.0.0/8", "::1/128")
CONNECT_TIMEOUT = 15   # seconds to read the request and reach Surf
IDLE_TIMEOUT = 120     # seconds a tunnel may sit silent before it is closed


def log(message):
    sys.stderr.write("%s %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), message))
    sys.stderr.flush()


def tailscale_address():
    """This machine's Tailscale IPv4 address, or None when Tailscale is missing or signed out."""
    try:
        out = subprocess.run(["tailscale", "ip", "-4"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    lines = out.stdout.split()
    return lines[0] if out.returncode == 0 and lines else None


def relay(client, upstream):
    """Copy bytes both ways until either side closes or the tunnel goes quiet."""
    pair = {client: upstream, upstream: client}
    while True:
        ready, _, _ = select.select(list(pair), [], [], IDLE_TIMEOUT)
        if not ready:
            return
        for source in ready:
            data = source.recv(65536)
            if not data:
                return
            pair[source].sendall(data)


class Tunnel(socketserver.StreamRequestHandler):
    timeout = CONNECT_TIMEOUT

    def refuse(self, status, reason):
        log("refused %s: %s" % (self.client_address[0], reason))
        body = (reason + "\n").encode("utf-8")
        self.wfile.write(b"HTTP/1.1 %d Refused\r\nContent-Type: text/plain\r\nContent-Length: %d\r\n"
                         b"Connection: close\r\n\r\n" % (status, len(body)) + body)

    def handle(self):
        peer = ipaddress.ip_address(self.client_address[0])
        peer = getattr(peer, "ipv4_mapped", None) or peer
        if not any(peer in network for network in self.server.clients):
            return self.refuse(403, "This address may not use the proxy.")
        parts = self.rfile.readline(4096).decode("latin-1").split()
        for _ in range(100):  # the request's headers are not needed
            if self.rfile.readline(4096) in (b"\r\n", b"\n", b""):
                break
        if not parts:  # opened and closed without a request, such as a port check
            return None
        if len(parts) != 3 or parts[0].upper() != "CONNECT":
            return self.refuse(405, "Only CONNECT is supported.")
        if parts[1].lower() not in self.server.destinations:
            return self.refuse(403, "Only %s can be reached through this proxy." % ", ".join(self.server.destinations))
        host, _, port = parts[1].rpartition(":")
        try:
            upstream = socket.create_connection((host, int(port)), timeout=CONNECT_TIMEOUT)
        except OSError as err:
            return self.refuse(502, "Could not reach %s: %s" % (parts[1], err))
        started = time.time()
        with upstream:
            self.wfile.write(b"HTTP/1.1 200 Connection established\r\n\r\n")
            self.wfile.flush()
            try:
                relay(self.connection, upstream)
            except OSError:
                pass
        log("%s -> %s (%.1fs)" % (self.client_address[0], parts[1], time.time() - started))


class Proxy(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    parser = argparse.ArgumentParser(prog="surf_proxy.py", description="A home relay for one agent's Surf requests.")
    parser.add_argument("--bind", default=None, help="Address to listen on (default: this machine's Tailscale address)")
    parser.add_argument("--port", type=int, default=PORT, help="Port to listen on (default %d)" % PORT)
    parser.add_argument("--allow-from", action="append", metavar="CIDR",
                        help="Client range allowed to connect (repeatable; default: Tailscale and this machine)")
    parser.add_argument("--dest", action="append", metavar="HOST:PORT",
                        help="Destination clients may reach (repeatable; default %s)" % DEST)
    args = parser.parse_args()

    bind = args.bind or tailscale_address()
    if not bind:
        sys.exit("No Tailscale address found. Start Tailscale, or pass --bind <address on your private network>.")
    try:
        clients = [ipaddress.ip_network(cidr, strict=False) for cidr in args.allow_from or PRIVATE_CLIENTS]
    except ValueError as err:
        sys.exit("--allow-from: %s" % err)
    if ipaddress.ip_address(bind).is_unspecified:
        log("WARNING: listening on every interface. Keep this port closed to the internet.")

    Proxy.address_family = socket.AF_INET6 if ":" in bind else socket.AF_INET
    try:
        server = Proxy((bind, args.port), Tunnel)
    except OSError as err:
        sys.exit("Could not listen on %s port %d: %s" % (bind, args.port, err))
    server.clients = clients
    server.destinations = [dest.lower() for dest in args.dest or [DEST]]
    log("listening on %s port %d; reaches %s; clients %s" % (
        bind, args.port, ", ".join(server.destinations), ", ".join(str(network) for network in clients)))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("stopped")


if __name__ == "__main__":
    main()
