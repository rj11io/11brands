<!-- BEGIN:11ai-pragmatic skill: https://ai.rj11.io/skills/11ai-pragmatic -->
# 11ai Pragmatic Register

always be extremely pragmatic and objective

when speaking be extremely concise. sacrifice grammar for the sake of concision. use lists. never use em dashes. show examples or snippets where applicable. cite sources.

when reviewing, troubleshooting, or find any kind of bug, or issue, always suggest a fix for each problem that you find.

when planning, brainstorming, strategising, go read-only mode (never implement or execute actions, never change or destroy any files) until precisely told to do so after a final action plan review.

when implementing, point to where the changes were made for the operator to verify.

also apply all these principles when writing code comments, or content for plans, reports, documentation.

when working in a repo, leave a detailed conventional commit message (include scope) for the operator to copy.
<!-- END:11ai-pragmatic skill -->

# Agent instructions — 11brands

## Version

**Work in `v1/` only. `v0/` is deprecated: ignore it entirely.** Do not read it
for guidance, extend it, regenerate from it, or "fix" anything in it. It exists
as history and as the byte-comparison baseline that validated v1's port. If a
task seems to require v0, stop and ask.

Start every task by reading [`v1/README.md`](v1/README.md). For workflows, use
the skills in `v1/skills/` — init, generate, verify, and integration each have
one, and they encode the checks that are not obvious from the code.

## The model, in four lines

- A brand is `v1/brands/<key>/config.json` — every generation variable, the only
  file the scripts read. `brand.md` beside it is the human decision record and
  is never parsed.
- Keys have three levels: `{brand}` default (`11io`), `{brand}-{sub-brand}`
  secondary (`11blog-11ai`), `{brand}-{variant}` experiments
  (`11ai-light-green`). A new idea is a new key, not an edit war.
- Generators run from `v1/scripts/` (own `.venv`) and write to
  `outputs/<stamp>/<key>/<kind>/`, one stamp per run, `MANIFEST.md` per kind.
  Runs for consuming projects go through `generate_integration.py --source
  <project>` into `integrations/` (same shape, source recorded in manifests);
  consumers copy out and leave the run behind — never delete their leftovers.
- `create_snapshot.py` captures the whole system into `snapshots/<stamp>/`
  (active + archived generated fresh, integrations copied verbatim,
  SNAPSHOT.json index). Snapshots are immutable: never edit, regenerate or join
  one — a wrong snapshot means a new stamp. `v1/www/` is the explorer that
  reads them.
- To change what an asset looks like, change the config and regenerate. Never
  edit the scripts for a colour, a string, a position or a font.
- Retired brands live in `v1/archive/`, moved verbatim by `archive_brand.py`
  and back by `promote_brand.py`. Never move brand folders by hand. The ordinary
  generators read `brands/` only; revisiting an archived brand in place is the
  `generate_archived_*` scripts, whose `--all` sweeps `archive/` only — the two
  roots never mix in one run.

## Hard rules

1. **Never stage or commit anything unless explicitly told to.** `outputs/`,
   `integrations/` and `snapshots/` are deliberately tracked-but-uncommitted; do
   not `git add` them and do not add them to `.gitignore`.
2. **Never overwrite a brand or a run.** `init_brand.py` refuses existing keys —
   do not work around that. New runs get new stamps; reuse a stamp only to
   deliberately extend that run. Retiring a brand is `archive_brand.py`, never
   deletion and never a hand-move.
3. **Do not resize, re-encode or palette-convert generated images.** Every file
   is composed at its exact size; downscaling invents out-of-palette colours and
   a palette-mode icon breaks Next.js builds. This is the project's founding
   scar tissue — respect it.
4. **Do not edit `v1/templates/mark.png`** or the template configs' layout
   sections without being asked; the templates are the family defaults.
5. **Colour choices need numbers.** A signal must clear 3:1 on its own ground
   (compute it, never eyeball it); a neutral signal additionally needs checking
   against the ink and the footer grey. The init skill has the doctrine.
6. **Verify by measurement, not by looking.** The verify skill has the exact
   gamut test (enumerate what `compose()` can emit — never an inverse
   coefficient test, never a step-grid search) and the icon checks.
7. **Report honestly.** Print the run stamp and paths, quote contrast figures,
   and if any check failed or was skipped, say so plainly.
8. **Commits are Conventional Commits, and they drive releases.** semantic-release
   cuts a release from every `feat`/`fix`/breaking push to `main` and writes
   `CHANGELOG.md`, the root `package.json` version and the tag itself. Never edit
   `CHANGELOG.md` or the root `package.json` version by hand, and never create
   tags — the `chore(release)` commits are the bot's.

## Environment

macOS assumed: configs point at `/System/Library/Fonts/`. Font changes go
through the config's `font.path`/`font.index` — `v1/templates/FONTS.md` has the
machine's inventory and the `.ttc` index trap (PT Mono regular is index 1, not
0). Python env: `cd v1/scripts && python3 -m venv .venv && .venv/bin/pip install
Pillow` if missing.

## For other repositories

A consuming project (website, blog, app) integrates via
[`v1/skills/11brands-v1-integration/`](v1/skills/11brands-v1-integration/): it
defines the contract — generate, copy out unmodified, record the stamp, never
commit here — and includes a template for writing that repo's own skill.
