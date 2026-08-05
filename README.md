# 11brands

Brand definitions and generated image assets for the `rj11.io` family: favicon
packages and Open Graph cards, all drawn by script from one config per brand.

**The current version is [`v1/`](v1/). `v0/` is deprecated** — kept only as
history and a comparison baseline. Do not use it, extend it, or copy from it.

## Start here

- **Read the v1 overview** → [`v1/README.md`](v1/README.md)
- **Add a brand** → [`v1/skills/11brands-v1-init-brand/`](v1/skills/11brands-v1-init-brand/)
- **Generate assets** → [`v1/skills/11brands-v1-generate-assets/`](v1/skills/11brands-v1-generate-assets/)
- **Verify output** → [`v1/skills/11brands-v1-verify-assets/`](v1/skills/11brands-v1-verify-assets/)
- **Archive / restore a brand** → [`v1/skills/11brands-v1-archive-brand/`](v1/skills/11brands-v1-archive-brand/), [`v1/skills/11brands-v1-promote-brand/`](v1/skills/11brands-v1-promote-brand/)
- **Revisit an archived brand** → [`v1/skills/11brands-v1-generate-archived/`](v1/skills/11brands-v1-generate-archived/)
- **Use from another repo** → [`v1/skills/11brands-v1-integration/`](v1/skills/11brands-v1-integration/)
- **Agent ground rules** → [`AGENTS.md`](AGENTS.md)

## Layout

```text
v1/                 current
├── templates/      mark master, config templates, FONTS.md
├── scripts/        init, generators (active + archived), archive/promote
├── brands/         the active registry: config.json + brand.md per brand
├── archive/        retired brands, out of generation, recoverable verbatim
├── outputs/        generated assets, one folder per stamped run
├── integrations/   runs triggered by consuming projects; they copy out, runs stay
└── skills/         11brands-v1-* agent workflows

v0/                 DEPRECATED — history only, do not touch
```

Generated assets land in `v1/outputs/` and are tracked but committed only
deliberately. Copying an asset into a consuming site is a separate step, done
from an outputs run, unmodified.
