---
name: 11brands-generate-assets
description: Generate brand assets in the 11brands repository — favicon packages, website Open Graph cards, and content Open Graph cards for one brand or all of them. Use when someone wants to generate, render, produce, re-generate or refresh favicons, icons, OG images, link previews or social cards for a brand. Handles the Python environment, picks the right script, and reports where the output went.
---

# Generate brand assets

Three scripts under `asset-generation-scripts/`, all driven by a brand's
`brand.md`. Each run writes a new `gen-<timestamp>` folder and never overwrites
anything.

## Pick the right one

| They asked for | Script |
| --- | --- |
| favicons, icons, the `.ico`, an app icon | `generate-favicons.py` |
| the site's OG image, a link preview for a whole site | `generate-website-og.py` |
| OG images for posts, article cards, social cards per title | `generate-content-og.py` |

A **website card** carries the domain in its main row. A **content card**
carries a title there and moves the domain up to a masthead. If it is unclear
which they mean, ask whether the image is for one page or the whole site.

## Set up the environment once

```bash
cd asset-generation-scripts
python3 -m venv .venv
.venv/bin/pip install Pillow
```

Reuse `.venv` if it is already there. Do not install Pillow globally.

## Run

```bash
.venv/bin/python generate-favicons.py blog-rj11io
.venv/bin/python generate-website-og.py --all
.venv/bin/python generate-content-og.py blog-rj11io --title "A tour of the platform"
.venv/bin/python generate-content-og.py blog-rj11io --titles-file titles.txt
```

`--all` covers every brand with a `brand.md`. Content cards need at least one
`--title` or a `--titles-file`; ask for the titles rather than inventing them.

Use `--stamp NAME` when the run is meant to be compared against another one —
it replaces the timestamp so two runs can share a folder name. For an ordinary
generation, leave it off.

## Check the output before reporting

Look at one generated image. The scripts are silent about anything that is
visually wrong but structurally valid.

Worth a glance:

- Does the title fit? Long titles step down through smaller point sizes and stop
  at 28pt; past that they run wide.
- Is the signal square visible against the ground at 16 pixels?
- Did the right number of files appear? Six for a favicon package, one per
  title for content cards.

Each folder gets a `MANIFEST.md` recording the exact colours used. Read it back
if a colour looks off — the brand file may be the problem, not the script.

## Report

Give the user the folder path and what landed in it. If they intend to use the
output somewhere, say plainly that these scripts only write into `brands/` —
copying a file into another repository is a separate, deliberate step, and the
`.ico` in particular has a live consumer.

## If something breaks

**`could not open /System/Library/Fonts/SFNSMono.ttf`** — not on macOS. Any
substitute changes the metrics and will not reproduce existing cards; say so
rather than quietly swapping a font.

**`no brand at brands/<key>/brand.md`** — the brand is not registered. Use
`11brands-init-brand`.

**`mode must be one of dark, light`** — the brand file has a typo.

Do not edit the scripts to work around a failure. If a genuine change is needed,
change it deliberately and note that the baseline in `brands/BASELINE.md` may no
longer hold.
