#!/usr/bin/env python3
# ci-line: Stub server pins (serve-stubbed.py answers every page-read file a workflow commits to main with a fixed body, never the bot's latest; every path a workflow stages with git add is classified in BOT_WRITTEN and every entry is still staged; the opt-out serves the committed file; four planted faults caught; contract PINNED-LIVE-DATA) | --selftest
# ci-deps: .github/workflows/ scripts/bank_common.py
"""Serve the site locally with analytics.js replaced by a no-op stub, and the files bots rewrite pinned.

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

WHAT IT PINS, AND WHY (contract PINNED-LIVE-DATA, 27 Nov 2026)
--------------------------------------------------------------
Jon's play and the bots' commits must never change a check's colour. Some files
a page reads are rewritten on main by workflows with [skip ci] (Jon's daily
MaffsCards result; the nightly answer counts), and pages read them with
XMLHttpRequest, which the analytics stub does not touch. So a check rendering
those pages through this server showed whatever the bot last wrote: Jon's
result or not, a game's answer line or not as its count crossed 1,000 or the
file went 7 days stale.

BOT_WRITTEN below lists every path any .github/workflows/*.yml stages with
`git add`. Each is either PINNED (this server answers that path, with or without
a query string, with a fixed "shows nothing" body, whatever the file on disk
says) or NOT PINNED with the reason. The guard (--check, and --selftest in CI)
fails when a workflow stages a path the table does not list, or the table lists
a path no workflow stages any more, so the next bot-written file cannot slip by.

The owner checks still cover each file's shown states with their own Playwright
routes, which answer before this server: verify-maffscards.py (daily.json),
check-answer-count.py and check-ugh-stats.py (answer-counts.json).

THE OPT-OUT
-----------
A check that must read the committed files through the server (check-ugh-stats.py,
whose REAL unit holds the /ugh-stats/ pages to the repo's own JSON files) starts
it with --committed, or with the environment variable MAFFS_STUB_COMMITTED=1;
bank_common.start_stub_server(committed=True) passes the flag. Nothing else uses
it: a check that needs the opt-out to pass is reported, not opted out.

USAGE
-----
    python scripts/serve-stubbed.py                  # serves on 127.0.0.1:8765
    python scripts/serve-stubbed.py 9000             # or pick a port
    python scripts/serve-stubbed.py 9000 --committed # the committed bot-written files, unpinned
    python scripts/serve-stubbed.py --check          # the guard and the pins, on the repo's workflows
    python scripts/serve-stubbed.py --selftest       # --check, then four planted faults must each fail

Then open http://127.0.0.1:8765/ , or a game directly:
    http://127.0.0.1:8765/games/trig-wars/

Ctrl-C to stop. Node is not installed on the Windows machine, so Python is the
way to serve this repo there.
"""
import datetime as dt
import functools
import glob
import http.server
import json
import os
import posixpath
import re
import shutil
import socket
import sys
import tempfile
import threading
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMITTED_ENV = "MAFFS_STUB_COMMITTED"

STUB = (
    b"// STUBBED FOR LOCAL RENDER TESTING - no network writes\n"
    b"window.mfg = function(){ console.log('[stub] mfg', arguments); };\n"
    b"window.fetch = function(){ console.log('[stub] fetch blocked', arguments[0]);"
    b" return Promise.reject(new Error('stubbed')); };\n"
    b"if (navigator.sendBeacon) navigator.sendBeacon = function(u){"
    b" console.log('[stub] sendBeacon blocked', u); return true; };\n"
)


def _now_iso():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def daily_not_played():
    """games/maffscards/daily.json as the workflow leaves it before Jon plays: the page shows "not played"."""
    return {"date": None, "result": None, "rounds": None, "line": None}


def counts_nothing():
    """schools/assets/answer-counts.json read as fresh (as_of now, never past answer-count.js's 7 days) with no game and
    a total of 0: under GAME_MIN and TOTAL_MIN, so no game page and not the homepage shows a line."""
    return {"as_of": _now_iso(), "since": "2026-09-01", "total": 0, "games": {}}


