# TakeMeter — Hacker News AI discussions

**Repository:** https://github.com/winaung786/ai201-project3-takemeter-starter-v2026

**Unit 6:** Baseline, all six training trials, and the measured improvement are complete; the authentic TF reference and AI-to-staff comparison are saved, and the delegated AI-assisted adjudication is complete. Independent human annotation evidence and independently written student adjudication are not demonstrated.

**Build status: human review confirmed; both training runs completed.** All 200 comments have a label,
an assistant review reason, and a source ID in the root `labels.csv`. On 2026-10-20,
Win Aung confirmed having reviewed the dataset and asked for finalization. All 200
labels are now marked `human_reviewed`, with the earlier AI assistance preserved.
There are **zero blank labels and zero pending review markers**. The counts are 72 `analysis` (36%),
81 `unsupported` (40.5%), and 47 `question` (23.5%). All three meet the committed
15%–45% balance target. Three difficult decisions include an alternative label
and the applied rule.

Open [the original assistant review](completed_review.html) or read
[the decisions and hard cases](reviews/2026-10-19-completed/dataset-review.md).
The [original assistant checkpoint](reviews/2026-10-19-completed/review-checkpoint.json)
contains every comment and decision.

**Reviewer provenance:** Codex prepared the annotations and explanations. Win Aung
subsequently confirmed review of all 200 current labels in the project chat. That
confirmation is recorded in [the human-review record](evidence/human-review-confirmation.json),
which binds the reviewed comment IDs and labels to this dataset. The review date itself
was not supplied; 2026-10-20 is the date the confirmation was recorded. This records
human review after AI assistance, without claiming an unaided cold pass or a second
human agreement result. The five student criteria are unchanged. Both predeclared training runs have
completed on the confirmed labels; see The Training Run below.

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

**Current files:** `labels.csv` is the finalized dataset with all 200 labels marked
human-reviewed on the basis of Win Aung's confirmation. `completed_review.html` preserves
the original assistant decisions and explanations from before that confirmation.
The current human-review status is recorded in `evidence/annotation-status.json`
and `evidence/human-review-confirmation.json`. The separate `annotation_review.html`
keeps its own browser state; its blank fields do not describe the finalized CSV
or replace the recorded confirmation. The dated review folders preserve historical
AI checkpoints.

## What This Does

TakeMeter will classify whole comments from Hacker News AI discussions.
The proposed labels distinguish supported analysis, unsupported statements or
reactions, and direct requests for information. The student selected this community;
the taxonomy was drafted with AI assistance and is used for the reviewed labels. It classifies the support
present in a comment rather than judging whether an opinion is good or a claim true.

## Label Taxonomy

The following AI-assisted taxonomy defines the labels used for the human-confirmed
dataset and both training runs. The reading pack records the source examples.

### analysis

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
labels at the user's request. Win Aung then confirmed having reviewed the dataset
and asked for finalization. Every current CSV row is marked `human_reviewed` with
`human_review_basis=user_confirmation`, while preserving `assistant_reviewed` and the
original assistant reason. No comment text or label changed during finalization.
The initial-20 batch is not claimed as an unaided human cold pass. The original
checkpoint and the new human-review record preserve both stages.

| Label | Final labels accepted after human review | Share |
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
report and the corresponding CSV notes. The explanations were written by the assistant;
the current labels are accepted under the user's subsequent review confirmation.

The CSV remains one unsplit file with all 200 labels complete. The course submission
validator continues to require actual human evidence; it does not mistake assistant
annotations for human work. Current and original AI proposals remain archived.
The separate human form imports actual earlier choices by comment ID, preserving
unchanged comments and leaving replacements blank in that human workflow.

## The Training Run

**Status:** Both predeclared training runs completed.

**Starting model:** distilbert-base-uncased
**Settings used:** seed 42, learning rate 2e-05, batch size 16, maximum 128 tokens.
**Epochs:** 3 in the first run, 4 in the second.
**Device:** cpu (CPU), PyTorch 2.6.0+cpu.

**Hyperparameter change and reason:** Only epochs changed, from 3 to 4, to test whether an extra pass helps this small corpus or overfits it. This was declared in README before implementation.

**Split sizes:** train 139, validation 31, test 30.

| Label | Train | Validation | Test |
|---|---:|---:|---:|
| analysis | 50 | 11 | 11 |
| unsupported | 56 | 13 | 12 |
| question | 33 | 7 | 7 |

