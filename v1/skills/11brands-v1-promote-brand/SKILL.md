---
name: 11brands-v1-promote-brand
description: Promote an archived brand in 11brands v1 — move archive/<key>/ back to brands/<key>/ verbatim, returning it to generation. Use when someone wants to promote, restore, unarchive, reactivate or bring back a brand or variant.
---

# Promote an archived brand (v1)

The exact inverse of archiving. One command, one move, no content changes:

```bash
cd v1/scripts
.venv/bin/python promote_brand.py <key>
.venv/bin/python promote_brand.py --list     # active vs archived
```

`archive/<key>/` moves back to `brands/<key>/` byte-for-byte, and the brand is
immediately generatable again — same config, same output, proven by round-trip
(archive then promote reproduces identical files).

## The one conflict that can exist

If `brands/<key>/` already exists, the script refuses: an active brand and an
archived one share a key, and silently overwriting either would destroy a
definition. Surface it to the user — the resolution is theirs (usually renaming
one, which means fixing the `brand` field inside its config to match the new
folder name).

## Promote only for active duty

If the user just wants to look at a retired brand's assets again, they do not
need this skill: `11brands-v1-generate-archived` generates from `archive/` in
place. Promote when the brand is genuinely returning to use.

## After promoting

- Check the brand's `brand.md`: if it was archived as a losing candidate, its
  notes say so, and a brand returning to active duty may need that paragraph
  updated to say why it is back.
- Generation works immediately: `generate_all.py <key>` for a fresh pack.
- If the brand was archived long ago, consider `11brands-v1-verify-assets`
  against its last run in `outputs/` — the config is identical, so any
  difference means the environment moved (font, Pillow), not the brand.

## Report

Say what moved, show `--list`, and mention the brand is generatable again.
