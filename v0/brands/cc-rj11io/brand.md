# cc.rj11.io

Bright titanium on the standard dark ground. The only brand in the family whose
signal is a neutral rather than a colour, which changes how it has to be checked.

**Domain:** cc.rj11.io
**Mode:** dark
**Signal:** `#B4BDC4`

## Notes

A bright, cool-neutral metal: light enough to read as titanium rather than
pewter, with just enough tint to look like brushed metal rather than flat grey.

### Why a neutral signal needs three checks

Every other signal in the family separates from the numeral by **hue**. Blog
green measures only 2.06:1 against the dark-mode ink and `b2b-rj11io` gold only
1.60:1, but they carry chroma of 157 and 215, so the eye reads them as obviously
different things. A neutral has almost no chroma, so it has nothing but lightness
to work with, and it has to be measured against three things rather than one:

| Gap | Why it matters | This brand |
| --- | --- | --- |
| vs ground `#0A0A0A` | the 3:1 minimum for a non-text graphic | **10.39:1** |
| vs ink `#FAFAFA` | the square sits beside the numeral in the mark | 1.83:1 |
| vs footer `#A1A1A1` | the accent must not match de-emphasised text | 1.36:1 |

### Why this exact value

Brightness and separation from the numeral pull against each other: the lighter
the silver, the closer it gets to the ink. `#B4BDC4` is the best available trade,
and it beats both of the obvious alternatives on the gap that actually matters:

| Candidate | vs ground | vs ink | vs footer | Chroma |
| --- | --- | --- | --- | --- |
| `#B4BDC4` — chosen | 10.39:1 | **1.83:1** | 1.36:1 | 16 |
| `#C0C0C0` classic silver | 10.88:1 | 1.74:1 | 1.42:1 | 0 — flat, no metal |
| `#B0C4DE` light steel blue | 11.12:1 | 1.71:1 | 1.45:1 | 46 — reads periwinkle |
| `#CDD3D8` one step lighter | 13.11:1 | 1.45:1 | 1.71:1 | 11 |
| `#A8B1B8` one step darker | 9.09:1 | 2.09:1 | 1.19:1 | 16 — nears the footer |

Going lighter costs separation from the numeral faster than it gains brightness.
Going darker walks into the footer grey, and two steps darker stops reading as
bright metal at all.

### The deliberate trade

At 1.83:1 the square is a soft tonal step off the numeral rather than a contrasting
accent, so the mark reads as **monochrome with a highlight** instead of
ink-plus-colour. That is the intended look here — restrained and premium — and it
is a brand decision, not an oversight. It is worth knowing that it is the one
place this brand behaves differently from the rest of the family, where the signal
is meant to jump.

Nothing about it is an accessibility problem. The square never touches the numeral
in the mark, so a band of ground separates the two shapes, and the 10.39:1 against
that ground is the ratio the 3:1 floor actually governs. Position and shape carry
the signal here; colour supports it.

An earlier draft used pewter `#64748B`, which measured 4.56:1 against the ink and
separated far more strongly, but read as dark grey rather than as silver. It was
rejected on those grounds. The light-mode gold attempt before it is kept in
`../../drafts/cc-rj11io/`.

### One note for whoever verifies this

The gamut check in `skills/11brands-verify-assets/` reports false positives on
this brand. It tests whether each colour is a blend of ground, ink and signal, and
with a near-neutral signal that triangle is a sliver — 8.4 degrees off the ink
axis, against 31.2 for `b2b-rj11io` gold — so one bit of rounding exceeds its
±0.01 tolerance. Use the forward test instead: ask whether a valid coverage pair
exists whose rounded blend equals the colour. Every colour in this brand's output
passes that test.

Contrast of the signal on its ground: **10.39:1**.
