# ci-line: Escape rooms (every set of every live room re-checked by escape_set_checks.py: one solution, answer and misconception settable and different, answer not in its clue, off the end of the travel, broken sets planted; every lock against the audited bank and variants.json; tokens; VALID draws; maxDigits answers settable; difficulty stars from lock grades matched on every hub and front-page card and the star key, three faults planted) |
# ci-deps: escape-rooms/ index.html
"""Check the built escape rooms against the audited lock bank.

Run after any edit to escape-rooms/*/room.js. It catches:

  * a lock id that is not in the audited bank
  * variant 0 disagreeing with the bank's ANSWER or MISCONCEPTION — the first
    variant of every lock is the audited one and must stay that way
  * room.js drifting from variants.json, which is the verified source
  * a {{token}} in the prose that some variant cannot fill, which would put
    literal braces in front of a class
  * a room with fewer than two empty objects
  * a room with fewer than 20 VALID draws — see "Cross-lock collisions" below
  * difficulty (contract ESCAPE-DIFFICULTY, 10 Oct 2026; Jon's scheme of 9 Oct): a lock in a
    live room with no `grade: N` (1-9); a card on the hub or the front page whose data-stars
    or label disagrees with the rating derived from its room's hardest lock (★ Warm-up 1-3,
    ★★ Core 4-5, ★★★ Challenge 6-9); a live room with no card on either page; bands in
    escape-rooms/assets/rating.js that differ from BANDS here; hub cards out of rating order
    (the hub says "Ordered easiest to hardest"). Two faults are planted on every run (Rugby
    Mud's hub card saying ★; a lock's grade removed) and must each be caught.
  * the star key (contract STAR-KEY, 10 Oct 2026): the one line on the hub and on the front
    page that says what the stars mean must name exactly the bands above, with the stars
    hidden from screen readers and read as "one star, Warm-up, grades 1 to 3" and so on, and
    must not say who a room suits. A key saying "Core, grades 4–6" is planted and must fail.
  * on a `maxDigits: N` keypad ("up to N digits, Set to submit", KEYPAD-VARIABLE),
    an answer or misconception the keypad cannot take: it must be a whole
    number of 1 to N digits with no leading zero, so a four-digit misconception
    needs maxDigits 4 or more. Fixed-length (`digits: N`) keypads are not
    checked here, as before.
  * every set of every live room's locks, re-checked (contract ESCAPE-SET-CHECKS,
    11 Oct 2026) by scripts/escape_set_checks.py, the same module the generator
    admits sets with: exactly one setting solves it, the answer and misconception
    are settable and differ, the clue does not print the answer, the answer is off
    the end of a dial's travel. A failure names the room, lock, set and check; a
    live lock with no entry in the module fails too. The run prints each live
    room's verified-set count and the total. Ten broken sets from
    scripts/fixtures/escape-broken-sets.json are planted through the same code on
    every run: each must fail, and its good original must pass.

Cross-lock collisions. Each lock's library is verified on its own, but a room
serves one variant per lock together, and those can collide. A draw is VALID
when, across its locks:
  a. no clue figure is printed in the clues of more than one lock
  b. no lock's answer is printed in another lock's clues
  c. no lock's answer equals another lock's misconception
  d. no two locks share an answer
A clue figure is any number the student reads in a clue: the resolved
{{key.token}} values and any numeral written into the clue string itself. A
clue belongs to the lock whose tokens it uses. Rules (a) and (b) ignore figures
of 2 or less — coefficients and numerators, not clues anyone could mistake for
another lock's; (c) and (d) apply at every size. engine.js pickVariants()
applies the same rules and serves only VALID draws, so the two must be changed
together.

The run reports every room's VALID count. Fewer than 20 fails, live or
withdrawn. An invalid variant-0 draw is a warning only — the engine never
serves it — and a withdrawn (noindex) room only ever warns about it.

Missing pictures are reported separately and do not fail the run. A room is
built and playable before its art exists: until then its room.js has no `art`
field, the engine requests no scene, fail or win picture (contract ART-PENDING,
10 Oct 2026), and this check lists it as "art pending". A room that names its art
but is missing a file is listed too, and check-site's tier 1 fails its page on
the 404. What is still to draw is tracked in docs/escape-room-image-prompts.md,
not by this exit code.
"""
import itertools, json, re, pathlib, sys

from escape_set_checks import NO_CHECK, check, covered

sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # the stars, on a cp1252 Windows console

BASE = pathlib.Path(__file__).resolve().parent.parent
ROOMS = BASE / "escape-rooms"
ART = BASE / "docs" / "art"
BROKEN_SETS = BASE / "scripts" / "fixtures" / "escape-broken-sets.json"

problems = []
warnings = []
pending_art = []
collision_report = []


def nums(s):
    return [float(x.rstrip(".")) for x in re.findall(r"-?\d+\.?\d*", str(s))]


# ---- cross-lock collisions (kept in step with pickVariants() in engine.js) ----
MIN_VALID = 20
EXEMPT = 2          # rules (a) and (b) ignore figures this small


def clue_strings(js):
    """The object clue strings, as (text, key of the lock whose tokens it uses)."""
    body = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    objs = body.split("objects: [", 1)[1].split("\n  locks: [", 1)[0]
    lit = r"'(?:[^'\\]|\\.)*'"
    out = []
    for m in re.finditer(r"clue:\s*((?:" + lit + r"\s*\+?\s*)+)", objs):
        text = "".join(s[1:-1] for s in re.findall(lit, m.group(1))).replace("\\'", "'")
        owners = set(re.findall(r"\{\{([\w-]+)\.", text))
        out.append((text, next(iter(owners)) if len(owners) == 1 else None))
    return out


def figures(text, key, var):
    """Every number a student reads in one clue, with this variant filled in."""
    text = re.sub(r"\{\{" + re.escape(key) + r"\.([\w-]+)\}\}",
                  lambda m: str(var.get(m.group(1), m.group(0))), text)
    text = re.sub(r"<[^>]*>|&[#\w]+;", " ", text)
    return {float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)}


def keypad_settable(v, max_digits):
    """A maxDigits keypad takes a whole number of 1 to N digits, no leading zero."""
    return (isinstance(v, (int, float)) and not isinstance(v, bool) and v == int(v)
            and 0 <= v and len(str(int(v))) <= max_digits)


def flat(x):
    if x is None:
        return set()
    return {float(v) for v in (x if isinstance(x, list) else [x])}


def draw_is_valid(draw, clues):
    """draw: [(key, variant)] one per lock. clues: from clue_strings()."""
    clue = [set() for _ in draw]
    for text, owner in clues:
        for i, (key, var) in enumerate(draw):
            if key == owner:
                clue[i] |= {f for f in figures(text, key, var) if f > EXEMPT}
    ans = [flat(v["answer"]) for _, v in draw]
    miss = [flat(v.get("miss")) for _, v in draw]
    for i in range(len(draw)):
        for j in range(len(draw)):
            if i == j:
                continue
            if i < j and (clue[i] & clue[j] or ans[i] & ans[j]):
                return False
            if ans[i] & clue[j] or ans[i] & miss[j]:
                return False
    return True


# ---- the audited bank ------------------------------------------------------
bank = {}
# Every batch file in docs/, found by pattern so a new batch needs no edit here.
# Sorted by batch number, so batch 10 follows batch 9 rather than batch 1.
BATCHES = sorted((BASE / "docs").glob("lock-bank-batch*.txt"),
                 key=lambda p: int(re.search(r"batch(\d+)", p.name).group(1)))
for f in BATCHES:
    txt = f.read_text(encoding="utf-8", errors="replace")
    for block in re.split(r"\n(?=ID:)", txt):
        m = re.match(r"ID:\s*(\S+)", block)
        if not m:
            continue
        e = {}
        for key in ("ANSWER", "MISCONCEPTION"):
            mm = re.search(key + r":\s*(.+)", block)
            if mm:
                e[key] = mm.group(1).strip()
        bank[m.group(1)] = e

verified = json.loads((ROOMS / "variants.json").read_text(encoding="utf-8"))

