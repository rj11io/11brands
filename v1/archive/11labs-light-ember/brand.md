# labs.rj11.io

Test variant for 11labs (labs.rj11.io) — a light-mode orange identity of its own; 11io's dark orange was the reference for the direction, not a template. Four candidates: a depth ramp on the standard light ground, plus a warm-ground character option.

## Palette decision

Mode light. Signal `#9A3412` on ground `#FAFAFA`: **7.00:1**.

Orange 800 at 7.00:1. Deep ember; the most contrast headroom of the four, and the most it departs from the bright-orange feel of the reference.

## Notes

Orange 500 `#F97316` (2.69:1, fails the floor) was never a candidate. No 16px collision risk: the active light brands are green and blue, and 11io's orange lives on a dark ground. Domain labs.rj11.io is an assumption; change config.json if it lands elsewhere. Once a winner is picked, promote it to the plain `11labs` key and archive the rest.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
