"""Fail early on unreviewed data or blank criteria; never trains or splits data."""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    labels = json.loads((root / "docs/label-map.json").read_text())
    with (root / "labels.csv").open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["text", "label", "note"]:
            return ["CSV columns must be exactly text,label,note in this project."], {}
        rows = list(reader)
    if len(rows) < 200:
        errors.append(f"Only {len(rows)} rows; use 200 or document the course's stop rule.")
    blanks = sum(not r["label"].strip() for r in rows)
    if blanks:
        errors.append(f"{blanks} rows have no label. Collection is not annotation.")
    unknown = sorted({r["label"] for r in rows if r["label"] and r["label"] not in labels})
    if unknown:
        errors.append(f"Unknown labels: {unknown}")
    if any(not r["text"].strip() for r in rows):
        errors.append("Blank post text.")
    normalized = [re.sub(r"\s+", " ", r["text"]).casefold().strip() for r in rows]
    if len(normalized) != len(set(normalized)):
        errors.append("Duplicate normalized post text would leak between splits.")
    counts = Counter(r["label"] for r in rows if r["label"])
    for label in labels:
        if counts[label] < 20:
            errors.append(f"{label} has only {counts[label]} labeled posts; collect or label more.")
        if rows and counts[label] / len(rows) > .70:
            errors.append(f"{label} exceeds the 70% cap.")
    cold = [r for r in rows if "cold" in {x.strip() for x in r["note"].split(";")}]
    if len(cold) != 20 or any(not r["label"] for r in cold):
        errors.append(f"Need 20 actually labeled cold rows; found {len(cold)}.")
    pending = sum(any(x in r["note"] for x in ("cold_pending", "unlabeled", "review_pending")) for r in rows)
    if pending:
        errors.append(f"{pending} rows still have a pending workflow marker.")
    hard = [r for r in rows if "hard_case" in r["note"]]
    if len(hard) < 3:
        errors.append("Record at least three actual hard-case decisions.")
    criteria = re.sub(r"<!--[\s\S]*?-->", "", (root / "criteria.md").read_text())
    blocks = re.findall(r"^## ([1-5])\.[^\n]*\n([\s\S]*?)(?=^## [1-5]\.|\Z)", criteria, re.M)
    if [n for n, _ in blocks] != list("12345"):
        errors.append("criteria.md must have exactly five numbered criteria.")
    for n, content in blocks:
        before, _, reason = content.partition("**Why this target:**")
        if not re.search(r"\d", before):
            errors.append(f"Criterion {n} has no numeric target.")
        if not reason.replace("---", "").strip():
            errors.append(f"Criterion {n} has no reason.")
    return errors, dict(counts)


if __name__ == "__main__":
    errors, counts = validate()
    print("Actual labeled counts:", json.dumps(counts))
    for error in errors:
        print("[FIX ME]", error)
    if not errors:
        print("Data and criteria checks passed. Verify milestone commits before training.")
    sys.exit(bool(errors))