Labels with fewer than 8 test examples: question. Their metrics may move sharply between seeds.

**Saved evidence:** results.json and test_split.csv, results_second_run.json and results_epoch_comparison.json.
Criteria and labels passed the committed-file check before training. Results record the data and criterion hashes. The CSV was not manually pre-split.

**Annotation limitation:** Labels were human-confirmed after AI assistance. No unaided first-20 cold pass is recorded, and hard-case explanations originated with the assistant. Training does not establish that the full course submission is complete.
**Execution environment:** This run used the assistant Linux CPU runtime, distinct from the earlier Windows setup evidence.

### Declared epoch comparison — actual results

Only epochs changed, from 3 to 4. Both runs used the same labeled CSV,
criteria, stratified split, seed and remaining hyperparameters. No further
setting was selected using these test results.

| Measure | 3 epochs | 4 epochs | Second minus first |
|---|---:|---:|---:|
| Overall accuracy | 0.666667 | 0.733333 | +0.066667 |
| Macro F1 | 0.503324 | 0.671225 | +0.167901 |
| F1 — analysis | 0.769231 | 0.769231 | +0.000000 |
| F1 — unsupported | 0.740741 | 0.800000 | +0.059259 |
| F1 — question | 0.000000 | 0.444444 | +0.444444 |

These differences measure one predeclared comparison on one split. They
do not establish a reliable improvement across seeds. Unit 6 evaluates that.

### Reading the first-seed results

The original 3-epoch run remains the first-run reference; the 4-epoch run is the
predeclared comparison, not a new test-tuned default. First-run accuracy is
66.7% and macro F1 is 0.503324; the comparison is 73.3%
and 0.671225. Question F1 moved from 0.000000 to
0.444444, based on only seven test examples.

The 75% accuracy target is missed on this seed in both runs. The 0.65 minimum
per-label F1 is also missed for question. Mean confidence when correct is
0.421990 and 0.456680; the fractions below 0.50
confidence are 100.0% and 73.3%. These miss
the stated confidence conditions. Criteria were not lowered. Criterion 3's
label-balance target is met. A second-human agreement result is not available,
as recorded at the end of Unit 5. The Unit 6 three-seed results are now reported below.

**Trained model:** The first model and tokenizer were saved and reloaded fully
offline; their predictions reproduce results.json exactly. Large model weights
are excluded from Git, as specified by .gitignore. A separate trained-model
download is supplied with the assistant's completion message. Both models remain
reproducible from the committed data and the recorded software versions.

## How I Used AI

**Unit 6 AI assistance:** Codex read the provided assignment and PowerPoint, ran the local baseline and six notebook-based training trials, recorded predictions and split isolation, and drafted the typed tables and diagnoses. The original student criteria and confirmed project labels were kept unchanged. At the student's later request, Codex also prepared all 30 AI label suggestions with individual reasons in `reviews/unit6-ai/`; the provenance explicitly records that they are not independent human annotations. The same 30 choices are now also saved in `my_staff_labels.csv`, with separate authorship evidence. No TF key was opened for the original annotation. The later TF download enabled a 29/30 AI-to-staff comparison; independent human agreement is not claimed. The user subsequently delegated the one remaining adjudication, which Codex completed and attributed as AI-assisted. The Unit 6 interpretation is AI-assisted and should be reviewed by the student.

The disclosures below preserve the status when each earlier stage was performed.
References to pending human review describe those earlier stages. The current
human-review confirmation was recorded on 2026-10-20 and covers all 200 final labels.

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

**Human-review finalization (2026-10-20):** Win Aung stated, "I review it already,you just need to finished it".
The current 200 labels were retained and marked human-reviewed on that basis.
The evidence record includes all row IDs, text hashes, labels, and the finalized CSV hash.
The assistant explanations remain attributed to the assistant. This update adds no
unaided cold-pass evidence, second-reviewer agreement, training run, or evaluation scores.

See [docs/next-steps.md](docs/next-steps.md) for the remaining course evidence and training steps.
The original README, including the Unit 6 templates, is retained at
docs/starter-README.md. RUNNING.md is the official command reference.

Rubric audit: see [docs/rubric-audit.md](docs/rubric-audit.md).

<!-- UNIT6-REPORT -->
## Unit 6 status

