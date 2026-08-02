# Asset generation scripts

Three scripts and one shared module. They read a brand's markdown file, draw its
assets, and write them into a timestamped folder under `../brands/`.

| Script | Makes | Output folder |
| --- | --- | --- |
| `generate-favicons.py` | 5 PNGs and a 6-frame `.ico` | `brands/<brand>/favicons/gen-<timestamp>/` |
| `generate-website-og.py` | one 1200×630 card | `brands/<brand>/web-og/gen-<timestamp>/` |
| `generate-content-og.py` | one 1200×630 card per title | `brands/<brand>/content-og/gen-<timestamp>/` |

`brandkit.py` holds everything shared: the brand file reader, the colour tables,
the card and icon geometry, and the drawing itself.

## Getting set up

Needs Python 3 and Pillow, and nothing else:

```bash
python3 -m venv .venv
.venv/bin/pip install Pillow
```

It also needs a monospaced font. `brandkit.py` points at
`/System/Library/Fonts/SFNSMono.ttf`, which macOS ships. On another machine,
change `MONO_FONT` — but note that a font with different metrics will not
reproduce cards that already exist.

## Running them

```bash
.venv/bin/python generate-favicons.py blog-rj11io
.venv/bin/python generate-website-og.py --all
.venv/bin/python generate-content-og.py blog-rj11io --title "Adding a publication or post"
.venv/bin/python generate-content-og.py blog-rj11io --titles-file titles.txt
```

`--all` runs every brand that has a `brand.md`. `--stamp NAME` replaces the
timestamp in the folder name, which is what you want when generating a set you
intend to compare against another one.

A titles file is one title per line; blank lines and `#` comments are skipped.

## What the three cards are

**A website card** is about a domain, so the domain takes the main row, framed by
a signal square on each side. It is the fallback link preview for a whole site.

**A content card** is about one piece of writing. The title takes the main row,
and the domain moves up above the mark as a masthead, because the card still has
to say where the piece lives and its old row is taken. The masthead sits 48
pixels below the top edge and the footer 49 above the bottom, so the two frame
the card as a pair.

**A favicon package** is the mark alone, cropped tight, at six sizes.

## Two rules the code will not let you break

Both were learned by breaking something, and both are why these scripts exist
rather than a person exporting images by hand.

**Colour is applied after resizing, never before.** The mark is stored as two
coverage maps — how much of each pixel the numeral covers, and how much the
signal square covers. Resizing a *finished picture* of the mark rings: Lanczos
overshoots at every hard edge, so a downscale invents pixels darker than the
ground, brighter than the numeral, and more saturated than the signal. That is
how a 16 pixel icon ended up carrying a `#2FE0A1` square that brand never had.
Resizing coverage instead means every output pixel is a blend of exactly three
known colours and can be nothing else.

**Icons are written RGBA, never as a palette image.** A 256 colour palette is a
valid PNG, looks identical for this artwork, and is about a third smaller. It
also breaks a Next.js build, which decodes `app/favicon.ico` itself and rejects
any frame that is not RGBA. The same applies inside the `.ico`: Pillow uses a
frame you supply only when it matches a requested size exactly and quietly
resamples the largest one for anything you leave out, so every frame is composed
and handed over.

## Adding a brand

Write `../brands/<key>/brand.md` and run the scripts. The file needs three
things:

```markdown
**Domain:** example.rj11.io
**Mode:** dark
**Signal:** `#EF4444`
```

`Mode` is `dark` or `light`, and it fixes the other three colours:

| Mode | Ground | Ink | Footer |
| --- | --- | --- | --- |
| dark | `#0A0A0A` | `#FAFAFA` | `#A1A1A1` |
| light | `#FAFAFA` | `#0A0A0A` | `#676767` |

Any of those can be overridden with `**Ground:**`, `**Ink:**` or `**Footer:**`.
Only `www-rj11io` does, because its ground and ink are warm rather than neutral.
`**Footer text:**` overrides the keyword line.

### Choosing a signal colour

Check it against its own ground before committing. A non-text graphic needs
3:1.

**A light ground cannot reuse a dark brand's hue.** The dark brands' signals sit
around the 500 step of a standard scale, tuned to be bright against black and
therefore weak against white. Blue 500 measures 3.52:1 on `#FAFAFA` — clearing
the minimum by so little that any later tweak to the ground breaks it — so
`cv-rj11io` uses blue 600 at 4.95:1. Step one darker on a light ground.

And check whether the colour already exists. `ai-rj11io` shipped for a while
carrying the blog's dark-mode green on a light ground, at 2.06:1. The fix was a
token the interface already defined for exactly that case.

## Reproducing what other repositories ship

These scripts were written to match the assets in the `11blog` repository, and
the match was measured rather than assumed. `../brands/BASELINE.md` records
exactly which files come out identical, which differ, and why.

The short version: every favicon is byte-identical, and the cards differ only
where an existing file predates the rules above.
