"""Generate a brand's website Open Graph card.

One 1200 by 630 image: the mark, the domain framed by two signal squares, and
the keyword footer. This is the card a site uses as its own link preview — the
fallback shown when a page has nothing more specific.

It is about the domain, so the domain takes the main row. There is no masthead;
that belongs on a content card, where the main row is already spoken for by a
title.

    python3 generate-website-og.py blog-rj11io
    python3 generate-website-og.py --all
"""

from __future__ import annotations

import argparse

import brandkit as kit


def generate(key: str, stamp: str | None = None) -> None:
    brand = kit.load_brand(key)
    masks = kit.build_masks()
    directory = kit.open_output_dir(brand, "web-og", stamp)

    image, draw = kit.new_card(brand, masks)
    kit.draw_framed_row(draw, brand.domain, brand)
    kit.draw_footer(draw, brand)

    name = f"{brand.key}-web-og.png"
    image.save(directory / name, optimize=True)
    kit.write_manifest(directory, brand, "website OG", [name])

    print(f"{brand.domain} -> {(directory / name).relative_to(kit.V0_DIR)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("brand", nargs="?", help="brand key, e.g. blog-rj11io")
    parser.add_argument("--all", action="store_true", help="every brand")
    parser.add_argument(
        "--stamp",
        help="override the gen-<timestamp> folder name, for reproducible runs",
    )
    args = parser.parse_args()

    if args.all:
        for key in kit.every_brand():
            generate(key, args.stamp)
    elif args.brand:
        generate(args.brand, args.stamp)
    else:
        parser.error("name a brand, or pass --all")


if __name__ == "__main__":
    main()
