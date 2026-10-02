#!/usr/bin/env python3
"""Take the generator's watermark off a downloaded image.

    python scripts/strip-gen-watermark.py in.png docs/art/out.webp
    python scripts/strip-gen-watermark.py --scan 'docs/art/*.webp'

Gemini stamps a small four-pointed sparkle into the bottom-right corner of PNG
downloads. It is not in the picture; it is a mark saying the picture was
generated. Shipping it would be a bad joke given why this pass exists at all
(see the site feedback of 08/09/2026), so nothing gets filed carrying one.

It appeared partway through the art run: the 53 images already in docs/art/ and
the eight scene JPGs are clean, and only PNG downloads from September 2026
onwards carry it. Run this on every PNG before filing regardless -- it is a
no-op on a clean image and says so.

What this does: looks only in the bottom-right corner, finds a compact, bright,
flat-filled blob that is roughly square and concave (a four-pointed star fills
about a third of its own bounding box, where scenery fills most of it), then
fills it by interpolating across the patch and composites that back through a
FEATHERED mask of the mark itself. The feather matters: a hard rectangular
paste leaves a visible seam on a flat wall, which is worse than the mark.

Where it works: the mark on smooth background, which is where it always lands.

Where it does not: a mark sitting over busy detail -- the interpolation has
nothing sensible to fill from. It will say so rather than make a mess.

--at X,Y removes a mark the detector misses. The shape test needs the whole
star to survive thresholding; a soft, low-contrast stamp loses its points first
and is then rejected for not being star-shaped. That is what happened to both
P.E. store pictures on 08/09/2026 -- the mark was plainly visible and scored
k4=0.19 against a required 0.85. Retuning the thresholds is how an earlier
version flagged 30 clean images out of 53, so when you can see the mark, point
at it: --at takes the centre in source pixels and grows the mark from there.

--clone DX,DY fills from elsewhere in the same picture instead of
interpolating. The default fill averages the four edges of the patch across it,
which is right for a mark on a plain wall and wrong for anything with structure
-- on the P.E. store pair it left a visible pale square on a concrete floor and
smeared a painted court line. These backgrounds are repetitive (bare concrete,
herringbone parquet), so copying a patch from (DX,DY) away reconstructs them
exactly. Pick the offset so the source lands on matching texture, and along a
line rather than across it if a line runs through the mark. Use --radius to set
how much is replaced; it wants to be generous enough to take the faint outer
glow, which is what is left behind when the mask is too tight.

--crop X0,Y0,X1,Y1 takes a region before anything else, in source pixels.
Sometimes the cheapest way past the mark is to frame it out: it sits a little
in from the bottom-right, so a crop that clears it costs about 10% of the width
or 19% of the height. Whether that is affordable depends on what is in the
strip you lose -- on the P.E. failure picture the right-hand strip is the coat
the whole picture is about, so that one had to lose its floor and its left edge
instead. Look before choosing a side.

--frame WxH crops to that aspect ratio before resizing, so sources of different
shapes all come out on the house frame. Gemini does not always return the same
aspect: the P.E. store scene came back 2816x1536 and its failure and victory
pictures 2752x1536, which silently filed them 20px taller than every other
image on the site.

--scan reports without writing, so a folder can be checked in one go.

Always look at the output before filing it.
"""
import glob
import sys

import numpy as np
from PIL import Image, ImageFilter

# The mark sits at a fixed inset from the bottom-right corner. Searching a
# window rather than the whole frame is what keeps a lamp or a window out of it.
WINDOW = (0.84, 0.72, 1.0, 1.0)


