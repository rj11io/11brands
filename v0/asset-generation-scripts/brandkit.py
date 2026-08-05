"""Shared parts of the three generators: brands, colours, geometry, drawing.

Everything that more than one script needs lives here, so the scripts themselves
are short enough to read in one go. Nothing in here writes a file except
open_output_dir and write_config.

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

Three other things to know
--------------------------

Output goes to drafts/ by default, not brands/. Promoting a draft into the
registered set is a separate step, described in skills/11brands-promote-draft/.

Nothing that affects an image is hardcoded where it is drawn. Colours, every
drawn string, and the whole layout come from the brand, so they can all be
changed per brand.

Each brand folder holds two files. brand.md is the human record: the three
required fields and, more importantly, the notes explaining why the colour is
what it is. config.json is the machine-readable, fully resolved version of every
variable, including the layout numbers brand.md has no syntax for. When both
exist, config.json wins and any disagreement is reported, so tweaking a config to
test an idea is a two-line job and never a silent one.
"""

from __future__ import annotations

import json
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

BRAND_NAME = "brand.md"
CONFIG_NAME = "config.json"

# macOS ships this. On any other machine, point it at a monospaced .ttf with the
# same metrics or the cards will not match what is already published.
MONO_FONT = "/System/Library/Fonts/SFNSMono.ttf"

# ------------------------------------------------------------------ text tables
DEFAULT_FOOTER_TEXT = "AI / SOFTWARE / PRODUCT / ENGINEERING / TECHNOLOGY"
DEFAULT_CONTENT_TITLE = "Lorem Ipsum"

# A text field set to this, in any capitalisation, draws nothing at all. In
# config.json, JSON null means the same thing and reads better.
OMIT = "none"

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

# ---------------------------------------------------------------- layout tables
# Every number that positions or sizes something. These are the values the whole
# published family was drawn with, so a brand that overrides none of them
# reproduces its existing assets byte for byte.
DEFAULT_LAYOUT = {
    "card": [1200, 630],
    "mark_origin": [425, 42],
    "mark_size": 350,
    "mark_crop": [247, 247, 1007, 1007],
    "square": 18,
    "gap": 20,
    "max_row": 1040,
    "row_top": 477,
    "row_middle": 486,
    "title_max_pt": 42,
    "title_min_pt": 28,
    "masthead_middle": 56,
    "masthead_pt": 15,
    "masthead_tracking": 4,
    "footer_middle": 574,
    "footer_pt": 15,
}

DEFAULT_ICONS = {
    "master": 512,
    "box": [462, 368],
    "files": [
        {"size": 512, "name": "icon-512.png"},
        {"size": 192, "name": "icon-192.png"},
        {"size": 180, "name": "apple-touch-icon.png"},
        {"size": 32, "name": "favicon-32x32.png"},
        {"size": 16, "name": "favicon-16x16.png"},
    ],
    "ico_sizes": [16, 32, 48, 64, 128, 256],
}

CONFIG_NOTE = (
    "Every variable used to generate this brand's assets. Generated from "
    "brand.md, and authoritative over it once it exists: edit a value here and "
    "re-run a generator to test an idea. A text field set to null draws nothing. "
    "See asset-generation-scripts/README.md."
)


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
    # Every drawn string. Each defaults to something sensible, so a brand that
    # sets none of them behaves exactly as it did before these existed.
    masthead: str = ""       # content cards, above the mark; defaults to domain
    website_row: str = ""    # website card main row; defaults to domain
    footer_text: str = DEFAULT_FOOTER_TEXT
    default_title: str = DEFAULT_CONTENT_TITLE
    # Every number, and the font. Same story: defaults reproduce the family.
    layout: dict = field(default_factory=lambda: dict(DEFAULT_LAYOUT))
    icons: dict = field(default_factory=lambda: json.loads(json.dumps(DEFAULT_ICONS)))
    font_path: str = MONO_FONT
    source: Path | None = field(default=None, repr=False)
    config_source: Path | None = field(default=None, repr=False)

    def directory_in(self, root: str = DEFAULT_OUTPUT) -> Path:
        return OUTPUT_ROOTS[root] / self.key

    # Layout access, so the drawing code reads like the old constants did.
    def L(self, name: str):
        try:
            return self.layout[name]
        except KeyError:
            raise SystemExit(
                f"{self.key}: layout is missing {name!r}. Delete config.json and "
                f"regenerate it, or add the key."
            ) from None

    @property
    def card(self) -> tuple[int, int]:
        return tuple(self.L("card"))


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


