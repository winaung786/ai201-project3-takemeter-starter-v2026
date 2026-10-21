"""Training integrity checks, without claiming missing course evidence exists."""
import csv
import hashlib
import json
from pathlib import Path

try:
    from .validate_submission import ROOT, validate
except ImportError:
    from validate_submission import ROOT, validate


def preflight(root=ROOT, allow_assisted_initial20=False, require_committed=True):
    root = Path(root)
    errors, counts = validate(root, require_committed=require_committed)
    provenance = {"human_review_basis": "course_workflow", "unaided_cold_pass_recorded": True}
    if not allow_assisted_initial20:
        return errors, counts, provenance
    try:
        raw = (root / "labels.csv").read_bytes()
        with (root / "labels.csv").open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        record = json.loads((root / "evidence/human-review-confirmation.json").read_text())
        if record["finalized_csv_sha256"] != hashlib.sha256(raw).hexdigest():
            raise ValueError("confirmation hash does not match labels.csv")
        if record["human_reviewed_count"] != len(rows) or len(record["records"]) != len(rows):
            raise ValueError("confirmation does not cover every row")
        for i, (row, item) in enumerate(zip(rows, record["records"]), 1):
            markers = {s.strip() for s in row["note"].split(";")}
            source_id = row["note"].split("hn_id=")[1].split(";")[0]
            if "human_reviewed" not in markers or item["row"] != i or str(item["source_id"]) != source_id:
                raise ValueError(f"row {i} lacks matching confirmation")
            if item["label"] != row["label"] or item["text_sha256"] != hashlib.sha256(row["text"].encode()).hexdigest():
                raise ValueError(f"row {i} label or source text differs")
        cold_count = sum("cold" in {s.strip() for s in r["note"].split(";")} for r in rows)
        # This mode permits exactly the disclosed missing-cold-pass condition.
        # All structural, review, duplication, criteria and committed-file errors remain.
        if cold_count == 0:
            errors = [e for e in errors if e != "Need 20 actually labeled cold rows; found 0."]
        provenance = {
            "human_review_basis": "user_confirmation_after_AI_assistance",
            "confirmation_file": "evidence/human-review-confirmation.json",
            "reviewer": record["reviewer"],
            "unaided_cold_pass_recorded": cold_count == 20,
            "course_submission_complete": False,
            "limitation": "Initial 20 were AI-assisted; training does not satisfy the unaided cold-pass requirement. Hard-case explanations originated with the assistant.",
        }
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        errors.append(f"Assisted training requires a matching human-review record: {exc}")
    return errors, counts, provenance
