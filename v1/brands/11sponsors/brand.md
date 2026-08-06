# sponsors.rj11.io

The sponsors site. A light-mode brand carrying 11blog's emerald.

## Palette decision

Mode light. Signal `#2BC88F` on ground `#FAFAFA`: **2.06:1**.

Emerald 400, the winner of a twelve-variant round (six pink, six green), chosen
by the operator. It is 11blog's exact signal moved onto a light ground.

**This signal is below the contrast floor, by explicit decision.** 2.06:1 misses
the 3:1 minimum for a non-text graphic. `init_brand.py` prints a warning every
time this brand is initialised, and that warning is correct — it is not a false
positive to be silenced. Recorded here so nobody later "fixes" the number
without knowing it was chosen.

Where it sits in the family:

| Brand | Signal on ground | Contrast |
| --- | --- | --- |
| **11sponsors** | `#2BC88F` on `#FAFAFA` | **2.06:1** — below the floor |
| 11support | `#EC4899` on `#FAFAFA` | 3.38:1 — floor-only, by decision |
| 11labs | `#EA580C` on `#FAFAFA` | 3.41:1 — floor-only |
| every other brand | — | 4.95:1 or better |

It is the lowest-contrast brand in the family by a margin of 1.32, and the only
one below the floor rather than merely below the 4.5:1 aim.

The round it won, for the record:

| Candidate | Signal | On ground | Verdict |
| --- | --- | --- | --- |
| bloggreen — **chosen** | `#2BC88F` | 2.06:1 | fails the 3:1 floor |
| green 600 | `#16A34A` | 3.16:1 | floor-only |
| emerald 600 | `#059669` | 3.61:1 | floor-only |
| fern | `#2F7D32` | 4.91:1 | clears the aim |
| moss | `#3F6212` | 6.78:1 | clears the aim |
| forest | `#14532D` | 8.73:1 | clears the aim |
| pink 500 (11support's) | `#EC4899` | 3.38:1 | floor-only, and dE 0.0 from 11support |
| fuchsia 600 | `#C026D3` | 4.51:1 | clears the aim |
| raspberry | `#C13B72` | 4.86:1 | clears the aim |
| mulberry | `#A34A78` | 5.28:1 | clears the aim |
| plum | `#8E3B6B` | 6.73:1 | clears the aim |
| pink 900 | `#831843` | 9.24:1 | clears the aim |

The eleven losers live in `../../archive/` as `11sponsors-light-*`.
`emerald600` (`#059669`, 3.61:1) is the same hue stepped dark enough to pass, if
this decision is ever revisited.

## Notes

**Binding consequences for every consumer.** These follow from the number, not
from taste:

- this green must **never be set as text** on this ground, at any size — mark
  and non-text graphics only
- the 16px favicon is low-contrast against a white browser tab, which is the
  common case; expect the mark to read faintly there
- the ground is load-bearing. Recheck the contrast before touching
  `colors.ground`; a lighter ground makes it worse, and there is no headroom
  left to spend

**The numbers invert.** Because this is a bright colour on a bright ground, the
usual pattern reverses: contrast against the ink (`#0A0A0A`) is **9.20:1** and
against the footer grey **2.63:1**, both unusually high, while the ground number
is the weak one. The accent square separates from the numeral easily; it is the
background it struggles against.

**Shared hex with 11blog.** 11blog carries `#2BC88F` on `#0A0A0A`, where the
same colour measures 11.6:1. Same signal, opposite grounds. That is why this
works for 11blog and does not work here — the colour was never the problem, the
ground is. See [`../11blog-11sponsors/brand.md`](../11blog-11sponsors/brand.md)
for the sharper version of that problem.

Domain `sponsors.rj11.io` follows the family pattern and has not been confirmed;
change `config.json` if the site lands elsewhere.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
