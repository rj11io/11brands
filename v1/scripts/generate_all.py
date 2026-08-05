"""Generate a brand's full asset pack: favicons, website OG, content OG.

Mints one run stamp and passes it to each generator, so the whole batch —
one brand or all of them — lands under a single outputs/<stamp>/ folder.

    python3 generate_all.py 11io
    python3 generate_all.py --all
    python3 generate_all.py --all --run 20260805-120000
    python3 generate_all.py 11io --title "Adding a Post"

Titles are passed through to the content generator; with none, each brand's
config `text.title` is used.
"""

from __future__ import annotations

import argparse

import brandkit as kit
import generate_favicons
import generate_og_content
import generate_og_web


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?", help="brand key, e.g. 11io")
    parser.add_argument("--all", action="store_true", help="every registered brand")
    parser.add_argument("--title", action="append", help="content title; repeat for more")
    parser.add_argument("--titles-file", help="one content title per line")
    parser.add_argument("--run", help="run stamp to join; defaults to now")
    args = parser.parse_args()

    stamp = args.run or kit.new_stamp()
    titles = generate_og_content.cli_titles(args)
    keys = kit.resolve_keys(args.key, args.all)

    print(f"run {stamp}: {len(keys)} brand(s)")
    for key in keys:
        generate_favicons.generate(key, stamp)
        generate_og_web.generate(key, stamp)
        generate_og_content.generate(key, stamp, titles)
    print(f"done -> outputs/{stamp}/")


if __name__ == "__main__":
    main()
