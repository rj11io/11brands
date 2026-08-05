# Asset generation scripts

Four scripts and one shared module. They read a brand's definition, draw its
assets, and write them into a timestamped folder — under `../drafts/` by default,
and under `../brands/` only when told.

| Script | Makes | Default output folder |
| --- | --- | --- |
| `generate-favicons.py` | 5 PNGs and a 6-frame `.ico` | `drafts/<brand>/favicons/gen-<timestamp>/` |
| `generate-website-og.py` | one 1200×630 card | `drafts/<brand>/web-og/gen-<timestamp>/` |
| `generate-content-og.py` | one 1200×630 card per title | `drafts/<brand>/content-og/gen-<timestamp>/` |
| `generate-config.py` | a brand's `config.json` | beside its `brand.md` |

`brandkit.py` holds everything shared: the definition reader, the colour tables,
the text and layout defaults, and the drawing itself.

## A brand is two files

Every brand folder, in `brands/` and in `drafts/` alike, holds both:

| File | What it is | Who reads it |
| --- | --- | --- |
| `brand.md` | the human record: three required fields, plus the notes explaining why the colour is what it is | people, and the scripts as a fallback |
| `config.json` | every generation variable, fully resolved, including the layout numbers `brand.md` has no syntax for | the scripts, first |

**`config.json` wins.** That is the point of it: change a value, re-run a
generator, look at the result. Nothing else needs editing and nothing needs
recompiling.

Because it wins, any disagreement with `brand.md` is reported rather than left to
be discovered later from an asset nobody can explain:

```
note: drafts/cc-rj11io/config.json overrides brand.md, and is what was used:
         signal #B4BDC4 -> #FF6B35
         mark_size 350 -> 300
       Update brand.md to match once an idea is settled, so the reasoning stays
       with the values.
```

Each run's `MANIFEST.md` also records the config it used and lists any layout
value that differs from the family default, so a folder still explains itself.

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
.venv/bin/python generate-favicons.py b2b-rj11io
.venv/bin/python generate-website-og.py --all
.venv/bin/python generate-content-og.py b2b-rj11io
.venv/bin/python generate-content-og.py b2b-rj11io --title "Adding a publication or post"
.venv/bin/python generate-content-og.py b2b-rj11io --titles-file titles.txt
```

A content run with no title uses the brand's default title, which is
`Lorem Ipsum` unless the brand overrides it. A bare run therefore produces a
complete, obviously-placeholder set, which is what you want when the thing under
review is the brand rather than the words.

A titles file is one title per line; blank lines and `#` comments are skipped.

### Where the output goes

Everything lands in `../drafts/<brand>/` unless you pass `--into brands`.
Promoting a draft into the registered set is a separate step, described in
`../skills/11brands-v0-promote-draft/`.

```bash
.venv/bin/python generate-favicons.py b2b-rj11io               # -> drafts/
.venv/bin/python generate-favicons.py b2b-rj11io --into brands # -> brands/
```

A key can have a `brand.md` in both roots at once — a registered brand that is
being reworked as a draft. The root you are writing to is the one whose
definition is read, so drafting reads the draft and promoting reads the promoted
copy. Every run prints which file it used and records it in the manifest.

`--all` covers every brand registered in `brands/`, and deliberately not every
folder in `drafts/`: a rejected draft still has a `brand.md`, and sweeping it up
would quietly resurrect a colour someone already decided against. Name a draft
explicitly.

`--stamp NAME` replaces the timestamp in the folder name, which is what you want
when generating a set you intend to compare against another one. Reusing the same
stamp targets the same folder and can replace files there; use a new stamp for a
separate run.

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

Write `../drafts/<key>/brand.md`, then run `generate-config.py <key>` to give it a
`config.json`, then run the generators. The markdown file needs three things:

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

## Every variable, and where it lives

`config.json` is the full list. `brand.md` can set the colours and the text but
not the layout, so the two overlap rather than duplicate.

```json
{
  "brand": "cc-rj11io",
  "domain": "cc.rj11.io",
  "mode": "dark",
  "colours": {"signal": "#B4BDC4", "ground": "#0A0A0A", "ink": "#FAFAFA", "footer": "#A1A1A1"},
  "text": {
    "masthead": "cc.rj11.io",
    "website_row": "cc.rj11.io",
    "footer_text": "AI / SOFTWARE / PRODUCT / ENGINEERING / TECHNOLOGY",
    "default_title": "Lorem Ipsum"
  },
  "layout": {
    "card": [1200, 630],
    "mark_origin": [425, 42],
    "mark_size": 350,
    "mark_crop": [247, 247, 1007, 1007],
    "square": 18,
    "gap": 20,
    "max_row": 1040,
    "row_top": 477,
    "row_middle": 486,
    "title_max_pt": 42,
    "title_min_pt": 28,
    "masthead_middle": 56,
    "masthead_pt": 15,
    "masthead_tracking": 4,
    "footer_middle": 574,
    "footer_pt": 15
  },
  "icons": {
    "master": 512,
    "box": [462, 368],
    "files": [{"size": 512, "name": "icon-512.png"}],
    "ico_sizes": [16, 32, 48, 64, 128, 256]
  },
  "font": {"mono": "/System/Library/Fonts/SFNSMono.ttf"}
}
```

