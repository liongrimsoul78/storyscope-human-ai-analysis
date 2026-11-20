#!/usr/bin/env python3
"""Validate the v0.3 compatibility export documents against each other.

The validator is documentary: it does not implement or simulate the exporter.
It checks that the contract, the mapping matrix and the test vectors agree on
the identifiers and vocabularies they share:

* rule identifiers declared in the contract;
* diagnostic codes (CE-xxx) declared once and used consistently;
* matrix row identifiers, decisions, routes and reversibility classes;
* vector identifiers across the preserved v0.1/v0.2 chain and the v0.3 set;
* coverage: every one of the 70 vectors appears in the coverage table;
* the specific v0.3 decisions (R-04 blocked, TV-03 quarantine, TV-56 route F+,
  no not_observed from a §3 dimension row, reversibility backed by the matrix
  rows for single and multi-reference vectors, and M-55 as a run-level
  provenance condition that does not emit records by itself).

Standard library only. Exit code 0 means PASS.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs" / "design" / "v0.3.0"

CONTRACT = DESIGN / "COMPATIBILITY_EXPORT_CONTRACT_v0.3.md"
MATRIX = DESIGN / "COMPATIBILITY_MAPPING_MATRIX_v0.3.md"
VECTORS = DESIGN / "COMPATIBILITY_TEST_VECTORS_v0.3.md"
VECTORS_V02 = DESIGN / "COMPATIBILITY_TEST_VECTORS_v0.2.md"
VECTORS_V01 = DESIGN / "COMPATIBILITY_TEST_VECTORS_v0.1.md"

CE_RE = re.compile(r"CE-\d{3}")
RULE_RE = re.compile(r"^\| (R-[0-9]{2}[a-z]?|R-D\d{2}|R-F\d{2}) \|", re.M)
MATRIX_ID_RE = re.compile(r"M-\d{2}")
VECTOR_ID_RE = re.compile(r"TV-\d{2}")
HEADING_RE = re.compile(r"^### (TV-\d+) — (.+)$", re.M)

ALLOWED_ROUTES = {"D", "F", "F+", "X"}
ALLOWED_DECISIONS = {
    "conversión fiel",
    "conversión condicionada",
    "preservación sin conversión",
    "conversión no segura",
    "no evaluable con la evidencia disponible",
}
ALLOWED_OUTCOMES = {
    "converted",
    "converted_with_flag",
    "preserved",
    "quarantined",
    "rejected",
}
# Vectors describe a result as a state or as an emitted object; these are the
# signals accepted in addition to the contract outcome words.
RESULT_SIGNALS = ALLOWED_OUTCOMES | {
    "observed",
    "rechazo",
    "conversión permitida",
    "EvidenceRecord",
    "run_level",
    "Presente–alineado",
    "registro",
}

# v0.3 redefines the F+ legacy vectors that changed meaning, and reproduces
# the whole TV-35…TV-56 projection block. TV-01…TV-34 keep their v0.1 text
# except for these revisions.
REVISED_LEGACY = {3, 4, 8, 9, 10, 11, 17, 29, 40}
EXPECTED_V03_VECTORS = sorted(REVISED_LEGACY | set(range(35, 71)))


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checks = 0

    def check(self, condition: bool, message: str) -> None:
        self.checks += 1
        if not condition:
            self.errors.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_contract(text: str) -> dict:
    ce_defs: dict[str, str] = {}
    for code, meaning, action in re.findall(
        r"^\| `(CE-\d{3})` \| (.+?) \| (.+?) \|$", text, re.M
    ):
        ce_defs[code] = f"{meaning} / {action}"

    rules = RULE_RE.findall(text)

    # R-04 must stay blocked.
    r04_lines = [line for line in text.splitlines() if line.startswith("| R-04 |")]
    return {
        "ce": ce_defs,
        "rules": rules,
        "r04": r04_lines[0] if r04_lines else "",
        "has_idempotency_key": "(source_document_sha256, legacy_sublocator)" in text,
        "ce021_informativo": "CE-021` informativo" in text,
    }


def parse_matrix(text: str) -> dict:
    table_a_start = text.index("### 2.2 Tabla A")
    table_b_start = text.index("### 2.3 Tabla B")
    counts_start = text.index("### 2.4 Recuento de decisiones")
    table_a = text[table_a_start:table_b_start]
    table_b = text[table_b_start:counts_start]

    rows_a: dict[str, dict] = {}
    for line in table_a.splitlines():
        if not line.startswith("| M-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 9:
            continue
        rows_a[cells[0]] = {
            "route": cells[1],
            "legacy_field": cells[2],
            "legacy_value": cells[3],
            "legacy_scope": cells[4],
            "legacy_meaning": cells[5],
            "target_field": cells[6],
            "target_value": cells[7],
            "conditions": cells[8],
        }

    rows_b: dict[str, dict] = {}
    for line in table_b.splitlines():
        if not line.startswith("| M-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 9:
            continue
        rows_b[cells[0]] = {
            "evidence": cells[1],
            "span": cells[2],
            "rationale": cells[3],
            "reference": cells[4],
            "loss": cells[5],
            "reversibility": cells[6],
            "decision": cells[7],
            "source": cells[8],
        }

    declared_counts: dict[str, int] = {}
    for line in text[counts_start:].splitlines():
        match = re.match(r"^\| (.+?) \| (M-\d.*?) \| (\d+) \|$", line)
        if match and match.group(1) in ALLOWED_DECISIONS:
            declared_counts[match.group(1)] = int(match.group(3))

    return {"a": rows_a, "b": rows_b, "declared_counts": declared_counts}


def parse_vectors(path: Path) -> dict[str, dict]:
    text = read(path)
    chunks = re.split(r"^### (TV-\d+) — (.+)$", text, flags=re.M)
    vectors: dict[str, dict] = {}
    for index in range(1, len(chunks), 3):
        vid, title, body = chunks[index], chunks[index + 1], chunks[index + 2]

        def field(name: str) -> str:
            match = re.search(
                r"^\| " + re.escape(name) + r" \| (.*?) \|$", body, re.M
            )
            return match.group(1) if match else ""

        vectors[vid] = {
            "title": title,
            "route": field("Ruta"),
            "result": field("Resultado esperado"),
            "reversibility": field("Reversibilidad"),
            "matrix": field("Matriz"),
            "body": body,
        }
    return vectors


REVERSIBILITY_CLASSES = {"A", "B", "C", "D", "—"}


def _components(value: str) -> set[str]:
    return {part.strip() for part in value.split("/") if part.strip()}


def reversibility_checks(
    vid: str,
    vrev: str,
    mats: list[str],
    mrevs: list[str],
    result: str,
) -> list[tuple[bool, str]]:
    """Return the (condition, message) checks for one vector.

    The function is pure so the adversarial tests can exercise the same logic
    the validator runs, without touching the repository documents.
    """
    checks: list[tuple[bool, str]] = []
    vector_components = _components(vrev)
    matrix_components: set[str] = set()
    for mrev in mrevs:
        matrix_components |= _components(mrev)

    # Correspondence: a converted result cannot coexist with —, and vice versa.
    converted_result = (
        "`observed`" in result
        and "quarantined" not in result
        and "rejected" not in result
        and "rechazo" not in result
    )
    if vrev == "—":
        checks.append(
            (
                "quarantined" in result
                or "rejected" in result
                or "rechazo" in result,
                f"{vid}: reversibility — requires a quarantined/rejected result",
            )
        )
    if converted_result:
        checks.append(
            (vrev != "—", f"{vid}: a converted result cannot have reversibility —")
        )

    # — means "no converted record exists": it cannot be combined with a class
    # that presupposes one.
    if "—" in vector_components and len(vector_components) > 1:
        checks.append(
            (
                False,
                f"{vid}: reversibility — cannot be combined with other classes",
            )
        )

    if len(mats) == 1:
        matrix_reversibility = mrevs[0]
        matrix_single = _components(matrix_reversibility)
        if "/" in matrix_reversibility:
            # Composite matrix row: the vector may declare one of its
            # components, but never an unsupported one.
            checks.append(
                (
                    vector_components <= matrix_single,
                    f"{vid}: reversibility {vrev!r} is not a sub-case of "
                    f"{mats[0]} ({matrix_reversibility!r})",
                )
            )
        else:
            checks.append(
                (
                    vrev == matrix_reversibility,
                    f"{vid}: reversibility {vrev!r} disagrees with "
                    f"{mats[0]} ({matrix_reversibility!r})",
                )
            )
    else:
        # Multi-reference vectors are compared component by component against
        # the union of the referenced rows. No component is exempt: in
        # particular, — must be backed by at least one referenced row.
        for component in sorted(vector_components):
            checks.append(
                (
                    component in matrix_components,
                    f"{vid}: reversibility component {component!r} is not "
                    f"supported by its matrix rows {mats}",
                )
            )
        if "—" in vector_components:
            checks.append(
                (
                    "—" in matrix_components,
                    f"{vid}: reversibility — is not backed by any referenced "
                    f"matrix row {mats}",
                )
            )
        # A composite vector cannot claim more distinct classes than its
        # referenced rows provide.
        checks.append(
            (
                len(vector_components) <= len(matrix_components),
                f"{vid}: reversibility {vrev!r} claims more classes than its "
                f"matrix rows {mats} provide ({sorted(matrix_components)})",
            )
        )

    # If every referenced row is —, the vector cannot claim a converted class.
    if matrix_components == {"—"}:
        checks.append(
            (
                vrev == "—",
                f"{vid}: keeps reversibility {vrev!r} while its matrix rows are —",
            )
        )
    return checks


def m55_checks(
    row_a: dict,
    row_b: dict,
    contract_text: str,
    matrix_text: str,
) -> list[tuple[bool, str]]:
    """Return the checks that pin down the M-55 run-level provenance semantics."""
    checks: list[tuple[bool, str]] = [
        (
            row_a["route"] == "X",
            "M-55 must be a run-level (X) condition, not a feature row",
        ),
        (
            "EvidenceRecord" not in row_a["target_field"],
            "M-55 must not emit an EvidenceRecord itself",
        ),
        (
            "run_level" in row_a["target_field"],
            "M-55 must target the run level",
        ),
        (
            "observation_origin" in row_a["target_value"],
            "M-55 must enable EvidenceRecord.observation_origin",
        ),
        (
            "atestación válida" in row_a["conditions"]
            and "§11.6" in row_a["conditions"],
            "M-55 must require a valid migration attestation (§11.6)",
        ),
        (
            row_b["decision"] == "conversión condicionada",
            "M-55 must stay a conditional conversion",
        ),
        (
            row_b["reversibility"].strip() == "B",
            "M-55 must keep reversibility B",
        ),
        (
            "migration_attestations" in contract_text,
            "contract must state that migration_attestations preserves the "
            "external attestation",
        ),
        (
            "no genera `EvidenceRecord`" in contract_text
            or "no genera EvidenceRecord" in contract_text,
            "contract must state that M-55 does not itself generate EvidenceRecords",
        ),
        (
            "attested_origin" in contract_text,
            "contract must document attested_origin",
        ),
        (
            "authorization_status" in contract_text,
            "contract must document authorization_status",
        ),
        (
            "Concordancia entre vías" in contract_text,
            "contract must define concordance between the two provenance paths",
        ),
        (
            "R-29a" in contract_text,
            "contract must declare R-29a for contradicting provenance paths",
        ),
    ]
    return checks


ALLOWED_ATTESTED_ORIGINS = {
    "human_annotation",
    "external_model",
    "independent_tool",
    "authorized_experiment",
}
ATTESTATION_REQUIRED_FIELDS = [
    "legacy_locator",
    "legacy_sublocator",
    "attested_origin",
    "attested_by",
    "attested_at_utc",
    "basis",
    "protocol_version",
    "authorization_status",
]


def _is_utc_iso8601(value: object) -> bool:
    if not isinstance(value, str) or value.strip() == "":
        return False
    text = value.strip()
    if text.endswith("Z") or text.endswith("z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return False
    if parsed.tzinfo is None:
        return False
    return parsed.utcoffset() == timedelta(0)


def attestation_is_structurally_valid(attestation: dict) -> bool:
    """Structural validity of a migration attestation entry (no correspondence)."""
    if not isinstance(attestation, dict) or not attestation:
        return False
    for field_name in ATTESTATION_REQUIRED_FIELDS:
        value = attestation.get(field_name)
        if value is None or str(value).strip() == "":
            return False
    if attestation.get("attested_origin") not in ALLOWED_ATTESTED_ORIGINS:
        return False
    if attestation.get("authorization_status") != "authorized":
        return False
    if not _is_utc_iso8601(attestation.get("attested_at_utc")):
        return False
    return True


_UNSET = object()


def attestation_is_valid(
    attestation: dict,
    expected_locator=_UNSET,
    expected_sublocator=_UNSET,
) -> bool:
    """Single source of truth for attestation validity (used by R-29/M-55).

    Structural validity is always required. When expected locators are supplied,
    exact correspondence with both of them is also required.
    """
    if not attestation_is_structurally_valid(attestation):
        return False
    if expected_locator is _UNSET and expected_sublocator is _UNSET:
        return True
    # Explicit (possibly None) locators: absence fails closed.
    if expected_locator is _UNSET:
        expected_locator = None
    if expected_sublocator is _UNSET:
        expected_sublocator = None
    if expected_locator is None or expected_sublocator is None:
        return False
    if attestation.get("legacy_locator") != expected_locator:
        return False
    if attestation.get("legacy_sublocator") != expected_sublocator:
        return False
    return True


def attestation_checks(
    attestation: dict,
    direct_origin: str | None,
    contract_text: str,
    expected_locator: str | None = None,
    expected_sublocator: str | None = None,
) -> list[tuple[bool, str]]:
    """Validate one migration attestation against the documented rules."""
    checks: list[tuple[bool, str]] = []

    for field_name in ATTESTATION_REQUIRED_FIELDS:
        value = attestation.get(field_name) if isinstance(attestation, dict) else None
        checks.append(
            (
                value is not None and str(value).strip() != "",
                f"attestation field {field_name!r} must be present and non-empty",
            )
        )

    origin = attestation.get("attested_origin") if isinstance(attestation, dict) else None
    checks.append(
        (
            origin in ALLOWED_ATTESTED_ORIGINS,
            f"attested_origin {origin!r} is outside the allowed vocabulary",
        )
    )

    status = attestation.get("authorization_status") if isinstance(attestation, dict) else None
    checks.append(
        (
            status in {"authorized", "not_authorized", "not_applicable"},
            f"authorization_status {status!r} is not a documented value",
        )
    )

    # "not_authorized" invalidates the attestation; "not_applicable" stays pending.
    checks.append(
        (
            status != "not_authorized",
            "authorization_status=not_authorized invalidates the attestation",
        )
    )

    checks.append(
        (
            _is_utc_iso8601(attestation.get("attested_at_utc")) if isinstance(attestation, dict) else False,
            "attested_at_utc must be a valid ISO 8601 timestamp in UTC",
        )
    )

    if expected_locator is not None:
        checks.append(
            (
                (attestation.get("legacy_locator") == expected_locator) if isinstance(attestation, dict) else False,
                "legacy_locator must match the observed record locator",
            )
        )
    if expected_sublocator is not None:
        checks.append(
            (
                (attestation.get("legacy_sublocator") == expected_sublocator) if isinstance(attestation, dict) else False,
                "legacy_sublocator must match the observed record sublocator",
            )
        )

    if direct_origin is not None and attestation:
        checks.append(
            (
                attestation.get("attested_origin") == direct_origin,
                "direct legacy_observation_origin and attested_origin must agree",
            )
        )

    checks.append(
        (
            "Concordancia entre vías" in contract_text,
            "contract must define concordance between the two provenance paths",
        )
    )
    checks.append(
        (
            all(field_name in contract_text for field_name in ATTESTATION_REQUIRED_FIELDS),
            "contract must document every migration_attestations field",
        )
    )
    checks.append(
        (
            "ISO 8601" in contract_text and "UTC" in contract_text,
            "contract must state the ISO 8601 UTC requirement",
        )
    )
    return checks


def provenance_checks(
    direct_origin: str | None,
    attestations,
    contract_text: str,
    expected_locator: str | None = None,
    expected_sublocator: str | None = None,
) -> list[tuple[bool, str]]:
    """Apply R-29/R-29a using a single validity rule for attestations.

    A migration attestation only authorizes the observation whose two expected
    locators are both known and match exactly. When either expected locator is
    missing, the attested path fails closed (no attestation can authorize).

    Conflicts are detected between all valid provenance assertions applicable
    to the same observation: direct declaration versus attestation, and
    attestation versus another attestation. Invalid or pending attestations never
    participate and never substitute a valid one.
    """
    if isinstance(attestations, dict):
        attestations = [attestations] if attestations else []
    attestations = attestations or []

    checks: list[tuple[bool, str]] = []
    has_direct = direct_origin in ALLOWED_ATTESTED_ORIGINS

    locators_known = expected_locator is not None and expected_sublocator is not None
    valid_matching = [
        a for a in attestations
        if locators_known
        and attestation_is_valid(a, expected_locator, expected_sublocator)
    ]

    checks.append(
        (
            has_direct or bool(valid_matching),
            "R-29: at least one valid provenance path is required",
        )
    )

    assertion_origins: list[str] = []
    if has_direct:
        assertion_origins.append(direct_origin)  # type: ignore[arg-type]
    for attestation in valid_matching:
        assertion_origins.append(attestation.get("attested_origin"))

    if len(set(assertion_origins)) > 1:
        checks.append(
            (
                False,
                "R-29a: conflicting provenance assertions for the same observation",
            )
        )
    elif has_direct and valid_matching:
        checks.append(
            (
                all(a.get("attested_origin") == direct_origin for a in valid_matching),
                "R-29a: direct and attested origins must agree",
            )
        )

    if attestations and not valid_matching and not has_direct:
        checks.append((False, "R-29: no attestation satisfies the validity rules"))

    checks.append(
        (
            "R-29a" in contract_text,
            "contract must declare R-29a for contradicting provenance paths",
        )
    )
    return checks


def coverage_ids(text: str) -> list[str]:
    start = text.index("## 5. Cobertura exigida")
    end = text.index("## 6. Criterios de aceptación")
    return VECTOR_ID_RE.findall(text[start:end])


def main() -> int:
    report = Report()

    contract_text = read(CONTRACT)
    matrix_text = read(MATRIX)
    vectors_text = read(VECTORS)

    contract = parse_contract(contract_text)
    matrix = parse_matrix(matrix_text)
    v03 = parse_vectors(VECTORS)
    v02 = parse_vectors(VECTORS_V02)
    v01 = parse_vectors(VECTORS_V01)

    # ---------------------------------------------------------------- contract
    report.check(bool(contract["rules"]), "contract declares no conversion rules")
    report.check(
        len(contract["rules"]) == len(set(contract["rules"])),
        "duplicate rule identifiers in the contract",
    )
    referenced_rules = set(
        re.findall(r"\b(R-[0-9]{2}[a-z]?|R-D\d{2}|R-F\d{2})\b", contract_text)
    )
    report.check(
        referenced_rules <= set(contract["rules"]),
        "contract references undefined rules: "
        f"{sorted(referenced_rules - set(contract['rules']))}",
    )
    report.check(
        "BLOQUEADA" in contract["r04"],
        "R-04 is not marked as blocked in the contract",
    )
    report.check(
        not contract["ce021_informativo"],
        "CE-021 is still used as an informative code; it is reserved for R-04",
    )
    ce021 = contract["ce"].get("CE-021", "")
    report.check(
        "R-04" in ce021 and "cuarentena" in ce021,
        "CE-021 must be defined as the R-04 quarantine code",
    )
    report.check(
        contract["has_idempotency_key"],
        "contract does not state the (source_document_sha256, legacy_sublocator) key",
    )
    for origin in ALLOWED_ATTESTED_ORIGINS:
        report.check(
            origin in contract_text,
            f"contract must list attested_origin value {origin!r}",
        )
    for field_name in ATTESTATION_REQUIRED_FIELDS:
        report.check(
            field_name in contract_text,
            f"contract must document attestation field {field_name!r}",
        )
    report.check(
        "no existe registro convertido" in contract_text,
        "contract must define the — reversibility class",
    )
    report.check(
        len(contract["ce"]) == len(set(contract["ce"])),
        "duplicate CE diagnostic definitions",
    )

    # ------------------------------------------------------------------ matrix
    a, b = matrix["a"], matrix["b"]

    # R-02 must not be applied to route D: it lives only in the F+ rule set.
    report.check(
        contract_text.count("| R-02 |") == 1,
        "R-02 must be declared exactly once, in the F+ rule set",
    )
    report.check(
        "| R-02 | `legacy_direction` ausente o no reconocido en F+" in contract_text,
        "R-02 must be scoped to F+ only",
    )
    report.check(
        "R-D07" in contract["rules"],
        "R-D07 (optional direction in route D) must be declared",
    )
    report.check(bool(a), "matrix Table A has no rows")
    report.check(set(a) == set(b), "matrix Table A and Table B row sets differ")
    report.check(len(a) == 55, f"matrix has {len(a)} rows; expected 55")

    for row_id, row in a.items():
        routes = {part.strip() for part in row["route"].split("/")}
        report.check(
            routes <= ALLOWED_ROUTES,
            f"{row_id}: unknown route {row['route']!r}",
        )
    for row_id, row in b.items():
        report.check(
            row["decision"] in ALLOWED_DECISIONS,
            f"{row_id}: unknown decision {row['decision']!r}",
        )
        classes = {part.strip() for part in row["reversibility"].split("/")}
        report.check(
            classes <= {"A", "B", "C", "D", "—"},
            f"{row_id}: unknown reversibility {row['reversibility']!r}",
        )
        # Reversibility must not contradict the existence of a converted record:
        # "—" is only valid when no EvidenceRecord is emitted.
        emits_record = "EvidenceRecord" in a[row_id]["target_field"]
        if row["reversibility"].strip() == "—":
            report.check(
                not emits_record,
                f"{row_id}: reversibility — but the row emits an EvidenceRecord",
            )
        if emits_record:
            report.check(
                row["reversibility"].strip() != "—",
                f"{row_id}: emits an EvidenceRecord but has no reversibility class",
            )

    # M-04 and M-08 are blocked/quarantined without a destination record.
    for row_id in ("M-04", "M-08"):
        report.check(
            b[row_id]["reversibility"].strip() == "—",
            f"{row_id}: blocked/quarantined row must use reversibility —",
        )

    # M-55: run-level provenance condition, not an EvidenceRecord emitter.
    report.check(
        "M-55" in a and "M-55" in b,
        "matrix must declare M-55 (migration attestation)",
    )
    if "M-55" in a and "M-55" in b:
        for condition, message in m55_checks(a["M-55"], b["M-55"], contract_text, matrix_text):
            report.check(condition, message)

    actual_counts = Counter(row["decision"] for row in b.values())
    report.check(
        dict(actual_counts) == matrix["declared_counts"],
        "matrix decision counts disagree with section 2.4: "
        f"actual={dict(actual_counts)} declared={matrix['declared_counts']}",
    )
    report.check(
        sum(actual_counts.values()) == 55,
        "matrix decision counts do not sum to 55",
    )

    for code in CE_RE.findall(matrix_text):
        report.check(code in contract["ce"], f"matrix uses undefined {code}")
    for code in CE_RE.findall(vectors_text):
        report.check(code in contract["ce"], f"vectors use undefined {code}")

    defined_rules = set(contract["rules"])
    for label, text in (("matrix", matrix_text), ("vectors", vectors_text)):
        for rule in re.findall(r"\b(R-[0-9]{2}[a-z]?|R-D\d{2}|R-F\d{2})\b", text):
            report.check(
                rule in defined_rules,
                f"{label} references undefined rule {rule}",
            )

    # ----------------------------------------------------------------- vectors
    defined_v03 = {int(vid.split("-")[1]) for vid in v03}
    report.check(
        sorted(defined_v03) == EXPECTED_V03_VECTORS,
        "v0.3 vector headings do not match the expected revision set: "
        f"{sorted(defined_v03)}",
    )

    union = set(v01) | set(v02) | set(v03)
    expected_union = {f"TV-{number:02d}" for number in range(1, 71)}
    report.check(
        union == expected_union,
        "vector chain does not cover TV-01…TV-70: "
        f"missing={sorted(expected_union - union)} extra={sorted(union - expected_union)}",
    )

    covered = coverage_ids(vectors_text)
    report.check(
        set(covered) == expected_union,
        "coverage table does not reference every vector: "
        f"missing={sorted(expected_union - set(covered))} "
        f"unknown={sorted(set(covered) - expected_union)}",
    )

    for vid, vector in v03.items():
        for code in CE_RE.findall(vector["body"]):
            report.check(code in contract["ce"], f"{vid}: undefined diagnostic {code}")
        vector_routes = {part.strip() for part in vector["route"].split("/") if part.strip()}
        referenced_routes: set[str] = set()
        for row_id in MATRIX_ID_RE.findall(vector["matrix"]):
            report.check(row_id in a, f"{vid}: unknown matrix row {row_id}")
            if vector_routes and row_id in a:
                matrix_routes = {part.strip() for part in a[row_id]["route"].split("/")}
                referenced_routes |= matrix_routes
                report.check(
                    bool(vector_routes & matrix_routes),
                    f"{vid}: route {vector['route']!r} incompatible with "
                    f"{row_id} route {a[row_id]['route']!r}",
                )
        if vector_routes and referenced_routes:
            report.check(
                vector_routes <= referenced_routes,
                f"{vid}: route {vector['route']!r} is not covered by its matrix rows "
                f"{sorted(referenced_routes)}",
            )

    # TV-03: quarantine only, never in a conversion coverage row.
    tv03 = v03.get("TV-03", {})
    report.check(
        "quarantined" in tv03.get("result", "")
        and "CE-035" in tv03.get("result", ""),
        "TV-03 must remain quarantined with CE-035",
    )
    for line in vectors_text.splitlines():
        if not line.startswith("|") or "TV-03" not in line:
            continue
        label = line.strip().strip("|").split("|")[0].strip()
        report.check(
            "Conversión" not in label and "Preservación" not in label,
            f"TV-03 appears under a non-quarantine coverage row: {label!r}",
        )

    # TV-17 / TV-40: R-04 blocked.
    for vid in ("TV-17", "TV-40"):
        result = v03.get(vid, {}).get("result", "")
        report.check(
            "quarantined" in result and "CE-021" in result,
            f"{vid} must be quarantined with CE-021",
        )

    # TV-56: F+ route and opposed result, consistent with M-09.
    tv56 = v03.get("TV-56", {})
    report.check(
        tv56.get("route", "").strip() == "F+",
        f"TV-56 route is {tv56.get('route')!r}; expected F+",
    )
    report.check(
        "opposed" in tv56.get("result", ""),
        "TV-56 must keep an opposed result consistent with R-09",
    )
    report.check(
        "M-09" in tv56.get("matrix", ""),
        "TV-56 must reference M-09",
    )

    # §3 rows must not emit not_observed / not_applicable / not_evaluable.
    # Negative mentions ("**no** se emite `not_observed`") are allowed; only a
    # positive emission is a contract violation.
    for vid in ("TV-08", "TV-09", "TV-10", "TV-11", "TV-65", "TV-66", "TV-67"):
        result = v03.get(vid, {}).get("result", "")
        report.check(
            "preserved" in result and "coverage_status" in result,
            f"{vid}: a §3 dimension row must be preserved as coverage",
        )
        for state in ("not_observed", "not_applicable", "not_evaluable"):
            positive = (
                result.lstrip().startswith(f"`{state}`")
                or f"→ `{state}`" in result
                or f"= `{state}`" in result
            )
            report.check(
                not positive,
                f"{vid}: a §3 dimension row must not emit {state}",
            )
        # Route D does not require legacy_direction; the vector must say so.
        body = v03.get(vid, {}).get("body", "")
        report.check(
            "legacy_direction" in body,
            f"{vid}: must state that legacy_direction is optional in route D",
        )

    # v0.3 results mention a contract outcome, an emitted object, or a
    # run-level destination. This catches empty or malformed result cells.
    for vid, vector in v03.items():
        result = vector["result"]
        report.check(
            any(token in result for token in RESULT_SIGNALS),
            f"{vid}: result does not mention any contract outcome or destination: "
            f"{result[:80]!r}",
        )

    # ---------------------------------------------------------------- reversibility
    # Precedence of v0.3 definitions over inherited v0.1/v0.2 vectors.
    report.check(
        "prevalece la de v0.3" in vectors_text,
        "vectors document must state that v0.3 definitions take precedence",
    )

    # TV-03, TV-17 and TV-40 are blocked/quarantined: reversibility must be —.
    for vid in ("TV-03", "TV-17", "TV-40"):
        report.check(
            v03.get(vid, {}).get("reversibility", "").strip() == "—",
            f"{vid}: blocked/quarantined vector must use reversibility —",
        )

    for vid, vector in v03.items():
        vrev = vector["reversibility"].strip()
        mats = MATRIX_ID_RE.findall(vector["matrix"])
        if not vrev or not mats:
            continue
        mrevs = [b[m]["reversibility"].strip() for m in mats if m in b]
        if not mrevs:
            continue
        for condition, message in reversibility_checks(
            vid, vrev, mats, mrevs, vector["result"]
        ):
            report.check(condition, message)

    # --------------------------------------------------------- textual hygiene
    for path in (CONTRACT, MATRIX, VECTORS):
        text = read(path)
        for artifact in ("<|", "\u2581", "begin_of_sentence"):
            report.check(
                artifact not in text,
                f"{path.name}: corrupted token {artifact!r} present",
            )

    # ------------------------------------------------------------------ output
    if report.errors:
        for error in report.errors:
            print(f"FAIL: {error}")
        print(f"FAILED: {len(report.errors)} of {report.checks} checks failed.")
        return 1

    print(
        f"PASS: {report.checks} cross-document checks; "
        f"{len(contract['rules'])} rules, {len(contract['ce'])} diagnostics, "
        f"{len(a)} matrix rows, {len(expected_union)} vectors."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
