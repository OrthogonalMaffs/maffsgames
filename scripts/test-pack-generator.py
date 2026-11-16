#!/usr/bin/env python3
# ci-line: Pack generator (tools/pack-generator/build_pack.py --selftest: every room with a pack config gets VALID sets, distinct answers per lock and one final-padlock shape, every value recomputed independently; sixty-seven planted faults caught (answers, draws, URL, score sheet, final padlock, penalties, answer-box hints, stakes placement, page-1 length, repeated rules, shape or calculator on a student page, an unfriendly product, DRAFT and approval, a broken caption or caption override, a multi-part clue's broken caption, a clue with no bold part, a caption starting with punctuation, a print override on a red herring, an ungraded lock, a printed unit's scale that is not whole or is wrong, an answer box left in the room's unit, a hint giving a scaled answer in the room's unit only, a cover, certificate or read-outs too long past their last fitting rule, read-outs left on one page, a dark answer box without its white fill, an answer box under 20 mm wide or under 4.5 mm high, a DRAFT pack with a small answer box built with --final, a hint card whose figure is not bound to its unit; multi-part, long-story, longest-story, answer-box and binding controls pass); then this file's HAMSTER-HEIST-PACK plants (a wrong recomputed answer for each Hamster Heist lock, its heat-lamp scale removed, its manual left in the room's unit, a product of two factors of 100 or more in final.py and lockcheck.py, fixed penalty figures on a hints page, a cover and the score sheet; controls: an entity-written and an other-spelling unit each converted, time maths on a hints page); no PDF is ever built in CI) |
# ci-deps: tools/pack-generator/ escape-rooms/ escape-rooms/variants.json scripts/check-escape-rooms.py scripts/escape_set_checks.py scripts/plant_common.py scripts/bank_common.py CNAME
"""CI's entry to the printable-pack generator's self-test (contract PACK-GENERATOR, 4 Nov 2026).

CI finds its lines only in scripts/*.py headers (scripts/ci-groups.py), and the generator lives in tools/pack-generator/,
so this file is the line. It runs `build_pack.py --selftest`, then the plants of contract HAMSTER-HEIST-PACK
(Amendments 1 and 2, 16 Nov 2026), which import the generator and plant faults against The Great Hamster Heist's own
locks, sets and config. Each plant must be caught by the check named beside it; each control must pass. A plant whose
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
