# b2b.rj11.io

The business-facing site. This file is candidate `honeyamber` in a small
round of four: four gold tones on the same dark ground `#0A0A0A`, all aiming
for a richer, more premium gold than the current live brand. None is chosen
yet; the other three are `11b2b-royalgold`, `11b2b-antiquegold` and
`11b2b-champagne`.

## Palette decision

Mode dark (unchanged from the live brand). Signal `#D97706` on ground
`#0A0A0A`: **6.21:1**.

`#D97706` is amber 600 on the standard Tailwind-style colour scale — noticeably
deeper and warmer than the live brand's amber 400 (`#FBBF24`), with enough
orange in it to read as honey, aged whiskey, or bronze rather than bright
yellow. It is the warmest candidate in the round and the furthest from
"yellow" in hue, which is the other lever for "premium" besides brightness:
depth and warmth, not just richness of tone.

The round was scored on three numbers, using the same method the rest of the
family uses:

- **Contrast against the dark ground** — how well the colour stands out from
  near-black. The web accessibility floor for a graphic (not running text) is
  3:1; this clears it twice over.
- **Contrast against the ink** — the near-white `#FAFAFA` used for the numeral
  next to the gold square. Too close and the square stops looking like a
  separate shape. At 3.05:1 this sits comfortably inside the family's usual
  range.
- **CIEDE2000 ("dE")** — a single number for how different two colours look to
  a human eye, calibrated so that roughly "dE 1" is the smallest gap most
  people can spot and anything past dE 10 reads as a clearly different colour.
  Used here to check this gold doesn't collide with the live `#FBBF24` or with
  any other brand's colour on the same ground.

| Measured against | Colour | Result |
| --- | --- | --- |
| ground | `#0A0A0A` | 6.21:1 |
| ink (the numeral beside the square) | `#FAFAFA` | 3.05:1 |
| footer grey | `#A1A1A1` | 1.23:1 |
| live 11b2b signal | `#FBBF24` | dE 22.2 |

Nearest other live brand on this ground is `11intel` (a red), at dE 24.5 —
comfortably clear, though this is the only candidate in the round whose
nearest neighbour isn't the grey `11cc`; the shift toward orange moves it
closer to red territory than the other three golds sit. The footer ratio
doesn't bind here: it only matters for a signal with no hue of its own
(silver, grey), and this candidate has plenty of hue to separate it from
de-emphasised footer text.

The full round, for comparison:

| Candidate | Signal | On ground | On ink | On footer | dE vs live 11b2b |
| --- | --- | --- | --- | --- | --- |
| royalgold — the reference "gold" | `#D4AF37` | 9.42:1 | 2.01:1 | 1.23:1 | 7.8 |
| antiquegold — dark goldenrod, deeper and more muted | `#B8860B` | 6.08:1 | 3.12:1 | 1.26:1 | 17.0 |
| champagne — pale, soft, elegant | `#DCB863` | 10.45:1 | 1.82:1 | 1.36:1 | 8.8 |
| honeyamber — deep, warm, closer to bronze | `#D97706` | 6.21:1 | 3.05:1 | 1.23:1 | 22.2 |

## Notes

This is the furthest the round moves in dE from the live colour (22.2) and the
only candidate that shifts hue toward orange rather than staying on the
yellow-gold line the other three share. It reads as the most distinct new
brand of the four rather than a refinement of the current one — worth
weighing against `11intel`'s red directly if the two ever appear side by side,
since dE 24.5 is comfortable but not huge.

Domain, layout, and everything except the signal colour are carried over
unchanged from the live `11b2b` brand. Nothing here is generated yet — this
is the decision record only.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
