# Reproduce the Unit 6 experiment

Use the project `.venv`. These runs used Python 3.12.14, PyTorch 2.6.0+cpu, Transformers 4.57.6, and the versions in `evidence/linux-training-versions.json`.

On Linux/macOS, set the same task environment:

```bash
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_DISABLE_XET=1
export HF_HOME=.cache/huggingface
```

All commands run inside the same repository with its virtual environment activated:

```bash
python baseline.py --trained results.json
python tools/run_unit6.py --run before --allow-assisted-initial20
python tools/run_unit6.py --run after --allow-assisted-initial20
python tools/verify_unit6.py
python tools/build_unit6_report.py
```

The result files already exist as evidence. The seed runner refuses to overwrite them; a deliberate reproduction should preserve them outside the output paths first. Do not commit regenerated test-driven changes as a second improvement. The after run requires the committed one-change plan and checks that each split matches its before counterpart. Changing total epochs also changes the duration of the starter’s default learning-rate decay schedule; the initial learning rate remains fixed. This is a consequence of the one epoch-setting change, not a second tuned parameter. The original notebook remains usable; the CLI executes its functions and actual section 6 loop without rerunning the Unit 5 cells that save `results.json`, `test_split.csv`, and model weights.

`--allow-assisted-initial20` explicitly permits training on the hash-bound, human-confirmed AI-assisted dataset. It does not manufacture an unaided cold pass or make the strict course-evidence validator pass.

The standard environment check returned 9 passes, 0 failures and one misleading cache warning. Its baseline check hardcodes the home cache and ignores `HF_HOME`; the real baseline ran from the repo-local cache. No model/checker behavior was changed to hide that warning.

For the remaining human exercise, follow `staff-review-instructions.md`; only run `python tools/complete_staff_agreement.py` after saving the student's 30 independent labels and obtaining the authentic TF reference. No model API key is needed.
