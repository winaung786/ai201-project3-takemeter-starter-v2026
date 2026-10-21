"""Execute notebook section 6 without overwriting any Unit 5 evidence.

python tools/run_unit6.py --run before --allow-assisted-initial20
python tools/run_unit6.py --run after --allow-assisted-initial20
"""
import argparse
import ast
import gc
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.training_preflight import preflight


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def definitions(source):
    """Load the notebook functions/imports without its single-run side effects."""
    tree = ast.parse(source)
    tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    return compile(ast.fix_missing_locations(tree), "takemeter.ipynb definitions", "exec")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run", required=True, choices=["before", "after"])
    p.add_argument("--allow-assisted-initial20", action="store_true")
    args = p.parse_args()
    os.chdir(ROOT)
    out = ROOT / f"results_three_seeds_{args.run}.json"
    if out.exists():
        raise SystemExit(f"Refusing to overwrite {out.name}")
    errors, counts, provenance = preflight(allow_assisted_initial20=args.allow_assisted_initial20)
    if errors:
        raise SystemExit("\n".join(errors))
    protected = ["labels.csv", "criteria.md", "label_definitions.txt", "results.json",
                 "results_second_run.json", "test_split.csv"]
    original = {f: digest(ROOT / f) for f in protected}
    epochs = 3
    if args.run == "after":
        plan_path = ROOT / "docs/unit6/improvement-plan.json"
        if not plan_path.exists():
            raise SystemExit("Record the one-change improvement plan before running after.")
        plan = json.loads(plan_path.read_text())
        if plan["changed_setting"] != "epochs" or plan["before"] != 3 or plan["after"] != 4:
            raise SystemExit("This runner implements only the declared 3-to-4 epoch comparison.")
        if plan["data_sha256"] != original["labels.csv"] or plan["criteria_sha256"] != original["criteria.md"]:
            raise SystemExit("Dataset or criteria differ from the improvement declaration.")
        before = json.loads((ROOT / "results_three_seeds_before.json").read_text())
        if [r["seed"] for r in before] != [42, 7, 2024]:
            raise SystemExit("Before must contain all three required seeds.")
        epochs = 4
    nb = json.loads((ROOT / "takemeter.ipynb").read_text())
    ns = {"__name__": "__main__"}
    for i in [2, 6, 8]:
        exec("".join(nb["cells"][i]["source"]), ns)
    for i in [12, 14, 16]:
        exec(definitions("".join(nb["cells"][i]["source"])), ns)
    ns["EPOCHS"] = epochs
    if args.run == "after" and any(r["device"] != ns["DEVICE"] for r in before):
        raise SystemExit("Device differs from before.")
    audit = ROOT / "evidence/unit6" / args.run
    audit.mkdir(parents=True, exist_ok=True)
    train_original, evaluate_original = ns["train_model"], ns["evaluate"]

    def train_recorded(*a, **kw):
        gc.collect()
        trainer, tokenizer = train_original(*a, **kw)
        return trainer, tokenizer

    def evaluate_recorded(trainer, tokenizer, test_df, labels, seed=None):
        import numpy as np
        captured = {}
        predict = trainer.predict

        def record_predict(*a, **kw):
            value = predict(*a, **kw)
            captured["output"] = value
            return value

        trainer.predict = record_predict
        try:
            result = evaluate_original(trainer, tokenizer, test_df, labels, seed=seed)
        finally:
            trainer.predict = predict
        output = captured["output"]
        logits = output.predictions
        exps = np.exp(logits - logits.max(axis=-1, keepdims=True))
        probs = exps / exps.sum(axis=-1, keepdims=True)
        predictions = probs.argmax(axis=-1)
        result.update({"run_label": args.run, "base_model": ns["BASE_MODEL"],
            "epochs": epochs, "learning_rate": ns["LEARNING_RATE"],
            "batch_size": ns["BATCH_SIZE"], "max_length": ns["MAX_LENGTH"],
            "labels": labels, "device": ns["DEVICE"], "device_name": ns["DEVICE_NAME"],
            "torch_version": ns["torch"].__version__, "data_sha256": original["labels.csv"],
            "criteria_sha256": original["criteria.md"], "annotation_provenance": provenance,
            "completed_at_utc": datetime.now(timezone.utc).isoformat(),
            "label_counts": dict(counts), "trainer_log_history": trainer.state.log_history})
        tr, va, te = ns["split_dataset"](ns["df"], seed)
        frames = {"train": tr, "validation": va, "test": te}
        split_hashes = {key: [hashlib.sha256(t.encode()).hexdigest() for t in frame.text] for key, frame in frames.items()}
        for a, b in [("train", "validation"), ("train", "test"), ("validation", "test")]:
            assert not set(split_hashes[a]) & set(split_hashes[b]), f"Leakage: {a}/{b}"
        result["splits"] = {key: {"n": len(frame), "label_counts": {k: int(v) for k, v in frame.label.value_counts().items()},
                                  "text_sha256": split_hashes[key]} for key, frame in frames.items()}
        if args.run == "after":
            old = next(r for r in before if r["seed"] == seed)
            assert old["splits"] == result["splits"], "Before/after split changed"
        result["predictions"] = [{"text": str(text), "gold": str(gold),
            "predicted": labels[int(predictions[i])], "confidence": float(probs[i].max()),
            "probabilities": {label: float(probs[i, j]) for j, label in enumerate(labels)}}
            for i, (text, gold) in enumerate(zip(test_df.text, test_df.label))]
        (audit / f"seed-{seed}.json").write_text(json.dumps(result, indent=2) + "\n")
        print(f"Saved audited seed {seed}, epochs={epochs}", flush=True)
        return result

    ns["train_model"], ns["evaluate"] = train_recorded, evaluate_recorded
    # Keep the starter's actual three-seed loop; only its output label changes.
    source = "".join(nb["cells"][19]["source"]).replace('RUN_LABEL = "before"', f'RUN_LABEL = "{args.run}"')
    exec(source, ns)
    for i in [21, 23]:
        exec("".join(nb["cells"][i]["source"]), ns)
    assert original == {f: digest(ROOT / f) for f in protected}, "A protected Unit 5 artifact changed"
    (audit / "protected-files.json").write_text(json.dumps(original, indent=2) + "\n")
    print("Protected Unit 5 artifacts unchanged; all within-seed splits disjoint.")


if __name__ == "__main__":
    main()
