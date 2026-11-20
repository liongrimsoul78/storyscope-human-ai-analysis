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
    ALLOWED_ATTESTED_ORIGINS,
    ATTESTATION_REQUIRED_FIELDS,
    attestation_checks,
    attestation_is_valid,
    m55_checks,
    provenance_checks,
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
        "M-55 no genera `EvidenceRecord` por sí misma. "
        "Concordancia entre vías. R-29a. attested_origin authorization_status "
        "ISO 8601 UTC " + " ".join(ATTESTATION_REQUIRED_FIELDS)
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

    def test_m55_documental_structure_passes(self) -> None:
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


class ProvenancePathTests(unittest.TestCase):
    """R-29: two provenance paths, with concordance."""

    CONTRACT = (
        "migration_attestations conserva la atestación externa. "
        "M-55 no genera `EvidenceRecord` por sí misma. "
        "Concordancia entre vías. R-29a. attested_origin authorization_status "
        "ISO 8601 UTC " + " ".join(ATTESTATION_REQUIRED_FIELDS)
    )

    def valid_attestation(self, origin: str = "human_annotation") -> dict:
        return {
            "legacy_locator": "abc:§4:1:feature",
            "legacy_sublocator": "abc:§4:1:feature:obs:1",
            "attested_origin": origin,
            "attested_by": "op-1",
            "attested_at_utc": "2026-11-19T00:00:00Z",
            "basis": "fundamento",
            "protocol_version": "0.2.3",
            "authorization_status": "authorized",
        }

    def test_direct_declaration_without_attestation_passes(self) -> None:
        checks = provenance_checks("human_annotation", {}, self.CONTRACT)
        self.assertEqual(failures(checks), [])

    def test_absent_declaration_with_valid_attestation_passes(self) -> None:
        att = self.valid_attestation()
        checks = provenance_checks(
            None, att, self.CONTRACT,
            expected_locator=att["legacy_locator"],
            expected_sublocator=att["legacy_sublocator"],
        )
        self.assertEqual(failures(checks), [])

    def test_absent_declaration_and_absent_attestation_fails_r29(self) -> None:
        checks = provenance_checks(None, {}, self.CONTRACT)
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_contradicting_direct_and_attested_origins_fails_r29a(self) -> None:
        att = self.valid_attestation("external_model")
        checks = provenance_checks(
            "human_annotation", att, self.CONTRACT,
            expected_locator=att["legacy_locator"],
            expected_sublocator=att["legacy_sublocator"],
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29a", messages)


class AttestationValidityTests(unittest.TestCase):
    """Validity of a migration attestation entry."""

    CONTRACT = (
        "migration_attestations conserva la atestación externa. "
        "M-55 no genera `EvidenceRecord` por sí misma. "
        "Concordancia entre vías. R-29a. attested_origin authorization_status "
        "ISO 8601 UTC " + " ".join(ATTESTATION_REQUIRED_FIELDS)
    )

    def base(self, **overrides: str) -> dict:
        entry = {
            "legacy_locator": "abc:§4:1:feature",
            "legacy_sublocator": "abc:§4:1:feature:obs:1",
            "attested_origin": "human_annotation",
            "attested_by": "op-1",
            "attested_at_utc": "2026-11-19T00:00:00Z",
            "basis": "fundamento",
            "protocol_version": "0.2.3",
            "authorization_status": "authorized",
        }
        entry.update(overrides)
        return entry

    def test_attested_origin_outside_vocabulary_fails(self) -> None:
        checks = attestation_checks(
            self.base(attested_origin="invented_origin"), None, self.CONTRACT
        )
        messages = " ".join(failures(checks))
        self.assertIn("outside the allowed vocabulary", messages)

    def test_missing_required_field_fails(self) -> None:
        entry = self.base()
        del entry["basis"]
        checks = attestation_checks(entry, None, self.CONTRACT)
        messages = " ".join(failures(checks))
        self.assertIn("basis", messages)

    def test_not_authorized_status_fails(self) -> None:
        checks = attestation_checks(
            self.base(authorization_status="not_authorized"), None, self.CONTRACT
        )
        messages = " ".join(failures(checks))
        self.assertIn("not_authorized", messages)

    def test_valid_attestation_passes(self) -> None:
        checks = attestation_checks(self.base(), None, self.CONTRACT)
        self.assertEqual(failures(checks), [])

    def test_not_applicable_status_is_pending_not_failure(self) -> None:
        # "not_applicable" has no documented criterion: it must not be treated
        # as an automatic failure, but it does not enable M-55.
        checks = attestation_checks(
            self.base(authorization_status="not_applicable"), None, self.CONTRACT
        )
        # All documented-value checks pass; only the enabling condition differs.
        self.assertTrue(
            all(condition for condition, _ in checks),
            failures(checks),
        )


    def test_spaces_only_fields_fail(self) -> None:
        entry = self.base(basis="   ")
        checks = attestation_checks(entry, None, self.CONTRACT)
        messages = " ".join(failures(checks))
        self.assertIn("basis", messages)

    def test_malformed_iso_date_fails(self) -> None:
        entry = self.base(attested_at_utc="not-a-date")
        checks = attestation_checks(entry, None, self.CONTRACT)
        messages = " ".join(failures(checks))
        self.assertIn("ISO 8601", messages)

    def test_non_utc_timezone_fails(self) -> None:
        entry = self.base(attested_at_utc="2026-11-19T00:00:00+02:00")
        checks = attestation_checks(entry, None, self.CONTRACT)
        messages = " ".join(failures(checks))
        self.assertIn("ISO 8601", messages)

    def test_locator_mismatch_fails(self) -> None:
        entry = self.base()
        checks = attestation_checks(
            entry, None, self.CONTRACT, expected_locator="other:locator"
        )
        messages = " ".join(failures(checks))
        self.assertIn("legacy_locator must match", messages)

    def test_sublocator_mismatch_fails(self) -> None:
        entry = self.base()
        checks = attestation_checks(
            entry, None, self.CONTRACT, expected_sublocator="other:sub"
        )
        messages = " ".join(failures(checks))
        self.assertIn("legacy_sublocator must match", messages)

    def test_not_applicable_with_direct_declaration_passes_direct_path(self) -> None:
        # not_applicable alone does not enable M-55, but a valid direct
        # declaration keeps the provenance path valid.
        checks = provenance_checks(
            "human_annotation", self.base(authorization_status="not_applicable"),
            self.CONTRACT,
        )
        self.assertEqual(failures(checks), [])

    def test_not_applicable_alone_fails_r29(self) -> None:
        checks = provenance_checks(
            None, self.base(authorization_status="not_applicable"), self.CONTRACT
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)


class ObservationCorrespondenceTests(unittest.TestCase):
    """Attestations only authorize the observation they point to."""

    CONTRACT = (
        "migration_attestations conserva la atestación externa. "
        "M-55 no genera `EvidenceRecord` por sí misma. "
        "Concordancia entre vías. R-29a. attested_origin authorization_status "
        "ISO 8601 UTC " + " ".join(ATTESTATION_REQUIRED_FIELDS)
    )

    def base(self, **overrides: str) -> dict:
        entry = {
            "legacy_locator": "loc-A",
            "legacy_sublocator": "sub-A",
            "attested_origin": "human_annotation",
            "attested_by": "op-1",
            "attested_at_utc": "2026-11-19T00:00:00Z",
            "basis": "fundamento",
            "protocol_version": "0.2.3",
            "authorization_status": "authorized",
        }
        entry.update(overrides)
        return entry

    def test_two_attestations_for_different_observations(self) -> None:
        att_a = self.base()
        att_b = self.base(
            legacy_locator="loc-B", legacy_sublocator="sub-B",
            attested_origin="external_model",
        )
        # Observation A: only att_a matches and is valid.
        checks_a = provenance_checks(
            None, [att_a, att_b], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        self.assertEqual(failures(checks_a), [])
        # Observation B: only att_b matches and is valid.
        checks_b = provenance_checks(
            None, [att_a, att_b], self.CONTRACT,
            expected_locator="loc-B", expected_sublocator="sub-B",
        )
        self.assertEqual(failures(checks_b), [])

    def test_valid_attestation_does_not_authorize_another_observation(self) -> None:
        att_a = self.base()
        # Observation B has no matching attestation.
        checks = provenance_checks(
            None, [att_a], self.CONTRACT,
            expected_locator="loc-B", expected_sublocator="sub-B",
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_invalid_attestation_cannot_satisfy_r29(self) -> None:
        att = self.base(authorization_status="not_authorized")
        checks = provenance_checks(None, [att], self.CONTRACT)
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_attestation_is_valid_rejects_non_authorized(self) -> None:
        att = self.base(authorization_status="not_authorized")
        self.assertFalse(attestation_is_valid(att))


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


class Phase1226AttestationTests(unittest.TestCase):
    """Adversarial coverage for FASE 1.22.6 attestation correspondence/conflicts."""

    CONTRACT = (
        "migration_attestations conserva la atestación externa. "
        "M-55 no genera `EvidenceRecord` por sí misma. "
        "Concordancia entre vías. R-29a. attested_origin authorization_status "
        "ISO 8601 UTC " + " ".join(ATTESTATION_REQUIRED_FIELDS)
    )

    def base(self, **overrides: str) -> dict:
        entry = {
            "legacy_locator": "loc-A",
            "legacy_sublocator": "sub-A",
            "attested_origin": "human_annotation",
            "attested_by": "op-1",
            "attested_at_utc": "2026-11-19T00:00:00Z",
            "basis": "fundamento",
            "protocol_version": "0.2.3",
            "authorization_status": "authorized",
        }
        entry.update(overrides)
        return entry

    def test_01_authorized_with_both_expected_locators_passes(self) -> None:
        att = self.base()
        self.assertTrue(attestation_is_valid(att, "loc-A", "sub-A"))
        checks = provenance_checks(
            None, [att], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        self.assertEqual(failures(checks), [])

    def test_02_without_expected_locator_does_not_enable_r29(self) -> None:
        att = self.base()
        checks = provenance_checks(
            None, [att], self.CONTRACT,
            expected_locator=None, expected_sublocator="sub-A",
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_03_without_expected_sublocator_does_not_enable_r29(self) -> None:
        att = self.base()
        checks = provenance_checks(
            None, [att], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator=None,
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_04_incorrect_locator_does_not_enable_r29(self) -> None:
        att = self.base()
        self.assertFalse(attestation_is_valid(att, "loc-X", "sub-A"))
        checks = provenance_checks(
            None, [att], self.CONTRACT,
            expected_locator="loc-X", expected_sublocator="sub-A",
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_05_incorrect_sublocator_does_not_enable_r29(self) -> None:
        att = self.base()
        self.assertFalse(attestation_is_valid(att, "loc-A", "sub-X"))
        checks = provenance_checks(
            None, [att], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-X",
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_06_direct_valid_without_attestation_passes(self) -> None:
        checks = provenance_checks("human_annotation", [], self.CONTRACT)
        self.assertEqual(failures(checks), [])

    def test_07_two_attestations_different_observations(self) -> None:
        att_a = self.base()
        att_b = self.base(
            legacy_locator="loc-B", legacy_sublocator="sub-B",
            attested_origin="external_model",
        )
        checks_a = provenance_checks(
            None, [att_a, att_b], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        checks_b = provenance_checks(
            None, [att_a, att_b], self.CONTRACT,
            expected_locator="loc-B", expected_sublocator="sub-B",
        )
        self.assertEqual(failures(checks_a), [])
        self.assertEqual(failures(checks_b), [])

    def test_08_two_attestations_same_observation_same_origin(self) -> None:
        att1 = self.base()
        att2 = self.base(attested_by="op-2")
        checks = provenance_checks(
            None, [att1, att2], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        self.assertEqual(failures(checks), [])

    def test_09_two_attestations_same_observation_different_origin_conflict(self) -> None:
        att1 = self.base()
        att2 = self.base(attested_origin="external_model")
        checks = provenance_checks(
            None, [att1, att2], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29a", messages)
        self.assertIn("conflict", messages.lower())

    def test_10_direct_valid_with_coincident_attestations_passes(self) -> None:
        att1 = self.base()
        att2 = self.base(attested_by="op-2")
        checks = provenance_checks(
            "human_annotation", [att1, att2], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        self.assertEqual(failures(checks), [])

    def test_11_direct_valid_with_contradictory_attestation_r29a(self) -> None:
        att = self.base(attested_origin="external_model")
        checks = provenance_checks(
            "human_annotation", [att], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29a", messages)

    def test_12_invalid_attestation_does_not_substitute_valid(self) -> None:
        valid = self.base()
        invalid = self.base(authorization_status="not_authorized", attested_origin="external_model")
        checks = provenance_checks(
            None, [valid, invalid], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        self.assertEqual(failures(checks), [])

    def test_13_each_required_field_absent(self) -> None:
        for field_name in ATTESTATION_REQUIRED_FIELDS:
            entry = self.base()
            del entry[field_name]
            checks = attestation_checks(entry, None, self.CONTRACT)
            messages = " ".join(failures(checks))
            self.assertIn(field_name, messages, field_name)

    def test_14_each_required_field_spaces_only(self) -> None:
        for field_name in ATTESTATION_REQUIRED_FIELDS:
            entry = self.base(**{field_name: "   "})
            checks = attestation_checks(entry, None, self.CONTRACT)
            messages = " ".join(failures(checks))
            self.assertIn(field_name, messages, field_name)

    def test_15_not_authorized_cannot_enable_r29(self) -> None:
        att = self.base(authorization_status="not_authorized")
        self.assertFalse(attestation_is_valid(att))
        checks = provenance_checks(
            None, [att], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_16_not_applicable_cannot_enable_m55_by_itself(self) -> None:
        att = self.base(authorization_status="not_applicable")
        self.assertFalse(attestation_is_valid(att))
        checks = provenance_checks(
            None, [att], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        messages = " ".join(failures(checks))
        self.assertIn("R-29", messages)

    def test_17_not_applicable_with_direct_valid(self) -> None:
        att = self.base(authorization_status="not_applicable")
        checks = provenance_checks(
            "human_annotation", [att], self.CONTRACT,
            expected_locator="loc-A", expected_sublocator="sub-A",
        )
        self.assertEqual(failures(checks), [])



if __name__ == "__main__":
    unittest.main()
