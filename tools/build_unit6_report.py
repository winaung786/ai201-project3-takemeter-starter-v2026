"""Build the typed Unit 6 report from the committed-format result artifacts."""
import json
import re
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from baseline import markdown_table
from tools.staff_reference_report import agreement_report_lines

LABELS = ["analysis", "unsupported", "question"]


def load(name):
    return json.loads((ROOT / name).read_text())


def verdict(passes):
    return "MET" if all(passes) else "MISSED"


def log(runs):
    rows = ["| Criterion | Original target | Seed 42 | Seed 7 | Seed 2024 | Verdict |",
            "|---|---|---|---|---|---|"]
    items = [
        ("1. Overall accuracy", "≥0.75 in every seed", [f"{r['accuracy']:.6f}" for r in runs], [r["accuracy"] >= .75 for r in runs]),
        ("2. Every label F1", "≥0.65 for all labels in every seed", ["; ".join(f"{l}: {r['per_label'][l]['f1']:.6f}" for l in LABELS) for r in runs], [all(r["per_label"][l]["f1"] >= .65 for l in LABELS) for r in runs]),
        ("3. Dataset balance", "Every label 15%–45% of all 200 comments", ["analysis 36%; unsupported 40.5%; question 23.5%"] * 3, [True] * 3),
        ("4. Human agreement", "≥80% on 30–50 comments", ["Independent human labels missing"] * 3, [False] * 3),
        ("5. Prediction confidence", "Correct mean ≥0.70; fraction of all test max-probs below 0.50 <15%; every seed", [f"correct mean {r['confidence']['mean_when_right']:.6f}; low {r['confidence']['fraction_below_0_50']:.1%}" for r in runs], [(r["confidence"]["mean_when_right"] or 0) >= .7 and r["confidence"]["fraction_below_0_50"] < .15 for r in runs]),
    ]
    for name, target, values, passing in items:
        rows.append("| " + " | ".join([name, target, *values, verdict(passing)]) + " |")
    return "\n".join(rows)


def matrices(runs):
    lines = []
    for r in runs:
        c = r["confusion"]
        lines += [f"### Confusion matrix — seed {r['seed']}", "", "| True / predicted | analysis | unsupported | question |", "|---|---:|---:|---:|"]
        lines += ["| **" + t + "** | " + " | ".join(str(c[t][p]) for p in LABELS) + " |" for t in LABELS]
        a, b = max(((a, b) for a in LABELS for b in LABELS if a != b), key=lambda pair: c[pair[0]][pair[1]])
        lines += ["", f"Largest off-diagonal cell (first in label order if tied): {c[a][b]} true `{a}` posts were called `{b}`; the reverse direction has {c[b][a]} errors.", ""]
    return "\n".join(lines)


