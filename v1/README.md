# 11brands v1

Brand assets for the `rj11.io` family: one mark, one layout, and a config per
brand that varies the colours, the words, and — when needed — everything else.

```
v1/
├── templates/          the mark master, the two config templates, brand.md
│                       skeleton, FONTS.md, titles example
├── scripts/            five Python scripts + shared brandkit.py + .venv
├── brands/             the registry: one folder per brand
│   └── <key>/
│       ├── config.json   every generation variable; the only file scripts read
│       └── brand.md      the decision record; never parsed
├── outputs/            generated assets, one folder per run
│   └── <stamp>/<key>/{favicons,og-web,og-content}/
└── skills/             11brands-v1-* agent workflows
```

## The model

**A brand is a config.** `brands/<key>/config.json` holds all of it: palette,
every drawn string, the full layout geometry, icon sizes, the font. The scripts
read that file and nothing else. To test an idea — another colour, a bigger
mark, different wording, another font — edit the config and regenerate; no
script changes, ever. `brand.md` beside it records *why* the values are what
they are, and is never parsed, so it cannot go stale as state — only as prose.

**Keys are `{brand-title}-{variant}`**: `11io-dark-orange`, `blog-dark-green`,
`cc-dark-titanium`. The variant lives in the key, so a second attempt at the
same site is just a second brand — nothing collides.

**Runs are stamped.** Every generation lands in `outputs/<stamp>/`, one stamp
per run, shared across a batch. Nothing is overwritten across stamps, every
kind folder carries a `MANIFEST.md` of exactly what was used, and two runs can
always be diffed. Outputs stay tracked in git but are committed only
deliberately.

## Setup (once)

Needs Python 3 and Pillow. macOS assumed — the configs point at
`/System/Library/Fonts/SFNSMono.ttf` (see `templates/FONTS.md` to change that,
including the `.ttc` index trap).

```bash
cd v1/scripts
python3 -m venv .venv
.venv/bin/pip install Pillow
```

## Initialise a brand

```bash
cd v1/scripts
.venv/bin/python init_brand.py 11io-dark-orange \
    --domain www.rj11.io --mode dark --signal '#F97316'
```

The mode picks the template — `config-dark` mirrors blog.rj11.io, `config-light`
mirrors ai.rj11.io — and the flags overwrite brand, domain and signal on top.
Optional: `--ground --ink --footer` (hex), `--masthead --website-row
--footer-text --title` (text; the literal value `none` writes null, which draws
nothing). It prints the signal-on-ground contrast — a non-text graphic needs
3:1 — and refuses to overwrite an existing key. Then fill in the placeholders in
the new `brand.md`.

## Generate

```bash
cd v1/scripts
.venv/bin/python generate_favicons.py 11io-dark-orange     # 5 PNGs + 6-frame .ico
.venv/bin/python generate_og_web.py --all                  # one 1200×630 card each
.venv/bin/python generate_og_content.py blog-dark-green --title "Adding a Post"
.venv/bin/python generate_og_content.py blog-dark-green --titles-file titles.txt
.venv/bin/python generate_all.py --all                     # full pack, one run folder
```

- every generator takes `<key>` or `--all`, plus `--run STAMP` to join a run;
  the stamp defaults to now, and `generate_all.py` mints one for the whole batch
- a content run with **no title** uses the config's `text.title` — the templates
  ship `"Lorem Ipsum"`, so a bare run produces a complete placeholder card
- a titles file is one title per line; blank lines and `#` comments are skipped

## The config, briefly

```json
{
  "schema": 1,
  "brand": "blog-dark-green",  "domain": "blog.rj11.io",  "mode": "dark",
  "colors": {"signal": "#2BC88F", "ground": "#0A0A0A", "ink": "#FAFAFA", "footer": "#A1A1A1"},
  "text":   {"masthead": "blog.rj11.io", "website_row": "blog.rj11.io",
             "footer_text": "AI / SOFTWARE / ...", "title": "Lorem Ipsum"},
  "layout": {"card": [1200, 630], "mark_size": 350, "row_max_pt": 42, "...": "..."},
  "icons":  {"files": [{"size": 512, "name": "icon-512.png"}], "ico_sizes": [16, 32, 48, 64, 128, 256]},
  "font":   {"path": "/System/Library/Fonts/SFNSMono.ttf", "index": 0}
}
```

- every value is explicit; a text value of `null` draws nothing
- `mode` is a record of which template the brand started from; the scripts never
  branch on it
- `font.index` selects a face inside a `.ttc` — see `templates/FONTS.md`
- the templates ARE the defaults; there is no second copy inside the scripts

## Two rules the code will not let you break

Both learned by breaking something, both the reason these scripts exist.

**Colour is applied after resizing, never before.** The mark is stored as two
coverage maps — how much of each pixel the numeral covers, and how much the
signal square covers — and painted at the target size. Resizing a finished
picture rings: the resampler invents pixels outside the brand's palette, which
is how a 16px icon once shipped with a `#2FE0A1` square its brand never had.
Composing from coverage makes every output pixel a blend of exactly three known
colours.

**Icons are RGBA, never palette images, at every size including inside the
`.ico`.** A palette PNG looks identical and is smaller — and it breaks a Next.js
build, which decodes `app/favicon.ico` itself and rejects non-RGBA frames.
Pillow silently resamples `.ico` frames you do not supply, so every frame is
composed at its own size and handed over explicitly.

## Verified against v0

This is v0's proven drawing code with the workflow rebuilt around a config
registry. The port was measured, not assumed: a brand initialised with
blog.rj11.io's values reproduces v0's published favicons, website card and
content card **byte-identically** (16/16 files, including the config-default
Lorem Ipsum card against ai.rj11.io's). `v0/` is deprecated and kept only as
history — nothing in it should be used or edited.

## Skills

| Skill | For |
| --- | --- |
| `skills/11brands-v1-init-brand/` | choosing a signal colour and registering a brand |
| `skills/11brands-v1-generate-assets/` | running the generators, testing config ideas |
| `skills/11brands-v1-verify-assets/` | measuring changes, gamut and icon checks |
| `skills/11brands-v1-integration/` | teaching a consuming repo to use all of this |
