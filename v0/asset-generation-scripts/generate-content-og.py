"""Generate content Open Graph cards: one per title.

A content card is the website card with two changes. The main row carries the
piece's title instead of the domain, and the domain moves up above the mark as a
masthead — because a card about a post still has to say where the post lives,
and the row it used to occupy is taken.

The masthead sits 48 pixels below the top edge and the footer 49 above the
bottom, so the two read as a matched pair framing the card rather than one line
hugging an edge.

    python3 generate-content-og.py blog-rj11io --title "Adding a publication or post"
    python3 generate-content-og.py blog-rj11io --titles-file titles.txt
    python3 generate-content-og.py --all --titles-file titles.txt

A titles file is one title per line; blank lines and lines starting with # are
skipped. Output names come from the title, so two titles that slugify the same
would collide — the second gets a numeric suffix rather than overwriting.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import brandkit as kit


def read_titles(args) -> list[str]:
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
    if not titles:
        raise SystemExit("give at least one --title, or a --titles-file")
    return titles


def unique_name(slug: str, taken: set[str]) -> str:
    name = f"{slug}-content-og.png"
    counter = 2
    while name in taken:
        name = f"{slug}-{counter}-content-og.png"
        counter += 1
    taken.add(name)
    return name


def generate(key: str, titles: list[str], stamp: str | None = None) -> None:
    brand = kit.load_brand(key)
    masks = kit.build_masks()
    directory = kit.open_output_dir(brand, "content-og", stamp)

    taken: set[str] = set()
    written: list[str] = []

    for title in titles:
        image, draw = kit.new_card(brand, masks)
        kit.draw_tracked(
            draw,
            brand.domain,
            kit.CARD[0] / 2,
            kit.MASTHEAD_MIDDLE,
            kit.MASTHEAD_PT,
            brand.footer,
            kit.MASTHEAD_TRACKING,
        )
        kit.draw_framed_row(draw, title, brand)
        kit.draw_footer(draw, brand)

        name = unique_name(kit.slugify(title), taken)
        image.save(directory / name, optimize=True)
        written.append(f"{name} — {title}")

    kit.write_manifest(directory, brand, "content OG", written)
    print(f"{brand.domain} -> {directory.relative_to(kit.V0_DIR)}  ({len(written)} cards)")
    for line in written:
        print(f"    {line}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("brand", nargs="?", help="brand key, e.g. blog-rj11io")
    parser.add_argument("--all", action="store_true", help="every brand")
    parser.add_argument(
        "--title", action="append", help="a title; repeat for more than one"
    )
    parser.add_argument("--titles-file", help="one title per line")
    parser.add_argument(
        "--stamp",
        help="override the gen-<timestamp> folder name, for reproducible runs",
    )
    args = parser.parse_args()

    titles = read_titles(args)
    if args.all:
        for key in kit.every_brand():
            generate(key, titles, args.stamp)
    elif args.brand:
        generate(args.brand, titles, args.stamp)
    else:
        parser.error("name a brand, or pass --all")


if __name__ == "__main__":
    main()
