# Changing a brand's font

Every string on every asset — the main row, the masthead, the footer — is drawn
in one font, set per brand in `config.json`:

```json
"font": {
  "path": "/System/Library/Fonts/SFNSMono.ttf",
  "index": 0
}
```

Change it, re-run a generator, look at the result. Nothing else needs editing.

## What to expect when you swap

The layout numbers in the config (`row_middle`, `max_row`, the point sizes) were
tuned to SF Mono's metrics. Every font has different glyph widths and a different
ascent/descent, so a swap moves every glyph: rows sit slightly higher or lower,
long titles step down to smaller sizes at different lengths, and nothing will
reproduce a card that already exists. That is fine for a new brand or variant —
it is a design change, not a drop-in.

Measured on this machine, the same 12-character domain at 42pt:

| Face | Width | Ascent/descent |
| --- | --- | --- |
| SF Mono (the default) | 312px | 41/9 |
| Menlo | 300px | 39/10 |
| Monaco | 300px | 42/11 |
| Courier New | 300px | 35/13 |
| PT Mono | 301px | 38/10 |
| Andale Mono | 300px | 39/10 |
| SF Pro (proportional) | 183px | 41/9 |
| New York (serif) | 174px | 40/11 |

## `.ttf` vs `.ttc`, and the index

A `.ttf` holds one face; leave `index` at 0. A `.ttc` is a collection of faces
and `index` picks one. **The regular face is not always index 0**:

| File | Faces by index |
| --- | --- |
| `Menlo.ttc` | 0 Regular, 1 Bold, 2 Italic, 3 Bold Italic |
| `Courier.ttc` | 0 Regular, 1 Bold, 2 Oblique, 3 Bold Oblique |
| `PTMono.ttc` | **0 Bold**, 1 Regular |

Point at `PTMono.ttc` without setting `"index": 1` and every card comes out bold.
To list the faces in any collection:

```python
from PIL import ImageFont
path, i = "/System/Library/Fonts/Menlo.ttc", 0
while True:
    try:
        print(i, *ImageFont.truetype(path, 12, index=i).getname()); i += 1
    except OSError:
        break
```

## Apple fonts on this machine

Monospaced, the natural fits for this design:

| Face | Config `path` | `index` |
| --- | --- | --- |
| SF Mono | `/System/Library/Fonts/SFNSMono.ttf` | 0 |
| SF Mono Italic | `/System/Library/Fonts/SFNSMonoItalic.ttf` | 0 |
| Menlo | `/System/Library/Fonts/Menlo.ttc` | 0 (1 bold, 2 italic) |
| Monaco | `/System/Library/Fonts/Monaco.ttf` | 0 |
| Courier | `/System/Library/Fonts/Courier.ttc` | 0 |
| Courier New | `/System/Library/Fonts/Supplemental/Courier New.ttf` | 0 |
| Courier New Bold | `/System/Library/Fonts/Supplemental/Courier New Bold.ttf` | 0 |
| PT Mono | `/System/Library/Fonts/Supplemental/PTMono.ttc` | **1** (0 is bold) |
| Andale Mono | `/System/Library/Fonts/Supplemental/Andale Mono.ttf` | 0 |

Proportional and serif faces, for experiments. Nothing in the drawing code
requires monospace — widths are measured per glyph and the masthead tracking is
applied per glyph — so these work; the rows just come out much narrower and the
brand stops looking like the rest of the family:

| Face | Config `path` |
| --- | --- |
| SF Pro | `/System/Library/Fonts/SFNS.ttf` |
| SF Compact | `/System/Library/Fonts/SFCompact.ttf` |
| New York (serif) | `/System/Library/Fonts/NewYork.ttf` |
| Helvetica | `/System/Library/Fonts/Helvetica.ttc` |
| Helvetica Neue | `/System/Library/Fonts/HelveticaNeue.ttc` |
| Avenir | `/System/Library/Fonts/Avenir.ttc` |
| Geneva | `/System/Library/Fonts/Geneva.ttf` |

Third-party fonts work the same way: any `.ttf` or `.ttc` Pillow can open, by
absolute path. User-installed fonts usually live in `~/Library/Fonts/`.

## After changing a font

1. Regenerate one content card with the longest title the brand is likely to
   carry, and check it still fits — different widths hit the `row_min_pt` floor
   at different lengths, and past the floor the row runs wide.
2. Look at the masthead and footer: a font with a different ascent sits
   differently on the same `_middle` lines. Adjust `masthead_middle`,
   `row_middle` and `footer_middle` in the config if the optics are off.
3. Run the `11brands-v1-verify-assets` checks. The gamut test is
   font-independent and should stay clean; the comparisons will show exactly
   which regions moved.

Fonts under `/System/Library/Fonts/` ship with macOS and are not in this
repository. A brand whose config points at one only regenerates identically on a
Mac that has it — which is every Mac for the tables above, but worth knowing for
anything from `~/Library/Fonts/`.
