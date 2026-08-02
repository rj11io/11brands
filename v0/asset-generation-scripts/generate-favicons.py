"""Generate a brand's favicon package.

Six files: 16, 32, 180 (Apple touch), 192 and 512 pixel PNGs, plus a favicon.ico
carrying six frames. Everything is RGBA and every size is composed at that size
rather than shrunk from a bigger one — see write_icon_set in brandkit.py for why
both of those matter.

    python3 generate-favicons.py blog-rj11io
    python3 generate-favicons.py --all
"""

from __future__ import annotations

import argparse

import brandkit as kit


def generate(key: str, stamp: str | None = None) -> None:
    brand = kit.load_brand(key)
    masks = kit.build_masks()
    directory = kit.open_output_dir(brand, "favicons", stamp)

    written = kit.write_icon_set(masks, brand, directory)
    kit.write_manifest(
        directory, brand, "favicons", [path.name for path in written]
    )

    print(f"{brand.domain} -> {directory.relative_to(kit.V0_DIR)}")
    for path in written:
        print(f"    {path.name}")


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
