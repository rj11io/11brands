# archive.rj11.io

The archive site. A light-mode teal identity, the family's first.

## Palette decision

Mode light. Signal `#0F766E` on ground `#FAFAFA`: **5.24:1**.

Teal 700, the winner of a ten-variant light-mode round, chosen by the operator.
Clears the 3:1 floor for a non-text graphic and the 4.5:1 aim, with room to
spare, so it can also be set in type on this ground if wanted.

| Candidate | Signal | On ground | On ink | On footer |
| --- | --- | --- | --- | --- |
| teal 700 — **chosen** | `#0F766E` | 5.24:1 | 3.62:1 | 1.03:1 |
| violet 700 | `#6D28D9` | 6.81:1 | 2.79:1 | 1.26:1 |
| purple 700 | `#7E22CE` | 6.69:1 | 2.84:1 | 1.23:1 |
| purple 800 | `#6B21A8` | 8.35:1 | 2.27:1 | 1.54:1 |
| indigo 600 | `#4F46E5` | 6.02:1 | 3.15:1 | 1.11:1 |
| indigo 700 | `#4338CA` | 7.57:1 | 2.51:1 | 1.40:1 |
| lime 700 | `#4D7C0F` | 4.78:1 | 3.96:1 | 1.13:1 |
| slate 600 | `#475569` | 7.26:1 | 2.61:1 | 1.34:1 — neutral, fails the footer check |
| amber 900 | `#78350F` | 8.69:1 | 2.18:1 | 1.60:1 |
| yellow 700 | `#A16207` | 4.72:1 | 4.02:1 | 1.15:1 |

Every candidate cleared both thresholds, so contrast did not decide the round.
The ten variants live in `../../archive/` as `11archive-light-*`.

## Notes

**11ai is the one neighbour that matters, and it is close.** 11ai carries
`#007A55` on the same `#FAFAFA` ground, so the two share a context:

- CIEDE2000 distance **10.3** — well past the roughly 2.3 at which a difference
  becomes visible, but by far the closest pair in the family (the next nearest
  is 11blog's emerald at 28.5, and that one sits on a dark ground)
- lightness is effectively identical: Lab L 44.5 against 45.0, a WCAG ratio of
  **1.02:1** between the two signals
- the separation is therefore **entirely hue**: 186.7 degrees against 162.4,
  teal against emerald

Two consequences worth carrying:

- a greyscale or monochrome rendering of these two marks is indistinguishable,
  because only hue tells them apart
- if 11ai's signal is ever restyled, recheck this pair before shipping

The other risk in the round, slate 600, was rejected on the neutral three-check:
1.34:1 against the footer grey `#676767`, with no hue to separate the accent
square from de-emphasised text.

Domain `archive.rj11.io` follows the family pattern and has not been confirmed;
change `config.json` if the site lands elsewhere.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
