#!/usr/bin/env python3
"""Independently verify the 30 features and 33 options against Table 16.

This checker reads ``validation/source_table16_v6.txt``, a verbatim extract of
Table 16 from the versioned arXiv 2604.03136v6 HTML rendering, and compares
each source feature/option with its corresponding entry in
``validation/table16_expected.json``.

Unlike a multiset comparison of Human/AI/Gap triples, this check requires the
feature name and option name to match. Duplicate triples cannot satisfy two
different features, and a value attached to the wrong feature or option fails.

Run from the Skill root:

    py -3 .\\validation\\check_source_table16.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "validation" / "source_table16_v6.txt"
EXPECTED = ROOT / "validation" / "table16_expected.json"

NUMBER_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?%?$")
TRAILING_KIND_RE = re.compile(r"\s+[so]$")

# The HTML table uses shortened or grammatically different labels. Each alias
# maps a source label to the canonical name used by the Skill and the JSON.
FEATURE_ALIASES = {
    "Thematic Explicitness & Moralizing": "Thematic Explicitness and Moralizing",
    "Moral / Philosophical Weighting": "Moral / Philosophical Weighting",
    "Thematic Unity": "Thematic Unity",
    "Narratorial Thematic Commentary": "Narratorial Thematic Commentary",
    "Dialogue Function": "Dialogue Function",
    "Reference Explicitness": "Reference Explicitness",
    "Emotional Expression": "Dominant Emotional Expression",
    "Setting as Psychological Mirror": "Setting as Psychological Mirror",
    "Environmental & Ecological Emphasis": "Environmental and Ecological Emphasis",
    "Sensory Modalities": "Dominant Sensory Modalities",
    "Sensory Density": "Sensory Density",
    "Depth of Interior Access": "Depth of Interior Access",
    "Causal Chain Continuity": "Continuity of Main Causal Chain",
    "Spatial Granularity": "Spatial Granularity Level",
    "Agency in Resolution": "Agency in Resolution",
    "Character Introduction": "Character Introduction",
    "Subplot Integration": "Subplot Integration",
    "Resolution Mode": "Mode of Resolution",
    "Opening Spatial Grounding": "Opening Spatial Grounding",
    "Pre-Threat Character Investment": "Pre-Threat Character Investment",
    "Intertextual Strategy": "Intertextual Strategy Types",
    "Fourth-Wall Permeability": "Fourth-Wall Permeability",
    "Direct Reader Address": "Frequency of Direct Reader Address",
    "Depth of Recontextualization After Surprise": "Depth of Recontextualization After Surprise",
    "Chronological Discontinuity": "Degree of Chronological Discontinuity",
    "Nonlinear Framing for Delayed Disclosure": "Nonlinear Framing for Delayed Disclosure",
    "Anachrony Intensity": "Anachrony Intensity",
    "Location Variety Scope": "Location Variety Scope",
    "Dialogue-to-Narration Proportion": "Dialogue-to-Narration Proportion",
    "Moral Polarity": "Moral Polarity Toward Protagonist",
}

# For features represented by a single summarized value in the Skill, the
# source names the winning response option but the canonical option is empty.
SINGLE_VALUE_OPTIONS = {
    ("Dialogue Function", "philosophical debate"): "",
    ("Character Introduction", "external description"): "",
    ("Mode of Resolution", "internal understanding"): "",
    ("Intertextual Strategy Types", "explicit named reference"): "",
    ("Moral Polarity Toward Protagonist", "ambivalent/mixed"): "",
}


def clean_number(line: str) -> str:
    return line.replace("−-", "-").replace("−", "-").replace("%", "").strip()


def is_number(line: str) -> bool:
    return bool(NUMBER_RE.match(clean_number(line)))


def parse_source(path: Path) -> list[tuple[str, str, float, float, float]]:
    lines = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    rows: list[tuple[str, str, float, float, float]] = []
    i = 0
    while i < len(lines):
        label = lines[i]
        if (
            label in {"Feature", "Human", "AI", "Gap"}
            or label.startswith(("AI-elevated:", "Human-elevated:", "Table 16:"))
            or is_number(label)
        ):
            i += 1
            continue

        if i + 3 >= len(lines) or not all(is_number(lines[i + 1 + n]) for n in range(3)):
            raise ValueError(f"source row without three numeric values: {label!r}")
        if "→" in label:
            feature_part, option_part = label.split("→", 1)
            option = option_part.replace("\\rightarrow", "").strip()
        else:
            feature_part, option = label, ""
        feature = TRAILING_KIND_RE.sub("", feature_part.strip())
        rows.append(
            (
                feature,
                option,
                float(clean_number(lines[i + 1])),
                float(clean_number(lines[i + 2])),
                float(clean_number(lines[i + 3])),
            )
        )
        i += 4
    return rows


def main() -> int:
    for path in (SOURCE, EXPECTED):
        if not path.is_file():
            print(f"FAIL: missing file: {path}")
            return 2

    try:
        source_rows = parse_source(SOURCE)
    except ValueError as exc:
        print(f"FAIL: cannot parse source extract: {exc}")
        return 2

    data = json.loads(EXPECTED.read_text(encoding="utf-8"))
    expected: dict[tuple[str, str], tuple[float, float, float]] = {}
    for feature in data["features"]:
        for option in feature["options"]:
            key = (feature["feature_name"], option["option"])
            if key in expected:
                print(f"FAIL: duplicate expected key: {key}")
                return 1
            expected[key] = (float(option["human"]), float(option["ai"]), float(option["gap"]))

    errors: list[str] = []
    seen: dict[tuple[str, str], tuple[float, float, float]] = {}
    for source_feature, source_option, human, ai, gap in source_rows:
        canonical_feature = FEATURE_ALIASES.get(source_feature)
        if canonical_feature is None:
            errors.append(f"unmapped source feature: {source_feature!r}")
            continue
        canonical_option = SINGLE_VALUE_OPTIONS.get(
            (canonical_feature, source_option), source_option
        )
        key = (canonical_feature, canonical_option)
        if key in seen:
            errors.append(f"duplicate source key: {key}")
            continue
        seen[key] = (human, ai, gap)

    missing = sorted(set(expected) - set(seen))
    extra = sorted(set(seen) - set(expected))
    for key in missing:
        errors.append(f"missing from source: {key}")
    for key in extra:
        errors.append(f"unexpected in source: {key}")

    for key in sorted(set(expected) & set(seen)):
        if expected[key] != seen[key]:
            errors.append(
                f"value mismatch for {key[0]} [{key[1] or '(single value)'}]: "
                f"source {seen[key]} != JSON {expected[key]}"
            )

    feature_count = len({key[0] for key in expected})
    if feature_count != 30:
        errors.append(f"expected 30 features, found {feature_count}")
    if len(expected) != 33:
        errors.append(f"expected 33 options, found {len(expected)}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(
        f"PASS: 30 features and 33 options matched by name and value "
        f"against {SOURCE.name}; 0 mismatches."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
