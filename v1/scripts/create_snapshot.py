"""Create a snapshot: a full, immutable, point-in-time capture of the system.

One snapshot folder holds a freshly generated full pack for every active brand
and every archived brand, a verbatim copy of the integrations/ workspace as it
stands, and a machine-readable index:

    snapshots/<stamp>/
    ├── SNAPSHOT.json     the index: every brand's palette, text, files
    ├── brands/<key>/{favicons,og-web,og-content}/
    ├── archive/<key>/{favicons,og-web,og-content}/
    └── integrations/<run>/<key>/<kind>/     (absent if integrations/ is empty)

A snapshot is a record, not a workspace: it is never edited, never regenerated
in place, and never joined — an existing stamp is refused. Prune old snapshots
by age when they pile up. The www explorer reads SNAPSHOT.json and streams the
files.

    python3 create_snapshot.py
    python3 create_snapshot.py --run 20260805-golden
"""

from __future__ import annotations

import argparse
import json
import re
import shutil

import brandkit as kit
import generate_favicons
import generate_og_content
import generate_og_web

SOURCE_ROW = re.compile(r"^\| Source \| (.+) \|$", re.M)


def brand_entry(key: str, root: str) -> dict:
    b = kit.load_brand(key, root)
    return {
        "key": key,
        "domain": b.domain,
        "mode": b.mode,
        "colors": {
            "signal": kit.hex_of(b.signal),
            "ground": kit.hex_of(b.ground),
            "ink": kit.hex_of(b.ink),
            "footer": kit.hex_of(b.footer),
        },
        "contrast": round(kit.contrast(b.signal, b.ground), 2),
        "text": {
            "masthead": b.masthead or None,
            "website_row": b.website_row or None,
            "footer_text": b.footer_text or None,
            "title": b.title or None,
        },
    }


def file_index(section_dir) -> dict:
    """{key: {kind: [files]}} for one generated section folder."""
    out = {}
    for key_dir in sorted(p for p in section_dir.iterdir() if p.is_dir()):
        kinds = {}
        for kind_dir in sorted(p for p in key_dir.iterdir() if p.is_dir()):
            kinds[kind_dir.name] = sorted(
                p.name for p in kind_dir.iterdir() if p.name != "MANIFEST.md"
            )
        out[key_dir.name] = kinds
    return out


def integration_index(dest) -> list[dict]:
    """One entry per copied integration run, with its sources from manifests."""
    runs = []
    for run_dir in sorted(p for p in dest.iterdir() if p.is_dir()):
        keys, sources = [], set()
        for key_dir in sorted(p for p in run_dir.iterdir() if p.is_dir()):
            keys.append(key_dir.name)
            for manifest in key_dir.glob("*/MANIFEST.md"):
                match = SOURCE_ROW.search(manifest.read_text())
                if match:
                    sources.add(match.group(1))
        runs.append({"run": run_dir.name, "keys": keys, "sources": sorted(sources)})
    return runs


def create(stamp: str) -> None:
    snap = kit.SNAPSHOTS_DIR / stamp
    if snap.exists():
        raise SystemExit(
            f"snapshots/{stamp} already exists. A snapshot is immutable — pick a "
            f"new stamp rather than adding to an old capture."
        )

    sections = {"brands": kit.every_brand(), "archive": kit.every_archived()}
    index = {
        "stamp": stamp,
        "created": kit.datetime.now().isoformat(timespec="seconds"),
        "sections": {},
    }

    for section, keys in sections.items():
        root = "brands" if section == "brands" else "archive"
        for key in keys:
            generate_favicons.generate(key, f"{stamp}/{section}", root=root, base=kit.SNAPSHOTS_DIR)
            generate_og_web.generate(key, f"{stamp}/{section}", root=root, base=kit.SNAPSHOTS_DIR)
            generate_og_content.generate(key, f"{stamp}/{section}", None, root=root, base=kit.SNAPSHOTS_DIR)
        section_dir = snap / section
        files = file_index(section_dir) if section_dir.exists() else {}
        index["sections"][section] = {
            "brands": [dict(brand_entry(k, root), files=files.get(k, {})) for k in keys],
        }

    copied_runs = 0
    if kit.INTEGRATIONS_DIR.exists() and any(kit.INTEGRATIONS_DIR.iterdir()):
        dest = snap / "integrations"
        shutil.copytree(kit.INTEGRATIONS_DIR, dest)
        runs = integration_index(dest)
        copied_runs = len(runs)
        index["sections"]["integrations"] = {"runs": runs}

    (snap / "SNAPSHOT.json").write_text(kit.pretty_json(index) + "\n")

    print(
        f"snapshot {stamp}: {len(sections['brands'])} active, "
        f"{len(sections['archive'])} archived, {copied_runs} integration run(s) copied"
    )
    print(f"  -> snapshots/{stamp}/  (SNAPSHOT.json indexes it)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", help="snapshot stamp; defaults to now. Never joins.")
    args = parser.parse_args()
    create(args.run or kit.new_stamp())


if __name__ == "__main__":
    main()