def main():
    before = load("results_three_seeds_before.json")
    after_path = ROOT / "results_three_seeds_after.json"
    after = load(after_path.name) if after_path.exists() else None
    baseline, original = load("baseline_results.json"), load("results.json")
    spread = max(r["accuracy"] for r in before) - min(r["accuracy"] for r in before)
    minima = [min((r["per_label"][l]["f1"], l) for l in LABELS) for r in before]
    other_f1_misses = "; ".join(f"seed {r['seed']} {l}: {r['per_label'][l]['f1']:.6f}" for r in before for l in LABELS if l != "question" and r["per_label"][l]["f1"] < .65)
    question_recall = ", ".join(f"seed {r['seed']}: {r['per_label']['question']['recall']:.6f}" for r in before)
    lines = ["<!-- UNIT6-REPORT -->", "## Unit 6 status", "",
        "**The baseline and before trials are complete.** " + ("All three after trials and the one-change comparison are also complete. " if after else "The declared after experiment is in progress. ") +
        "**The assignment is not complete:** the independent human annotation requirement and independently authored student adjudication remain unverified. The user delegated the remaining adjudication to Codex, which has completed an attributed assisted decision. The authentic TF reference has now been imported, and the existing 30 AI-assisted labels have been compared against it.", "",
        "The original `criteria.md`, `labels.csv`, taxonomy, Unit 5 `results.json`, and `test_split.csv` are preserved. The [pre-run protocol](docs/unit6/plan.md) records the baseline prediction and measurement conventions. No Unit 6 stretch feature is claimed.", "",
        "## Baseline vs. Trained", "",
        "**Prediction recorded before baseline scoring:** The trained model will beat the zero-shot baseline on `unsupported` F1 because it has seen Hacker News agreement, jokes, and bare statements assigned to this deliberately broad category.", "",
        markdown_table(baseline["scores"], LABELS, original), "",
        "Both columns score exactly the same 30 original Unit 5 test comments. The baseline is `facebook/bart-large-mnli`, using all three exact one-sentence README definitions in `label_definitions.txt`, with no examples, fallback, or cap. Trained means the original three-epoch seed-42 model. The prediction held for unsupported F1, yet the baseline beat training on question F1 (0.444444 versus 0). The 20-point accuracy advantage therefore does not mean training learned every category. The requested one-sentence prompt does not include all boundary tie-breakers; a weak baseline could partly reflect that limitation. These are local CPU runs, without hosted-model API calls.", "",
        "## Run Log — Before", "",
        "Three real retrainings using the notebook section 6 loop: seeds **42, 7, 2024**. Device **CPU**, PyTorch **2.6.0+cpu**, model **distilbert-base-uncased**, 3 epochs, learning rate **2e-5**, batch **16**, maximum **128 tokens**. Stratified splits are 139 train / 31 validation / 30 test. In each test: analysis 11, unsupported 12, question 7. Each seed's full predictions, softmax probabilities, split hashes and trainer history are saved in the results JSON and `evidence/unit6/before/`.", "",
        log(before), "",
        "Criterion 3 is one dataset measurement repeated for clarity; criterion 4 is one human exercise, not three model-seed trials. `MISSED` on criterion 4 means the required evidence has not been demonstrated, **not** 0% measured agreement. The 30 staff posts use the staff running-forum taxonomy, which cannot directly validate every Hacker News annotation. No original target has been changed.", "",
        f"Before accuracy spread is **{spread:.6f} ({spread * 100:.1f} percentage points)**. " + ("This exceeds the brief's 10-point instability flag; one favorable split would be unreliable." if spread > .1 else "This does not exceed the brief's 10-point flag, but 30 test comments still make each accuracy error worth 3.33 points."), "",
        "Always guessing the training-majority label `unsupported` would score 12/30 = 40% on each held-out split. The trained model beats that trivial reference, but its zero question recall shows why overall accuracy alone is insufficient.", "",
        "Rows below are true labels; columns are model predictions. Each matrix is for its own 30-post split, not a pooled independent sample.", "", matrices(before),
        "## Verdicts and Diagnoses", "",
        "1. **Accuracy — " + verdict([r["accuracy"] >= .75 for r in before]) + ".** The original rule requires every seed to reach 0.75. Minority-question errors limit accuracy: question recall is " + question_recall + ". Each split has only seven question examples and the training subset only 33. This makes weak question learning costly and estimates coarse. Continued validation-loss decline supports testing more optimization, but does not prove that training length is the only cause.", "",
        "2. **Every-label F1 — " + verdict([all(r["per_label"][l]["f1"] >= .65 for l in LABELS) for r in before]) + ".** Minimum F1 by seed is " + "; ".join(f"{r['seed']}: {l} {v:.6f}" for r, (v, l) in zip(before, minima)) + ". Other misses: " + (other_f1_misses or "none") + ". Seed 42 sends all seven true questions to analysis or unsupported, while making no question predictions. Even the straightforward request “What are you using? whisper?” becomes unsupported. A more complex Cursor free-trial question becomes analysis, showing that an information request with contextual details is also difficult. The direction suggests a request-versus-statement weakness. False unsupported predictions also reduce that label's precision, while seed 2024 additionally confuses analysis and unsupported in both directions. Without the independent staff exercise, inconsistent labeling is a hypothesis, not an established diagnosis.", "",
        "3. **Balance — MET.** Counts remain analysis 72/200, unsupported 81/200, question 47/200: all fall within the original 15%–45% band. The smallest class still provides only 33 training examples per split. Passing the balance target does not ensure enough examples or representative prevalence; the Unit 5 purposive sampling remains disclosed.", "",
        "4. **Human agreement — MISSED, not demonstrated.** The authentic TF key is available and the AI-assisted labels match 29/30. Independent human annotations remain unavailable, so this rate does not measure agreement between two humans. A prior confirmation of all 200 AI-assisted project labels is one human review, not agreement between two humans. The staff exercise must be completed before diagnosing inconsistent rule application. Its different taxonomy also limits how far its result transfers to the Hacker News dataset.", "",
        "5. **Confidence — " + verdict([(r["confidence"]["mean_when_right"] or 0) >= .7 and r["confidence"]["fraction_below_0_50"] < .15 for r in before]) + ".** Read both conditions in each run-log cell. Winning probabilities remain too low, consistent with weak class separation after three epochs; they do not show that hedging caused the problem. Softmax confidence is uncalibrated, and raising it alone would not prove correctness. The saved probabilities permit direct recomputation of the correct-only mean and all-test low-confidence fraction.", "",
        "## Agreement Report", "",
        *agreement_report_lines(ROOT),
        "## The Improvement", "",
        "**One change: epochs 3 → 4.** The [improvement declaration](docs/unit6/improvement-plan.json) is recorded after the before diagnosis and before starting after. The question weakness and low confidence, together with declining validation loss, justify a limited optimization test. The earlier Unit 5 3-versus-4 comparison was already known; this Unit 6 experiment tests its repeatability across three seeds and is not a previously unseen hypothesis. More epochs may overfit and are not a substitute for label-agreement evidence. No rows, taxonomy, learning rate, batch size, token limit, split, seeds, or criteria changed. This is the sole Unit 6 improvement; no second fix was tried.", ""]
    if after:
        lines += ["### Run Log — After", "", log(after), "", "### Paired before/after comparison", "",
                  "Each cell is before → after (after minus before). These paired comparisons use identical splits within each seed; overlapping posts across seeds mean these are not independent 90-post trials.", "",
                  "| Measure | Seed 42 | Seed 7 | Seed 2024 |", "|---|---|---|---|"]
        measures = [("Accuracy", lambda r: r["accuracy"]), ("Macro F1", lambda r: r["f1_macro"])]
        measures += [(f"F1 {l}", lambda r, l=l: r["per_label"][l]["f1"]) for l in LABELS]
        measures += [("Correct-prediction mean confidence", lambda r: r["confidence"]["mean_when_right"]), ("Fraction confidence <0.50", lambda r: r["confidence"]["fraction_below_0_50"])]
        comparison = []
        for name, fn in measures:
            vals = [(fn(b), fn(a)) for b, a in zip(before, after)]
            lines.append("| " + name + " | " + " | ".join(f"{b:.6f} → {a:.6f} ({a-b:+.6f})" for b, a in vals) + " |")
            comparison.append({"measure": name, "seeds": [{"seed": b["seed"], "before": x, "after": y, "delta": y-x} for b, (x, y) in zip(before, vals)]})
        (ROOT / "docs/unit6/paired-comparison.json").write_text(json.dumps(comparison, indent=2) + "\n")
        improvements = sum(a["accuracy"] > b["accuracy"] for b, a in zip(before, after))
        regressions = sum(a["accuracy"] < b["accuracy"] for b, a in zip(before, after))
        ties = len(after) - improvements - regressions
        after_spread = max(r["accuracy"] for r in after) - min(r["accuracy"] for r in after)
        lines += ["", f"Accuracy improved in **{improvements}/3** seeds, stayed unchanged in **{ties}/3**, and regressed in **{regressions}/3**; the paired table shows the size and label-specific direction of every change. " + ("The accuracy improvement repeated across all seeds, though this small experiment does not establish performance outside these eight threads." if improvements == 3 else "The change did not improve accuracy in every seed, so its benefit is partial rather than a reliable fix for all splits."), "",
                  f"After accuracy spread: **{after_spread:.6f}**. " + ("It remains above the 10-point instability flag. " if after_spread > .1 else "It is within the brief's 10-point flag, though the samples remain small. ") + "Final criterion verdicts must still hold in every seed; improvements do not automatically become passes.", "", matrices(after)]
        lines += ["Final verdicts: accuracy **" + verdict([r["accuracy"] >= .75 for r in after]) + "**; every-label F1 **" + verdict([all(r["per_label"][l]["f1"] >= .65 for l in LABELS) for r in after]) + "**; balance **MET**; human agreement **MISSED — not demonstrated**; confidence **" + verdict([(r["confidence"]["mean_when_right"] or 0) >= .7 and r["confidence"]["fraction_below_0_50"] < .15 for r in after]) + "**.", ""]
        lines += ["The extra epoch recovered " + "; ".join(f"seed {r['seed']}: {r['confusion']['question']['question']}/7 true questions" for r in after) + ". Seed 2024's accuracy gain comes from analysis/unsupported classification rather than learning question. Training length therefore explains part of the measured weakness, but this one change did not solve the request boundary across seeds. The after log still misses accuracy, every-label F1, and both-part confidence targets; the absent independent agreement evidence prevents deciding whether remaining boundary errors originate in annotation consistency, task difficulty, or inadequate training data.", ""]
    else:
        lines += ["The after experiment is not yet complete; no after scores are reported.", ""]
    lines += ["## What's Still Broken", "",
        "For any remaining accuracy or per-label F1 miss, the next step would be a separate development-set audit of request-versus-statement examples, followed by targeted new questions if warranted; no extra fix is made here because this unit allows one measured improvement. Seven question test examples per seed remain too few for precise per-label estimates, and comment-level splits within eight threads do not establish transfer to unseen threads or the whole of Hacker News.", "",
        "Criterion 4 remains unproven because the saved labels are AI-assisted. The authentic TF reference is now available; the one disagreement now has an attributed AI-assisted adjudication retaining analysis under category (c). Independently written student adjudication is not demonstrated. Confidence misses require a later calibration/abstention study on validation data rather than forcing probabilities upward to pass a threshold; no additional test-driven tuning was performed.", "",
        "The intended taxonomy distinguishes evidence supporting a main claim, unsupported statements, and genuine information requests. The before matrix shows that the learned classifier instead favors the two statement categories and misses genuine questions, so it has only partially learned that intended distinction.", "",
        "Reproduce with the repository virtual environment and the environment variables in [the reproduction guide](docs/unit6/reproduce.md): `python tools/run_unit6.py --run before --allow-assisted-initial20`, then the declared `--run after`, then `python tools/verify_unit6.py` and `python tools/build_unit6_report.py`. The runner refuses to overwrite existing results; preserve or move prior outputs for a deliberate new experiment. After verification runs, `evidence/unit6/verification.json` records its arithmetic and split checks. Large model caches and weights remain excluded from Git.", ""]
    readme = (ROOT / "README.md").read_text().split("<!-- UNIT6-REPORT -->")[0].rstrip()
    trials = "six notebook-based training trials" if after else "three before trials and launched the after experiment"
    disclosure = f"**Unit 6 AI assistance:** Codex read the provided assignment and PowerPoint, ran the local baseline and {trials}, recorded predictions and split isolation, and drafted the typed tables and diagnoses. The original student criteria and confirmed project labels were kept unchanged. At the student's later request, Codex also prepared all 30 AI label suggestions with individual reasons in `reviews/unit6-ai/`; the provenance explicitly records that they are not independent human annotations. The same 30 choices are now also saved in `my_staff_labels.csv`, with separate authorship evidence. No TF key was opened for the original annotation. The later TF download enabled a 29/30 AI-to-staff comparison; independent human agreement is not claimed. The user subsequently delegated the one remaining adjudication, which Codex completed and attributed as AI-assisted. The Unit 6 interpretation is AI-assisted and should be reviewed by the student.\n\n"
    readme = re.sub(r"\*\*Unit 6 AI assistance:\*\*.*?\n\n", "", readme, count=1, flags=re.S)
    readme = readme.replace("## How I Used AI\n\n", "## How I Used AI\n\n" + disclosure)
    readme = readme.replace("and the three-seed Unit 6 evaluation has not run. No three-seed pass is claimed.", "as recorded at the end of Unit 5. The Unit 6 three-seed results are now reported below.")
    note = "**Unit 6:** " + ("Baseline, all six training trials, and the measured improvement are complete" if after else "Baseline and three before trials are complete; the after experiment is running") + "; the authentic TF reference and AI-to-staff comparison are saved, and the delegated AI-assisted adjudication is complete. Independent human annotation evidence and independently written student adjudication are not demonstrated."
    readme = re.sub(r"^\*\*Unit 6:\*\*.*?\n\n", "", readme, count=1, flags=re.M)
    readme = readme.replace("**Build status:", note + "\n\n**Build status:", 1)
    (ROOT / "README.md").write_text(readme + "\n\n" + "\n".join(lines))
    print("Typed Unit 6 README report rebuilt from actual results.")


if __name__ == "__main__":
    main()
