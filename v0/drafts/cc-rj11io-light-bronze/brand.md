# cc.rj11.io

Gold on the standard light ground. The light-mode counterpart to `b2b-rj11io`.

**Domain:** cc.rj11.io
**Mode:** light
**Signal:** `#B45309`

## Notes

Amber 700, which is two steps darker than a dark-ground gold rather than the
usual one. Gold is intrinsically light, so it loses contrast against `#FAFAFA`
faster than any other hue in the family:

| Step | Hex | On `#FAFAFA` |
| --- | --- | --- |
| amber 500 | `#F59E0B` | 2.06:1 — fails |
| amber 600 | `#D97706` | 3.05:1 — clears by 0.05 |
| amber 700 | `#B45309` | 4.81:1 — chosen |

Amber 600 was rejected rather than failed. It passes the 3:1 floor for a
non-text graphic by five hundredths, which is the same margin that pushed
`cv-rj11io` from blue 500 to blue 600: any later change to the ground breaks it,
and the colour cannot be set in type.

The consequence is that this reads as a deep bronze, not a bright gold. That is
the honest cost of gold on a light ground, and it still separates cleanly at 16
pixels from the other light brands, which are green `#007A55` and blue
`#2563EB`.

Contrast of the signal on its ground: **4.81:1**.
