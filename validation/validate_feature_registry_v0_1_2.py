#!/usr/bin/env python3
"""Validate StoryScope Feature Registry v0.1.2-draft.

This validator checks the structural and referential integrity of
``docs/design/v0.3.0/FEATURE_REGISTRY_v0.1.2-draft.json``, including the
A2 historical-reference rules. It uses only the Python standard library.

It does not classify narratives, invent thresholds, directions, patterns or
evidence values. Its purpose is to verify that the registry remains internally
consistent and that v0.1.2 differs from v0.1.1 only in the authorized
transition fields.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_REGISTRY = Path(__file__).resolve().parents[1] / "docs" / "design" / "v0.3.0" / "FEATURE_REGISTRY_v0.1.2-draft.json"
DEFAULT_BASELINE = Path(__file__).resolve().parents[1] / "docs" / "design" / "v0.3.0" / "FEATURE_REGISTRY_v0.1.1_draft.json"

ALLOWED_PATTERN_DIRECTIONS = {"pattern_ai", "pattern_human"}
AUTHORIZED_EXTRA_FEATURE_KEYS = {"historical_reference_pattern_id"}
AUTHORIZED_TOP_LEVEL_CHANGES = {"registry_version", "schema_version", "integrity_notes"}
AUTHORIZED_INTEGRITY_NOTE_ADDITIONS = {
    "historical_reference_pattern_id is added in registry version 0.1.2-draft as an explicit, validated selection of an existing reference pattern. It is not a new empirical claim: if an AI pattern exists, that pattern is selected; otherwise the human pattern is selected.",
    "For the current 30 features, historical_reference_pattern_id is mandatory and non-null. Future features without directional patterns may use null and then support only not_assessed relations.",
    "historical_reference_pattern_id is resolved by feature_id plus AnalysisRun.feature_registry_version; it is not duplicated in EvidenceRecord. Registry schema 1.1.0 adds this field; registry version 0.1.1-draft used schema 1.0.0.",
    "In the three bidirectional features, the historical reference is the AI pattern as a compatibility convention for historical comparison. This is not a hierarchy of quality between human and AI writing.",
}

REQUIRED_TOP_LEVEL_KEYS = {
    "registry_name",
    "registry_version",
    "schema_version",
    "status",
    "created_date",
    "source_baseline",
    "id_policy",
    "dimensions",
    "cluster_catalog",
    "counts",
    "feature_records",
    "integrity_notes",
    "source_provenance_policy",
}

REQUIRED_DIMENSION_KEYS = {
    "dimension_id",
    "display_name",
    "paper_dimension_code_in_core_map",
    "core_feature_count",
}

REQUIRED_CLUSTER_KEYS = {
    "cluster_id",
    "display_name",
    "display_name_es",
    "origin",
}

REQUIRED_FEATURE_KEYS = {
    "feature_id",
    "canonical_name",
    "dimension_id",
    "paper_dimension_code",
    "paper_dimension_name",
    "cluster_id",
    "measurement_type_source",
    "reference_patterns",
    "historical_reference_pattern_id",
    "research_direction_or_option_source",
    "table16_values_reference",
    "interpretive_caution",
    "source_baseline",
}

REQUIRED_PATTERN_KEYS = {
    "pattern_id",
    "pattern_direction",
    "pattern_label",
    "pattern_level",
    "source_tables",
}

EXPECTED_COUNTS = {
    "core_features": 30,
    "reference_patterns": 33,
    "dimensions": 10,
    "operational_clusters": 8,
}


def load_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle), None
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"cannot read or parse JSON: {exc}"


def _is_nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _validate_object_keys(
    owner: str,
    value: Any,
    required_keys: set[str],
    errors: list[str],
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{owner}: must be a JSON object")
        return False
    missing = required_keys - set(value)
    extra = set(value) - required_keys
    if missing:
        errors.append(f"{owner}: missing keys {sorted(missing)}")
    if extra:
        errors.append(f"{owner}: unexpected keys {sorted(extra)}")
    return not missing and not extra


def validate_registry(registry_path: Path, baseline_path: Path | None = None) -> tuple[list[str], list[str]]:
    """Return ``(errors, checks)`` for the registry at ``registry_path``.

    A baseline is mandatory for a complete validation. If ``baseline_path`` is
    ``None``, the scientific comparison is not performed and the result contains
    an error.
    """
    errors: list[str] = []
    checks: list[str] = []

    data, error = load_json(registry_path)
    if error is not None:
        return [f"registry: {error}"], checks
    if not isinstance(data, dict):
        return ["registry: top-level value must be a JSON object"], checks

    # Top-level structure.
    missing_top = REQUIRED_TOP_LEVEL_KEYS - set(data)
    extra_top = set(data) - REQUIRED_TOP_LEVEL_KEYS
    if missing_top:
        errors.append(f"registry: missing top-level keys {sorted(missing_top)}")
    if extra_top:
        errors.append(f"registry: unexpected top-level keys {sorted(extra_top)}")

    if data.get("registry_name") is not None and not _is_nonempty_str(data.get("registry_name")):
        errors.append("registry: registry_name must be a non-empty string")
    if data.get("registry_version") != "0.1.2-draft":
        errors.append(
            "registry: registry_version must be '0.1.2-draft', "
            f"found {data.get('registry_version')!r}"
        )
    else:
        checks.append("registry_version is 0.1.2-draft")

    if data.get("schema_version") != "1.1.0":
        errors.append(
            "registry: schema_version must be '1.1.0', "
            f"found {data.get('schema_version')!r}"
        )
    else:
        checks.append("schema_version is 1.1.0")

    if data.get("status") != "draft_for_review":
        errors.append(
            "registry: status must be 'draft_for_review', "
            f"found {data.get('status')!r}"
        )
    else:
        checks.append("status is draft_for_review")

    if not _is_nonempty_str(data.get("created_date")):
        errors.append("registry: created_date must be a non-empty string")
    if not isinstance(data.get("source_baseline"), dict) or not data.get("source_baseline"):
        errors.append("registry: source_baseline must be a non-empty object")
    if not isinstance(data.get("id_policy"), dict) or not data.get("id_policy"):
        errors.append("registry: id_policy must be a non-empty object")
    if not isinstance(data.get("source_provenance_policy"), dict) or not data.get("source_provenance_policy"):
        errors.append("registry: source_provenance_policy must be a non-empty object")
    if not isinstance(data.get("integrity_notes"), list) or not all(_is_nonempty_str(note) for note in data.get("integrity_notes", [])):
        errors.append("registry: integrity_notes must be a list of non-empty strings")

    # Dimensions.
    dimensions = data.get("dimensions")
    if not isinstance(dimensions, list) or len(dimensions) != 10:
        errors.append(f"registry: dimensions must be a list of 10, found {dimensions!r}")
        dimensions = []
    else:
        checks.append("10 dimensions")
    dimension_ids: list[str] = []
    for index, dimension in enumerate(dimensions, 1):
        owner = f"dimensions[{index}]"
        if not _validate_object_keys(owner, dimension, REQUIRED_DIMENSION_KEYS, errors):
            continue
        dimension_id = dimension.get("dimension_id")
        display_name = dimension.get("display_name")
        paper_code = dimension.get("paper_dimension_code_in_core_map")
        feature_count = dimension.get("core_feature_count")
        if not _is_nonempty_str(dimension_id):
            errors.append(f"{owner}: dimension_id must be a non-empty string")
            continue
        if dimension_id in dimension_ids:
            errors.append(f"registry: duplicate dimension_id {dimension_id!r}")
        dimension_ids.append(dimension_id)
        if not _is_nonempty_str(display_name):
            errors.append(f"{owner}: display_name must be a non-empty string")
        if paper_code is not None and not _is_nonempty_str(paper_code):
            errors.append(f"{owner}: paper_dimension_code_in_core_map must be a string or null")
        if not isinstance(feature_count, int) or isinstance(feature_count, bool) or feature_count < 0:
            errors.append(f"{owner}: core_feature_count must be a non-negative integer")

    # Operational clusters.
    clusters = data.get("cluster_catalog")
    if not isinstance(clusters, list) or len(clusters) != 8:
        errors.append(f"registry: cluster_catalog must be a list of 8, found {clusters!r}")
        clusters = []
    else:
        checks.append("8 operational clusters")
    cluster_ids: list[str] = []
    for index, cluster in enumerate(clusters, 1):
        owner = f"cluster_catalog[{index}]"
        if not _validate_object_keys(owner, cluster, REQUIRED_CLUSTER_KEYS, errors):
            continue
        cluster_id = cluster.get("cluster_id")
        if not _is_nonempty_str(cluster_id):
            errors.append(f"{owner}: cluster_id must be a non-empty string")
            continue
        if cluster_id in cluster_ids:
            errors.append(f"registry: duplicate cluster_id {cluster_id!r}")
        cluster_ids.append(cluster_id)
        for field in ("display_name", "display_name_es", "origin"):
            if not _is_nonempty_str(cluster.get(field)):
                errors.append(f"{owner}: {field} must be a non-empty string")

    dimension_id_set = set(dimension_ids)
    cluster_id_set = set(cluster_ids)

    # Counts.
    counts = data.get("counts")
    if counts != EXPECTED_COUNTS:
        errors.append(f"registry: counts must equal {EXPECTED_COUNTS!r}, found {counts!r}")
    elif isinstance(counts, dict):
        checks.append("counts are coherent")

    # Feature records.
    features = data.get("feature_records")
    if not isinstance(features, list):
        errors.append("registry: feature_records must be a list")
        features = []
    if len(features) != 30:
        errors.append(f"registry: feature_records must contain 30 entries, found {len(features)}")
    else:
        checks.append("30 feature_records")

    feature_ids: list[str] = []
    historical_refs: list[str] = []
    pattern_ids: set[str] = set()
    duplicate_pattern_ids: set[str] = set()
    ai_unidirectional = 0
    human_unidirectional = 0
    bidirectional = 0
    total_ai_patterns = 0
    total_human_patterns = 0

    for index, feature in enumerate(features, 1):
        if not isinstance(feature, dict):
            errors.append(f"feature #{index}: feature_record must be a JSON object")
            continue

        feature_id = feature.get("feature_id")
        if not _is_nonempty_str(feature_id):
            errors.append(f"feature #{index}: feature_id must be a non-empty string")
            feature_id = f"<feature #{index}>"
        feature_ids.append(feature_id)

        if not _validate_object_keys(feature_id, feature, REQUIRED_FEATURE_KEYS, errors):
            # Continue with available fields; missing keys are already reported.
            pass

        for field in (
            "canonical_name",
            "dimension_id",
            "paper_dimension_code",
            "paper_dimension_name",
            "cluster_id",
            "measurement_type_source",
            "research_direction_or_option_source",
            "table16_values_reference",
            "interpretive_caution",
            "source_baseline",
        ):
            if field in feature and not _is_nonempty_str(feature.get(field)):
                errors.append(f"{feature_id}: {field} must be a non-empty string")

        dimension_id = feature.get("dimension_id")
        if dimension_id not in dimension_id_set:
            errors.append(f"{feature_id}: dimension_id {dimension_id!r} does not exist in dimensions")

        cluster_id = feature.get("cluster_id")
        if cluster_id not in cluster_id_set:
            errors.append(f"{feature_id}: cluster_id {cluster_id!r} does not exist in cluster_catalog")

        patterns = feature.get("reference_patterns")
        if not isinstance(patterns, list) or not patterns:
            errors.append(f"{feature_id}: reference_patterns must be a non-empty list")
            patterns = []

        pattern_map: dict[str, str] = {}
        for pattern_index, pattern in enumerate(patterns, 1):
            owner = f"{feature_id}: reference_patterns[{pattern_index}]"
            if not _validate_object_keys(owner, pattern, REQUIRED_PATTERN_KEYS, errors):
                continue
            pattern_id = pattern.get("pattern_id")
            direction = pattern.get("pattern_direction")
            if not _is_nonempty_str(pattern_id):
                errors.append(f"{owner}: pattern_id must be a non-empty string")
                continue
            if direction not in ALLOWED_PATTERN_DIRECTIONS:
                errors.append(f"{owner}: pattern_direction must be 'pattern_ai' or 'pattern_human', found {direction!r}")
                continue
            if pattern_id in pattern_map:
                errors.append(f"{feature_id}: duplicate pattern_id {pattern_id!r} within the same feature")
            pattern_map[pattern_id] = direction
            if pattern_id in pattern_ids:
                duplicate_pattern_ids.add(pattern_id)
            else:
                pattern_ids.add(pattern_id)
            if not _is_nonempty_str(pattern.get("pattern_label")):
                errors.append(f"{owner}: pattern_label must be a non-empty string")
            if not _is_nonempty_str(pattern.get("pattern_level")):
                errors.append(f"{owner}: pattern_level must be a non-empty string")
            source_tables = pattern.get("source_tables")
            if not isinstance(source_tables, list) or not source_tables or not all(_is_nonempty_str(item) for item in source_tables):
                errors.append(f"{owner}: source_tables must be a non-empty list of non-empty strings")

        ai_candidates = [pid for pid, direction in pattern_map.items() if direction == "pattern_ai"]
        human_candidates = [pid for pid, direction in pattern_map.items() if direction == "pattern_human"]
        total_ai_patterns += len(ai_candidates)
        total_human_patterns += len(human_candidates)

        if "historical_reference_pattern_id" not in feature:
            errors.append(f"{feature_id}: missing historical_reference_pattern_id")
            continue
        historical_ref = feature.get("historical_reference_pattern_id")
        if not _is_nonempty_str(historical_ref):
            errors.append(f"{feature_id}: historical_reference_pattern_id must be a non-empty string")
            continue
        if historical_ref not in pattern_map:
            errors.append(
                f"{feature_id}: historical_reference_pattern_id {historical_ref!r} "
                "does not belong to this feature's reference_patterns"
            )
            continue

        if len(ai_candidates) > 1 or len(human_candidates) > 1:
            errors.append(
                f"{feature_id}: ambiguous historical reference; more than one candidate "
                "pattern exists for the same direction"
            )
            continue

        if ai_candidates:
            expected_ref = ai_candidates[0]
            if human_candidates:
                bidirectional += 1
            else:
                ai_unidirectional += 1
        elif human_candidates:
            expected_ref = human_candidates[0]
            human_unidirectional += 1
        else:
            errors.append(f"{feature_id}: no directional reference pattern is available")
            continue

        if historical_ref != expected_ref:
            if ai_candidates and historical_ref in human_candidates:
                errors.append(
                    f"{feature_id}: historical_reference_pattern_id {historical_ref!r} "
                    "uses the human pattern, but an AI pattern exists; expected "
                    f"{expected_ref!r}"
                )
            elif (not ai_candidates) and historical_ref in ai_candidates:
                errors.append(
                    f"{feature_id}: historical_reference_pattern_id {historical_ref!r} "
                    "uses the AI pattern, but no AI pattern exists; expected "
                    f"{expected_ref!r}"
                )
            else:
                errors.append(
                    f"{feature_id}: historical_reference_pattern_id {historical_ref!r} "
                    f"does not follow the AI-first rule; expected {expected_ref!r}"
                )
            continue

        historical_refs.append(historical_ref)

    # Uniqueness checks.
    if len(feature_ids) != len(set(feature_ids)):
        duplicates = sorted({fid for fid in feature_ids if feature_ids.count(fid) > 1})
        errors.append(f"registry: duplicate feature_id values: {duplicates}")
    else:
        checks.append("30 unique feature_id values")

    if duplicate_pattern_ids:
        errors.append(f"registry: duplicate pattern_id values: {sorted(duplicate_pattern_ids)}")
    elif len(pattern_ids) == 33:
        checks.append("33 unique pattern_id values")
    else:
        errors.append(f"registry: expected 33 unique pattern_id values, found {len(pattern_ids)}")

    if len(historical_refs) == 30 and len(set(historical_refs)) != len(historical_refs):
        duplicates = sorted({ref for ref in historical_refs if historical_refs.count(ref) > 1})
        errors.append(f"registry: duplicate historical_reference_pattern_id values: {duplicates}")
    elif len(historical_refs) == 30:
        checks.append("30 unique historical_reference_pattern_id values")

    # Pattern and feature counts.
    if total_ai_patterns != 20:
        errors.append(f"registry: expected 20 pattern_ai entries, found {total_ai_patterns}")
    else:
        checks.append("20 pattern_ai entries")

    if total_human_patterns != 13:
        errors.append(f"registry: expected 13 pattern_human entries, found {total_human_patterns}")
    else:
        checks.append("13 pattern_human entries")

    if ai_unidirectional != 17:
        errors.append(f"registry: expected 17 unidirectional AI features, found {ai_unidirectional}")
    else:
        checks.append("17 unidirectional AI features")

    if human_unidirectional != 10:
        errors.append(f"registry: expected 10 unidirectional human features, found {human_unidirectional}")
    else:
        checks.append("10 unidirectional human features")

    if bidirectional != 3:
        errors.append(f"registry: expected 3 bidirectional features, found {bidirectional}")
    else:
        checks.append("3 bidirectional features")

    # Cross-check declared counts with actual elements.
    if isinstance(counts, dict):
        if counts.get("core_features") == 30 and len(features) != 30:
            errors.append("registry: counts.core_features does not match the number of feature_records")
        if counts.get("reference_patterns") == 33 and len(pattern_ids) != 33:
            errors.append("registry: counts.reference_patterns does not match the number of unique patterns")
        if counts.get("dimensions") == 10 and len(dimension_ids) != 10:
            errors.append("registry: counts.dimensions does not match the number of dimensions")
        if counts.get("operational_clusters") == 8 and len(cluster_ids) != 8:
            errors.append("registry: counts.operational_clusters does not match the number of clusters")

    # Cross-check declared dimension feature counts.
    for dimension in dimensions if isinstance(dimensions, list) else []:
        if not isinstance(dimension, dict):
            continue
        dimension_id = dimension.get("dimension_id")
        declared_count = dimension.get("core_feature_count")
        if not _is_nonempty_str(dimension_id) or not isinstance(declared_count, int) or isinstance(declared_count, bool):
            continue
        actual_count = sum(
            1 for feature in features
            if isinstance(feature, dict) and feature.get("dimension_id") == dimension_id
        )
        if actual_count != declared_count:
            errors.append(
                f"registry: dimension {dimension_id!r} declares core_feature_count "
                f"{declared_count}, but {actual_count} features use it"
            )

    # Scientific comparison with the baseline registry.
    if baseline_path is None:
        errors.append(
            "registry: scientific comparison requires a baseline registry; "
            "baseline_path is None"
        )
    else:
        baseline, baseline_error = load_json(baseline_path)
        if baseline_error is not None:
            errors.append(f"baseline: {baseline_error}")
        elif not isinstance(baseline, dict):
            errors.append("baseline: top-level value must be a JSON object")
        else:
            compare_scientific(data, baseline, errors, checks)

    return errors, checks


def compare_scientific(candidate: dict[str, Any], baseline: dict[str, Any], errors: list[str], checks: list[str]) -> None:
    """Compare v0.1.2 with v0.1.1, allowing only authorized transition changes."""
    for key, baseline_value in baseline.items():
        if key in AUTHORIZED_TOP_LEVEL_CHANGES or key == "feature_records":
            continue
        if key not in candidate:
            errors.append(f"scientific comparison: missing top-level key {key!r}")
            continue
        if candidate[key] != baseline_value:
            errors.append(f"scientific comparison: top-level key {key!r} changed")

    extra_top_level = set(candidate) - set(baseline) - AUTHORIZED_TOP_LEVEL_CHANGES
    if extra_top_level:
        errors.append(f"scientific comparison: unexpected top-level keys {sorted(extra_top_level)}")

    missing_top_level = set(baseline) - set(candidate) - AUTHORIZED_TOP_LEVEL_CHANGES
    if missing_top_level:
        errors.append(f"scientific comparison: missing top-level keys {sorted(missing_top_level)}")

    # integrity_notes must contain exactly the baseline notes plus the four
    # authorized transition notes, each once. Multiplicity is significant.
    baseline_notes = baseline.get("integrity_notes")
    candidate_notes = candidate.get("integrity_notes")
    if isinstance(baseline_notes, list) and isinstance(candidate_notes, list):
        from collections import Counter

        expected_notes = Counter(baseline_notes)
        for note in AUTHORIZED_INTEGRITY_NOTE_ADDITIONS:
            expected_notes[note] += 1
        if Counter(candidate_notes) != expected_notes:
            unauthorized_notes = [
                note for note in candidate_notes
                if note not in baseline_notes and note not in AUTHORIZED_INTEGRITY_NOTE_ADDITIONS
            ]
            details = ""
            if unauthorized_notes:
                details = f"; unauthorized additions: {unauthorized_notes!r}"
            errors.append(
                "scientific comparison: integrity_notes multiplicity does not match "
                f"the authorized transition{details}"
            )
        else:
            checks.append("baseline integrity_notes preserved")
    else:
        errors.append("scientific comparison: integrity_notes must be a list in both registries")

    baseline_features = baseline.get("feature_records")
    candidate_features = candidate.get("feature_records")
    if not isinstance(baseline_features, list) or not isinstance(candidate_features, list):
        errors.append("scientific comparison: feature_records must be a list in both registries")
        return
    if len(baseline_features) != len(candidate_features):
        errors.append(
            "scientific comparison: feature_records length changed from "
            f"{len(baseline_features)} to {len(candidate_features)}"
        )
        return

    for index, (baseline_feature, candidate_feature) in enumerate(zip(baseline_features, candidate_features), 1):
        if not isinstance(baseline_feature, dict) or not isinstance(candidate_feature, dict):
            errors.append(f"scientific comparison: feature #{index} must be an object in both registries")
            continue

        baseline_id = baseline_feature.get("feature_id", f"<feature #{index}>")
        candidate_id = candidate_feature.get("feature_id", f"<feature #{index}>")
        if baseline_id != candidate_id:
            errors.append(
                f"scientific comparison: feature #{index} changed feature_id from "
                f"{baseline_id!r} to {candidate_id!r}"
            )

        extra_keys = set(candidate_feature) - set(baseline_feature) - AUTHORIZED_EXTRA_FEATURE_KEYS
        if extra_keys:
            errors.append(
                f"{candidate_id}: unexpected feature keys {sorted(extra_keys)}"
            )
        missing_keys = set(baseline_feature) - set(candidate_feature)
        if missing_keys:
            errors.append(f"{candidate_id}: missing feature keys {sorted(missing_keys)}")

        for key, baseline_value in baseline_feature.items():
            if key not in candidate_feature:
                continue
            if candidate_feature[key] != baseline_value:
                errors.append(
                    f"{candidate_id}: scientific field {key!r} changed"
                )

    checks.append("scientific fields preserved against baseline")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help="path to FEATURE_REGISTRY_v0.1.2-draft.json (default: repository location)",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=DEFAULT_BASELINE,
        help="path to FEATURE_REGISTRY_v0.1.1_draft.json for scientific comparison (default: repository location)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print each successful check",
    )
    args = parser.parse_args()

    if not args.registry.is_file():
        print(f"FAIL: registry file not found: {args.registry}")
        return 2
    if args.baseline is not None and not args.baseline.is_file():
        print(f"FAIL: baseline file not found: {args.baseline}")
        return 2

    errors, checks = validate_registry(args.registry, args.baseline)
    if args.verbose:
        for check in checks:
            print(f"OK: {check}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(
        "PASS: FEATURE_REGISTRY_v0.1.2-draft validated; "
        f"{len(checks)} checks passed; 0 failures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())