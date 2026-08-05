# Brands

One folder per brand. Each holds the brand's definition and every set of assets
ever generated for it.

```
<brand-key>/
├── brand.md          what the brand is, and why: domain, mode, signal, notes
├── config.json       every generation variable, resolved; wins over brand.md
├── favicons/
│   └── gen-<timestamp>/    icon-512, icon-192, apple-touch-icon,
│                           favicon-32x32, favicon-16x16, favicon.ico,
│                           MANIFEST.md
├── web-og/
│   └── gen-<timestamp>/    <brand>-web-og.png, MANIFEST.md
└── content-og/
    └── gen-<timestamp>/    one card per title, MANIFEST.md
```

## Why every run gets its own folder

By default, each run gets a new timestamped folder. A generation is a dated fact:
this is what these scripts produced from this brand file on this day. Two runs
can be compared against each other, and against what another repository already
ships, without either being destroyed first — which is the whole point of
[BASELINE.md](BASELINE.md). If you deliberately reuse `--stamp`, the scripts
target that existing folder and can replace files there.

It does mean the folders accumulate. That is fine; they are small, and deleting
an old one is a decision someone can make later with the evidence in front of
them. Deleting the only copy of an asset that turned out to be live is not.

Each folder carries a `MANIFEST.md` recording the exact colours used, so a
directory explains itself without anyone having to re-derive it.

## The brands

| Key | Domain | Mode | Signal | Contrast |
| --- | --- | --- | --- | --- |
| `blog-rj11io` | blog.rj11.io | dark | `#2BC88F` green | 9.20:1 |
| `blog-rj11io-11ai` | blog.rj11.io | light | `#007A55` green | 5.14:1 |
| `www-rj11io` | www.rj11.io | dark, warm | `#F97316` orange | 7.08:1 |
| `ai-rj11io` | ai.rj11.io | light | `#007A55` green | 5.14:1 |
| `cv-rj11io` | cv.rj11.io | light | `#2563EB` blue | 4.95:1 |
| `intel-rj11io` | intel.rj11.io | dark | `#EF4444` red | 5.26:1 |
| `b2b-rj11io` | b2b.rj11.io | dark | `#FBBF24` gold | 11.86:1 |
| `cc-rj11io` | cc.rj11.io | dark | `#B4BDC4` titanium | 10.39:1 |

Contrast is the signal against its own ground. A non-text graphic needs 3:1 and
every brand clears it. The family keeps one mark and one layout; the signal
colour carries the main distinction, with `www-rj11io` also using warm ground
and ink values. The signal has to survive a 16 pixel favicon, so it is checked
with a number rather than an opinion.

`cc-rj11io` is the one signal that is a neutral rather than a colour, and a
neutral has to be measured against three things rather than one. Every chromatic
signal separates from the numeral by hue, so its lightness against the ink can be
low and no one notices; a titanium has only lightness, so the ink and the footer
grey both matter as well as the ground. Its brand file records all three numbers,
and records that its low ink figure is a deliberate choice: that mark reads as
monochrome with a highlight rather than ink plus colour.

## A brand file

Three fields are required and the rest are defaults:

```markdown
**Domain:** example.rj11.io
**Mode:** dark
**Signal:** `#EF4444`
```

`Mode` fixes the ground, the ink and the footer grey. Override any of them with
`**Ground:**`, `**Ink:**` or `**Footer:**`; only `www-rj11io` needs to. The
reader accepts any `**Key:** value` line anywhere in the document, so the file
stays something a person writes rather than a config file in disguise —
everything outside those lines is notes, and the notes are the point. Each of
these files records why its colour is what it is.

### Colour

| Field | Default | What it sets |
| --- | --- | --- |
| `**Signal:**` | required | the accent colour |
| `**Ground:**` | from mode | background |
| `**Ink:**` | from mode | the numeral, and the main row text |
| `**Footer:**` | from mode | the footer and masthead text colour |

### Text

Every string drawn on any asset is one of these four, and each can be changed or
switched off per brand:

| Field | Default | Where it appears |
| --- | --- | --- |
| `**Masthead:**` | the domain | the small tracked line above the mark, content cards only |
| `**Website row:**` | the domain | the framed main row on the website card |
| `**Footer text:**` | `AI / SOFTWARE / …` | the keyword line at the bottom of every card |
| `**Default title:**` | `Lorem Ipsum` | the main row of a content card, when no title is given |

Set any of them to `none` to draw nothing there. A brand with
`**Footer text:** none` gets cards with no footer line at all, and
`**Default title:** none` gets a content card with no title row when no title is
passed. The word is needed because the reader has to see a value to notice the
line, so a blank field would be invisible to it.

The only text that does not come from a brand file is a title passed on the
command line, and that falls back to `**Default title:**` when it is left out.

Backticks are stripped from every field, `**Domain:**` included, so a brand file
can quote any value without the quoting reaching a card.

See `../asset-generation-scripts/README.md` for the full field table, and
`../drafts/README.md` for where new assets land before they arrive here.
