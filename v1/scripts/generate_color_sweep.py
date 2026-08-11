"""Generate an exhaustive Tailwind color preview for one testing brand.

The sweep keeps the brand key singular and varies only the signal colour and
light/dark palette context. It is an experiment, not a canonical asset pack:
every Tailwind token is rendered, including tokens that fail the normal
contrast guidance. The source palette is a small, checked-in CSS extract from
Tailwind's v4.3 theme.

Output defaults to /private/tmp/11colorlab/<stamp>/ and contains an HTML atlas,
machine-readable metadata, exact-size favicon previews, and 1200x630 cards.
The candidate config is read but never changed.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
from dataclasses import replace
from pathlib import Path

import brandkit as kit


DEFAULT_PALETTE = kit.SCRIPTS_DIR / "data" / "tailwind-v4.3.2.css"
DEFAULT_OUTPUT = Path("/private/tmp/11colorlab")
SHADE_ORDER = (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950)
TOKEN_RE = re.compile(
    r"--color-(?P<family>[a-z]+)-(?P<shade>50|100|200|300|400|500|600|700|800|900|950):\s*"
    r"(?P<value>oklch\([^;]+\));"
)
SPECIAL_RE = re.compile(r"--color-(?P<name>black|white):\s*(?P<value>#[0-9a-fA-F]{3,6});")
OKLCH_RE = re.compile(
    r"oklch\(\s*(?P<l>[0-9.]+)%\s+(?P<c>[0-9.]+)\s+(?P<h>[0-9.]+)\s*\)"
)


def oklch_to_hex(value: str) -> str:
    """Convert CSS OKLCH to clamped six-digit sRGB hex."""
    match = OKLCH_RE.fullmatch(value.strip())
    if not match:
        raise SystemExit(f"unsupported OKLCH value {value!r}")

    lightness = float(match["l"]) / 100
    chroma = float(match["c"])
    hue = math.radians(float(match["h"]))
    a = chroma * math.cos(hue)
    b = chroma * math.sin(hue)

    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
    l = l_**3
    m = m_**3
    s = s_**3

    linear = (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )

    def srgb(channel: float) -> int:
        if channel <= 0:
            return 0
        if channel >= 1:
            return 255
        encoded = 12.92 * channel if channel <= 0.0031308 else 1.055 * channel ** (1 / 2.4) - 0.055
        return max(0, min(255, round(encoded * 255)))

    return "#%02X%02X%02X" % tuple(srgb(channel) for channel in linear)


def parse_palette(path: Path) -> list[dict]:
    text = path.read_text()
    tokens = []
    for match in TOKEN_RE.finditer(text):
        family = match["family"]
        shade = int(match["shade"])
        value = match["value"].strip()
        tokens.append(
            {
                "token": f"{family}-{shade}",
                "family": family,
                "shade": shade,
                "source": value,
                "hex": oklch_to_hex(value),
                "oklch": value,
            }
        )
    for match in SPECIAL_RE.finditer(text):
        value = match["value"]
        if len(value) == 4:
            value = "#" + "".join(char * 2 for char in value[1:])
        tokens.append(
            {
                "token": match["name"],
                "family": match["name"],
                "shade": None,
                "source": value.upper(),
                "hex": value.upper(),
                "oklch": None,
            }
        )

    families = {token["family"] for token in tokens if token["shade"] is not None}
    by_family = {family: [] for family in families}
    for token in tokens:
        if token["shade"] is not None:
            by_family[token["family"]].append(token["shade"])
    bad_families = {
        family: sorted(shades)
        for family, shades in by_family.items()
        if tuple(sorted(shades)) != SHADE_ORDER
    }
    if len(families) != 26 or len(tokens) != 288 or bad_families:
        raise SystemExit(
            f"expected Tailwind v4.3 palette: 26 families, 288 tokens, "
            f"11 shades each plus black and white; got {len(families)} families, {len(tokens)} tokens, "
            f"invalid families {bad_families}"
        )

    family_order = list(dict.fromkeys(token["family"] for token in tokens))
    order = {family: index for index, family in enumerate(family_order)}
    return sorted(
        tokens,
        key=lambda token: (
            token["shade"] is None,
            order[token["family"]],
            token["shade"] if token["shade"] is not None else 0,
        ),
    )


def context_brand(brand: kit.Brand, mode: str, signal: str, title: str) -> kit.Brand:
    if mode == "dark":
        ground, ink, footer = "#0A0A0A", "#FAFAFA", "#A1A1A1"
    else:
        ground, ink, footer = "#FAFAFA", "#0A0A0A", "#676767"
    return replace(
        brand,
        mode=mode,
        signal=kit.parse_hex(signal),
        ground=kit.parse_hex(ground),
        ink=kit.parse_hex(ink),
        footer=kit.parse_hex(footer),
        title=title,
    )


def write_card(brand: kit.Brand, masks, path: Path) -> None:
    image, draw = kit.new_card(brand, masks)
    kit.draw_masthead(draw, brand)
    kit.draw_framed_row(draw, brand, brand.title)
    kit.draw_footer(draw, brand)
    image.save(path, optimize=True)


def write_icon(brand: kit.Brand, masks, size: int, path: Path) -> None:
    box = kit.union_box(masks)
    artwork_size = (box[2] - box[0], box[3] - box[1])
    kit.icon_at(masks, box, artwork_size, size, brand).convert("RGBA").save(
        path, optimize=True
    )


def tile_html(item: dict) -> str:
    label = html.escape(item["token"])
    mode = html.escape(item["mode"])
    signal = html.escape(item["signal"])
    contrast = f"{item['contrast']:.2f}:1"
    path = html.escape(item["relative_card"])
    icon16 = html.escape(item["relative_icon16"])
    icon32 = html.escape(item["relative_icon32"])
    return f"""
    <article class=tile data-mode={mode} data-token={label}>
      <div class=swatch style=background:{signal} title={signal}></div>
      <div class=meta><strong>{label}</strong><span>{mode}</span></div>
      <code>{signal}</code><span class=contrast>{contrast}</span>
      <div class=icons><img src={icon16} width=16 height=16 alt="16px mark"><img src={icon32} width=32 height=32 alt="32px mark"></div>
      <img class=card src={path} loading=lazy alt="{label} {mode} OG card">
    </article>
    """


def write_index(path: Path, brand: kit.Brand, metadata: dict) -> None:
    tiles = "\n".join(tile_html(item) for item in metadata["previews"])
    path.write_text(
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tailwind color sweep</title><style>
:root{color-scheme:light dark;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#111;color:#eee}
body{margin:0;padding:24px}.header{position:sticky;top:0;z-index:2;background:#111;padding:12px 0 20px;border-bottom:1px solid #444}.filters{display:flex;gap:12px;flex-wrap:wrap;align-items:center}.filters button{font:inherit;background:#222;color:#eee;border:1px solid #666;border-radius:6px;padding:6px 10px;cursor:pointer}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-top:20px}.tile{background:#222;border:1px solid #444;border-radius:8px;padding:10px;display:grid;grid-template-columns:44px 1fr auto;gap:6px 10px;align-items:center}.swatch{grid-row:span 3;width:44px;height:44px;border-radius:6px;border:1px solid #888}.meta{display:flex;flex-direction:column;gap:2px}.meta span,.contrast{color:#aaa;font-size:12px}.icons{display:flex;align-items:center;gap:8px}.icons img{image-rendering:pixelated;background:#000;border:1px solid #555}.card{grid-column:1/-1;width:100%;height:auto;border:1px solid #555}.muted{color:#aaa;font-size:12px}
</style></head><body><header class=header><h1>Tailwind color sweep: """
        + html.escape(brand.key)
        + """</h1><p class=muted>All tokens rendered against both palette contexts. Contrast is reported, never filtered.</p><div class=filters><button onclick="filter('all')">all</button><button onclick="filter('dark')">dark</button><button onclick="filter('light')">light</button><span id=count></span></div></header><main class=grid>"""
        + tiles
        + """</main><script>function filter(mode){document.querySelectorAll('.tile').forEach(tile=>tile.hidden=mode!=='all'&&tile.dataset.mode!==mode);document.getElementById('count').textContent=[...document.querySelectorAll('.tile')].filter(tile=>!tile.hidden).length+' previews'}filter('all')</script></body></html>
"""
    )