# Every repo path any workflow stages with `git add`. ("pinned", body) or ("not pinned", reason).
BOT_WRITTEN = {
    "games/maffscards/daily.json": ("pinned", daily_not_played),
    "schools/assets/answer-counts.json": ("pinned", counts_nothing),
    "schools/assets/ugh-stats.json": (
        "not pinned",
        "no valid body shows nothing: ugh-stats.js SHAPE.stats needs a daily row and 24 hours a side, and "
        "/ugh-stats/charts/ draws them with a date; held for Jon (PINNED-LIVE-DATA STOP IF). Read only by the "
        "/ugh-stats/ pages, whose owner check is check-ugh-stats.py"),
    "docs/audits/REGISTER.md": ("not pinned", "never read by a page"),
    "docs/handover/home.md": ("not pinned", "never read by a page"),
    "docs/handover/cloud.md": ("not pinned", "never read by a page"),
    "docs/history/handover-home-archive.md": ("not pinned", "never read by a page"),
    "docs/history/handover-cloud-archive.md": ("not pinned", "never read by a page"),
    "scripts/ci-timings.json": ("not pinned", "never read by a page (read by ci-groups.py)"),
    "scripts/ci-pack.json": ("not pinned", "never read by a page (read by ci-groups.py)"),
    "scripts/ci-timings-regions.json": ("not pinned", "never read by a page (read by ci-groups.py)"),
    "scripts/ci-warn-list.json": ("not pinned", "never read by a page (read by the Gate's scripts)"),
}


def repo_path(request_path):
    """The repo-relative path a request names, query and fragment dropped, or None outside the root."""
    p = urllib.parse.unquote(urllib.parse.urlsplit(request_path).path)
    p = posixpath.normpath("/" + p.lstrip("/"))
    return p.lstrip("/")


def committed_from_env():
    return os.environ.get(COMMITTED_ENV, "").strip().lower() in ("1", "true", "yes")


class Handler(http.server.SimpleHTTPRequestHandler):
    table = BOT_WRITTEN
    committed = False

    def _send(self, body, kind):
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0].endswith("analytics.js"):
            self._send(STUB, "application/javascript")
            return
        entry = self.table.get(repo_path(self.path))
        if entry and entry[0] == "pinned" and not self.committed:
            self._send(json.dumps(entry[1]()).encode("utf-8"), "application/json")
            return
        super().do_GET()

    def log_message(self, *args):
        pass


class Server(http.server.ThreadingHTTPServer):
    """The listen queue is the fix for LOCAL-FLAKES (18 Oct 2026). socketserver's default is 5; a page load opens
    up to six connections at once and the checks load several pages at once, so on a loaded Windows machine the
    accept loop falls behind, the queue fills and Windows REFUSES the next connection (net::ERR_CONNECTION_REFUSED).
    A script or the page itself then never arrives and the check fails on an error the game never had. A queue
    deep enough for every page a check can have in flight leaves nothing to refuse."""
    request_queue_size = 128


# ------------------------------------------------------------------------------------------------ the guard
GIT_ADD = re.compile(r"\bgit\s+add\s+([^;&|\n]*)")


def staged_paths(workflows):
    """{workflow name: text} -> {path: [where]} for every path a non-comment line stages with git add."""
    out = {}
    for name, text in workflows.items():
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            for m in GIT_ADD.finditer(line):
                for tok in m.group(1).split():
                    tok = tok.strip("'\"")
                    if tok and not tok.startswith("-"):
                        out.setdefault(tok, []).append("%s:%d" % (name, n))
    return out


def repo_workflows():
    return {os.path.relpath(p, ROOT).replace(os.sep, "/"): open(p, encoding="utf-8").read()
            for p in sorted(glob.glob(os.path.join(ROOT, ".github", "workflows", "*.yml")))}


