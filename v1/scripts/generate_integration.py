"""Generate assets for a consuming project, into integrations/.

The entry point another repository's agent runs. Same drawing code and run
shape as the ordinary generators, with two differences: output lands in
integrations/<stamp>/<key>/<kind>/ instead of outputs/, and every manifest
records the --source — the project that asked.

The intended flow for the caller: run this, read the printed stamp, copy what
you need out of integrations/<stamp>/<key>/, leave the run behind. It is the
record on the 11brands side; never delete or tidy it.

    python3 generate_integration.py 11blog --source 11blog-site
    python3 generate_integration.py 11blog --source 11blog-site --kind og-content --title "A Post"
    python3 generate_integration.py 11bench --source bench-app --kind favicons --kind og-web

Default is the full pack; --kind (repeatable) narrows it. Active brands only —
archived brands are operator territory.

Stamp policy: an explicit --run is honoured verbatim (an existing folder is
joined, exactly like outputs/). The default tries {datetime}; on collision
{datetime}-{source}; if that also exists, it is joined.
"""

from __future__ import annotations

import argparse
import re

import brandkit as kit
import generate_favicons
import generate_og_content
import generate_og_web

SOURCE_SHAPE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def integration_stamp(explicit: str | None, source: str) -> str:
    """{datetime}, on collision {datetime}-{source}, on collision join."""
    if explicit:
        return explicit
    stamp = kit.new_stamp()
    if not (kit.INTEGRATIONS_DIR / stamp).exists():
        return stamp
    return f"{stamp}-{source}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", help="brand key, e.g. 11blog")
    parser.add_argument(
        "--source", required=True,
        help="the consuming project triggering this run, e.g. 11blog-site",
    )
    parser.add_argument(
        "--kind", action="append", choices=list(kit.KINDS),
        help="limit to a kind; repeat for several (default: all three)",
    )
    parser.add_argument("--title", action="append", help="content title; repeat for more")
    parser.add_argument("--titles-file", help="one content title per line")
    parser.add_argument("--run", help="run stamp to join; defaults per the stamp policy")
    args = parser.parse_args()

    if not SOURCE_SHAPE.match(args.source):
        raise SystemExit(
            f"source {args.source!r} should be a simple project name "
            f"(lowercase letters, digits, . _ -), e.g. 11blog-site"
        )

    stamp = integration_stamp(args.run, args.source)
    kinds = args.kind or list(kit.KINDS)
    titles = generate_og_content.cli_titles(args)
    base = kit.INTEGRATIONS_DIR

    print(f"integration run {stamp} for {args.source}: {args.key} ({', '.join(kinds)})")
    if "favicons" in kinds:
        generate_favicons.generate(args.key, stamp, base=base, source=args.source)
    if "og-web" in kinds:
        generate_og_web.generate(args.key, stamp, base=base, source=args.source)
    if "og-content" in kinds:
        generate_og_content.generate(args.key, stamp, titles, base=base, source=args.source)
    print(f"done -> integrations/{stamp}/{args.key}/  (copy what you need; leave the run)")


if __name__ == "__main__":
    main()
