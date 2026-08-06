# pc.rj11.io

The `11pc` site. This file is candidate `amber600` in the first 11pc colour
round: six light-mode yellow variants, none of them chosen yet.

## Palette decision

Mode light. Signal `#D97706` on ground `#FAFAFA`: **3.05:1**.

Amber 600. The brightest candidate that clears the floor at all, and the closest thing to a real amber in the round.

**Yellow is the hard case on a light ground, and it shaped this whole round.**
A bright yellow simply cannot clear the 3:1 floor on `#FAFAFA`: yellow 400
`#FACC15` measures 1.47:1, yellow 500 `#EAB308` 1.84:1, yellow 600 `#CA8A04`
2.81:1. All three fail. Anything that passes has to be dark enough to read as
gold, amber or mustard rather than as yellow. Three of the six candidates are
therefore deliberately floor-only (3:1 to 4.5:1), kept in the round so the
brightness-against-contrast trade is an explicit choice rather than a
constraint applied silently. 11support made the same trade at 3.38:1.

The three numbers for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#FAFAFA` | 3.05:1 |
| ink (the numeral beside the square) | `#0A0A0A` | 6.21:1 |
| footer grey | `#676767` | 1.78:1 |

Nearest active brand: `11blog-11labs`, CIEDE2000 **11.6**. Every candidate in this
round is a chromatic signal, so the footer ratio does not bind any of them; it
would only bind a neutral, which has no hue to separate it from de-emphasised
text.

The full round, for comparison:

| Candidate | Signal | On ground | On ink | On footer | Verdict |
| --- | --- | --- | --- | --- | --- |
| amber600 — amber 600 | `#D97706` | 3.05:1 | 6.21:1 | 1.78:1 | floor-only |
| brass — brass, yellow 650-ish | `#B08900` | 3.13:1 | 6.06:1 | 1.73:1 | floor-only |
| gold — gold, yellow 700 darkened | `#9F7A00` | 3.83:1 | 4.96:1 | 1.42:1 | floor-only |
| mustard — mustard, yellow 750-ish | `#8A6D0B` | 4.71:1 | 4.03:1 | 1.15:1 | clears the 4.5:1 aim |
| amber700 — amber 700 | `#B45309` | 4.81:1 | 3.94:1 | 1.13:1 | clears the 4.5:1 aim |
| yellow800 — yellow 800 | `#854D0E` | 6.56:1 | 2.89:1 | 1.21:1 | clears the 4.5:1 aim |

## Notes

Floor-only at 3.05:1, the lowest of any candidate here and lower than any active brand in the family (11support sits at 3.38). Never set this in type. It is also the closest of the six to 11labs' orange 600, at dE 11.6, which is workable but the tightest pairing in this round.

Domain `pc.rj11.io` follows the family pattern and is an assumption; change
`config.json` if the site lands elsewhere. The base key `11pc` is
deliberately not registered yet — it gets created from whichever candidate wins,
and the other five go to `archive/` with their keys reserved.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
