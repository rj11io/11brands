---
name: 11brands-v1-integration
description: Teach another repository or agent to use 11brands v1 — the paths, script contracts, and rules for generating brand assets from outside, plus a template for writing that repo's own skill. Use when a consuming project (a website, blog, app) wants favicons or OG images from 11brands, wants to automate asset generation, or asks how to integrate with or build a skill for 11brands.
---

# Integrating with 11brands v1

This skill is the contract. It tells an agent working in another repository
everything needed to consume 11brands without reading its internals, and ends
with a template for writing that repository's own local skill.

## The contract

**Location.** The 11brands repo, `v1/` subtree. `v0/` is deprecated; never touch
it.

**A brand** is `v1/brands/<key>/config.json` — every generation variable — plus
`brand.md`, the human decision record. Keys have three levels: `{brand}` default (`11io`), `{brand}-{sub-brand}`
secondary (`11blog-11ai`), `{brand}-{variant}` experiments (`11cc-bronze`).
List brands: `ls v1/brands/`.

**Generation** is four scripts, run from `v1/scripts/` with its own venv:

```bash
cd <11brands>/v1/scripts
.venv/bin/python generate_favicons.py <key>            # 5 PNGs + favicon.ico
.venv/bin/python generate_og_web.py <key>              # <key>-og-web.png
.venv/bin/python generate_og_content.py <key> --title "Post Title"
.venv/bin/python generate_all.py <key>                 # everything
```

All accept `--all` instead of a key, and `--run STAMP` to land in a chosen run
folder. `generate_og_content.py` with no title uses the brand's config
`text.title` (a "Lorem Ipsum" placeholder card). First-time setup:
`python3 -m venv .venv && .venv/bin/pip install Pillow`. macOS only by default —
the configs point at `/System/Library/Fonts/`.

**Output** lands in `v1/outputs/<stamp>/<key>/{favicons,og-web,og-content}/`,
each kind with a `MANIFEST.md` recording exactly what was used. Outputs are never
overwritten across stamps; a fresh run is a fresh folder.

**Consuming an asset = copying it out.** Nothing in 11brands deploys anything.
Copy from an `outputs/` run into your repository, and note the source stamp in
your commit message so the asset stays traceable.

## Rules for outside agents

1. **Read configs, don't guess.** Colours, text and layout all live in the
   brand's `config.json`; the manifest of any run repeats them.
2. **Never edit `v1/scripts/` or `v1/templates/`** from a consuming project. If
   an asset looks wrong, the brand's config is the interface — and changing a
   brand's config is the 11brands operator's call, not yours. Ask.
3. **Never stage or commit inside 11brands.** Generate, copy out, leave the
   working tree alone. Outputs are deliberately tracked-but-uncommitted.
4. **Do not resize or re-encode the assets you copy.** Every file was composed
   at its exact size for a reason: downscaling a finished image invents colours
   outside the brand's palette, and re-encoding an icon to palette-PNG breaks
   Next.js builds. Take `favicon-16x16.png` as-is; do not shrink `icon-512.png`.
5. **The `.ico` is load-bearing.** Its six frames are RGBA on purpose; ship the
   file untouched.
6. **New brand or variant needed?** That is `11brands-v1-init-brand`, run inside
   11brands with a human choosing the colour. Do not fabricate a config.

## Template: a consuming repo's own skill

Adapt and drop into the consuming repository's skills directory:

```markdown
---
name: <project>-brand-assets
description: Generate and import brand assets (favicons, OG images) for <project> from the 11brands repository. Use when favicons, link previews, OG or social images need generating, refreshing or importing.
---

# <project> brand assets

Assets come from the 11brands repo at <path-to-11brands>, brand key
`<key>` (see v1/brands/<key>/config.json for its palette and text).

## Generate

    cd <path-to-11brands>/v1/scripts
    .venv/bin/python generate_all.py <key>

For post/article cards:

    .venv/bin/python generate_og_content.py <key> --title "<post title>"

Output: <path-to-11brands>/v1/outputs/<stamp>/<key>/

## Import

Copy what this project ships, unmodified:

    cp <outputs>/<stamp>/<key>/favicons/favicon.ico   <project>/app/favicon.ico
    cp <outputs>/<stamp>/<key>/og-web/<key>-og-web.png <project>/public/og.png
    # ...project-specific destinations

Record the source stamp in the commit. Never resize, re-encode or palette-
convert an asset; never edit anything inside the 11brands repo; never commit
there. If the brand itself needs changing, ask the 11brands operator.
```

Fill in: the path to 11brands, the brand key, the project's real destination
paths, and any project-specific kinds (a blog wants og-content per post; a
landing page may only want favicons + og-web).
