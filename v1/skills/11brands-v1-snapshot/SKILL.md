---
name: 11brands-v1-snapshot
description: Create a snapshot in 11brands v1 — one immutable, point-in-time capture of every active brand, every archived brand, and the integrations workspace, indexed for the www explorer. Use when someone wants to snapshot, capture, freeze or index the whole system, or refresh what the explorer shows.
---

# Create a snapshot (v1)

One command:

```bash
cd v1/scripts
.venv/bin/python create_snapshot.py
.venv/bin/python create_snapshot.py --run 20260805-golden   # named stamp
```

## What a snapshot is

```
snapshots/<stamp>/
├── SNAPSHOT.json     the index: palette, contrast, text, file lists per brand
├── brands/<key>/{favicons,og-web,og-content}/    freshly generated, every active brand
├── archive/<key>/...                             freshly generated, every archived brand
└── integrations/<run>/...                        verbatim COPY of integrations/
```

- `brands/` and `archive/` are **generated at snapshot time** from the configs —
  the capture of what the system produces today.
- `integrations/` is **copied, never regenerated** — those runs are consumer
  artifacts whose manifests carry their sources; regenerating would forge
  history. An empty `integrations/` is simply absent from the snapshot.
- `SNAPSHOT.json` indexes all of it: per brand the domain, mode, colors,
  contrast, text and file lists; per integration run its keys and sources. The
  `www/` explorer reads this file and streams the images.

## The rules

- **Immutable.** A snapshot is never edited, never regenerated in place, never
  joined — the script refuses an existing stamp. Wrong content means a new
  snapshot, not a fix to an old one.
- **Prune by age.** Snapshots are large (~270 images each today). Deleting an
  old one is fine; it is reproducible except for the integrations copy, which
  also still exists in `integrations/` unless separately pruned.
- **Git policy as everywhere:** tracked, never staged or committed unless the
  user says so.

## When to snapshot

- before working on the `www/` explorer, so it has fresh data
- after a candidate round settles (winner promoted to its plain key, losers
  archived) — the snapshot is the family portrait of that state
- not per generation; `outputs/` already records ordinary runs

## Report

Print the stamp and the three counts (active, archived, integration runs). If
active and archived counts do not match `archive_brand.py --list`, something
moved mid-snapshot — say so and re-run on a fresh stamp.
