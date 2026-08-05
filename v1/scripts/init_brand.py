"""Initialise a brand: brands/<key>/{config.json,brand.md} from the templates.

The key convention is {brand-title}-{variant}, e.g. 11io-dark-orange — where
11io is the brand title for www.rj11.io and dark-orange is what distinguishes
this variant from any other attempt at the same brand.

The mode picks the template (config-dark or config-light); operator flags
overwrite brand, domain and colours on top of it. Every value in the written
config is explicit — a text flag given the literal value `none` writes JSON
null, which draws nothing.

    python3 init_brand.py 11io-dark-orange --domain www.rj11.io --mode dark --signal '#F97316'
    python3 init_brand.py cc-dark-titanium --domain cc.rj11.io --mode dark \
        --signal '#B4BDC4' --title 'Lorem Ipsum'

Prints the signal-on-ground contrast before finishing: a non-text graphic needs
3:1, and the number is reported rather than assumed. Refuses to overwrite an
existing brand.
"""

from __future__ import annotations

import argparse
import re

import brandkit as kit

KEY_SHAPE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)+$")


def text_value(raw: str | None, fallback):
    """A text flag: absent keeps the fallback, literal `none` writes null."""
    if raw is None:
        return fallback
    return None if raw.strip().lower() == "none" else raw


def init(args) -> None:
    key = args.key
    if not KEY_SHAPE.match(key):
        raise SystemExit(
            f"key {key!r} does not match the {{brand-title}}-{{variant}} "
            f"convention, e.g. 11io-dark-orange"
        )
    target = kit.BRANDS_DIR / key
    if target.exists():
        raise SystemExit(
            f"{target.relative_to(kit.V1_DIR)} already exists; refusing to "
            f"overwrite. Pick a new variant key or remove the old brand first."
        )

    _, cfg = kit.template_config(args.mode)
    cfg.pop("_note", None)
    cfg["brand"] = key
    cfg["domain"] = args.domain
    cfg["mode"] = args.mode
    cfg["colors"]["signal"] = kit.hex_of(kit.parse_hex(args.signal))
    for name, raw in (("ground", args.ground), ("ink", args.ink), ("footer", args.footer)):
        if raw is not None:
            cfg["colors"][name] = kit.hex_of(kit.parse_hex(raw))
    cfg["text"]["masthead"] = text_value(args.masthead, args.domain)
    cfg["text"]["website_row"] = text_value(args.website_row, args.domain)
    cfg["text"]["footer_text"] = text_value(args.footer_text, cfg["text"]["footer_text"])
    cfg["text"]["title"] = text_value(args.title, cfg["text"]["title"])

    ratio = kit.contrast(
        kit.parse_hex(cfg["colors"]["signal"]), kit.parse_hex(cfg["colors"]["ground"])
    )

    template_md = (kit.TEMPLATES_DIR / "brand.template.md").read_text()
    brand_md = (
        template_md.replace("__DOMAIN__", args.domain)
        .replace("__MODE__", args.mode)
        .replace("__SIGNAL__", cfg["colors"]["signal"])
        .replace("__GROUND__", cfg["colors"]["ground"])
        .replace("__CONTRAST__", f"{ratio:.2f}")
    )

    target.mkdir(parents=True)
    (target / kit.CONFIG_NAME).write_text(kit.pretty_json(cfg) + "\n")
    (target / kit.BRAND_NAME).write_text(brand_md)

    print(f"{key} -> {target.relative_to(kit.V1_DIR)}/  ({kit.CONFIG_NAME}, {kit.BRAND_NAME})")
    print(f"    signal {cfg['colors']['signal']} on ground {cfg['colors']['ground']}: "
          f"{ratio:.2f}:1")
    if ratio < 3:
        print(
            "    WARNING: below the 3:1 floor for a non-text graphic. "
            "Pick a darker or lighter step before generating."
        )
    print(f"    fill in the placeholders in {target.relative_to(kit.V1_DIR)}/{kit.BRAND_NAME}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", help="brand key, {brand-title}-{variant}, e.g. 11io-dark-orange")
    parser.add_argument("--domain", required=True, help="e.g. www.rj11.io")
    parser.add_argument("--mode", required=True, choices=("dark", "light"))
    parser.add_argument("--signal", required=True, help="hex, e.g. '#F97316'")
    parser.add_argument("--ground", help="hex override; template default otherwise")
    parser.add_argument("--ink", help="hex override")
    parser.add_argument("--footer", help="hex override")
    parser.add_argument("--masthead", help="content-card top line; default domain; `none` omits")
    parser.add_argument("--website-row", help="og-web main row; default domain; `none` omits")
    parser.add_argument("--footer-text", help="keyword line; template default; `none` omits")
    parser.add_argument("--title", help="og-content default title; template default; `none` omits")
    init(parser.parse_args())


if __name__ == "__main__":
    main()
