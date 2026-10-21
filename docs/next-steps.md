# Review status and remaining course steps

Win Aung confirmed having reviewed the current dataset in the project chat. The
confirmation was recorded on 2026-10-20. Root `labels.csv` now has 200 filled labels,
200 human-review markers based on that confirmation, zero blanks and zero pending
review markers. The earlier assistant judgments and reasons remain attributed.
See [the confirmation record](../evidence/human-review-confirmation.json) and
[the original assistant review](../completed_review.html).

Counts are 72 analysis, 81 unsupported and 47 question. All labels meet the
committed 15%–45% balance target. Comment text, row order and label choices did not
change during finalization. The historical AI checkpoints remain historical.

The review confirmation does not establish that the first 20 labels were made
independently before AI answers were seen. No unaided cold labels or second-human
agreement result are added by this update. The three existing hard-case explanations
were written by the assistant; separate student explanations are not recorded.

1. Preserve the finalized CSV and the human-review confirmation. The separate
   offline form starts with its own browser state and can export an incomplete
   worksheet; that export should not overwrite the finalized CSV unless it contains
   actual additional choices or corrections.
2. Provide the independent first-20 evidence and student hard-case explanations
   required by the course, where available. Do not substitute AI labels for an
   unaided cold pass. Collect the separate second-human agreement sample required
   by criterion 4.
3. Run `python tools/validate_submission.py` to inspect outstanding course evidence. Its independent
   cold-label check is unchanged and is not satisfied by a general review confirmation.
4. The five acceptance criteria were committed before scores and remain unchanged.
   Follow RUNNING.md to reproduce the environment. Unit 6 three-seed evaluation
   and the independent second-human agreement measurement remain future work.
5. Both training runs are now complete. Keep results.json, test_split.csv,
   results_second_run.json and results_epoch_comparison.json. See the README for
   actual metrics; the original review-only update preceded these results.

## Training on the confirmed assisted dataset

The disclosed missing unaided cold pass remains a course-evidence gap. It does
not prevent measuring this human-confirmed classifier. The explicit
`--allow-assisted-initial20` runner option verifies the existing confirmation's
CSV hash and every row's ID, text hash and label. It does not waive other data
checks or mark any row cold. See training-provenance.md. The strict submission
validator remains unchanged. Training results will not establish second-human
agreement or three-seed acceptance.
