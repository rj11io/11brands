---
name: 11brands-promote-draft
description: Promote a draft brand in the 11brands repository into the registered set — move its brand.md from drafts/ to brands/, copy the approved generation run across, and add or update its row in brands/README.md. Use when someone approves a draft, says a colour or a set is final, or asks to promote, register, publish, accept, or land a draft brand. Also handles the reverse: demoting a registered brand back to drafts, and archiving a rejected attempt under its own key.
---

# Promote a draft

Promotion is the step that moves a brand from "being decided" to "registered". It
is deliberately manual, because `brands/` has consumers: a favicon package there
can be copied into a live site, and `brands/BASELINE.md` measures that folder
against what the `11blog` repository ships.

Nothing here is automated by a script. It is a handful of file operations and one
table edit, and the checks matter more than the commands.

## Before anything, confirm what is being promoted

A draft usually holds more than one run. Get these three answers and do not guess
at any of them:

1. **Which brand key.** e.g. `cc-rj11io`.
2. **Which run of each kind.** List what is in the draft and ask, unless the user
   has already named one or there is only one candidate. The newest run is a
   reasonable default suggestion but a bad silent assumption — a user who
   generated three colours in a row is choosing between them, not accumulating
   them.
3. **Whether the current `brand.md` matches the run being promoted.** This is the
   one people get wrong. If the draft was iterated, `brand.md` describes the
   *latest* attempt, and an earlier run's colours live only in its `MANIFEST.md`.
   Promoting run 1 alongside a `brand.md` that describes run 3 produces a
   registered brand whose definition does not generate its own assets.

```bash
find drafts/<key> -name MANIFEST.md | sort
grep -E '^\| (Signal|Ground|Ink|Footer|Masthead|Website row|Footer text|Default title)' \
  drafts/<key>/*/gen-*/MANIFEST.md
```

Compare that against `drafts/<key>/brand.md`. If they disagree, stop and say so.
Either the user picks the run that matches the definition, or the definition needs
updating to describe the run they want.

## Then check the target

```bash
ls brands/<key> 2>/dev/null
```

**If `brands/<key>/` does not exist**, this is a first promotion. Create it.

**If it does exist**, this is a re-promotion of a brand that is already
registered, and two things change. Existing runs are never touched — a new run
goes in beside them under its own timestamp, exactly as generation works. And the
existing `brands/<key>/brand.md` is about to be replaced, so say what is changing:
which fields differ, and that assets already generated from the old definition
stay where they are and keep their own manifests.

Never overwrite an existing `gen-<timestamp>` folder. If the stamps collide,
generate the draft again with a fresh stamp rather than replacing anything.

## Promote

**Move the definition. Copy the assets.**

```bash
mkdir -p brands/<key>/{favicons,web-og,content-og}
mv drafts/<key>/brand.md brands/<key>/brand.md
cp -R drafts/<key>/favicons/gen-<stamp>   brands/<key>/favicons/gen-<stamp>
cp -R drafts/<key>/web-og/gen-<stamp>     brands/<key>/web-og/gen-<stamp>
cp -R drafts/<key>/content-og/gen-<stamp> brands/<key>/content-og/gen-<stamp>
```

Three details in those commands are load bearing. Each one fails in the *first
promotion of a new brand*, which is the most common case, and works fine on a
re-promotion, which is how a bug like this survives testing.

**Use `mv`, not `git mv`.** A brand-new draft's `brand.md` has usually never been
committed, and `git mv` refuses to touch an untracked file:

```
fatal: not under version control, source=drafts/<key>/brand.md, …
```

Plain `mv` works whether the file is tracked or not, and git records it as a rename
at commit time either way.

**Create the three kind folders first**, because the `cp` lines need their
destination's parent to exist.

