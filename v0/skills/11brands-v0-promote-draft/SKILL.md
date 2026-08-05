---
name: 11brands-v0-promote-draft
description: Promote a draft brand in the 11brands repository into the registered set — copy its brand.md and config.json from drafts/ to brands/, copy the approved generation run across, and add or update its row in brands/README.md. Use when someone approves a draft, says a colour or a set is final, or asks to promote, register, publish, accept, or land a draft brand. Also handles the reverse: demoting a registered brand back to drafts, and archiving a rejected attempt under its own key.
---

# Promote a draft

Promotion is the step that moves a brand from "being decided" to "registered". It
is deliberately manual, because `brands/` has consumers: a favicon package there
can be copied into a live site, and `brands/BASELINE.md` measures that folder
against what the `11blog` repository ships.

Nothing here is automated by a script. It is a handful of file operations and one
table edit, and the checks matter more than the commands.

## What a brand consists of

Two definition files, in `drafts/` and `brands/` alike:

- `brand.md` — the human record. Three required fields, and the notes that explain
  why the colour is what it is.
- `config.json` — every generation variable, resolved: colours, all four text
  fields, the whole layout, the icon sizes, the font. **This is the file the
  generators read**, so it is the one that decides what the assets look like.

Promotion copies both. Copying `brand.md` alone registers a brand whose assets are
drawn from a file that is not there.

## Before anything, confirm what is being promoted

A draft usually holds more than one run. Get these three answers and do not guess
at any of them:

1. **Which brand key.** e.g. `cc-rj11io`.
2. **Which run of each kind.** List what is in the draft and ask, unless the user
   has already named one or there is only one candidate. The newest run is a
   reasonable default suggestion but a bad silent assumption — a user who
   generated three colours in a row is choosing between them, not accumulating
   them.
3. **Whether the definition still matches the run being promoted.** This is the
   one people get wrong. If the draft was iterated, the definition describes the
   *latest* attempt, and an earlier run's values live only in its `MANIFEST.md`.
   Promoting run 1 alongside a config that describes run 3 produces a registered
   brand whose definition does not generate its own assets.

```bash
find drafts/<key> -name MANIFEST.md | sort
grep -E '^\| (Signal|Ground|Ink|Footer|Masthead|Website row|Footer text|Default title|Config)' \
  drafts/<key>/*/gen-*/MANIFEST.md
```

Each manifest also carries a `## Layout` section listing anything that differs
from the family default, which is where a config tweak shows up. Compare all of it
against `drafts/<key>/config.json`. If they disagree, stop and say so. Either the
user picks the run that matches the config, or the config needs to be set back to
what produced the run they want.

Check the two definition files agree with each other too:

```bash
cd asset-generation-scripts && .venv/bin/python -c "
import brandkit as kit; kit.load_brand('<key>', prefer='drafts')"
```

That prints a `note:` listing every value where `config.json` overrides
`brand.md`. Silence means they agree. A promotion is the right moment to fold a
settled experiment back into `brand.md`, so the reasoning ends up beside the
values rather than trailing them.

## Then check the target

```bash
ls brands/<key> 2>/dev/null
```

**If `brands/<key>/` does not exist**, this is a first promotion. Create it.

**If it does exist**, this is a re-promotion of a brand that is already
registered, and two things change. Existing runs are never touched — a new run
goes in beside them under its own timestamp, exactly as generation works. And the
existing definition files are about to be replaced, so say what is changing: which
values differ, and that assets already generated from the old definition stay where
they are and keep their own manifests.

Never overwrite an existing `gen-<timestamp>` folder. If the stamps collide,
generate the draft again with a fresh stamp rather than replacing anything.

## Promote

```bash
mkdir -p brands/<key>/{favicons,web-og,content-og}
cp drafts/<key>/brand.md    brands/<key>/brand.md
cp drafts/<key>/config.json brands/<key>/config.json
cp -R drafts/<key>/favicons/gen-<stamp>   brands/<key>/favicons/gen-<stamp>
cp -R drafts/<key>/web-og/gen-<stamp>     brands/<key>/web-og/gen-<stamp>
cp -R drafts/<key>/content-og/gen-<stamp> brands/<key>/content-og/gen-<stamp>
```

Two details are load bearing, and both only fail on the *first* promotion of a new
brand, which is the common case. A re-promotion works either way, which is how a
bug like this survives testing.

**Create the three kind folders first.** The `cp -R` lines need their destination's
parent to exist.

**Name each `cp -R` destination in full.** `cp -R source dest/` copies *into*
`dest` only when `dest` already exists, and creates `dest` as a copy of `source`
when it does not. On a first promotion that silently flattens a run: you get
`brands/<key>/web-og/MANIFEST.md` where you wanted
`brands/<key>/web-og/gen-<stamp>/MANIFEST.md`, the manifest loses the stamp that
identifies it, and the folder stops matching every other folder in the repository.
Spelling out the destination makes the command behave the same either way.

