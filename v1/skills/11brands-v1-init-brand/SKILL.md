---
name: 11brands-v1-init-brand
description: Initialise a brand in 11brands v1 — pick and prove a signal colour, run scripts/init_brand.py to create brands/<key>/{config.json,brand.md}, and write the decision record. Use when someone wants to add, set up, initialise or register a brand, sub-brand, site or variant in 11brands, or asks what colour a new brand should use. Does not generate assets; hand off to 11brands-v1-generate-assets for that.
---

# Initialise a brand (v1)

One script creates the two files; the real work is choosing a signal colour that
survives a 16 pixel favicon, and writing down why.

Work in `v1/`. Ignore `v0/` entirely — it is deprecated.

## The key convention

`{brand-title}-{variant}`, lowercase, dash-separated: `11io-dark-orange`,
`blog-dark-green`, `cc-dark-titanium`. The brand title is the site's short name
(`11io` for www.rj11.io); the variant is what distinguishes this attempt from any
other at the same brand. The script rejects keys that do not match.

Because the variant is part of the key, a second idea for the same site is simply
a second brand: `cc-light-bronze` next to `cc-dark-titanium`. Nothing collides
and nothing gets overwritten.

## What you need before running anything

Ask for whatever is missing:

- **The domain**, e.g. `intel.rj11.io`.
- **Light or dark.**
- **A signal colour**, or a direction like "red" or "warmer than the orange one".

Everything else — masthead, website row, footer text, default title — has a
template default. Do not ask about them up front.

## Choose the signal, then prove it

**It must clear 3:1 against its own ground** — the floor for a non-text graphic.
Aim past it: 4.5:1 also covers the colour later being set in type.

**It must be separable from the other brands at 16 pixels.** Check what is
already taken in `brands/` (and the family history in the brand.md files).

Compute, never estimate:

```python
def luminance(c):
    def channel(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
```

Grounds are `#0A0A0A` dark, `#FAFAFA` light, unless overridden. The script
computes and prints the ratio too, and warns under 3:1 — but report the number to
the user **before** running it, with the reasoning.

Traps that have each caught someone:

- **A light ground cannot reuse a dark brand's hue.** Dark-ground signals sit
  around the 500 step of a standard scale; blue 500 is 3.52:1 on `#FAFAFA`, blue
  600 is 4.95:1. Step darker on a light ground. Gold needs two steps.
- **A neutral signal (silver, grey) needs three checks, not one**: the ground,
  the ink (the square sits beside the numeral and has no hue to separate it) and
  the footer grey (the accent must not match de-emphasised text). Chromatic
  signals pass the ink at 1.6–3.6:1 because chroma separates them; a neutral has
  only lightness. Going deliberately low against the ink is legitimate — it makes
  the mark read as monochrome-with-a-highlight — but say so and record it.

## Run the script

```bash
cd v1/scripts
.venv/bin/python init_brand.py intel-dark-red --domain intel.rj11.io --mode dark --signal '#EF4444'
```

Optional flags: `--ground --ink --footer` (hex overrides), `--masthead
--website-row --footer-text --title` (text; literal `none` writes null, which
draws nothing). The mode picks the matching template
(`templates/config-{mode}.template.json`); flags overwrite on top. It refuses to
overwrite an existing key.

## Then write the decision record

The script leaves placeholders in `brands/<key>/brand.md`. Fill them: what the
site is, why this colour, what it was chosen against and the number that killed
each rejected candidate. The notes are the point — they are what stops the next
person repeating a mistake. The config holds the state; brand.md holds the
reasoning; the scripts never parse it.

## Report

Give the user the key, the contrast figure, and what was written. Say nothing has
been generated yet and offer `11brands-v1-generate-assets`.
