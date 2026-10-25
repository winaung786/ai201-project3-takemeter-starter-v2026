"""Record the authentic TF import and report AI-to-staff comparison honestly."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN_LABEL_COMMIT = "7cc80560b80ae83656841ac2b50bd771c4654e66"
FROZEN_LABEL_SHA256 = "348bbadf6defff2bd5fc6ad45bfc5ada164b150234369d0e9400910af5553ab1"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def agreement_report_lines(root=ROOT):
    report = json.loads((root / "agreement_results.json").read_text())
    by_text = {r["text"]: r["id"] for r in rows(root / "data/staff_post_texts.csv")}
    reference = {r["id"]: r for r in rows(root / "data/staff_labels.csv")}
    lines = [f"**Measured AI-to-staff agreement: {report['agreed']}/{report['compared']} = {report['agreement_rate']:.6f} ({report['agreement_rate']:.1%}).** The pre-key labels in `my_staff_labels.csv` were prepared by Codex. This is a diagnostic comparison, not two independent human annotators. Criterion 4 remains **MISSED — independent human evidence not demonstrated**, despite the numerical rate exceeding 80%.", "",
        "The authentic reference was supplied through [the TF Drive file](https://drive.google.com/file/d/1Cp8PeB-MkDaNifSPNixNfo7xVfi6R3GF/view). It was downloaded after the 30 label choices had been committed at `7cc80560b80ae83656841ac2b50bd771c4654e66`; those choices have not changed after seeing the key. [Import provenance](evidence/unit6/staff-reference-import.json) records the file hashes and filename mapping.", "",
        "**File mapping:** At the user's explicit request, the downloaded answer CSV is saved as [data/staff_posts.csv](data/staff_posts.csv). It contains `id,label,borderline,why`, not post text. The identical answer bytes are also saved as [data/staff_labels.csv](data/staff_labels.csv). The original `id,text` file is preserved byte-for-byte as [data/staff_post_texts.csv](data/staff_post_texts.csv). `python agreement.py` now defaults to that text file and the canonical labels file.", "",
        "| Compared | Matched | Disagreed | Missing posts | Annotation authorship |", "|---:|---:|---:|---:|---|",
        f"| {report['compared']} | {report['agreed']} | {len(report['disagreements'])} | {report['staff_posts_not_in_mine']} | Codex AI versus staff reference |", "",
        "### Every actual disagreement", ""]
    for r in report["disagreements"]:
        post_id = by_text[r["text"]]
        lines += [f"#### {post_id}", "", "> " + r["text"].replace("\n", "\n> "), "",
            f"**Saved pre-key label:** `{r['mine']}`. **Staff label:** `{r['staff']}`.", "",
            "**Staff's supplied rationale:** " + reference[post_id]["why"], "",
            "**AI-assisted case for `analysis`:** The post uses the 3% change after the shoe-rule change as a premise and explicitly connects it with 'so' to a causal conclusion. Rule 1's analysis example also reasons from a change in times and a change in shoe rules. The causal inference is too strong, but a weak inference can still use a fact as its premise.", "",
            "**AI-assisted case for `hot_take`:** 'Obviously', 'the whole story', and the judgment that the sport has a problem express a sweeping conclusion that the single statistic cannot establish. Under Rule 1's decoration clause, the statistic can be read as a flourish attached to that conclusion. This follows the staff interpretation of its own canonical boundary case.", "",
            "**AI-assisted adjudication, prepared at the user's request:** Retain `analysis` as a defensible reading. The measured time change and its timing relative to the rule change explicitly supply the premise for the conclusion. Rule 1 asks whether a fact carries the argument; it does not require that the resulting causal inference be valid. The wording 'so obviously' overstates the evidence but does not by itself show that the writer reached the conclusion before considering the statistic. Staff's reading remains plausible because the claim about the whole sport extends beyond the fact supplied.", "",
            "**Disagreement category: (c) — two defensible readings.** This call preserves the pre-key label rather than changing it to match staff. It is the assistant's argued adjudication, delegated by the user, and is not represented as an independently written student judgment.", ""]
    lines += ["The one dispute concerns `analysis` versus `hot_take` in the staff running-forum taxonomy. It does not establish that the separate Hacker News `question` boundary caused the trained model's errors. The assisted adjudication is complete; independent human annotation and independently authored student adjudication are not demonstrated. The original training results and criteria are unchanged.", ""]
    return lines


def main():
    posts = rows(ROOT / "data/staff_post_texts.csv")
    ref = rows(ROOT / "data/staff_labels.csv")
    mine = rows(ROOT / "my_staff_labels.csv")
    assert len(posts) == len(ref) == len(mine) == 30
    assert sha(ROOT / "my_staff_labels.csv") == FROZEN_LABEL_SHA256
    assert [r["text"] for r in mine] == [r["text"] for r in posts]
    assert len({r["id"] for r in ref}) == 30
    assert {r["id"] for r in ref} == {r["id"] for r in posts}
    assert (ROOT / "data/staff_posts.csv").read_bytes() == (ROOT / "data/staff_labels.csv").read_bytes()
    result_path = ROOT / "agreement_results.json"
    result = json.loads(result_path.read_text())
    by_id = {r["id"]: r["label"] for r in ref}
    pairs = [(by_id[p["id"]], m["label"]) for p, m in zip(posts, mine)]
    agreed = sum(a == b for a, b in pairs)
    assert result["compared"] == 30 and result["staff_posts_not_in_mine"] == 0
    assert result["agreed"] == agreed and result["agreement_rate"] == agreed / 30
    assert len(result["disagreements"]) == 30 - agreed
    result["comparison_provenance"] = {"annotation_author": "Codex AI assistant",
        "reference_source": "TF-supplied Google Drive file", "frozen_label_commit": FROZEN_LABEL_COMMIT,
        "label_file_sha256": FROZEN_LABEL_SHA256, "independent_human_agreement": False,
        "criterion_4_demonstrated": False, "student_adjudications_completed": False,
        "ai_assisted_adjudications_completed": True, "adjudication_author": "Codex, delegated by the user"}
    result["assisted_adjudications"] = [{"text": r["text"], "original_label": r["mine"],
        "staff_label": r["staff"], "adjudicated_label": "analysis", "category": "c",
        "author": "Codex AI assistant", "reason": "The 3% change and its timing explicitly function as a causal premise under Rule 1. The inference overreaches, but inference validity is not required by the taxonomy. Staff can defensibly treat the statistic as decoration on the broader unsupported conclusion."}
        for r in result["disagreements"]]
    result_path.write_text(json.dumps(result, indent=2) + "\n")
    standalone = "\n".join(agreement_report_lines())
    for prefix in ["data/", "evidence/"]:
        standalone = standalone.replace("](" + prefix, "](../../" + prefix)
    (ROOT / "docs/unit6/staff-comparison.md").write_text("# AI-to-staff agreement report\n\n" + standalone)
    print(f"Verified {agreed}/30 AI-to-staff agreement; the delegated AI-assisted adjudication is complete.")


if __name__ == "__main__":
    main()