Check the shape before moving on:

```bash
find brands/<key> -type f | sort
```

Two definition files at the top, and every generated file inside a `gen-<stamp>`
folder with its `MANIFEST.md` beside it.

Copy only the kinds that exist. A draft with no favicons is normal — some brands
only ever need content cards. `blog-rj11io-11ai` is one, and it deliberately has no
favicons or website card, because its palette is identical to `ai-rj11io` and the
icons would be byte-for-byte the same file.

## Update the registry table

Add or update the brand's row in `brands/README.md`:

```markdown
| `<key>` | <domain> | <mode> | `#RRGGBB` <colour name> | N.NN:1 |
```

The contrast figure is the signal against its own ground and comes from the brand
file, which already records it. Do not recompute it into a different number of
decimal places than the rest of the table.

If the brand does anything the table cannot show — a neutral signal, a colour
override, a changed layout, no footer — check that the prose under the table still
reads true, and add a sentence if it does not. That paragraph is where the family's
exceptions are explained, and an unexplained exception is how the next person
repeats a mistake.

## What is left behind

The draft keeps everything: both definition files and every run. Nothing is
deleted and nothing moves out.

That means `drafts/<key>/` and `brands/<key>/` now hold two copies of the same
definition, and they will drift the moment someone tests another idea in the draft.
That is the intended shape rather than an oversight, because the draft is the
sandbox: it is where you change a config value and regenerate. Two things keep the
drift honest:

- The generators read the definition in the root they are **writing** to. Drafting
  reads the draft copy; a `--into brands` run reads the promoted copy. Neither
  silently picks the wrong one.
- Every run prints the definition and config it used, and records both in its
  `MANIFEST.md`.

To see whether a draft has moved on since it was promoted:

```bash
diff brands/<key>/config.json drafts/<key>/config.json
```

If the user wants the leftover draft runs gone, that is their call to make
explicitly, and it is a separate action from the promotion. Do not fold a deletion
into this step. Deleting the only copy of an asset that turns out to be live is the
failure this repository is arranged to prevent.

## Archiving a rejected attempt

Different job, same folder. When an attempt is not going to be promoted but is
worth keeping, give it a key that says what it was:

```bash
mv drafts/<key> drafts/<key>-<what-made-it-distinct>
```

`drafts/cc-rj11io-light-bronze` is the light-mode gold that `cc.rj11.io` tried
before it went dark; `drafts/cc-rj11io-dark-pewter` is the attempt after that. The
suffix is load bearing: a definition describes one set of colours, so two attempts
cannot share a key without one erasing the other's. Renaming frees the plain key
for the attempt still in progress.

Use `mv`, not `git mv`. A draft that has never been committed is untracked, and
`git mv` refuses to touch an untracked file:

```
fatal: not under version control, source=drafts/<key>, …
```

Plain `mv` works either way and git records the rename at commit time.

After renaming, fix the `brand` key inside `config.json` so it matches its folder:

```bash
cd asset-generation-scripts && .venv/bin/python generate-config.py <new-key> --refresh
```

An archived attempt keeps both definition files. `brand.md` should open by saying
it was rejected and why; check that it does, and add a line if it does not.
Otherwise the next reader finds a well-argued case for a colour with no indication
that it lost.

One side effect to expect rather than fix: a website card is named after the brand
key at the time it was drawn, so renaming the folder leaves
`cc-rj11io-web-og.png` sitting inside `cc-rj11io-light-bronze/`. Leave it. The name
records which key produced it, the run's `MANIFEST.md` says the same, and renaming
the file would make the archived run disagree with its own manifest. A fresh run
under the new key will simply produce the new name.

## Demoting

To take a brand out of the registered set, remove its definition files and its row
from the table. The draft already has its own copies, so nothing needs moving back:

```bash
rm brands/<key>/brand.md brands/<key>/config.json
```

If the draft somehow has no copy — an old brand registered before drafts existed —
move rather than delete, and create the folder first, because `mv` into a missing
parent fails:

```bash
mkdir -p drafts/<key>
mv brands/<key>/brand.md    drafts/<key>/brand.md
mv brands/<key>/config.json drafts/<key>/config.json
```

Leave the generated runs in `brands/` unless the user asks otherwise, and tell them
the runs are still there. Then say plainly what the demotion does not do: any copy
of those assets already taken into a consuming repository is unaffected, and
`brands/BASELINE.md` may now describe a brand that is no longer registered.

## Report

Say what was copied, what the table now says, and name the promoted run by its
stamp so the user can find it. If you found a disagreement between the two
definition files, or between the definition and the run, or a `BASELINE.md` claim
that promotion has made stale, say that too — it is more useful than the file list.
