"""Validate the student's blind 30-row annotation before using the staff key."""
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    with (ROOT / "data/staff_posts.csv").open(newline="") as f:
        posts = list(csv.DictReader(f))
    with (ROOT / "my_staff_labels.csv").open(newline="") as f:
        mine = list(csv.DictReader(f))
    if len(mine) != 30 or [r["text"] for r in mine] != [r["text"] for r in posts]:
        raise SystemExit("Keep all 30 staff posts unchanged and in their original order.")
    invalid = [i for i, r in enumerate(mine, 1) if r["label"] not in {"analysis", "hot_take", "reaction"}]
    if invalid:
        raise SystemExit(f"Student labels still missing or invalid at rows {invalid}. Fill these independently before opening the key.")
    committed = subprocess.run(["git", "show", "HEAD:my_staff_labels.csv"], cwd=ROOT, capture_output=True)
    if committed.returncode or committed.stdout != (ROOT / "my_staff_labels.csv").read_bytes():
        raise SystemExit("Commit the completed blind labels before using the staff key.")
    if not (ROOT / "data/staff_labels.csv").exists():
        raise SystemExit("Get data/staff_labels.csv from the TF now that your own labels are saved.")
    subprocess.run([sys.executable, "agreement.py"], cwd=ROOT, check=True)
    print("Add your own reasoned call and one of the three piles for every disagreement.")


if __name__ == "__main__":
    main()
