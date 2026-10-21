# Unit 6 plan — recorded before baseline scores

Prediction: The trained model will beat the zero-shot baseline on `unsupported` F1 because it has seen Hacker News agreement, jokes, and bare statements assigned to this deliberately broad category.

Compare `facebook/bart-large-mnli` using the exact README definitions against the original three-epoch `results.json` on all 30 unchanged posts in `test_split.csv`; do not cap or sample.

Run the notebook training functions at seeds 42, 7, and 2024, initially with three epochs, learning rate 2e-5, batch size 16, and maximum length 128. Keep the dataset, taxonomy, criteria, split procedure, and hardware fixed. Choose and record one improvement after the before diagnosis and before the after run. Do not overwrite Unit 5 artifacts.

No optional stretch features are declared. The confidence measurements are necessary for original criterion 5; they are not a new stretch claim. Do not run a second improvement or tune repeatedly against the test set.

Criterion 3 measures the entire unchanged 200-comment dataset; repeat that seed-independent measurement in each column. Criterion 4 is a human reference-label exercise, not a model prediction metric; its value must not be invented or multiplied into three trials. Until genuine student labels and the staff reference are available, report it as MISSED — not demonstrated, with no numeric agreement rate. Softmax confidence for criterion 5 is the largest class probability; average only correct test predictions and count probabilities strictly below 0.50 over all test predictions. A seed passes criterion 5 only if both original thresholds hold.

The staff exercise uses `data/staff_taxonomy.md`, not the Hacker News taxonomy. `my_staff_labels.csv` is a blank, unchanged-text form for the student. The student must complete all 30 before the TF supplies `data/staff_labels.csv`. No AI-generated human answers, staff labels, agreement rate, or student adjudications will be substituted.
