# 11brands v0

Brand assets for the `rj11.io` family, and the scripts that make them.

Every site in the family shares one mark and one layout. The only thing that
changes between them is a single signal colour and whether the ground is dark or
light. That is the whole system: it is why a new brand is a short markdown file
rather than a design exercise, and why the signal colour is the one decision
worth checking with a number.

```
v0/
├── asset-generation-scripts/   three generators and their shared module
├── brands/                     one folder per brand, plus every generated set
└── skills/                     11brands-* skills for driving all of it
```

## Start here

- **Adding a brand** → `skills/11brands-init-brand/`
- **Making assets** → `skills/11brands-generate-assets/`
- **Checking output** → `skills/11brands-verify-assets/`
- **How the scripts work** → `asset-generation-scripts/README.md`
- **What exists today** → `brands/README.md`

## What this replaces

These assets used to be generated inside the `11blog` repository, by scripts
that grew one change at a time: a generator per design revision, plus two more
that edited existing images in place. This is that work consolidated into three
scripts that take the brand as data.

The consolidation was checked rather than assumed. Every favicon this repository
produces is byte-identical to the one `11blog` ships, and the cards differ only
where an `11blog` file predates a rule the scripts now enforce.
`brands/BASELINE.md` records exactly which files match, which do not, and why.

Nothing here writes outside `brands/`. Copying an asset into a consuming
repository is a separate, deliberate step.

## Requirements

Python 3, Pillow, and a monospaced font — `/System/Library/Fonts/SFNSMono.ttf`
by default, which means macOS unless `MONO_FONT` in `brandkit.py` is changed. A
font with different metrics will not reproduce cards that already exist.
