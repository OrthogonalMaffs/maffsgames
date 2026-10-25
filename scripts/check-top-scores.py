#!/usr/bin/env python3
"""Does every game's "Top scores" panel come from score-history.js, in British dates, with no score of 0?

Contract TOP-SCORES (Jon, 25 Oct 2026). Eleven games each kept their own top-five list in localStorage
(pf_scores, dd_scores_<level> ...), dated with a bare toLocaleDateString() (10/25/2026 in a US-set browser) and saved
after every game, a 0 included (most also saved one on every page load). They now draw the panel with
MaffsScoreHistory.renderTop(el, slug, level, 5): score-history.js's record() keeps each game+level's best five, all
time, in a key of its own (mfg_top_v1::<slug>::<level>), never a score of 0 or less, a tie keeping the earlier score;
the last-10 history (mfg_hist_v1::) that the leaderboards hub reads is unchanged. Old per-game lists are no longer read.

    python scripts/check-top-scores.py              # every page under games/ (stdlib; a site-wide check)
    python scripts/check-top-scores.py --selftest   # each planted fault must fail

Static (this script), on every .html and .js file under games/:
  - no toLocaleDateString(), toLocaleTimeString() or toLocaleString() whose first argument is not 'en-GB', and no
    Intl.DateTimeFormat or Intl.NumberFormat without it (a date or number formatted in the browser's own locale);
  - no string literal naming a *_scores key: a game keeps no top-scores list of its own (OWN_LIST below are the
    games that still do, each with why it is not migrated: reported every run, never failed; the list may only shrink);
  - each PANEL game loads score-history.js and calls MaffsScoreHistory.renderTop( exactly once, into #lbList.
In Chromium (scripts/test-top-scores.py, a content line; locale en-US, the clock set to 25 Oct 2026, firebase-leaderboard.js blocked so window.MaffsLeaderboard
is undefined), each PANEL game is opened and its own end-of-game function run once a session for the scores
30, 0, 50, 10, 40, 20, 10, 5 in turn (score set, MaffsLock.newSession(), the function called):
  - every score is in its last-10 history (a game records whether or not Firebase loads);
  - after each game, its top key and the panel hold the best five scores so far above 0, highest first (after 30
    and 0: 30 alone; at the end 50, 40, 30, 20, 10), the 10 kept being the first one (a tie keeps the earlier);
  - #lbList ends with five rows, #1 to #5, those scores, each dated 25/10/2026.
Plants: here (--selftest), a bare toLocaleDateString() in a game and a game's own scores list restored; in
test-top-scores.py --selftest, on percentage-flip in Chromium: a zero stored and shown; a sixth-best score displacing the top five (the newest five
kept); a tie keeping the later score; the renderer's date in the browser's locale; the game's record() back inside its
Firebase check. Each must fail.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

ASSET = "schools/assets/score-history.js"
# The panel games and the end-of-game function each defines (MaffsLock.finishOnce): contract TOP-SCORES.
PANEL = {
    "differentiation-duel": "endGame", "percentage-flip": "endGame", "trig-worms": "endGame", "suvat": "endGame",
    "fraction-equivalence": "endGame", "modular-battle": "finishGame", "prime-factorisation": "endGame",
    "integration-duel": "endGame", "quadratic-factoriser": "finishGame", "factor-race": "endGame",
    "index-laws": "finishGame",
}
# Games that still keep a top-scores list of their own: not in the contract's eleven, and each panel shows something
# score-history.js does not record, so the shared renderer would lose it (the contract's STOP IF). For Jon to rule.
OWN_LIST = {
    "log-laws": "Laws and Solve keep separate lists (ll_scores, ll_scores_solve); score-history.js has no mode, and "
                "Solve records no history while LEADERBOARD_MODE_READY is false",
    "fermi-lab": "each row shows the session's question count, \"(10Q)\" (fermi_scores_<tier>); score-history.js "
                 "records no question count",
}

LOCALE = re.compile(r"\.toLocale(?:Date|Time)?String\(([^)]*)\)|\bIntl\.(?:DateTimeFormat|NumberFormat)\(([^)]*)\)")
GB = re.compile(r"""^\s*(['"])en-GB\1""")
SCORES_KEY = re.compile(r"""(['"`])[A-Za-z0-9]*_scores[A-Za-z0-9_]*\1""")
INCLUDE = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/score-history\.js"')
RENDER = re.compile(r"MaffsScoreHistory\.renderTop\(\s*document\.getElementById\('lbList'\)\s*,")


def game_files(root):
    games = os.path.join(root, "games")
    for slug in sorted(os.listdir(games)):
        d = os.path.join(games, slug)
        if not os.path.isdir(d):
            continue
        for dirpath, _, files in os.walk(d):
            for f in sorted(files):
                if f.endswith((".html", ".js")):
                    p = os.path.join(dirpath, f)
                    yield slug, os.path.relpath(p, root).replace(os.sep, "/"), p


def static_faults(root=ROOT, texts=None):
    """texts: {rel path: text} overriding files on disk (the plants)."""
    texts = texts or {}
    faults, own = [], set()
    for slug, rel, p in game_files(root):
        src = texts.get(rel) or open(p, encoding="utf-8").read()
        for m in LOCALE.finditer(src):
            args = m.group(1) if m.group(1) is not None else m.group(2)
            if not GB.match(args):
                line = src.count("\n", 0, m.start()) + 1
                faults.append("%s:%d: %s without 'en-GB' (the browser's own locale)" % (rel, line, m.group(0)[:60]))
        keys = sorted(set(k.group(0) for k in SCORES_KEY.finditer(src)))
        if keys:
            if slug in OWN_LIST:
                own.add(slug)
            else:
                faults.append("%s: keeps its own top-scores list (%s); draw it with MaffsScoreHistory.renderTop" % (rel, ", ".join(keys)))
        if slug in PANEL and rel.endswith("/index.html"):
            if len(INCLUDE.findall(src)) != 1:
                faults.append("%s: must load score-history.js exactly once" % rel)
            if len(RENDER.findall(src)) != 1:
                faults.append("%s: must call MaffsScoreHistory.renderTop(document.getElementById('lbList'), ...) exactly once" % rel)
    for slug in OWN_LIST:
        if slug not in own:
            faults.append("%s: on OWN_LIST but keeps no list of its own any more: take it off" % slug)
        if slug in PANEL:
            faults.append("%s: on both PANEL and OWN_LIST" % slug)
    return faults


def _sub(src, old, new, what):
    assert src.count(old) == 1, "plant: %s not found exactly once" % what
    return src.replace(old, new)


def plants():
    pf_rel = "games/percentage-flip/index.html"
    pf = open(os.path.join(ROOT, pf_rel), encoding="utf-8").read()
    bare_game = _sub(pf, "function getBest() {", "var _d = new Date().toLocaleDateString();\nfunction getBest() {", "a bare date")
    own = _sub(pf, "function getBest() {", "localStorage.setItem('pf_scores', '[]');\nfunction getBest() {", "an own list")
    return [("a bare toLocaleDateString() in a game", {pf_rel: bare_game}),
            ("a game's own scores list restored", {pf_rel: own})]


def selftest():
    ok = True
    for name, texts in plants():
        f = static_faults(ROOT, texts)
        print("plant (%s): %s" % (name, ("CAUGHT: " + f[0][:160]) if f else "MISSED"))
        ok = ok and bool(f)
    print("selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    f = static_faults()
    print("Top scores, static (TOP-SCORES): every page under games/; %d panel games" % len(PANEL))
    for s, why in OWN_LIST.items():
        print("  note  %s keeps its own list, not migrated: %s" % (s, why))
    print("  %s  dates and numbers in en-GB, no own *_scores list, the panel games on renderTop%s"
          % ("FAIL" if f else "ok  ", (":\n    " + "\n    ".join(f)) if f else ""))
    print("PASS" if not f else "FAIL")
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
