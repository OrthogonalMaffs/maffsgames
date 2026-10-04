"""Does every game carry the teacher feedback line, mounted for itself, in Jon's exact words?

The line (schools/assets/teacher-invite.js, `MaffsInvite.mount(el, slug)`; contract 4 Oct 2026) sits under
each game's Start control and links to /feedback/?type=classroom&game=<slug>. It fails if:

  - a roster game (every numbered row of .claude/rules/game-roster.md; a withdrawn game, numbered "—", is a
    holding page and is skipped) does not load teacher-invite.js exactly once, does not make exactly one
    MaffsInvite.mount call, mounts with a slug other than its own directory name, or mounts onto an id that
    is not on the page exactly once;
  - the escape-room engine (escape-rooms/assets/engine.js) no longer renders the mount point and mounts it
    with the room's directory name, a live room (one that loads the engine) does not load teacher-invite.js,
    or a room's R.slug is not 'escape-' + its directory name (the engine derives the game value from it);
  - /leaderboards/ does not load it once and mount once with no game (null);
  - the link text in teacher-invite.js is not exactly TEXT below.

    python scripts/check-teacher-invite.py              # the check
    python scripts/check-teacher-invite.py --selftest   # each planted fault must fail; the clean copy passes
"""
import argparse, json, pathlib, re, shutil, sys, tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ".claude/rules/game-roster.md"
ASSET = "schools/assets/teacher-invite.js"
ENGINE = "escape-rooms/assets/engine.js"
TEXT = "Using this with a class? I'd love to hear how it went. — Jon"
ROW = re.compile("^\\|\\s*(\\d+)\\s*\\|[^|]*\\|\\s*`([a-z0-9-]+)`\\s*\\|")
INCLUDE = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/teacher-invite\.js"', re.I)
MOUNT = re.compile(r"MaffsInvite\.mount\(\s*document\.getElementById\('([^']+)'\)\s*,\s*(null|'([^']*)')\s*\)")
ANY_MOUNT = re.compile(r"MaffsInvite\.mount\(")
ENGINE_MOUNT = "window.MaffsInvite.mount(el('teacherInvite'), R.slug.replace(/^escape-/, ''))"
ENGINE_POINT = "'<p id=\"teacherInvite\"></p>'"
ROOM_SLUG = re.compile(r"slug:\s*'([^']+)'")


def roster(root):
    """Slugs of the roster's numbered (listed or unlisted) game rows."""
    out = []
    for line in (root / ROSTER).read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            out.append(m.group(2))
    return out


def check_page(rel, src, want_slug):
    """Problems with one page's include and mount. want_slug None means mount with null."""
    fails = []
    n = len(INCLUDE.findall(src))
    if n != 1:
        fails.append("%s: loads %s %d times (want once)" % (rel, ASSET, n))
    mounts = MOUNT.findall(src)
    if len(ANY_MOUNT.findall(src)) != 1 or len(mounts) != 1:
        fails.append("%s: %d MaffsInvite.mount calls in the expected form (want exactly one)" % (rel, len(ANY_MOUNT.findall(src))))
        return fails
    el_id, raw, slug = mounts[0]
    if want_slug is None and raw != "null":
        fails.append("%s: mounts with %s; this page names no game (want null)" % (rel, raw))
    if want_slug is not None and slug != want_slug:
        fails.append("%s: mounts with slug %r, but its directory is %r" % (rel, slug or raw, want_slug))
    ids = len(re.findall(r'\bid="%s"' % re.escape(el_id), src))
    if ids != 1:
        fails.append("%s: the mount point id=%r is on the page %d times (want once)" % (rel, el_id, ids))
    return fails


