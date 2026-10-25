"""Validate the student's blind 30-row annotation before using the staff key."""
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    with (ROOT / "data/staff_post_texts.csv").open(newline="") as f:
        posts = list(csv.DictReader(f))
    with (ROOT / "my_staff_labels.csv").open(newline="") as f:
        mine = list(csv.DictReader(f))
    if len(mine) != 30 or [r["text"] for r in mine] != [r["text"] for r in posts]:
        raise SystemExit("Keep all 30 staff posts unchanged and in their original order.")
    invalid = [i for i, r in enumerate(mine, 1) if r["label"] not in {"analysis", "hot_take", "reaction"}]
    if invalid:
        raise SystemExit(f"Student labels still missing or invalid at rows {invalid}. Fill these independently before opening the key.")
    provenance_path = ROOT / "evidence/unit6/staff-labels-provenance.json"
    if provenance_path.exists():
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        if provenance.get("independent_student_labels") is False:
            raise SystemExit("These labels are recorded as AI-assisted. They cannot be counted as independent student agreement. With the authentic TF key, agreement.py can produce an AI-to-staff diagnostic; retain the authorship disclosure.")
    committed = subprocess.run(["git", "show", "HEAD:my_staff_labels.csv"], cwd=ROOT, capture_output=True)
    if committed.returncode or committed.stdout != (ROOT / "my_staff_labels.csv").read_bytes():
        raise SystemExit("Commit the completed blind labels before using the staff key.")
    if not (ROOT / "data/staff_labels.csv").exists():
        raise SystemExit("Get data/staff_labels.csv from the TF now that your own labels are saved.")
    with (ROOT / "data/staff_labels.csv").open(newline="") as f:
        reference = list(csv.DictReader(f))
    ids = [r["id"] for r in reference]
    if len(ids) != 30 or len(set(ids)) != 30 or set(ids) != {r["id"] for r in posts}:
        raise SystemExit("The TF key must contain exactly one answer for each of the 30 staff post IDs.")
    column = next((c for c in ["label", "staff_label", "my_label", "your_label"] if reference and c in reference[0]), None)
    if column is None or any(r[column] not in {"analysis", "hot_take", "reaction"} for r in reference):
        raise SystemExit("The TF reference must use the exact staff taxonomy label strings.")
    frozen_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    subprocess.run([sys.executable, "agreement.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "agreement_results.json").read_text())
    if result["compared"] != 30 or result["staff_posts_not_in_mine"]:
        raise SystemExit("Agreement must cover every one of the 30 posts.")
    evidence = {"student_labels_committed_at": frozen_commit,
        "student_labels_sha256": hashlib.sha256((ROOT / "my_staff_labels.csv").read_bytes()).hexdigest(),
        "reference_sha256": hashlib.sha256((ROOT / "data/staff_labels.csv").read_bytes()).hexdigest(),
        "full_30_rows_compared": True,
        "student_adjudications_still_required": bool(result["disagreements"])}
    (ROOT / "evidence/unit6/staff-comparison-inputs.json").write_text(json.dumps(evidence, indent=2) + "\n")
    worksheet = ROOT / "docs/unit6/staff-disagreements.md"
    if not worksheet.exists():
        lines = ["# Student adjudication worksheet", "", f"Measured agreement: {result['agreed']}/30 ({result['agreement_rate']:.1%}).", "",
                 "For each disagreement, write your own call and reason using a staff rule, then choose pile a, b, or c. The blank fields are not completed adjudications.", ""]
        for i, row in enumerate(result["disagreements"], 1):
            lines += [f"## Disagreement {i}", "", row["text"], "", f"Staff: `{row['staff']}`. Student: `{row['mine']}`.", "", "Student call and rule-based reason: **PENDING**", "", "Pile: **PENDING**", ""]
        worksheet.write_text("\n".join(lines))
    print("Add your own reasoned call and one of the three piles for every disagreement.")


if __name__ == "__main__":
    main()
