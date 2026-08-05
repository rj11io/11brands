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

Two other things to know
------------------------

Output goes to drafts/ by default, not brands/. Promoting a draft into the
registered set is a separate step, described in skills/11brands-promote-draft/.

Every string drawn on any asset is a brand field, and every one of them can be
overridden or omitted in brand.md. Nothing is hardcoded where it is drawn.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCRIPTS_DIR = Path(__file__).resolve().parent
V0_DIR = SCRIPTS_DIR.parent
BRANDS_DIR = V0_DIR / "brands"
DRAFTS_DIR = V0_DIR / "drafts"
MARK_PATH = SCRIPTS_DIR / "assets/mark-xl-dot-centered.png"

# Two output roots. Work lands in drafts by default and is promoted into brands
# as a separate, deliberate step, so nothing reaches the registered set without
# someone choosing to put it there.
OUTPUT_ROOTS = {"drafts": DRAFTS_DIR, "brands": BRANDS_DIR}
DEFAULT_OUTPUT = "drafts"

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

# ------------------------------------------------------------------ text tables
# Every string drawn on any asset comes from one of these, and every one of them
# is overridable per brand. Nothing is hardcoded at the point of drawing.
DEFAULT_FOOTER_TEXT = "AI / SOFTWARE / PRODUCT / ENGINEERING / TECHNOLOGY"
DEFAULT_CONTENT_TITLE = "Lorem Ipsum"

# A text field set to this, in any capitalisation, draws nothing at all.
OMIT = "none"

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
    # Every drawn string. Each defaults to something sensible, so a brand file
    # that sets none of them behaves exactly as it did before these existed.
    masthead: str = ""       # content cards, above the mark; defaults to domain
    website_row: str = ""    # website card main row; defaults to domain
    footer_text: str = DEFAULT_FOOTER_TEXT
    default_title: str = DEFAULT_CONTENT_TITLE
    source: Path | None = field(default=None, repr=False)

    def directory_in(self, root: str = DEFAULT_OUTPUT) -> Path:
        return OUTPUT_ROOTS[root] / self.key


def strip_value(value: str) -> str:
    """Unwrap a field value: surrounding space, then backticks, then space again.

    Every field goes through this, so a brand file can quote any value the way it
    quotes a colour without the quoting leaking into a card or a manifest.
    """
    return value.strip().strip("`").strip()


def parse_hex(value: str) -> tuple[int, int, int]:
    text = strip_value(value).lstrip("#")
    if len(text) != 6:
        raise ValueError(f"expected a six digit hex colour, got {value!r}")
    return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))


def parse_text(value: str) -> str:
    """An optional text field, where the literal `none` means draw nothing.

    That word is the only way to say "this brand has no footer": the field reader
    needs a value to see the line at all, so an empty one would be invisible to
    it.
    """
    text = strip_value(value)
    return "" if text.lower() == OMIT else text


def hex_of(colour) -> str:
    return "#%02X%02X%02X" % colour


def brand_file(key: str, prefer: str = DEFAULT_OUTPUT) -> Path:
    """Find a brand's markdown file, looking in the preferred root first.

    A key can exist in both roots at once: a promoted brand in brands/ that is
    being reworked in drafts/. Whichever root is being written to is the one whose
    definition wins, so drafting reads the draft and promoting reads the promoted
    copy. The chosen path is reported and recorded in every manifest, because
    "which file did this come from" is the first question a surprising asset
    raises.
    """
    order = [prefer] + [name for name in OUTPUT_ROOTS if name != prefer]
    for name in order:
        path = OUTPUT_ROOTS[name] / key / "brand.md"
        if path.exists():
            return path
    looked = ", ".join(
        str((OUTPUT_ROOTS[name] / key / "brand.md").relative_to(V0_DIR))
        for name in order
    )
    raise SystemExit(f"no brand named {key!r}. Looked for: {looked}")


def load_brand(key: str, prefer: str = DEFAULT_OUTPUT) -> Brand:
    """Read one brand's markdown file.

    The format is deliberately loose: any line shaped `**Key:** value` counts,
    anywhere in the document, so the file stays something a person writes rather
    than a config file wearing a disguise.
    """
    path = brand_file(key, prefer)

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

    domain = strip_value(fields["domain"])
    # The two rows that describe the site default to the domain, because that is
    # what they are for. Overriding either is what makes them variables. All four
    # text fields honour `none` the same way, including the title: a brand that
    # says it has no default title gets a card with no title row, not a silent
    # fallback to the built-in one.
    return Brand(
        key=key,
        domain=domain,
        mode=mode,
        signal=parse_hex(fields["signal"]),
        ground=palette["ground"],
        ink=palette["ink"],
        footer=palette["footer"],
        masthead=parse_text(fields.get("masthead", domain)),
        website_row=parse_text(fields.get("website row", domain)),
        footer_text=parse_text(fields.get("footer text", DEFAULT_FOOTER_TEXT)),
        default_title=parse_text(fields.get("default title", DEFAULT_CONTENT_TITLE)),
        source=path,
    )


