# TakeMeter — Hacker News AI discussions

**Build status:** Preparation complete; student annotation, acceptance criteria,
GitHub fork, and training remain pending. This is not a completed Unit 5 submission.
No metric, cold label, human review, or milestone completion is invented.

## What This Does

TakeMeter will classify whole comments from Hacker News AI discussions.
The proposed labels distinguish supported analysis, unsupported statements or
reactions, and direct requests for information. The student selected this community;
the taxonomy is an AI-assisted draft awaiting review. It classifies the support
present in a comment rather than judging whether an opinion is good or a claim true.

## Label Taxonomy

The complete definitions, two real examples per label, source links, and boundary
rules are in [docs/taxonomy-draft.md](docs/taxonomy-draft.md). The student should
confirm or revise them after reading [the 40-post pack](collection/reading-pack.md).

| Proposed label | One-sentence definition |
|---|---|
| analysis | A statement supports its main claim with a specific, checkable detail, a concrete first-hand observation, or a cited source. |
| unsupported | A comment primarily makes a statement, judgment, joke, agreement, or reaction without specific support for its main point. |
| question | A comment primarily asks another person for information or clarification without advancing its own answer or advocating a conclusion. |

**Hardest boundary:** analysis versus unsupported. A detail must support the main
claim. A number expressing agreement does not count; a concrete measured experience
or relevant citation does. Sarcasm does not remove evidence actually present.
An information request is question only when it does not advance its own answer.
The exact benchmark-specificity boundary needs student review before labeling.

The eight generated boundary posts in docs/boundary-stress-test.md are synthetic
and excluded from all data and results. No stretch feature is currently claimed.

## The Dataset

**Source:** 260 distinct complete comments from eight public Hacker News AI threads,
collected using the public Algolia HN API. Each comment is one collection unit.
Sources, original HTML, collection time, IDs and exact-text hashes are retained in
collection/sources.json. Rendering HTML as readable plain text preserves the whole
comment's visible wording. No included comment is shortened.

**Sampling:** Round-robin through eight comment trees. Whole comments of 5–180 words
are eligible. Blank/deleted and normalized duplicate text are excluded. This short
comment sample is not representative of every HN post. Related replies may be placed
in different random splits by the unchanged notebook, so the held-out score measures
within-community performance and can overstate transfer to entirely new threads.

**Annotation:** No posts are labeled yet. The first 20 are reserved as cold_pending,
not marked cold. The offline annotation form supplies no suggested labels. After
these 20 are labeled by the student without AI assistance, the remaining posts may
be manually labeled or AI pre-labeled and individually reviewed by the student.
Workflow notes must reflect what actually happened.

| Label or status | Count | Share of all collected posts |
|---|---:|---:|
| analysis | 0 | 0% |
| unsupported | 0 | 0% |
| question | 0 | 0% |
| Unlabeled | 260 | 100% |
| **Total collected** | **260** | **100%** |

Label balance cannot be assessed yet. No final label may exceed 70%.
Three real candidate hard cases are documented in docs/hard-case-candidates.md.
The student's actual decisions and explanations must replace candidates before
submission; they are not claimed as completed annotations.

## The Training Run

**Status:** No training, practice training, or evaluation has run. results.json and
test_split.csv do not yet exist. No test split has been created or examined.

**Planned base model:** distilbert-base-uncased.
**Defaults:** 3 epochs, learning rate 2e-5, batch size 16, maximum 128 tokens, seed 42.
**Planned split:** The starter notebook creates stratified 70/15/15 partitions from
one unsplit labels.csv. Actual split sizes and per-label counts are not available yet.

**Verified environment:** Python 3.12.14, CPU, 9 passed and 0 failed in test.py.
The expected Unit 6 baseline-cache warning remains. See evidence/environment-check.txt,
evidence/notebook-setup.txt and evidence/package-versions.json. This is the assistant's
Linux runtime, not proof of the student's own device or notebook setup.

**Changes from the starter:** A pre-training guard stops unfinished annotation and
criteria from producing results. Notebook instructions that incorrectly referred to
a hosted connection or automatic pushes were corrected. The name is Win Aung and
email remains blank because it was not provided. The proposed label map is configured
in section 2. Section 5 saves the actual model and tokenizer under models/takemeter
in addition to the starter's metrics and test split. Hyperparameters and splitting
logic are unchanged. Models and caches remain excluded from Git.

## How I Used AI

**Moment 1 — assistance already provided:** The student asked ChatGPT to work on the
project under the PPT and assignment rules. ChatGPT read the 29 slides and official
starter, collected 260 public comments, and read a separate 40-post sample. It proposed
three labels and a decision rule. The student's review and revisions are pending.

**Moment 2 — assistance already provided:** ChatGPT generated eight synthetic boundary
cases and an offline review form with blank criterion fields and no label suggestions.
It configured and verified the environment and added a training check. The student's
responses to the boundary cases and changes to definitions are pending.

**Pre-labeling disclosure:** None has occurred. No row is falsely described as cold,
human-reviewed, or AI-pre-labeled. Update this disclosure after the actual workflow.

See [docs/next-steps.md](docs/next-steps.md) for the student steps needed to finish.
The original README, including the Unit 6 templates, is retained at
docs/starter-README.md. RUNNING.md is the official command reference.
