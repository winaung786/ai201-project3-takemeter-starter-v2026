# Student steps required before training

1. Read the 40-post reading pack and edit or confirm the proposed taxonomy. It must
   describe a distinction you want to measure. Read the eight synthetic boundary
   examples, which are not training data.
2. Write five acceptance criteria in your own words, each with a numeric target and
   a reason. Cover at least three areas from accuracy, per-label performance,
   balance, consistency, confidence. State the evaluation set, calculation, and
   what happens if the relevant subset is empty. The review form provides blank
   fields; it does not choose targets. Return your criteria for a check of whether
   another person can measure them.
3. Label the first 20 posts without AI advice. The form offers no predictions.
   Saving a choice marks that row cold. No existing row is claimed to be cold.
4. After those 20, either label the rest manually or request AI pre-labeling. If
   pre-labeled, read and correct every row and retain that disclosure in note.
   Record at least three hard cases. Export labels.csv and your review checkpoint.
5. Commit the reading, then taxonomy, then student-authored criteria, then reviewed
   labels as actual milestone commits. Keep criteria and labels committed before
   running section 4. At least four new commits are required; do not manufacture
   completed milestones from drafts. Use a fork of the official starter and keep
   that same repository for Unit 6.
6. Activate .venv, run python test.py, and open takemeter.ipynb with that kernel.
   Use your finalized labels in LABELS. Run sections 1–5 only. Do not inspect
   test texts while choosing labels or settings. Commit results.json and
   test_split.csv after section 5. Model files are saved to models/takemeter;
   notebook defaults remain 3 epochs, 2e-5, batch 16, 128 tokens, seed 42.
7. Finish the five README sections with your actual counts, hard-case choices,
   training device, settings, split counts and two specific AI interactions.
   No stretch feature is currently claimed. Save any actual errors honestly.

The project is prepared but not ready for submission until these steps are complete.
