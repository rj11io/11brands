# b2b.rj11.io

The business-facing site. This file is candidate `royalgold` in a small
round of four: four gold tones on the same dark ground `#0A0A0A`, all aiming
for a richer, more premium gold than the current live brand. None is chosen
yet; the other three are `11b2b-antiquegold`, `11b2b-champagne` and
`11b2b-honeyamber`.

## Palette decision

Mode dark (unchanged from the live brand). Signal `#D4AF37` on ground
`#0A0A0A`: **9.42:1**.

`#D4AF37` is the colour most people picture when they hear the word "gold" —
it is the standard reference hex for metallic gold. That familiarity is the
point: next to the live brand's `#FBBF24` (a bright, lemon-leaning amber closer
to a warning-sign yellow than a precious metal), this reads immediately as
gold rather than yellow.

The round was scored on three numbers, using the same method the rest of the
family uses:

- **Contrast against the dark ground** — how well the colour stands out from
  near-black. The web accessibility floor for a graphic (not running text) is
  3:1; this clears it more than three times over.
- **Contrast against the ink** — the near-white `#FAFAFA` used for the numeral
  next to the gold square. Too close and the square stops looking like a
  separate shape.
- **CIEDE2000 ("dE")** — a single number for how different two colours look to
  a human eye, calibrated so that roughly "dE 1" is the smallest gap most
  people can spot and anything past dE 10 reads as a clearly different colour.
  Used here to check this gold doesn't collide with the live `#FBBF24` or with
  any other brand's colour on the same ground.

| Measured against | Colour | Result |
| --- | --- | --- |
| ground | `#0A0A0A` | 9.42:1 |
| ink (the numeral beside the square) | `#FAFAFA` | 2.01:1 |
| footer grey | `#A1A1A1` | 1.23:1 |
| live 11b2b signal | `#FBBF24` | dE 7.8 |

Nearest other live brand on this ground is `11cc` (a cool grey), at dE 31.9 —
nowhere close enough to matter. The footer ratio doesn't bind here: it only
matters for a signal with no hue of its own (silver, grey), and gold has
plenty of hue to separate it from de-emphasised footer text.

The full round, for comparison:

| Candidate | Signal | On ground | On ink | On footer | dE vs live 11b2b |
| --- | --- | --- | --- | --- | --- |
| royalgold — the reference "gold" | `#D4AF37` | 9.42:1 | 2.01:1 | 1.23:1 | 7.8 |
| antiquegold — dark goldenrod, deeper and more muted | `#B8860B` | 6.08:1 | 3.12:1 | 1.26:1 | 17.0 |
| champagne — pale, soft, elegant | `#DCB863` | 10.45:1 | 1.82:1 | 1.36:1 | 8.8 |
| honeyamber — deep, warm, closer to bronze | `#D97706` | 6.21:1 | 3.05:1 | 1.23:1 | 22.2 |

## Notes

This is the boldest and most literal reading of "gold" in the round — closest
in weight and brightness to the live colour (dE 7.8, the smallest gap of the
four), so it reads as an upgrade to the same idea rather than a new direction.
If the goal is "still recognisably 11b2b, just richer," this is the safest
pick; `antiquegold` and `honeyamber` are further departures.

Domain, layout, and everything except the signal colour are carried over
unchanged from the live `11b2b` brand. Nothing here is generated yet — this
is the decision record only.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