def parse_text(value) -> str:
    """An optional text field. `none`, or JSON null, means draw nothing.

    The word is needed in brand.md because the field reader has to see a value to
    notice the line at all, so an empty one would be invisible to it. In
    config.json, null says the same thing without the magic word.
    """
    if value is None:
        return ""
    text = strip_value(str(value))
    return "" if text.lower() == OMIT else text


def hex_of(colour) -> str:
    return "#%02X%02X%02X" % tuple(colour)


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
        path = OUTPUT_ROOTS[name] / key / BRAND_NAME
        if path.exists():
            return path
    looked = ", ".join(
        str((OUTPUT_ROOTS[name] / key / BRAND_NAME).relative_to(V0_DIR))
        for name in order
    )
    raise SystemExit(f"no brand named {key!r}. Looked for: {looked}")


def _from_markdown(key: str, path: Path) -> Brand:
    """Read brand.md into a Brand carrying the default layout.

    The format is deliberately loose: any line shaped `**Key:** value` counts,
    anywhere in the document, so the file stays something a person writes rather
    than a config file wearing a disguise.
    """
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


def config_of(brand: Brand) -> dict:
    """The full resolved configuration, ready to write as JSON."""
    return {
        "_note": CONFIG_NOTE,
        "brand": brand.key,
        "domain": brand.domain,
        "mode": brand.mode,
        "colours": {
            "signal": hex_of(brand.signal),
            "ground": hex_of(brand.ground),
            "ink": hex_of(brand.ink),
            "footer": hex_of(brand.footer),
        },
        "text": {
            "masthead": brand.masthead or None,
            "website_row": brand.website_row or None,
            "footer_text": brand.footer_text or None,
            "default_title": brand.default_title or None,
        },
        "layout": dict(brand.layout),
        "icons": json.loads(json.dumps(brand.icons)),
        "font": {"mono": brand.font_path},
    }


def _apply_config(brand: Brand, path: Path, quiet: bool = False) -> Brand:
    """Overlay config.json onto a Brand read from brand.md, and report drift.

    config.json wins. That is the point of it: change a number, regenerate, look
    at the result. But brand.md is where the reasoning lives, so a disagreement
    between the two is worth saying out loud rather than discovering later from an
    asset nobody can explain.
    """
    try:
        cfg = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise SystemExit(f"{path.relative_to(V0_DIR)}: invalid JSON — {error}") from None

    drift = []

    if "domain" in cfg and cfg["domain"] != brand.domain:
        drift.append(f"domain {brand.domain!r} -> {cfg['domain']!r}")
        brand.domain = cfg["domain"]
    if "mode" in cfg and cfg["mode"] != brand.mode:
        drift.append(f"mode {brand.mode!r} -> {cfg['mode']!r}")
        brand.mode = cfg["mode"]

    for name in ("signal", "ground", "ink", "footer"):
        raw = cfg.get("colours", {}).get(name)
        if raw is None:
            continue
        value = parse_hex(raw)
        if value != getattr(brand, name):
            drift.append(f"{name} {hex_of(getattr(brand, name))} -> {hex_of(value)}")
            setattr(brand, name, value)

    for name in ("masthead", "website_row", "footer_text", "default_title"):
        section = cfg.get("text", {})
        if name not in section:
            continue
        value = parse_text(section[name])
        if value != getattr(brand, name):
            drift.append(
                f"{name} {getattr(brand, name) or '(omitted)'!r} -> "
                f"{value or '(omitted)'!r}"
            )
            setattr(brand, name, value)

    brand.layout = {**DEFAULT_LAYOUT, **cfg.get("layout", {})}
    layout_drift = [
        f"{k} {DEFAULT_LAYOUT[k]} -> {v}"
        for k, v in brand.layout.items()
        if k in DEFAULT_LAYOUT and v != DEFAULT_LAYOUT[k]
    ]
    brand.icons = {**json.loads(json.dumps(DEFAULT_ICONS)), **cfg.get("icons", {})}
    brand.font_path = cfg.get("font", {}).get("mono", brand.font_path)
    brand.config_source = path

    if not quiet and (drift or layout_drift):
        lines = [
            f"note: {path.relative_to(V0_DIR)} overrides {BRAND_NAME}, and is what "
            f"was used:",
        ]
        lines += [f"         {d}" for d in drift + layout_drift]
        lines.append(
            "       Update brand.md to match once an idea is settled, so the "
            "reasoning stays with the values."
        )
        print("\n".join(lines), file=sys.stderr)

    return brand


