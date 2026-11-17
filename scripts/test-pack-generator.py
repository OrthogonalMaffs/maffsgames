#!/usr/bin/env python3
# ci-line: Pack generator (tools/pack-generator/build_pack.py --selftest: every room with a pack config gets VALID sets, distinct answers per lock and one final-padlock shape, every value recomputed independently; sixty-seven planted faults caught (answers, draws, URL, score sheet, final padlock, penalties, answer-box hints, stakes placement, page-1 length, repeated rules, shape or calculator on a student page, an unfriendly product, DRAFT and approval, a broken caption or caption override, a multi-part clue's broken caption, a clue with no bold part, a caption starting with punctuation, a print override on a red herring, an ungraded lock, a printed unit's scale that is not whole or is wrong, an answer box left in the room's unit, a hint giving a scaled answer in the room's unit only, a cover, certificate or read-outs too long past their last fitting rule, read-outs left on one page, a dark answer box without its white fill, an answer box under 20 mm wide or under 4.5 mm high, a DRAFT pack with a small answer box built with --final, a hint card whose figure is not bound to its unit; multi-part, long-story, longest-story, answer-box and binding controls pass); then this file's HAMSTER-HEIST-PACK plants (a wrong recomputed answer for each Hamster Heist lock, its heat-lamp scale removed, its manual left in the room's unit, a product of two factors of 100 or more in final.py and lockcheck.py, fixed penalty figures on a hints page, a cover and the score sheet) and HAMSTER-PACK-FINAL plants (a miss_scale of 0, 1.5 or true, lockcheck's printed miss disagreeing, a set whose printed common wrong answer is its answer, lock_words for an unknown lock, hint number or token or empty, an override with an unbound figure) and PE-SHED-FINAL plants (a readout_voice that is empty, holds a {{token}} or is not a string) and HEATWAVE-PACK plants (a wrong recomputed answer and common wrong answer for each Heatwave Mutiny lock, a clue with no bold part given only "printed", only "caption" or an empty "printed", a lock_words label that still gives the code's length or is empty) and FINAL-PADLOCK-FAIR plants (a product of 10,001, a pack whose sets mix digit signatures, a largest product over 3 x the smallest, a plus-and-minus pack whose largest terms differ in digits, a PDF name without its version); controls: an entity-written and an other-spelling unit each converted, time maths on a hints page, the room's own lock_words, the heat lamp as printed, car-trap with no miss_scale, a readout_voice printed in italics above the hook on the read-out page, the P.E. Store Rebellion's own readout_voice, a clue with no bold part given both overrides, Heatwave's own clock and sticky note, Heatwave's keypad label as printed, a product of exactly 10,000, Hamster Heist's and Heatwave's packs as built, the build's versioned PDF name; no PDF is ever built in CI) |
# ci-deps: tools/pack-generator/ escape-rooms/ escape-rooms/variants.json scripts/check-escape-rooms.py scripts/escape_set_checks.py scripts/plant_common.py scripts/bank_common.py CNAME
"""CI's entry to the printable-pack generator's self-test (contract PACK-GENERATOR, 4 Nov 2026).

CI finds its lines only in scripts/*.py headers (scripts/ci-groups.py), and the generator lives in tools/pack-generator/,
so this file is the line. It runs `build_pack.py --selftest`, then the plants of contract HAMSTER-HEIST-PACK
(Amendments 1 and 2, 16 Nov 2026), which import the generator and plant faults against The Great Hamster Heist's own
locks, sets and config, then those of HAMSTER-PACK-FINAL (miss_scale, the answer/miss rule, lock_words), then those of PE-SHED-FINAL
(readout_voice, the line naming whose voice the start read-out is in), then those of HEATWAVE-PACK (its three
recomputes, a clue with no bold part, a lock's print-only instrument label), then those of FINAL-PADLOCK-FAIR (the 10,000
ceiling, one difficulty per pack, the version in the PDF's name). Each plant must be caught by the check named beside it; each control must pass. A plant whose
target has gone is a STALE PLANT, which fails the run (plant_common). The self-test builds no PDF: the pack is the
product, and never a CI artifact.
"""
import copy
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS = os.path.join(ROOT, "tools", "pack-generator")
BUILD = os.path.join(PACKS, "build_pack.py")
SLUG = "hamster-heist"
SCALED = "heat-lamp-gradient"


