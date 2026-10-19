# What remains before training

The five student acceptance criteria were committed at cc8ae32 before any scores.
Do not write them again or replace their targets in response to eventual results.

1. Review the draft taxonomy, its examples, reading pack and boundary rule.
2. Download annotation_review.html with GitHub's **Download raw file** control and
   open the downloaded file locally. If you used an older form, download its
   checkpoint before replacing it. The new form can import the older checkpoint
   and retains the first 200 comments' saved choices and manual provenance.
3. Label comments 1–20 independently without AI advice. No AI suggestion exists
   for these rows. This is required by the assignment's cold-label rule.
4. Read each of the remaining 180 comments; compare the AI suggestion with the
   definitions and save your own label. Suggestions alone do not count as human
   review. Record at least three actual hard cases, both possible labels and the
   rule you used. The 47 AI boundary flags are candidates, not your decisions.
5. Download labels.csv, the checkpoint and dataset evidence. Replace labels.csv
   in your repository and commit it; browser saves do not upload to GitHub.
   There are 200 working rows and 60 untouched reserves in sources.json.
6. Check the actual reviewed counts. The required cap is 70%; your criterion 3
   sets 15%–45% (30–90 rows per label). Current AI suggestions include 113
   unsupported rows, so that stricter target is at risk. Never change an accurate
   label to force balance. No final balance result is claimed before review.
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