def generate(key: str, output: Path, palette_path: Path) -> None:
    brand = kit.load_brand(key)
    tokens = parse_palette(palette_path)
    masks = kit.build_masks()
    output.mkdir(parents=True, exist_ok=False)
    previews = []

    for mode in ("dark", "light"):
        mode_dir = output / mode
        mode_dir.mkdir()
        for token in tokens:
            slug = token["token"]
            token_dir = mode_dir / slug
            token_dir.mkdir()
            variant = context_brand(brand, mode, token["hex"], f"{brand.domain} / {slug}")
            card = token_dir / "og-card.png"
            icon16 = token_dir / "icon-16.png"
            icon32 = token_dir / "icon-32.png"
            write_card(variant, masks, card)
            write_icon(variant, masks, 16, icon16)
            write_icon(variant, masks, 32, icon32)
            previews.append(
                {
                    **token,
                    "mode": mode,
                    "ground": kit.hex_of(variant.ground),
                    "ink": kit.hex_of(variant.ink),
                    "footer": kit.hex_of(variant.footer),
                    "signal": token["hex"],
                    "contrast": round(kit.contrast(variant.signal, variant.ground), 4),
                    "relative_card": str(card.relative_to(output)),
                    "relative_icon16": str(icon16.relative_to(output)),
                    "relative_icon32": str(icon32.relative_to(output)),
                }
            )

    metadata = {
        "schema": 1,
        "brand": key,
        "source_config": str(brand.source.relative_to(kit.V1_DIR)),
        "palette_source": str(palette_path.relative_to(kit.V1_DIR))
        if palette_path.is_relative_to(kit.V1_DIR)
        else str(palette_path),
        "palette_source_url": "https://tailwindcss.com/docs/colors",
        "palette_version": "tailwind-v4.3.2",
        "conversion": "CSS OKLCH to sRGB hex with channel clamping; black and white remain source hex",
        "token_count": len(tokens),
        "mode_count": 2,
        "preview_count": len(previews),
        "previews": previews,
    }
    (output / "COLOR-SWEEP.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (output / "MANIFEST.md").write_text(
        f"# Tailwind color sweep — {key}\n\n"
        f"Experimental preview. Source config: `{brand.source.relative_to(kit.V1_DIR)}`.\n\n"
        f"- Palette: Tailwind v4.3.2, 288 tokens\n"
        f"- Modes: dark and light\n"
        f"- Previews: {len(previews)}\n"
        f"- Contrast: reported only; no candidates filtered\n"
        f"- Source: https://tailwindcss.com/docs/colors\n"
    )
    write_index(output / "index.html", brand, metadata)
    print(f"color sweep {key}: {len(tokens)} tokens x 2 modes = {len(previews)} previews")
    print(f"  -> {output}/index.html")
    print(f"  -> {output}/COLOR-SWEEP.json")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", help="one active testing brand key")
    parser.add_argument("--palette-css", type=Path, default=DEFAULT_PALETTE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run", help="run stamp; defaults to now")
    args = parser.parse_args()

    if not args.palette_css.exists():
        raise SystemExit(f"no palette CSS at {args.palette_css}")
    stamp = args.run or kit.new_stamp()
    output = args.output / stamp
    if output.exists():
        raise SystemExit(f"{output} already exists; choose a new run stamp")
    generate(args.key, output, args.palette_css)


if __name__ == "__main__":
    main()
