---
name: 11brands-init-brand
description: Add a new brand to the 11brands repository — pick and check a signal colour against its ground, write brands/<key>/brand.md, and create the three output folders. Use when someone wants to set up, initialise, register or add a brand, sub-brand or site to 11brands, or asks what colour a new brand should use. Does not generate assets; hand off to 11brands-generate-assets for that.
---

# Initialise a brand

A brand in this repository is one markdown file and three empty folders. The
work is not the file — it is choosing a signal colour that survives contact with
a 16 pixel favicon, and writing down why.

## What you need before writing anything

Ask for whatever is missing:

- **The domain**, e.g. `intel.rj11.io`. The key is the domain with dots turned
  into dashes and the TLD dropped: `intel-rj11io`.
- **Light or dark.**
- **A signal colour**, or a direction like "red" or "something warmer than the
  orange one".

## Choose the signal, then prove it

Every brand keeps the same mark and the same layout. The signal colour carries
the entire distinction between them, so two things have to be true, and both are
checkable rather than matters of taste.

**It must clear 3:1 against its own ground.** That is the floor for a non-text
graphic. Aim past it: 4.5:1 also covers the case where the colour is later set
in type.

**It must be separable from the other brands at 16 pixels.** Read
`brands/README.md` for what is taken. A dark crimson next to `#F97316` orange
reads as brown at that size.

Two traps, both of which have already caught someone here:

- **A light ground cannot reuse a dark brand's hue.** Signals for dark grounds
  sit around the 500 step of a standard scale, which is bright against black and
  weak against white. Blue 500 measures 3.52:1 on `#FAFAFA`; blue 600 measures
  4.95:1. Step one darker on a light ground.
- **Check whether the colour already exists.** `ai.rj11.io` shipped at 2.06:1
  because it reused the blog's dark-mode green on a light ground, when the
  interface already defined a light-mode token for exactly that.

Compute the ratio rather than estimating it:

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

Grounds are `#0A0A0A` for dark and `#FAFAFA` for light, unless the brand
overrides them.

**Report the number to the user before writing the file.** If it is under 3:1,
say so and propose a darker or lighter step instead of writing it.

## Write the file

`brands/<key>/brand.md`:

```markdown
# <domain>

<One or two lines on what this site is.>

**Domain:** <domain>
**Mode:** <dark|light>
**Signal:** `#RRGGBB`

## Notes

<Why this colour. What it was chosen against. Anything a future reader would
otherwise have to re-derive.>

Contrast of the signal on its ground: **N.NN:1**.
```

Only `Domain`, `Mode` and `Signal` are read by the scripts. Add
`**Ground:**`, `**Ink:**` or `**Footer:**` only if the brand genuinely deviates
— `www-rj11io` is the one that does, because its ground and ink are warm.

The notes section is not decoration. Every existing brand file records the
reasoning behind its colour, and that is what stops the next person repeating a
mistake.

## Then create the folders

```bash
mkdir -p brands/<key>/{favicons,web-og,content-og}
```

## Finally

Add the brand to the table in `brands/README.md`, with its contrast figure.

Tell the user the brand is registered and that nothing has been generated yet,
and offer to run `11brands-generate-assets`.
