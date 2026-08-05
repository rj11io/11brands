---
name: 11brands-verify-assets
description: Check generated brand assets in the 11brands repository — compare a draft run against a promoted run, against another run, or against the assets a consuming repository already ships, and check every pixel sits inside the brand's own colours. Use when someone asks whether the output matches, is the same as before, still reproduces 11blog, is correct, or has drifted; or when a generator or brand file has changed and the effect needs measuring.
---

# Verify brand assets

Two different questions, and they need different checks.

**Did anything change?** Compare a run against another run, or against what a
consuming repository ships. `brands/BASELINE.md` records the expected answer for
`11blog`.

**Is the output correct in itself?** Every pixel of a brand asset should be a
blend of that brand's own colours and nothing else. A pixel outside that set is
either a resampling artefact or a brand whose palette does not agree with itself.

Note **four** colours, not three. The mark uses ground, ink and signal; the footer
and masthead are drawn in a fourth, `**Footer:**`. In every standard mode the
footer happens to sit exactly on the line between ground and ink — `#A1A1A1` is
62.9 per cent of the way from `#0A0A0A` to `#FAFAFA` — so its anti-aliased blends
land on the triangle's own edge and a three-colour test passes anyway. Override
ground or ink without warming the footer to match and that stops being true. See
"When a brand's palette disagrees with itself" below.

Never answer either by looking at an image. Both are measurements.

Runs live under two roots. `drafts/<key>/` holds work in progress and rejected
attempts; `brands/<key>/` holds the registered set. The most common comparison in
this repository is now a draft against the promoted run it would replace, which
answers "what would promoting this actually change".

Take the colours from the run's own `MANIFEST.md`, or from the brand's
`config.json` — never from `brand.md`, and never by retyping them. `config.json` is
what the generators read, so a run made from a tweaked config was drawn with values
`brand.md` does not mention. The manifest records which config was used and lists
any layout value that differs from the family default.

A third question is worth asking before either of the two below:

**Did the definition change, or did the code?** If two runs of the same brand
differ, compare the definitions first — it is one command and it usually explains
everything:

```bash
diff brands/<key>/config.json drafts/<key>/config.json
```

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

Ask it as a forward question: could the drawing code have produced this colour at
all? Build the set of everything `compose` in `brandkit.py` can emit, then subtract.

The coverage pair comes from two 8-bit masks, so `i` and `s` are always `k/255`,
and `compose` renormalises the pair when `i + s` exceeds 1. Enumerate exactly
that, and the answer is exact:

```python
def emittable(ground, ink, signal):
    """Every colour compose() can produce. 65,536 pairs, so just enumerate them."""
    out = set()
    for a in range(256):
        for b in range(256 - a):                    # i + s <= 1, drawn as given
            i, s = a / 255, b / 255
            out.add(tuple(
                round(ground[c] * (1 - i - s) + ink[c] * i + signal[c] * s)
                for c in range(3)
            ))
    for a in range(256):                            # i + s > 1, renormalised
        for b in range(256):
            if a + b <= 255:
                continue
            t = (a + b) / 255
            i, s = (a / 255) / t, (b / 255) / t
            out.add(tuple(
                round(ground[c] * (1 - i - s) + ink[c] * i + signal[c] * s)
                for c in range(3)
            ))
    return out


def artefacts(paths, ground, ink, signal):
    """Distinct colours the drawing code could not have produced."""
    ok = emittable(ground, ink, signal)
    seen = set()
    for path in paths:
        seen |= set(Image.open(path).convert("RGB").get_flattened_data())
    return sorted(seen - ok)
```

Anything in that list is real. Read the brand's colours and text from the run's
`MANIFEST.md` rather than retyping them.

Two things that will bite you:

**Enumerate, do not search with a step size.** An earlier version of this check
searched coverage on an arbitrary grid (`step=0.001`) and asked whether any point
hit the colour exactly. A grid that does not include the true coverage value misses
it, so the test reports an artefact that is not there. At `step=0.002` it invented
phantom artefacts in nine brands out of ten. `k/255` is not a tuning parameter, it
is the actual domain.

