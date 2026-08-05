---
name: 11brands-v1-generate-assets
description: Generate brand assets in 11brands v1 — favicon packages, website OG cards, content OG cards, or the full pack, for one brand or all. Also covers testing an idea by editing a brand's config.json and regenerating. Use when someone wants to generate, render, produce, regenerate or refresh favicons, icons, OG images, link previews or social cards for a brand.
---

# Generate brand assets (v1)

Four generators in `v1/scripts/`, all reading `brands/<key>/config.json` and
nothing else. Work in `v1/`; ignore `v0/` entirely — it is deprecated.

| They asked for | Script |
| --- | --- |
| favicons, icons, the `.ico` | `generate_favicons.py` |
| the site's OG image, a whole-site link preview | `generate_og_web.py` |
| OG images for posts, per-title cards | `generate_og_content.py` |
| everything, the full pack | `generate_all.py` |

```bash
cd v1/scripts
.venv/bin/python generate_favicons.py 11io-dark-orange
.venv/bin/python generate_og_web.py --all
.venv/bin/python generate_og_content.py blog-dark-green --title "Adding a Post"
.venv/bin/python generate_all.py --all
```

If `.venv` is missing: `python3 -m venv .venv && .venv/bin/pip install Pillow`.

## Runs and stamps

Every run lands in `outputs/<stamp>/<key>/<kind>/`. The stamp defaults to now;
`--run STAMP` joins an existing run. `generate_all.py` mints one stamp and passes
it to each generator, so a batch is one folder. Use an explicit `--run` named
after the idea when comparing attempts: `--run bigger-mark`.

Each kind folder gets a `MANIFEST.md`: full palette, text, font, and any layout
value that differs from the template. A run explains itself.

## Titles

**A content run with no `--title` is the normal case.** It uses the brand's
config `text.title` — "Lorem Ipsum" from the templates — and produces a complete,
obviously-placeholder card. Do not invent titles and do not ask for ones the user
has not offered; generate the placeholder and say that is what it is. Pass
`--title` (repeatable) or `--titles-file` only when the user gives real titles.

## Testing an idea

The config is the whole interface. To try a different colour, mark size, wording
or font:

1. Edit `brands/<key>/config.json`.
2. Regenerate with a `--run` named for the idea.
3. Compare against the previous run.

Do not edit the scripts to change a colour, position, string or font — everything
that affects an image is in the config. Font changes have their own reference:
`templates/FONTS.md`, including the `.ttc` index trap. When an idea is settled,
record the why in `brands/<key>/brand.md`.

## Check before reporting

Look at one generated image. The scripts are silent about visually-wrong but
structurally-valid output:

- Long titles step down to `row_min_pt` and then run wide — does it fit?
- Is the signal square visible at 16 pixels?
- Right file count? Six per favicon pack, one card per title.
- Text missing? A null in the config draws nothing on purpose — check the config
  before calling it a bug.

## Git

`outputs/` stays tracked but is never staged or committed unless the user says
so. Do not add it to `.gitignore` and do not `git add` it.

## If something breaks

**`could not open <font>`** — the config's `font.path` is wrong for this machine.
`templates/FONTS.md` lists what exists. Do not silently swap a font.

**`no brand named 'X'`** — not initialised. Use `11brands-v1-init-brand`.

**`schema is None/0/2...`** — the config predates or postdates these scripts.
Stop and say so rather than editing the check away.

Do not edit the scripts to work around a failure.