def every_brand() -> list[str]:
    """The registered family: every key with a brand.md in brands/.

    Deliberately not "every key in either root". drafts/ holds work in progress
    and rejected attempts, and neither belongs in a sweep — regenerating a
    rejected draft because it still has a brand.md is a good way to resurrect a
    colour someone already decided against. A draft is named explicitly.
    """
    return sorted(path.parent.name for path in BRANDS_DIR.glob("*/brand.md"))


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

    An empty string draws nothing, squares included — a row framing no text is
    two floating dots, not a design.
    """
    if not text:
        return

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


def draw_masthead(draw, brand: Brand) -> None:
    """The tracked domain line above the mark, on content cards only."""
    if not brand.masthead:
        return
    draw_tracked(
        draw,
        brand.masthead,
        CARD[0] / 2,
        MASTHEAD_MIDDLE,
        MASTHEAD_PT,
        brand.footer,
        MASTHEAD_TRACKING,
    )


def draw_footer(draw, brand: Brand) -> None:
    if not brand.footer_text:
        return
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


def open_output_dir(
    brand: Brand,
    kind: str,
    stamp: str | None = None,
    into: str = DEFAULT_OUTPUT,
) -> Path:
    """<root>/<brand>/<kind>/gen-<timestamp>/, created.

    The root is drafts/ unless told otherwise. Every run writes a new directory.
    Nothing is ever overwritten, so two runs can be diffed against each other,
    and against what a repository already ships, without either being lost first.
    """
    if into == "brands" and brand.source and DRAFTS_DIR in brand.source.parents:
        # Allowed, because --into brands is explicit, but it leaves the registered
        # set holding runs whose definition lives somewhere else, which is the one
        # state this layout exists to prevent. Say so rather than doing it quietly.
        print(
            f"warning: writing into brands/ from a definition still in drafts/\n"
            f"         definition: {brand.source.relative_to(V0_DIR)}\n"
            f"         brands/{brand.key}/ will hold runs with no brand.md beside "
            f"them.\n"
            f"         To register the brand properly, use "
            f"skills/11brands-promote-draft/.",
            file=sys.stderr,
        )

    stamp = stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    directory = brand.directory_in(into) / kind / f"gen-{stamp}"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _text_row(label: str, value: str) -> str:
    """A manifest row for a text field, showing an omitted one as such."""
    return f"| {label} | {'*(omitted)*' if not value else value} |\n"


def write_manifest(directory: Path, brand: Brand, kind: str, entries: list[str]) -> Path:
    """What was made, from what, so a directory explains itself later.

    Records the text as well as the colours. A card's strings are as much a part
    of what was generated as its palette, and once they are variables they can no
    longer be re-derived from the domain alone.
    """
    path = directory / "MANIFEST.md"
    source = (
        str(brand.source.relative_to(V0_DIR)) if brand.source else "unknown"
    )
    path.write_text(
        f"# {brand.domain} — {kind}\n\n"
        f"Generated {datetime.now().isoformat(timespec='seconds')} "
        f"by `asset-generation-scripts/`.\n\n"
        f"| Setting | Value |\n| --- | --- |\n"
        f"| Brand | `{brand.key}` |\n"
        f"| Domain | {brand.domain} |\n"
        f"| Definition | `{source}` |\n"
        f"| Mode | {brand.mode} |\n"
        f"| Signal | `{hex_of(brand.signal)}` |\n"
        f"| Ground | `{hex_of(brand.ground)}` |\n"
        f"| Ink | `{hex_of(brand.ink)}` |\n"
        f"| Footer | `{hex_of(brand.footer)}` |\n\n"
        "## Text\n\n"
        f"| Field | Value |\n| --- | --- |\n"
        + _text_row("Masthead", brand.masthead)
        + _text_row("Website row", brand.website_row)
        + _text_row("Footer text", brand.footer_text)
        + _text_row("Default title", brand.default_title)
        + "\n## Files\n\n" + "\n".join(f"- `{name}`" for name in entries) + "\n"
    )
    return path
