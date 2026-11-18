"""Run the pinned historical verifier or statistics scripts on authorized inputs."""

import argparse
import csv
from hashlib import sha256
from pathlib import Path
import subprocess
import sys


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("mode", choices=("stats", "routes"))
    cli.add_argument("package", type=Path, help="root containing the authorized scripts/ and data/")
    cli.add_argument("output", type=Path, help="new output directory, outside the source package")
    cli.add_argument("--external-maps", type=Path, help="verified external V22/ and R4/ map directories")
    cli.add_argument("--partial", action="store_true", help="routes only; classify missing inputs explicitly")
    args = cli.parse_args()
    source, out = args.package.resolve(), args.output.resolve()
    if source == out or source in out.parents or out.exists():
        cli.error("use a new output directory outside the input package")
    if args.mode == "stats" and (args.external_maps or args.partial):
        cli.error("external maps and partial verification apply only to routes")
    with Path(__file__).with_name("replay_inputs.csv").open(encoding="utf-8-sig", newline="") as f:
        inputs = [row for row in csv.DictReader(f) if row["mode"] == args.mode]
    verified = {}
    for row in inputs:
        rel = Path(row["file"])
        data = (source / rel).read_bytes()
        digest = sha256(data).hexdigest()
        if digest not in {row["frozen_working_sha256"], row["published_blob_sha256"]}:
            raise ValueError(f"unrecognized frozen input: {rel}")
        verified[rel] = data
    out.mkdir(parents=True, exist_ok=False)
    if args.mode == "routes":
        # Running the verifier at its original location preserves its registered route root.
        command = [sys.executable, "-B", "-X", "utf8", str(source / "scripts/verify_tsp_routes.py"),
                   "--output", str(out / "route_verification.json")]
        if args.external_maps:
            for batch in ("V22", "R4"):
                command.extend(["--external-" + batch.lower(), str((args.external_maps / batch).resolve())])
        if args.partial:
            command.append("--allow-missing")
    else:
        # The historical plotting script chooses output relative to itself. Keep the source untouched.
        for rel, data in verified.items():
            dest = out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        command = [sys.executable, "-B", "-X", "utf8", str(out / "scripts/run_all.py")]
    return subprocess.run(command, cwd=out).returncode


if __name__ == "__main__":
    sys.exit(main())