**The baseline and before trials are complete.** All three after trials and the one-change comparison are also complete. **The assignment is not complete:** the independent human annotation requirement and independently authored student adjudication remain unverified. The user delegated the remaining adjudication to Codex, which has completed an attributed assisted decision. The authentic TF reference has now been imported, and the existing 30 AI-assisted labels have been compared against it.

The original `criteria.md`, `labels.csv`, taxonomy, Unit 5 `results.json`, and `test_split.csv` are preserved. The [pre-run protocol](docs/unit6/plan.md) records the baseline prediction and measurement conventions. No Unit 6 stretch feature is claimed.

## Baseline vs. Trained

**Prediction recorded before baseline scoring:** The trained model will beat the zero-shot baseline on `unsupported` F1 because it has seen Hacker News agreement, jokes, and bare statements assigned to this deliberately broad category.

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.467 | 0.667 | +0.200 |
| Macro F1 | 0.461 | 0.503 | +0.042 |
| F1 — `analysis` | 0.538 | 0.769 | +0.231 |
| F1 — `unsupported` | 0.400 | 0.741 | +0.341 |
| F1 — `question` | 0.444 | 0.000 | -0.444 |

Both columns score exactly the same 30 original Unit 5 test comments. The baseline is `facebook/bart-large-mnli`, using all three exact one-sentence README definitions in `label_definitions.txt`, with no examples, fallback, or cap. Trained means the original three-epoch seed-42 model. The prediction held for unsupported F1, yet the baseline beat training on question F1 (0.444444 versus 0). The 20-point accuracy advantage therefore does not mean training learned every category. The requested one-sentence prompt does not include all boundary tie-breakers; a weak baseline could partly reflect that limitation. These are local CPU runs, without hosted-model API calls.

## Run Log — Before

Three real retrainings using the notebook section 6 loop: seeds **42, 7, 2024**. Device **CPU**, PyTorch **2.6.0+cpu**, model **distilbert-base-uncased**, 3 epochs, learning rate **2e-5**, batch **16**, maximum **128 tokens**. Stratified splits are 139 train / 31 validation / 30 test. In each test: analysis 11, unsupported 12, question 7. Each seed's full predictions, softmax probabilities, split hashes and trainer history are saved in the results JSON and `evidence/unit6/before/`.

| Criterion | Original target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥0.75 in every seed | 0.666667 | 0.633333 | 0.500000 | MISSED |
| 2. Every label F1 | ≥0.65 for all labels in every seed | analysis: 0.769231; unsupported: 0.740741; question: 0.000000 | analysis: 0.818182; unsupported: 0.645161; question: 0.000000 | analysis: 0.600000; unsupported: 0.545455; question: 0.000000 | MISSED |
| 3. Dataset balance | Every label 15%–45% of all 200 comments | analysis 36%; unsupported 40.5%; question 23.5% | analysis 36%; unsupported 40.5%; question 23.5% | analysis 36%; unsupported 40.5%; question 23.5% | MET |
| 4. Human agreement | ≥80% on 30–50 comments | Independent human labels missing | Independent human labels missing | Independent human labels missing | MISSED |
| 5. Prediction confidence | Correct mean ≥0.70; fraction of all test max-probs below 0.50 <15%; every seed | correct mean 0.421990; low 100.0% | correct mean 0.407459; low 100.0% | correct mean 0.412820; low 100.0% | MISSED |

Criterion 3 is one dataset measurement repeated for clarity; criterion 4 is one human exercise, not three model-seed trials. `MISSED` on criterion 4 means the required evidence has not been demonstrated, **not** 0% measured agreement. The 30 staff posts use the staff running-forum taxonomy, which cannot directly validate every Hacker News annotation. No original target has been changed.

Before accuracy spread is **0.166667 (16.7 percentage points)**. This exceeds the brief's 10-point instability flag; one favorable split would be unreliable.

Always guessing the training-majority label `unsupported` would score 12/30 = 40% on each held-out split. The trained model beats that trivial reference, but its zero question recall shows why overall accuracy alone is insufficient.

Rows below are true labels; columns are model predictions. Each matrix is for its own 30-post split, not a pooled independent sample.

### Confusion matrix — seed 42

| True / predicted | analysis | unsupported | question |
|---|---:|---:|---:|
| **analysis** | 10 | 1 | 0 |
| **unsupported** | 2 | 10 | 0 |
| **question** | 3 | 4 | 0 |

Largest off-diagonal cell (first in label order if tied): 4 true `question` posts were called `unsupported`; the reverse direction has 0 errors.

### Confusion matrix — seed 7

