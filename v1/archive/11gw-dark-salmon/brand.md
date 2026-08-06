# gw.rj11.io

The `11gw` site. This file is candidate `salmon` in the 11gw **dark-mode**
round: six variants on `#0A0A0A`, none of them chosen yet. A separate
light-mode round of six exists as `11gw-light-*`.

## Palette decision

Mode dark. Signal `#F98A80` on ground `#0A0A0A`: **8.46:1**.

Salmon. A soft, warm red — clearly distinct from 11intel without leaving the red family.

**11intel owns dark red, and that is what this round has to work around.** Its
`#EF4444` is exactly where a dark-mode red brand naturally lands, so every
canonical red is too close to use: carmine `#E63946` measures CIEDE2000 **3.8**
from it, clay `#DE6B5E` 7.1, red 600 `#DC2626` 7.6, coral `#FF6B5A` 8.4,
vermilion `#FF5533` 8.5. Clearing it means moving toward rose, salmon or
terracotta rather than staying on pure red. Contrast is not the constraint here:
every candidate clears 5.3:1 on the ground.

The three numbers for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#0A0A0A` | 8.46:1 |
| ink (the numeral beside the square) | `#FAFAFA` | 2.24:1 |
| footer grey | `#A1A1A1` | 1.10:1 |

Nearest brand sharing this ground: `11blog-11intel`, CIEDE2000 **14.4**. Every
candidate here is chromatic, so the footer ratio binds none of them; it would
only bind a neutral signal, which has no hue to separate it from de-emphasised
text.

The full round, for comparison:

| Candidate | Signal | On ground | On ink | On footer | dE to nearest |
| --- | --- | --- | --- | --- | --- |
| red300 — red 300 | `#FCA5A5` | 10.43:1 | 1.82:1 | 1.36:1 | 18.2 (11blog-11brands) |
| salmon — salmon | `#F98A80` | 8.46:1 | 2.24:1 | 1.10:1 | 14.4 (11blog-11intel) |
| red400 — red 400 | `#F87171` | 7.16:1 | 2.65:1 | 1.07:1 | 9.8 (11blog-11intel) |
| rose400 — rose 400 | `#FB7185` | 7.36:1 | 2.58:1 | 1.04:1 | 13.0 (11blog-11brands) |
| raspberry — raspberry | `#F0416C` | 5.35:1 | 3.54:1 | 1.43:1 | 11.2 (11blog-11intel) |
| terracotta — terracotta | `#E77E63` | 7.13:1 | 2.66:1 | 1.07:1 | 12.0 (11blog-11intel) |

## Notes

dE 14.4 from 11intel with a workable 2.24:1 against the ink. The best-balanced candidate in the round if the brand wants to stay recognisably red rather than shifting to rose or terracotta.

Domain `gw.rj11.io` follows the family pattern and is an assumption; change
`config.json` if the site lands elsewhere. The base key `11gw` is
deliberately not registered yet — it gets created from whichever candidate wins
across both the light and dark rounds, and the losers go to `archive/` with
their keys reserved.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
