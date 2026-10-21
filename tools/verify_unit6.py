"""Recompute reported metrics from saved predictions and audit split isolation."""
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from baseline import score


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def same(actual, expected):
    if isinstance(expected, dict):
        for k, v in expected.items():
            same(actual[k], v)
    elif isinstance(expected, float):
        assert math.isclose(actual, expected, abs_tol=1e-6), (actual, expected)
    else:
        assert actual == expected, (actual, expected)


def main():
    labels = ["analysis", "unsupported", "question"]
    data_hash = sha(ROOT / "labels.csv")
    criteria_hash = sha(ROOT / "criteria.md")
    assert data_hash == "a60e1a1fa9b9d8504ab692d360012d7fa25d195f5668db5a26a017e6b0994345"
    assert criteria_hash == "256d7d354dff1847ee27277a9a5cdc77ae88c43e17962febefd27dc30d2a8d6e"
    with (ROOT / "labels.csv").open(newline="") as f:
        data = list(csv.DictReader(f))
    gold_by_text = {r["text"]: r["label"] for r in data}
    all_hashes = {hashlib.sha256(t.encode()).hexdigest() for t in gold_by_text}
    assert len(all_hashes) == 200
    counts = Counter(r["label"] for r in data)
    with (ROOT / "test_split.csv").open(newline="") as f:
        test = list(csv.DictReader(f))
    baseline = json.loads((ROOT / "baseline_results.json").read_text())
    assert baseline["held_out"] and baseline["used_definitions"]
    assert [(p["text"], p["gold"]) for p in baseline["predictions"]] == [(r["text"], r["label"]) for r in test]
    same(baseline["scores"], score([r["gold"] for r in baseline["predictions"]], [r["predicted"] for r in baseline["predictions"]], sorted(labels)))
    runs = {}
    for stage, epochs in [("before", 3), ("after", 4)]:
        runs[stage] = json.loads((ROOT / f"results_three_seeds_{stage}.json").read_text())
        assert [r["seed"] for r in runs[stage]] == [42, 7, 2024]
        for r in runs[stage]:
            assert r["data_sha256"] == data_hash and r["criteria_sha256"] == criteria_hash
            assert r["epochs"] == epochs and r["max_length"] == 128
            assert r["learning_rate"] == 2e-5 and r["batch_size"] == 16
            assert r["base_model"] == "distilbert-base-uncased" and r["device"] == "cpu"
            ps = r["predictions"]
            assert len(ps) == r["n_test"] == 30
            assert all(gold_by_text[p["text"]] == p["gold"] for p in ps)
            recalculated = score([p["gold"] for p in ps], [p["predicted"] for p in ps], labels)
            recalculated.pop("n")
            same(r, recalculated)
            matrix = {t: {p: 0 for p in labels} for t in labels}
            for p in ps:
                matrix[p["gold"]][p["predicted"]] += 1
                assert abs(sum(p["probabilities"].values()) - 1) < 1e-6
                same(p["confidence"], max(p["probabilities"].values()))
                assert p["predicted"] == max(p["probabilities"], key=p["probabilities"].get)
            same(r["confusion"], matrix)
            right = [p["confidence"] for p in ps if p["gold"] == p["predicted"]]
            same(r["confidence"]["mean_when_right"], sum(right) / len(right))
            same(r["confidence"]["fraction_below_0_50"], sum(p["confidence"] < .5 for p in ps) / 30)
            split_sets = {name: set(s["text_sha256"]) for name, s in r["splits"].items()}
            assert set.union(*split_sets.values()) == all_hashes
            assert sum(len(s) for s in split_sets.values()) == 200
            assert split_sets["test"] == {hashlib.sha256(p["text"].encode()).hexdigest() for p in ps}
            for a, b in [("train", "validation"), ("train", "test"), ("validation", "test")]:
                assert not split_sets[a] & split_sets[b]
            same(r["label_counts"], dict(counts))
    for before, after in zip(runs["before"], runs["after"]):
        assert before["splits"] == after["splits"]
        for key in ["base_model", "learning_rate", "batch_size", "max_length", "labels", "device", "torch_version"]:
            assert before[key] == after[key]
    original = json.loads((ROOT / "results.json").read_text())
    original_seed_reproduced = all(math.isclose(original[k], runs["before"][0][k], abs_tol=1e-6) for k in ["accuracy", "f1_macro"])
    status = {"baseline_same_original_30": True, "six_real_trials_checked": True,
        "all_prediction_metrics_recomputed": True, "all_within_seed_splits_disjoint": True,
        "before_after_splits_identical": True, "only_training_setting_changed": "epochs: 3 -> 4",
        "original_seed_metrics_reproduced": original_seed_reproduced,
        "dataset_unchanged": True, "criteria_unchanged": True,
        "data_sha256": data_hash, "criteria_sha256": criteria_hash,
        "staff_comparison_complete": False, "assignment_complete": False,
        "remaining": ["student independently labels all 30 staff posts", "TF supplies authentic staff_labels.csv after blind labels frozen", "student adjudicates every actual disagreement"]}
    (ROOT / "evidence/unit6/verification.json").write_text(json.dumps(status, indent=2) + "\n")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
