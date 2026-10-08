"""Run the declared Unit 5 comparison using the starter notebook's own code.

Run first:  python tools/run_epoch_comparison.py --run first
Run second: python tools/run_epoch_comparison.py --run second
No model is imported until reviewed data and committed criteria pass preflight.
"""
import argparse
import ast
import hashlib
import json
import os
import re
from pathlib import Path

from validate_submission import ROOT, validate


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def settings(notebook):
    selected = {}
    for node in ast.parse("".join(notebook["cells"][6]["source"])).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            selected[node.targets[0].id] = ast.literal_eval(node.value)
    return {"base_model": selected["BASE_MODEL"], "epochs": selected["EPOCHS"],
            "learning_rate": selected["LEARNING_RATE"], "batch_size": selected["BATCH_SIZE"],
            "max_length": selected["MAX_LENGTH"], "seed": selected["SEED"], "labels": selected["LABELS"]}


def comparison(first, second):
    measures = {"Overall accuracy": (first["accuracy"], second["accuracy"]),
                "Macro F1": (first["f1_macro"], second["f1_macro"])}
    for label in first["labels"]:
        measures[f"F1 — {label}"] = (first["per_label"][label]["f1"], second["per_label"][label]["f1"])
    report = {"changed_hyperparameter": "epochs", "first_epochs": 3, "second_epochs": 4,
              "fixed_settings": {k: first[k] for k in ("base_model", "learning_rate", "batch_size", "max_length", "seed", "labels")},
              "data_sha256": first["data_sha256"], "criteria_sha256": first["criteria_sha256"],
              "first_metrics_file": "results.json", "second_metrics_file": "results_second_run.json",
              "measures": {name: {"first": a, "second": b, "second_minus_first": b-a} for name, (a,b) in measures.items()}}
    lines = ["### Declared epoch comparison — actual results", "",
             "Only epochs changed, from 3 to 4. Both runs used the same labeled CSV,",
             "criteria, stratified split, seed and remaining hyperparameters. No further",
             "setting was selected using these test results.", "",
             "| Measure | 3 epochs | 4 epochs | Second minus first |", "|---|---:|---:|---:|"]
    lines.extend(f"| {name} | {a:.6f} | {b:.6f} | {b-a:+.6f} |" for name, (a,b) in measures.items())
    lines += ["", "These differences measure one predeclared comparison on one split. They",
              "do not establish a reliable improvement across seeds. Unit 6 evaluates that."]
    return report, "\n".join(lines) + "\n"


