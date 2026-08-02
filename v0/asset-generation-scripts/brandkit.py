"""Shared parts of the three generators: brands, colours, geometry, drawing.

Everything that more than one script needs lives here, so the scripts themselves
are short enough to read in one go. Nothing in here writes a file except
open_output_dir.

The one idea worth understanding
--------------------------------

The mark is never stored as a picture. It is stored as two coverage maps: how
much of each pixel the numeral covers, and how much the signal square covers.
Colour is applied last, at the size being drawn.

That ordering is the whole point. Resizing a finished picture of the mark rings:
Lanczos overshoots at every hard edge, so a downscale invents pixels darker than
the ground, brighter than the numeral, and more saturated than the signal. It is
why an earlier 16 pixel icon in the 11blog repository carried a #2FE0A1 square
the brand never had. Resizing coverage cannot do that, because every output
pixel ends up a blend of exactly three known colours.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCRIPTS_DIR = Path(__file__).resolve().parent
V0_DIR = SCRIPTS_DIR.parent
BRANDS_DIR = V0_DIR / "brands"
MARK_PATH = SCRIPTS_DIR / "assets/mark-xl-dot-centered.png"

# macOS ships this. On any other machine, point it at a monospaced .ttf with the
# same metrics or the cards will not match what is already published.
MONO_FONT = "/System/Library/Fonts/SFNSMono.ttf"

# ---------------------------------------------------------------- card geometry
CARD = (1200, 630)
MARK_ORIGIN = (425, 42)
MARK_SIZE = 350
MARK_CROP = (247, 247, 1007, 1007)

SQUARE = 18
GAP = 20
MAX_ROW = 1040
ROW_TOP = 477
ROW_MIDDLE = 486
TITLE_MAX_PT = 42
TITLE_MIN_PT = 28

MASTHEAD_MIDDLE = 56
MASTHEAD_PT = 15
MASTHEAD_TRACKING = 4

FOOTER_MIDDLE = 574
FOOTER_PT = 15
DEFAULT_FOOTER_TEXT = "AI / SOFTWARE / PRODUCT / ENGINEERING / TECHNOLOGY"

# ---------------------------------------------------------------- icon geometry
ICON_MASTER = 512
ICON_BOX = (462, 368)
ICON_PNG_SIZES = [512, 192, 180, 32, 16]
ICON_PNG_NAMES = {
    512: "icon-512.png",
    192: "icon-192.png",
    180: "apple-touch-icon.png",
    32: "favicon-32x32.png",
    16: "favicon-16x16.png",
}
ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# ------------------------------------------------------------------ mode tables
# A mode fixes the three colours a signal has to work against. Overriding any of
# them is allowed and is what www.rj11.io does, because its ground and ink are
# warm rather than neutral.
MODES = {
    "dark": {
        "ground": (10, 10, 10),
        "ink": (250, 250, 250),
        "footer": (161, 161, 161),
    },
    "light": {
        "ground": (250, 250, 250),
        "ink": (10, 10, 10),
        "footer": (103, 103, 103),
    },
}


# ------------------------------------------------------------------------ brand
@dataclass
class Brand:
    key: str
    domain: str
    mode: str
    signal: tuple[int, int, int]
    ground: tuple[int, int, int]
    ink: tuple[int, int, int]
    footer: tuple[int, int, int]
    footer_text: str = DEFAULT_FOOTER_TEXT
    source: Path | None = field(default=None, repr=False)

    @property
    def directory(self) -> Path:
        return BRANDS_DIR / self.key


def parse_hex(value: str) -> tuple[int, int, int]:
    text = value.strip().strip("`").lstrip("#")
    if len(text) != 6:
        raise ValueError(f"expected a six digit hex colour, got {value!r}")
    return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))


def hex_of(colour) -> str:
    return "#%02X%02X%02X" % colour


def load_brand(key: str) -> Brand:
    """Read one brand's markdown file.

    The format is deliberately loose: any line shaped `**Key:** value` counts,
    anywhere in the document, so the file stays something a person writes rather
    than a config file wearing a disguise.
    """
    path = BRANDS_DIR / key / "brand.md"
    if not path.exists():
        raise SystemExit(f"no brand at {path}")

    fields = {
        match.group(1).strip().lower(): match.group(2).strip()
        for match in re.finditer(r"^\*\*(.+?):\*\*\s*(.+?)\s*$", path.read_text(), re.M)
    }

    for required in ("domain", "mode", "signal"):
        if required not in fields:
            raise SystemExit(f"{path} is missing **{required.title()}:**")

    mode = fields["mode"].lower()
    if mode not in MODES:
        raise SystemExit(f"{path}: mode must be one of {', '.join(MODES)}")

    palette = dict(MODES[mode])
    for name in ("ground", "ink", "footer"):
        if name in fields:
            palette[name] = parse_hex(fields[name])

    return Brand(
        key=key,
        domain=fields["domain"],
        mode=mode,
        signal=parse_hex(fields["signal"]),
        ground=palette["ground"],
        ink=palette["ink"],
        footer=palette["footer"],
        footer_text=fields.get("footer text", DEFAULT_FOOTER_TEXT),
        source=path,
    )


def every_brand() -> list[str]:
    return sorted(
        path.parent.name for path in BRANDS_DIR.glob("*/brand.md")
    )


# ------------------------------------------------------------------------ masks
def build_masks(mark_path: Path = MARK_PATH):
    """Split the mark master into numeral coverage and signal coverage.

    Sorted by hue, because green leading is the only thing that tells the signal
    square apart from the numeral, at any opacity including its anti-aliased
    edge. The two never overlap: the square does not touch the numeral in the
    master, which was checked rather than assumed.
    """
    source = Image.open(mark_path).convert("RGB")
    pixels = source.load()
    ink = Image.new("L", source.size, 0)
    signal = Image.new("L", source.size, 0)
    ink_out, signal_out = ink.load(), signal.load()

    for y in range(source.height):
        for x in range(source.width):
            red, green, blue = pixels[x, y]
            brightest = max(red, green, blue)
            if brightest <= 12:
                continue
            if green > red + 18 and green > blue + 8:
                signal_out[x, y] = min(255, round(green * 255 / 200))
            else:
                ink_out[x, y] = min(255, round(brightest * 255 / 250))

    return ink, signal


def union_box(masks):
    boxes = [mask.getbbox() for mask in masks]
    return (
        min(b[0] for b in boxes),
        min(b[1] for b in boxes),
        max(b[2] for b in boxes),
        max(b[3] for b in boxes),
    )


def compose(masks, box, size, ground, ink_colour, signal_colour):
    """Paint the mark at one size, on a solid ground, guaranteed in gamut."""
    ink_mask, signal_mask = (
        mask.crop(box).resize(size, Image.Resampling.LANCZOS) for mask in masks
    )
    ink_px, signal_px = ink_mask.load(), signal_mask.load()

    tile = Image.new("RGB", size, ground)
    out = tile.load()

    for y in range(size[1]):
        for x in range(size[0]):
            i = ink_px[x, y] / 255
            s = signal_px[x, y] / 255
            if i == 0 and s == 0:
                continue

            # Clamp back onto the simplex. Ringing in a mask can push the pair
            # a little past full coverage; without this the surplus would be
            # paid for by the ground going negative.
            total = i + s
            if total > 1:
                i, s = i / total, s / total

            out[x, y] = tuple(
                round(
                    ground[c] * (1 - i - s)
                    + ink_colour[c] * i
                    + signal_colour[c] * s
                )
                for c in range(3)
            )

    return tile


# ------------------------------------------------------------------------- type
def font(points: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(MONO_FONT, points)
    except OSError as error:  # pragma: no cover - environment dependent
        raise SystemExit(
            f"could not open {MONO_FONT}. Set MONO_FONT in brandkit.py to a "
            "monospaced .ttf with the same metrics."
        ) from error


def text_width(draw: ImageDraw.ImageDraw, value: str, points: int) -> int:
    box = draw.textbbox((0, 0), value, font=font(points))
    return box[2] - box[0]


def draw_tracked(draw, value, centre_x, middle_y, points, fill, tracking):
    """Mono with extra letter spacing, drawn centred, one glyph at a time.

    Pillow has no tracking. The domain needs it: unspaced, a short string at
    this size looks dropped into the space rather than placed in it.
    """
    glyphs = [(char, text_width(draw, char, points)) for char in value]
    total = sum(w for _, w in glyphs) + tracking * (len(glyphs) - 1)
    x = centre_x - total / 2
    for char, width in glyphs:
        draw.text((x, middle_y), char, font=font(points), fill=fill, anchor="lm")
        x += width + tracking


def fit_row(draw, text: str) -> tuple[int, int, int]:
    """Largest point size whose framed row fits, with that row's measurements."""
    fixed = SQUARE + GAP + GAP + SQUARE
    for points in range(TITLE_MAX_PT, TITLE_MIN_PT - 1, -1):
        width = text_width(draw, text, points)
        if fixed + width <= MAX_ROW:
            return points, width, fixed + width
    width = text_width(draw, text, TITLE_MIN_PT)
    return TITLE_MIN_PT, width, fixed + width


