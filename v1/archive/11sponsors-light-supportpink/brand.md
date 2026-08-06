# sponsors.rj11.io

The `11sponsors` site. This file is candidate `supportpink` in the first
11sponsors colour round: twelve light-mode variants, six pink and six green,
none of them chosen yet.

## Palette decision

Mode light. Signal `#EC4899` on ground `#FAFAFA`: **3.38:1**.

Pink 500. Requested explicitly: 11support's exact signal.

**The family is already dense with pink.** Twelve registry entries sit in the
pink-to-magenta band, and one of them — 11support's `#EC4899` — is an active
light-ground brand, the same context this round targets. So separation from
11support, not contrast, is what this round is really deciding. One candidate
(`supportpink`) shares that colour exactly, on purpose, because it was asked
for.

The three numbers for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#FAFAFA` | 3.38:1 |
| ink (the numeral beside the square) | `#0A0A0A` | 5.61:1 |
| footer grey | `#676767` | 1.60:1 |

Measured against `11support / 11blog-11support`, the brand this half of the
round has to clear: CIEDE2000 **0.0**. Every candidate here is chromatic, so
the footer ratio binds none of them; it would only bind a neutral signal,
which has no hue to separate it from de-emphasised text.

The pink half of the round, brightest to deepest:

| Candidate | Signal | On ground | On ink | On footer | dE to rival | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| supportpink — pink 500 | `#EC4899` | 3.38:1 | 5.61:1 | 1.60:1 | 0.0 | floor-only |
| fuchsia600 — fuchsia 600 | `#C026D3` | 4.51:1 | 4.20:1 | 1.20:1 | 17.7 | clears the 4.5:1 aim |
| raspberry — raspberry | `#C13B72` | 4.86:1 | 3.90:1 | 1.11:1 | 11.0 | clears the 4.5:1 aim |
| mulberry — mulberry | `#A34A78` | 5.28:1 | 3.59:1 | 1.03:1 | 14.7 | clears the 4.5:1 aim |
| plum — plum | `#8E3B6B` | 6.73:1 | 2.82:1 | 1.24:1 | 20.5 | clears the 4.5:1 aim |
| pink900 — pink 900 | `#831843` | 9.24:1 | 2.05:1 | 1.71:1 | 26.6 | clears the 4.5:1 aim |

## Notes

**This candidate is not merely close to 11support — it is 11support.** The
same hex, on the same `#FAFAFA` ground: CIEDE2000 **0.0**, already carried by
`11support`, `11blog-11support` and the archived `11support-light-pink500`.

Contrast is not the problem. At 3.38:1 it clears the 3:1 floor, and 11support
ships at exactly this number today. The problem is identity: if this wins,
11sponsors and 11support have the same mark in the same colour on the same
ground, and nothing but the wordmark tells them apart. Their favicon packs
would be byte-identical.

It is in the round because it was asked for, so the comparison can show what
sharing 11support's pink actually looks like. `raspberry` at dE 11.0 is the
nearest candidate here that keeps the pink while being its own colour.

Domain `sponsors.rj11.io` follows the family pattern and is an assumption;
change `config.json` if the site lands elsewhere. The base key `11sponsors` is
deliberately not registered yet — it gets created from whichever candidate
wins, and the other eleven go to `archive/` with their keys reserved.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
