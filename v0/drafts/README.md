# Drafts

Where generated assets land first. Everything the scripts make comes here unless
someone passes `--into brands`, and moving a set into `../brands/` is a separate,
deliberate step — see [`../skills/11brands-v0-promote-draft/`](../skills/11brands-v0-promote-draft/).

The layout is identical to `../brands/`, so a promotion is a copy rather than a
translation:

```
<key>/
├── brand.md          the human record: fields plus the notes
├── config.json       every generation variable; what the scripts read
├── favicons/gen-<timestamp>/
├── web-og/gen-<timestamp>/
└── content-og/gen-<timestamp>/
```

Every draft has both definition files, exactly like a registered brand. That is
what makes a draft a place to work: edit a value in `config.json`, re-run a
generator, look at the result. A run reports any value where the config overrides
`brand.md`, so an experiment is never mistaken for the brand.

A promoted brand keeps its draft copies, so `drafts/<key>/` and `brands/<key>/` can
hold definitions that have since diverged. That is intended — the draft is the
sandbox. `diff brands/<key>/config.json drafts/<key>/config.json` shows whether it
has moved on.

## Why drafts exist

Two reasons, and the second is the one that matters.

Choosing a signal colour takes more than one attempt. Generating straight into
`brands/` meant the registered set filled up with runs nobody had approved, and
the only way to tell an approved run from an abandoned one was to remember.

More importantly, `brands/` has consumers. A favicon package there can be copied
into a live site, and `BASELINE.md` measures that folder against what `11blog`
ships. Anything that lands in it should have been looked at first.

## Two kinds of folder live here

**Work in progress**, keyed the same as the brand it will become — `cc-rj11io`
while `cc.rj11.io` is still being decided. Promotion copies its two definition
files and the chosen run into `brands/`, and the draft keeps its own copies so it
stays a place to work.

**Rejected attempts**, kept for reference, keyed with what made them distinct.
`cc.rj11.io` took three tries and the first two are both here:

| Folder | Signal | Why it is not the brand |
| --- | --- | --- |
| `cc-rj11io-light-bronze` | `#B45309` | light-mode gold; wrong direction for the brand |
| `cc-rj11io-dark-pewter` | `#64748B` | read as dark grey rather than silver |

The suffix is not decoration. A `brand.md` describes one set of colours, so two
attempts at the same brand cannot share a key without one overwriting the other's
definition. Naming the attempt keeps every one of them readable.

An archived attempt keeps its `brand.md`, and that file should open by saying it
was rejected and why. Otherwise the next reader finds a well-argued case for a
colour with no indication that it lost.

Each generated folder carries a `MANIFEST.md` recording the exact colours and
text used, so a run explains itself whatever happens to the `brand.md` above it.

## What `--all` does and does not cover

`--all` covers the brands registered in `brands/`. It deliberately skips folders
that exist only here: a rejected attempt still has a valid `brand.md`, and
sweeping it up would quietly regenerate a colour someone already decided against.
Name a draft explicitly.
