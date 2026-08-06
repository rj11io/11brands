# support.rj11.io

Bright-pink test variant for 11support (support.rj11.io), round two — the brighter end of the space after the first four (bright/pink/rose/magenta at 600-700 steps).

## Palette decision

Mode light. Signal `#F472B6` on ground `#FAFAFA`: **2.54:1**.

Pink 400 `#F472B6` — **the same pink 11brands carries**, included by explicit operator request for the cross-brand pairing. **It FAILS the 3:1 floor on this ground: 2.54:1.** This is the exact failure mode v0's ai.rj11.io actually shipped with (dark-mode green on light at 2.06:1) before it was caught. As specced, this candidate is not usable for a real brand; it exists to be seen and compared.

## Notes

If the pairing idea survives, the honest paths are: darken the ground until 3:1 clears, or keep the hue and step down (pink 600/700 — see round one). 11brands itself runs this hex on a dark ground at 7.48:1, where it is legal. Round-one candidates (pink 600/700, rose 700, fuchsia 700) hold the honest end of the range. Domain support.rj11.io is an assumption. Once a winner is picked, promote it to the plain `11support` key and archive the rest.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
