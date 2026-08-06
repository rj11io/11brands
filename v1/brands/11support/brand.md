# support.rj11.io

The support site — a light-mode bright pink identity.

## Palette decision

Mode light. Signal `#EC4899` on ground `#FAFAFA`: **3.38:1**.

Pink 500, the winner of two candidate rounds (eight variants), chosen by the
operator for the bright-pink feel. Chosen over:

| Candidate | Signal | Contrast |
| --- | --- | --- |
| pink 500 — **chosen** | `#EC4899` | 3.38:1 |
| pink 600 | `#DB2777` | 4.40:1 |
| pink 700 | `#BE185D` | 5.78:1 |
| rose 500 | `#F43F5E` | 3.52:1 |
| rose 700 | `#BE123C` | 6.02:1 |
| fuchsia 500 | `#D946EF` | 3.31:1 |
| fuchsia 700 | `#A21CAF` | 6.06:1 |
| pink 400 (11brands' hex) | `#F472B6` | 2.54:1 — fails the floor |

All eight candidates live in `../../archive/` once archived (rounds one and two,
`11support-light-*`).

## Notes

**This signal is floor-only, by explicit decision.** 3.38:1 clears the 3:1
minimum for a non-text graphic but misses the 4.5:1 aim by more than any other
active brand (11labs sits at 3.41). Accepted for the bright feel. Binding
consequences for every consumer:

- this pink must **never be set as text** on this ground — mark and non-text
  graphics only
- the ground is load-bearing: recheck the number before touching
  `colors.ground`

Hue neighbours: 11brands carries pink 400 on a dark ground (never the same
context); the nearest light-mode active is 11labs' orange 600, distinguishable
at 16px but both warm and bright — worth a side-by-side if either ever changes.
Domain support.rj11.io is an assumption; change config.json if it lands
elsewhere.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