def lock_index(locks, lock_id, pc):
    i = next((k for k, l in enumerate(locks) if l["id"] == lock_id), None)
    if i is None:
        raise pc.StalePlant("a %s plant" % lock_id, "%s has no lock %s" % (SLUG, lock_id))
    return i


def unit_words_on_art(B, cfg, room, teach, locks, s):
    """A NEW check (this test's, HAMSTER-HEIST-PACK item 5c): for every lock the pack asks for in a printed unit, the
    words printed on the art of each clue the room's teacher page maps to that lock (TEACH.clueMap, matched by the
    lock's name) must not name the room's own rate ("per minute", from the room's unit spellings) and one of them must
    name the printed unit's ("ten minutes"). A manual that still says "degrees per minute" over an answer box asking
    for degrees per ten minutes would set students the wrong question."""
    out = []
    by_obj = {im.get("object"): im for im in cfg["images"]}
    fill = B.filler(locks, s)
    for l in locks:
        au = l.get("answer_unit")
        if not au:
            continue
        own = B.text_of((l.get("instrument") or {}).get("unit", "")).strip()
        rate = lambda u: u[u.index(" per ") + len(" per "):].strip().lower() if " per " in u else None
        room_rates = {r for r in (rate(x) for x in [own] + au.get(B.ROOM_SPELLINGS, [])) if r}
        printed_rate = rate(au["unit"])
        clues = [cid for cid, what in (teach.get("clueMap") or {}).items()
                 if B.text_of(what).strip().lower().startswith(l["name"].lower())]
        if not clues:
            out.append("%s: the teacher page maps no clue to %r" % (l["id"], l["name"]))
            continue
        said = []
        for cid in clues:
            o = next(x for x in room["objects"] if x["id"] == cid)
            im = by_obj.get(cid, {})
            printed, _ = B.split_clue(fill(o["clue"]), SLUG, cid,
                                      *(fill(im[k]) if k in im else None for k in B.OVERRIDES))
            words = " ".join(B.text_of(printed).replace(chr(160), " ").lower().split())
            said.append(words)
            for r in room_rates:
                if re.search(r"\bper %s\b" % re.escape(r), words):
                    out.append("%s, clue %s: its art says %r, the room's unit, but the answer box asks for %s"
                               % (l["id"], cid, "per " + r, au["unit"]))
        if printed_rate and not any(printed_rate in w for w in said):
            out.append("%s: no clue's art names %r, the printed unit's rate" % (l["id"], printed_rate))
    return out


