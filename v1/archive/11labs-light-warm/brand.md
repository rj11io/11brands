# labs.rj11.io

Test variant for 11labs (labs.rj11.io) — a light-mode orange identity of its own; 11io's dark orange was the reference for the direction, not a template. Four candidates: a depth ramp on the standard light ground, plus a warm-ground character option.

## Palette decision

Mode light. Signal `#C2410C` on ground `#FAF8F6`: **4.89:1**.

Orange 700 on a warm ground `#FAF8F6` with warm-dark ink `#0C0907` (4.89:1). The character option: the whole canvas warms up instead of only the signal, giving 11labs a texture no other light brand has. Costs two colour overrides in the config.

## Notes

If chosen, note the family precedent: a warm ground with the standard cool footer grey `#676767` is the same footer-off-the-ground-ink-line quirk 11io carries; the footer may deserve a warm value too. Check with the verify skill's four-colour section. Orange 500 `#F97316` (2.69:1, fails the floor) was never a candidate. No 16px collision risk: the active light brands are green and blue, and 11io's orange lives on a dark ground. Domain labs.rj11.io is an assumption; change config.json if it lands elsewhere. Once a winner is picked, promote it to the plain `11labs` key and archive the rest.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
