# 11brands v0

Brand assets for the `rj11.io` family, and the scripts that make them.

Every site in the family shares one mark and one layout. Most of the variation is
a single signal colour and whether the ground is dark or light. `www-rj11io`
overrides the ground and ink with warm neutrals, and `cc-rj11io` is the one signal
that is a neutral rather than a colour. That is why a new brand is a short
markdown file rather than a design exercise, and why the signal colour is the one
decision worth checking with a number.

```
v0/
├── asset-generation-scripts/   three generators and their shared module
├── drafts/                     where generated assets land first
├── brands/                     the registered set, plus every promoted run
└── skills/                     11brands-* skills for driving all of it
```

## Start here

- **Adding a brand** → `skills/11brands-init-brand/`
- **Making assets** → `skills/11brands-generate-assets/`
- **Checking output** → `skills/11brands-verify-assets/`
- **Approving a draft** → `skills/11brands-promote-draft/`
- **How the scripts work** → `asset-generation-scripts/README.md`
- **What exists today** → `brands/README.md`
- **What is still being decided** → `drafts/README.md`

## Drafts first

Generation writes to `drafts/`. Getting into `brands/` is a separate, deliberate
step, because `brands/` has consumers: a favicon package there can be copied into
a live site, and `brands/BASELINE.md` measures that folder against what the
`11blog` repository ships.

The two folders have the same shape, so promoting is a copy rather than a
translation: both definition files and the approved run are copied across, and the
draft keeps its own. The draft is the sandbox and stays one, so it will diverge as
soon as someone tests the next idea. That is intended, and it is kept honest by two
rules: the generators read the definition in the root they are writing to, and every
run records the definition and config it used.

## Brands are data, all the way down

Every brand folder, draft or registered, holds two files:

- **`brand.md`** — the human record. Three required fields (domain, mode, signal)
  and, more importantly, the notes explaining why the colour is what it is.
- **`config.json`** — every generation variable, resolved: the four colours, all
  four drawn strings, the whole layout, the icon sizes, the font.

`config.json` is what the generators read, and that is the point. To test an idea —
a different signal, a bigger mark, smaller type, other wording — change a value and
re-run a generator. Nothing is fixed at the point of drawing and no script needs
editing. A run reports every value where the config overrides `brand.md`, so an
experiment is never mistaken for the brand, and the defaults reproduce the whole
published family byte for byte.

A content run given no title uses the brand's default title, which is
`Lorem Ipsum`. A bare run therefore produces a complete, obviously-placeholder
set — the right thing when what is under review is the brand and not the words.

## What this replaces

These assets used to be generated inside the `11blog` repository, by scripts
that grew one change at a time: a generator per design revision, plus two more
that edited existing images in place. This is that work consolidated into three
scripts that take the brand as data.

The consolidation was checked rather than assumed. `brands/BASELINE.md` records
the measured comparison against the selected favicon and card packages in
`11blog`, including which files match, which do not, and why. Making the text
into brand fields did not disturb any of it: a brand file that sets none of them
produces byte-identical output to before they existed.

## Requirements

Python 3, Pillow, and a monospaced font — `/System/Library/Fonts/SFNSMono.ttf`
by default, which means macOS unless `MONO_FONT` in `brandkit.py` is changed. A
font with different metrics will not reproduce cards that already exist.
