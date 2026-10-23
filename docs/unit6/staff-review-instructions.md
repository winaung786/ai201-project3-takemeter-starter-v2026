# Staff exercise — current status and completion

As of 2026-10-22, all 30 labels in [my_staff_labels.csv](../../my_staff_labels.csv) were prepared by Codex at the user's request. Each post has a rule-based explanation in [staff-label-decisions.md](staff-label-decisions.md). Original post text, order, and taxonomy are preserved. [The authorship record](../../evidence/unit6/staff-labels-provenance.json) explicitly records that the labels are AI-assisted, no TF key was accessed, and independent student work has not been demonstrated.

The authentic TF `data/staff_labels.csv` is unavailable. There is no measured agreement or known disagreement set. No final student adjudications are claimed.

## What can be done with the assisted labels

1. Keep this committed version before opening any authentic staff key.
2. Obtain `data/staff_labels.csv` from the TF. Preserve its original provenance and all 30 post IDs.
3. Run `python agreement.py` to calculate an explicitly disclosed AI-to-staff diagnostic. Keep this result separate from criterion 4's independent human-agreement requirement.
4. Use each actual disagreement's full text and both actual labels to consider the strongest rule-based case for each reading. The existing decision record supplies the assistant's initial reasoning, including difficult boundaries.
5. The student must supply the final call, rule-based explanation, and category (a), (b), or (c) for every actual disagreement before a student adjudication report can be claimed complete.

`python tools/complete_staff_agreement.py` is the independent-student route and rejects the recorded AI authorship. This prevents the assistant-prepared file from being counted as independent student evidence. It does not prevent an honestly attributed diagnostic using the starter script.

## Original course requirements

Read [the staff definitions](../../data/staff_taxonomy.md). The course's independent route requires the student's own labels, saved and committed before seeing the TF key, followed by a personal adjudication of every disagreement. An assistant-prepared file cannot establish that evidence, and later review does not retroactively make it an unaided annotation pass.

Valid staff labels remain `analysis`, `hot_take`, and `reaction`. The Hacker News labels `unsupported` and `question` do not belong in this exercise. Preserve every original post unchanged.

The disagreement categories remain: (a) the rule covered the case but was applied loosely; (b) the rule was underspecified; (c) the reading is defensible under an ambiguous rule. Update README Agreement Report and criterion 4 only from evidence actually available; retain the original target.
