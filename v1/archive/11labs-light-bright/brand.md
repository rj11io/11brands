# labs.rj11.io

Test variant for 11labs (labs.rj11.io) — a light-mode orange identity of its own; 11io's dark orange was the reference for the direction, not a template. Four candidates: a depth ramp on the standard light ground, plus a warm-ground character option.

## Palette decision

Mode light. Signal `#EA580C` on ground `#FAFAFA`: **3.41:1**.

Orange 600. The brightest legal orange on this ground and the closest in feel to the reference. **Floor-only: 3.41:1** clears the 3:1 minimum for a non-text graphic but misses the 4.5:1 aim — the same margin band that v0 rejected for gold. Choosing it means the colour can never be set in type and any ground tweak breaks it. A legitimate candidate only with that accepted.

## Notes

Orange 500 `#F97316` (2.69:1, fails the floor) was never a candidate. No 16px collision risk: the active light brands are green and blue, and 11io's orange lives on a dark ground. Domain labs.rj11.io is an assumption; change config.json if it lands elsewhere. Once a winner is picked, promote it to the plain `11labs` key and archive the rest.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
