# 11brands skills

Four repo-local workflow guides for the main brand-asset tasks. Each guide is a
`SKILL.md` file with the checks, commands, and hand-off rules for that workflow.

| Skill | Use it for |
| --- | --- |
| [`11brands-init-brand/`](11brands-init-brand/) | Drafting a new brand and choosing its signal colour |
| [`11brands-generate-assets/`](11brands-generate-assets/) | Generating favicons and website or content Open Graph cards |
| [`11brands-verify-assets/`](11brands-verify-assets/) | Measuring output changes and checking colour gamut |
| [`11brands-promote-draft/`](11brands-promote-draft/) | Moving an approved draft into the registered set |

They run in that order. A brand is drafted, generated, checked, and only then
promoted — which is why the first three all work inside
[`../drafts/`](../drafts/) and only the last one writes to
[`../brands/`](../brands/).

The guides operate on the scripts and brand files documented in
[`../asset-generation-scripts/README.md`](../asset-generation-scripts/README.md),
[`../brands/README.md`](../brands/README.md) and
[`../drafts/README.md`](../drafts/README.md). They are instructions, not
additional executables.
