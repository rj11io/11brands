# bench.rj11.io

The bench site. The family's only dark-mode blue.

## Palette decision

Mode dark. Signal `#22D3EE` on ground `#0A0A0A`: **10.96:1**.

Cyan 400, the winner of a four-candidate round across the dark-mode blue arc.
Chosen by the operator over:

| Candidate | Signal | Contrast |
| --- | --- | --- |
| cyan 400 — **chosen** | `#22D3EE` | 10.96:1 |
| sky 400 | `#38BDF8` | 9.24:1 |
| blue 400 | `#60A5FA` | 7.79:1 |
| indigo 400 | `#818CF8` | 6.64:1 |

Blue 500 `#3B82F6` (5.38:1) was dropped before the round: it tests depth, not
hue. All four candidates are kept verbatim in `../../archive/11bench-dark-*`.

## Notes

Cyan is the closest active signal to 11blog's green-teal `#2BC88F` at 16 pixels
— the closest pair on the board. The side-by-side favicon check was run before
selection and the two are distinguishable (cyan leans clearly blue), but if the
family ever gains another colour in the teal region, this pair is where the
crowding starts. Accepted at selection time.

11cv also carries blue (`#2563EB`), but on a light ground — the two never share
a context.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
