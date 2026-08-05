"""Generate content Open Graph cards: one per title.

A content card is the website card with two changes. The main row carries the
piece's title instead of the domain, and the domain moves up above the mark as a
masthead — because a card about a post still has to say where the post lives, and
the row it used to occupy is taken. A brand can override that masthead line with
**Masthead:** in its brand.md.

The masthead sits 48 pixels below the top edge and the footer 49 above the
bottom, so the two read as a matched pair framing the card rather than one line
hugging an edge.

With no title given, the brand's **Default title:** is used, which is
"Lorem Ipsum" unless the brand says otherwise. That makes a bare run produce a
complete, obviously-placeholder set — useful when what is being reviewed is the
brand rather than the words.

Output goes to drafts/ unless --into brands is given. Values come from the
brand's config.json when it has one, and a missing one is created on first run.

    python3 generate-content-og.py b2b-rj11io
    python3 generate-content-og.py b2b-rj11io --title "Adding a publication or post"
    python3 generate-content-og.py b2b-rj11io --titles-file titles.txt
    python3 generate-content-og.py --all

A titles file is one title per line; blank lines and lines starting with # are
skipped. Output names come from the title, so two titles that slugify the same
would collide — the second gets a numeric suffix rather than overwriting.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import brandkit as kit


def explicit_titles(args) -> list[str]:
    """Titles named on the command line. May be empty, in which case the brand's
    own default is used instead — resolved per brand, so --all respects each."""
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
    name = f"{slug}-content-og.png"
    counter = 2
    while name in taken:
        name = f"{slug}-{counter}-content-og.png"
        counter += 1
    taken.add(name)
    return name


def generate(
    key: str,
    titles: list[str],
    stamp: str | None = None,
    into: str = kit.DEFAULT_OUTPUT,
) -> None:
    brand = kit.load_brand(key, prefer=into)
    kit.ensure_config(brand)
    used_default = not titles
    titles = titles or [brand.default_title]

    masks = kit.build_masks()
    directory = kit.open_output_dir(brand, "content-og", stamp, into)

    taken: set[str] = set()
    written: list[str] = []

    for title in titles:
        image, draw = kit.new_card(brand, masks)
        kit.draw_masthead(draw, brand)
        kit.draw_framed_row(draw, title, brand)
        kit.draw_footer(draw, brand)

        name = unique_name(kit.slugify(title), taken)
        image.save(directory / name, optimize=True)
        written.append(f"{name} — {title or '(no title row)'}")

    kit.write_manifest(directory, brand, "content OG", written)
    note = "  (brand default title)" if used_default else ""
    print(
        f"{brand.domain} -> {directory.relative_to(kit.V0_DIR)}"
        f"  ({len(written)} cards){note}"
    )
    print(f"    from {brand.source.relative_to(kit.V0_DIR)}")
    for line in written:
        print(f"    {line}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("brand", nargs="?", help="brand key, e.g. b2b-rj11io")
    parser.add_argument(
        "--all",
        action="store_true",
        help="every brand registered in brands/ (drafts are named explicitly)",
    )
    parser.add_argument(
        "--title", action="append", help="a title; repeat for more than one"
    )
    parser.add_argument("--titles-file", help="one title per line")
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

    titles = explicit_titles(args)
    if args.all:
        for key in kit.every_brand():
            generate(key, titles, args.stamp, args.into)
    elif args.brand:
        generate(args.brand, titles, args.stamp, args.into)
    else:
        parser.error("name a brand, or pass --all")


if __name__ == "__main__":
    main()
