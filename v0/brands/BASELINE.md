# Baseline: how this output compares to 11blog

The brand assets in this repository were previously generated inside `11blog`,
by a set of scripts that grew one change at a time. These scripts are the
consolidated version. This file records how closely they reproduce what `11blog`
ships, so that a future run can be checked against a known answer rather than a
guess.

Measured on 2026-08-02, against `11blog` at that date. Every number below came
from a pixel comparison, not an eye.

## Favicons: everything matches

All five packages, all six files each — **30 of 30 byte-identical**.

| This repository | 11blog | Result |
| --- | --- | --- |
| `blog-rj11io/favicons/` | `favicons/blog-rj11io-v1/` | identical |
| `www-rj11io/favicons/` | `favicons/www-rj11io-v2/` | identical |
| `ai-rj11io/favicons/` | `favicons/ai-rj11io-v2/` | identical |
| `intel-rj11io/favicons/` | `favicons/intel-rj11io-v1/` | identical |
| `cv-rj11io/favicons/` | `favicons/cv-rj11io-v1/` | identical |

Note that `11blog` also holds older packages — `www-rj11io-v1`, `ai-rj11io-v1`,
and the `11blog-favicon-*` files. Those are superseded and will **not** match:
they were drawn before the two rules in the scripts README and carry colours
outside their own brand's palette. Compare against the versions in the table.

## Website cards: two of five match

| This repository | 11blog | Result |
| --- | --- | --- |
| `intel-rj11io/web-og/` | `og/intel-rj11io-favicon-style-red-og-v1.png` | identical |
| `cv-rj11io/web-og/` | `og/cv-rj11io-favicon-style-inverted-blue-og-v1.png` | identical |
| `blog-rj11io/web-og/` | `og/11blog-favicon-style-og-v5.png` | 26,506 px differ |
| `www-rj11io/web-og/` | `og/rj11io-favicon-style-orange-og-v3.png` | 14,920 px differ |
| `ai-rj11io/web-og/` | `og/ai-rj11io-favicon-style-inverted-green-og-v4.png` | 14,682 px differ |

The two that match were generated from parameters in the first place. The three
that differ were not: they were produced by editing existing images, and the
differences are the fingerprints of that.

Broken down by region:

| Card | Mark | Main row | Footer |
| --- | --- | --- | --- |
| blog | 23,932 px | 2,574 px | 0 |
| www | 10,574 px | 2,915 px | 1,431 px |
| ai | 10,574 px | 2,735 px | 1,373 px |

**The mark** differs because the `11blog` files carry a mark that was resized as
a picture, so it rings. Ours is composed from coverage masks. Ours is the
correct one: in the mark region of a blog card, `11blog` holds 106 colours
outside the brand's three-colour triangle and this repository holds none.

**The main row** sits one to three pixels across. In `11blog` the row was nudged
into place by a script that moved existing pixels to add the second signal
square, and the arithmetic rounded. Here it is computed.

**The footer** matches exactly on the blog card, which confirms the dark default
is right. It differs on `www` and `ai` because those two cards inherited a
slightly different grey from the tool that first drew them. Neither is recorded
anywhere as intentional.

## Content cards: the mark, and nothing else

Compared against the `blog-platform` cover set in `11blog`:

| Region | Difference |
| --- | --- |
| Masthead | 0 px |
| Mark | 23,932 px |
| Title row | 0 px |
| Footer | 0 px |

Three cards were checked and all three gave the same result. Masthead, title row
and footer are pixel-identical; only the mark differs, for the reason above, and
again this repository's version is the in-gamut one.

## What to do with a mismatch

Re-running these scripts should reproduce this table exactly. If it does not,
something changed, and the order to check it in is:

1. **The font.** Different metrics move every glyph. `brandkit.py` expects
   `/System/Library/Fonts/SFNSMono.ttf`.
2. **The mark master.** `asset-generation-scripts/assets/mark-xl-dot-centered.png`
   is a copy of the one in `11blog`; if either moves, the mark moves.
3. **Pillow.** Resampling and PNG encoding are its job. This baseline was taken
   with Pillow 12.3.0.
4. **A brand file.** A changed colour changes every asset for that brand.

If the goal is to bring `11blog` into line rather than to match it, the three
website cards and the whole content set can be replaced with the output here.
That is a real improvement — it removes the out-of-gamut mark from every card —
but it is a change to published images, so it is a decision rather than a
cleanup.
