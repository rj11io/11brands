"""Generate a brand's website Open Graph card.

One 1200 by 630 image: the mark, a framed main row, and the keyword footer. This
is the card a site uses as its own link preview — the fallback shown when a page
has nothing more specific.

The card is about the domain, so the main row carries the domain by default. A
brand can put something else there with **Website row:** in its brand.md. There
is no masthead; that belongs on a content card, where the main row is already
spoken for by a title.

Output goes to drafts/ unless --into brands is given. Values come from the
brand's config.json when it has one, and a missing one is created on first run.

    python3 generate-website-og.py b2b-rj11io
    python3 generate-website-og.py --all
    python3 generate-website-og.py b2b-rj11io --into brands
"""

from __future__ import annotations

import argparse

import brandkit as kit


def generate(key: str, stamp: str | None = None, into: str = kit.DEFAULT_OUTPUT) -> None:
    brand = kit.load_brand(key, prefer=into)
    kit.ensure_config(brand)
    masks = kit.build_masks()
    directory = kit.open_output_dir(brand, "web-og", stamp, into)

    image, draw = kit.new_card(brand, masks)
    kit.draw_framed_row(draw, brand.website_row, brand)
    kit.draw_footer(draw, brand)

    name = f"{brand.key}-web-og.png"
    image.save(directory / name, optimize=True)
    kit.write_manifest(directory, brand, "website OG", [name])

    print(
        f"{brand.domain} -> {(directory / name).relative_to(kit.V0_DIR)}"
        f"  (from {brand.source.relative_to(kit.V0_DIR)})"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("brand", nargs="?", help="brand key, e.g. b2b-rj11io")
    parser.add_argument(
        "--all",
        action="store_true",
        help="every brand registered in brands/ (drafts are named explicitly)",
    )
    parser.add_argument(
        "--into",
        choices=sorted(kit.OUTPUT_ROOTS),
        default=kit.DEFAULT_OUTPUT,
        help="output root (default: %(default)s)",
    )
    parser.add_argument(
        "--stamp",
        help="override the gen-<timestamp> folder name, for reproducible runs",
    )
    args = parser.parse_args()

    if args.all:
        for key in kit.every_brand():
            generate(key, args.stamp, args.into)
    elif args.brand:
        generate(args.brand, args.stamp, args.into)
    else:
        parser.error("name a brand, or pass --all")


if __name__ == "__main__":
    main()
