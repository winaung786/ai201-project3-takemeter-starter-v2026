"""Fail early on unreviewed data or blank criteria; never trains or splits data."""
import csv
import json
import re
import sys
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT, require_committed=True):
    root = Path(root)
    errors = []
    labels = json.loads((root / "docs/label-map.json").read_text())
    with (root / "labels.csv").open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["text", "label", "note"]:
            return ["CSV columns must be exactly text,label,note in this project."], {}
        rows = list(reader)
    for row in rows:
        if None in row or any(row.get(k) is None for k in ("text", "label", "note")):
            errors.append("Malformed CSV row: missing or extra fields.")
            return errors, {}
    if len(rows) < 150:
        errors.append(f"Only {len(rows)} rows; the documented floor is 150 labeled examples.")
    elif len(rows) < 200:
        readme = (root / "README.md").read_text()
        stop = re.search(r"\*\*Collection stop rule:\*\*\s*(.+?)(?=\n\n|\Z)", readme, re.S)
        if not stop or not stop.group(1).strip() or stop.group(1).strip().lower() in {"pending", "todo"}:
            errors.append("150–199 rows: document the actual stop-rule reason in README after '**Collection stop rule:**'.")
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
        if counts[label] == 0:
            errors.append(f"Declared label {label} has no examples; review the taxonomy or collect that label.")
        if rows and counts[label] / len(rows) > .70:
            errors.append(f"{label} exceeds the 70% cap.")
    cold = [r for r in rows if "cold" in {x.strip() for x in r["note"].split(";")}]
    if len(cold) != 20 or any(not r["label"] for r in cold):
        errors.append(f"Need 20 actually labeled cold rows; found {len(cold)}.")
    if any("ai_prelabel" in r["note"] for r in cold):
        errors.append("A cold row cannot also be AI-pre-labeled.")
    ai_unreviewed = sum("ai_prelabel" in r["note"] and "human_reviewed" not in r["note"] for r in rows)
    if ai_unreviewed:
        errors.append(f"{ai_unreviewed} AI-pre-labeled rows lack a human-review marker.")
    pending = sum(any(x in r["note"] for x in ("cold_pending", "unlabeled", "review_pending")) for r in rows)
    if pending:
        errors.append(f"{pending} rows still have a pending workflow marker.")
    hard = [r for r in rows if "hard_case" in r["note"]]
    if len(hard) < 3:
        errors.append("Record at least three actual hard-case decisions.")
    criteria = re.sub(r"<!--[\s\S]*?-->", "", (root / "criteria.md").read_text())
    blocks = re.findall(r"^## (\d+)\.[^\n]*\n([\s\S]*?)(?=^## \d+\.|\Z)", criteria, re.M)
    if [n for n, _ in blocks] != list("12345"):
        errors.append("criteria.md must have exactly five numbered criteria.")
    for n, content in blocks:
        before, _, reason = content.partition("**Why this target:**")
        if not re.search(r"\d", before):
            errors.append(f"Criterion {n} has no numeric target.")
        if not reason.replace("---", "").strip():
            errors.append(f"Criterion {n} has no reason.")
    if require_committed:
        try:
            for filename in ("criteria.md", "labels.csv"):
                snapshot = subprocess.check_output(["git", "show", f"HEAD:{filename}"], cwd=root, stderr=subprocess.DEVNULL)
                if snapshot != (root / filename).read_bytes():
                    errors.append(f"Commit the current {filename} before creating the training split.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            errors.append("Restore the Git repository and commit criteria.md and labels.csv before training.")
    return errors, dict(counts)


if __name__ == "__main__":
    errors, counts = validate(require_committed="--files-only" not in sys.argv)
    print("Actual labeled counts:", json.dumps(counts))
    for error in errors:
        print("[FIX ME]", error)
    if not errors:
        print("Structure and provenance checks passed. Manually review criterion testability and community-specific reasons before training.")
    sys.exit(bool(errors))
