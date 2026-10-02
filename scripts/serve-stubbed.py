#!/usr/bin/env python3
"""Serve the site locally with analytics.js replaced by a no-op stub.

WHY THIS EXISTS
---------------
Every page on this site loads `schools/assets/analytics.js`, which posts to the
live Apps Script endpoint and therefore into the production "MaffsGames Events"
sheet. Opening a real game page against the live endpoint to check a layout
writes junk rows into the data Jon actually makes decisions from. That happened
once (2026-08-26, ~5 rows).

This server rewrites the response for analytics.js so `mfg()`, `fetch` and
`sendBeacon` all become no-ops that log to the console instead. Nothing leaves
the machine, and index.html and the game files stay untouched, so you are
render-testing exactly the bytes that would ship.

USAGE
-----
    python scripts/serve-stubbed.py            # serves on 127.0.0.1:8765
    python scripts/serve-stubbed.py 9000       # or pick a port

Then open http://127.0.0.1:8765/ , or a game directly:
    http://127.0.0.1:8765/games/trig-wars/

Ctrl-C to stop. Node is not installed on the Windows machine, so Python is the
way to serve this repo there.
"""
import http.server
import os
import socket
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STUB = (
    b"// STUBBED FOR LOCAL RENDER TESTING - no network writes\n"
    b"window.mfg = function(){ console.log('[stub] mfg', arguments); };\n"
    b"window.fetch = function(){ console.log('[stub] fetch blocked', arguments[0]);"
    b" return Promise.reject(new Error('stubbed')); };\n"
    b"if (navigator.sendBeacon) navigator.sendBeacon = function(u){"
    b" console.log('[stub] sendBeacon blocked', u); return true; };\n"
)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0].endswith("analytics.js"):
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Content-Length", str(len(STUB)))
            self.end_headers()
            self.wfile.write(STUB)
            return
        super().do_GET()

    def log_message(self, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    os.chdir(ROOT)
    # Fail loudly rather than silently fighting an already-bound port.
    probe = socket.socket()
    try:
        probe.bind(("127.0.0.1", port))
    except OSError:
        print("Port %d is already in use - another server is running." % port)
        print("Either use it, or pass a different port: serve-stubbed.py %d" % (port + 1))
        return
    finally:
        probe.close()
    print("Serving %s on http://127.0.0.1:%d/  (analytics stubbed)" % (ROOT, port))
    print("Ctrl-C to stop.")
    try:
        # Threading matters: a single-threaded HTTPServer wedges completely if
        # one keep-alive connection is left hanging, which a closed browser tab
        # does routinely. ThreadingHTTPServer keeps serving.
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
        srv.daemon_threads = True
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
