# Human-only course steps

The assistant's annotation task is complete: root `labels.csv` has 200 filled
labels, a reason per comment, zero pending markers, and three documented hard
cases. See [the completed review](../reviews/2026-10-19-completed/dataset-review.md).
The counts are 72 analysis, 81 unsupported and 47 question, all within 15%–45%.

The checklist below concerns the assignment's separate human-only requirements.
It is not a list of unfinished assistant annotations. Assistant work cannot be
represented as an unaided human cold pass or a second human's agreement result.
No training or evaluation has run.

The five student acceptance criteria were committed at cc8ae32 before any scores.
Do not write them again or replace their targets in response to eventual results.

A historical **AI-only** review of the initial sample is available in
[reviews/2026-10-19-ai/dataset-review.md](../reviews/2026-10-19-ai/dataset-review.md).
It includes 200 AI judgments, three corrections to the original 180 suggestions,
and three explained hard cases. All human steps below remain pending. Do not open
the package's first-20 AI answers before completing your unaided cold pass. Its
checkpoint cannot be imported into the human form, and its CSV must not be mistaken
for a human-reviewed export. The sample was subsequently revised, then the 20
remaining labels were filled in the completed assistant review. See
[balance-revision.md](balance-revision.md) for the earlier sampling change.

1. Review the draft taxonomy, its examples, reading pack and boundary rule.
2. Download annotation_review.html with GitHub's **Download raw file** control and
   open the downloaded file locally. If you used an older form, download its
   checkpoint before replacing it. The new form can import the older checkpoint
   and retains saved choices for matching comment IDs and their manual provenance.
   The 44 new comments stay blank. Keep the original checkpoint as a backup.
3. Label comments 1–20 independently without AI advice. The form shows no AI
   suggestions for these rows; do not consult their historical AI answers.
   This is required by the assignment's cold-label rule.
4. Read each of the remaining 180 comments; compare the AI suggestion with the
   definitions and save your own label. Suggestions alone do not count as human
   review. Record at least three actual hard cases, both possible labels and the
   rule you used. AI boundary flags are candidates, not your decisions.
5. Download labels.csv, the checkpoint and dataset evidence. Replace labels.csv
   in your repository and commit it; browser saves do not upload to GitHub.
   There are 200 working rows and 91 reserves in the 291-comment source archive.
6. Check the actual reviewed counts. The required cap is 70%; your criterion 3
   sets 15%–45% (30–90 rows per label). If all 180 revised suggestions are confirmed,
   any distribution of the 20 cold labels fits that target. Human corrections can
   change it. Never change an accurate label to force balance; calculate final counts.
7. Run python tools/validate_submission.py. Resolve pending markers, missing
   choices, hard-case decisions, duplicates or other data problems before
   splitting. Commit the final criteria and CSV before training.
8. Follow RUNNING.md: activate .venv, install the pinned packages, run python
   test.py, and select that environment's notebook kernel. Use the final label
   map. Run notebook sections 1–5 and commit the actual results.json and
   test_split.csv. No scores have been generated yet.
9. Update README with actual reviewed counts, three decisions, training device,
   settings, split sizes and results. The declared extra-epoch comparison may
   run after the real first run; no bonus is claimed until both are documented.

The independent labels and human reviews must be your work. Everything that can
be prepared without inventing those choices has been provided.