**Compare against `set(...)`, never against the pixels.** A card has around 300
distinct colours and 756,000 pixels.

### When a brand's palette disagrees with itself

A non-empty result is not always a resampling bug. If the artefacts all lie on the
ramp from the ground to some other brand colour, the palette itself is
inconsistent, and the fix is the brand file rather than the code:

```python
ramp = {
    tuple(round(ground[c] + (a / 255) * (other[c] - ground[c])) for c in range(3))
    for a in range(256)
}
print(len(set(bad) & ramp), "of", len(bad), "lie on the ground->other ramp")
```

`www-rj11io` is the worked example. It overrides ground and ink to warm neutrals
but leaves `**Footer:**` at the family's cool `#A1A1A1`, so every anti-aliased
pixel of its footer and masthead is a blend of a cool grey into a warm ground:
164 of 164 artefacts on its website card sit exactly on that ramp, and its
favicons, which carry no text, are clean. Check the footer against the ground-to-ink
line before blaming the resampler:

```python
ts = [(footer[c] - ground[c]) / (ink[c] - ground[c]) for c in range(3) if ink[c] != ground[c]]
# max(ts) - min(ts) near zero means the footer is a true blend of ground and ink
```

### Why not test it the other way round

The obvious alternative is an inverse test: solve for the pixel's position in the
triangle formed by ground, ink and signal, and flag anything whose coefficients
fall outside it. That works, but only while the triangle is wide, and it fails
silently when it is not.

A near-neutral signal sits close to the line between ground and ink, so the
triangle collapses to a sliver. Measure the angle between `ink − ground` and
`signal − ground`:

| Brand | Signal | Angle |
| --- | --- | --- |
| `b2b-rj11io` | `#FBBF24` gold | 31.2° |
| `cc-rj11io` | `#B4BDC4` titanium | 8.4° |

In that sliver, one bit of rounding in the output becomes a coefficient excursion
of about 1%, which is outside the ±0.01 tolerance such a test needs. It reports
false positives on every file of a neutral-signal brand, and the colours it flags
are within one unit of the ground, a legitimate blend, or the ink.

Clamping the coefficients back onto the simplex does not rescue it either: the
clamp itself moves the point about 2.6 channel units along the long axis, so the
residual measures the clamp rather than the image.

The forward test has no tolerance to tune, needs no special case for neutrals, and
answers the question you actually have. Use it.

### The matching favicon trap

Checking that the signal "survives" at 16 pixels by counting pixels close to the
signal colour has the same flaw. For a neutral signal, an anti-aliased numeral edge
ramps from ground to ink and passes straight through the silver's own value, so the
count inflates: `cc-rj11io` reported 15 of 256 against 4 or 5 for the chromatic
brands, which looks like the square has grown.

Recover the coverage and count pixels above 90% signal instead:

```python
def solid_signal(path, ground, ink, signal):
    """Pixels that are at least 90 per cent signal coverage."""
    im = Image.open(path).convert("RGB")
    u = [ink[i] - ground[i] for i in range(3)]
    v = [signal[i] - ground[i] for i in range(3)]
    uu = sum(x * x for x in u); vv = sum(x * x for x in v)
    uv = sum(a * b for a, b in zip(u, v))
    det = uu * vv - uv * uv
    out = []
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            w = [px[x, y][i] - ground[i] for i in range(3)]
            wu = sum(a * b for a, b in zip(w, u)); wv = sum(a * b for a, b in zip(w, v))
            if (wv * uu - wu * uv) / det >= 0.90:
                out.append((x, y))
    return out
```

At 16 pixels that is a contiguous 2×2 block at x13–14, y11–12, in every brand in
the family, neutral or not.

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
- **One text region entirely, others untouched** — a text field changed, or was
  set to `none`. Compare the `## Text` tables in the two manifests before
  assuming a bug; a missing footer may be exactly what the brand asked for.

If the result contradicts `brands/BASELINE.md`, say so explicitly. That file is
the record of what was true on 2026-08-02, and a contradiction means either the
scripts changed or the other repository did. Work out which before proposing a
fix, and update the baseline rather than leaving it wrong.
