# Balance revision before human annotation

The first AI review of the original 200-comment sample gave 59 analysis, 125
unsupported and 16 question labels. Unsupported was 62.5% and question was 8.0%,
outside the student's committed 15%–45% target. That result is preserved in
`reviews/2026-10-19-ai/`; it is historical evidence for the initial sample.

The current working sample keeps the original 20 cold comments unchanged and
blank. It replaces 44 later unsupported examples with 13 concrete analyses from
the original reserve and 31 new information requests from the same eight threads.
The replacements were read in full and given individual AI reasons. No existing
comment was relabeled to force the distribution.

| Current status | Analysis | Unsupported | Question | Blank cold rows |
|---|---:|---:|---:|---:|
| AI proposals requiring human review | 65 | 70 | 45 | 20 |
| Possible final count if the 180 proposals are confirmed | 65–85 | 70–90 | 45–65 | 0 |
| Possible share of the final 200 | 32.5%–42.5% | 35.0%–45.0% | 22.5%–32.5% | 0% |

These are conditional ranges, not completed human labels. All 231 possible ways
to distribute 20 cold choices across the three labels fit the target when the 180
proposals are confirmed. Human corrections can change the outcome, so the final
distribution must be calculated after review. The student criteria are unchanged.

## Sources and selection

`collection/sources.json` retains the original 260 records and appends the 31 new
records, for 291 total. Original HTML and text hashes are retained. The working
CSV contains 200 distinct complete comments; the other 91 are reserves.

New candidates came from the same eight public Algolia HN comment trees. A screen
found 1,555 previously unarchived comments of 5–90 words containing a question
mark and an interrogative word. The first 180 candidates in round-robin traversal
order were read. Thirty-one information requests were selected, with alternatives
noted for ambiguous cases. The punctuation screen alone did not assign labels.
The 13 reserve analyses contain concrete observations or relevant references.
Every included comment still meets the original 5–180-word whole-comment rule.

`collection/selection-manifest.json` lists every removed and replacement ID, row,
source, rationale and text hash. Replacements occupy the final 44 unsupported
AI-draft positions after row 20, excluding the three recorded boundary cases.
The first 20 comments and the cases at rows 26, 78 and 170 are retained.

This is purposive sampling to improve class coverage. It does not estimate HN's
natural label prevalence. Related replies may cross the notebook's random split;
high scores would not establish transfer to unseen threads. No train, validation,
or test split or model scores were consulted. This revision does not claim the
optional extra-50 feature: 13 replacements were already in the original reserve.

## Human review and training status

The regenerated `annotation_review.html` starts with zero human choices. It hides
all AI suggestions until the 20 cold labels have been saved. Earlier human
checkpoints can be imported by comment ID: choices for the 156 retained comments
are preserved, while new comments stay blank. The form uses a new local save key
so old choices cannot silently attach to different comments at the same row.

The form was checked in memory for cold gating, ID-based checkpoint migration,
atomic rejection of invalid checkpoints, and exclusion of the separate AI-review
checkpoint. Test choices were not written to a user checkpoint or counted as
human evidence. The resulting CSV still requires the student's real choices and
three real hard-case notes before training.

The Windows environment is installed and checked: `test.py` reported 9 passed and
0 failed, with a warning that the Unit 6 baseline model has not yet downloaded.
See `evidence/windows-environment-ready.json`. No training or evaluation has run;
the existing submission gate remains active.