def load_brand(
    key: str, prefer: str = DEFAULT_OUTPUT, use_config: bool = True, quiet: bool = False
) -> Brand:
    """Read one brand: brand.md for the record, config.json for the values."""
    path = brand_file(key, prefer)
    brand = _from_markdown(key, path)
    config = path.parent / CONFIG_NAME
    if use_config and config.exists():
        brand = _apply_config(brand, config, quiet=quiet)
    return brand


def _pretty_json(value, indent: int = 0) -> str:
    """JSON that a person can edit: short flat collections stay on one line.

    The stock encoder puts every element of `[1200, 630]` on its own line, which
    turns a config of forty values into two hundred lines and buries the layout
    section. This is the same output, wrapped only where wrapping helps.
    """
    pad = " " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        flat = all(not isinstance(v, (dict, list)) for v in value.values())
        if flat:
            one = "{" + ", ".join(
                f"{json.dumps(k)}: {json.dumps(v)}" for k, v in value.items()
            ) + "}"
            if len(one) + indent <= 78:
                return one
        body = ",\n".join(
            f"{pad}  {json.dumps(k)}: {_pretty_json(v, indent + 2)}"
            for k, v in value.items()
        )
        return "{\n" + body + f"\n{pad}}}"
    if isinstance(value, list):
        if not value:
            return "[]"
        if all(not isinstance(v, (dict, list)) for v in value):
            return "[" + ", ".join(json.dumps(v) for v in value) + "]"
        body = ",\n".join(f"{pad}  {_pretty_json(v, indent + 2)}" for v in value)
        return "[\n" + body + f"\n{pad}]"
    return json.dumps(value)


def write_config(brand: Brand, directory: Path | None = None) -> Path:
    """Write config.json beside a brand's brand.md.

    Regenerating one is always safe in the sense that nothing is lost that was not
    already expressible: it is the resolved view of brand.md plus the defaults. It
    is not safe for hand-edited layout values, which is why the generators only
    ever create a missing one and never refresh an existing one.
    """
    directory = directory or (brand.source.parent if brand.source else None)
    if directory is None:
        raise SystemExit(f"{brand.key}: nowhere to write {CONFIG_NAME}")
    path = directory / CONFIG_NAME
    path.write_text(_pretty_json(config_of(brand)) + "\n")
    return path


def ensure_config(brand: Brand, quiet: bool = False) -> Path | None:
    """Create config.json if the brand has none. Never overwrites one."""
    if brand.config_source is not None:
        return None
    path = write_config(brand)
    brand.config_source = path
    if not quiet:
        print(f"    wrote {path.relative_to(V0_DIR)}")
    return path


