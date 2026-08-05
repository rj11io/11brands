"""Shared parts of the v1 generators: config reading, colour maths, drawing.

The one idea worth understanding
--------------------------------

The mark is never stored as a picture. It is stored as two coverage maps: how
much of each pixel the numeral covers, and how much the signal square covers.
Colour is applied last, at the size being drawn.

That ordering is the whole point. Resizing a finished picture of the mark rings:
Lanczos overshoots at every hard edge, so a downscale invents pixels darker than
the ground, brighter than the numeral, and more saturated than the signal. It is
how a 16 pixel icon once shipped carrying a #2FE0A1 square its brand never had.
Resizing coverage cannot do that, because every output pixel ends up a blend of
exactly three known colours.

How v1 is arranged
------------------

A brand is brands/<key>/config.json (every variable, the only file the scripts
read) plus brands/<key>/brand.md (the decision record, never parsed). Templates
for both live in templates/. Output goes to outputs/<stamp>/<key>/<kind>/, one
stamp per run, shared across a batch.

archive/ holds retired brands, moved there verbatim by archive_brand.py and
back by promote_brand.py. Nothing else ever reads it: the generators resolve
keys through brands/ only, so an archived brand cannot be generated, swept up
by --all, or collide with a new brand of the same key.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCRIPTS_DIR = Path(__file__).resolve().parent
V1_DIR = SCRIPTS_DIR.parent
TEMPLATES_DIR = V1_DIR / "templates"
BRANDS_DIR = V1_DIR / "brands"
ARCHIVE_DIR = V1_DIR / "archive"
OUTPUTS_DIR = V1_DIR / "outputs"
MARK_PATH = TEMPLATES_DIR / "mark.png"

SCHEMA = 1
CONFIG_NAME = "config.json"
BRAND_NAME = "brand.md"

# The three output kinds and their folder names.
KINDS = ("favicons", "og-web", "og-content")

REQUIRED_COLORS = ("signal", "ground", "ink", "footer")
REQUIRED_TEXT = ("masthead", "website_row", "footer_text", "title")
REQUIRED_LAYOUT = (
    "card", "mark_origin", "mark_size", "mark_crop", "square", "gap", "max_row",
    "row_top", "row_middle", "row_max_pt", "row_min_pt", "masthead_middle",
    "masthead_pt", "masthead_tracking", "footer_middle", "footer_pt",
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
    masthead: str        # "" draws nothing (null in config)
    website_row: str
    footer_text: str
    title: str           # the content-og default title
    layout: dict
    icons: dict
    font_path: str
    font_index: int
    source: Path = field(repr=False, default=None)

    def L(self, name: str):
        return self.layout[name]

    @property
    def card(self) -> tuple[int, int]:
        return tuple(self.layout["card"])


def parse_hex(value: str) -> tuple[int, int, int]:
    text = str(value).strip().lstrip("#")
    if len(text) != 6:
        raise SystemExit(f"expected a six digit hex colour, got {value!r}")
    return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))


def hex_of(colour) -> str:
    return "#%02X%02X%02X" % tuple(colour)


def load_config(path: Path) -> dict:
    """Read and structurally validate a config.json."""
    try:
        cfg = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise SystemExit(f"{path}: invalid JSON — {error}") from None

    if cfg.get("schema") != SCHEMA:
        raise SystemExit(
            f"{path}: schema is {cfg.get('schema')!r}, these scripts read schema "
            f"{SCHEMA}"
        )
    problems = []
    for name in ("brand", "domain", "mode"):
        if not cfg.get(name):
            problems.append(f"missing {name!r}")
    for name in REQUIRED_COLORS:
        if not cfg.get("colors", {}).get(name):
            problems.append(f"missing colors.{name}")
    for name in REQUIRED_TEXT:
        if name not in cfg.get("text", {}):
            problems.append(f"missing text.{name}")
    for name in REQUIRED_LAYOUT:
        if name not in cfg.get("layout", {}):
            problems.append(f"missing layout.{name}")
    if not cfg.get("icons", {}).get("files"):
        problems.append("missing icons.files")
    if not cfg.get("font", {}).get("path"):
        problems.append("missing font.path")
    if problems:
        raise SystemExit(f"{path}: " + "; ".join(problems))
    return cfg


def load_brand(key: str) -> Brand:
    path = BRANDS_DIR / key / CONFIG_NAME
    if not path.exists():
        hint = (
            "It is archived; promote it with promote_brand.py first."
            if (ARCHIVE_DIR / key / CONFIG_NAME).exists()
            else "Initialise it with init_brand.py."
        )
        raise SystemExit(
            f"no brand named {key!r} (no {path.relative_to(V1_DIR)}). {hint}"
        )
    cfg = load_config(path)
    if cfg["brand"] != key:
        raise SystemExit(
            f"{path.relative_to(V1_DIR)}: 'brand' is {cfg['brand']!r} but the "
            f"folder is {key!r}. Fix the config so the two agree."
        )
    text = cfg["text"]
    return Brand(
        key=key,
        domain=cfg["domain"],
        mode=cfg["mode"],
        signal=parse_hex(cfg["colors"]["signal"]),
        ground=parse_hex(cfg["colors"]["ground"]),
        ink=parse_hex(cfg["colors"]["ink"]),
        footer=parse_hex(cfg["colors"]["footer"]),
        masthead=text["masthead"] or "",
        website_row=text["website_row"] or "",
        footer_text=text["footer_text"] or "",
        title=text["title"] or "",
        layout=cfg["layout"],
        icons=cfg["icons"],
        font_path=cfg["font"]["path"],
        font_index=int(cfg["font"].get("index", 0)),
        source=path,
    )


def every_brand() -> list[str]:
    """Active brands only. archive/ is deliberately invisible to generation."""
    return sorted(p.parent.name for p in BRANDS_DIR.glob(f"*/{CONFIG_NAME}"))


def every_archived() -> list[str]:
    return sorted(p.parent.name for p in ARCHIVE_DIR.glob(f"*/{CONFIG_NAME}"))


def resolve_keys(key: str | None, all_flag: bool) -> list[str]:
    """The brand list a generator should run over, from its CLI arguments."""
    if all_flag:
        keys = every_brand()
        if not keys:
            raise SystemExit("no brands registered yet; initialise one first")
        return keys
    if key:
        return [key]
    raise SystemExit("name a brand, or pass --all")


def template_config(mode: str) -> tuple[Path, dict]:
    path = TEMPLATES_DIR / f"config-{mode}.template.json"
    if not path.exists():
        raise SystemExit(f"no template for mode {mode!r} at {path}")
    return path, json.loads(path.read_text())


def contrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    """WCAG contrast ratio between two colours."""
    def luminance(c):
        def channel(v):
            v /= 255
            return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
        r, g, bl = (channel(x) for x in c)
        return 0.2126 * r + 0.7152 * g + 0.0722 * bl
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def pretty_json(value, indent: int = 0) -> str:
    """JSON a person can edit: short flat collections stay on one line."""
    pad = " " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        if all(not isinstance(v, (dict, list)) for v in value.values()):
            one = "{" + ", ".join(
                f"{json.dumps(k)}: {json.dumps(v)}" for k, v in value.items()
            ) + "}"
            if len(one) + indent <= 78:
                return one
        body = ",\n".join(
            f"{pad}  {json.dumps(k)}: {pretty_json(v, indent + 2)}"
            for k, v in value.items()
        )
        return "{\n" + body + f"\n{pad}}}"
    if isinstance(value, list):
        if not value:
            return "[]"
        if all(not isinstance(v, (dict, list)) for v in value):
            return "[" + ", ".join(json.dumps(v) for v in value) + "]"
        body = ",\n".join(f"{pad}  {pretty_json(v, indent + 2)}" for v in value)
        return "[\n" + body + f"\n{pad}]"
    return json.dumps(value)


# ------------------------------------------------------------------------ masks
def build_masks(mark_path: Path = MARK_PATH):
    """Split the mark master into numeral coverage and signal coverage.

    Sorted by hue, because green leading is the only thing that tells the signal
    square apart from the numeral, at any opacity including its anti-aliased
    edge. The two never overlap in the master.
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
    box, size = tuple(box), tuple(size)
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
            # Clamp back onto the simplex: mask ringing can push the pair past
            # full coverage, and the surplus would otherwise come out of the
            # ground going negative.
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
def font(brand: Brand, points: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(brand.font_path, points, index=brand.font_index)
    except OSError as error:  # pragma: no cover - environment dependent
        raise SystemExit(
            f"could not open {brand.font_path} (index {brand.font_index}). "
            f"Fix font.path in {brand.source}; templates/FONTS.md lists what "
            f"this machine has."
        ) from error


def text_width(draw, brand: Brand, value: str, points: int) -> int:
    box = draw.textbbox((0, 0), value, font=font(brand, points))
    return box[2] - box[0]


def draw_tracked(draw, brand: Brand, value, centre_x, middle_y, points, fill, tracking):
    """Text with extra letter spacing, drawn centred, one glyph at a time.

    Pillow has no tracking. The masthead needs it: unspaced, a short string at
    this size looks dropped into the space rather than placed in it.
    """
    glyphs = [(char, text_width(draw, brand, char, points)) for char in value]
    total = sum(w for _, w in glyphs) + tracking * (len(glyphs) - 1)
    x = centre_x - total / 2
    for char, width in glyphs:
        draw.text((x, middle_y), char, font=font(brand, points), fill=fill, anchor="lm")
        x += width + tracking


def fit_row(draw, brand: Brand, text: str) -> tuple[int, int, int]:
    """Largest point size whose framed row fits, with that row's measurements."""
    square, gap = brand.L("square"), brand.L("gap")
    fixed = square + gap + gap + square
    for points in range(brand.L("row_max_pt"), brand.L("row_min_pt") - 1, -1):
        width = text_width(draw, brand, text, points)
        if fixed + width <= brand.L("max_row"):
            return points, width, fixed + width
    width = text_width(draw, brand, text, brand.L("row_min_pt"))
    return brand.L("row_min_pt"), width, fixed + width


def draw_framed_row(draw, brand: Brand, text: str) -> None:
    """The signature row: a signal square, the text, a signal square.

    An empty string draws nothing, squares included — a row framing no text is
    two floating dots, not a design.
    """
    if not text:
        return
    points, width, row_width = fit_row(draw, brand, text)
    square, gap = brand.L("square"), brand.L("gap")
    row_top, row_middle = brand.L("row_top"), brand.L("row_middle")
    start = round(brand.card[0] / 2 - row_width / 2)

    draw.rectangle(
        (start, row_top, start + square - 1, row_top + square - 1), fill=brand.signal
    )
    left = start + square + gap
    draw.text(
        (left, row_middle), text, font=font(brand, points), fill=brand.ink, anchor="lm"
    )
    right = left + width + gap
    draw.rectangle(
        (right, row_top, right + square - 1, row_top + square - 1), fill=brand.signal
    )


def draw_masthead(draw, brand: Brand) -> None:
    """The tracked line above the mark, content cards only."""
    if not brand.masthead:
        return
    draw_tracked(
        draw, brand, brand.masthead,
        brand.card[0] / 2, brand.L("masthead_middle"), brand.L("masthead_pt"),
        brand.footer, brand.L("masthead_tracking"),
    )


def draw_footer(draw, brand: Brand) -> None:
    if not brand.footer_text:
        return
    draw.text(
        (brand.card[0] / 2, brand.L("footer_middle")),
        brand.footer_text,
        font=font(brand, brand.L("footer_pt")),
        fill=brand.footer,
        anchor="mm",
    )


def new_card(brand: Brand, masks):
    """A blank card with the mark already on it."""
    image = Image.new("RGB", brand.card, tuple(brand.ground))
    size = brand.L("mark_size")
    # Composed on the card's own ground and pasted opaquely, which is exact
    # because they are the same colour.
    image.paste(
        compose(masks, brand.L("mark_crop"), (size, size),
                brand.ground, brand.ink, brand.signal),
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
    """The PNGs and a multi-frame .ico, every frame composed at its own size.

    Two rules are load bearing, both learned by breaking something:

    Write RGBA, never a palette image. A palette PNG is valid and smaller, and it
    breaks a Next.js build, which decodes app/favicon.ico itself and rejects any
    frame that is not RGBA.

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


def new_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def output_dir(brand: Brand, kind: str, stamp: str) -> Path:
    """outputs/<stamp>/<key>/<kind>/, created.

    One stamp per run; a batch passes the same stamp to every generator so the
    whole run lands in one folder. Reusing a stamp adds to that run.
    """
    if kind not in KINDS:
        raise SystemExit(f"unknown kind {kind!r}, expected one of {KINDS}")
    directory = OUTPUTS_DIR / stamp / brand.key / kind
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _text_row(label: str, value: str) -> str:
    return f"| {label} | {'*(omitted)*' if not value else value} |\n"


def write_manifest(directory: Path, brand: Brand, kind: str, entries: list[str]) -> Path:
    """What was made, from what, so a run explains itself later.

    Records the full palette and text, and any layout value that differs from
    the brand's mode template — a config tweak should be visible here, not
    re-derived from the pixels.
    """
    try:
        defaults = template_config(brand.mode)[1].get("layout", {})
    except SystemExit:
        defaults = {}
    changed = {
        k: v for k, v in brand.layout.items() if defaults.get(k, v) != v
    }
    layout_section = (
        "## Layout\n\nTemplate default.\n"
        if not changed
        else "## Layout\n\nChanged from the template:\n\n"
        + "| Key | Template | Used |\n| --- | --- | --- |\n"
        + "".join(f"| {k} | `{defaults[k]}` | `{v}` |\n" for k, v in changed.items())
    )
    path = directory / "MANIFEST.md"
    path.write_text(
        f"# {brand.domain} — {kind}\n\n"
        f"Generated {datetime.now().isoformat(timespec='seconds')} by "
        f"`v1/scripts/` from `brands/{brand.key}/{CONFIG_NAME}`.\n\n"
        f"| Setting | Value |\n| --- | --- |\n"
        f"| Brand | `{brand.key}` |\n"
        f"| Domain | {brand.domain} |\n"
        f"| Mode | {brand.mode} |\n"
        f"| Signal | `{hex_of(brand.signal)}` |\n"
        f"| Ground | `{hex_of(brand.ground)}` |\n"
        f"| Ink | `{hex_of(brand.ink)}` |\n"
        f"| Footer | `{hex_of(brand.footer)}` |\n"
        f"| Font | `{brand.font_path}` index {brand.font_index} |\n\n"
        "## Text\n\n| Field | Value |\n| --- | --- |\n"
        + _text_row("Masthead", brand.masthead)
        + _text_row("Website row", brand.website_row)
        + _text_row("Footer text", brand.footer_text)
        + _text_row("Title (default)", brand.title)
        + "\n" + layout_section
        + "\n## Files\n\n" + "\n".join(f"- `{name}`" for name in entries) + "\n"
    )
    return path
