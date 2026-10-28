"""Planted-fault helpers shared by the verifiers (contract STALE-PLANTS, 28 Oct 2026).

A verifier proves its checks still work by planting a fault and requiring the check to catch it. Two shapes let a plant
"pass" without ever running:

  * the plant's target is gone (the text it replaces was reworded, the room it patches is not live, the bank id it edits
    was renamed), so nothing was planted, or the patch threw before it changed anything;
  * the check itself errored, and the error was read as "found something".

Everything here fails the safe way. A plant that did not apply raises StalePlant, which a verifier reports as
"STALE PLANT: <name>" and counts as a FAILURE of the run, never a catch. A catch needs a finding AND no error
(is_caught). bank_common.py is frozen, so this is a separate file; it imports nothing outside the standard library.

    import plant_common as pc

    src2 = pc.apply_plant(src, old, new, name="B25's old pair")                 # str.replace that must change exactly one place
    src2 = pc.apply_re_plant(src, r"\\n  grade: \\d+,", "", name="a lock's grade")  # the same for a regex
    await pc.apply_js(page, name, "COC.BANK[11].explain = ' ';")                # page.evaluate whose failure means a stale target
    caught = pc.is_caught(found, err)                                           # found is non-empty and err is None

New verifiers with planted faults use this file. The existing ones move onto it when next edited (CLAUDE.md lists them).
"""
import re


class StalePlant(Exception):
    """A planted fault that did not apply. str() is "STALE PLANT: <name>: <why>"."""

    def __init__(self, name, why):
        self.name, self.why = name, why
        super().__init__("STALE PLANT: %s: %s" % (name, why))


def apply_plant(src, old, new, name="(unnamed plant)", allow_multiple=False):
    """src with `old` replaced by `new`. Raises StalePlant if `old` is absent, if it appears more than once (unless
    allow_multiple), or if new == old (nothing would change). Replaces every occurrence when allow_multiple."""
    if old == new:
        raise StalePlant(name, "the replacement equals the original, so nothing is planted")
    n = src.count(old)
    if n == 0:
        raise StalePlant(name, "the text to replace is not in the source: %r" % old[:80])
    if n > 1 and not allow_multiple:
        raise StalePlant(name, "the text to replace appears %d times (expected once): %r" % (n, old[:80]))
    return src.replace(old, new)


def apply_re_plant(src, pattern, repl, name="(unnamed plant)", flags=0, count=1):
    """src with the first `count` matches of `pattern` replaced. Raises StalePlant if the pattern matches nothing or
    the result is unchanged."""
    out, n = re.subn(pattern, repl, src, count=count, flags=flags)
    if n == 0:
        raise StalePlant(name, "the pattern matches nothing: %r" % pattern[:80])
    if out == src:
        raise StalePlant(name, "the pattern matched but changed nothing: %r" % pattern[:80])
    return out


async def apply_js(page, name, code):
    """page.evaluate(code) for a plant. Any error while APPLYING it (a missing object, an index out of range, a bank
    id that no longer exists) means the plant's target is stale: StalePlant, not a catch."""
    try:
        return await page.evaluate(code)
    except Exception as exc:
        raise StalePlant(name, "the patch did not apply: %s" % str(exc).splitlines()[0][:120]) from exc


def apply_js_sync(page, name, code):
    """apply_js for Playwright's sync API."""
    try:
        return page.evaluate(code)
    except Exception as exc:
        raise StalePlant(name, "the patch did not apply: %s" % str(exc).splitlines()[0][:120]) from exc


def is_caught(found, err=None):
    """True only if the check found something AND did not error while looking. An error is never a catch."""
    return bool(found) and err is None
