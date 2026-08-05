"""Generate a brand's favicon package.

Five PNGs and a six-frame favicon.ico by default (the exact set comes from the
brand's config). Every frame is RGBA and composed at its own size — see
write_icon_set in brandkit.py for why both rules exist.

    python3 generate_favicons.py 11io-dark-orange
    python3 generate_favicons.py --all
    python3 generate_favicons.py 11io-dark-orange --run 20260805-120000

Output: outputs/<stamp>/<key>/favicons/
"""

from __future__ import annotations

import argparse

import brandkit as kit


def generate(key: str, stamp: str) -> None:
    brand = kit.load_brand(key)
    masks = kit.build_masks()
    directory = kit.output_dir(brand, "favicons", stamp)

    written = kit.write_icon_set(masks, brand, directory)
    kit.write_manifest(directory, brand, "favicons", [p.name for p in written])

    print(f"{brand.domain} -> {directory.relative_to(kit.V1_DIR)}  ({len(written)} files)")


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
