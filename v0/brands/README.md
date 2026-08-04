# Brands

One folder per brand. Each holds the brand's definition and every set of assets
ever generated for it.

```
<brand-key>/
├── brand.md          what the brand is: domain, mode, signal colour
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

Contrast is the signal against its own ground. A non-text graphic needs 3:1 and
every brand clears it. The family keeps one mark and one layout; the signal
colour carries the main distinction, with `www-rj11io` also using warm ground
and ink values. The signal has to survive a 16 pixel favicon, so it is checked
with a number rather than an opinion.

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

See `../asset-generation-scripts/README.md` for how to add one.
