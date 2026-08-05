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
translation. What moves is the `brand.md` — a definition should have one home,
because two copies drift and the scripts read whichever root they are writing to.
What copies is the generated run, because it is dated evidence and cheap to keep.

## Brands are data, including their words

Three fields are required — domain, mode, signal — and everything else has a
default. That includes every string drawn on every asset: the masthead, the
website card's main row, the footer keyword line, and the title a content card
falls back to. Any of them can be changed per brand, or set to `none` to draw
nothing. Nothing is fixed at the point of drawing.

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