# ---- each room -------------------------------------------------------------
locks_seen = 0
for room_dir in sorted(p for p in ROOMS.iterdir() if p.is_dir() and p.name != "assets"):
    slug = room_dir.name
    js = (room_dir / "room.js").read_text(encoding="utf-8")

    # images: the room's own `art` is its top-level field; any other art: is a lock's
    room_art = re.search(r"^  art:\s*'([^']+)'", js, re.M)
    lock_art = [a for a in re.findall(r"art:\s*'([^']+)'", js) if not room_art or a != room_art.group(1)]
    if room_art:
        wanted = [room_art.group(1) + "-scene", room_art.group(1) + "-fail"] + lock_art
        # a room shows a victory picture only once it has a winAlt to describe it,
        # so the two arrive together or not at all
        if re.search(r"^  winAlt:", js, re.M):
            wanted.append(room_art.group(1) + "-win")
    else:
        pending_art.append(f"{slug}: art pending (no `art` field: no scene, fail or win picture is requested)")
        wanted = lock_art
    for name in wanted:
        if not (ART / (name + ".webp")).exists():
            pending_art.append(f"{slug}: {name}.webp not drawn yet")

    if len(re.findall(r"clue: null", js)) < 2:
        problems.append(f"{slug}: fewer than two empty objects")

    # locks, with their injected libraries
    lock_ids = re.findall(r"\n      id: '([^']+)'", js)
    keys = re.findall(r"\n      key: '([^']+)'", js)
    if len(lock_ids) != len(keys):
        problems.append(f"{slug}: every lock needs a `key` for its tokens")
        continue

    token_values = {}
    for lid, key in zip(lock_ids, keys):
        locks_seen += 1
        if lid not in bank:
            problems.append(f"{slug}: lock '{lid}' is not in the audited bank")
            continue
        if lid not in verified:
            problems.append(f"{slug}/{lid}: no verified library in variants.json")
            continue

        # the library in room.js must be exactly the verified one
        block = js.split("id: '" + lid + "'", 1)[1]
        start = block.index("variants: [")
        depth, end = 0, block.index("[", start)
        for pos in range(end, len(block)):
            if block[pos] == "[":
                depth += 1
            elif block[pos] == "]":
                depth -= 1
                if depth == 0:
                    end = pos
                    break
        try:
            in_file = json.loads(block[block.index("[", start):end + 1])
        except ValueError as exc:
            problems.append(f"{slug}/{lid}: variants are not valid JSON ({exc})")
            continue
        if in_file != verified[lid]:
            problems.append(f"{slug}/{lid}: room.js has drifted from variants.json "
                            f"— re-run scripts/gen-escape-variants.py")
            continue
        if not in_file:
            problems.append(f"{slug}/{lid}: empty variant library")
            continue

        ins_line = re.search(r"instrument:\s*\{[^\n]*\}", block)
        md = re.search(r"\bmaxDigits:\s*(\d+)", ins_line.group(0)) if ins_line else None
        if md:
            n = int(md.group(1))
            for i, var in enumerate(in_file):
                for what in ("answer", "miss"):
                    if what in var and var[what] is not None and not keypad_settable(var[what], n):
                        problems.append(f"{slug}/{lid}: variant {i} {what} {var[what]} cannot be "
                                        f"set on a keypad of up to {n} digits")

        # variant 0 is the audited lock and must match the bank
        b = bank[lid]
        if nums(in_file[0]["answer"]) != nums(b.get("ANSWER", "")):
            problems.append(f"{slug}/{lid}: variant 0 answer {in_file[0]['answer']} "
                            f"but the bank says {b.get('ANSWER')}")
        if "MISCONCEPTION" in b and in_file[0].get("miss") is not None:
            got = nums(in_file[0]["miss"])
            want = nums(b["MISCONCEPTION"])[:len(got)]
            if got != want:
                problems.append(f"{slug}/{lid}: variant 0 misconception {got} "
                                f"but the bank says {want}")

        for i, var in enumerate(in_file):
            for tok, val in var.items():
                token_values.setdefault(f"{key}.{tok}", set()).add(i)

    # every {{token}} the prose uses must be fillable by every variant.
    # Block comments are stripped first — the file header explains the syntax
    # using {{key.token}} as an example, which is not a real token.
    prose = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    used = set(re.findall(r"\{\{([\w.-]+)\}\}", prose))
    for tok in sorted(used):
        if tok not in token_values:
            problems.append(f"{slug}: {{{{{tok}}}}} is used but no variant supplies it")
            continue
        lid_key = tok.split(".")[0]
        count = len(verified[[k for k, v in zip(lock_ids, keys) if v == lid_key][0]])
        if len(token_values[tok]) != count:
            problems.append(f"{slug}: {{{{{tok}}}}} is missing from some variants")

    # cross-lock collisions: count the VALID draws the engine can serve
    if all(lid in verified for lid in lock_ids):
        withdrawn = "noindex" in (room_dir / "index.html").read_text(encoding="utf-8")
        clues = clue_strings(js)
        libs = [[(key, v) for v in verified[lid]] for lid, key in zip(lock_ids, keys)]
        total = valid = 0
        for draw in itertools.product(*libs):
            total += 1
            valid += draw_is_valid(list(draw), clues)
        v0 = draw_is_valid([lib[0] for lib in libs], clues)
        state = "withdrawn" if withdrawn else "live"
        collision_report.append(f"{slug:<20} {state:<9} VALID {valid:>4} of {total:<4}  "
                                f"variant 0 {'VALID' if v0 else 'INVALID'}")
        if valid < MIN_VALID:
            problems.append(f"{slug}: only {valid} VALID draws, fewer than {MIN_VALID}")
        if not v0:
            warnings.append(f"{slug}: variant-0 draw is not VALID (never served)")

