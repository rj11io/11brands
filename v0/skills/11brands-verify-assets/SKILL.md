---
name: 11brands-verify-assets
description: Check generated brand assets in the 11brands repository — compare a run against another run or against the assets a consuming repository already ships, and check every pixel sits inside the brand's own colours. Use when someone asks whether the output matches, is the same as before, still reproduces 11blog, is correct, or has drifted; or when a generator or brand file has changed and the effect needs measuring.
---

# Verify brand assets

Two different questions, and they need different checks.

**Did anything change?** Compare a run against another run, or against what a
consuming repository ships. `brands/BASELINE.md` records the expected answer for
`11blog`.

**Is the output correct in itself?** Every pixel of a brand asset should be a
blend of that brand's three colours — ground, ink, signal — and nothing else. A
pixel outside that set is a resampling artefact.

Never answer either by looking at an image. Both are measurements.

## Comparing two sets

Generate with `--stamp` so the runs are findable, then compare bytes first:

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
    worst = max(max(px[x, y]) for y in range(h) for x in range(w))
    return f"{n} px differ, max channel delta {worst}"
```

When something differs, say **where**. A count alone is not a finding. Split the
card into its regions and report per region — masthead `y 20..80`, mark
`y 42..392`, main row `y 455..525`, footer `y 560..590`. "Only the mark differs"
and "the row moved two pixels" are diagnoses; "23,932 pixels differ" is not.

For an `.ico`, compare every frame:

```python
im = Image.open(path)
for size in sorted(im.ico.sizes()):
    frame = im.ico.getimage(size)   # check .mode is RGBA
```

## Checking a set on its own

Every colour must sit inside the triangle formed by the brand's ground, ink and
signal:

```python
def outside_triangle(path, ground, ink, signal):
    """Count distinct colours that are not a blend of the brand's three."""
    im = Image.open(path).convert("RGB")
    u = [ink[i] - ground[i] for i in range(3)]
    v = [signal[i] - ground[i] for i in range(3)]
    uu = sum(x * x for x in u); vv = sum(x * x for x in v)
    uv = sum(a * b for a, b in zip(u, v))
    det = uu * vv - uv * uv
    bad = 0
    for c in set(im.get_flattened_data()):
        w = [c[i] - ground[i] for i in range(3)]
        wu = sum(a * b for a, b in zip(w, u)); wv = sum(a * b for a, b in zip(w, v))
        g = (wu * vv - wv * uv) / det
        a = (wv * uu - wu * uv) / det
        recon = [ground[i] + g * u[i] + a * v[i] for i in range(3)]
        if g < -0.01 or a < -0.01 or g + a > 1.01 or max(
            abs(recon[i] - c[i]) for i in range(3)
        ) > 1.5:
            bad += 1
    return bad
```

Anything above zero means resampling has invented a colour. Read the brand's
colours from the run's `MANIFEST.md` rather than retyping them.

Do not use a cruder test. Checking whether a channel exceeds the signal's own
maximum gives false positives on light grounds, where a blend toward a near-white
ground legitimately does exceed it.

Also worth checking on an icon set: every `.ico` frame is `RGBA`, not palette
mode. A palette frame breaks a Next.js build.

## Reporting

Lead with the verdict — matches, or differs and where. Give counts, and name the
likely cause when the shape of the difference points at one:

- **Mark only** — one side composes from coverage masks and the other resized a
  finished picture.
- **Row shifted one to three pixels** — one side computed the position and the
  other inherited it from an edit.
- **Everything, slightly** — a different font, or a different mark master.
- **One region's colour only** — a brand file changed.

If the result contradicts `brands/BASELINE.md`, say so explicitly. That file is
the record of what was true on 2026-08-02, and a contradiction means either the
scripts changed or the other repository did. Work out which before proposing a
fix, and update the baseline rather than leaving it wrong.
