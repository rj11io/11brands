"""Create or refresh a brand's config.json.

config.json is the machine-readable, fully resolved list of every variable used to
generate a brand's assets: its colours, all four text fields, the whole layout,
the icon sizes, and the font. brand.md holds the same colours and text, but it has
no syntax for a layout number and it is where the reasoning lives, so the two are
kept side by side and config.json wins at generation time.

That is what makes it useful: change a value, re-run a generator, look at the
result. Nothing else needs editing.

    python3 generate-config.py b2b-rj11io          # create if missing
    python3 generate-config.py --all               # every registered brand
    python3 generate-config.py --all --drafts      # and every draft
    python3 generate-config.py b2b-rj11io --refresh

By default an existing config.json is left alone, because it may hold hand-edited
layout values that brand.md cannot express and a rewrite would silently discard
them. `--refresh` is the explicit way to say "throw those away and rebuild from
brand.md".
"""

from __future__ import annotations

import argparse

import brandkit as kit


def report(brand: kit.Brand, action: str) -> None:
    where = brand.source.parent.relative_to(kit.V0_DIR)
    print(f"{action:<9} {where}/{kit.CONFIG_NAME}")


def process(key: str, root: str, refresh: bool) -> None:
    # Read brand.md alone when refreshing, so the rebuild comes from the record
    # rather than from the file being replaced.
    brand = kit.load_brand(key, prefer=root, use_config=not refresh, quiet=True)
    existing = brand.source.parent / kit.CONFIG_NAME

    if existing.exists() and not refresh:
        report(brand, "kept")
        return

    action = "refreshed" if existing.exists() else "wrote"
    kit.write_config(brand)
    report(brand, action)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("brand", nargs="?", help="brand key, e.g. b2b-rj11io")
    parser.add_argument(
        "--all",
        action="store_true",
        help="every brand registered in brands/",
    )
    parser.add_argument(
        "--drafts",
        action="store_true",
        help="with --all, also cover every draft in drafts/",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="rebuild an existing config.json from brand.md, discarding hand edits",
    )
    args = parser.parse_args()

    if args.all:
        for key in kit.every_brand():
            process(key, "brands", args.refresh)
        if args.drafts:
            for key in kit.every_draft():
                process(key, "drafts", args.refresh)
    elif args.brand:
        root = "drafts" if args.brand in kit.every_draft() else "brands"
        process(args.brand, root, args.refresh)
    else:
        parser.error("name a brand, or pass --all")


if __name__ == "__main__":
    main()
