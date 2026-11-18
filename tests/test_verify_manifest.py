#!/usr/bin/env python3
"""Regression tests for validation/verify_manifest.py.

Each test builds a throwaway skill root containing a copy of the real verifier,
so the repository working tree is never modified. The contract under test is
narrow: strict mode ignores only root VCS metadata (``.git``) and the root
``_export`` directory, and keeps verifying every other project file.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "validation" / "verify_manifest.py"
PY = sys.executable
MANIFEST = "MANIFEST_SHA256SUMS.txt"
VERIFIER_RELATIVE = "validation/verify_manifest.py"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ManifestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "validation").mkdir()
        (self.root / "validation" / "verify_manifest.py").write_bytes(SCRIPT.read_bytes())
        self.verifier_entry = f"{digest(SCRIPT.read_bytes())}  {VERIFIER_RELATIVE}"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, relative: str, data: bytes | str = "content\n") -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            data = data.encode("utf-8")
        path.write_bytes(data)
        return path

    def entry(self, relative: str) -> str:
        return f"{digest((self.root / relative).read_bytes())}  {relative}"

    def write_manifest(self, lines: list[str]) -> None:
        """Write the manifest, always listing the copied verifier itself."""
        content = [self.verifier_entry, *lines]
        (self.root / MANIFEST).write_text("\n".join(content) + "\n", encoding="utf-8")

    def run_verifier(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [PY, str(self.root / "validation" / "verify_manifest.py"), *args],
            cwd=str(self.root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def assert_passes(self, *args: str) -> None:
        result = self.run_verifier(*args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 failures", result.stdout)

    def assert_fails_with(self, needle: str, *args: str) -> None:
        result = self.run_verifier(*args)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(needle, result.stdout)


class VcsMetadataScopeTests(ManifestCase):
    def test_strict_passes_with_git_directory(self) -> None:
        self.write("README.md")
        self.write(".git/config", "[core]\n")
        self.write(".git/objects/ab/cdef0123", b"\x00binary\n")
        self.write_manifest([self.entry("README.md")])
        self.assert_passes("--strict")

    def test_strict_passes_with_git_file_pointer(self) -> None:
        self.write("README.md")
        self.write(".git", "gitdir: ../worktrees/storyscope\n")
        self.write_manifest([self.entry("README.md")])
        self.assert_passes("--strict")

    def test_git_like_names_are_still_inspected(self) -> None:
        self.write("archivo.git", "not metadata\n")
        self.write("docs/.git-example/notes.md", "not metadata\n")
        self.write("docs/git-reference.md", "not metadata\n")
        self.write_manifest([])
        result = self.run_verifier("--strict")
        self.assertEqual(result.returncode, 1, result.stdout)
        for expected in (
            "archivo.git",
            "docs/.git-example/notes.md",
            "docs/git-reference.md",
        ):
            self.assertIn(expected, result.stdout)


class ExportScopeTests(ManifestCase):
    def test_root_export_directory_is_ignored(self) -> None:
        self.write("README.md")
        self.write("_export/README.md", "exported copy\n")
        self.write("_export/validation/verify_manifest.py", "# copy\n")
        self.write_manifest([self.entry("README.md")])
        self.assert_passes("--strict")

    def test_exported_directory_is_still_inspected(self) -> None:
        self.write("README.md")
        self.write("_exported/extra.txt", "unexpected\n")
        self.write_manifest([self.entry("README.md")])
        self.assert_fails_with("_exported/extra.txt", "--strict")

    def test_nested_export_directory_is_still_inspected(self) -> None:
        self.write("docs/_export/extra.txt", "unexpected\n")
        self.write_manifest([])
        self.assert_fails_with("docs/_export/extra.txt", "--strict")

    def test_export_file_at_root_is_still_inspected(self) -> None:
        self.write("_export", "a file, not the generated directory\n")
        self.write_manifest([])
        self.assert_fails_with("unlisted file: _export", "--strict")


class StrictCoverageTests(ManifestCase):
    def test_unlisted_root_file_fails(self) -> None:
        self.write("unlisted.txt", "unexpected\n")
        self.write_manifest([])
        self.assert_fails_with("unlisted file: unlisted.txt", "--strict")

    def test_unlisted_nested_file_fails(self) -> None:
        self.write("docs/design/extra.md", "unexpected\n")
        self.write_manifest([])
        self.assert_fails_with("unlisted file: docs/design/extra.md", "--strict")

    def test_listed_nested_paths_resolve(self) -> None:
        self.write("docs/design/notes.md", "listed\n")
        self.write_manifest([self.entry("docs/design/notes.md")])
        self.assert_passes("--strict")

    def test_hash_mismatch_fails(self) -> None:
        self.write("README.md", "real content\n")
        self.write_manifest(["0" * 64 + "  README.md"])
        self.assert_fails_with("hash mismatch: README.md", "--strict")

    def test_missing_expected_file_fails(self) -> None:
        self.write_manifest(["a" * 64 + "  missing.txt"])
        self.assert_fails_with("missing file: missing.txt", "--strict")

    def test_malformed_entry_fails(self) -> None:
        self.write("README.md")
        self.write_manifest(["not-a-hash  README.md"])
        self.assert_fails_with("malformed manifest entry", "--strict")

    def test_duplicate_entry_fails(self) -> None:
        self.write("README.md")
        line = self.entry("README.md")
        self.write_manifest([line, line])
        self.assert_fails_with("duplicate manifest entries: README.md", "--strict")

    def test_pycache_directories_are_ignored(self) -> None:
        self.write("README.md")
        self.write("validation/__pycache__/module.cpython-312.pyc", b"\x00")
        self.write(".pytest_cache/v/cache/nodeids", "[]\n")
        self.write_manifest([self.entry("README.md")])
        self.assert_passes("--strict")

    def test_manifest_is_not_required_to_list_itself(self) -> None:
        self.write("README.md")
        self.write_manifest([self.entry("README.md")])
        self.assert_passes("--strict")

    def test_non_strict_mode_allows_unlisted_files(self) -> None:
        self.write("README.md")
        self.write("unlisted.txt", "unexpected\n")
        self.write_manifest([self.entry("README.md")])
        self.assert_passes()

    def test_missing_manifest_returns_exit_code_two(self) -> None:
        result = self.run_verifier("--strict")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("missing manifest", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
