# blog.rj11.io

Blog-hosted content in the palette of `11sponsors`. The masthead stays
blog.rj11.io while the colours identify the leading brand.

## Palette decision

Mode light. Signal `#2BC88F` on ground `#FAFAFA`: **2.06:1**.

Colours are `11sponsors`'s emerald 400, unmodified — see that brand.md for the
twelve-variant round and for the below-floor caveat, which this brand inherits
in full. This key exists because content cards carry their consuming domain:
generating against `11sponsors` directly would put sponsors.rj11.io on a
blog.rj11.io asset.

## Notes

**This sub-brand carries 11blog's own signal, so it does not distinguish
anything.** That is worth stating plainly, because it defeats the purpose the
`{brand}-{sub-brand}` level exists for. Every other blog sub-brand announces
whose content it is by using a colour 11blog does not have:

| Key | Ground | Signal | Distinct from 11blog? |
| --- | --- | --- | --- |
| 11blog | `#0A0A0A` | `#2BC88F` | — it is 11blog |
| **11blog-11sponsors** | `#FAFAFA` | `#2BC88F` | **no — CIEDE2000 0.0, same hex** |
| 11blog-11ai | `#FAFAFA` | `#007A55` | yes, dE 24.7 |
| 11blog-11archive | `#FAFAFA` | `#0F766E` | yes, dE 28.5 |
| 11blog-11support | `#FAFAFA` | `#EC4899` | yes, far |

A reader seeing a sponsored card and an ordinary 11blog card sees the same green
accent on both. Only the ground differs — light against dark — so the signal
that says "this is sponsor content" is carried entirely by the background
colour, not by the accent. If sponsored content ever needs to be visually
distinguishable from ordinary blog content, this palette cannot do it, and the
fix is `11sponsors`' colour, not this file.

**The contrast caveat applies here too**, and matters more: this brand's cards
sit next to ordinary 11blog cards where the same green reads at 11.6:1 on dark.
Side by side, the light version will look washed out against the dark version's
crispness. Never set this green as text.

Favicon packs are byte-identical to `11sponsors`'s, so this brand usually only
needs og-content.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