def draw_framed_row(draw, text: str, brand: Brand) -> None:
    """The signature row: a signal square, the text, a signal square.

    Two squares rather than one. A single square reads as a bullet pointing at
    the text; a pair frames it, and it centres against the mark above and the
    footer below, both of which were already centred.
    """
    points, width, row_width = fit_row(draw, text)
    start = round(CARD[0] / 2 - row_width / 2)

    draw.rectangle(
        (start, ROW_TOP, start + SQUARE - 1, ROW_TOP + SQUARE - 1), fill=brand.signal
    )
    left = start + SQUARE + GAP
    draw.text((left, ROW_MIDDLE), text, font=font(points), fill=brand.ink, anchor="lm")
    right = left + width + GAP
    draw.rectangle(
        (right, ROW_TOP, right + SQUARE - 1, ROW_TOP + SQUARE - 1), fill=brand.signal
    )


def draw_footer(draw, brand: Brand) -> None:
    draw.text(
        (CARD[0] / 2, FOOTER_MIDDLE),
        brand.footer_text,
        font=font(FOOTER_PT),
        fill=brand.footer,
        anchor="mm",
    )


def new_card(brand: Brand, masks) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """A blank card with the mark already on it."""
    image = Image.new("RGB", CARD, brand.ground)
    # Composed on the card's own ground and pasted opaquely, which is exact
    # because they are the same colour.
    image.paste(
        compose(masks, MARK_CROP, (MARK_SIZE, MARK_SIZE), brand.ground, brand.ink, brand.signal),
        MARK_ORIGIN,
    )
    return image, ImageDraw.Draw(image)


