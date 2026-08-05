"""Generate content Open Graph cards: one per title.

A content card is the website card with two changes: the main row carries the
piece's title, and the domain moves up above the mark as a masthead. With no
title given, the brand's config `text.title` is used — "Lorem Ipsum" in the
templates — so a bare run produces a complete, obviously-placeholder card.

    python3 generate_og_content.py 11io
    python3 generate_og_content.py 11io --title "Adding a Post"
    python3 generate_og_content.py 11io --titles-file titles.txt
    python3 generate_og_content.py --all

A titles file is one title per line; blank lines and # comments are skipped.
Two titles that slugify identically get numeric suffixes rather than colliding.

Output: outputs/<stamp>/<key>/og-content/<slug>-og-content.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import brandkit as kit


def cli_titles(args) -> list[str]:
    titles = list(args.title or [])
    if args.titles_file:
        path = Path(args.titles_file)
        if not path.exists():
            raise SystemExit(f"no titles file at {path}")
        titles += [
            line.strip()
            for line in path.read_text().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
    return titles


def unique_name(slug: str, taken: set[str]) -> str:
    name = f"{slug}-og-content.png"
    counter = 2
    while name in taken:
        name = f"{slug}-{counter}-og-content.png"
        counter += 1
    taken.add(name)
    return name


def generate(key: str, stamp: str, titles: list[str] | None = None, root: str = "brands") -> None:
    brand = kit.load_brand(key, root)
    titles = titles or [brand.title]
    masks = kit.build_masks()
    directory = kit.output_dir(brand, "og-content", stamp)

    taken: set[str] = set()
    written: list[str] = []
    for title in titles:
        image, draw = kit.new_card(brand, masks)
        kit.draw_masthead(draw, brand)
        kit.draw_framed_row(draw, brand, title)
        kit.draw_footer(draw, brand)

        name = unique_name(kit.slugify(title), taken)
        image.save(directory / name, optimize=True)
        written.append(f"{name} — {title or '(no title row)'}")

    kit.write_manifest(directory, brand, "content OG", written)
    print(f"{brand.domain} -> {directory.relative_to(kit.V1_DIR)}  ({len(written)} cards)")
    for line in written:
        print(f"    {line}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?", help="brand key, e.g. 11io")
    parser.add_argument("--all", action="store_true", help="every registered brand")
    parser.add_argument("--title", action="append", help="a title; repeat for more")
    parser.add_argument("--titles-file", help="one title per line")
    parser.add_argument("--run", help="run stamp to join; defaults to now")
    args = parser.parse_args()

    stamp = args.run or kit.new_stamp()
    titles = cli_titles(args)
    for key in kit.resolve_keys(args.key, args.all):
        generate(key, stamp, titles)


if __name__ == "__main__":
    main()