def training_summary(namespace, stage):
    run = namespace["results"]
    lines = ["## The Training Run", "",
             "**Status:** " + ("Both predeclared training runs completed." if stage == "second" else "The first training run completed; the declared second run remains pending."), "",
             f"**Starting model:** {run['base_model']}",
             f"**Settings used:** seed {run['seed']}, learning rate {run['learning_rate']}, batch size {run['batch_size']}, maximum {run['max_length']} tokens.",
             "**Epochs:** " + ("3 in the first run, 4 in the second." if stage == "second" else "3 in the first run."),
             f"**Device:** {run['device']} ({run['device_name']}), PyTorch {run['torch_version']}.", "",
             "**Hyperparameter change and reason:** " + ("Only epochs changed, from 3 to 4, to test whether an extra pass helps this small corpus or overfits it. This was declared in README before implementation." if stage == "second" else "No hyperparameter changed from the defaults in this first run."), "",
             f"**Split sizes:** train {len(namespace['train_df'])}, validation {len(namespace['val_df'])}, test {len(namespace['test_df'])}.", "",
             "| Label | Train | Validation | Test |", "|---|---:|---:|---:|"]
    table = namespace["table"]
    for label in run["labels"]:
        lines.append(f"| {label} | {int(table.loc[label, 'train'])} | {int(table.loc[label, 'val'])} | {int(table.loc[label, 'test'])} |")
    thin = [label for label in run["labels"] if int(table.loc[label, "test"]) < 8]
    if thin:
        lines += ["", "Labels with fewer than 8 test examples: " + ", ".join(thin) + ". Their metrics may move sharply between seeds."]
    lines += ["", "**Saved evidence:** results.json and test_split.csv" + (", results_second_run.json and results_epoch_comparison.json." if stage == "second" else "."),
              "Criteria and labels passed the committed-file check before training. Results record the data and criterion hashes. The CSV was not manually pre-split."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", choices=("first", "second"), required=True)
    args = parser.parse_args()
    errors, _ = validate()
    if errors:
        raise SystemExit("Student work must be completed before training:\n" + "\n".join(errors))
    os.chdir(ROOT)
    notebook = json.loads((ROOT / "takemeter.ipynb").read_text())
    config = settings(notebook)
    declared = {"base_model": "distilbert-base-uncased", "epochs": 3, "learning_rate": 2e-5, "batch_size": 16, "max_length": 128, "seed": 42}
    if any(config[key] != value for key, value in declared.items()):
        raise SystemExit("The predeclared comparison uses the original default settings. Do not silently change its experiment.")
    out = ROOT / ("results.json" if args.run == "first" else "results_second_run.json")
    if out.exists():
        raise SystemExit(f"{out.name} already exists. This runner will not overwrite test evidence.")
    first = None
    if args.run == "second":
        if not (ROOT / "results.json").exists() or not (ROOT / "test_split.csv").exists():
            raise SystemExit("Complete the first run and keep results.json and test_split.csv first.")
        first = json.loads((ROOT / "results.json").read_text())
        expected = dict(config, data_sha256=digest(ROOT / "labels.csv"), criteria_sha256=digest(ROOT / "criteria.md"))
        for key, value in expected.items():
            if first.get(key) != value:
                raise SystemExit(f"First-run {key} differs or lacks recorded metadata; do not compare unmatched runs.")
    namespace = {"__name__": "__main__"}
    # Sections 1–5 only. Unit 6's three-seed cells are deliberately excluded.
    for index in (2, 4, 6, 8, 10, 12, 14, 16):
        source = "".join(notebook["cells"][index]["source"])
        if args.run == "second" and index == 14:
            namespace["EPOCHS"] = 4
            if namespace["DEVICE"] != first.get("device"):
                raise SystemExit("Use the same training device as the first run for this comparison.")
            print("Predeclared second run: epochs=4; all other settings stay fixed.")
        if args.run == "second" and index == 16:
            source = source.replace('"results.json"', '"results_second_run.json"')
            source = source.replace('test_df.to_csv("test_split.csv", index=False)',
                                    'assert test_df.to_csv(index=False) == Path("test_split.csv").read_text(), "Test split changed"')
            source = source.replace('"models/takemeter"', '"models/takemeter_second"')
            source = source.replace("Wrote results.json and test_split.csv.",
                                    "Wrote results_second_run.json; verified the existing test_split.csv.")
        exec(compile(source, f"takemeter.ipynb:cell-{index}", "exec"), namespace)
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text()
    if not re.search(r"^## The Training Run\n[\s\S]*?(?=\n## How I Used AI)", readme, re.M):
        raise SystemExit("Metrics saved. The README section boundaries changed; insert an actual run summary manually.")
    readme = re.sub(r"^## The Training Run\n[\s\S]*?(?=\n## How I Used AI)", lambda _: training_summary(namespace, args.run), readme, count=1, flags=re.M)
    readme_path.write_text(readme)
    if args.run == "second":
        second = json.loads(out.read_text())
        report, markdown = comparison(first, second)
        (ROOT / "results_epoch_comparison.json").write_text(json.dumps(report, indent=2) + "\n")
        (ROOT / "docs/epoch-comparison.md").write_text(markdown)
        readme = readme_path.read_text()
        marker = "\n## How I Used AI"
        if marker not in readme:
            raise SystemExit("Metrics saved. Insert docs/epoch-comparison.md into the README's Training Run section.")
        readme_path.write_text(readme.replace(marker, "\n" + markdown + marker, 1))
        print("Saved the actual comparison and inserted it into the README Training Run section.")


if __name__ == "__main__":
    main()