# ---- difficulty stars (ESCAPE-DIFFICULTY) ------------------------------------
BANDS = [(3, 1, "Warm-up", "1–3"), (5, 2, "Core", "4–5"), (9, 3, "Challenge", "6–9")]   # (top grade, stars, name, grades)
CARD = {"hub": (r'<a class="room-card" href="([a-z0-9-]+)/"', "chip"),
        "front page": (r'<a class="esc-card" href="escape-rooms/([a-z0-9-]+)/"', "esc-chip")}


def lock_grades(js):
    """[(lock id, grade or None)] in the order the locks appear."""
    out = []
    for m in re.finditer(r"\n      id: '([^']+)',", js):
        g = re.match(r"\n      key: '[^']+',\n      grade: (\d+),", js[m.end():].replace("\r\n", "\n"))
        out.append((m.group(1), int(g.group(1)) if g else None))
    return out


def room_label(js):
    """A room's optional student-facing label (contract STARTER-LABEL), or None."""
    m = re.search(r"\n  label: '([^']+)',", js.replace("\r\n", "\n"))
    return m.group(1) if m else None


def order_rank(label, stars):
    """Where a room sorts in the easiest-first order (contract STARTER-FIRST): a Starter room before every
    starred room (rank 0), an unlabelled room by its stars. Any other label has no rank until Jon rules (None)."""
    if label is None:
        return stars
    return 0 if label == "Starter" else None


def room_rating(grades):
    top = max(grades)
    return next((stars, name, gr) for t, stars, name, gr in BANDS if top <= t)


