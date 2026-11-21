#!/usr/bin/env python3
"""Some Thingies question bank generator (Project Claude, 21 Nov 2026). Deterministic: no randomness.
Tables: main 2, 5, 10 (Year 2); pro 3, 4, 8 (Year 3). Every value is computed here; nothing typed."""
import json, hashlib, sys

TABLES = {"main": (2, 5, 10), "pro": (3, 4, 8)}
PIC_CAP = 50          # most thingies drawn in one picture
SUM_TERMS_MAX = 6     # longest repeated addition shown (fits 360 px)

def uniq_opts(answer, cands):
    out = []
    for c in cands:
        if isinstance(c, int) and c > 0 and c != answer and c not in out:
            out.append(c)
    return out

def num_options(answer, cands, fill):
    d = uniq_opts(answer, cands)
    k = 1
    while len(d) < 3:                       # pad with nearest unused numbers, deterministic
        for c in (answer + k, answer - k):
            if c > 0 and c != answer and c not in d and len(d) < 3:
                d.append(c)
        k += 1
    return d[:3]

def bank():
    items = []
    for mode, T in TABLES.items():
        p = "m" if mode == "main" else "p"
        # Stage 1: equal groups. g groups of n thingies -> how many altogether?
        for n in T:
            for g in range(2, 11):
                if n * g > PIC_CAP: continue
                a = n * g
                items.append({"id": f"{p}1-{g}x{n}", "mode": mode, "stage": 1, "type": "groups",
                              "groups": g, "each": n, "answer": a,
                              "decoys": num_options(a, [g + n, n * (g + 1), n * (g - 1)], None),
                              "say": f"{g} groups of {n}"})
        # Stage 2a: repeated addition -> total and how many lots. 2b: groups -> matching sum.
        for n in T:
            for g in range(2, SUM_TERMS_MAX + 1):
                if n * g > PIC_CAP: continue
                a = n * g
                items.append({"id": f"{p}2a-{g}x{n}", "mode": mode, "stage": 2, "type": "sum-to-groups",
                              "sum": [n] * g, "groups": g, "each": n, "answer": a,
                              "groups_decoys": uniq_opts(g, [n, g + 1, g - 1])[:2],
                              "decoys": num_options(a, [g + n, n * (g + 1), n * (g - 1)], None)})
                # Decoys: one group too many, one too few (or each one bigger), and adding the two numbers.
                # Never "n groups of g": it has the same total, so it isn't wrong.
                dec = []
                for t in ([n] * (g + 1) if g + 1 <= SUM_TERMS_MAX else [n + 1] * g,
                          [n] * (g - 1) if g > 2 else [n + 2] * g,
                          [g, n] if g != n else [g + 1, n]):
                    if t != [n] * g and t not in dec: dec.append(t)
                items.append({"id": f"{p}2b-{g}x{n}", "mode": mode, "stage": 2, "type": "groups-to-sum",
                              "groups": g, "each": n, "answer_sum": [n] * g, "decoy_sums": dec[:3]})
        # Stage 3: arrays, r rows of c dots, one factor from the table.
        seen = set()
        for n in T:
            for k in range(2, 11):
                for r, c in ((k, n), (n, k)):
                    if r * c > PIC_CAP or (r, c) in seen or c > 10: continue
                    seen.add((r, c)); a = r * c
                    items.append({"id": f"{p}3-{r}r{c}c", "mode": mode, "stage": 3, "type": "array",
                                  "rows": r, "cols": c, "answer": a,
                                  "decoys": num_options(a, [r + c, a + c, a - c, a + r], None)})
        # Stage 4: facts, both orders and the missing factor, multipliers 1 to 12.
        seen = set()
        for n in T:
            for m in range(1, 13):
                a = m * n
                for x, y in ((m, n), (n, m)):
                    if (x, y) in seen: continue
                    seen.add((x, y))
                    items.append({"id": f"{p}4-{x}x{y}", "mode": mode, "stage": 4, "type": "fact",
                                  "a": x, "b": y, "answer": a,
                                  "decoys": num_options(a, [a + n, a - n, m + n], None)})
                if m >= 2:
                    items.append({"id": f"{p}4-q{m}x{n}", "mode": mode, "stage": 4, "type": "missing",
                                  "b": n, "product": a, "answer": m,
                                  "decoys": num_options(m, [m + 1, m - 1, a - n if a - n != m else n], None)})
    return items

def check(items):
    ids = [i["id"] for i in items]; assert len(ids) == len(set(ids)), "duplicate ids"
    for i in items:
        t = i["type"]
        if t in ("groups", "sum-to-groups"): assert i["answer"] == i["groups"] * i["each"] == sum([i["each"]] * i["groups"])
        if t == "sum-to-groups": assert sum(i["sum"]) == i["answer"] and len(i["sum"]) == i["groups"]
        if t == "groups-to-sum":
            assert sum(i["answer_sum"]) == i["groups"] * i["each"] and len(i["decoy_sums"]) == 3
            for d in i["decoy_sums"]: assert d != i["answer_sum"]
        if t == "array": assert i["answer"] == i["rows"] * i["cols"] <= PIC_CAP
        if t == "fact": assert i["answer"] == i["a"] * i["b"]
        if t == "missing": assert i["answer"] * i["b"] == i["product"]
        if "decoys" in i:
            assert len(i["decoys"]) == 3 and i["answer"] not in i["decoys"] and len(set(i["decoys"])) == 3 and min(i["decoys"]) > 0, i
    return True

if __name__ == "__main__":
    items = bank(); check(items)
    from collections import Counter
    c = Counter((i["mode"], i["stage"]) for i in items)
    for k in sorted(c): print(k, c[k])
    print("total", len(items))
    blob = "".join(json.dumps(i, separators=(",", ":")) + "\n" for i in items)
    print("sha256", hashlib.sha256(blob.encode()).hexdigest())
    if "--out" in sys.argv: open(sys.argv[sys.argv.index("--out") + 1], "w", newline="\n").write(blob)
