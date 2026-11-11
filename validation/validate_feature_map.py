#!/usr/bin/env python3
"""Validate the StoryScope v0.2.3 30-feature map against Table 16.

Standard library only. The expected data in ``table16_expected.json`` is a
transcription of the Human, AI and published-gap values in Russell et al.,
StoryScope, arXiv:2604.03136v6, Table 16.

The validator checks:
- exactly 30 feature rows and 30 unique feature names;
- every feature name against the Table 16 transcription;
- Human and AI values for every option;
- the published Human - AI gap;
- the Human/AI direction text and the sign of each gap;
- documented rounding exceptions where the printed gap differs from the
  subtraction of the displayed rounded values.

Table 15 is deliberately not used for these values: it lists the 13 core
human-characterizing features and their response options, but not the means
and gaps of the 30-feature table.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

NUMBER_RE = re.compile(r"[+-]?\d+(?:\.\d+)?")
PAIR_RE = re.compile(r"^(.+?)\s+([+-]?\d+(?:\.\d+)?)\s*(?:%|pp)?$")
VALUE_FIRST_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)\s*(?:%|pp)?\s+(.+)$")
SINGLE_RE = re.compile(r"^([+-]?\d+(?:\.\d+)?)\s*(?:%|pp)?$")


def parse_values(text: str, field: str, feature: str) -> dict[str, float]:
    """Parse '3.28', '57%', 'embodied 38%; explicit labels 29%', etc."""
    text = (text or "").strip()
    if not text:
        raise ValueError(f"{feature}: empty field {field!r}")
    result: dict[str, float] = {}
    for part in (piece.strip() for piece in text.split(";")):
        if not part:
            continue
        part = re.sub(r"\s+pp$", "", part, flags=re.IGNORECASE).strip()
        part = re.sub(r"%$", "", part).strip()
        pair = PAIR_RE.match(part)
        value_first = VALUE_FIRST_RE.match(part)
        if pair:
            label = " ".join(pair.group(1).split()).lower()
            value = float(pair.group(2))
        elif value_first:
            label = " ".join(value_first.group(2).split()).lower()
            value = float(value_first.group(1))
        else:
            single = SINGLE_RE.match(part)
            if not single:
                raise ValueError(f"{feature}: cannot parse {field!r} value {part!r}")
            label = ""
            value = float(single.group(1))
        if label in result:
            raise ValueError(f"{feature}: duplicate option {label!r} in {field!r}")
        result[label] = value
    if not result:
        raise ValueError(f"{feature}: no values parsed from {field!r}")
    return result


def direction_for(feature: dict, option: str) -> str:
    direction = feature["direction"]
    if isinstance(direction, str):
        return direction
    if option not in direction:
        raise ValueError(f"{feature['feature_name']}: no direction for option {option!r}")
    return direction[option]


def close(a: float, b: float, tolerance: float = 0.001) -> bool:
    return abs(a - b) <= tolerance


def align_single_label(values: dict[str, float], expected_labels: set[str]) -> dict[str, float]:
    """Allow an unlabeled field when the feature has one named option.

    Example: the gap field is ``-26 pp`` while the Human/AI fields name the
    single option ``olfactory``. The gap still belongs to that option.
    """
    if set(values) == {""} and len(expected_labels) == 1 and "" not in expected_labels:
        return {next(iter(expected_labels)): values[""]}
    return values


def load_expected(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    features = data.get("features")
    if not isinstance(features, list):
        raise ValueError("expected JSON has no features list")
    if data.get("feature_count") != len(features):
        raise ValueError("expected JSON feature_count does not match features length")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true", help="list every feature check")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    csv_path = skill_root / "references" / "feature-dimension-map.csv"
    expected_path = skill_root / "validation" / "table16_expected.json"

    errors: list[str] = []
    for path in (csv_path, expected_path):
        if not path.is_file():
            print(f"FAIL: missing file: {path}")
            return 2

    try:
        expected = load_expected(expected_path)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: invalid expected JSON: {exc}")
        return 2

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    required_columns = {
        "feature_name",
        "research_direction_or_option",
        "human_value_or_prevalence",
        "ai_value_or_prevalence",
        "paper_gap_human_minus_ai_or_note",
    }
    missing_columns = required_columns - set(fieldnames)
    if missing_columns:
        errors.append(f"CSV missing columns: {sorted(missing_columns)}")

    if len(rows) != 30:
        errors.append(f"expected 30 feature rows, found {len(rows)}")

    csv_names = [row.get("feature_name", "") for row in rows]
    if len(set(csv_names)) != len(csv_names):
        errors.append("duplicate feature_name values found in CSV")
    if len(csv_names) != len(set(csv_names)):
        errors.append("CSV feature names are not unique")

    expected_names = [feature["feature_name"] for feature in expected["features"]]
    if len(set(expected_names)) != len(expected_names):
        errors.append("expected JSON feature names are not unique")
    if set(csv_names) != set(expected_names):
        missing = sorted(set(expected_names) - set(csv_names))
        extra = sorted(set(csv_names) - set(expected_names))
        if missing:
            errors.append(f"features missing from CSV: {missing}")
        if extra:
            errors.append(f"unexpected features in CSV: {extra}")

    by_name = {row.get("feature_name", ""): row for row in rows}
    option_checks = 0
    rounding_exceptions = 0

    for feature in expected["features"]:
        name = feature["feature_name"]
        row = by_name.get(name)
        if row is None:
            continue

        direction_text = row.get("research_direction_or_option", "").strip()
        if direction_text != feature["direction_text"]:
            errors.append(
                f"{name}: direction text expected {feature['direction_text']!r}, "
                f"found {direction_text!r}"
            )

        try:
            human = parse_values(row.get("human_value_or_prevalence", ""), "human", name)
            ai = parse_values(row.get("ai_value_or_prevalence", ""), "ai", name)
            gaps = parse_values(row.get("paper_gap_human_minus_ai_or_note", ""), "gap", name)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        expected_options = {option["option"]: option for option in feature["options"]}
        expected_labels = set(expected_options)
        human = align_single_label(human, expected_labels)
        ai = align_single_label(ai, expected_labels)
        gaps = align_single_label(gaps, expected_labels)
        if set(human) != set(expected_options):
            errors.append(f"{name}: Human options {sorted(human)} != expected {sorted(expected_options)}")
            continue
        if set(ai) != set(expected_options):
            errors.append(f"{name}: AI options {sorted(ai)} != expected {sorted(expected_options)}")
            continue
        if set(gaps) != set(expected_options):
            errors.append(f"{name}: gap options {sorted(gaps)} != expected {sorted(expected_options)}")
            continue

        for option_name, option in expected_options.items():
            option_checks += 1
            label = option_name or "(single value)"
            if not close(human[option_name], option["human"]):
                errors.append(
                    f"{name} [{label}]: Human expected {option['human']}, found {human[option_name]}"
                )
            if not close(ai[option_name], option["ai"]):
                errors.append(
                    f"{name} [{label}]: AI expected {option['ai']}, found {ai[option_name]}"
                )
            if not close(gaps[option_name], option["gap"]):
                errors.append(
                    f"{name} [{label}]: published gap expected {option['gap']}, "
                    f"found {gaps[option_name]}"
                )

            direction = direction_for(feature, option_name)
            if direction == "AI" and gaps[option_name] >= 0:
                errors.append(f"{name} [{label}]: AI direction but non-negative gap {gaps[option_name]}")
            if direction == "Human" and gaps[option_name] <= 0:
                errors.append(f"{name} [{label}]: Human direction but non-positive gap {gaps[option_name]}")

            arithmetic_gap = round(human[option_name] - ai[option_name], 2)
            documented = option.get("arithmetic_gap")
            if documented is None:
                if not close(arithmetic_gap, option["gap"]):
                    errors.append(
                        f"{name} [{label}]: arithmetic gap {arithmetic_gap} != published gap "
                        f"{option['gap']} without a documented rounding exception"
                    )
            else:
                rounding_exceptions += 1
                if not close(arithmetic_gap, documented):
                    errors.append(
                        f"{name} [{label}]: documented arithmetic gap {documented} != "
                        f"computed {arithmetic_gap}"
                    )
                if close(arithmetic_gap, option["gap"]):
                    errors.append(
                        f"{name} [{label}]: rounding exception is unnecessary; "
                        f"arithmetic gap equals published gap {option['gap']}"
                    )
                if not option.get("rounding_note"):
                    errors.append(f"{name} [{label}]: rounding exception has no note")

        if args.verbose:
            print(f"OK: {name}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(
        f"PASS: {len(rows)} features, {option_checks} option-level checks, "
        f"{len(set(csv_names))} unique names, {rounding_exceptions} documented rounding exceptions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
