"""Verify the 14 registered DataSTORRE members; optionally stage exact bytes."""

import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", type=Path, help="directory with RUE.zip, NETGEN.zip and MORPH.zip")
    parser.add_argument("--stage", type=Path, help="create a NEW private input directory after verification")
    args = parser.parse_args()
    if args.stage and args.stage.exists():
        parser.error("stage directory already exists")
    manifest = Path(__file__).with_name("stirling_14.csv")
    with manifest.open(encoding="utf-8-sig", newline="") as stream:
        listings = list(csv.DictReader(stream))
    if len(listings) != 14 or len({(r["batch"], r["map_id"]) for r in listings}) != 14:
        raise ValueError("unexpected manifest")

    checked = []
    content = {}
    for archive in ("RUE.zip", "NETGEN.zip", "MORPH.zip"):
        path = args.archives / archive
        digest = sha256(path.read_bytes()).hexdigest()
        members = [r for r in listings if r["archive"] == archive]
        with ZipFile(path) as zf:
            names = zf.namelist()
            for row in members:
                if digest != row["archive_sha256"] or names.count(row["source_member"]) != 1:
                    raise ValueError(f"archive version or member mismatch for {row['map_id']}")
                raw = zf.read(row["source_member"])
                if sha256(raw).hexdigest() != row["member_sha256"]:
                    raise ValueError(f"instance bytes differ for {row['map_id']}")
                if row["batch"] not in ("V22", "R4") or not all(
                    c.isascii() and (c.isalnum() or c == "-") for c in row["map_id"]
                ):
                    raise ValueError("invalid logical instance path")
                content[Path(row["batch"]) / (row["map_id"] + ".tsp")] = raw
                checked.append(row["map_id"])
    if len(content) != 14:
        raise ValueError("missing one or more registered members")
    if args.stage:
        args.stage.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=args.stage.parent) as scratch:
            tree = Path(scratch) / "maps"
            for name, raw in content.items():
                dest = tree / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(raw)
            if args.stage.exists():
                raise FileExistsError(args.stage)
            tree.rename(args.stage)
    print(json.dumps({"matched": len(content), "map_ids": checked, "private_staging_requested": bool(args.stage)}))


if __name__ == "__main__":
    main()
