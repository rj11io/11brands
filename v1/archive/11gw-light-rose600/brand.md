# gw.rj11.io

The `11gw` site. This file is candidate `rose600` in the first 11gw colour
round: six light-mode red variants, none of them chosen yet.

## Palette decision

Mode light. Signal `#E11D48` on ground `#FAFAFA`: **4.50:1**.

Rose 600. The brightest candidate and the only pink-leaning one.

Red behaves far better than yellow on a light ground: every candidate in this
round clears both the 3:1 floor and the 4.5:1 aim, so contrast does not decide
it. Separation from 11labs' orange and 11support's pink does, along with how
deep a red the brand wants.

The three numbers for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#FAFAFA` | 4.50:1 |
| ink (the numeral beside the square) | `#0A0A0A` | 4.21:1 |
| footer grey | `#676767` | 1.20:1 |

Nearest active brand: `11blog-11support`, CIEDE2000 **17.7**. Every candidate in this
round is a chromatic signal, so the footer ratio does not bind any of them; it
would only bind a neutral, which has no hue to separate it from de-emphasised
text.

The full round, for comparison:

| Candidate | Signal | On ground | On ink | On footer | Verdict |
| --- | --- | --- | --- | --- | --- |
| rose600 — rose 600 | `#E11D48` | 4.50:1 | 4.21:1 | 1.20:1 | clears the 4.5:1 aim |
| red600 — red 600 | `#DC2626` | 4.63:1 | 4.10:1 | 1.17:1 | clears the 4.5:1 aim |
| crimson — crimson | `#C81E1E` | 5.50:1 | 3.45:1 | 1.01:1 | clears the 4.5:1 aim |
| red700 — red 700 | `#B91C1C` | 6.20:1 | 3.06:1 | 1.14:1 | clears the 4.5:1 aim |
| rose800 — rose 800 | `#9F1239` | 7.68:1 | 2.47:1 | 1.47:1 | clears the 4.5:1 aim |
| red800 — red 800 | `#991B1B` | 7.96:1 | 2.38:1 | 1.47:1 | clears the 4.5:1 aim |

## Notes

Sits exactly on the 4.5:1 aim, so it has no headroom: any future change to the ground breaks it. Nearest active brand is 11support's pink 500 at dE 17.7, comfortably separated but the relevant pairing to check, since both are bright and light-ground.

Domain `gw.rj11.io` follows the family pattern and is an assumption; change
`config.json` if the site lands elsewhere. The base key `11gw` is
deliberately not registered yet — it gets created from whichever candidate wins,
and the other five go to `archive/` with their keys reserved.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
