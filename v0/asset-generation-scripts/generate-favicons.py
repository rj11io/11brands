"""Generate a brand's favicon package.

Six files: 16, 32, 180 (Apple touch), 192 and 512 pixel PNGs, plus a favicon.ico
carrying six frames. Everything is RGBA and every size is composed at that size
rather than shrunk from a bigger one — see write_icon_set in brandkit.py for why
both of those matter.

Output goes to drafts/ unless --into brands is given. Values come from the
brand's config.json when it has one, and a missing one is created on first run. Promoting a draft is a
separate step; see skills/11brands-v0-promote-draft/.

    python3 generate-favicons.py b2b-rj11io
    python3 generate-favicons.py --all
    python3 generate-favicons.py b2b-rj11io --into brands
"""

from __future__ import annotations

import argparse

import brandkit as kit


def generate(key: str, stamp: str | None = None, into: str = kit.DEFAULT_OUTPUT) -> None:
    brand = kit.load_brand(key, prefer=into)
    kit.ensure_config(brand)
    masks = kit.build_masks()
    directory = kit.open_output_dir(brand, "favicons", stamp, into)

    written = kit.write_icon_set(masks, brand, directory)
    kit.write_manifest(
        directory, brand, "favicons", [path.name for path in written]
    )

    print(
        f"{brand.domain} -> {directory.relative_to(kit.V0_DIR)}"
        f"  (from {brand.source.relative_to(kit.V0_DIR)})"
    )
    for path in written:
        print(f"    {path.name}")


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