def check_ratings(room_js, live, pages, rating_js):
    """Problems with the difficulty stars. room_js {slug: text}; live {slug}; pages {name: html}."""
    out, want, seqs, rank = [], {}, {}, {}
    for slug in sorted(live):
        gs = lock_grades(room_js[slug])
        missing = [lid for lid, g in gs if g is None or not 1 <= g <= 9]
        if missing:
            out.append(f"{slug}: lock(s) with no grade 1-9: {', '.join(missing)}")
            continue
        want[slug] = room_rating([g for _, g in gs])
        rank[slug] = order_rank(room_label(room_js[slug]), want[slug][0])
        if rank[slug] is None:
            out.append(f"{slug}: the label {room_label(room_js[slug])!r} has no place in the easiest-first order; "
                       "it needs a ruling from Jon (contract STARTER-FIRST)")
            rank[slug] = want[slug][0]
    for page, html in pages.items():
        pat, chip = CARD[page]
        seen = []
        for m in re.finditer(pat + r".*?</a>", html, re.S):
            slug = m.group(1)
            seen.append(slug)
            if slug not in want:
                continue
            # A labelled room's card shows its label chip and never data-stars (STARTER-LABEL); the order below
            # still uses the derived rating.
            lab = room_label(room_js[slug])
            if lab:
                want_chip = ('<span class="%s" data-label="%s"><span aria-hidden="true">%s</span>'
                             '<span class="sr-only">Level: %s</span></span>' % (chip, lab.lower(), lab, lab))
                if 'data-stars' in m.group(0):
                    out.append(f"{page}: {slug}'s card carries data-stars, but the room has the label {lab!r}")
                elif want_chip not in m.group(0):
                    out.append(f"{page}: {slug}'s card has no label chip (want {want_chip})")
                continue
            if re.search(r'<span class="%s" data-label=' % chip, m.group(0)):
                out.append(f"{page}: {slug}'s card shows a label chip, but the room has no label")
                continue
            c = re.search(r'<span class="%s" data-stars="(\d)"><span aria-hidden="true">([^<]*)</span>'
                          r'<span class="sr-only">([^<]*)</span></span>' % chip, m.group(0))
            stars, name, gr = want[slug]
            label = "%s %s &middot; grades %s" % ("★" * stars, name, gr)
            sr = "Difficulty: %d of 3, %s, grades %s" % (stars, name, gr)
            if not c:
                out.append(f"{page}: {slug}'s card has no difficulty chip (want {label})")
            elif (int(c.group(1)), c.group(2), c.group(3)) != (stars, label, sr):
                out.append(f"{page}: {slug}'s card says {c.group(2)} (data-stars {c.group(1)}), "
                           f"its locks make it {label}")
        for slug in sorted(set(want) - set(seen)):
            out.append(f"{page}: no card for live room {slug}")
        # Every page that lists rooms lists them easiest first (FRONT-PAGE-ROOM-ORDER, 12 Oct 2026; the hub
        # says "Ordered easiest to hardest").
        seqs[page] = [s for s in seen if s in want]
        # A Starter room sorts before every starred room (STARTER-FIRST); an unlabelled room by its stars.
        order = [rank[s] for s in seqs[page]]
        if order != sorted(order):
            out.append(f"{page}: cards are not in rating order (easiest first, Starter before every star): "
                       + ", ".join(f"{s} {'Starter' if rank[s] == 0 else '*' * rank[s]}" for s in seqs[page]))
    # The hub is the one source for the order within a star band: the front page lists the same rooms in the same order.
    if "hub" in seqs:
        for page, seq in seqs.items():
            if page != "hub" and seq != seqs["hub"]:
                out.append(f"{page}: room order differs from the hub's (the hub is the source for the order within a band)."
                           f" hub: {', '.join(seqs['hub'])}; {page}: {', '.join(seq)}")
    js_bands = [(int(t), int(st), n, g) for st, n, g, t in re.findall(
        r"\{ stars: (\d), name: '([^']+)', grades: '([^']+)', top: (\d) \}", rating_js)]
    if js_bands != BANDS:
        out.append(f"escape-rooms/assets/rating.js bands {js_bands} differ from this checker's {BANDS}")
    return out


WORDS = {1: "one star", 2: "two stars", 3: "three stars"}


def check_star_key(pages):
    """Problems with the star key (contract STAR-KEY, 10 Oct 2026): the line on the hub and the front page
    that says what the stars mean must name exactly BANDS (already matched to rating.js above), each with
    its stars hidden from screen readers and a readable equivalent ("one star, Warm-up, grades 1 to 3"),
    and must say nothing about who a room suits."""
    out = []
    for page, html in pages.items():
        keys = re.findall(r"<p [^>]*data-star-key[^>]*>(.*?)</p>", html, re.S)
        if len(keys) != 1:
            out.append(f"{page}: {len(keys)} star-key lines (want exactly one)")
            continue
        seen = re.findall(r'<span aria-hidden="true">(★+) ([^,<]+), grades ([^<]+)</span>'
                          r'<span class="sr-only">([^<]*)</span>', keys[0])
        got = [(len(st), n, g) for st, n, g, _ in seen]
        want = [(st, n, g) for _, st, n, g in BANDS]
        if got != want:
            out.append(f"{page}: the star key says {got}, the bands are {want}")
        for (st, n, g), (_, _, _, sr) in zip(got, seen):
            a, _, b = g.partition("–")
            if sr.rstrip(";") != f"{WORDS.get(st, '?')}, {n}, grades {a} to {b}":
                out.append(f"{page}: the star key's screen-reader text for {n} reads {sr!r}")
        if re.search(r"top set|resit|suits", keys[0], re.I):
            out.append(f"{page}: the star key says who a room suits (teacher pages only)")
    return out


room_js = {d.name: (d / "room.js").read_text(encoding="utf-8")
           for d in ROOMS.iterdir() if d.is_dir() and (d / "room.js").exists()}
live = {s for s in room_js if "noindex" not in (ROOMS / s / "index.html").read_text(encoding="utf-8")}
pages = {"hub": (ROOMS / "index.html").read_text(encoding="utf-8"),
         "front page": (BASE / "index.html").read_text(encoding="utf-8")}
