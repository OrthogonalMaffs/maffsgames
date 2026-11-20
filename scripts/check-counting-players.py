#!/usr/bin/env python3
# ci-line: Counting Players pack (core-maths/counting-players/: build.py --check, every Values key recomputed from the two CSVs and every Condition true; the CSVs carry no fbclid, no query key but level, game, type, mode, topic, and no source naming a single school or college; each committed PDF's text holds every value its section fills; five planted faults caught) |
# ci-deps: core-maths/counting-players/ tools/counting-players/ scripts/check-counting-players.py scripts/plant_common.py
"""Counting Players: the pack's data, text and committed PDFs agree (contract COUNTING-PLAYERS, 20 Nov 2026).

    python -X utf8 scripts/check-counting-players.py

Fails when:
  1. tools/counting-players/build.py --check fails: a value computed from the CSVs differs from text.md's Values table,
     a Condition is false, or a placeholder is left unfilled;
  2. either CSV holds "fbclid" anywhere; a site-data landing page carries a query key other than level, game, type,
     mode or topic; or a source may name a single school or college (only school platform A, B and C stand for one);
  3. a committed PDF's text lacks any value its section of text.md fills in (or a TABLE 5 row): the PDF was not
     rebuilt after the data or the text changed. The text is read by a small stdlib PDF reader below (pdftotext's
     job: Chromium's Flate streams, Type0 fonts and ToUnicode maps), because CI's image has no pdftotext and the repo
     adds no dependency for it. Spaces are ignored in the comparison.
Then it plants five faults in temporary copies, each of which must be caught (plant_common: a plant that did not
apply is a STALE PLANT and fails the run): a Values number changed; Condition 8 broken by editing one TABLE 5 game's
row in the game records; a leftover placeholder; an fbclid row; a stale PDF (the committed PDFs against data changed
after they were built).
"""
import csv
import importlib.util
import pathlib
import re
import shutil
import sys
import tempfile
import urllib.parse
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import plant_common as pc  # noqa: E402

DATA = ROOT / "core-maths" / "counting-players"
TEXT = ROOT / "tools" / "counting-players" / "text.md"


def load_build():
    spec = importlib.util.spec_from_file_location("cp_build", ROOT / "tools" / "counting-players" / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = load_build()


# ------------------------------------------------------------------------------------------------ a small PDF reader
OBJ = re.compile(rb"(\d+)\s+0\s+obj\b(.*?)\bendobj", re.S)
REF = rb"(\d+)\s+0\s+R"


def pdf_objects(data):
    objs = {}
    for m in OBJ.finditer(data):
        body = m.group(2)
        stream = None
        s = re.search(rb"stream\r?\n", body)
        if s and b"endstream" in body:
            head = body[:s.start()]
            raw = body[s.end():body.rindex(b"endstream")].rstrip(b"\r\n")
            if b"/FlateDecode" in head:
                try:
                    raw = zlib.decompress(raw)
                except zlib.error:
                    raw = zlib.decompressobj().decompress(raw)
            stream, body = raw, head
        objs[int(m.group(1))] = (body, stream)
    return objs


def cmap_of(stream):
    """A ToUnicode CMap: code (bytes as int) -> text."""
    out = {}
    u16 = lambda h: bytes.fromhex(h.decode()).decode("utf-16-be", "replace")
    for block in re.findall(rb"beginbfchar(.*?)endbfchar", stream, re.S):
        for a, b in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>", block):
            out[int(a, 16)] = u16(b)
    for block in re.findall(rb"beginbfrange(.*?)endbfrange", stream, re.S):
        for a, b, rest in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(\[[^\]]*\]|<[0-9A-Fa-f]+>)", block):
            lo, hi = int(a, 16), int(b, 16)
            if rest.startswith(b"["):
                for k, h in enumerate(re.findall(rb"<([0-9A-Fa-f]+)>", rest)):
                    out[lo + k] = u16(h)
            else:
                base = bytes.fromhex(rest[1:-1].decode())
                for k in range(hi - lo + 1):
                    v = bytearray(base)
                    v[-1] = (v[-1] + k) & 0xFF
                    out[lo + k] = bytes(v).decode("utf-16-be", "replace")
    return out


def resolve_dict(objs, body, key):
    """The dictionary text for /key in body: inline << >> or an indirect reference."""
    m = re.search(rb"/" + key + rb"\s*" + REF, body)
    if m:
        return objs.get(int(m.group(1)), (b"", None))[0]
    m = re.search(rb"/" + key + rb"\s*<<", body)
    if not m:
        return b""
    i, depth = m.end() - 2, 0
    for j in range(i, len(body) - 1):
        if body[j:j + 2] == b"<<":
            depth += 1
        elif body[j:j + 2] == b">>":
            depth -= 1
            if depth == 0:
                return body[i:j + 2]
    return b""