def components(mask):
    """Connected components, 4-connected. No scipy on the Windows machine."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    out, cur = [], 0
    for sy, sx in zip(*np.nonzero(mask)):
        if lab[sy, sx]:
            continue
        cur += 1
        stack, pix = [(sy, sx)], []
        lab[sy, sx] = cur
        while stack:
            y, x = stack.pop()
            pix.append((y, x))
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = cur
                    stack.append((ny, nx))
        out.append(np.array(pix))
    return out


def four_fold(pix):
    """How strongly a blob's outline repeats every 90 degrees.

    This is what separates the mark from scenery. A four-pointed star's radius,
    swept round its centroid, peaks four times at right angles and dips sharply
    between; a bright window or a lamp does no such thing. Returns (ratio of the
    4th harmonic to the rest, longest radius over shortest), or None.
    """
    ys, xs = pix[:, 0].astype(float), pix[:, 1].astype(float)
    cy, cx = ys.mean(), xs.mean()
    ang = np.arctan2(ys - cy, xs - cx)
    rad = np.hypot(ys - cy, xs - cx)
    bins = 72
    idx = ((ang + np.pi) / (2 * np.pi) * bins).astype(int) % bins
    prof = np.zeros(bins)
    for i in range(bins):
        m = idx == i
        if not m.any():
            return None
        prof[i] = rad[m].max()
    if prof.min() <= 0:
        return None
    p = prof / prof.mean()
    f = np.abs(np.fft.rfft(p - p.mean()))
    return float(f[4] / (np.sum(f[1:12]) - f[4] + 1e-9)), float(prof.max() / prof.min())


def find_mark(im):
    """Return (bbox, full-frame boolean mask) for the sparkle, or (None, None)."""
    w, h = im.size
    x0, y0 = int(w * WINDOW[0]), int(h * WINDOW[1])
    x1, y1 = int(w * WINDOW[2]), int(h * WINDOW[3])
    crop = im.crop((x0, y0, x1, y1)).convert("L")
    reg = np.asarray(crop).astype(float)
    bg = np.asarray(crop.filter(ImageFilter.GaussianBlur(30))).astype(float)
    lit = (reg - bg) > 16

    # the mark scales with the frame; allow a generous band either side
    lo, hi = w * 0.015, w * 0.06
    best = None
    for pix in components(lit):
        ys, xs = pix[:, 0], pix[:, 1]
        bw, bh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        if not (lo < bw < hi and lo < bh < hi):
            continue
        if not 0.7 < bw / float(bh) < 1.4:          # a star is near square
            continue
        fill = len(pix) / float(bw * bh)
        if not 0.2 < fill < 0.62:                    # concave: points, not a slab
            continue
        vals = reg[ys, xs]
        if vals.std() > 26:                          # flat colour, not texture
            continue
        sym = four_fold(pix)
        if sym is None:
            continue
        k4, peak = sym
        if k4 < 0.85 or not 1.6 < peak < 3.2:        # the shape test; see above
            continue
        score = len(pix)
        if best is None or score > best[0]:
            best = (score, (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()), pix)

    if best is None:
        return None, None
    _, bbox, pix = best
    full = np.zeros((h, w), bool)
    full[pix[:, 0] + y0, pix[:, 1] + x0] = True
    return bbox, full


def strip(im, bbox, mark, pad=16, feather=9):
    a = np.asarray(im.convert("RGB")).astype(float)
    H, W = a.shape[:2]
    l, t, r, b = bbox
    l, t = max(l - pad, 1), max(t - pad, 1)
    r, b = min(r + pad, W - 2), min(b + pad, H - 2)

    fill = a.copy()
    left, right = a[t:b + 1, l - 1][:, None, :], a[t:b + 1, r + 1][:, None, :]
    wx = np.linspace(0, 1, r - l + 1)[None, :, None]
    top, bot = a[t - 1, l:r + 1][None, :, :], a[b + 1, l:r + 1][None, :, :]
    wy = np.linspace(0, 1, b - t + 1)[:, None, None]
    fill[t:b + 1, l:r + 1] = (left * (1 - wx) + right * wx + top * (1 - wy) + bot * wy) / 2

    soft = Image.fromarray((mark * 255).astype("uint8"))
    soft = soft.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(feather))
    m = np.clip(np.asarray(soft).astype(float) / 255.0 * 1.9, 0, 1)[:, :, None]
    return Image.fromarray((a * (1 - m) + fill * m).round().clip(0, 255).astype("uint8"))


def mark_at(im, cx, cy):
    """Grow the mark outward from a point the operator can see.

    No shape test and no symmetry test -- those are what the automatic path
    uses to avoid false positives, and they are unnecessary once a person has
    said where the mark is. The disc clamp matters: on the victory picture the
    mark sits on a painted court line, and without it the lit region runs away
    down the line and takes half the floor with it.
    """
    w, h = im.size
    reach = max(int(w * 0.035), 40)
    l, t = max(cx - reach, 0), max(cy - reach, 0)
    r, b = min(cx + reach, w), min(cy + reach, h)
    crop = im.crop((l, t, r, b)).convert("L")
    reg = np.asarray(crop).astype(float)
    bg = np.asarray(crop.filter(ImageFilter.GaussianBlur(30))).astype(float)
    diff = reg - bg

    py, px = cy - t, cx - l
    seed = diff[max(py - 6, 0):py + 7, max(px - 6, 0):px + 7].max()
    if seed < 6:
        return None, None

    # everything a third as bright as the core, so the faint tips come too
    lit = diff > max(seed * 0.33, 5)

    # clamp to a disc so a bright line through the mark cannot drag it away
    yy, xx = np.mgrid[0:lit.shape[0], 0:lit.shape[1]]
    lit &= (yy - py) ** 2 + (xx - px) ** 2 <= (reach * 0.7) ** 2

    best, bd = None, None
    for pix in components(lit):
        d = np.hypot(pix[:, 0].mean() - py, pix[:, 1].mean() - px)
        if bd is None or d < bd:
            best, bd = pix, d
    if best is None or bd > reach * 0.5:
        return None, None

    full = np.zeros((h, w), bool)
    full[best[:, 0] + t, best[:, 1] + l] = True
    return (l + best[:, 1].min(), t + best[:, 0].min(),
            l + best[:, 1].max(), t + best[:, 0].max()), full


def clone_patch(im, cx, cy, dx, dy, radius, feather=11):
    """Replace a disc around (cx,cy) with the same disc taken from (dx,dy) away.

    A disc rather than the detected blob, because the mark's faint outer glow
    never survives thresholding and a tight mask leaves a halo behind. On a
    repeating background a generous disc costs nothing.
    """
    a = np.asarray(im.convert("RGB")).astype(float)
    H, W = a.shape[:2]
    if not (0 <= cx + dx < W and 0 <= cy + dy < H):
        return None
    src = np.roll(np.roll(a, -dy, axis=0), -dx, axis=1)

    yy, xx = np.mgrid[0:H, 0:W]
    disc = ((yy - cy) ** 2 + (xx - cx) ** 2 <= radius ** 2)
    soft = Image.fromarray((disc * 255).astype("uint8")).filter(
        ImageFilter.GaussianBlur(feather))
    m = (np.asarray(soft).astype(float) / 255.0)[:, :, None]
    return Image.fromarray((a * (1 - m) + src * m).round().clip(0, 255).astype("uint8"))


def busy(im, bbox):
    """True if the ring around the mark has too much detail to fill from."""
    l, t, r, b = bbox
    pad = 30
    ring = im.convert("L").crop((max(l - pad, 0), max(t - pad, 0),
                                 min(r + pad, im.size[0]), min(b + pad, im.size[1])))
    return np.asarray(ring).astype(float).std() > 34


def main():
    args = sys.argv[1:]
    if args and args[0] == "--scan":
        files = []
        for pat in args[1:]:
            files.extend(sorted(glob.glob(pat)))
        marked = 0
        for f in files:
            bbox, _ = find_mark(Image.open(f))
            if bbox:
                marked += 1
                print("MARK  %s  at %s" % (f, bbox))
        print("\n%d marked, %d clean, %d scanned" % (marked, len(files) - marked, len(files)))
        return 0

    width = None
    if "--width" in args:
        i = args.index("--width")
        width = int(args[i + 1])
        args = args[:i] + args[i + 2:]

    crop = None
    if "--crop" in args:
        i = args.index("--crop")
        crop = tuple(int(v) for v in args[i + 1].split(","))
        args = args[:i] + args[i + 2:]

    frame = None
    if "--frame" in args:
        i = args.index("--frame")
        fw, fh = args[i + 1].lower().split("x")
        frame = (int(fw), int(fh))
        args = args[:i] + args[i + 2:]

    clone = None
    if "--clone" in args:
        i = args.index("--clone")
        dx, dy = args[i + 1].split(",")
        clone = (int(dx), int(dy))
        args = args[:i] + args[i + 2:]

    radius = 55
    if "--radius" in args:
        i = args.index("--radius")
        radius = int(args[i + 1])
        args = args[:i] + args[i + 2:]

    at = None
    if "--at" in args:
        i = args.index("--at")
        ax, ay = args[i + 1].split(",")
        at = (int(ax), int(ay))
        args = args[:i] + args[i + 2:]

    if len(args) != 2:
        print(__doc__)
        return 2

    src, dst = args
    im = Image.open(src)
    if crop:
        im = im.crop(crop)
        print("%s: cropped to %s -> %sx%s" % (src, crop, im.size[0], im.size[1]))
    if at and clone:
        out = clone_patch(im, at[0], at[1], clone[0], clone[1], radius)
        if out is None:
            print("%s: clone offset %s falls outside the image" % (src, clone))
            return 1
        print("%s: disc r=%d at %s cloned from %s away" % (src, radius, at, clone))
        im = out
    elif at:
        bbox, mark = mark_at(im, at[0], at[1])
        if bbox is None:
            print("%s: nothing to remove at %s -- give the centre in source "
                  "pixels, not coordinates read off a resized copy." % (src, at))
            return 1
        if busy(im, bbox):
            print("%s: WARNING -- the mark at %s sits over detail. The fill "
                  "interpolates across the patch, so on an edge or a line it "
                  "leaves a visible smudge. Look at the output; a JPG download "
                  "of the same image carries no mark at all and is the cheaper "
                  "fix." % (src, bbox))
        print("%s: mark at %s removed (pointed at %s)" % (src, bbox, at))
        im = strip(im, bbox, mark)
    else:
        bbox, mark = find_mark(im)
        if bbox is None:
            print("%s: no watermark found" % src)
        elif busy(im, bbox):
            print("%s: watermark at %s sits over busy detail -- not filled. "
                  "Fix it by hand or reroll." % (src, bbox))
            return 1
        else:
            print("%s: watermark at %s removed" % (src, bbox))
            im = strip(im, bbox, mark)

    if frame:
        fw, fh = frame
        w, h = im.size
        want = fw / float(fh)
        if abs(w / float(h) - want) > 1e-4:
            if w / float(h) > want:                 # too wide: trim the sides
                nw = int(round(h * want))
                off = (w - nw) // 2
                im = im.crop((off, 0, off + nw, h))
            else:                                   # too tall: trim top/bottom
                nh = int(round(w / want))
                off = (h - nh) // 2
                im = im.crop((0, off, w, off + nh))
            print("  cropped %sx%s -> %sx%s for the %sx%s frame"
                  % (w, h, im.size[0], im.size[1], fw, fh))
        im = im.convert("RGB").resize((fw, fh), Image.LANCZOS)
    elif width:
        h = int(round(im.size[1] * width / float(im.size[0])))
        im = im.convert("RGB").resize((width, h), Image.LANCZOS)

    if dst.lower().endswith(".webp"):
        im.convert("RGB").save(dst, "WEBP", quality=80)
    else:
        im.save(dst)
    print("  written %s  %sx%s" % (dst, im.size[0], im.size[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
