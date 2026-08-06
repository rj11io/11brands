# archive.rj11.io

The archive site. This file is candidate `purple` in the first 11archive
colour round: ten light-mode variants, none of them chosen yet.

## Palette decision

Mode light. Signal `#7E22CE` on ground `#FAFAFA`: **6.69:1**.

Purple 700. Purple sits between the family's violet gap and its pink block, redder than violet 700 and bluer than any pink in use.

Every candidate in the round clears the 3:1 floor for a non-text graphic and
also clears the 4.5:1 aim, so contrast alone does not decide this round —
separability from the rest of the family at 16 pixels does. The three numbers
for this candidate:

| Measured against | Colour | Ratio |
| --- | --- | --- |
| ground | `#FAFAFA` | 6.69:1 |
| ink (the numeral beside the square) | `#0A0A0A` | 2.84:1 |
| footer grey | `#676767` | 1.23:1 |

The full round, for comparison:

| Candidate | Signal | On ground | On ink | On footer |
| --- | --- | --- | --- | --- |
| violet — violet 700 | `#6D28D9` | 6.81:1 | 2.79:1 | 1.26:1 |
| purple — purple 700 | `#7E22CE` | 6.69:1 | 2.84:1 | 1.23:1 |
| plum — purple 800 | `#6B21A8` | 8.35:1 | 2.27:1 | 1.54:1 |
| indigo — indigo 600 | `#4F46E5` | 6.02:1 | 3.15:1 | 1.11:1 |
| indigo700 — indigo 700 | `#4338CA` | 7.57:1 | 2.51:1 | 1.40:1 |
| teal — teal 700 | `#0F766E` | 5.24:1 | 3.62:1 | 1.03:1 |
| olive — lime 700 | `#4D7C0F` | 4.78:1 | 3.96:1 | 1.13:1 |
| slate — slate 600 | `#475569` | 7.26:1 | 2.61:1 | 1.34:1 |
| sepia — amber 900 | `#78350F` | 8.69:1 | 2.18:1 | 1.60:1 |
| bronze — yellow 700 | `#A16207` | 4.72:1 | 4.02:1 | 1.15:1 |

## Notes

The closest active brand is 11support's pink 500 (`#EC4899`) and the closest archived one is `11brands-light-fuchsia` (`#A21CAF`). Both are far more magenta, but purple 700 is the candidate most worth a 16px side-by-side against 11support.

Domain `archive.rj11.io` follows the family pattern and is an assumption; change
`config.json` if the site lands elsewhere. The base key `11archive` is
deliberately not registered yet — it gets created from whichever candidate wins,
and the other nine go to `archive/` with their keys reserved.

---

This file is the decision record and is never parsed by the scripts. All live
values are in `config.json` next to it — change that file to change the assets.
