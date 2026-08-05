"""Generate an ARCHIVED brand's full asset pack, in place.

Identical behaviour to generate_all.py except it reads archive/ instead of
brands/: one run stamp, favicons + og-web + og-content per brand. --all sweeps
archived brands only; active brands are never touched.

    python3 generate_archived_all.py 11bench-dark-sky
    python3 generate_archived_all.py --all
    python3 generate_archived_all.py 11brands-dark-violet --title "A Post"
"""

from __future__ import annotations

import argparse

import brandkit as kit
import generate_favicons
import generate_og_content
import generate_og_web


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?", help="archived brand key")
    parser.add_argument("--all", action="store_true", help="every archived brand")
    parser.add_argument("--title", action="append", help="content title; repeat for more")
    parser.add_argument("--titles-file", help="one content title per line")
    parser.add_argument("--run", help="run stamp to join; defaults to now")
    args = parser.parse_args()

    stamp = args.run or kit.new_stamp()
    titles = generate_og_content.cli_titles(args)
    keys = kit.resolve_keys(args.key, args.all, root="archive")

    print(f"run {stamp}: {len(keys)} archived brand(s)")
    for key in keys:
        generate_favicons.generate(key, stamp, root="archive")
        generate_og_web.generate(key, stamp, root="archive")
        generate_og_content.generate(key, stamp, titles, root="archive")
    print(f"done -> outputs/{stamp}/")


if __name__ == "__main__":
    main()