def page_text(objs, page_body):
    res = resolve_dict(objs, page_body, b"Resources")
    fonts = resolve_dict(objs, res, b"Font")
    maps = {}
    for name, num in re.findall(rb"/([A-Za-z0-9_.+-]+)\s*" + REF, fonts):
        fbody = objs.get(int(num), (b"", None))[0]
        tu = re.search(rb"/ToUnicode\s*" + REF, fbody)
        if tu:   # Skia: Type0 fonts take two-byte codes, its Type3 fonts one-byte codes
            maps[name] = (cmap_of(objs[int(tu.group(1))][1] or b""), 2 if b"/Type0" in fbody else 1)
    contents = re.search(rb"/Contents\s*(\[[^\]]*\]|" + REF + rb")", page_body)
    nums = [int(n) for n in re.findall(REF, contents.group(1))] if contents else []
    out, cmap, width = [], {}, 2
    for n in nums:
        stream = objs.get(n, (b"", None))[1] or b""
        for tok in re.finditer(rb"/([A-Za-z0-9_.+-]+)\s+[\d.]+\s+Tf|\[((?:[^\]\\]|\\.)*)\]\s*TJ|<([0-9A-Fa-f]*)>\s*Tj|"
                               rb"\b(T\*|Td|TD|Tm|ET)\b", stream):
            if tok.group(1):
                cmap, width = maps.get(tok.group(1), ({}, 2))
            elif tok.group(2) is not None or tok.group(3) is not None:
                hexes = re.findall(rb"<([0-9A-Fa-f]*)>", tok.group(2)) if tok.group(2) is not None else [tok.group(3)]
                for h in hexes:
                    raw = bytes.fromhex(h.decode())
                    for k in range(0, len(raw) - width + 1, width):
                        out.append(cmap.get(int.from_bytes(raw[k:k + width], "big"), ""))
            else:
                out.append(" ")
    return "".join(out)


def pdf_text(path):
    data = pathlib.Path(path).read_bytes()
    objs = pdf_objects(data)
    order = []
    for body, _ in objs.values():          # the page tree's /Kids, in reading order (Chromium's tree is flat)
        if re.search(rb"/Type\s*/Pages\b", body):
            kids = re.search(rb"/Kids\s*\[([^\]]*)\]", body)
            order += [int(n) for n in re.findall(REF, kids.group(1))] if kids else []
    pages = [objs[n][0] for n in order if n in objs and re.search(rb"/Type\s*/Page\b", objs[n][0])]
    return [page_text(objs, p) for p in pages]


