#!/usr/bin/env python3
"""Verify MANIFEST_SHA256SUMS.txt with the Python standard library."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

LINE_RE = re.compile(r"^([0-9a-fA-F]{64})\s{2}(.+?)\s*$")
IGNORED_PARTS = {"__pycache__", ".pytest_cache"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="also fail when a file under the skill root is not listed in the manifest",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = root / "MANIFEST_SHA256SUMS.txt"
    if not manifest.is_file():
        print(f"FAIL: missing manifest: {manifest}")
        return 2

    errors: list[str] = []
    entries: dict[str, str] = {}
    for number, raw in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        match = LINE_RE.match(line)
        if not match:
            errors.append(f"line {number}: malformed manifest entry: {raw!r}")
            continue
        expected, relative = match.groups()
        entries[relative] = expected.lower()

    if len(entries) != len(set(entries)):
        errors.append("duplicate manifest entries")

    for relative, expected in sorted(entries.items()):
        path = root / relative
        if not path.is_file():
            errors.append(f"missing file: {relative}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(f"hash mismatch: {relative} (expected {expected}, found {actual})")

    if args.strict:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if relative == "MANIFEST_SHA256SUMS.txt":
                continue
            if any(part in IGNORED_PARTS for part in path.parts):
                continue
            if relative not in entries:
                errors.append(f"unlisted file: {relative}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {len(entries)} manifest entries verified; 0 failures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
