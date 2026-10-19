# TakeMeter — Hacker News AI discussions

**Repository:** https://github.com/winaung786/ai201-project3-takemeter-starter-v2026

**Annotation status: complete.** All 200 comments now have a label, a specific
review reason, and a source ID in the root `labels.csv`. There are **zero blank
labels and zero pending assistant reviews**. The counts are 72 `analysis` (36%),
81 `unsupported` (40.5%), and 47 `question` (23.5%). All three meet the committed
15%–45% balance target. Three difficult decisions include an alternative label
and the applied rule.

Open [the completed review](completed_review.html) or read
[the decisions and hard cases](reviews/2026-10-19-completed/dataset-review.md).
The [completed checkpoint](reviews/2026-10-19-completed/review-checkpoint.json)
contains every comment and decision.

**Reviewer provenance:** Codex completed these annotations as an AI assistant.
They are not represented as human-reviewed, unaided student labels, or
second-human agreement. The assignment's human-only requirements are not
satisfied by these annotations. The five student criteria are unchanged.
No training or evaluation has run.

**Earlier balance revision (2026-10-19):** Before annotation completion, the 180 AI suggestions contained 65
`analysis`, 70 `unsupported`, and 45 `question` comments. At that stage, the original 20 cold
comments remained blank. Forty-four later comments were replaced
with 13 analyses from the existing reserve and 31 newly collected information
requests from the same eight threads. If human review confirms the 180 suggestions,
every possible distribution of the 20 cold labels fits criterion 3's 30–90-per-label
range. The subsequently completed assistant annotations have the actual counts above.
The revision is documented in [the selection manifest](collection/selection-manifest.json)
and [balance report](docs/balance-revision.md).

**Historical AI review of the initial sample (2026-10-19):** A separate, disclosed AI pass made 20 judgments
before reading the existing suggestions, then reviewed all 180 suggestions and
recorded three hard cases. It confirmed 177 suggestions and corrected rows 26, 82,
and 101. The full AI draft contains 59 `analysis`, 125 `unsupported`, and 16
`question` labels; that initial sample failed criterion 3's 15%–45% balance target
and prompted the later sampling revision above. See the historical
[review report](reviews/2026-10-19-ai/dataset-review.md),
[AI-draft CSV](reviews/2026-10-19-ai/labels.csv), and
[AI checkpoint](reviews/2026-10-19-ai/review-checkpoint.ai.json).
These historical files describe the initial sample, not the current completed CSV.
Their checkpoint uses a separate schema and cannot be imported as human choices.

**Current files:** `labels.csv` is the completed annotated dataset;
`completed_review.html` shows all saved decisions. The separate
`annotation_review.html` remains available for actual human choices if the course's
human-only requirements are to be completed. Its blank human state is not the
status of the completed assistant review.

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

**Source:** The original collection contained 260 distinct complete comments from
eight public Hacker News AI threads. The later balance revision added 31 new
comments from those same threads using the public Algolia HN API. The archive now
contains 291 comments with original HTML, collection metadata, IDs and text hashes.
The working `labels.csv` retains 156 original examples, including all first 20,
and replaces 44 later examples with 13 reserve analyses and 31 new questions.
The remaining 91 archived comments are reserves, not a test set. No included
comment is shortened. `collection/selection-manifest.json` records every change.

**Sampling:** Collection rotated through eight comment trees. Whole comments of
5–180 words were eligible; blank/deleted and normalized duplicates were excluded.
The revised working sample is deliberately enriched by proposed class. It must
not be used to estimate label prevalence across HN. No model score or test split
was used to select replacements. This short-comment sample is not representative
of every HN post. Related replies
may fall in different random splits under the unchanged notebook, so the eventual
score can overstate transfer to entirely new threads.

**Labeling process:** Codex saved judgments for the initial 20 before opening the
prior suggestions, reviewed all 180 suggestions individually, and read the 44
replacement comments with individual reasons. It then finalized all 200 current
labels at the user's request. Every root CSV row is marked `assistant_reviewed`;
none has a pending marker or a fabricated human-review marker. The initial-20
batch is not claimed as an unaided human cold pass. The complete review checkpoint
preserves the reviewer, source text, label and reason for every row.