# ------------------------------------------------------------------------------------------------ the checks
def csv_problems(folder):
    folder = pathlib.Path(folder)
    out = []
    for name in (B.SITE_NAME, B.GAMES_NAME):
        text = (folder / name).read_text(encoding="utf-8")
        if "fbclid" in text.lower():
            out.append("%s: contains fbclid" % name)
    with open(folder / B.SITE_NAME, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        q = urllib.parse.urlsplit(r["landing_page"]).query
        keys = {k for k, _ in urllib.parse.parse_qsl(q, keep_blank_values=True)}
        bad = keys - B.QUERY_KEYS
        if bad:
            out.append("%s: landing page %s carries %s" % (B.SITE_NAME, r["landing_page"], ", ".join(sorted(bad))))
    out += ["%s: source %s" % (B.SITE_NAME, s) for s in B.source_problems(rows)]
    return out


def pdf_problems(text_path, data_dir, pdf_dir):
    text = pathlib.Path(text_path).read_text(encoding="utf-8")
    site, games = B.load(data_dir)
    v, f = B.compute(site, games)
    out = []
    norm = lambda s: re.sub(r"\s+", "", s)
    for pdf, keys in B.placeholders_by_doc(text).items():
        path = pathlib.Path(pdf_dir) / pdf
        if not path.exists():
            out.append("%s: missing" % pdf)
            continue
        pages = pdf_text(path)
        body = norm("".join(pages))
        if "CountingPlayers" not in body:
            out.append("%s: no text read from the PDF (reader fault?)" % pdf)
            continue
        for k in keys:
            if norm(v[k]) not in body:
                out.append("%s: lacks {{%s}} = %s" % (pdf, k, v[k]))
        if pdf.endswith("preliminary-material.pdf"):
            for t in f["t5"]:
                row = norm("%s%s%s%s%%" % (t["game"], B.thou(t["answers"]), B.thou(t["correct"]), B.fixed(t["acc"], 0)))
                if row not in body:
                    out.append("%s: lacks the TABLE 5 row for %s" % (pdf, t["game"]))
        footer = norm(B.footer_text(text))
        for i, p in enumerate(pages, 1):
            if footer + str(i) not in norm(p):
                out.append("%s: page %d lacks the footer with its page number" % (pdf, i))
    return out


def check_build(text_path, data_dir):
    code, lines = B.run(text_path, data_dir, check_only=True)
    return [] if code == 0 else lines[1:]


def run_checks(text_path=TEXT, data_dir=DATA, pdf_dir=DATA):
    return {"build": check_build(text_path, data_dir), "csv": csv_problems(data_dir),
            "pdf": pdf_problems(text_path, data_dir, pdf_dir)}


# ------------------------------------------------------------------------------------------------ plants
def plants():
    """[(name, caught, detail)]. Each plant works in a temporary copy; nothing in the repo is changed."""
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)

        def copy():
            d = tmp / ("c%d" % len(list(tmp.iterdir())))
            d.mkdir()
            for name in (B.SITE_NAME, B.GAMES_NAME):
                shutil.copy(DATA / name, d / name)
            shutil.copy(TEXT, d / "text.md")
            return d

        def plant(name, fn, judge):
            try:
                d = copy()
                fn(d)
                found = judge(d)
                results.append((name, pc.is_caught(found), "; ".join(found)[:200] or "NOT CAUGHT"))
            except pc.StalePlant as e:
                results.append((name, False, str(e)))

        def edit(path, old, new, name, **kw):
            path.write_text(pc.apply_plant(path.read_text(encoding="utf-8"), old, new, name=name, **kw), encoding="utf-8",
                            newline="")

        # 1. a Values number changed: days 61 -> 62
        plant("a Values number changed",
              lambda d: edit(d / "text.md", "| days from 20 Sep to 19 Nov 2026 inclusive | 61 |",
                             "| days from 20 Sep to 19 Nov 2026 inclusive | 62 |", "the days row"),
              lambda d: [m for m in check_build(d / "text.md", d) if m.startswith("VALUE days:")])

        # 2. Condition 8 broken: six-sevens-bruv's busiest row in the TABLE 5 week loses its correct answers
        def break_c8(d):
            p = d / B.GAMES_NAME
            lines = p.read_text(encoding="utf-8").split("\n")
            best = max((i for i, ln in enumerate(lines) if re.match(r"2026-11-1[3-9],six-sevens-bruv,", ln)),
                       key=lambda i: int(lines[i].split(",")[3]), default=None)
            if best is None:
                raise pc.StalePlant("Condition 8", "no six-sevens-bruv row in the TABLE 5 week")
            lines[best] = ",".join(lines[best].split(",")[:4] + ["0"])
            p.write_text("\n".join(lines), encoding="utf-8", newline="")
        plant("Condition 8 broken (one TABLE 5 row edited)", break_c8,
              lambda d: [m for m in check_build(d / "text.md", d) if m.startswith("CONDITION condition 8 ")])

        # 3. a leftover placeholder
        plant("a leftover placeholder",
              lambda d: edit(d / "text.md", "Time allowed: 1 hour 30 minutes", "Time allowed: {{time_allowed}}",
                             "the cover's time"),
              lambda d: [m for m in check_build(d / "text.md", d) if "time_allowed" in m])

        # 4. an fbclid row
        def fbclid(d):
            p = d / B.SITE_NAME
            raw = p.read_bytes()
            eol = b"\r\n" if b"\r\n" in raw else b"\n"
            p.write_bytes(raw + b"2026-11-19,facebook.com,referral,mobile,/?fbclid=IwAR0plant,1,0,1" + eol)
        plant("an fbclid row", fbclid, lambda d: [m for m in csv_problems(d) if "fbclid" in m])

        # 5. a stale PDF: the committed PDFs judged against data changed after they were built
        def stale(d):
            p = d / B.GAMES_NAME
            text = p.read_text(encoding="utf-8")
            m = re.search(r"^2026-11-03,([^,]+),(\d+),(\d+),(\d+)", text, re.M)
            if not m:
                raise pc.StalePlant("a stale PDF", "no 2026-11-03 row in the game records")
            old = m.group(0)
            new = "2026-11-03,%s,%d,%s,%s" % (m.group(1), int(m.group(2)) + 1, m.group(3), m.group(4))
            p.write_text(pc.apply_plant(text, old, new, name="a 3 November row"), encoding="utf-8", newline="")
        plant("a stale PDF", stale, lambda d: [m for m in pdf_problems(d / "text.md", d, DATA) if " lacks {{" in m])
    return results


def main():
    problems = run_checks()
    failed = False
    for k, label in (("build", "build.py --check"), ("csv", "CSVs"), ("pdf", "committed PDFs")):
        if problems[k]:
            failed = True
            print("FAIL %s:" % label)
            for p in problems[k]:
                print("  " + p)
        else:
            print("ok   %s" % label)
    for name, caught, detail in plants():
        print("%s plant: %s (%s)" % ("ok  " if caught else "FAIL", name, detail))
        failed |= not caught
    print("FAILED" if failed else "PASSED")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
