# pc.rj11.io

The `11pc` site. This file is candidate `gold600` in the 11pc **dark-mode**
round: six variants on `#0A0A0A`, none of them chosen yet. A separate
light-mode round of six exists as `11pc-light-*`.

## Palette decision

Mode dark. Signal `#C9A227` on ground `#0A0A0A`: **8.18:1**.

Gold 600. A muted, slightly desaturated gold: the least saturated candidate in the round.

**Dark mode inverts the yellow problem, and then adds a second one.** On the
light ground, yellow failed the contrast floor and every candidate had to be
dark. Here contrast is free — the whole round sits between 6.74:1 and 10.31:1 —
and two other constraints bind instead:

- **11b2b already owns bright yellow on dark.** Its amber 400 `#FBBF24` sits
  exactly where a dark-mode yellow brand naturally lands. Amber 450 `#F0B429`
  measures CIEDE2000 **3.1** from it, mustard `#D4B106` **8.0**, saffron
  `#E8A317` **7.7** — all too close to ship as a separate brand.
- **The ink is now near-white, and so are pale yellows.** On `#0A0A0A` the
  numeral is `#FAFAFA`, and the accent square sits right beside it. Yellow 200
  `#FEF08A` measures only **1.11:1** against that ink, lemon `#F2E85C` 1.22:1,
  chartreuse `#C7E22A` 1.40:1, citron `#D8E020` 1.38:1. The family's chromatic
  signals sit at 1.6:1 to 3.6:1; below that the square stops reading as a
  separate shape.

Those two push in opposite directions: getting clear of 11b2b wants paler or
greener, keeping the square distinct from the numeral wants darker. Only the
middle band satisfies both, and that is what this round explores.

The three numbers for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#0A0A0A` | 8.18:1 |
| ink (the numeral beside the square) | `#FAFAFA` | 2.32:1 |
| footer grey | `#A1A1A1` | 1.07:1 |

Nearest brand sharing this ground: `11b2b`, CIEDE2000 **10.2**. Every
candidate here is chromatic, so the footer ratio binds none of them; it would
only bind a neutral signal, which has no hue to separate it from de-emphasised
text.

The full round, for comparison:

| Candidate | Signal | On ground | On ink | On footer | dE to nearest |
| --- | --- | --- | --- | --- | --- |
| amber500 — amber 500 | `#F59E0B` | 9.22:1 | 2.06:1 | 1.20:1 | 10.6 (11b2b) |
| gold600 — gold 600 | `#C9A227` | 8.18:1 | 2.32:1 | 1.07:1 | 10.2 (11b2b) |
| yellow600 — yellow 600 | `#CA8A04` | 6.74:1 | 2.81:1 | 1.14:1 | 15.0 (11b2b) |
| brass600 — brass 600 | `#BFA100` | 7.84:1 | 2.42:1 | 1.02:1 | 12.1 (11b2b) |
| citron600 — citron 600 | `#B8C400` | 10.31:1 | 1.84:1 | 1.35:1 | 18.3 (11b2b) |
| olive500 — olive 500 | `#9CAF00` | 8.06:1 | 2.35:1 | 1.05:1 | 21.6 (11b2b) |

## Notes

dE 10.2 from 11b2b, effectively tied with amber 500 as the closest in the round. The muting is what separates it visually rather than the hue, which is a weaker kind of separation at small sizes.

Domain `pc.rj11.io` follows the family pattern and is an assumption; change
`config.json` if the site lands elsewhere. The base key `11pc` is
deliberately not registered yet — it gets created from whichever candidate wins
across both the light and dark rounds, and the losers go to `archive/` with
their keys reserved.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
