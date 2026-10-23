"""Write a disclosed AI annotation draft without modifying the student's blind form."""
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Each decision was made from the post and staff taxonomy, without the TF key.
DECISIONS = [
    ("sp_001", "analysis", "The winning-time and 100th-place changes support the distinction between front performance and field depth.", None),
    ("sp_002", "analysis", "Eleven weeks of tracked sleep and interval times support the scheduling conclusion. The writer acknowledges the sample limitation.", None),
    ("sp_003", "analysis", "The dated top-6 to top-10 scoring change and two B-team results are evidence for the claim that turnout, rather than depth, explains the outcomes.", None),
    ("sp_004", "analysis", "The comparison of two first-half pace groups supplies the premise for disputing the hill explanation. The inference can be debated without removing its evidence-based form.", None),
    ("sp_005", "analysis", "Two measured 2% improvements, with unchanged shoes and increased mileage in the second period, support rejecting a shoes-only explanation.", None),
    ("sp_006", "analysis", "Entry-list percentages of 41% and 26% support the explanation involving first-time entrants.", None),
    ("sp_007", "analysis", "The same loop, matched heart-rate effort, two temperatures, and a 90-second difference support the conclusion about heat cost.", "reaction: This is first-hand experience, but rule 3 gives priority to the measured comparison doing argumentative work."),
    ("sp_008", "analysis", "The recurring 18%-23% non-start rate across results since 2012 supports the base-rate explanation.", None),
    ("sp_009", "analysis", "The 2021 remeasurement and 60-metre discrepancy support the warning that before/after personal bests are not directly comparable.", None),
    ("sp_010", "analysis", "The three runners' same-session comparison within ten seconds supports the limited claim that any shoe effect was smaller than that observed variation.", None),
    ("sp_011", "hot_take", "The monthly-racing cutoff supports a general judgment only by assertion. No observations or source establish that racing frequently prevents training.", None),
    ("sp_012", "hot_take", "The astrology comparison dismisses heart-rate zones without offering evidence.", None),
    ("sp_013", "hot_take", "The post makes a general claim that the Tuesday session excludes some runners, without examples or supporting facts.", None),
    ("sp_014", "analysis", "Under rule 1, the measured time change and its timing relative to the shoe rules are explicitly used as a causal premise, signaled by 'so'. The conclusion overstates what the evidence establishes, but the definition does not require a correct inference.", "hot_take: 'the whole story' and 'the sport has a problem' can be read as the main unsupported conclusions, with the statistic decorating them. This is the hardest draft boundary; a final human call must decide whether the number actually carries the main argument."),
    ("sp_015", "hot_take", "The claim that all marathon plans are the same has no named comparison or examples.", None),
    ("sp_016", "hot_take", "Ninety minutes is an asserted cutoff, not a measured observation supporting the fueling diagnosis.", "analysis: The number looks factual, but rule 1 requires a fact to support the argument; an unexplained threshold alone does not do so."),
    ("sp_017", "hot_take", "The date identifies the alleged peak but supplies no evidence that later racing is just marketing.", None),
    ("sp_018", "hot_take", "The eight-minute-mile cutoff and claimed better alternative are unsupported recommendations. A numeric cutoff is not itself evidence.", None),
    ("sp_019", "hot_take", "The post generalizes about everyone's feelings toward long runs without observations or support.", None),
    ("sp_020", "hot_take", "'Every injury thread' and 'the same three replies' are sweeping assertions without cited threads or an actual comparison.", None),
    ("sp_021", "reaction", "The main content is the writer's immediate joy after a personal best. The four-minute change supplies the occasion, not an argued conclusion.", "analysis: The time improvement is checkable, but rule 1 asks whether it carries an argument. Here the post expresses happiness."),
    ("sp_022", "reaction", "The writer describes being stranded after a cancellation. Departure time and travel duration provide context for the immediate frustration.", None),
    ("sp_023", "reaction", "The writer expresses relief about a first run back. The eight weeks and two miles describe the occasion rather than support an argument.", None),
    ("sp_024", "reaction", "Standing up while watching the finish expresses an immediate physical and emotional response. The 400 metres is scene-setting.", None),
    ("sp_025", "reaction", "The post reports a recent personal blow-up and disappointment without making a general claim about pacing tools.", None),
    ("sp_026", "reaction", "The orange-slice incident and crying are a personal emotional response. Mile 22 locates the event.", None),
    ("sp_027", "reaction", "The wind angle describes the experience, and the main conclusion is how the return leg felt. There is no measured performance comparison or argued general claim.", "analysis: The 20-degree lean could support a wind-resistance explanation, but this reading supplies an argument the post does not explicitly make. Under rules 1 and 3, a number alone is insufficient."),
    ("sp_028", "reaction", "The writer shares a recent DNF and distress. Counting three DNFs gives context without an argument about their cause.", None),
    ("sp_029", "reaction", "'Just realised' reports a fresh personal discovery about accidentally purchased shoes. No explicit conclusion about shoe fit or performance is argued.", "analysis: A reader could infer a claim about fit from the personal-best history, but that general argument is unstated. The immediate personal discovery is explicit."),
    ("sp_030", "reaction", "The charged card and immediate regret describe the writer's own recent decision and feelings.", None),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    protected = ["my_staff_labels.csv", "labels.csv", "criteria.md", "results.json",
                 "results_three_seeds_before.json", "results_three_seeds_after.json", "baseline_results.json"]
    before = {p: sha(ROOT / p) for p in protected}
    with (ROOT / "data/staff_posts.csv").open(newline="") as f:
        posts = list(csv.DictReader(f))
    assert len(posts) == len(DECISIONS) == 30
    assert [p["id"] for p in posts] == [r[0] for r in DECISIONS]
    assert all(r[1] in {"analysis", "hot_take", "reaction"} for r in DECISIONS)
    out = ROOT / "reviews/unit6-ai"
    out.mkdir(parents=True, exist_ok=True)
    dest = out / "ai_staff_labels.csv"
    with dest.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["text", "label"])
        w.writeheader()
        w.writerows({"text": p["text"], "label": d[1]} for p, d in zip(posts, DECISIONS))
    with dest.open(newline="") as f:
        written = list(csv.DictReader(f))
    assert [r["text"] for r in written] == [r["text"] for r in posts]
    assert all(r["label"] for r in written)
    counts = dict(Counter(r["label"] for r in written))
    records = [{"id": p["id"], "label": d[1], "reason": d[2], "alternative_reading": d[3],
                "text_sha256": hashlib.sha256(p["text"].encode()).hexdigest()}
               for p, d in zip(posts, DECISIONS)]
    provenance = {"annotation_source": "Codex AI assistant", "independent_human_annotation": False,
        "staff_key_accessed_for_this_review": False, "human_reviewed": False,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_posts": "data/staff_posts.csv", "source_posts_sha256": sha(ROOT / "data/staff_posts.csv"),
        "taxonomy": "data/staff_taxonomy.md", "taxonomy_sha256": sha(ROOT / "data/staff_taxonomy.md"),
        "output": str(dest.relative_to(ROOT)), "output_sha256": sha(dest), "n": 30,
        "counts": counts, "course_independent_annotation_requirement_satisfied": False,
        "records": records}
    (out / "annotation-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    lines = ["# AI-assisted draft of all 30 staff labels", "",
        "These decisions were written by Codex from the staff definitions and original posts. They are AI suggestions, not independent student annotations or a TF reference key. No staff key was opened for this review. The student's independent form remains `my_staff_labels.csv`.", "",
        "**Checked:** 30/30 labels filled, exact `text,label` columns, valid staff label names, original post text and order preserved.", "",
        "Counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()) + ". These counts describe the staff draft, not the 200-comment Hacker News training dataset.", "",
        "**Hardest boundary:** sp_014 could be analysis or hot_take. The draft treats the time change as an explicit causal premise. The alternative reading treats the unsupported sweeping conclusion as the main point. This is a provisional AI decision for the student to evaluate; no staff agreement or final student adjudication is claimed.", ""]
    for post, decision in zip(posts, DECISIONS):
        lines += [f"## {post['id']} — {decision[1]}", "", "> " + post["text"].replace("\n", "\n> "), "",
                  "**Reason:** " + decision[2], ""]
        if decision[3]:
            lines += ["**Alternative reading:** " + decision[3], ""]
    (out / "staff-label-review.md").write_text("\n".join(lines))
    assert before == {p: sha(ROOT / p) for p in protected}
    print(json.dumps({"n": 30, "blank_labels": 0, "counts": counts, "source_text_exact": True,
                      "protected_files_unchanged": True, "independent_human_annotation": False}))


if __name__ == "__main__":
    main()