def every_brand() -> list[str]:
    """The registered family: every key with a brand.md in brands/.

    Deliberately not "every key in either root". drafts/ holds work in progress
    and rejected attempts, and neither belongs in a sweep — regenerating a
    rejected draft because it still has a brand.md is a good way to resurrect a
    colour someone already decided against. A draft is named explicitly.
    """
    return sorted(path.parent.name for path in BRANDS_DIR.glob(f"*/{BRAND_NAME}"))


def every_draft() -> list[str]:
    """Every key with a brand.md in drafts/. Never used for --all; see above."""
    return sorted(path.parent.name for path in DRAFTS_DIR.glob(f"*/{BRAND_NAME}"))


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
    box = tuple(box)
    size = tuple(size)
    ink_mask, signal_mask = (
        mask.crop(box).resize(size, Image.Resampling.LANCZOS) for mask in masks
    )
    ink_px, signal_px = ink_mask.load(), signal_mask.load()

    tile = Image.new("RGB", size, tuple(ground))
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
def font(points: int, path: str = MONO_FONT) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, points)
    except OSError as error:  # pragma: no cover - environment dependent
        raise SystemExit(
            f"could not open {path}. Set the font in the brand's "
            f"{CONFIG_NAME} (font.mono), or MONO_FONT in brandkit.py, to a "
            "monospaced .ttf with the same metrics."
        ) from error


def text_width(draw: ImageDraw.ImageDraw, value: str, points: int,
               path: str = MONO_FONT) -> int:
    box = draw.textbbox((0, 0), value, font=font(points, path))
    return box[2] - box[0]


def draw_tracked(draw, value, centre_x, middle_y, points, fill, tracking,
                 path: str = MONO_FONT):
    """Mono with extra letter spacing, drawn centred, one glyph at a time.

    Pillow has no tracking. The domain needs it: unspaced, a short string at
    this size looks dropped into the space rather than placed in it.
    """
    glyphs = [(char, text_width(draw, char, points, path)) for char in value]
    total = sum(w for _, w in glyphs) + tracking * (len(glyphs) - 1)
    x = centre_x - total / 2
    for char, width in glyphs:
        draw.text((x, middle_y), char, font=font(points, path), fill=fill, anchor="lm")
        x += width + tracking


def fit_row(draw, text: str, brand: Brand) -> tuple[int, int, int]:
    """Largest point size whose framed row fits, with that row's measurements."""
    square, gap = brand.L("square"), brand.L("gap")
    fixed = square + gap + gap + square
    top, bottom = brand.L("title_max_pt"), brand.L("title_min_pt")
    for points in range(top, bottom - 1, -1):
        width = text_width(draw, text, points, brand.font_path)
        if fixed + width <= brand.L("max_row"):
            return points, width, fixed + width
    width = text_width(draw, text, bottom, brand.font_path)
    return bottom, width, fixed + width


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

    points, width, row_width = fit_row(draw, text, brand)
    square, gap = brand.L("square"), brand.L("gap")
    row_top, row_middle = brand.L("row_top"), brand.L("row_middle")
    start = round(brand.card[0] / 2 - row_width / 2)

    draw.rectangle(
        (start, row_top, start + square - 1, row_top + square - 1), fill=brand.signal
    )
    left = start + square + gap
    draw.text(
        (left, row_middle), text, font=font(points, brand.font_path),
        fill=brand.ink, anchor="lm",
    )
    right = left + width + gap
    draw.rectangle(
        (right, row_top, right + square - 1, row_top + square - 1), fill=brand.signal
    )


def draw_masthead(draw, brand: Brand) -> None:
    """The tracked domain line above the mark, on content cards only."""
    if not brand.masthead:
        return
    draw_tracked(
        draw,
        brand.masthead,
        brand.card[0] / 2,
        brand.L("masthead_middle"),
        brand.L("masthead_pt"),
        brand.footer,
        brand.L("masthead_tracking"),
        brand.font_path,
    )


