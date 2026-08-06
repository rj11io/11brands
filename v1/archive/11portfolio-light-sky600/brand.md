# portfolio.rj11.io

The `11portfolio` site. This file is candidate `sky600` in the 11portfolio
colour round, which now holds ten light-mode blue variants. None chosen yet.

## Palette decision

Mode light. Signal `#0284C7` on ground `#FAFAFA`: **3.92:1**.

Sky 600. One step brighter than `sky700`, and the best contrast in the bright
group.

**A bright blue cannot clear the 4.5:1 aim on this ground.** Four bright
candidates
were added to the round's original six, and together with the cyan 400 already
there they form a bright group of five that lands between 1.73:1 and 3.92:1.
That is not a shortage of options — it is the shape
of the problem. Brightening a blue on `#FAFAFA` costs contrast directly, and
the only bright blues that do clear the aim sit on top of 11cv:

| Bright blue that clears 4.5:1 | Signal | On ground | dE to 11cv |
| --- | --- | --- | --- |
| electric | `#0066FF` | 4.63:1 | 2.5 — indistinguishable from 11cv |
| lapis | `#1064C8` | 5.47:1 | 5.6 — too close |

So the bright half of this round is floor-only by necessity. Floor-only is a
real, precedented choice — 11support ships at 3.38:1 — but it binds the brand:

- the signal must **never be set as text** on this ground, mark and non-text
  graphics only
- the ground becomes load-bearing; recheck the number before touching
  `colors.ground`

The deep half of the round (`sky700` through `blue900`, 5.68:1 to 9.92:1) is
where the candidates that clear the aim live.

The three numbers for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#FAFAFA` | 3.92:1 |
| ink (the numeral beside the square) | `#0A0A0A` | 4.83:1 |
| footer grey | `#676767` | 1.38:1 |

Nearest active brand on this ground: `11cv` / `11blog-11cv` (`#2563EB`),
CIEDE2000 **14.8**. Every candidate here is chromatic, so the footer ratio
binds none of them.

The full round, brightest to deepest:

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

3.92:1 is the strongest of the five bright candidates, so if the round wants
brightness with the least contrast cost, this is it. dE 10.4 from `sky700`,
which is the pair to compare directly — they are the same hue one step apart.

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
