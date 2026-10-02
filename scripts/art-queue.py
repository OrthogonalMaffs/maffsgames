#!/usr/bin/env python3
"""Rewrite the header of docs/escape-room-image-prompts.md from its own contents.

    python scripts/art-queue.py

The file is a queue: a prompt sits in it until the image is made, then the
prompt is deleted. That means the count, the per-room state and the "next three"
can all be derived rather than maintained by hand - and hand-maintained status
drifts the moment two edits happen in a row.

Reads the `### `name`` blocks left under each `# X. Room` heading, and rewrites
the count line, the Next three list and the Where each room is table in place.
Everything else is left alone.
"""
import re
import sys

DOC = "docs/escape-room-image-prompts.md"
PER_ROOM = 6   # establishing shot, three instruments, a failure, a victory


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DOC
    with open(path, encoding="utf-8") as f:
        s = f.read()

    body = s[s.index("\n# ", s.index("## Four checks")):]
    rooms = []                      # [(letter, title, [remaining files])]
    for m in re.finditer(r"^# ([A-J])\. (.+?)$", body, re.M):
        end = body.find("\n# ", m.end())
        chunk = body[m.end():end if end != -1 else len(body)]
        if chunk.lstrip().startswith("Appendix"):
            continue
        files = re.findall(r"^### `([^`]+)`", chunk, re.M)
        rooms.append((m.group(1), m.group(2), files))

    # rooms whose prompts have all gone are complete, and drop out of the body
    titles = dict((l, t) for l, t, _ in rooms)
    left = dict((l, f) for l, _, f in rooms)
    all_letters = sorted(set(list(titles) + re.findall(r"^\| \*\*([A-J])\*\*", s, re.M)))

    total = sum(len(v) for v in left.values())
    nxt = ["%s · `%s`" % (l, f) for l in all_letters for f in left.get(l, [])][:3]

    rows = []
    for l in all_letters:
        title = titles.get(l) or re.search(r"^\| \*\*%s\*\* — (.+?) \|" % l, s, re.M).group(1)
        files = left.get(l, [])
        if not files:
            state = "**complete**"
        else:
            state = "%d of %d done — still to do: %s" % (
                PER_ROOM - len(files), PER_ROOM, ", ".join("`%s`" % f for f in files))
        rows.append("| **%s** — %s | %s |" % (l, title, state))

    s = re.sub(r"\*\*\d+ images left\.\*\*", "**%d images left.**" % total, s, count=1)
    # Replace whatever sits under the heading, numbered list or sentence. A
    # list-only pattern stopped matching the moment the section was hand-edited
    # to "Nothing. The set is complete.", and it then sat stale through three runs.
    body = "".join("%d. %s\n" % (i, n) for i, n in enumerate(nxt, 1)) or "Nothing. The set is complete.\n"
    s = re.sub(r"(## Next three\n\n).*?(\n## )",
               lambda m: m.group(1) + body + m.group(2),
               s, count=1, flags=re.S)
    s = re.sub(r"(## Where each room is\n\n\| Room \| State \|\n\|---\|---\|\n)(?:\|.*\n)+",
               lambda m: m.group(1) + "\n".join(rows) + "\n", s, count=1)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("%d images left; next: %s" % (total, ", ".join(nxt) or "nothing"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