def draw_footer(draw, brand: Brand) -> None:
    if not brand.footer_text:
        return
    draw.text(
        (brand.card[0] / 2, brand.L("footer_middle")),
        brand.footer_text,
        font=font(brand.L("footer_pt"), brand.font_path),
        fill=brand.footer,
        anchor="mm",
    )


def new_card(brand: Brand, masks) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """A blank card with the mark already on it."""
    image = Image.new("RGB", brand.card, tuple(brand.ground))
    size = brand.L("mark_size")
    # Composed on the card's own ground and pasted opaquely, which is exact
    # because they are the same colour.
    image.paste(
        compose(
            masks, brand.L("mark_crop"), (size, size),
            brand.ground, brand.ink, brand.signal,
        ),
        tuple(brand.L("mark_origin")),
    )
    return image, ImageDraw.Draw(image)


# ------------------------------------------------------------------------ icons
def icon_at(masks, box, artwork_size, size, brand: Brand) -> Image.Image:
    """One square icon, artwork scaled to the shared margin and centred."""
    icon_box = brand.icons["box"]
    scale = min(
        icon_box[0] / artwork_size[0], icon_box[1] / artwork_size[1]
    ) * (size / brand.icons["master"])
    target = (
        max(1, round(artwork_size[0] * scale)),
        max(1, round(artwork_size[1] * scale)),
    )

    icon = Image.new("RGB", (size, size), tuple(brand.ground))
    icon.paste(
        compose(masks, box, target, brand.ground, brand.ink, brand.signal),
        ((size - target[0]) // 2, (size - target[1]) // 2),
    )
    return icon


def write_icon_set(masks, brand: Brand, directory: Path) -> list[Path]:
    """The PNGs and a multi-frame .ico, every one composed at its own size.

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
    for entry in brand.icons["files"]:
        path = directory / entry["name"]
        icon_at(masks, box, artwork_size, entry["size"], brand).convert("RGBA").save(
            path, optimize=True
        )
        written.append(path)

    ico_sizes = [(n, n) for n in brand.icons["ico_sizes"]]
    frames = [
        icon_at(masks, box, artwork_size, width, brand).convert("RGBA")
        for width, _ in sorted(ico_sizes, reverse=True)
    ]
    ico = directory / "favicon.ico"
    frames[0].save(ico, format="ICO", sizes=ico_sizes, append_images=frames[1:])
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
            f"         brands/{brand.key}/ will hold runs with no {BRAND_NAME} "
            f"beside them.\n"
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

    Records the text and any changed layout as well as the colours. A card's
    strings and positions are as much a part of what was generated as its palette,
    and once they are variables they can no longer be re-derived from the domain
    alone.
    """
    path = directory / "MANIFEST.md"
    source = str(brand.source.relative_to(V0_DIR)) if brand.source else "unknown"
    config = (
        str(brand.config_source.relative_to(V0_DIR)) if brand.config_source else "none"
    )
    changed = {
        k: v for k, v in brand.layout.items()
        if k in DEFAULT_LAYOUT and v != DEFAULT_LAYOUT[k]
    }
    layout_section = (
        "## Layout\n\nDefault for the family.\n\n"
        if not changed
        else "## Layout\n\nChanged from the family default:\n\n"
        + "| Key | Default | Used |\n| --- | --- | --- |\n"
        + "".join(f"| {k} | `{DEFAULT_LAYOUT[k]}` | `{v}` |\n" for k, v in changed.items())
        + "\n"
    )
    path.write_text(
        f"# {brand.domain} — {kind}\n\n"
        f"Generated {datetime.now().isoformat(timespec='seconds')} "
        f"by `asset-generation-scripts/`.\n\n"
        f"| Setting | Value |\n| --- | --- |\n"
        f"| Brand | `{brand.key}` |\n"
        f"| Domain | {brand.domain} |\n"
        f"| Definition | `{source}` |\n"
        f"| Config | `{config}` |\n"
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
        + "\n" + layout_section
        + "## Files\n\n" + "\n".join(f"- `{name}`" for name in entries) + "\n"
    )
    return path