def check(root):
    fails = []
    js = (root / ASSET).read_text(encoding="utf-8")
    m = re.search(r'var TEXT = ("(?:[^"\\]|\\.)*");', js)
    text = json.loads(m.group(1)) if m else None
    if text != TEXT:
        fails.append("%s: link text is %r; it must be exactly %r" % (ASSET, text, TEXT))
    if "a.textContent = TEXT" not in js:
        fails.append("%s: the link no longer shows TEXT" % ASSET)

    slugs = roster(root)
    if not slugs:
        return fails + ["no game rows found in %s: the table changed shape, so this check is blind" % ROSTER]
    for slug in slugs:
        page = root / "games" / slug / "index.html"
        if not page.exists():
            fails.append("games/%s/: in the roster but has no index.html" % slug)
            continue
        fails += check_page("games/%s/index.html" % slug, page.read_text(encoding="utf-8"), slug)

    engine = (root / ENGINE).read_text(encoding="utf-8")
    if ENGINE_POINT not in engine:
        fails.append("%s: the start screen no longer renders the mount point %s" % (ENGINE, ENGINE_POINT))
    if engine.count(ENGINE_MOUNT) != 1:
        fails.append("%s: want exactly one %s" % (ENGINE, ENGINE_MOUNT))
    for room in sorted((root / "escape-rooms").iterdir()):
        page = room / "index.html"
        if not page.exists() or not (room / "room.js").exists():
            continue
        src = page.read_text(encoding="utf-8")
        if "assets/engine.js" not in src:
            continue  # a withdrawn room's holding page
        rel = "escape-rooms/%s/index.html" % room.name
        n = len(INCLUDE.findall(src))
        if n != 1:
            fails.append("%s: loads %s %d times (want once)" % (rel, ASSET, n))
        sm = ROOM_SLUG.search((room / "room.js").read_text(encoding="utf-8"))
        if not sm or sm.group(1) != "escape-" + room.name:
            fails.append("escape-rooms/%s/room.js: slug %r is not 'escape-%s', so the line would name the wrong room"
                         % (room.name, sm and sm.group(1), room.name))

    fails += check_page("leaderboards/index.html", (root / "leaderboards/index.html").read_text(encoding="utf-8"), None)
    return fails


def selftest():
    slugs = roster(BASE)
    g = slugs[0]
    rooms = [r.name for r in sorted((BASE / "escape-rooms").iterdir())
             if (r / "room.js").exists() and "assets/engine.js" in (r / "index.html").read_text(encoding="utf-8")]

    def scratch():
        d = pathlib.Path(tempfile.mkdtemp(prefix="invite-check-"))
        for rel in [ROSTER, ASSET, ENGINE, "leaderboards/index.html"] + \
                   ["games/%s/index.html" % s for s in slugs] + \
                   ["escape-rooms/%s/%s" % (r, f) for r in rooms for f in ("index.html", "room.js")]:
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(BASE / rel, d / rel)
        return d

    def edit(path, fn):
        s = path.read_text(encoding="utf-8")
        t = fn(s)
        assert t != s, "planted fault changed nothing in %s" % path
        path.write_text(t, encoding="utf-8")

    page = lambda d: d / "games" / g / "index.html"
    cases = [
        ("clean copy passes", lambda d: None, False),
        ("mount call removed", lambda d: edit(page(d), lambda s: MOUNT.sub("", s)), True),
        ("wrong slug", lambda d: edit(page(d), lambda s: s.replace("'%s')" % g, "'%s-x')" % g)), True),
        ("link text altered", lambda d: edit(d / ASSET, lambda s: s.replace("love to hear", "like to hear")), True),
        ("script include removed", lambda d: edit(page(d), lambda s: INCLUDE.sub("<script data-x", s)), True),
        ("mount point id removed", lambda d: edit(page(d), lambda s: s.replace('<p id="teacherInvite"></p>', "<p></p>")), True),
        ("escape-room engine mount removed", lambda d: edit(d / ENGINE, lambda s: s.replace(ENGINE_MOUNT, "0")), True),
        ("live room without the include", lambda d: edit(d / "escape-rooms" / rooms[0] / "index.html", lambda s: INCLUDE.sub("<script data-x", s)), True),
        ("leaderboards names a game", lambda d: edit(d / "leaderboards/index.html", lambda s: s.replace("'teacherInvite'), null)", "'teacherInvite'), 'x')")), True),
    ]
    bad = []
    for name, plant, should_fail in cases:
        d = scratch()
        try:
            plant(d)
            got = check(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = bool(got) == should_fail
        print("  %s  %-36s %s" % ("PASS" if ok else "FAIL", name, got[0] if got else "(no failures)"))
        if not ok:
            bad.append(name)
    print("selftest: %s (%d cases)" % ("FAILED: " + ", ".join(bad) if bad else "PASS", len(cases)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    if ap.parse_args().selftest:
        return selftest()
    fails = check(BASE)
    for f in fails:
        print("FAIL", f)
    n = len(roster(BASE))
    print("teacher line: %s (%d roster games, the escape-room engine, /leaderboards/)" % ("FAIL" if fails else "PASS", n))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