# ------------------------------------------------------------------------ icons
def icon_at(masks, box, artwork_size, size, brand: Brand) -> Image.Image:
    """One square icon, artwork scaled to the shared margin and centred."""
    scale = min(
        ICON_BOX[0] / artwork_size[0], ICON_BOX[1] / artwork_size[1]
    ) * (size / ICON_MASTER)
    target = (
        max(1, round(artwork_size[0] * scale)),
        max(1, round(artwork_size[1] * scale)),
    )

    icon = Image.new("RGB", (size, size), brand.ground)
    icon.paste(
        compose(masks, box, target, brand.ground, brand.ink, brand.signal),
        ((size - target[0]) // 2, (size - target[1]) // 2),
    )
    return icon


def write_icon_set(masks, brand: Brand, directory: Path) -> list[Path]:
    """Five PNGs and a six-frame .ico, every one composed at its own size.

    Two rules are load bearing here, both learned by breaking something:

    Write RGBA, never a palette image. A 256 colour palette is a valid PNG,
    visually identical for this artwork, and a third smaller. It also breaks a
    Next.js build, which decodes app/favicon.ico itself and rejects any frame
    that is not RGBA.

    Compose every frame, including inside the .ico. Pillow uses a frame you
    supply only when it matches a requested size exactly, and quietly resamples
    the largest one for any size you leave out, which puts the ringing straight
    back.
    """
    box = union_box(masks)
    artwork_size = (box[2] - box[0], box[3] - box[1])
    directory.mkdir(parents=True, exist_ok=True)

    written = []
    for size in ICON_PNG_SIZES:
        path = directory / ICON_PNG_NAMES[size]
        icon_at(masks, box, artwork_size, size, brand).convert("RGBA").save(
            path, optimize=True
        )
        written.append(path)

    frames = [
        icon_at(masks, box, artwork_size, width, brand).convert("RGBA")
        for width, _ in sorted(ICO_SIZES, reverse=True)
    ]
    ico = directory / "favicon.ico"
    frames[0].save(ico, format="ICO", sizes=ICO_SIZES, append_images=frames[1:])
    written.append(ico)
    return written


# ----------------------------------------------------------------------- output
def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled"


def open_output_dir(brand: Brand, kind: str, stamp: str | None = None) -> Path:
    """brands/<brand>/<kind>/gen-<timestamp>/, created.

    Every run writes a new directory. Nothing is ever overwritten, so two runs
    can be diffed against each other, and against what a repository already
    ships, without either being lost first.
    """
    stamp = stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    directory = brand.directory / kind / f"gen-{stamp}"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def write_manifest(directory: Path, brand: Brand, kind: str, entries: list[str]) -> Path:
    """What was made, from what, so a directory explains itself later."""
    path = directory / "MANIFEST.md"
    path.write_text(
        f"# {brand.domain} — {kind}\n\n"
        f"Generated {datetime.now().isoformat(timespec='seconds')} "
        f"by `asset-generation-scripts/`.\n\n"
        f"| Setting | Value |\n| --- | --- |\n"
        f"| Brand | `{brand.key}` |\n"
        f"| Domain | {brand.domain} |\n"
        f"| Mode | {brand.mode} |\n"
        f"| Signal | `{hex_of(brand.signal)}` |\n"
        f"| Ground | `{hex_of(brand.ground)}` |\n"
        f"| Ink | `{hex_of(brand.ink)}` |\n"
        f"| Footer | `{hex_of(brand.footer)}` |\n\n"
        "## Files\n\n" + "\n".join(f"- `{name}`" for name in entries) + "\n"
    )
    return path