def hamster_plants():
    sys.path[:0] = [PACKS, os.path.join(ROOT, "scripts")]
    import build_pack as B
    import final as finalpad
    import lockcheck
    import plant_common as pc
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            pg = B.offline_context(browser).new_page()
            checker, cfg, room, teach, room_js, locks, sets, valid, total, n, seed, rating = B.prepare(SLUG, None, None, pg)
            car = B.prepare("car-trap", None, None, pg)       # the control room: a scaled lock with no miss_scale
            heat = B.prepare("heatwave-mutiny", None, None, pg)  # HEATWAVE-PACK: no-bold clues, a keypad label
        finally:
            browser.close()
    shape = cfg.get("final_shape", finalpad.DEFAULT_SHAPE)
    s0 = sets[0]
    results = []          # (name, kind "plant" or "control", findings, which check)

    # (a) a wrong recomputed answer for each lock: lockcheck's RECOMPUTE entry, through verify_sets
    for lock_id in ("hamster-wheel-rpm", "hamster-feeder-bounds", SCALED):
        def plant(lock_id=lock_id):
            i = lock_index(locks, lock_id, pc)
            s = copy.deepcopy(sets)
            s[0]["vars"][i]["answer"] = s[0]["vars"][i]["answer"] + 1
            return [x for x in B.verify_sets(locks, s)[0] if "%s: answer is " % lock_id in x]
        results.append(("a wrong recomputed answer for %s" % lock_id, "plant", plant, "verify_sets / lockcheck.RECOMPUTE"))

    # (b) the heat-lamp scale removed: its decimal answer reaches the final padlock, whose printed expression no longer
    # uses the set's answers
    def plant_scale_removed():
        i = lock_index(locks, SCALED, pc)
        if not locks[i].get("answer_unit"):
            raise pc.StalePlant("the heat-lamp scale removed", "%s has no printed unit to remove" % SCALED)
        bare = [dict(l) for l in locks]
        del bare[i]["answer_unit"]
        if B.verify_finals(checker, locks, sets, shape):
            return []                                    # the control: as configured, every set's padlock passes
        return B.verify_finals(checker, bare, sets, shape)
    results.append(("the heat-lamp scale removed (the decimal reaches the final padlock)", "plant",
                    plant_scale_removed, "verify_finals / lockcheck.final_problems"))

    # (c) the manual's printed words left in the room's unit ("per minute") while the answer box asks per ten minutes
    def plant_manual_per_minute():
        if unit_words_on_art(B, cfg, room, teach, locks, s0):
            return []                                    # the control: the pack's own manual names ten minutes
        bad = copy.deepcopy(cfg)
        im = next((x for x in bad["images"] if x.get("object") == "manual"), None)
        if not im or "printed" not in im:
            raise pc.StalePlant("the manual left per minute", "the manual has no printed override")
        im["printed"] = pc.apply_plant(im["printed"], "every ten minutes", "per minute",
                                       name="the manual left per minute")
        return unit_words_on_art(B, bad, room, teach, locks, s0)
    results.append(("the manual's printed text left saying per minute", "plant", plant_manual_per_minute,
                    "unit_words_on_art (new, this file)"))

    # (d) controls: a unit written as an HTML entity, and the declared other spelling, each converted
    i = lock_index(locks, SCALED, pc)
    lamp, v = locks[i], s0["vars"][i]
    want = "= %s %s" % (B.format_token(B.printed_number(lamp, v["answer"])), lamp["answer_unit"]["unit"])
    for label, text in (("an entity-written unit (&deg;C/min)", "Set it to <b>{{grad.aTxt}} &deg;C/min</b>."),
                        ("the declared other spelling (°C per minute)", "Set it to {{grad.aTxt}} °C per minute.")):
        def control(text=text):
            shown = " ".join(B.text_of(B.filler(locks, s0)(text)).replace(chr(160), " ").split())
            return [] if want in shown else ["%r printed %r, without %r" % (text, shown, want)]
        results.append((label + " gets its scaled version", "control", control, "both_units / as_read"))

    def plant_undeclared_spelling():
        # the other side of (d): a spelling the config does not declare still stops the build
        try:
            B.filler(locks, s0)("Set it to {{grad.aTxt}} degrees a minute.")
        except B.BuildError as e:
            return [str(e)] if "without the room's unit" in str(e) else []
        return []
    results.append(("an undeclared spelling of the unit", "plant", plant_undeclared_spelling, "both_units"))

    # (e) a final padlock whose one solution multiplies two numbers of 100 or more: final.py and lockcheck.py each
    nums, expr = [420, 812, 18], "420 × 812 − 18"
    target = 420 * 812 - 18

    def plant_big_product_final():
        bad = finalpad.canon((420, 812, 18), ("*", "-"))
        if finalpad.value(bad) != target:
            raise pc.StalePlant("a product of two factors of 100 or more", "final.canon no longer reads 420 x 812 - 18")
        if not finalpad.friendly(finalpad.canon((18, 420, 812), ("*", "+"))):
            return []                                    # the control: 18 x 420 + 812 is friendly
        return [] if finalpad.friendly(bad) else ["final.py: 420 x 812 is not friendly"]
    results.append(("a product of two factors of 100 or more, in final.py", "plant", plant_big_product_final,
                    "final.friendly"))

    def plant_big_product_lockcheck():
        good = lockcheck.final_problems("F", [420, 812, 18], {"target": 18 * 420 + 812, "expr": "18 × 420 + 812"}, shape)
        if any("100 or more" in x for x in good):
            return []                                    # the control: 18 x 420 + 812 passes the rule
        return [x for x in lockcheck.final_problems("F", nums, {"target": target, "expr": expr}, shape)
                if "two numbers of 100 or more" in x]
    results.append(("a product of two factors of 100 or more, in lockcheck.py", "plant", plant_big_product_lockcheck,
                    "lockcheck.final_problems"))

    # ---- HAMSTER-PACK-FINAL (16 Nov 2026): miss_scale, the answer/miss rule, lock_words ------------------------------
    def refused(fn):
        try:
            fn()
        except B.BuildError as e:
            return [str(e)]
        return []

    for bad in (0, 1.5, True):
        def plant_miss_scale(bad=bad):
            return refused(lambda: B.answer_units(
                {"answer_units": {SCALED: {"unit": "°C per ten minutes", "scale": 10, "miss_scale": bad}}}, SLUG))
        results.append(("a miss_scale of %r" % (bad,), "plant", plant_miss_scale, "answer_units"))

    def plant_printed_miss_disagrees():
        # without miss_scale the wrong answer prints as the rise x 10, which lockcheck's own figure (the rise) refutes
        if B.verify_sets(locks, sets)[0]:
            return []                                    # the control: as configured, every printed figure agrees
        bare = [dict(l, answer_unit={k: v for k, v in l["answer_unit"].items() if k != "miss_scale"})
                if l.get("answer_unit") else l for l in locks]
        if bare == locks:
            raise pc.StalePlant("the printed miss disagreeing", "%s has no miss_scale to remove" % SCALED)
        return [x for x in B.verify_sets(bare, sets)[0] if "miss prints as" in x]
    results.append(("lockcheck's printed miss disagreeing with the printed miss", "plant", plant_printed_miss_disagrees,
                    "verify_sets / lockcheck PRINTED"))

    def plant_miss_is_answer():
        # a set whose heat lamp has readings ten minutes apart: the rise is the answer per ten minutes
        i = lock_index(locks, SCALED, pc)
        k = next((j for j, v in enumerate(locks[i]["variants"]) if v["run"] == 10), None)
        if k is None:
            raise pc.StalePlant("a set whose printed miss is its answer", "no heat-lamp variant is ten minutes apart")
        if any("prints as its answer" in x for x in B.check_sets(checker, room_js, locks, sets)):
            return []                                    # the control: the chosen sets have none
        s = copy.deepcopy(sets)
        s[0]["vars"][i] = copy.deepcopy(locks[i]["variants"][k])
        return [x for x in B.check_sets(checker, room_js, locks, s) if "prints as its answer" in x]
    results.append(("a set whose printed common wrong answer is its printed answer", "plant", plant_miss_is_answer,
                    "check_sets / miss_is_answer"))

    base = B.with_answer_units(cfg, B.room_locks(room, SLUG), SLUG)       # the locks before lock_words
    words = cfg.get("lock_words") or {}
    if not words:
        raise pc.StalePlant("lock_words plants", "%s has no lock_words" % SLUG)

    def with_words(w):
        return refused(lambda: B.with_lock_words(dict(cfg, lock_words=w), base, SLUG))
    w0 = copy.deepcopy(words)
    for label, w in (("an unknown lock", {"no-such-lock": {"missSays": "Words."}}),
                     ("an unknown hint number", {SCALED: {"hints": {"9": "Words."}}}),
                     ("an unknown token", {SCALED: {"missSays": "It took {{grad.nope}} minutes."}}),
                     ("an empty string", {SCALED: {"hints": {"1": "  "}}})):
        results.append(("a lock_words entry with %s" % label, "plant", lambda w=w: with_words(w), "with_lock_words"))
    results.append(("Hamster Heist's own lock_words", "control", lambda: with_words(w0), "with_lock_words"))

    def plant_unbound_override():
        # the override as the pack fills it is bound ("4 minutes" with a no-break space); with an ordinary space the
        # printed-words figure rule must catch it
        i = lock_index(locks, SCALED, pc)
        good = B.filler(locks, s0)(locks[i]["missSays"])
        if words[SCALED]["missSays"] != locks[i]["missSays"]:
            raise pc.StalePlant("an override with an unbound figure", "the lock does not carry its lock_words missSays")
        if B.unbound_figures(good):
            return []                                    # the control: as filled, the override is bound
        bad = pc.apply_plant(good, chr(160) + "minutes", " minutes", allow_multiple=True,
                             name="an override with an unbound figure")
        return B.unbound_figures(bad)
    results.append(("an override with an unbound figure", "plant", plant_unbound_override, "unbound_figures"))

    def control_overrides_printed():
        i = lock_index(locks, SCALED, pc)
        out = []
        if locks[i]["hints"][0] != words[SCALED]["hints"]["1"]:
            out.append("hint 1 is not the override")
        if room["locks"][i]["hints"][0] == locks[i]["hints"][0]:
            out.append("the live room's hint 1 was changed")
        for s in sets:
            v = s["vars"][i]
            a, m = B.printed_number(locks[i], v["answer"], "answer"), B.printed_number(locks[i], v["miss"], "miss")
            if m != v["rise"] or a == m:
                out.append("set %s: printed miss %s, answer %s, rise %s" % (s["letter"], m, a, v["rise"]))
            if v["run"] == 10:
                out.append("set %s: readings ten minutes apart" % s["letter"])
        return out
    results.append(("the heat lamp as printed: hint 1 and missSays overridden, miss the rise, never the answer",
                    "control", control_overrides_printed, "with_lock_words / miss_scale"))

    def control_car_trap():
        c_checker, c_cfg, c_room, c_teach, c_js, c_locks, c_sets = car[:7]
        au = next(l["answer_unit"] for l in c_locks if l.get("answer_unit"))
        out = ["car-trap has a miss_scale"] if "miss_scale" in au else []
        out += B.verify_sets(c_locks, c_sets)[0] + B.check_sets(c_checker, c_js, c_locks, c_sets)
        for l in c_locks:
            if l.get("answer_unit"):
                for s in c_sets:
                    v = s["vars"][c_locks.index(l)]
                    if B.printed_number(l, v["miss"], "miss") != B.printed_number(l, v["miss"], "answer"):
                        out.append("car-trap's miss is not scaled as its answer")
        return out
    results.append(("car-trap with no miss_scale", "control", control_car_trap, "scale_of / verify_sets"))

    # ---- PE-SHED-FINAL (16 Nov 2026): readout_voice, whose voice the start read-out is in ---------------------------
    def voiced(v):
        return refused(lambda: B.readout_voice(dict(cfg, readout_voice=v), SLUG))
    for label, bad in (("empty", "   "), ("holding a {{token}}", "Read this as the keeper of {{wheel.r}} hamsters."),
                       ("not a string", ["Read this as the keeper."])):
        results.append(("a readout_voice %s" % label, "plant", lambda bad=bad: voiced(bad), "readout_voice"))

    def control_voice_printed():
        # the read-out page as build_html prints it, with a voice: the voice in italics, first in the start read-out,
        # above the hook; and the pack as configured (no voice) prints no voice line
        voice = "Read this as the head keeper, standing at the cage door. It&rsquo;s feeding time."
        greys = {l["id"]: 255 for l in locks}          # every answer box over white art: covers only, not read here
        out = []
        for c, want in ((dict(cfg, readout_voice=voice), True), (cfg, False)):
            if "readout_voice" in cfg:
                raise pc.StalePlant("a readout_voice control", "%s now has a readout_voice of its own" % SLUG)
            doc = B.build_html(SLUG, room, teach, locks, sets, c, seed, "2026-11-16", B.room_url(SLUG), rating,
                               greys=greys)[0]
            kinds = re.findall(r'<section class="page[^"]*" data-kind="(\w+)"', doc)
            pages = re.split(r'(?=<section class="page)', doc)[1:]
            if len(pages) != len(kinds) or kinds[:2] != ["run", "readouts"]:
                out.append("the pages begin %r, not run then readouts" % kinds[:2])
                continue
            page2 = pages[1]
            start = page2[page2.index("Read this at the start"):page2.index("</blockquote>")]
            line = "<p class='voice'><i>%s</i></p>" % voice
            hook = B.text_of(room["hook"]).split()[0]
            if want:
                if line not in start:
                    out.append("the voice is not printed in italics in the start read-out")
                elif not re.match(r"<blockquote>%s<p>" % re.escape(line), start[start.index("<blockquote>"):]):
                    out.append("the voice is not the start read-out's first line")
                elif B.text_of(start).find(hook) < B.text_of(start).find("feeding time"):
                    out.append("the voice is not above the hook")
                if line in doc.replace(page2, ""):
                    out.append("the voice is printed off the read-out page")
            elif "class='voice'" in doc:
                out.append("a pack with no readout_voice prints a voice line")
        return out
    results.append(("a readout_voice printed in italics above the hook, on the read-out page", "control",
                    control_voice_printed, "readout_voice / readouts / build_html"))
    results.append(("The P.E. Store Rebellion's own readout_voice", "control",
                    lambda: voiced(B.load_config("pe-shed-rebellion").get("readout_voice")) or
                    ([] if B.load_config("pe-shed-rebellion").get("readout_voice") else ["pe-shed-rebellion has none"]),
                    "readout_voice"))

    # ---- HEATWAVE-PACK (16 Nov 2026): its recomputes, a clue with no <b> part, a lock's print-only label ------------
    HW = "heatwave-mutiny"
    h_checker, h_cfg, h_room, h_teach, h_js, h_locks, h_sets = heat[:7]
    for lock_id in ("patrol-lcm-timer", "cube-surface-volume", "canteen-freezer-inequality"):
        for key in ("answer", "miss"):
            def plant_hw(lock_id=lock_id, key=key):
                i = next((k for k, l in enumerate(h_locks) if l["id"] == lock_id), None)
                if i is None:
                    raise pc.StalePlant("a %s plant" % lock_id, "%s has no lock %s" % (HW, lock_id))
                s = copy.deepcopy(h_sets)
                s[0]["vars"][i][key] = s[0]["vars"][i][key] + 1
                return [x for x in B.verify_sets(h_locks, s)[0] if "%s: %s is " % (lock_id, key) in x]
            results.append(("a wrong recomputed %s for %s" % (key, lock_id), "plant", plant_hw,
                            "verify_sets / lockcheck.RECOMPUTE"))
    results.append(("Heatwave Mutiny's six sets as chosen", "control", lambda: B.verify_sets(h_locks, h_sets)[0],
                    "verify_sets / lockcheck.RECOMPUTE"))

    NO_BOLD = "The note says: “Back <i>at the same time</i>. Not before.”"

    def split(printed, caption):
        return refused(lambda: B.split_clue(NO_BOLD, "plant", "clock", printed, caption))
    for label, printed, caption in (('only "printed"', "At the same time.", None),
                                    ('only "caption"', None, "The note says it."),
                                    ('an empty "printed"', "  ", "The note says it.")):
        results.append(("a clue with no <b> part given %s" % label, "plant",
                        lambda printed=printed, caption=caption: split(printed, caption), "split_clue"))

    def control_no_bold_both():
        got = B.split_clue(NO_BOLD, "control", "clock", "At the same time.", "The note says it.")
        return [] if got == ("At the same time.", "The note says it.") else ["split_clue returned %r" % (got,)]
    results.append(("a clue with no <b> part given both overrides", "control", control_no_bold_both, "split_clue"))

    def control_heatwave_no_bold():
        # the room's own clock and sticky note, as configured, through split_clue for every set
        by_obj = {im.get("object"): im for im in h_cfg["images"]}
        out, seen = [], 0
        for x in h_sets:
            f = B.filler(h_locks, x)
            for o in h_room["objects"]:
                if o.get("clue") and "<b>" not in o["clue"]:
                    seen += 1
                    im = by_obj[o["id"]]
                    out += refused(lambda: B.split_clue(f(o["clue"]), HW, o["id"],
                                                        *(f(im[k]) if k in im else None for k in B.OVERRIDES)))
        if not seen:
            raise pc.StalePlant("Heatwave's no-bold clues", "%s has no clue without a <b> part" % HW)
        return out
    results.append(("Heatwave Mutiny's clock and sticky note (no <b> part, both overrides)", "control",
                    control_heatwave_no_bold, "split_clue"))

    KEYPAD = "cube-surface-volume"
    h_base = B.with_answer_units(h_cfg, B.room_locks(h_room, HW), HW)

    def labelled(label):
        locks2 = B.with_lock_words(dict(h_cfg, lock_words={KEYPAD: {"label": label}}), h_base, HW)
        return B.instrument_hints([B.answer_caption(l) for l in locks2])
    room_label = next(l for l in h_room["locks"] if l["id"] == KEYPAD)["instrument"]["label"]
    results.append(("a lock_words label that still gives the code's length (the room's own)", "plant",
                    lambda: labelled(B.text_of(room_label)), "with_lock_words / instrument_hints"))
    results.append(("an empty lock_words label", "plant", lambda: refused(lambda: labelled("  ")), "with_lock_words"))

    def control_keypad_label():
        lock = next(l for l in h_locks if l["id"] == KEYPAD)
        out = [] if B.answer_caption(lock) == "Door keypad" else ["the keypad's box says %r" % B.answer_caption(lock)]
        if next(l for l in h_room["locks"] if l["id"] == KEYPAD)["instrument"]["label"] == lock["instrument"]["label"]:
            out.append("the pack's keypad label is the room's own")
        if "four digits" not in B.text_of(room_label):
            raise pc.StalePlant("the keypad label control", "the room's keypad label no longer names its length")
        return out + B.instrument_hints([B.answer_caption(l) for l in h_locks])
    results.append(("Heatwave Mutiny's keypad label as printed, the room's own untouched", "control",
                    control_keypad_label, "with_lock_words / answer_caption"))

    # item 9: fixed penalty figures (Amendment 6), strict on the score sheet, penalty-worded on student pages
    for label, kind, text in (("each hint adds 1 minute, on a hints page", "hints", "Each hint adds 1 minute."),
                              ("a 2 minutes penalty, on a cover", "cover", "Wrong answer: 2 minutes penalty"),
                              ("1 minute, on the score sheet", "score", "Penalty: write 1 minute in the box")):
        results.append((label, "plant", lambda kind=kind, text=text: B.fixed_penalties([(kind, text)]), "fixed_penalties"))
    results.append(("time maths on a hints page (Run = 16 − 4 = 12 minutes)", "control",
                    lambda: B.fixed_penalties([("hints", "Run = 16 − 4 = 12 minutes.")]), "fixed_penalties"))
    results.append(("the score sheet as the pack prints it", "control",
                    lambda: B.fixed_penalties([("score", B.text_of("".join(B.score_extras())))]), "fixed_penalties"))
    results.append(("Hamster Heist's own art and hints, every set", "control",
                    lambda: [x for s in sets for x in unit_words_on_art(B, cfg, room, teach, locks, s)],
                    "unit_words_on_art"))

    # ---- FINAL-PADLOCK-FAIR (17 Nov 2026): the 10,000 ceiling, one difficulty per pack, the version in the name ----
    def ceiling(nums, ops, expr):
        form = finalpad.canon(nums, ops)
        return (finalpad.friendly(form),
                [x for x in lockcheck.final_problems("A", list(nums), {"target": int(finalpad.value(form)), "expr": expr},
                                                     shape) if "is above" in x])

    def plant_over_ceiling():
        ok, said = ceiling((1, 10001, 7), ("*", "+"), "1 × 10001 + 7")
        return [] if ok else said                        # caught only when both refuse it
    results.append(("a product of 10,001 (1 x 10001 + 7), in final.py and lockcheck.py", "plant", plant_over_ceiling,
                    "final.friendly / lockcheck.final_problems"))

    def control_at_ceiling():
        ok, said = ceiling((5, 2000, 7), ("*", "+"), "5 × 2000 + 7")
        return ([] if ok else ["final.py refuses 5 x 2000 = 10,000"]) + said
    results.append(("a product of exactly 10,000 (5 x 2000 + 7)", "control", control_at_ceiling,
                    "final.friendly / lockcheck.final_problems"))

    def replaced(the_sets, expr, the_shape, want):
        """The pack's printed padlocks with the last set's expression replaced, judged together (lockcheck), and
        through the build's own verify_finals (filtered to the pack-wide finding)."""
        finals = [(x["letter"], x["final"]["expr"]) for x in the_sets]
        finals[-1] = (finals[-1][0], expr)
        if lockcheck.pack_problems([(x["letter"], x["final"]["expr"]) for x in the_sets], the_shape):
            raise pc.StalePlant("a FINAL-PADLOCK-FAIR plant", "the pack as built is not one difficulty")
        return [x for x in lockcheck.pack_problems(finals, the_shape) if want in x]

    h_shape = heat[1].get("final_shape", finalpad.DEFAULT_SHAPE)
    results.append(("a pack whose sets mix digit signatures (set F 9 x 500 + 1, 1-digit x 3-digit)", "plant",
                    lambda: replaced(sets, "9 × 500 + 1", shape, "not one digit signature"), "lockcheck.pack_problems"))
    results.append(("a pack whose largest product is more than 3 x its smallest (set F 11 x 100 + 1)", "plant",
                    lambda: replaced(sets, "11 × 100 + 1", shape, "more than 3 x"), "lockcheck.pack_problems"))
    results.append(("a plus-and-minus pack whose largest terms differ in digits (Heatwave set F 999 + 31 − 154)",
                    "plant", lambda: replaced(heat[6], "999 + 31 − 154", h_shape, "largest terms differ"),
                    "lockcheck.pack_problems"))

    def control_uniform():
        out = []
        for the_sets, the_shape in ((sets, shape), (heat[6], h_shape)):
            out += lockcheck.pack_problems([(x["letter"], x["final"]["expr"]) for x in the_sets], the_shape)
        if h_shape != "plus-and-minus":
            out.append("Heatwave Mutiny's final_shape is %r, not plus-and-minus" % h_shape)
        return out
    results.append(("Hamster Heist's and Heatwave Mutiny's packs as built (one class each)", "control", control_uniform,
                    "lockcheck.pack_problems"))

    def plant_unversioned_name():
        if B.pdf_name_problems(B.pdf_name(SLUG, cfg), SLUG, cfg):
            return []                                    # the control: the build's own name passes
        return B.pdf_name_problems("%s-pack.pdf" % SLUG, SLUG, cfg)
    results.append(("a PDF name without its version (hamster-heist-pack.pdf)", "plant", plant_unversioned_name,
                    "pdf_name_problems"))
    results.append(("the build's PDF name, %s" % B.pdf_name(SLUG, cfg), "control",
                    lambda: B.pdf_name_problems(B.pdf_name(SLUG, cfg), SLUG, cfg)
                    + ([] if B.pdf_name(SLUG, cfg).endswith("-pack-v%s.pdf" % cfg["pack_version"]) else ["no version"]),
                    "pdf_name / pdf_name_problems"))

    failures = 0
    for name, kind, run, check in results:
        try:
            found, err = run(), None
        except pc.StalePlant as e:
            print(str(e))
            failures += 1
            continue
        except Exception as e:                           # an error is never a catch
            found, err = None, e
        if kind == "plant":
            ok = pc.is_caught(found, err)
            print("%s %s (%s): %s" % ("CAUGHT" if ok else "MISSED", name, check, (found or [err])[0] if (found or err) else "nothing found"))
        else:
            ok = err is None and not found
            print("%s %s (%s)%s" % ("PASSES" if ok else "FAILS", name, check, "" if ok else ": %s" % (found or err)))
        failures += not ok
    plants = sum(1 for r in results if r[1] == "plant")
    controls = len(results) - plants
    print("hamster-heist-pack: %s" % ("%d plants caught, %d controls pass" % (plants, controls) if not failures
                                      else "%d failure(s) of %d plants and %d controls" % (failures, plants, controls)))
    return failures


if __name__ == "__main__":
    status = subprocess.call([sys.executable, "-X", "utf8", BUILD, "--selftest"])
    status = hamster_plants() or status
    sys.exit(1 if status else 0)