| True / predicted | analysis | unsupported | question |
|---|---:|---:|---:|
| **analysis** | 9 | 2 | 0 |
| **unsupported** | 2 | 10 | 0 |
| **question** | 0 | 7 | 0 |

Largest off-diagonal cell (first in label order if tied): 7 true `question` posts were called `unsupported`; the reverse direction has 0 errors.

### Confusion matrix — seed 2024

| True / predicted | analysis | unsupported | question |
|---|---:|---:|---:|
| **analysis** | 6 | 5 | 0 |
| **unsupported** | 3 | 9 | 0 |
| **question** | 0 | 7 | 0 |

Largest off-diagonal cell (first in label order if tied): 7 true `question` posts were called `unsupported`; the reverse direction has 0 errors.

## Verdicts and Diagnoses

1. **Accuracy — MISSED.** The original rule requires every seed to reach 0.75. Minority-question errors limit accuracy: question recall is seed 42: 0.000000, seed 7: 0.000000, seed 2024: 0.000000. Each split has only seven question examples and the training subset only 33. This makes weak question learning costly and estimates coarse. Continued validation-loss decline supports testing more optimization, but does not prove that training length is the only cause.

2. **Every-label F1 — MISSED.** Minimum F1 by seed is 42: question 0.000000; 7: question 0.000000; 2024: question 0.000000. Other misses: seed 7 unsupported: 0.645161; seed 2024 analysis: 0.600000; seed 2024 unsupported: 0.545455. Seed 42 sends all seven true questions to analysis or unsupported, while making no question predictions. Even the straightforward request “What are you using? whisper?” becomes unsupported. A more complex Cursor free-trial question becomes analysis, showing that an information request with contextual details is also difficult. The direction suggests a request-versus-statement weakness. False unsupported predictions also reduce that label's precision, while seed 2024 additionally confuses analysis and unsupported in both directions. Without the independent staff exercise, inconsistent labeling is a hypothesis, not an established diagnosis.

3. **Balance — MET.** Counts remain analysis 72/200, unsupported 81/200, question 47/200: all fall within the original 15%–45% band. The smallest class still provides only 33 training examples per split. Passing the balance target does not ensure enough examples or representative prevalence; the Unit 5 purposive sampling remains disclosed.

4. **Human agreement — MISSED, not demonstrated.** The authentic TF key is available and the AI-assisted labels match 29/30. Independent human annotations remain unavailable, so this rate does not measure agreement between two humans. A prior confirmation of all 200 AI-assisted project labels is one human review, not agreement between two humans. The staff exercise must be completed before diagnosing inconsistent rule application. Its different taxonomy also limits how far its result transfers to the Hacker News dataset.

5. **Confidence — MISSED.** Read both conditions in each run-log cell. Winning probabilities remain too low, consistent with weak class separation after three epochs; they do not show that hedging caused the problem. Softmax confidence is uncalibrated, and raising it alone would not prove correctness. The saved probabilities permit direct recomputation of the correct-only mean and all-test low-confidence fraction.

## Agreement Report

**Measured AI-to-staff agreement: 29/30 = 0.966667 (96.7%).** The pre-key labels in `my_staff_labels.csv` were prepared by Codex. This is a diagnostic comparison, not two independent human annotators. Criterion 4 remains **MISSED — independent human evidence not demonstrated**, despite the numerical rate exceeding 80%.

