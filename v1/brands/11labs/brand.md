# labs.rj11.io

The labs site — a light-mode orange identity of its own; 11io's dark orange was the direction reference, not a template.

## Palette decision

Mode light. Signal `#EA580C` on ground `#FAFAFA`: **3.41:1**.

Orange 600, the winner of a four-candidate round, chosen by the operator for
staying closest to the bright-orange feel of the reference. Chosen over:

| Candidate | Signal | Contrast |
| --- | --- | --- |
| orange 600 — **chosen** | `#EA580C` | 3.41:1 |
| orange 700 | `#C2410C` | 4.96:1 |
| orange 800 (ember) | `#9A3412` | 7.00:1 |
| orange 700 on warm ground (warm) | `#C2410C` on `#FAF8F6` | 4.89:1 |

Orange 500 `#F97316` (2.69:1) failed the floor and was never a candidate. All
four candidates are kept verbatim in `../../archive/11labs-light-*`, plus the
cross-mode experiment `../../archive/11io-dark-bright` (this same hex on 11io's
warm dark ground, 5.58:1).

## Notes

**This signal is floor-only, by explicit decision.** 3.41:1 clears the 3:1
minimum for a non-text graphic but misses the 4.5:1 aim — the margin band v0
rejected for gold. Accepted at selection time for the brighter feel. Two hard
consequences, binding on every consumer:

- this orange must **never be set as text** on this ground; it is legal only as
  the mark's square and other non-text graphics
- any later tweak to the ground eats the margin — recheck the number before
  touching `colors.ground`

Same hex as archived `11io-dark-bright`: if 11io ever adopts orange 600, the two
brands share one hue across modes, with the light side (this brand) carrying all
the contrast risk. Domain labs.rj11.io is an assumption; change config.json if
it lands elsewhere.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
