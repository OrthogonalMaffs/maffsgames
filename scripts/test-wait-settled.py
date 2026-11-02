#!/usr/bin/env python3
# ci-line: Shared settle (bank_common.wait_settled: a page with a late font measured after fonts.ready and settled layout; the premature read is the race, an element truly off screen still fails) |
"""bank_common.wait_settled / settle_js: the one place a verifier waits for fonts and layout before it measures (Jon, 27 Oct 2026).

Two red mains (#566; run 40529609805) came from measuring a page the instant its feedback appeared, while a late font was still about to
grow it. wait_settled() waits for document.fonts.ready, then for two frames and a quiet period, repeating while a font is still loading.

    python scripts/test-wait-settled.py

Three pages, each with a font that arrives 900 ms late and makes the text bigger (size-adjust), and a Next button below the text, on a
375 x 300 screen:
  A  the button is on screen before the font and after it             settled: on screen   (passes)
  B  the button is off screen before the font and after it            settled: off screen  (fails, as it must: genuinely off screen)
  C  the button is on screen before the font, off screen after it     read at once: on screen (the race); settled: off screen (the truth)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

FONT = os.path.join(bc.ROOT, "scripts", "fonts", "katex", "fonts", "KaTeX_Main-Regular.woff2")
DELAY_MS = 900


def page_html(words):
    text = " ".join(["word"] * words)
    return ("<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><style>"
            "@font-face{font-family:Late;src:url(/late.woff2) format('woff2');size-adjust:220%;font-display:swap}"
            "body{margin:0}p{font:16px Late,serif;margin:0;padding:8px}button{display:block;margin:8px;height:40px}</style>"
            "<p>" + text + "</p><button id=next>Next</button>")


def fonts_path():
    if os.path.isfile(FONT):
        return FONT
    for d, _, names in os.walk(os.path.join(bc.ROOT, "scripts", "fonts")):
        for n in names:
            if n.endswith(".woff2"):
                return os.path.join(d, n)
    raise SystemExit("test-wait-settled: no .woff2 under scripts/fonts to serve as the late font")


def read(page):
    return page.evaluate("() => { const r = document.getElementById('next').getBoundingClientRect(); return { bottom: Math.round(r.bottom), vh: innerHeight }; }")


def run():
    from playwright.sync_api import sync_playwright
    import time
    font_bytes = open(fonts_path(), "rb").read()
    results = []

    import http.server
    import threading

    def serve(words):
        body = page_html(words).encode("utf-8")

        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path.endswith("/late.woff2"):
                    time.sleep(DELAY_MS / 1000.0)          # this thread only: the page keeps rendering meanwhile
                    data, kind = font_bytes, "font/woff2"
                else:
                    data, kind = body, "text/html; charset=utf-8"
                self.send_response(200)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *a):
                pass
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        return srv

    def case(pw, name, words):
        srv = serve(words)
        br = pw.chromium.launch()
        ctx = br.new_context(viewport={"width": 375, "height": 300})
        page = ctx.new_page()
        page.goto("http://127.0.0.1:%d/" % srv.server_address[1], wait_until="domcontentloaded")
        page.wait_for_selector("#next")
        early = read(page)
        bc.wait_settled(page)
        late = read(page)
        br.close()
        srv.shutdown()
        return early, late

    with sync_playwright() as pw:
        ea, la = case(pw, "A", 6)
        eb, lb = case(pw, "B", 140)
        ec, lc = case(pw, "C", 85)
    on = lambda m: m["bottom"] <= m["vh"]
    results.append(("A: on screen before and after the late font; passes once settled", on(ea) and on(la), (ea, la)))
    results.append(("B: genuinely off screen; fails once settled (and at once)", (not on(lb)) and (not on(eb)), (eb, lb)))
    results.append(("C: on screen at once (the race), off screen once settled (the truth)", on(ec) and not on(lc), (ec, lc)))
    ok = True
    for name, good, detail in results:
        print("%s  %s  %s" % ("ok  " if good else "FAIL", name, detail))
        ok &= good
    return ok


def main():
    try:
        ok = run()
    except Exception as exc:                       # a crash is a failure, never a pass
        print("FAIL  test-wait-settled stopped: %s: %s" % (type(exc).__name__, exc))
        return 1
    print("PASS" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
