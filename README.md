# 11brands

Reusable brand definitions and generated image assets for the `rj11.io` family.
The current version lives under `v0/` and contains the Python generators, one
Markdown definition per brand, generated favicon and Open Graph assets, and
the repo-local workflow guides for using them.

## Start here

- **Add a brand** → [`v0/skills/11brands-init-brand/`](v0/skills/11brands-init-brand/)
- **Generate assets** → [`v0/skills/11brands-generate-assets/`](v0/skills/11brands-generate-assets/)
- **Verify generated assets** → [`v0/skills/11brands-verify-assets/`](v0/skills/11brands-verify-assets/)
- **Promote a draft** → [`v0/skills/11brands-promote-draft/`](v0/skills/11brands-promote-draft/)
- **Read the v0 overview** → [`v0/README.md`](v0/README.md)
- **Browse the registered brands** → [`v0/brands/README.md`](v0/brands/README.md)

## Layout

```text
v0/
├── asset-generation-scripts/   Python generators and their shared module
├── drafts/                     where generated assets land first
├── brands/                     the registered set and its generated output
└── skills/                     repo-local workflow guides
```

Generated assets and manifests are written under `v0/drafts/` by default, and
reach `v0/brands/` only by promotion. Copying an asset into a consuming site is a
further separate step.
