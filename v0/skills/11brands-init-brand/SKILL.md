---
name: 11brands-init-brand
description: Add a new brand to the 11brands repository as a draft — pick and check a signal colour against its ground, write drafts/<key>/brand.md and its config.json, and create the three output folders. Use when someone wants to set up, initialise, register or add a brand, sub-brand or site to 11brands, or asks what colour a new brand should use. Does not generate assets; hand off to 11brands-generate-assets for that. Does not add the brand to brands/; that is 11brands-promote-draft.
---

# Initialise a brand

A brand starts life as two files and three empty folders under `drafts/`. The work
is not the files — it is choosing a signal colour that survives contact with a 16
pixel favicon, and writing down why.

The two files are `brand.md`, the human record, and `config.json`, the resolved
list of every generation variable. You write the markdown; `generate-config.py`
writes the JSON from it. Every brand and every draft has both.

New brands go to `drafts/`, never straight to `brands/`. `brands/` is the
registered set, it has live consumers, and `brands/BASELINE.md` measures it
against another repository. Getting into it is a separate step —
`11brands-promote-draft`.

## What you need before writing anything

Ask for whatever is missing:

- **The domain**, e.g. `intel.rj11.io`. The key is the domain with dots turned
  into dashes and the TLD dropped: `intel-rj11io`.
- **Light or dark.**
- **A signal colour**, or a direction like "red" or "something warmer than the
  orange one".

Anything else — the footer wording, the masthead, a default title — has a working
default. Do not ask about them up front. Mention them once the brand exists, if
the brand sounds like it wants different wording.

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

### If the signal is a neutral

A silver, grey or off-white needs two checks the others do not, because it has
almost no hue to separate it from anything. Measure it against three things:

| Gap | Why | Floor |
| --- | --- | --- |
| vs the ground | the standard non-text graphic minimum | 3:1 |
| vs the ink | the signal square sits beside the numeral in the mark | 3:1, or a stated decision to go below |
| vs the footer grey | the accent must not be the same value as de-emphasised text | not equal |

Chromatic signals routinely sit at 1.60:1 to 3.61:1 against the ink and look
fine, because chroma does the separating. A neutral has nothing else. If the user
wants a bright neutral anyway, that is a legitimate choice — it makes the mark
read as monochrome with a highlight rather than ink plus colour — but say so and
record it in the notes. `cc-rj11io` is the worked example.

## Write the file

`drafts/<key>/brand.md`:

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

Only `Domain`, `Mode` and `Signal` are required. Add a colour override —
`**Ground:**`, `**Ink:**` or `**Footer:**` — only if the brand genuinely
deviates; `www-rj11io` is the one that does, because its ground and ink are warm.

Add a text field only if the brand actually wants different wording:

| Field | Default | Set it when |
| --- | --- | --- |
| `**Masthead:**` | the domain | content cards should say something other than the domain |
| `**Website row:**` | the domain | the site card's main row is not the domain |
| `**Footer text:**` | the standard keyword line | this site's keywords differ |
| `**Default title:**` | `Lorem Ipsum` | placeholder cards should say something else |

Any of them set to `none` draws nothing at all, including `**Default title:**`,
which then gives a content card with no title row. Document any field you set in
the notes, in the same way a colour is documented — someone reading a card later
should be able to find out why it says what it says.

Backticks are stripped from every field, so quoting a value is safe and never
reaches a card.

The notes section is not decoration. Every existing brand file records the
reasoning behind its colour, and that is what stops the next person repeating a
mistake.

## Then create the config and the folders

```bash
mkdir -p drafts/<key>/{favicons,web-og,content-og}
cd asset-generation-scripts && .venv/bin/python generate-config.py <key>
```

`generate-config.py` resolves `brand.md` against the family defaults and writes
`drafts/<key>/config.json`: the colours, all four text fields, the whole layout,
the icon sizes and the font. From then on that file is what the generators read,
so it is where someone tests an idea — change `mark_size` or a colour, re-run a
generator, look at the result. It never needs to be written by hand.

Do not hand-edit the new `config.json` at this point. It should match `brand.md`
exactly on the day the brand is created; a divergence on day one is just a brand
file that is wrong.

## Finally

Do **not** add the brand to the table in `brands/README.md`. That table lists the
registered set, and this brand is not in it yet; `11brands-promote-draft` adds the
row when the draft is approved. Adding it early makes the table describe assets
that do not exist.

Tell the user the brand is drafted and that nothing has been generated yet, give
them the contrast figure, and offer to run `11brands-generate-assets`.