**Name each `cp` destination in full.** `cp -R source dest/` copies *into* `dest`
only when `dest` already exists, and creates `dest` as a copy of `source` when it
does not. On a first promotion that silently flattens a run: you get
`brands/<key>/web-og/MANIFEST.md` where you wanted
`brands/<key>/web-og/gen-<stamp>/MANIFEST.md`, the manifest loses the stamp that
identifies it, and the folder stops matching every other folder in the repository.
Spelling out the destination makes the command behave identically either way.

Check the shape before moving on:

```bash
find brands/<key> -type f | sort
```

Every generated file should sit inside a `gen-<stamp>` folder, each with its
`MANIFEST.md` beside it.

The asymmetry is on purpose.

`brand.md` **moves**, because a definition should have exactly one home. Two
copies drift, and then nobody can say which one the next generation will read —
and the scripts read whichever root they are writing to, so a stale draft copy
silently wins during drafting.

The generated folders **copy**, because they are dated evidence. The draft run and
the promoted run are the same bytes with two different meanings: "this is what was
produced on this day" and "this is what the registered brand ships". Deleting the
first to save space costs the ability to reconstruct how the brand got here, and
these files are a few hundred kilobytes.

Copy only the kinds that exist. A draft with no favicons is normal — some brands
only ever need content cards. `blog-rj11io-11ai` is one.

## Update the registry table

Add or update the brand's row in `brands/README.md`:

```markdown
| `<key>` | <domain> | <mode> | `#RRGGBB` <colour name> | N.NN:1 |
```

The contrast figure is the signal against its own ground and comes from the brand
file, which already records it. Do not recompute it into a different number of
decimal places than the rest of the table.

If the brand does anything the table cannot show — a neutral signal, a colour
override, no footer — check that the prose under the table still reads true, and
add a sentence if it does not. That paragraph is where the family's exceptions are
explained, and an unexplained exception is how the next person repeats a mistake.

## What is left behind

The draft folder keeps its remaining generation runs and no longer has a
`brand.md`. That is the intended end state: the runs are self-describing through
their manifests, and the definition now lives in one place.

If the user wants the leftover draft runs gone, that is their call to make
explicitly, and it is a separate action from the promotion. Do not fold a deletion
into this step. Deleting the only copy of an asset that turns out to be live is
the failure this repository is arranged to prevent.

## Archiving a rejected attempt

Different job, same folder. When an attempt is not going to be promoted but is
worth keeping, give it a key that says what it was:

```bash
mv drafts/<key> drafts/<key>-<what-made-it-distinct>
```

`drafts/cc-rj11io-light-bronze` is the light-mode gold that `cc.rj11.io` tried
before it went dark. The suffix is load bearing: a `brand.md` describes one set of
colours, so two attempts cannot share a key without one erasing the other's
definition. Renaming frees the plain key for the attempt still in progress.

An archived draft keeps its `brand.md`. That file is the record of what was tried
and, if the notes were written properly, why it was rejected. Check the notes say
that before you move on; if they do not, add a line.

## Demoting

To take a registered brand back to drafts, reverse the move and remove its row
from the table:

```bash
mkdir -p drafts/<key>
mv brands/<key>/brand.md drafts/<key>/brand.md
```

The `mkdir` is not optional. `mv` into a path whose parent does not exist fails,
and after a promotion the draft folder often has no `brand.md` left in it or is
gone entirely:

```
fatal: renaming 'brands/<key>/brand.md' failed: No such file or directory
```

Leave the generated runs in `brands/` unless the user asks otherwise, and tell
them the runs are still there. Then say plainly what the demotion does not do: any
copy of those assets already taken into a consuming repository is unaffected, and
`brands/BASELINE.md` may now describe a brand that is no longer registered.

## Report

Say what moved, what was copied, and what the table now says. Name the run that
was promoted by its stamp, so the user can find it. If you found a mismatch
between `brand.md` and the promoted run, or a `BASELINE.md` claim that promotion
has made stale, say that too — it is more useful than the file list.