What the layout numbers mean:

| Key | Meaning |
| --- | --- |
| `card` | card size in pixels |
| `mark_origin`, `mark_size` | where the mark sits on a card, and how big |
| `mark_crop` | the region of the mark master to use |
| `square`, `gap` | the signal square, and its distance from the row text |
| `max_row` | widest a framed row may be before the type steps down |
| `row_top`, `row_middle` | the main row's top edge and text baseline centre |
| `title_max_pt`, `title_min_pt` | the range the row steps through to fit |
| `masthead_middle`, `masthead_pt`, `masthead_tracking` | the content card's top line |
| `footer_middle`, `footer_pt` | the keyword line |
| `icons.master`, `icons.box` | the reference size and the margin the artwork fits inside |
| `icons.files` | which PNG sizes to write, and under what names |
| `icons.ico_sizes` | which frames go in the `.ico` |

A text value of `null` draws nothing. Every value shown above is the family
default, so a config that changes none of them reproduces its existing assets byte
for byte — which was measured, not assumed.

### Creating and refreshing a config

```bash
.venv/bin/python generate-config.py b2b-rj11io
.venv/bin/python generate-config.py --all --drafts
.venv/bin/python generate-config.py b2b-rj11io --refresh
```

An existing `config.json` is left alone by default, and the three generators
create one only when it is missing. Nothing ever rewrites one silently, because a
hand-edited layout value cannot be recovered from `brand.md`. `--refresh` is the
explicit way to discard those edits and rebuild from the record.

## Every field a brand file can set

Three are required. Everything else has a default, so a file that sets only the
three behaves exactly as it always did.

| Field | Required | Default | What it does |
| --- | --- | --- | --- |
| `**Domain:**` | yes | — | the site, and the default for both text rows |
| `**Mode:**` | yes | — | `dark` or `light`; fixes ground, ink and footer colour |
| `**Signal:**` | yes | — | the accent colour |
| `**Ground:**` | no | from mode | background |
| `**Ink:**` | no | from mode | the numeral, and the main row text |
| `**Footer:**` | no | from mode | the footer and masthead text colour |
| `**Masthead:**` | no | the domain | the small tracked line above the mark, on content cards |
| `**Website row:**` | no | the domain | the framed main row on the website card |
| `**Footer text:**` | no | `AI / SOFTWARE / PRODUCT / ENGINEERING / TECHNOLOGY` | the keyword line on every card |
| `**Default title:**` | no | `Lorem Ipsum` | the title used when a content run is given none |

Those four text fields are every string drawn on any asset. Nothing is fixed at
the point of drawing; the only text that does not come from the brand file is a
title passed on the command line, and even that falls back to a brand field.

**To draw no text at all, set the field to `none`.** All four honour it:

- `**Footer text:** none` gives cards with no footer line.
- `**Masthead:** none` gives content cards with nothing above the mark.
- `**Website row:** none` gives a website card with no main row, squares included.
- `**Default title:** none` gives a content card with no title row when no title
  is passed. The file is named `untitled-content-og.png`.

The word is needed because the reader has to see a value to notice the line at
all, so leaving the field blank would simply be invisible to it.

Any value may be backticked or bare — colours with or without a `#`, text with or
without quotes. Backticks are stripped from every field, including `**Domain:**`,
so quoting never leaks into a card or a manifest.

### Where the output goes when the definition is elsewhere

`--into brands` reads the promoted definition when there is one and falls back to
the draft when there is not. That fallback is allowed but warns, because it leaves
`brands/<key>/` holding runs with no `brand.md` beside them:

```
warning: writing into brands/ from a definition still in drafts/
```

If you see that, you wanted `11brands-v0-promote-draft` instead.

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

**A neutral signal needs two more checks than a colour does.** Every chromatic
signal separates from the numeral by hue, so its lightness against the ink can be
low and nobody notices. A silver or grey has only lightness, so it has to be
measured against the ink and the footer grey as well as the ground.
`cc-rj11io` is the worked example.

## Reproducing what other repositories ship

These scripts were written to match the assets in the `11blog` repository, and
the match was measured rather than assumed. `../brands/BASELINE.md` records
exactly which files come out identical, which differ, and why.

The short version: the five favicon packages match the selected packages listed
in the baseline, while the cards have the documented mark, row, and footer
differences.

Adding the text fields did not change any of this. A brand file that sets none of
them produces byte-identical output to before they existed, which was checked
against the `blog-rj11io` run of 2026-08-02 rather than assumed.