| Label | Completed assistant annotations | Share |
|---|---:|---:|
| analysis | 72 | 36.0% |
| unsupported | 81 | 40.5% |
| question | 47 | 23.5% |
| **Total** | **200** | **100%** |

**Balance finding:** Criterion 3 requires 15%–45% per label in the final 200 rows
(30–90 examples per label). The completed counts of 72, 81 and 47 meet it.
All classes are also below the assignment's 70% cap. The class-enriched sampling
revision is disclosed above; no existing comment was relabeled to force balance.

**Completed hard cases:** Row 26 is `question` rather than `unsupported` because
the writer asks for a reason without supplying an answer. Row 78 is `unsupported`
rather than `analysis` because quoted detector statistics support the rejected
position, not the writer's rejection. Row 170 is `question` rather than
`unsupported` because its tentative free-trial edit leaves the request unresolved.
The full comments, alternatives and applied rules are in the completed review
report and the corresponding CSV notes. These are assistant decisions.

The CSV remains one unsplit file with all 200 labels complete. The course submission
validator continues to require actual human evidence; it does not mistake assistant
annotations for human work. Current and original AI proposals remain archived.
The separate human form imports actual earlier choices by comment ID, preserving
unchanged comments and leaving replacements blank in that human workflow.

## The Training Run

**Status:** No training, practice training, or evaluation has run. results.json and
test_split.csv do not yet exist. No test split has been created or examined.

**Planned base model:** distilbert-base-uncased.
**Defaults:** 3 epochs, learning rate 2e-5, batch size 16, maximum 128 tokens, seed 42.
**Planned split:** The starter notebook creates stratified 70/15/15 partitions from
one unsplit labels.csv. Actual split sizes and per-label counts are not available yet.

**Verified local Windows environment:** Python 3.12.14, CPU, all six required packages
installed in `.venv`; `test.py` reported 9 passed and 0 failed. The Unit 6 baseline
model has not been downloaded and produces the expected cache warning. See
`evidence/windows-environment-ready.json` for exact versions. Earlier Linux checks
remain historical evidence. Environment readiness is not a completed training run.

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
boundary candidates. The first 20 remain blank in the student workflow. No AI suggestion
is claimed as a human-reviewed or cold choice. Human review has not occurred.
ChatGPT also updated the offline review form to preserve this provenance and show
the student's already-committed criteria, rather than ask for them again.

**Second AI review disclosure:** At the student's request, ChatGPT (Codex) saved
20 initial AI judgments before opening the original 180 suggestions, then read and
reviewed those 180 comments individually. Reasons, three hard-case alternatives
and applied rules, source IDs, hashes, and the three corrections are recorded in
`reviews/2026-10-19-ai/`. This is an AI-to-AI review, not the required human cold
pass, human confirmations, student hard-case evidence, or second-human agreement.
That historical AI review changed no source comment, root CSV label, criterion,
form state, or training gate.

**Balance revision disclosure:** After the initial AI draft missed criterion 3,
ChatGPT screened additional whole comments from the same eight threads, selected
31 real information requests with individual reasons, and reused 13 previously
archived analyses. It replaced 44 later unsupported examples before any training
or split. The first 20 comments and the five student criteria are unchanged.
This is purposive sampling with AI suggestions; no human review or final balanced
dataset is claimed. It is not the optional extra-50 feature. Existing checkpoints
can be imported by comment ID so earlier human choices are preserved when applicable.

**Completed annotation disclosure:** The user then explicitly asked Codex to finish
the review rather than leave blank labels and pending flags. Codex finalized all
200 labels, retained a comment-specific reason for each, and recorded three complete
hard-case decisions. The root CSV now has zero blanks and zero pending markers.
All work is accurately attributed to the assistant; no human cold-label or
agreement claim was added. See `evidence/annotation-status.json` and the completed
review checkpoint for the current status.

See [docs/next-steps.md](docs/next-steps.md) for the student steps needed to finish.
The original README, including the Unit 6 templates, is retained at
docs/starter-README.md. RUNNING.md is the official command reference.

Rubric audit: see [docs/rubric-audit.md](docs/rubric-audit.md).