rating_js = (ROOMS / "assets" / "rating.js").read_text(encoding="utf-8")
problems += check_ratings(room_js, live, pages, rating_js)
problems += check_star_key(pages)
star_report = {s: room_rating([g for _, g in lock_grades(room_js[s])]) for s in sorted(live)
               if all(g for _, g in lock_grades(room_js[s]))}

# Planted faults: each must be caught, or the rule has stopped working.
HUB_CARD = r'<a class="room-card" href="%s/".*?</a>'


def swap_cards(html, a, b, pat=r'<a class="esc-card" href="escape-rooms/%s/".*?</a>'):
    """The page with the whole cards (with any wrapper's note left in place) of rooms a and b swapped."""
    ma, mb = re.search(pat % a, html, re.S), re.search(pat % b, html, re.S)
    (x, y) = sorted([ma, mb], key=lambda m: m.start())
    return (html[:x.start()] + y.group(0) + html[x.end():y.start()] + x.group(0) + html[y.end():])


if "rugby-mud" in live:
    hub_card = re.search(r'<a class="room-card" href="rugby-mud/".*?</a>', pages["hub"], re.S).group(0)
    one_star = re.sub(r'data-stars="\d"><span aria-hidden="true">[^<]*</span><span class="sr-only">[^<]*</span>',
                      'data-stars="1"><span aria-hidden="true">★ Warm-up &middot; grades 1–3</span>'
                      '<span class="sr-only">Difficulty: 1 of 3, Warm-up, grades 1–3</span>', hub_card, count=1)
    plants = {
        "Rugby Mud's hub card says ★": (room_js, dict(pages, hub=pages["hub"].replace(hub_card, one_star)), "rugby-mud's card says"),
        "a lock's grade removed": (dict(room_js, **{"rugby-mud": re.sub(r"\n      grade: \d+,", "", room_js["rugby-mud"], count=1)}),
                                   pages, "with no grade"),
    }
    key_mismatch = check_star_key(dict(pages, hub=pages["hub"].replace(
        "Core, grades 4–5</span>", "Core, grades 4–6</span>", 1)))
    if not any("the star key says" in g for g in key_mismatch):
        problems.append(f"planted fault NOT caught: the hub's star key saying grades 4–6 "
                        f"(the star-key check found {key_mismatch or 'nothing'})")
    # STARTER-LABEL: a label chip on an unlabelled room's card, and a star chip on a labelled room's card.
    label_chip = ('<span class="chip" data-label="starter"><span aria-hidden="true">Starter</span>'
                  '<span class="sr-only">Level: Starter</span></span>')
    star_chip = re.search(r'<span class="chip" data-stars="\d">.*?</span></span>', hub_card, re.S).group(0)
    plants["a label chip on Rugby Mud's card, which has no label"] = (
        room_js, dict(pages, hub=pages["hub"].replace(hub_card, hub_card.replace(star_chip, label_chip))),
        "shows a label chip, but the room has no label")
    plants["a star chip on the card of a labelled room"] = (
        dict(room_js, **{"rugby-mud": room_js["rugby-mud"].replace("\n  level:", "\n  label: 'Starter',\n  level:", 1)}),
        pages, "carries data-stars")
    # STARTER-FIRST: a Starter room's card after a starred room's card, and a label with no rank.
    starters = [s for s in live if room_label(room_js[s]) == "Starter"]
    if starters:
        st = starters[0]
        first_star = next(s for s in re.findall(CARD["hub"][0], pages["hub"]) if s in live and s != st
                          and room_label(room_js[s]) is None)
        plants["a Starter card placed after a starred card on the hub"] = (
            room_js, dict(pages, hub=swap_cards(pages["hub"], st, first_star, HUB_CARD)),
            "hub: cards are not in rating order")
    plants["a label other than Starter, which has no rank"] = (
        dict(room_js, **{"rugby-mud": room_js["rugby-mud"].replace("\n  level:", "\n  label: 'Beginner',\n  level:", 1)}),
        pages, "needs a ruling")
    for what, (rj, pg, expect) in plants.items():
        got = check_ratings(rj, live, pg, rating_js)
        if not any(expect in g for g in got):
            problems.append(f"planted fault NOT caught: {what} (the rating check found {got or 'nothing'})")
    plant_line = "planted faults caught: " + "; ".join(plants) + "; the hub's star key saying grades 4–6"
else:
    plant_line = "planted faults: skipped (rugby-mud is not live)"


