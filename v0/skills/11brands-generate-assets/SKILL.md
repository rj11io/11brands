---
name: 11brands-generate-assets
description: Generate brand assets in the 11brands repository — favicon packages, website Open Graph cards, and content Open Graph cards for one brand or all of them. Output goes to drafts/ by default. Use when someone wants to generate, render, produce, re-generate or refresh favicons, icons, OG images, link previews or social cards for a brand. Handles the Python environment, picks the right script, and reports where the output went.
---

# Generate brand assets

Three scripts under `asset-generation-scripts/`, all driven by a brand's
`brand.md`. By default each run writes a new `gen-<timestamp>` folder under
`drafts/`. Reusing the same `--stamp` targets that existing folder and can
overwrite its files.

## Output goes to drafts

`drafts/<brand>/` is the default and is almost always right. `brands/` is the
registered set: it has live consumers, and `brands/BASELINE.md` measures it
against the `11blog` repository. Assets arrive there by promotion, not by
generation — see `11brands-promote-draft`.

Only pass `--into brands` when the user has explicitly asked to write into the
registered set, or when you are regenerating a promoted brand in place and they
have said so. If they just say "generate assets for X", that means drafts.

If a run prints this, stop and reconsider:

```
warning: writing into brands/ from a definition still in drafts/
```

It means the brand is not registered and you have just put assets in the
registered set without its definition. Either the user wanted
`11brands-promote-draft`, or they wanted `drafts/`. Say which you think it is.

A key can have a `brand.md` in both roots — a registered brand being reworked as
a draft. The root you write to is the one whose definition is read. Every run
prints the file it used; include that in what you report, because "which
definition did this come from" is the first question a surprising asset raises.

## Pick the right one

| They asked for | Script |
| --- | --- |
| favicons, icons, the `.ico`, an app icon | `generate-favicons.py` |
| the site's OG image, a link preview for a whole site | `generate-website-og.py` |
| OG images for posts, article cards, social cards per title | `generate-content-og.py` |

A **website card** carries the domain in its main row. A **content card**
carries a title there and moves the domain up to a masthead. If it is unclear
which they mean, ask whether the image is for one page or the whole site.

A brand can override any of that text in its `brand.md` — `**Masthead:**`,
`**Website row:**`, `**Footer text:**`, `**Default title:**`, and any of them set
to `none` draws nothing. If the user wants different wording on a card, that is a
brand file change, not a command line flag. Do not edit the scripts for it.

## Set up the environment once

```bash
cd asset-generation-scripts
python3 -m venv .venv
.venv/bin/pip install Pillow
```

Reuse `.venv` if it is already there. Do not install Pillow globally.

## Run

```bash
.venv/bin/python generate-favicons.py b2b-rj11io
.venv/bin/python generate-website-og.py --all
.venv/bin/python generate-content-og.py b2b-rj11io
.venv/bin/python generate-content-og.py b2b-rj11io --title "A tour of the platform"
.venv/bin/python generate-content-og.py b2b-rj11io --titles-file titles.txt
```

**A content run with no title is the normal case.** It uses the brand's
`**Default title:**`, which is `Lorem Ipsum` unless the brand says otherwise, and
produces a complete, obviously-placeholder set. That is what you want when the
thing being reviewed is the brand rather than the words. Do not invent titles to
fill a set, and do not ask for titles the user has not offered — generate the
placeholder set and say that is what it is.

Pass `--title` only when the user has given you real titles, or asked for cards
for specific pieces.

`--all` covers every brand registered in `brands/`, not every folder in
`drafts/`. A rejected draft still has a valid `brand.md`, and sweeping it up would
regenerate a colour someone already decided against. To generate for a draft, name
it.

Use `--stamp NAME` when the output needs a deterministic folder name, such as
when comparing it with an expected path. Do not reuse a stamp when you need to
preserve an earlier run. For an ordinary generation, leave it off.

## Check the output before reporting

Look at one generated image. The scripts are silent about anything that is
visually wrong but structurally valid.

Worth a glance:

- Does the title fit? Long titles step down through smaller point sizes and stop
  at 28pt; past that they run wide.
- Is the signal square visible against the ground at 16 pixels?
- Did the right number of files appear? Six for a favicon package, one per
  title for content cards.
- Is any text missing that should be there? A `none` in the brand file removes a
  line silently and on purpose, so check the brand file before calling it a bug.

Each folder gets a `MANIFEST.md` recording the exact colours and text used, and
the brand file they came from. Read it back if something looks off — the brand
file may be the problem, not the script.

## Report

Give the user the folder path, the brand file it was generated from, and what
landed in it. Say plainly that it is a draft: it is in `drafts/`, nothing
downstream sees it, and promoting it into `brands/` is a separate step you can run
next if they want it.

If they intend to use the output in a live site, the promotion step comes first,
and copying a file out of this repository is a further deliberate step after that.
The `.ico` in particular has a live consumer.

## If something breaks

**`could not open /System/Library/Fonts/SFNSMono.ttf`** — not on macOS. Any
substitute changes the metrics and will not reproduce existing cards; say so
rather than quietly swapping a font.

**`no brand named 'X'. Looked for: …`** — the brand is not drafted or
registered. The message lists both paths it tried. Use `11brands-init-brand`.

**`mode must be one of dark, light`** — the brand file has a typo.

Do not edit the scripts to work around a failure. If a genuine change is needed,
change it deliberately and note that the baseline in `brands/BASELINE.md` may no
longer hold.
