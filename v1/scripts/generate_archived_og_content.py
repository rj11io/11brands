"""Generate an ARCHIVED brand's content OG cards, in place.

Identical behaviour to generate_og_content.py except it reads archive/ instead
of brands/. With no title, the archived config's text.title is used. --all
sweeps archived brands only.

    python3 generate_archived_og_content.py 11bench-dark-sky
    python3 generate_archived_og_content.py 11bench-dark-sky --title "A Post"
    python3 generate_archived_og_content.py --all --titles-file titles.txt

Output: outputs/<stamp>/<key>/og-content/  (manifest records the archive/ config)
"""

from __future__ import annotations

import argparse

import brandkit as kit
from generate_og_content import cli_titles, generate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?", help="archived brand key")
    parser.add_argument("--all", action="store_true", help="every archived brand")
    parser.add_argument("--title", action="append", help="a title; repeat for more")
    parser.add_argument("--titles-file", help="one title per line")
    parser.add_argument("--run", help="run stamp to join; defaults to now")
    args = parser.parse_args()

    stamp = args.run or kit.new_stamp()
    titles = cli_titles(args)
    for key in kit.resolve_keys(args.key, args.all, root="archive"):
        generate(key, stamp, titles, root="archive")


if __name__ == "__main__":
    main()
