#!/usr/bin/env python3
# ci-line: Escape-room search order and herrings (every live room shows the note and treats a searched herring like a clue; Chromium checks shuffled positions over 60 plays, refresh persistence, replay and an old save without order) |
# ci-deps: escape-rooms/ scripts/check-teacher-invite.py
"""Browser check for saved object order and notebook treatment in the shared escape engine."""
import importlib.util
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("teacher_invite", ROOT / "scripts" / "check-teacher-invite.py")
ti = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ti)
LINE = "Not every note will help you. Part of the puzzle is working out which ones do."


def live_rooms():
    for room in sorted((ROOT / "escape-rooms").iterdir()):
        if (room / "room.js").exists() and "noindex" not in (room / "index.html").read_text(encoding="utf-8"):
            yield room.name, "play.html" if (room / "play.html").exists() else ""


def order(page):
    return page.locator("#objects [data-obj]").evaluate_all("nodes => nodes.map(n => n.dataset.obj)")


def main():
    faults = []
    proc, base = ti._serve(ROOT)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            ctx = browser.new_context()
            page = ctx.new_page()
            for slug, path in live_rooms():
                page.goto(f"{base}/escape-rooms/{slug}/{path}?cb=order", wait_until="load")
                page.evaluate("localStorage.clear()")
                page.reload(wait_until="load")
                page.locator("#startBtn").click()
                if LINE not in page.locator("#scrPlay").inner_text():
                    faults.append(f"{slug}: room note missing")
                herring = page.evaluate("() => ROOM.objects.find(o => !o.clue && o.flavour)")
                clue = page.evaluate("() => ROOM.objects.find(o => o.clue)")
                if not herring or not clue:
                    faults.append(f"{slug}: missing herring or clue fixture")
                    continue
                page.locator(f'#objects [data-obj="{herring["id"]}"]').click()
                btn = page.locator(f'#objects [data-obj="{herring["id"]}"]')
                if "found something" not in btn.inner_text() or "empty" in (btn.get_attribute("class") or ""):
                    faults.append(f"{slug}: herring button gives itself away")
                if "got" not in (page.locator("#searchOut").get_attribute("class") or ""):
                    faults.append(f"{slug}: herring search result uses a different style")
                if herring["name"] not in (page.locator("#notebook").text_content() or ""):
                    faults.append(f"{slug}: herring missing from notebook")
                body = page.evaluate("name => document.querySelector('#searchOut').textContent.slice(name.length)", herring["name"])
                if not body.strip() or body not in (page.locator("#notebook").text_content() or ""):
                    faults.append(f"{slug}: herring flavour missing from notebook")
                page.locator(f'#objects [data-obj="{clue["id"]}"]').click()
                if page.locator("#notebook .clue").count() != 2:
                    faults.append(f"{slug}: clue and herring are not styled alike")
                expected = [obj for obj in order(page) if obj in (herring["id"], clue["id"])]
                got = page.locator("#notebook .clue").evaluate_all(
                    "nodes => nodes.map(n => n.querySelector('.clue-src').textContent)")
                names = page.evaluate("() => Object.fromEntries(ROOM.objects.map(o => [o.id, o.name]))")
                if got != [names[obj] for obj in expected]:
                    faults.append(f"{slug}: notebook does not follow room order")
                page.goto(f"{base}/escape-rooms/{slug}/teacher.html?cb=order", wait_until="load")
                if "Students are told: " + LINE not in page.locator("body").inner_text():
                    faults.append(f"{slug}: teacher note missing")

            slug, path = "rightful-king", ""
            url = f"{base}/escape-rooms/{slug}/{path}?cb=order"
            page.goto(url, wait_until="load")
            page.evaluate("localStorage.clear()")
            seen = set()
            positions = {}
            for _ in range(60):
                page.reload(wait_until="load")
                page.locator("#startBtn").click()
                ids = order(page)
                seen.add(tuple(ids))
                herrings = page.evaluate("() => ROOM.objects.filter(o => !o.clue).map(o => o.id)")
                for i, obj in enumerate(ids):
                    positions.setdefault(i, set()).add(obj in herrings)
            if len(seen) < 2 or any(values != {True, False} for values in positions.values()):
                faults.append(f"{slug}: object position predicts a herring across 60 plays")
            before = order(page)
            page.reload(wait_until="load")
            page.locator("#resumeBtn").click()
            if order(page) != before:
                faults.append(f"{slug}: order changed on refresh")
            page.evaluate("() => { const k = 'mfg_escape_' + ROOM.slug; const s = JSON.parse(localStorage.getItem(k)); delete s.order; localStorage.setItem(k, JSON.stringify(s)); }")
            page.reload(wait_until="load")
            page.locator("#resumeBtn").click()
            saved = page.evaluate("() => JSON.parse(localStorage.getItem('mfg_escape_' + ROOM.slug)).order")
            if sorted(saved) != sorted(order(page)):
                faults.append(f"{slug}: old save did not get a saved order")
            page.reload(wait_until="load")
            page.locator("#resumeBtn").click()
            if order(page) != saved:
                faults.append(f"{slug}: migrated order did not survive refresh")
            for _ in range(100):
                if page.locator("#scrEnd").get_attribute("class") == "screen active":
                    break
                page.evaluate(ti.ROOM_STEP + "(true)")
                page.wait_for_timeout(40)
            if page.locator("#scrEnd").get_attribute("class") != "screen active":
                faults.append(f"{slug}: play-through did not reach Play again")
            else:
                replay_orders = []
                for _ in range(3):
                    page.locator("#againBtn").click()
                    replay_orders.append(order(page))
                    for _ in range(100):
                        if page.locator("#scrEnd").get_attribute("class") == "screen active":
                            break
                        page.evaluate(ti.ROOM_STEP + "(true)")
                        page.wait_for_timeout(40)
                if all(item == saved for item in replay_orders):
                    faults.append(f"{slug}: Play again never changed the order")
            browser.close()
    finally:
        proc.terminate()
        proc.wait(timeout=10)
    print(f"escape order: {len(list(live_rooms()))} live rooms, 60 plays, {len(faults)} faults")
    for fault in faults:
        print("  - " + fault)
    return bool(faults)


if __name__ == "__main__":
    raise SystemExit(main())
