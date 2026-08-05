# labs.rj11.io

Test variant for 11labs (labs.rj11.io) — a light-mode orange identity of its own; 11io's dark orange was the reference for the direction, not a template. Four candidates: a depth ramp on the standard light ground, plus a warm-ground character option.

## Palette decision

Mode light. Signal `#C2410C` on ground `#FAFAFA`: **4.96:1**.

Orange 700, the first step that honestly clears the 4.5:1 aim (4.96:1). Reads as strong burnt orange rather than bright orange — the price every bright hue pays on a near-white ground; gold paid two steps in v0, orange pays one.

## Notes

Orange 500 `#F97316` (2.69:1, fails the floor) was never a candidate. No 16px collision risk: the active light brands are green and blue, and 11io's orange lives on a dark ground. Domain labs.rj11.io is an assumption; change config.json if it lands elsewhere. Once a winner is picked, promote it to the plain `11labs` key and archive the rest.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
