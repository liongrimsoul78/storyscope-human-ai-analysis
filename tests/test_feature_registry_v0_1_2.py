"""Automated tests for validation/validate_feature_registry_v0_1_2.py.

These tests operate only on temporary copies. The two real registry files are
never modified.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DIR = ROOT / "validation"
VALIDATOR = VALIDATION_DIR / "validate_feature_registry_v0_1_2.py"
REGISTRY_V011 = ROOT / "docs" / "design" / "v0.3.0" / "FEATURE_REGISTRY_v0.1.1_draft.json"
REGISTRY_V012 = ROOT / "docs" / "design" / "v0.3.0" / "FEATURE_REGISTRY_v0.1.2-draft.json"

sys.path.insert(0, str(VALIDATION_DIR))
from validate_feature_registry_v0_1_2 import validate_registry  # noqa: E402


def copy_file(source: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return destination


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def mutate(path: Path, mutator) -> None:
    data = load_json(path)
    mutator(data)
    write_json(path, data)


def run_cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=str(cwd or Path(tempfile.gettempdir())),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class TestFeatureRegistryV012(unittest.TestCase):
    def make_registry(self, tmp: str, mutator=None, source: Path = REGISTRY_V012, filename: str = "registry.json") -> Path:
        path = Path(tmp) / filename
        copy_file(source, path)
        if mutator is not None:
            mutate(path, mutator)
        return path

    def make_baseline(self, tmp: str, source: Path = REGISTRY_V011) -> Path:
        path = Path(tmp) / "baseline.json"
        copy_file(source, path)
        return path

    def assert_errors(self, errors, *fragments):
        self.assertTrue(errors, "expected validation errors, but none were returned")
        joined = "\n".join(errors)
        for fragment in fragments:
            self.assertIn(fragment, joined)

    def assert_no_errors(self, errors):
        self.assertEqual(errors, [], "\n".join(errors))

    # --- Original 20 cases ---

    def test_valid_registry(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_no_errors(errors)

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            path.write_text("{not valid json", encoding="utf-8")
            errors, _checks = validate_registry(path, None)
            self.assert_errors(errors, "cannot read or parse JSON")

    def test_wrong_registry_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d.__setitem__("registry_version", "0.1.1-draft"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "registry_version must be '0.1.2-draft'")

    def test_wrong_schema_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d.__setitem__("schema_version", "1.0.0"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "schema_version must be '1.1.0'")

    def test_wrong_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d.__setitem__("status", "approved"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "status must be 'draft_for_review'")

    def test_wrong_feature_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"].pop())
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "feature_records must contain 30 entries")

    def test_duplicate_feature_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                data["feature_records"][1]["feature_id"] = data["feature_records"][0]["feature_id"]

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "duplicate feature_id values")

    def test_missing_historical_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                del data["feature_records"][0]["historical_reference_pattern_id"]

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "missing historical_reference_pattern_id")

    def test_null_historical_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("historical_reference_pattern_id", None))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "historical_reference_pattern_id must be a non-empty string")

    def test_nonexistent_historical_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("historical_reference_pattern_id", "ssha.pattern.does_not_exist"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "does not belong to this feature's reference_patterns")

    def test_cross_feature_historical_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                data["feature_records"][0]["historical_reference_pattern_id"] = data["feature_records"][1]["reference_patterns"][0]["pattern_id"]

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "does not belong to this feature's reference_patterns")

    def test_ai_reference_omitted_when_ai_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            bidirectional = next(f for f in load_json(REGISTRY_V012)["feature_records"] if len({p["pattern_direction"] for p in f["reference_patterns"]}) == 2)
            feature_id = bidirectional["feature_id"]

            def mutate_data(data):
                feature = next(f for f in data["feature_records"] if f["feature_id"] == feature_id)
                human_pattern = next(p["pattern_id"] for p in feature["reference_patterns"] if p["pattern_direction"] == "pattern_human")
                feature["historical_reference_pattern_id"] = human_pattern

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "uses the human pattern, but an AI pattern exists")

    def test_wrong_human_reference_when_no_ai_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = load_json(REGISTRY_V012)
            human_only = next(f for f in original["feature_records"] if all(p["pattern_direction"] == "pattern_human" for p in f["reference_patterns"]))
            target_id = human_only["feature_id"]
            other_human = next(
                f["reference_patterns"][0]["pattern_id"]
                for f in original["feature_records"]
                if f["feature_id"] != target_id and all(p["pattern_direction"] == "pattern_human" for p in f["reference_patterns"])
            )

            def mutate_data(data):
                feature = next(f for f in data["feature_records"] if f["feature_id"] == target_id)
                feature["historical_reference_pattern_id"] = other_human

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "does not belong to this feature's reference_patterns")

    def test_ambiguous_reference_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                feature = data["feature_records"][0]
                duplicate = dict(feature["reference_patterns"][0])
                duplicate["pattern_id"] = feature["reference_patterns"][0]["pattern_id"] + ".ambiguous_candidate"
                feature["reference_patterns"].append(duplicate)

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "ambiguous historical reference")

    def test_unauthorized_scientific_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("canonical_name", "Changed Name"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "scientific field 'canonical_name' changed")

    def test_allowed_version_and_schema_changes(self):
        errors, _checks = validate_registry(REGISTRY_V012, REGISTRY_V011)
        self.assert_no_errors(errors)

    def test_nonexistent_dimension(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("dimension_id", "does_not_exist"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "dimension_id 'does_not_exist' does not exist")

    def test_nonexistent_cluster(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("cluster_id", "does_not_exist"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "cluster_id 'does_not_exist' does not exist")

    def test_duplicate_pattern(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                data["feature_records"][1]["reference_patterns"][0]["pattern_id"] = data["feature_records"][0]["reference_patterns"][0]["pattern_id"]

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "duplicate pattern_id values")

    def test_duplicate_historical_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                shared_ref = data["feature_records"][0]["historical_reference_pattern_id"]
                data["feature_records"][1]["reference_patterns"][0]["pattern_id"] = shared_ref
                data["feature_records"][1]["historical_reference_pattern_id"] = shared_ref

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "duplicate historical_reference_pattern_id values")

    # --- M-1: baseline protection ---

    def test_no_baseline_requires_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp)
            errors, _checks = validate_registry(registry, None)
            self.assert_errors(errors, "scientific comparison requires a baseline registry")

    def test_missing_baseline_file_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing-baseline.json"
            result = run_cli("--baseline", str(missing))
            self.assertEqual(result.returncode, 2)
            self.assertIn("baseline file not found", result.stdout + result.stderr)

    # --- M-2: CLI coverage ---

    def test_cli_help(self):
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout.lower())

    def test_cli_default_success(self):
        result = run_cli()
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS:", result.stdout)

    def test_cli_verbose(self):
        result = run_cli("--verbose")
        self.assertEqual(result.returncode, 0)
        self.assertIn("OK:", result.stdout)

    def test_cli_registry_and_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp)
            baseline = self.make_baseline(tmp)
            result = run_cli("--registry", str(registry), "--baseline", str(baseline))
            self.assertEqual(result.returncode, 0)
            self.assertIn("PASS:", result.stdout)

    def test_cli_invalid_registry_exit_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invalid.json"
            path.write_text("{not valid json", encoding="utf-8")
            baseline = self.make_baseline(tmp)
            result = run_cli("--registry", str(path), "--baseline", str(baseline))
            self.assertEqual(result.returncode, 1)
            self.assertIn("FAIL:", result.stdout + result.stderr)

    def test_cli_missing_registry_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing-registry.json"
            result = run_cli("--registry", str(missing))
            self.assertEqual(result.returncode, 2)
            self.assertIn("registry file not found", result.stdout + result.stderr)

    def test_cli_invalid_argument_exit_2(self):
        result = run_cli("--not-a-real-option")
        self.assertEqual(result.returncode, 2)
        self.assertIn("error:", (result.stdout + result.stderr).lower())

    def test_cli_from_different_working_directory(self):
        result = run_cli(cwd=Path(tempfile.gettempdir()))
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS:", result.stdout)

    # --- M-3: scientific comparison coverage ---

    def test_nested_reference_pattern_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0]["reference_patterns"][0].__setitem__("pattern_label", "changed"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "scientific field 'reference_patterns' changed")

    def test_feature_property_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("canonical_name", "Changed Name"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "scientific field 'canonical_name' changed")

    def test_reordered_feature_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                data["feature_records"][0], data["feature_records"][1] = data["feature_records"][1], data["feature_records"][0]

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "changed feature_id")

    def test_unexpected_top_level_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d.__setitem__("unexpected_top_level", 1))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "unexpected top-level keys")

    def test_unexpected_feature_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("unexpected_feature_key", 1))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "unexpected feature keys")

    def test_missing_top_level_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d.pop("source_baseline"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "missing top-level key 'source_baseline'")

    def test_missing_feature_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].pop("canonical_name"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "missing feature keys")

    def test_nested_list_property_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0]["reference_patterns"][0].__setitem__("pattern_label", "changed"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "scientific field 'reference_patterns' changed")

    def test_reordered_patterns_does_not_change_ai_first_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                feature = next(f for f in data["feature_records"] if len(f["reference_patterns"]) > 1)
                feature["reference_patterns"].reverse()

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "scientific field 'reference_patterns' changed")
            joined = "\n".join(errors)
            self.assertNotIn("does not follow the AI-first rule", joined)
            self.assertNotIn("ambiguous historical reference", joined)

    # --- M-4: integrity_notes restrictions ---

    def test_integrity_notes_original_preserved(self):
        errors, _checks = validate_registry(REGISTRY_V012, REGISTRY_V011)
        self.assert_no_errors(errors)

    def test_integrity_notes_authorized_addition_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            baseline = self.make_registry(tmp, source=REGISTRY_V012, filename="baseline.json")
            candidate = self.make_registry(tmp, source=REGISTRY_V012, filename="candidate.json")
            data = load_json(baseline)
            authorized_notes = {
                "historical_reference_pattern_id is added in registry version 0.1.2-draft as an explicit, validated selection of an existing reference pattern. It is not a new empirical claim: if an AI pattern exists, that pattern is selected; otherwise the human pattern is selected.",
                "For the current 30 features, historical_reference_pattern_id is mandatory and non-null. Future features without directional patterns may use null and then support only not_assessed relations.",
                "historical_reference_pattern_id is resolved by feature_id plus AnalysisRun.feature_registry_version; it is not duplicated in EvidenceRecord. Registry schema 1.1.0 adds this field; registry version 0.1.1-draft used schema 1.0.0.",
                "In the three bidirectional features, the historical reference is the AI pattern as a compatibility convention for historical comparison. This is not a hierarchy of quality between human and AI writing.",
            }
            data["integrity_notes"] = [note for note in data["integrity_notes"] if note not in authorized_notes]
            write_json(baseline, data)
            errors, _checks = validate_registry(candidate, baseline)
            self.assert_no_errors(errors)

    def test_integrity_notes_arbitrary_addition_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["integrity_notes"].append("arbitrary note"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "integrity_notes multiplicity")

    def test_integrity_notes_original_modified_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            def mutate_data(data):
                data["integrity_notes"][0] = "tampered note"

            registry = self.make_registry(tmp, mutate_data)
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "integrity_notes multiplicity")

    def test_integrity_notes_original_removed_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["integrity_notes"].pop(0))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "integrity_notes multiplicity")

    def test_integrity_notes_original_duplicated_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["integrity_notes"].insert(0, d["integrity_notes"][0]))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "integrity_notes multiplicity")

    def test_integrity_notes_transition_duplicated_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            authorized = "historical_reference_pattern_id is added in registry version 0.1.2-draft as an explicit, validated selection of an existing reference pattern. It is not a new empirical claim: if an AI pattern exists, that pattern is selected; otherwise the human pattern is selected."
            registry = self.make_registry(tmp, lambda d: d["integrity_notes"].append(authorized))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "integrity_notes multiplicity")

    def test_integrity_notes_two_repeated_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["integrity_notes"].extend([d["integrity_notes"][0], d["integrity_notes"][1]]))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "integrity_notes multiplicity")

    def test_invalid_baseline_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp)
            baseline = Path(tmp) / "invalid-baseline.json"
            baseline.write_text("{not valid json", encoding="utf-8")
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "cannot read or parse JSON")

    # --- M-5: complete structural validation ---

    def test_wrong_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["counts"].__setitem__("core_features", 31))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "counts must equal")

    def test_wrong_dimension_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["dimensions"].pop())
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "dimensions must be a list of 10")

    def test_wrong_cluster_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["cluster_catalog"].pop())
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "cluster_catalog must be a list of 8")

    def test_duplicate_dimension(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["dimensions"][1].__setitem__("dimension_id", d["dimensions"][0]["dimension_id"]))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "duplicate dimension_id")

    def test_duplicate_cluster(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["cluster_catalog"][1].__setitem__("cluster_id", d["cluster_catalog"][0]["cluster_id"]))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "duplicate cluster_id")

    def test_core_feature_count_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["dimensions"][0].__setitem__("core_feature_count", 999))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "declares core_feature_count")

    def test_invalid_dimension_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["dimensions"][0].__setitem__("display_name", ""))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "display_name must be a non-empty string")

    def test_invalid_cluster_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["cluster_catalog"][0].__setitem__("origin", ""))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "origin must be a non-empty string")

    def test_invalid_pattern_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0]["reference_patterns"][0].__setitem__("pattern_label", ""))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "pattern_label must be a non-empty string")

    def test_invalid_feature_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("canonical_name", ""))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "canonical_name must be a non-empty string")

    def test_missing_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d.pop("counts"))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "missing top-level keys")

    def test_unknown_top_level_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d.__setitem__("unexpected_top_level", 1))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "unexpected top-level keys")

    def test_unknown_feature_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = self.make_registry(tmp, lambda d: d["feature_records"][0].__setitem__("unexpected_feature_key", 1))
            baseline = self.make_baseline(tmp)
            errors, _checks = validate_registry(registry, baseline)
            self.assert_errors(errors, "unexpected feature keys")

    # --- B improvements: behavior preserved ---

    def test_ai_unidirectional_count_preserved(self):
        errors, _checks = validate_registry(REGISTRY_V012, REGISTRY_V011)
        self.assert_no_errors(errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)