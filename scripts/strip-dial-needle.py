#!/usr/bin/env python3
"""Take the painted needle off a generated instrument image.

    python scripts/strip-dial-needle.py in.jpg docs/art/out.webp

Escape-room instrument art must not contain the moving part: the live needle is
DOM/SVG, and a painted one at any position gives the student two needles the
moment the real one moves (see docs/escape-room-image-prompts.md, rule 3). The
prompts now ask for a bare face, but image models keep drawing one anyway.

What this does: finds the dial face as the largest bright low-saturation disc,
wipes everything inside 80% of its radius (needle, shadow, and any stray mark),
fills the hole from its own edges, and puts a small pivot boss back. Tick marks
sit outside that radius and survive. It also crops the white panel border some
renders arrive in.

Where it works: a needle on a pale, near-uniform face - the compressor gauge in
room C, and most round gauges.

Where it does not: a grey needle on a grey face with a dark arc track that has
to stay, like the sprinkler control. Nothing separates the two automatically.
Reroll those with the current prompt, which asks for no pointer at all.

Always look at the output before filing it.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def crop_panel_border(im):
    """Some renders come matted in a white border with a thin dark frame."""
    g = im.convert("L")
    w, h = im.size
    px = g.load()
    row = lambda y: sum(px[x, y] for x in range(0, w, 8)) / len(range(0, w, 8))
    col = lambda x: sum(px[x, y] for y in range(0, h, 8)) / len(range(0, h, 8))
    try:
        top = next(y for y in range(h // 4) if row(y) < 200)
        bot = next(y for y in range(h - 1, h * 3 // 4, -1) if row(y) < 200)
        left = next(x for x in range(w // 4) if col(x) < 200)
        right = next(x for x in range(w - 1, w * 3 // 4, -1) if col(x) < 200)
    except StopIteration:
        return im
    if top < 4 and left < 4:      # no border, the art runs to the edge
        return im
    return im.crop((left + 20, top + 20, right - 20, bot - 20))


def strip(im):
    a = np.asarray(im).astype(np.float32)
    H, W, _ = a.shape
    bright = (a.min(axis=2) > 175) & ((a.max(axis=2) - a.min(axis=2)) < 45)
    if bright.sum() < 500:
        raise SystemExit("no pale dial face found - is this a dial?")
    ys, xs = np.nonzero(bright)
    cy, cx = int(np.median(ys)), int(np.median(xs))
    rad = int(np.sqrt(bright.sum() / np.pi) * 1.12)

    yy, xx = np.mgrid[0:H, 0:W]
    inner = (yy - cy) ** 2 + (xx - cx) ** 2 <= (0.80 * rad) ** 2
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    mask = inner & ((lum < 200) | (sat > 32))

    out, m = a.copy(), mask.copy()
    while m.any():                       # grow the clean edges inward
        pad = np.pad(out, ((1, 1), (1, 1), (0, 0)), mode="edge")
        padk = np.pad((~m).astype(np.float32), ((1, 1), (1, 1)), mode="edge")
        acc = np.zeros_like(out)
        cnt = np.zeros((H, W, 1), np.float32)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                k = padk[1 + dy:1 + dy + H, 1 + dx:1 + dx + W][..., None]
                acc += pad[1 + dy:1 + dy + H, 1 + dx:1 + dx + W] * k
                cnt += k
        fill = np.where(cnt > 0, acc / np.maximum(cnt, 1), out)
        newly = m & (cnt[:, :, 0] > 0)
        if not newly.any():
            break
        out[newly] = fill[newly]
        m = m & ~newly

    img = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    seam = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    img = Image.composite(img.filter(ImageFilter.GaussianBlur(9)), img, seam)
    r = max(7, rad // 13)
    ImageDraw.Draw(img).ellipse((cx - r, cy - r, cx + r, cy + r),
                                fill=(150, 150, 153), outline=(38, 38, 42), width=max(3, r // 4))
    return img


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    im = strip(crop_panel_border(Image.open(sys.argv[1]).convert("RGB")))
    im.resize((1200, 1200), Image.LANCZOS).save(sys.argv[2], quality=82, method=6)
    print("wrote %s" % sys.argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main())
