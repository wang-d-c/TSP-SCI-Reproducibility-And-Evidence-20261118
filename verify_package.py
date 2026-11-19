"""Verify the exact bytes listed in the public package manifest."""
import csv
import hashlib
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
RECOVERY = (
    "Extract a fresh copy of the public ZIP, or make a fresh Git clone containing "
    ".gitattributes. Recheck before analyzing the data."
)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def line_ending_change(data, expected):
    lf = data.replace(b"\r\n", b"\n")
    crlf = lf.replace(b"\n", b"\r\n")
    return (lf != data and sha256(lf) == expected) or (crlf != data and sha256(crlf) == expected)


def verify_file(path, expected, size=None):
    """Return a readable error or None. Checks and diagnostics leave input bytes intact."""
    try:
        data = (ROOT / path).read_bytes()
    except OSError:
        return f"{path}: could not read the expected package file."
    if sha256(data) != expected:
        if line_ending_change(data, expected):
            return f"{path}: line endings changed during transfer, such as by Git autocrlf."
        return f"{path}: SHA256 does not match the registered file."
    if size is not None and len(data) != size:
        return f"{path}: byte count does not match the manifest."
    return None


def manifest():
    with (ROOT / "FILE_SHA256.csv").open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["file", "bytes", "sha256"]:
            raise ValueError("unexpected FILE_SHA256.csv columns")
        seen = set()
        for row in reader:
            name = row["file"]
            path = PurePosixPath(name)
            if (name != path.as_posix() or name in ("FILE_SHA256.csv", ".")
                or path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name
                or name in seen or not (ROOT / path).resolve().is_relative_to(ROOT)):
                raise ValueError(f"invalid or duplicate manifest path {name!r}")
            size = int(row["bytes"])
            expected = row["sha256"]
            if size < 0 or not re.fullmatch(r"[0-9a-f]{64}", expected):
                raise ValueError(f"invalid byte count or SHA256 for {name}")
            seen.add(name)
            yield name, expected, size


def main():
    try:
        rows = list(manifest())
        if not rows:
            raise ValueError("empty FILE_SHA256.csv")
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise SystemExit(f"Cannot read the package manifest: {error}\n{RECOVERY}") from None
    failures = [error for name, expected, size in rows if (error := verify_file(name, expected, size))]
    if failures:
        raise SystemExit("\n".join(failures + [RECOVERY]))
    print(f"Verified exact bytes and SHA256 for all {len(rows)} files listed in FILE_SHA256.csv.")


if __name__ == "__main__":
    main()
