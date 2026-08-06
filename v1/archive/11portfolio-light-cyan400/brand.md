# portfolio.rj11.io

The `11portfolio` site. This file is candidate `cyan400` in the 11portfolio
colour round, which now holds ten light-mode blue variants. None chosen yet.

## Palette decision

Mode light. Signal `#22D3EE` on ground `#FAFAFA`: **1.73:1**.

Cyan 400. Requested explicitly: this is 11bench's live signal, carried onto a
light ground.

**11cv already owns blue on this exact ground.** Its blue 600 `#2563EB` is a
light-mode signal, so a light-mode blue portfolio brand competes with it
head-on — the tightest starting position of any round so far. Three otherwise
good blues were excluded for sitting too close to it:

| Excluded | Signal | Reason |
| --- | --- | --- |
| blue 600 | `#2563EB` | 11cv's exact signal |
| azure | `#0B69C7` | CIEDE2000 6.5 from 11cv |
| blue 700 | `#1D4ED8` | CIEDE2000 7.1 from 11cv |
| indigo 600 | `#4F46E5` | duplicate of the archived `11archive-light-indigo` |

The nine passing candidates all sit at CIEDE2000 8.9 or better from 11cv.

The three numbers for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#FAFAFA` | 1.73:1 |
| ink (the numeral beside the square) | `#0A0A0A` | 10.96:1 |
| footer grey | `#676767` | 3.13:1 |

Nearest active brand on this ground: `11archive`, CIEDE2000 **31.6**. Every
candidate here is chromatic, so the footer ratio binds none of them; it would
only bind a neutral signal, which has no hue to separate it from de-emphasised
text.

The full round, for comparison:

| Candidate | Signal | On ground | On ink | On footer | dE to 11cv | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| cyan400 — cyan 400 | `#22D3EE` | 1.73:1 | 10.96:1 | 3.13:1 | 31.6 | **fails the 3:1 floor** |
| dodger — dodger blue | `#1E90FF` | 3.10:1 | 6.12:1 | 1.75:1 | 16.2 | floor-only |
| blue500 — blue 500 | `#3B82F6` | 3.52:1 | 5.38:1 | 1.54:1 | 10.9 | floor-only |
| cyan600 — cyan 600 | `#0891B2` | 3.53:1 | 5.38:1 | 1.54:1 | 22.8 | floor-only |
| sky600 — sky 600 | `#0284C7` | 3.92:1 | 4.83:1 | 1.38:1 | 14.8 | floor-only |
| sky700 — sky 700 | `#0369A1` | 5.68:1 | 3.34:1 | 1.05:1 | 11.3 | clears the 4.5:1 aim |
| cerulean — cerulean | `#17638F` | 6.25:1 | 3.03:1 | 1.15:1 | 12.0 | clears the 4.5:1 aim |
| cobalt — cobalt | `#1552B5` | 6.92:1 | 2.74:1 | 1.28:1 | 8.9 | clears the 4.5:1 aim |
| ultramarine — ultramarine | `#2B3FBF` | 7.84:1 | 2.42:1 | 1.45:1 | 12.5 | clears the 4.5:1 aim |
| blue900 — blue 900 | `#1E3A8A` | 9.92:1 | 1.91:1 | 1.83:1 | 17.5 | clears the 4.5:1 aim |

## Notes

**This candidate fails the contrast floor and is in the round on purpose.**
1.73:1 against `#FAFAFA` misses the 3:1 minimum for a non-text graphic by a
wide margin — the largest miss of any candidate the project has considered
(11support's rejected pink 400 measured 2.54:1). `init_brand.py` printed the
warning when it was created.

It is here because it was asked for, so the round can show what 11bench's cyan
actually looks like on a light ground rather than argue about it. Two things
follow if it wins:

- the mark would be low-contrast at every size, and unusable at 16px against a
  white browser tab
- it duplicates `11bench`'s signal exactly, so the two brands would share a
  colour and differ only by ground

`sky700` in this same round is the closest passing relative if the cyan
direction is what appeals. Note the inverted numbers: this is the only
candidate
whose contrast against the ink (10.96:1) and the footer grey (3.13:1) is high
while its ground contrast is low, because it is a bright colour on a bright
ground.

Domain `portfolio.rj11.io` follows the family pattern and is an assumption;
change `config.json` if the site lands elsewhere. The base key `11portfolio`
is
deliberately not registered yet — it gets created from whichever candidate
wins,
and the other nine go to `archive/` with their keys reserved.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the
assets.
