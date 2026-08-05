"""Generate a brand's website Open Graph card.

One card: the mark, the website row (the domain, unless the config says
otherwise) framed by two signal squares, and the keyword footer. The link
preview a site falls back to when a page has nothing more specific.

    python3 generate_og_web.py 11io-dark-orange
    python3 generate_og_web.py --all
    python3 generate_og_web.py 11io-dark-orange --run 20260805-120000

Output: outputs/<stamp>/<key>/og-web/<key>-og-web.png
"""

from __future__ import annotations

import argparse

import brandkit as kit


def generate(key: str, stamp: str) -> None:
    brand = kit.load_brand(key)
    masks = kit.build_masks()
    directory = kit.output_dir(brand, "og-web", stamp)

    image, draw = kit.new_card(brand, masks)
    kit.draw_framed_row(draw, brand, brand.website_row)
    kit.draw_footer(draw, brand)

    name = f"{brand.key}-og-web.png"
    image.save(directory / name, optimize=True)
    kit.write_manifest(directory, brand, "website OG", [name])

    print(f"{brand.domain} -> {(directory / name).relative_to(kit.V1_DIR)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?", help="brand key, e.g. 11io-dark-orange")
    parser.add_argument("--all", action="store_true", help="every registered brand")
    parser.add_argument("--run", help="run stamp to join; defaults to now")
    args = parser.parse_args()

    stamp = args.run or kit.new_stamp()
    for key in kit.resolve_keys(args.key, args.all):
        generate(key, stamp)


if __name__ == "__main__":
    main()
