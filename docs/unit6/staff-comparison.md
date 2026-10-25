# AI-to-staff agreement report

**Measured AI-to-staff agreement: 29/30 = 0.966667 (96.7%).** The pre-key labels in `my_staff_labels.csv` were prepared by Codex. This is a diagnostic comparison, not two independent human annotators. Criterion 4 remains **MISSED — independent human evidence not demonstrated**, despite the numerical rate exceeding 80%.

The authentic reference was supplied through [the TF Drive file](https://drive.google.com/file/d/1Cp8PeB-MkDaNifSPNixNfo7xVfi6R3GF/view). It was downloaded after the 30 label choices had been committed at `7cc80560b80ae83656841ac2b50bd771c4654e66`; those choices have not changed after seeing the key. [Import provenance](../../evidence/unit6/staff-reference-import.json) records the file hashes and filename mapping.

**File mapping:** At the user's explicit request, the downloaded answer CSV is saved as [data/staff_posts.csv](../../data/staff_posts.csv). It contains `id,label,borderline,why`, not post text. The identical answer bytes are also saved as [data/staff_labels.csv](../../data/staff_labels.csv). The original `id,text` file is preserved byte-for-byte as [data/staff_post_texts.csv](../../data/staff_post_texts.csv). `python agreement.py` now defaults to that text file and the canonical labels file.

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
