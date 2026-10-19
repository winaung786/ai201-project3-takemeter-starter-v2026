# Unit 5 rubric audit

This rubric has **20 required points and 3 optional points**. This document is a
check of actual evidence, not an awarded grade or a promise of full credit.

| Category | Points | Evidence required | Current status |
|---|---:|---|---|
| Required evidence and good-faith build | 3 | Root criteria.md with five real criteria; one labeled CSV with text/label/note and at least 150 rows; five populated README sections and at least four new commits | Root files exist and README sections are populated. Five criteria are committed and the commit-count requirement is met. Human annotation, hard-case decisions and training remain pending. |
| Criteria name a target | 5 | Each of five criteria names a numerical target | 5/5 numeric targets supplied by the student and committed at cc8ae32 before training. |
| Criteria testable by another reader | 4 | Each defines data/population, a calculation and an outcome; aggregation/empty-subset handling when relevant | All five state measurements. Remaining clarity issues: criterion 4 leaves sample selection unspecified; criterion 5 needs the maximum-softmax and empty-correct-subset conventions stated before testing. Targets are preserved. |
| Criteria carry a reason | 3 | All five have a reason; at least three reasons specifically reference HN, the chosen labels or actual distribution | 5/5 reasons supplied. Several reference HN examples; final reasons should align with analysis/unsupported/question and the actual reviewed distribution. |
| README taxonomy | 2 | Each label has one sentence and two real examples, plus a hardest-boundary rule | Now included directly in README. Draft still requires student review. |
| README dataset | 2 | Source, actual labeling workflow, real counts per label, three hard cases with decisions | 291 archived; 200 working rows; revised suggestions are 65 analysis, 70 unsupported and 45 question; 20 original cold rows remain blank; no human choices or student hard-case decisions. Replacement IDs, reasons and sampling limitations are documented. |
| README training | 1 | Starting model, actual settings, any change and reason | Default plan documented; no completed run yet. |

## Floor versus target

200 labeled posts is the target. A set of 150–199 can use the course's stop rule
only with an honest README explanation of why the student stopped. The validator
must not silently treat that floor as a failed 200-row requirement, nor count
unlabeled rows as labeled examples. The current file has 200 rows: 180 unreviewed AI suggestions and 20 blank cold rows. These are not 200 completed human-reviewed examples.

## Timing and integrity

- Student authors all five criteria and their numbers, before seeing model results.
- First 20 rows must be labeled cold, without AI help. Pending rows do not count.
- AI pre-labeling of remaining rows is allowed only with individual student review
  and a truthful note. 180 AI proposals now exist; none has a human-review claim.
- No final label may exceed 70%. Use one unsplit CSV; the notebook splits it.
- Keep the test split sealed during preparation. Do not choose another setting
  based on its results. Use validation data when iterating.
- Preserve real milestone history. Four real commits alone do not turn unfinished
  criteria, unreviewed labels or pending training into a finished submission.
- Commit actual results.json and test_split.csv after the training run.
- Use the same GitHub fork for Units 5 and 6: https://github.com/winaung786/ai201-project3-takemeter-starter-v2026. The fork is published; no course-portal submission is claimed.

## Optional points

All-or-nothing: declare an item in README before implementing it; implement it;
then explain its actual effect in README. None is currently earned.

1. Fourth label: needs a real gap in the community, one-sentence definition, two
   examples and an explanation of what the first three missed. Not declared.
2. Second run: declared before implementation. Default 3 epochs versus 4 epochs,
   with every other setting and the data/split unchanged. Keep both metrics files
   and report exact differences. Criteria committed; pending reviewed labels and training.
3. Extra 50: identify the thinnest label from the original labeled file, freeze
   that evidence, declare the collection plan, then collect and review at least
   50 new unique posts for that label. The 260 originally collected posts cannot be
   retroactively described as this stretch feature. Not declared.

## What the student needs to return

The criteria are already committed. Return the 20 independent cold labels, then
review all 180 AI suggestions. Record three actual difficult decisions with both
candidate labels and your reasons. Export and commit the final CSV; training
remains blocked until those real choices exist.