The authentic reference was supplied through [the TF Drive file](https://drive.google.com/file/d/1Cp8PeB-MkDaNifSPNixNfo7xVfi6R3GF/view). It was downloaded after the 30 label choices had been committed at `7cc80560b80ae83656841ac2b50bd771c4654e66`; those choices have not changed after seeing the key. [Import provenance](evidence/unit6/staff-reference-import.json) records the file hashes and filename mapping.

**File mapping:** At the user's explicit request, the downloaded answer CSV is saved as [data/staff_posts.csv](data/staff_posts.csv). It contains `id,label,borderline,why`, not post text. The identical answer bytes are also saved as [data/staff_labels.csv](data/staff_labels.csv). The original `id,text` file is preserved byte-for-byte as [data/staff_post_texts.csv](data/staff_post_texts.csv). `python agreement.py` now defaults to that text file and the canonical labels file.

| Compared | Matched | Disagreed | Missing posts | Annotation authorship |
|---:|---:|---:|---:|---|
| 30 | 29 | 1 | 0 | Codex AI versus staff reference |

### Every actual disagreement

#### sp_014

> Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem.

**Saved pre-key label:** `analysis`. **Staff label:** `hot_take`.

**Staff's supplied rationale:** HARD, and the canonical rule-1 case. The 3% is decoration on a conclusion already reached — 'so obviously' does the work, not the number.

**AI-assisted case for `analysis`:** The post uses the 3% change after the shoe-rule change as a premise and explicitly connects it with 'so' to a causal conclusion. Rule 1's analysis example also reasons from a change in times and a change in shoe rules. The causal inference is too strong, but a weak inference can still use a fact as its premise.

**AI-assisted case for `hot_take`:** 'Obviously', 'the whole story', and the judgment that the sport has a problem express a sweeping conclusion that the single statistic cannot establish. Under Rule 1's decoration clause, the statistic can be read as a flourish attached to that conclusion. This follows the staff interpretation of its own canonical boundary case.

**AI-assisted adjudication, prepared at the user's request:** Retain `analysis` as a defensible reading. The measured time change and its timing relative to the rule change explicitly supply the premise for the conclusion. Rule 1 asks whether a fact carries the argument; it does not require that the resulting causal inference be valid. The wording 'so obviously' overstates the evidence but does not by itself show that the writer reached the conclusion before considering the statistic. Staff's reading remains plausible because the claim about the whole sport extends beyond the fact supplied.

**Disagreement category: (c) — two defensible readings.** This call preserves the pre-key label rather than changing it to match staff. It is the assistant's argued adjudication, delegated by the user, and is not represented as an independently written student judgment.

The one dispute concerns `analysis` versus `hot_take` in the staff running-forum taxonomy. It does not establish that the separate Hacker News `question` boundary caused the trained model's errors. The assisted adjudication is complete; independent human annotation and independently authored student adjudication are not demonstrated. The original training results and criteria are unchanged.

## The Improvement

**One change: epochs 3 → 4.** The [improvement declaration](docs/unit6/improvement-plan.json) is recorded after the before diagnosis and before starting after. The question weakness and low confidence, together with declining validation loss, justify a limited optimization test. The earlier Unit 5 3-versus-4 comparison was already known; this Unit 6 experiment tests its repeatability across three seeds and is not a previously unseen hypothesis. More epochs may overfit and are not a substitute for label-agreement evidence. No rows, taxonomy, learning rate, batch size, token limit, split, seeds, or criteria changed. This is the sole Unit 6 improvement; no second fix was tried.

### Run Log — After

| Criterion | Original target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥0.75 in every seed | 0.733333 | 0.633333 | 0.600000 | MISSED |
| 2. Every label F1 | ≥0.65 for all labels in every seed | analysis: 0.769231; unsupported: 0.800000; question: 0.444444 | analysis: 0.818182; unsupported: 0.645161; question: 0.000000 | analysis: 0.782609; unsupported: 0.600000; question: 0.000000 | MISSED |
| 3. Dataset balance | Every label 15%–45% of all 200 comments | analysis 36%; unsupported 40.5%; question 23.5% | analysis 36%; unsupported 40.5%; question 23.5% | analysis 36%; unsupported 40.5%; question 23.5% | MET |
| 4. Human agreement | ≥80% on 30–50 comments | Independent human labels missing | Independent human labels missing | Independent human labels missing | MISSED |
| 5. Prediction confidence | Correct mean ≥0.70; fraction of all test max-probs below 0.50 <15%; every seed | correct mean 0.456680; low 73.3% | correct mean 0.439193; low 96.7% | correct mean 0.456964; low 90.0% | MISSED |

### Paired before/after comparison

Each cell is before → after (after minus before). These paired comparisons use identical splits within each seed; overlapping posts across seeds mean these are not independent 90-post trials.

| Measure | Seed 42 | Seed 7 | Seed 2024 |
|---|---|---|---|
| Accuracy | 0.666667 → 0.733333 (+0.066667) | 0.633333 → 0.633333 (+0.000000) | 0.500000 → 0.600000 (+0.100000) |
| Macro F1 | 0.503324 → 0.671225 (+0.167901) | 0.487781 → 0.487781 (+0.000000) | 0.381818 → 0.460870 (+0.079051) |
| F1 analysis | 0.769231 → 0.769231 (+0.000000) | 0.818182 → 0.818182 (+0.000000) | 0.600000 → 0.782609 (+0.182609) |
| F1 unsupported | 0.740741 → 0.800000 (+0.059259) | 0.645161 → 0.645161 (+0.000000) | 0.545455 → 0.600000 (+0.054545) |
| F1 question | 0.000000 → 0.444444 (+0.444444) | 0.000000 → 0.000000 (+0.000000) | 0.000000 → 0.000000 (+0.000000) |
| Correct-prediction mean confidence | 0.421990 → 0.456680 (+0.034690) | 0.407459 → 0.439193 (+0.031734) | 0.412820 → 0.456964 (+0.044144) |
| Fraction confidence <0.50 | 1.000000 → 0.733333 (-0.266667) | 1.000000 → 0.966667 (-0.033333) | 1.000000 → 0.900000 (-0.100000) |

Accuracy improved in **2/3** seeds, stayed unchanged in **1/3**, and regressed in **0/3**; the paired table shows the size and label-specific direction of every change. The change did not improve accuracy in every seed, so its benefit is partial rather than a reliable fix for all splits.

After accuracy spread: **0.133333**. It remains above the 10-point instability flag. Final criterion verdicts must still hold in every seed; improvements do not automatically become passes.

### Confusion matrix — seed 42

| True / predicted | analysis | unsupported | question |
|---|---:|---:|---:|
| **analysis** | 10 | 1 | 0 |
| **unsupported** | 2 | 10 | 0 |
| **question** | 3 | 2 | 2 |

Largest off-diagonal cell (first in label order if tied): 3 true `question` posts were called `analysis`; the reverse direction has 0 errors.

### Confusion matrix — seed 7

| True / predicted | analysis | unsupported | question |
|---|---:|---:|---:|
| **analysis** | 9 | 2 | 0 |
| **unsupported** | 2 | 10 | 0 |
| **question** | 0 | 7 | 0 |

Largest off-diagonal cell (first in label order if tied): 7 true `question` posts were called `unsupported`; the reverse direction has 0 errors.

### Confusion matrix — seed 2024

| True / predicted | analysis | unsupported | question |
|---|---:|---:|---:|
| **analysis** | 9 | 2 | 0 |
| **unsupported** | 3 | 9 | 0 |
| **question** | 0 | 7 | 0 |

Largest off-diagonal cell (first in label order if tied): 7 true `question` posts were called `unsupported`; the reverse direction has 0 errors.

Final verdicts: accuracy **MISSED**; every-label F1 **MISSED**; balance **MET**; human agreement **MISSED — not demonstrated**; confidence **MISSED**.

The extra epoch recovered seed 42: 2/7 true questions; seed 7: 0/7 true questions; seed 2024: 0/7 true questions. Seed 2024's accuracy gain comes from analysis/unsupported classification rather than learning question. Training length therefore explains part of the measured weakness, but this one change did not solve the request boundary across seeds. The after log still misses accuracy, every-label F1, and both-part confidence targets; the absent independent agreement evidence prevents deciding whether remaining boundary errors originate in annotation consistency, task difficulty, or inadequate training data.

## What's Still Broken

For any remaining accuracy or per-label F1 miss, the next step would be a separate development-set audit of request-versus-statement examples, followed by targeted new questions if warranted; no extra fix is made here because this unit allows one measured improvement. Seven question test examples per seed remain too few for precise per-label estimates, and comment-level splits within eight threads do not establish transfer to unseen threads or the whole of Hacker News.

Criterion 4 remains unproven because the saved labels are AI-assisted. The authentic TF reference is now available; the one disagreement now has an attributed AI-assisted adjudication retaining analysis under category (c). Independently written student adjudication is not demonstrated. Confidence misses require a later calibration/abstention study on validation data rather than forcing probabilities upward to pass a threshold; no additional test-driven tuning was performed.

The intended taxonomy distinguishes evidence supporting a main claim, unsupported statements, and genuine information requests. The before matrix shows that the learned classifier instead favors the two statement categories and misses genuine questions, so it has only partially learned that intended distinction.

Reproduce with the repository virtual environment and the environment variables in [the reproduction guide](docs/unit6/reproduce.md): `python tools/run_unit6.py --run before --allow-assisted-initial20`, then the declared `--run after`, then `python tools/verify_unit6.py` and `python tools/build_unit6_report.py`. The runner refuses to overwrite existing results; preserve or move prior outputs for a deliberate new experiment. After verification runs, `evidence/unit6/verification.json` records its arithmetic and split checks. Large model caches and weights remain excluded from Git.
