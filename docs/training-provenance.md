# Training provenance and the remaining course evidence

The exact dataset and the student's five criteria were committed at fe558f8 before
this training attempt. All 200 choices are bound to the human-review confirmation
by source IDs, labels and text hashes. Neither labels.csv nor criteria.md changed.

The first 20 comments were AI-assisted, and the current evidence does not establish
an unaided human cold pass. The hard-case explanations originated with the
assistant. Model training cannot retrospectively satisfy these course requirements.
The strict submission validator remains unchanged and continues to report that gap.

The explicit training option below permits the disclosed missing-cold-pass condition
only when every label matches the existing human-confirmation record. It retains
all checks for complete labels, review markers, data hashes, duplicates, classes,
criteria, actual hard-case records and committed input files:

```bash
python tools/run_epoch_comparison.py --run first --allow-assisted-initial20
python tools/run_epoch_comparison.py --run second --allow-assisted-initial20
```

No errors other than the zero-cold-rows condition are waived. The default command
remains strict. Results record annotation provenance and do not claim that the
course submission is complete. The extra-epoch comparison was declared before
implementation and before scores; no new setting will be chosen from test scores.

The runner also fixes repository imports when invoked as a script. The notebook
now records the fraction of maximum-softmax confidences below 0.50, needed for
criterion 5. Thresholds and training hyperparameters are unchanged.

The assistant's Linux CPU runtime is separate from the earlier Windows setup.
Actual library versions and the environment check are saved in evidence/. The
starter's stratified split implementation remains unchanged; floating-point
rounding produces 139 training, 31 validation and 30 test comments for this data.
All 200 source comments remain whole in the CSV; the model's 128-token setting can
truncate its input, as in the original starter.