# Order faults on the front page (FRONT-PAGE-ROOM-ORDER): each must be caught, or the order rule has stopped working.
hub_seq = re.findall(CARD["hub"][0], pages["hub"])
stars_of = {s: order_rank(room_label(room_js[s]), room_rating([g for _, g in lock_grades(room_js[s])])[0]) for s in live}
hub_seq = [s for s in hub_seq if s in stars_of]
same_band = next(((a, b) for a, b in zip(hub_seq, hub_seq[1:]) if stars_of[a] == stars_of[b]), None)
order_plants = {}
if hub_seq and stars_of[hub_seq[0]] != stars_of[hub_seq[-1]]:
    order_plants["two front-page cards swapped across a star band"] = (
        swap_cards(pages["front page"], hub_seq[0], hub_seq[-1]), "front page: cards are not in rating order")
if same_band:
    order_plants["front page rating-ordered but with a different tie order from the hub"] = (
        swap_cards(pages["front page"], *same_band), "front page: room order differs from the hub's")
for what, (fp, expect) in order_plants.items():
    got = check_ratings(room_js, live, dict(pages, **{"front page": fp}), rating_js)
    if not any(expect in g for g in got):
        problems.append(f"planted fault NOT caught: {what} (the rating check found {got or 'nothing'})")
if len(order_plants) != 2:
    problems.append(f"order plants: expected 2, built {len(order_plants)} (need a star band change and a tie in the hub)")
order_line = "order faults caught: " + "; ".join(order_plants)


# ---- every set, re-checked (ESCAPE-SET-CHECKS) -------------------------------
def check_sets(slug, lock_ids, library):
    """(problems, sets that passed) for one room: every set of every lock through escape_set_checks.check()."""
    out, passed = [], 0
    for lid in lock_ids:
        if not covered(lid):
            out.append(f"{slug}/{lid}: {NO_CHECK} (no entry in scripts/escape_set_checks.py), so its sets are unchecked")
            continue
        for i, var in enumerate(library.get(lid, [])):
            reason = check(lid, var)
            if reason:
                out.append(f"{slug}/{lid}: set {i} fails the check \"{reason}\"")
            else:
                passed += 1
    return out, passed


set_counts = {}
for slug in sorted(live):
    got, set_counts[slug] = check_sets(slug, re.findall(r"\n      id: '([^']+)'", room_js[slug]), verified)
    problems += got

# Planted: each broken set must fail with its check, through the same function, and its good original pass.
broken_cases = json.loads(BROKEN_SETS.read_text(encoding="utf-8"))["cases"]
for case in broken_cases:
    lid = case["lock"]
    got, _ = check_sets("fixture", [lid], {lid: [case["broken"]]})
    if not any(case["expect"] in g for g in got):
        problems.append(f"planted fault NOT caught: {case['why']} ({lid}; expected \"{case['expect']}\", "
                        f"the set check found {got or 'nothing'})")
    if case["good"] is not None:
        got, _ = check_sets("fixture", [lid], {lid: [case["good"]]})
        if got:
            problems.append(f"planted fault's good original fails: {lid} ({got})")

print(f"locks checked: {locks_seen}")
print(f"variants checked: {sum(len(v) for v in verified.values())}")
print("difficulty (hardest lock's grade):")
for slug, (stars, name, gr) in star_report.items():
    print(f"  {slug:<20} {'★' * stars:<3} {name} (grades {gr})")
print(plant_line)
print(order_line)
print("verified sets per live room (every set re-checked by scripts/escape_set_checks.py):")
for slug, n in set_counts.items():
    print(f"  {slug:<20} {n:>4}")
print(f"  {'total':<20} {sum(set_counts.values()):>4}  in {len(set_counts)} live rooms")
for slug in sorted(set(room_js) - live):
    print(f"  {slug:<20}  not checked (withdrawn)")
print(f"broken sets planted: {len(broken_cases)}, from {BROKEN_SETS.relative_to(BASE).as_posix()}; each must fail")
print("cross-lock collisions (VALID draws per room):")
for line in collision_report:
    print("  " + line)
if warnings:
    print(f"warnings: {len(warnings)}")
    for w in warnings:
        print("  -", w)
if pending_art:
    print(f"pending art: {len(pending_art)} (tracked in docs/escape-room-image-prompts.md)")
    for a in pending_art:
        print("  -", a)
if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("every room agrees with the audited bank and with variants.json; "
      "all tokens resolve" + ("" if pending_art else "; all art present"))
