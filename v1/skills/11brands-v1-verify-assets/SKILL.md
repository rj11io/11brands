---
name: 11brands-v1-verify-assets
description: Check generated assets in 11brands v1 — compare two runs, verify every pixel is a blend of the brand's own colours, and check icon integrity. Use when someone asks whether output matches, is correct, has drifted, or reproduces an earlier run; or when a config or script changed and the effect needs measuring.
---

# Verify brand assets (v1)

Never answer by looking at an image. Every question here is a measurement.
Work in `v1/`; ignore `v0/` — it is deprecated.

Take colours from the run's `MANIFEST.md` or the brand's `config.json`, never by
retyping them.

## Question 0: did the config change, or did the code?

If two runs of the same brand differ, compare the manifests first — palette,
text, font, and the layout-diff table are all recorded there. One `diff` usually
explains everything before a single pixel is compared.

## Comparing two runs

Bytes first:

```python
from pathlib import Path
from PIL import Image, ImageChops

def compare(a: Path, b: Path) -> str:
    if a.read_bytes() == b.read_bytes():
        return "identical bytes"
    ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    if ia.size != ib.size:
        return f"different size {ia.size} vs {ib.size}"
    diff = ImageChops.difference(ia, ib)
    if diff.getbbox() is None:
        return "identical pixels, different encoding"
    px = diff.load()
    w, h = ia.size
    n = sum(1 for y in range(h) for x in range(w) if px[x, y] != (0, 0, 0))
    return f"{n} px differ, bbox {diff.getbbox()}"
```

When something differs, say **where**, not just how much. Card regions at the
default layout: masthead `y 20..80`, mark `y 42..392`, main row `y 455..525`,
footer `y 560..590`. "Only the mark differs" is a diagnosis; a bare pixel count
is not. Likely causes by shape:

- **mark only** — mark master or `mark_crop`/`mark_size` changed
- **one text region entirely** — a text field changed or went null; check the
  manifests before calling it a bug
- **everything, slightly** — a different font (or `.ttc` index), or Pillow
  version changed
- **one region's colour** — the config's palette changed

## Is the output correct in itself?

Every pixel of the mark and icons must be a blend the drawing code can actually
produce. Ask it as a forward question — enumerate everything `compose()` can
emit, then subtract. Coverage comes from two 8-bit masks, so the pairs are
exactly `k/255`, plus a renormalised branch when they sum past 1:

```python
def emittable(ground, ink, signal):
    """Every colour compose() can produce. 65,536 pairs; just enumerate."""
    out = set()
    for a in range(256):
        for b in range(256 - a):
            i, s = a / 255, b / 255
            out.add(tuple(round(ground[c]*(1-i-s) + ink[c]*i + signal[c]*s)
                          for c in range(3)))
    for a in range(256):
        for b in range(256):
            if a + b <= 255:
                continue
            t = (a + b) / 255
            i, s = (a/255)/t, (b/255)/t
            out.add(tuple(round(ground[c]*(1-i-s) + ink[c]*i + signal[c]*s)
                          for c in range(3)))
    return out

def artefacts(paths, ground, ink, signal):
    ok = emittable(ground, ink, signal)
    seen = set()
    for p in paths:
        seen |= set(Image.open(p).convert("RGB").get_flattened_data())
    return sorted(seen - ok)
```

Rules learned the hard way:

- **Enumerate; never search coverage on a step grid.** A grid that misses the
  true `k/255` value reports phantom artefacts — a `step=0.002` version once
  invented them in nine brands out of ten.
- **Do not use an inverse (solve-for-coefficients) test.** It needs a tolerance,
  and a near-neutral signal collapses the colour triangle to a sliver where one
  bit of rounding exceeds any sane tolerance. The forward test has nothing to
  tune.
- **Work on `set(...)` of distinct colours** (~300), never per pixel (~756,000).

### Text regions are drawn in a fourth colour

The footer and masthead use `colors.footer`, not the mark's three. If artefacts
appear only in text regions, check whether the footer colour is a true blend of
ground and ink:

```python
ts = [(footer[c]-ground[c])/(ink[c]-ground[c]) for c in range(3) if ink[c] != ground[c]]
# max(ts)-min(ts) near zero => on the line; text anti-aliasing stays in gamut
```

A footer off that line (e.g. a cool grey on a warm ground) makes every
anti-aliased text pixel an out-of-triangle blend. That is a palette
inconsistency; the fix is the config, not the code.

## Icons

Every `.ico` frame must be RGBA — a palette frame breaks a Next.js build:

```python
im = Image.open(path)
for size in sorted(im.ico.sizes()):
    assert im.ico.getimage(size).mode == "RGBA", size
```

The 16px signal square: recover coverage and count pixels at >= 90% signal — do
NOT count pixels "close to the signal colour", which overcounts for neutral
signals (a numeral's anti-aliased edge ramps straight through a grey's value).
At the default layout it is a contiguous 2x2 block at x13-14, y11-12.

## Reporting

Lead with the verdict — matches, or differs and where. Name the likely cause
when the shape points at one, and name the runs by their stamps.
