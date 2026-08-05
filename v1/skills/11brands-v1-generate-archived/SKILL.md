---
name: 11brands-v1-generate-archived
description: Generate assets for ARCHIVED brands in 11brands v1, in place — favicons, OG cards or full packs from archive/ without promoting anything. Use when someone wants to revisit, regenerate, re-render or look again at a retired brand or losing candidate without reactivating it.
---

# Generate from the archive (v1)

Four standalone scripts, mirrors of the ordinary generators — same drawing code,
same output location, same stamps and titles — except they read `archive/`
instead of `brands/`:

```bash
cd v1/scripts
.venv/bin/python generate_archived_favicons.py 11bench-dark-sky
.venv/bin/python generate_archived_og_web.py 11brands-dark-violet
.venv/bin/python generate_archived_og_content.py 11bench-dark-sky --title "A Post"
.venv/bin/python generate_archived_all.py --all        # every ARCHIVED brand
```

Output lands in `outputs/<stamp>/<key>/<kind>/` as usual; the manifest records
the config it actually read (`archive/<key>/config.json`), so a revisit run is
distinguishable from an active one forever.

## When this, when promote

- **Revisit only** — compare a retired candidate again, show someone what it
  looked like, re-run a check: these scripts. The brand stays retired; nothing
  in `archive/` or `brands/` changes.
- **Returning to active duty** — `11brands-v1-promote-brand`. A brand that is
  being consumed again belongs in `brands/`.

Editing an archived config to test ideas is a smell: experiments belong on an
active variant key. If the user wants to iterate on an archived brand, suggest
promoting it or initialising a fresh variant instead.

## Scoping rules

- `--all` here means every archived brand and nothing else. The ordinary
  generators' `--all` means every active brand and nothing else. No run mixes
  the two roots — that separation is what keeps a retired candidate from
  sneaking into a "regenerate everything" batch.
- An active key passed to these scripts errors with a pointer to the ordinary
  generators, and vice versa. Do not work around either error.

## Fidelity

Same config, same code, same environment → same bytes. Verified: a full pack
generated from `archive/` reproduces the brand's pre-archive run byte for byte.
A difference in a revisit run therefore means the environment moved (font,
Pillow) — worth flagging, and `11brands-v1-verify-assets` will localise it.
