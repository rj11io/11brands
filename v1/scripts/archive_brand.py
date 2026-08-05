"""Archive a brand: move brands/<key>/ to archive/<key>/, verbatim.

Nothing inside the folder changes — config.json and brand.md keep their exact
contents, so a promoted brand comes back byte-identical. An archived brand is
invisible to every generator: it cannot be generated, is skipped by --all, and
its key stays reserved so a new brand cannot silently take its place.

    python3 archive_brand.py 11brands-dark-violet
    python3 archive_brand.py --list

Refuses to archive a key that another active brand still builds on (a variant
or sub-brand prefix), unless --force is given.
"""

from __future__ import annotations

import argparse
import shutil

import brandkit as kit


def archive(key: str, force: bool = False) -> None:
    source = kit.BRANDS_DIR / key
    target = kit.ARCHIVE_DIR / key

    if not (source / kit.CONFIG_NAME).exists():
        hint = "It is already archived." if (target / kit.CONFIG_NAME).exists() \
            else "Nothing to archive."
        raise SystemExit(f"no active brand named {key!r}. {hint}")
    if target.exists():
        raise SystemExit(
            f"archive/{key} already exists; refusing to overwrite it. "
            f"Resolve that folder first."
        )

    dependants = [k for k in kit.every_brand() if k != key and k.startswith(f"{key}-")]
    if dependants and not force:
        raise SystemExit(
            f"{key} has active sub-brands or variants: {', '.join(dependants)}. "
            f"They stay generatable either way (each brand is self-contained), "
            f"but archive them first or pass --force if this is intended."
        )

    kit.ARCHIVE_DIR.mkdir(exist_ok=True)
    shutil.move(str(source), str(target))
    print(f"{key}: brands/{key}/ -> archive/{key}/  (contents untouched)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?", help="brand key to archive")
    parser.add_argument("--list", action="store_true", help="show active and archived brands")
    parser.add_argument(
        "--force", action="store_true",
        help="archive even if active brands build on this key's name",
    )
    args = parser.parse_args()

    if args.list:
        print("active:  ", ", ".join(kit.every_brand()) or "(none)")
        print("archived:", ", ".join(kit.every_archived()) or "(none)")
        return
    if not args.key:
        parser.error("name a brand, or pass --list")
    archive(args.key, args.force)


if __name__ == "__main__":
    main()
