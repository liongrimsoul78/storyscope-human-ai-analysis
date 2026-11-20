#!/usr/bin/env python3
"""Adversarial tests for the reversibility and M-55 checks.

The validator exposes pure helpers (``reversibility_checks`` and
``m55_checks``) so these tests exercise exactly the logic used by
``validation/validate_compatibility_docs.py`` against synthetic inputs that
must fail. The repository documents are never modified.

An integration block also copies the real documents into a temporary root,
introduces one discrepancy, and runs the validator end to end to prove that
the failure is detected by the command the CI runs.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = ROOT / "validation"
DESIGN_DIR = ROOT / "docs" / "design" / "v0.3.0"

sys.path.insert(0, str(VALIDATION_DIR))
from validate_compatibility_docs import (  # noqa: E402
    m55_checks,
    reversibility_checks,
)


def failures(checks: list[tuple[bool, str]]) -> list[str]:
    return [message for condition, message in checks if not condition]


class ReversibilityCompositeTests(unittest.TestCase):
    def test_composite_with_supported_classes_passes(self) -> None:
        checks = reversibility_checks(
            "TV-XX",
            "A / B",
            ["M-01", "M-09"],
            ["A", "B"],
            "`observed` + `pattern_ai`",
        )
        self.assertEqual(failures(checks), [])

    def test_composite_introducing_unbacked_dash_fails(self) -> None:
        # M-01/M-09 never use —, so the vector cannot claim it.
        checks = reversibility_checks(
            "TV-XX",
            "A / —",
            ["M-01", "M-09"],
            ["A", "B"],
            "`observed` + `pattern_ai`",
        )
        messages = " ".join(failures(checks))
        self.assertIn("—", messages)
        self.assertTrue(failures(checks))

    def test_composite_with_unsupported_component_fails(self) -> None:
        checks = reversibility_checks(
            "TV-XX",
            "A / C",
            ["M-01", "M-09"],
            ["A", "B"],
            "`observed` + `pattern_ai`",
        )
        messages = " ".join(failures(checks))
        self.assertIn("'C'", messages)

    def test_composite_claiming_more_classes_than_rows_fails(self) -> None:
        checks = reversibility_checks(
            "TV-XX",
            "A / B / D",
            ["M-01"],
            ["A"],
            "`observed` + `pattern_ai`",
        )
        self.assertTrue(failures(checks))

    def test_all_dash_matrix_requires_dash_vector(self) -> None:
        checks = reversibility_checks(
            "TV-XX",
            "B",
            ["M-04", "M-08"],
            ["—", "—"],
            "quarantined; `CE-021`",
        )
        self.assertTrue(failures(checks))


class ReversibilitySingleReferenceTests(unittest.TestCase):
    def test_composite_matrix_row_accepts_sub_case(self) -> None:
        checks = reversibility_checks(
            "TV-XX",
            "D",
            ["M-32"],
            ["A/D"],
            "rejected; `CE-037`",
        )
        self.assertEqual(failures(checks), [])

    def test_dash_is_not_a_sub_case_of_a_converted_row(self) -> None:
        checks = reversibility_checks(
            "TV-XX",
            "—",
            ["M-32"],
            ["A/D"],
            "quarantined; `CE-037`",
        )
        self.assertTrue(failures(checks))

    def test_dash_requires_quarantine_or_rejection(self) -> None:
        checks = reversibility_checks(
            "TV-XX",
            "—",
            ["M-04"],
            ["—"],
            "conversión permitida",
        )
        messages = " ".join(failures(checks))
        self.assertIn("quarantined/rejected", messages)


class M55Tests(unittest.TestCase):
    CONTRACT = (
        "migration_attestations conserva la atestación externa. "
        "M-55 no genera `EvidenceRecord` por sí misma."
    )
    MATRIX = "M-55 | atestación válida (`migration_attestations`)"

    def row_a(self, **overrides: str) -> dict:
        row = {
            "route": "X",
            "target_field": "`run_level`",
            "target_value": "habilita `EvidenceRecord.observation_origin`",
            "conditions": "atestación válida (§11.6)",
        }
        row.update(overrides)
        return row

    def row_b(self, **overrides: str) -> dict:
        row = {
            "decision": "conversión condicionada",
            "reversibility": "B",
        }
        row.update(overrides)
        return row

    def test_m55_with_valid_attestation_and_complete_records_passes(self) -> None:
        checks = m55_checks(
            self.row_a(), self.row_b(), self.CONTRACT, self.MATRIX
        )
        self.assertEqual(failures(checks), [])

    def test_m55_without_valid_attestation_fails(self) -> None:
        checks = m55_checks(
            self.row_a(conditions="origen histórico demostrado"),
            self.row_b(),
            self.CONTRACT,
            self.MATRIX,
        )
        messages = " ".join(failures(checks))
        self.assertIn("valid migration attestation", messages)

    def test_m55_must_not_emit_an_evidence_record(self) -> None:
        checks = m55_checks(
            self.row_a(target_field="`EvidenceRecord`"),
            self.row_b(),
            self.CONTRACT,
            self.MATRIX,
        )
        messages = " ".join(failures(checks))
        self.assertIn("must not emit an EvidenceRecord", messages)

    def test_m55_requires_contract_to_preserve_attestations(self) -> None:
        checks = m55_checks(
            self.row_a(),
            self.row_b(),
            "M-55 no genera `EvidenceRecord` por sí misma.",
            self.MATRIX,
        )
        messages = " ".join(failures(checks))
        self.assertIn("migration_attestations", messages)

    def test_m55_must_stay_conditional_and_reversible_b(self) -> None:
        checks = m55_checks(
            self.row_a(),
            self.row_b(decision="conversión fiel", reversibility="A"),
            self.CONTRACT,
            self.MATRIX,
        )
        messages = " ".join(failures(checks))
        self.assertIn("conditional conversion", messages)
        self.assertIn("reversibility B", messages)


class ValidatorIntegrationTests(unittest.TestCase):
    """End-to-end: mutate a temporary copy and expect the validator to fail."""

    DOCS = (
        "COMPATIBILITY_EXPORT_CONTRACT_v0.3.md",
        "COMPATIBILITY_MAPPING_MATRIX_v0.3.md",
        "COMPATIBILITY_TEST_VECTORS_v0.3.md",
        "COMPATIBILITY_TEST_VECTORS_v0.2.md",
        "COMPATIBILITY_TEST_VECTORS_v0.1.md",
    )

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "validation").mkdir()
        shutil.copyfile(
            VALIDATION_DIR / "validate_compatibility_docs.py",
            self.root / "validation" / "validate_compatibility_docs.py",
        )
        (self.root / "docs" / "design" / "v0.3.0").mkdir(parents=True)
        for name in self.DOCS:
            shutil.copyfile(DESIGN_DIR / name, self.root / "docs" / "design" / "v0.3.0" / name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        # Force UTF-8 in the child: the validator prints "—" and accents, and
        # Windows would otherwise emit them in the legacy console code page.
        env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
        return subprocess.run(
            [sys.executable, "validation/validate_compatibility_docs.py"],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )

    def mutate(self, name: str, old: str, new: str) -> None:
        path = self.root / "docs" / "design" / "v0.3.0" / name
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")

    def test_baseline_copy_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unbacked_dash_on_composite_vector_is_detected(self) -> None:
        # TV-29 is A / B over M-01/M-09 (A, B). Replacing B with — introduces
        # a class no referenced row supports.
        self.mutate(
            "COMPATIBILITY_TEST_VECTORS_v0.3.md",
            "| Reversibilidad | A / B |\n| Matriz | M-01 / M-09 |",
            "| Reversibilidad | A / — |\n| Matriz | M-01 / M-09 |",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("not backed by any referenced matrix row", result.stdout)

    def test_m55_without_attestation_is_detected(self) -> None:
        self.mutate(
            "COMPATIBILITY_MAPPING_MATRIX_v0.3.md",
            "| M-55 | X | ejecución | origen atestable durante la migración | ejecución | procedencia demostrable por atestación válida del operador | `run_level` | habilita `EvidenceRecord.observation_origin` en las filas completas; no emite registros por sí misma | atestación válida (§11.6) |",
            "| M-55 | X | ejecución | origen atestable durante la migración | ejecución | procedencia demostrable por atestación válida del operador | `run_level` | habilita `EvidenceRecord.observation_origin` en las filas completas; no emite registros por sí misma | sin condición |",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("valid migration attestation", result.stdout)


if __name__ == "__main__":
    unittest.main()