def guard(table, workflows):
    """Faults: a staged path the table does not list, a listed path nothing stages, an entry of neither kind."""
    faults = []
    staged = staged_paths(workflows)
    for path, where in sorted(staged.items()):
        if path not in table:
            faults.append("%s stages %s, which BOT_WRITTEN does not list (pin it or give the reason)" % (", ".join(where), path))
    for path, entry in sorted(table.items()):
        if path not in staged:
            faults.append("BOT_WRITTEN lists %s, which no workflow stages any more" % path)
        kind = entry[0] if isinstance(entry, tuple) and len(entry) == 2 else None
        if kind == "pinned" and not callable(entry[1]):
            faults.append("%s is pinned with no body" % path)
        elif kind == "not pinned" and not (isinstance(entry[1], str) and entry[1].strip()):
            faults.append("%s is not pinned and gives no reason" % path)
        elif kind not in ("pinned", "not pinned"):
            faults.append("%s is neither pinned nor not pinned: %r" % (path, entry))
    return faults


# Each pinned body must be its file's "shows nothing" state, valid for its reader.
def _daily_ok(o):
    return o == daily_not_played()


def _counts_ok(o):
    if not isinstance(o, dict) or set(o) != {"as_of", "since", "total", "games"}:
        return False
    try:
        t = dt.datetime.strptime(o["as_of"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except (TypeError, ValueError):
        return False
    age = (dt.datetime.now(dt.timezone.utc) - t).total_seconds()
    # The time of serving: answer-count.js ignores a file over 7 days old, so a pin must never be one.
    return -60 <= age <= 300 and o["since"] == "2026-09-01" and o["total"] == 0 and o["games"] == {}


BODY_OK = {"games/maffscards/daily.json": _daily_ok, "schools/assets/answer-counts.json": _counts_ok}

# What a bot might have written on the day a check runs: Jon played and won; a busy, fresh counts file.
LIVE = {
    "games/maffscards/daily.json": {"date": "2026-11-27", "result": "won", "rounds": 15, "line": "Beat that."},
    "schools/assets/answer-counts.json": {"as_of": "2026-11-27T05:00:00Z", "since": "2026-09-01", "total": 50000,
                                          "games": {"maffscards": 4000, "six-sevens-bruv": 9000}},
    "schools/assets/ugh-stats.json": {"as_of": "2026-11-27T05:00:00Z", "marker": "on disk"},
}


serving_root = [None]      # the temporary root serve_test is serving (the "file on disk" plant reads it)


def serve_test(table):
    """Serve a temporary root whose bot-written files hold LIVE data and check every pin holds over it, with and without
    a query string, that the opt-out serves the file on disk, and that an ordinary file is served from disk."""
    faults = []
    tmp = tempfile.mkdtemp(prefix="stub-pins-")
    serving_root[0] = tmp
    try:
        for path in table:
            full = os.path.join(tmp, *path.split("/"))
            os.makedirs(os.path.dirname(full), exist_ok=True)
            body = LIVE.get(path, {"marker": "on disk"}) if path.endswith(".json") else "on disk\n"
            with open(full, "w", encoding="utf-8") as f:
                f.write(json.dumps(body) if path.endswith(".json") else body)
        with open(os.path.join(tmp, "plain.txt"), "w", encoding="utf-8") as f:
            f.write("plain")
        for committed in (False, True):
            handler = type("H", (Handler,), {"table": table, "committed": committed})
            srv = Server(("127.0.0.1", 0), functools.partial(handler, directory=tmp))
            srv.daemon_threads = True
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            base = "http://127.0.0.1:%d/" % srv.server_address[1]
            try:
                def get(rel):
                    with urllib.request.urlopen(base + rel, timeout=5) as r:
                        return r.read().decode("utf-8")
                if get("plain.txt") != "plain":
                    faults.append("an ordinary file is not served from disk")
                for path, entry in sorted(table.items()):
                    if entry[0] != "pinned":
                        continue
                    on_disk = open(os.path.join(tmp, *path.split("/")), encoding="utf-8").read()
                    for rel in (path, path + "?t=1764230400000", "./" + path + "?cb=verify"):
                        got = get(rel)
                        if committed:
                            if got != on_disk:
                                faults.append("--committed: /%s is not the file on disk" % rel)
                            continue
                        if got == on_disk:
                            faults.append("/%s answers with the file on disk, not its pin" % rel)
                        try:
                            obj = json.loads(got)
                        except ValueError:
                            faults.append("/%s's pin is not JSON" % rel)
                            continue
                        ok = BODY_OK.get(path)
                        if ok is None:
                            faults.append("%s is pinned with no rule for a 'shows nothing' body (add it to BODY_OK)" % path)
                        elif not ok(obj):
                            faults.append("/%s's pin is not its 'shows nothing' body: %s" % (rel, got[:160]))
            finally:
                srv.shutdown()
                srv.server_close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return faults


def check(table=None, workflows=None):
    table = BOT_WRITTEN if table is None else table
    workflows = repo_workflows() if workflows is None else workflows
    return guard(table, workflows) + serve_test(table)


def selftest():
    bad = []
    real = check()
    print("check: %s" % ("PASS" if not real else "FAILED: " + "; ".join(real)))
    if real:
        bad.append("the real check fails")
    wf = repo_workflows()
    extra = dict(wf)
    extra["planted.yml"] = "      - run: |\n          git add schools/assets/new-bot-file.json\n"
    no_daily = {k: v for k, v in BOT_WRITTEN.items() if k != "games/maffscards/daily.json"}
    disk = dict(BOT_WRITTEN)
    disk["games/maffscards/daily.json"] = ("pinned", lambda: json.load(open(
        os.path.join(serving_root[0], "games", "maffscards", "daily.json"), encoding="utf-8")))
    old = dict(BOT_WRITTEN)
    eight = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=8)).strftime("%Y-%m-%dT%H:%M:%SZ")
    old["schools/assets/answer-counts.json"] = ("pinned", lambda: dict(counts_nothing(), as_of=eight))
    plants = [("a workflow line adding an unlisted path", lambda: guard(BOT_WRITTEN, extra), "new-bot-file.json"),
              ("daily.json removed from the table", lambda: guard(no_daily, wf), "games/maffscards/daily.json"),
              ("a pin answering with the file on disk", lambda: serve_test(disk), "file on disk"),
              ("answer-counts.json's pin with an as_of 8 days old", lambda: serve_test(old), "answer-counts.json's pin")]
    for label, run, want in plants:
        faults = run()
        caught = any(want in f for f in faults)
        print("plant %-50s %s" % (label + ":", "caught" if caught else "MISSED (%s)" % ("; ".join(faults) or "no fault")))
        if not caught:
            bad.append(label)
    print("selftest: %s (%d plants)" % ("FAILED: " + "; ".join(bad) if bad else "PASS", len(plants)))
    return 1 if bad else 0


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    if "--check" in args:
        faults = check()
        for f in faults:
            print("FAIL: " + f)
        print("stub server pins: %s (%d bot-written paths)" % ("FAILED" if faults else "PASS", len(BOT_WRITTEN)))
        return 1 if faults else 0
    committed = "--committed" in args or committed_from_env()
    rest = [a for a in args if a != "--committed"]
    port = int(rest[0]) if rest else 8765
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
    Handler.committed = committed
    print("Serving %s on http://127.0.0.1:%d/  (analytics stubbed; bot-written files %s)"
          % (ROOT, port, "as committed" if committed else "pinned"))
    print("Ctrl-C to stop.")
    try:
        # Threading matters: a single-threaded HTTPServer wedges completely if
        # one keep-alive connection is left hanging, which a closed browser tab
        # does routinely. ThreadingHTTPServer keeps serving.
        srv = Server(("127.0.0.1", port), Handler)
        srv.daemon_threads = True
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    sys.exit(main())
