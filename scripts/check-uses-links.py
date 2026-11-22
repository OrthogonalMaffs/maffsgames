#!/usr/bin/env python3
# ci-held: fetches external sites, which are flaky (contract WHEN-WILL-I-USE-THIS: never in CI; run by hand, results in the PR)
"""Does every source URL in data/uses.json answer 200? Run by hand, never in CI (external sites are flaky).

    python -X utf8 scripts/check-uses-links.py --live

Each URL is fetched once with GET (some sites refuse HEAD), following redirects, with a generic browser-like
User-Agent and no other identifying header. It prints one line per URL: the status, the final URL when it redirected,
and the scenarios that cite it. Exit 1 if any URL does not end on 200. A 403 or 429 is often a site refusing scripts,
not a dead page: open it in a browser before reporting it. Never replace a URL from this script's output alone: the
contract says report any that 404, don't replace them.
"""
import argparse, json, pathlib, sys, urllib.error, urllib.request

BASE = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/pdf,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            r.read(2048)
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:   # DNS, TLS, timeout: reported as the error, never as a pass
        return "error: %s" % (str(e).splitlines()[0] if str(e) else type(e).__name__), url


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--live", action="store_true", required=True)
    ap.parse_args()
    data = json.loads((BASE / "data" / "uses.json").read_text(encoding="utf-8"))
    cites = {}
    for sc in data["scenarios"]:
        for s in sc["sources"]:
            cites.setdefault(s["url"], []).append(sc["id"])
    bad = 0
    for url, ids in cites.items():
        status, final = fetch(url)
        ok = status == 200
        bad += not ok
        print("%s  %s  %s%s" % (status, url, ", ".join(ids), "" if final == url else "  -> " + final))
    print("%d of %d source URLs answered 200" % (len(cites) - bad, len(cites)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
