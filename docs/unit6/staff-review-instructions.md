# Complete the independent staff exercise

1. Read [the staff definitions](../../data/staff_taxonomy.md).
2. Fill the 30 blank labels in [my_staff_labels.csv](../../my_staff_labels.csv) yourself, using only `analysis`, `hot_take`, or `reaction`. Preserve every text byte. Do not use the project labels `unsupported` or `question` here.
3. Save and commit this completed file **before** obtaining or opening the staff key.
4. Ask the TF for `data/staff_labels.csv`; do not invent it or copy a different student's key.
5. Run `python tools/complete_staff_agreement.py`. It validates all 30 rows and calls the starter `agreement.py`.
6. For every disagreement, write the full post, both labels, your call and a reason grounded in a staff rule. Classify it as (a) rule applied loosely, (b) rule underspecified, or (c) defensible ambiguity. AI can argue both sides; your final call must be yours.
7. Add the real rate and adjudications to README Agreement Report and update criterion 4 without changing its target.

The current blank form is preparation, not completed annotation or agreement evidence.
