# Unit 5 evidence audit

This is an evidence inventory, not an awarded grade or promise of full credit.

| Evidence | Status |
|---|---|
| Five numeric criteria and reasons | Student-supplied; committed before model scores at cc8ae32; preserved unchanged |
| Single unsplit labels.csv | 200 complete comments; no duplicates; exact IDs/text/labels bound to the human-review confirmation |
| Final class distribution | analysis 72 (36%); unsupported 81 (40.5%); question 47 (23.5%); meets criterion 3 and the required 70% cap |
| Human review | User-confirmed for all 200 labels at fe558f8; original AI assistance remains disclosed |
| Unaided first 20 | Not established; initial labels were AI-assisted; no cold marker invented |
| Hard cases | Three alternative-label decisions and rules are documented; explanations originated with the assistant and labels were subsequently accepted by the user |
| README | All five required sections, definitions and two source examples per label, boundary rule, counts, workflow and training settings |
| Commit history | More than four genuine new commits beyond the official starter |
| Training | See the actual results files and Training Run section; training is distinct from full course-evidence completion |
| Second-human agreement | Not performed; general review confirmation is not a second-reviewer comparison |

The strict course validator remains unchanged. A separate explicit training mode
can accept the exact hash-bound human-confirmed dataset while disclosing the missing
unaided cold pass. It does not claim that this course requirement is satisfied.

## Stretch feature

The second run was declared before implementation and before scores: 3 versus 4
epochs, with the same data, stratified split, seed 42 and remaining settings. Both runs completed and their actual
metrics and differences are saved in results_epoch_comparison.json and the README.
No fourth label or extra 50-example stretch is claimed. The 31 newly collected
questions were part of a documented sample revision, not an extra-50 claim.

## Acceptance targets

Overall accuracy, per-label F1 and confidence targets must hold individually across
the three Unit 6 seeds. One-seed Unit 5 results do not establish a three-seed pass.
The balance criterion can be checked now. Inter-annotator agreement still needs a
second human and the specified independent sample. Do not lower targets after
seeing scores or rewrite the student's explanations.
