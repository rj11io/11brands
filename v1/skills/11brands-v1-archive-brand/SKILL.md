---
name: 11brands-v1-archive-brand
description: Archive a brand in 11brands v1 — move brands/<key>/ to archive/<key>/ verbatim, taking it out of generation while keeping it recoverable. Use when someone wants to archive, retire, park, or deactivate a brand or variant, or clean up losing candidates after picking a winner.
---

# Archive a brand (v1)

One command, one move, no content changes:

```bash
cd v1/scripts
.venv/bin/python archive_brand.py <key>
.venv/bin/python archive_brand.py --list     # active vs archived
```

## What archiving means

`brands/<key>/` moves to `archive/<key>/` byte-for-byte — config.json and
brand.md keep their exact contents, so promotion restores a brand that generates
exactly what it did before. An archived brand:

- is invisible to the ordinary generators (a run against its key points at the
  alternatives) — revisiting it in place is `11brands-v1-generate-archived`,
  which reads `archive/` directly
- is skipped by the ordinary generators' `--all`
- keeps its key reserved — `init_brand.py` scans only `brands/`, so if a new
  brand should take the key, decide about the archived one first

Past runs in `outputs/` are untouched; they are dated facts and stay where they
are.

## The one check the script enforces

Archiving a key that active brands build on (`11blog` while `11blog-11ai` is
active) is refused without `--force`. The sub-brands keep working either way —
every brand is self-contained — but a family whose base is archived while its
variants generate is usually a mistake, not a plan. Confirm intent with the user
before reaching for `--force`.

## When asked to archive several

Run the script once per key; do not move folders by hand. After a
pick-the-winner round, the usual shape is: promote nothing (the winner was
already copied or re-initialised under its final key), archive every losing
candidate, and check `--list` reads as expected.

## After a round

Once winners are promoted and losers archived, a `11brands-v1-snapshot` captures
the settled state — that is what the www explorer shows.

## Report

Say what moved and show the `--list` state. If any archived brand's `brand.md`
does not record why it lost, say so — the decision record is the point of
keeping the folder at all.
