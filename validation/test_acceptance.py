#!/usr/bin/env python3
"""Positive and negative acceptance tests for StoryScope v0.2.3.

Run from the Skill root:

    py -3 .\validation\test_acceptance.py

The tests copy the Skill to temporary directories for negative controls, so
the installed or build copy is never modified.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
CSV_REL = Path("references") / "feature-dimension-map.csv"


def run_script(root: Path, relative: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, str(root / relative), *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def read_csv(root: Path) -> tuple[list[str], list[dict[str, str]]]:
    with (root / CSV_REL).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(root: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with (root / CSV_REL).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def copy_skill(destination: Path) -> Path:
    target = destination / "storyscope-human-ai-analysis"
    shutil.copytree(ROOT, target)
    return target


class PositiveAcceptance(unittest.TestCase):
    def test_validator_passes(self) -> None:
        result = run_script(ROOT, "validation/validate_feature_map.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS: 30 features", result.stdout)
        self.assertIn("33 option-level checks", result.stdout)
        self.assertIn("9 documented rounding exceptions", result.stdout)

    def test_source_check_passes_by_name_and_option(self) -> None:
        result = run_script(ROOT, "validation/check_source_table16.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("30 features and 33 options", result.stdout)
        self.assertIn("matched by name and value", result.stdout)
        self.assertIn("0 mismatches", result.stdout)

    def test_readme_install_uses_git_clone(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        install = readme.split("## Instalación", 1)[1].split("## Uso", 1)[0]
        self.assertIn("git clone", install)
        self.assertIn("storyscope-human-ai-analysis", install)
        self.assertIn("opencode", install.lower())
        self.assertNotIn("Expand-Archive", install)
        self.assertNotIn(".zip", install)
        self.assertNotIn(r"C:\LION-LAB", readme)

    def test_manifest_passes_strict(self) -> None:
        result = run_script(ROOT, "validation/verify_manifest.py", "--strict")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 failures", result.stdout)

    def test_version_metadata(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        research = (ROOT / "references" / "research-basis.md").read_text(encoding="utf-8")
        template = (ROOT / "references" / "report-template.md").read_text(encoding="utf-8")
        self.assertRegex(skill, r'version:\s*"0\.2\.3"')
        self.assertIn("v0.2.3", readme.splitlines()[0])
        self.assertIn("## 0.2.3", changelog)
        self.assertIn("revisión v0.2.3", research.splitlines()[0])
        self.assertIn("v0.2.3", template.splitlines()[0])
        self.assertIn("English instructions", skill)
        self.assertIn("Spanish documentation", skill)
        frontmatter = skill.split("---", 2)[1]
        version_lines = [
            line for line in frontmatter.splitlines() if line.strip().startswith("version:")
        ]
        language_lines = [
            line for line in frontmatter.splitlines() if line.strip().startswith("language:")
        ]
        self.assertEqual(len(version_lines), 1, version_lines)
        self.assertEqual(len(language_lines), 1, language_lines)

    def test_five_v022_values_remain_correct(self) -> None:
        _, rows = read_csv(ROOT)
        by_name = {row["feature_name"]: row for row in rows}
        expected = {
            "Frequency of Direct Reader Address": ("0.28", "0.07", "+0.21"),
            "Fourth-Wall Permeability": ("0.67", "0.39", "+0.28"),
            "Location Variety Scope": ("1.34", "1.08", "+0.26"),
            "Moral Polarity Toward Protagonist": ("59%", "38%", "+21 pp"),
            "Nonlinear Framing for Delayed Disclosure": ("1.96", "1.68", "+0.28"),
        }
        for name, values in expected.items():
            row = by_name[name]
            actual = (
                row["human_value_or_prevalence"],
                row["ai_value_or_prevalence"],
                row["paper_gap_human_minus_ai_or_note"],
            )
            self.assertEqual(actual, values, name)

    def test_reference_balanced_mix_corrected(self) -> None:
        _, rows = read_csv(ROOT)
        row = next(r for r in rows if r["feature_name"] == "Reference Explicitness")
        self.assertIn("balanced mix 37%", row["human_value_or_prevalence"])
        self.assertIn("balanced mix 16%", row["ai_value_or_prevalence"])
        self.assertIn("balanced mix +21", row["paper_gap_human_minus_ai_or_note"])

    def test_gate_typo_absent_and_thresholds_present(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized = skill.replace("–", "-").replace("—", "-")
        self.assertNotIn("300/500", normalized)
        self.assertNotIn("300/1,000", normalized)
        self.assertIn("Fewer than 500 words", normalized)
        self.assertIn("500-999 words", normalized)
        self.assertIn("1,000 words or more", normalized)

    def test_table_15_is_not_cited_for_numeric_values(self) -> None:
        offenders = []
        # Data-like values: two-decimal means or percentages. Version strings
        # such as v0.2.3 are deliberately excluded by the negative lookbehind.
        data_value = re.compile(r"(?<!v)\b\d+\.\d{2}\b|\b\d+%")
        for path in ROOT.rglob("*.md"):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "Tabla 15" in line or "Table 15" in line:
                    if data_value.search(line):
                        offenders.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
        self.assertEqual(offenders, [], "\n".join(offenders))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Tabla 16", readme)

    def test_no_broken_internal_references(self) -> None:
        missing = []
        pattern = re.compile(r"(?:`|\]\()(references/[^`)\s]+|validation/[^`)\s]+)")
        for path in ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for match in pattern.finditer(text):
                relative = match.group(1).rstrip("`")
                if not (ROOT / relative).exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {relative}")
        self.assertEqual(missing, [], "\n".join(missing))

    def test_calibration_example_still_insufficient(self) -> None:
        path = ROOT / "references" / "worked-examples" / "01-microrelato-21-palabras.md"
        text = path.read_text(encoding="utf-8")
        block = re.search(r"(?m)^> (.+)$", text)
        self.assertIsNotNone(block)
        words = re.findall(r"\S+", block.group(1))
        self.assertEqual(len(words), 21)
        self.assertIn("Etiqueta global: **evidencia insuficiente**", text)
        self.assertIn("Confianza en la calidad del perfil de autoría: baja", text)
        self.assertIn("No concluir", text)
        self.assertIn("mixto con inclinación IA", text)
        self.assertIn("No fabricar porcentaje ni probabilidad de autoría", text)

    def test_no_authorship_probability_generated(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        template = (ROOT / "references" / "report-template.md").read_text(encoding="utf-8")
        example = (ROOT / "references" / "worked-examples" / "01-microrelato-21-palabras.md").read_text(encoding="utf-8")
        self.assertIn("No invented probabilities", skill)
        self.assertIn("no es prueba de autoría", template)
        self.assertIn("No fabricar porcentaje ni probabilidad de autoría", example)
        self.assertNotIn("posterior probability:", skill.lower())


class NegativeAcceptance(unittest.TestCase):
    def test_negative_five_value_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            fields, rows = read_csv(root)
            row = next(r for r in rows if r["feature_name"] == "Frequency of Direct Reader Address")
            row["human_value_or_prevalence"] = "0.07"
            row["ai_value_or_prevalence"] = "0.28"
            row["paper_gap_human_minus_ai_or_note"] = "-0.21"
            write_csv(root, fields, rows)
            result = run_script(root, "validation/validate_feature_map.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Frequency of Direct Reader Address", result.stdout)

    def test_negative_nonfive_value_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            fields, rows = read_csv(root)
            row = next(r for r in rows if r["feature_name"] == "Location Variety Scope")
            row["human_value_or_prevalence"] = "1.08"
            row["ai_value_or_prevalence"] = "1.34"
            row["paper_gap_human_minus_ai_or_note"] = "-0.26"
            write_csv(root, fields, rows)
            result = run_script(root, "validation/validate_feature_map.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Location Variety Scope", result.stdout)

    def test_negative_reference_balanced_regression(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            fields, rows = read_csv(root)
            row = next(r for r in rows if r["feature_name"] == "Reference Explicitness")
            row["human_value_or_prevalence"] = "implicit echoes 50%; balanced mix 16%"
            row["ai_value_or_prevalence"] = "implicit echoes 72%; balanced mix 37%"
            write_csv(root, fields, rows)
            result = run_script(root, "validation/validate_feature_map.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Reference Explicitness", result.stdout)

    def test_negative_duplicate_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            fields, rows = read_csv(root)
            rows[1]["feature_name"] = rows[0]["feature_name"]
            write_csv(root, fields, rows)
            result = run_script(root, "validation/validate_feature_map.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate", result.stdout.lower())

    def test_negative_missing_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            fields, rows = read_csv(root)
            write_csv(root, fields, rows[:-1])
            result = run_script(root, "validation/validate_feature_map.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("30", result.stdout)

    def test_negative_direction_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            fields, rows = read_csv(root)
            row = next(r for r in rows if r["feature_name"] == "Thematic Explicitness and Moralizing")
            row["research_direction_or_option"] = "Human"
            write_csv(root, fields, rows)
            result = run_script(root, "validation/validate_feature_map.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("direction text", result.stdout)

    def test_negative_gap_sign_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            fields, rows = read_csv(root)
            row = next(r for r in rows if r["feature_name"] == "Thematic Explicitness and Moralizing")
            row["paper_gap_human_minus_ai_or_note"] = "+0.65"
            write_csv(root, fields, rows)
            result = run_script(root, "validation/validate_feature_map.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Thematic Explicitness and Moralizing", result.stdout)

    def test_negative_removed_rounding_exception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            path = root / "validation" / "table16_expected.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            feature = next(f for f in data["features"] if f["feature_name"] == "Thematic Explicitness and Moralizing")
            feature["options"][0].pop("arithmetic_gap", None)
            feature["options"][0].pop("rounding_note", None)
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            result = run_script(root, "validation/validate_feature_map.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("without a documented rounding exception", result.stdout)

    def test_negative_source_value_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            path = root / "validation" / "table16_expected.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            feature = next(
                f for f in data["features"] if f["feature_name"] == "Thematic Unity"
            )
            feature["options"][0]["human"] = 4.40
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            result = run_script(root, "validation/check_source_table16.py")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("value mismatch", result.stdout)
            self.assertIn("Thematic Unity", result.stdout)

    def test_negative_manifest_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            readme = root / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            result = run_script(root, "validation/verify_manifest.py", "--strict")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("README.md", result.stdout)

    def test_negative_unlisted_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_skill(Path(tmp))
            (root / "unlisted.txt").write_text("unexpected\n", encoding="utf-8")
            result = run_script(root, "validation/verify_manifest.py", "--strict")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unlisted file", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
