# sponsors.rj11.io

The `11sponsors` site. This file is candidate `fern` in the first 11sponsors
colour round: twelve light-mode variants, six pink and six green, none of them
chosen yet.

## Palette decision

Mode light. Signal `#2F7D32` on ground `#FAFAFA`: **4.91:1**.

Fern. A mid-depth true green, the first in this round to clear the 4.5:1 aim.

**11ai already owns green on this exact ground.** Its `#007A55` is an active
light-mode signal, so a light-mode green brand competes with it directly, the
same way 11portfolio's blues compete with 11cv. Two otherwise good greens were
excluded for sitting on top of it: emerald 700 `#047857` at CIEDE2000 **1.3**,
and pine `#0B6E4F` at **4.3**. One candidate (`bloggreen`) is 11blog's exact
signal, included on purpose because it was asked for, and it fails the floor
on this ground.

The three numbers for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#FAFAFA` | 4.91:1 |
| ink (the numeral beside the square) | `#0A0A0A` | 3.87:1 |
| footer grey | `#676767` | 1.10:1 |

Measured against `11ai`, the brand this half of the round has to clear:
CIEDE2000 **9.9**. Every candidate here is chromatic, so the footer ratio
binds none of them; it would only bind a neutral signal, which has no hue to
separate it from de-emphasised text.

The green half of the round, brightest to deepest:

| Candidate | Signal | On ground | On ink | On footer | dE to rival | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| bloggreen — emerald 400 | `#2BC88F` | 2.06:1 | 9.20:1 | 2.63:1 | 24.7 | **fails the 3:1 floor** |
| green600 — green 600 | `#16A34A` | 3.16:1 | 6.01:1 | 1.72:1 | 17.0 | floor-only |
| emerald600 — emerald 600 | `#059669` | 3.61:1 | 5.25:1 | 1.50:1 | 10.1 | floor-only |
| fern — fern | `#2F7D32` | 4.91:1 | 3.87:1 | 1.10:1 | 9.9 | clears the 4.5:1 aim |
| moss — moss | `#3F6212` | 6.78:1 | 2.80:1 | 1.25:1 | 16.5 | clears the 4.5:1 aim |
| forest — forest | `#14532D` | 8.73:1 | 2.17:1 | 1.61:1 | 13.3 | clears the 4.5:1 aim |

## Notes

dE 9.9 from 11ai is the tightest in this round, and the two share the light
ground, so they will genuinely co-occur. Comparable to the dE 10.3 that
11archive accepted against 11ai, but slightly tighter — check the pair at 16px
before choosing it.

Domain `sponsors.rj11.io` follows the family pattern and is an assumption;
change `config.json` if the site lands elsewhere. The base key `11sponsors` is
deliberately not registered yet — it gets created from whichever candidate
wins, and the other eleven go to `archive/` with their keys reserved.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
