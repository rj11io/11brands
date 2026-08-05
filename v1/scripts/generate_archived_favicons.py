"""Generate an ARCHIVED brand's favicon package, in place.

Identical behaviour to generate_favicons.py — same drawing code, same output
location — except it reads archive/ instead of brands/. For revisiting a retired
candidate without promoting it. --all sweeps archived brands only.

    python3 generate_archived_favicons.py 11bench-dark-sky
    python3 generate_archived_favicons.py --all

Output: outputs/<stamp>/<key>/favicons/  (manifest records the archive/ config)
"""

from __future__ import annotations

import argparse

import brandkit as kit
from generate_favicons import generate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?", help="archived brand key")
    parser.add_argument("--all", action="store_true", help="every archived brand")
    parser.add_argument("--run", help="run stamp to join; defaults to now")
    args = parser.parse_args()

    stamp = args.run or kit.new_stamp()
    for key in kit.resolve_keys(args.key, args.all, root="archive"):
        generate(key, stamp, root="archive")


if __name__ == "__main__":
    main()
