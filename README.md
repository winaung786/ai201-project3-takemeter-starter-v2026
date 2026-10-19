# TakeMeter — Hacker News AI discussions

**Repository:** https://github.com/winaung786/ai201-project3-takemeter-starter-v2026

**Build status:** The student's five criteria are committed. The working dataset now
contains 200 complete comments: 20 untouched cold rows and 180 AI-pre-labeled rows
awaiting individual human review. No training or evaluation has run. This is not
ready for submission yet.

**Next action:** Download `annotation_review.html` using GitHub's **Download raw file**
button and open it locally in your browser. Label comments 1–20 independently, then
read and confirm or correct each remaining suggestion. Download the resulting
`labels.csv`, checkpoint and dataset evidence. Replace the repository's CSV with the
exported file and commit it. Saving in the form alone does not update GitHub.

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

**Source:** 260 distinct complete comments were collected from eight public Hacker
News AI threads with the public Algolia HN API. The working `labels.csv` uses the
first 200 in their original collection order, selected without using suggested
labels or model scores. The remaining 60 are reserves in `collection/sources.json`,
not a pre-split test set. Sources, original HTML, collection times, IDs and text
hashes for all 260 remain in that archive. No included comment is shortened.

**Sampling:** Collection rotated through eight comment trees. Whole comments of
5–180 words were eligible; blank/deleted and normalized duplicates were excluded.
This short-comment sample is not representative of every HN post. Related replies
may fall in different random splits under the unchanged notebook, so the eventual
score can overstate transfer to entirely new threads.

**Labeling process:** On 2026-10-19, ChatGPT read comments 21–200 and proposed a label
and rationale for each. Comments 1–20 remain blank with `cold_pending`; no AI labels
were supplied for them. The other 180 rows have `ai_prelabel; review_pending` notes.
There are currently **zero human-reviewed choices**. Every suggestion must be read
and individually confirmed or corrected by the student. The form starts with no
saved choices and shows suggestions only after the independent batch is saved.

| Label or status | AI suggestions, not human-reviewed | Human-reviewed choices |
|---|---:|---:|
| analysis | 53 | 0 |
| unsupported | 113 | 0 |
| question | 14 | 0 |
| Cold rows awaiting student choice | 20 blank | 0 |
| **Total working rows** | **200 (180 suggested + 20 blank)** | **0** |

**Balance finding:** Criterion 3 requires 15%–45% per label in the final 200 rows
(30–90 examples per label). The 113 current `unsupported` suggestions already
exceed that ceiling; this is an initial warning, not a final verdict based on human
labels. Do not change a label just to hit a target. Review the text honestly and
report the final distribution. The assignment's separate maximum remains 70%.

**Hard cases:** `collection/ai-suggestions.json` contains 47 AI boundary flags with
both candidate labels and an AI rationale. For example, comment 26 is a possible
rhetorical question; comment 78 quotes detector statistics but rejects them without
new support; comment 170 asks for recommendations and then mentions a tentative
trial. These are **AI candidates**, not completed student decisions. The student
must record at least three actual difficult choices, name the alternative and
explain the applied rule. The form exports only saved student hard-case decisions.

The CSV remains one unsplit file. Training is deliberately blocked until the first
20 real cold choices, all human reviews and at least three hard cases are saved and
committed. `collection/ai-suggestions.json` preserves the AI's original proposals
and explanations even when the student changes a label.

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

**Pre-labeling disclosure:** ChatGPT pre-labeled comments 21–200 on 2026-10-19,
using the draft definitions and text alone; it supplied reasons and marked 47
boundary candidates. The first 20 remain unaided and unlabeled. No AI suggestion
is claimed as a human-reviewed or cold choice. Human review has not occurred.
ChatGPT also updated the offline review form to preserve this provenance and show
the student's already-committed criteria, rather than ask for them again.

See [docs/next-steps.md](docs/next-steps.md) for the student steps needed to finish.
The original README, including the Unit 6 templates, is retained at
docs/starter-README.md. RUNNING.md is the official command reference.

Rubric audit: see [docs/rubric-audit.md](docs/rubric-audit.md).
