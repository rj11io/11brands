"""Promote an archived brand: move archive/<key>/ back to brands/<key>/, verbatim.

The exact inverse of archive_brand.py. Nothing inside the folder changes, so the
brand generates exactly what it generated before it was archived.

    python3 promote_brand.py 11brands-dark-violet
    python3 promote_brand.py --list
"""

from __future__ import annotations

import argparse
import shutil

import brandkit as kit


def promote(key: str) -> None:
    source = kit.ARCHIVE_DIR / key
    target = kit.BRANDS_DIR / key

    if not (source / kit.CONFIG_NAME).exists():
        hint = "It is already active." if (target / kit.CONFIG_NAME).exists() \
            else "Nothing to promote."
        raise SystemExit(f"no archived brand named {key!r}. {hint}")
    if target.exists():
        raise SystemExit(
            f"brands/{key} already exists; refusing to overwrite it. An active "
            f"brand and an archived one share a key — resolve that first."
        )

    shutil.move(str(source), str(target))
    print(f"{key}: archive/{key}/ -> brands/{key}/  (contents untouched)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("key", nargs="?", help="brand key to promote")
    parser.add_argument("--list", action="store_true", help="show active and archived brands")
    args = parser.parse_args()

    if args.list:
        print("active:  ", ", ".join(kit.every_brand()) or "(none)")
        print("archived:", ", ".join(kit.every_archived()) or "(none)")
        return
    if not args.key:
        parser.error("name a brand, or pass --list")
    promote(args.key)


if __name__ == "__main__":
    main()
