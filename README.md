# TakeMeter — Hacker News AI discussions

**Repository:** https://github.com/winaung786/ai201-project3-takemeter-starter-v2026

**Build status:** Prepared work published with four new commits; student annotation,
acceptance criteria, and training remain pending. This is not a completed Unit 5 submission.
No metric, cold label, human review, or milestone completion is invented.

## What This Does

TakeMeter will classify whole comments from Hacker News AI discussions.
The proposed labels distinguish supported analysis, unsupported statements or
reactions, and direct requests for information. The student selected this community;
the taxonomy is an AI-assisted draft awaiting review. It classifies the support
present in a comment rather than judging whether an opinion is good or a claim true.

## Label Taxonomy

The following taxonomy is an AI-assisted draft awaiting the student's review.
Read the 40-post reading pack before adopting or changing it.

## analysis

**Definition:** A statement supports its main claim with a specific, checkable detail, a concrete first-hand observation, or a cited source.

**Real example 1 — HN 41050420:**
> They're actually updating their license to allow LLAMA outputs for training!
>
> https://x.com/AIatMeta/status/1815766335219249513

**Real example 2 — HN 48087215:**
> I would love for local inference to be possible, but from my experience, Kimi 2.6 is the only model that would be worth it, and its a $10k (M3 Ultra max spec'd - 30s TTFT so kind of slowish) to $30k (RTX6000/700GB+ DDR5) upfront, noise / power consumption aside.

Sources: https://news.ycombinator.com/item?id=41050420 and https://news.ycombinator.com/item?id=48087215.
Classifying the presence of support does not verify whether the support is true.

### unsupported

**Definition:** A comment primarily makes a statement, judgment, joke, agreement, or reaction without specific support for its main point.

**Real example 1 — HN 46990941:**
> It’s just human nature, no big deal. Personally I find it mildly cute.

**Real example 2 — HN 48292641:**
> I agree with that 100%

Sources: https://news.ycombinator.com/item?id=46990941 and https://news.ycombinator.com/item?id=48292641.
This category does not mean false, useless, or bad. A bare factual correction can belong here too.

### question

**Definition:** A comment primarily asks another person for information or clarification without advancing its own answer or advocating a conclusion.

**Real example 1 — HN 47340345:**
> Is it the technology you hate or some of its applications (or both)?

**Real example 2 — HN 41055065:**
> > You also can't use it if you're the government of India.
>
> Why is that?

Sources: https://news.ycombinator.com/item?id=47340345 and https://news.ycombinator.com/item?id=41055065.

### Hardest boundary: analysis versus unsupported

Use only the comment's own text, including material it quotes and links it supplies.
A specific supporting detail must relate to the main claim. A number that only
expresses enthusiasm, such as "I agree 100%", does not count. Naming AI or a model
without evidence does not count. A specific measured result, a concrete experience
with a named tool and outcome, or a directly relevant citation does count.
Heated tone and sarcasm do not remove support that is actually present.
A broad speculation or analogy without a specific supporting observation stays unsupported.

### Question boundary and priority

First ask whether the main purpose is to obtain information without presenting an
answer. If yes, use question. A quotation provided merely to identify what the
question is about is not evidence for the writer's claim. A rhetorical question
that asserts a position, or a comment that answers its own question, follows the
analysis/unsupported rule. If a comment mixes functions, classify the main point;
write a hard-case note when two functions are equally substantial.

### Coverage limitation to test before approval

Standalone facts, jokes and reactions share unsupported. This is broader than
"hot takes" but avoids inventing an opinion where the text contains none.
After reviewing the reading pack, the student should decide whether this distinction
matches what they want TakeMeter to measure. Do not finalize it merely because it
produces neat counts.

### Stretch feature declared before implementation: second training run

Planned: after the student-authored criteria and reviewed labels are committed,
run the default 3-epoch model and one 4-epoch model. Change only the epoch count.
Keep the base model, labeled CSV, stratified split, seed 42, learning rate 2e-5,
batch size 16 and 128-token limit fixed. Compare accuracy, macro F1 and each
label's F1, reporting second minus first. The purpose is to see whether one
extra pass improves this small corpus or overfits it. No run or bonus point is
claimed yet, and the test results will not be used to choose another setting.
The declaration is committed before the comparison runner is implemented.
A fourth label and 50 extra examples for the thinnest label are not declared.

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
No completed hard-case decision is currently claimed.
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
in addition to the starter's metrics and test split. First-run hyperparameters and splitting
logic are unchanged. Results also record settings and file hashes so the declared
second run can reject mismatched data or criteria. The comparison runner is
`python tools/run_epoch_comparison.py --run first`, followed by `--run second`;
both are gated on completed, committed student work. No comparison has run yet. Models and caches remain excluded from Git.

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

Rubric audit: see [docs/rubric-audit.md](docs/rubric-audit.md).
