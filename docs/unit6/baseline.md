# Baseline vs. Trained

Prediction, recorded in the pre-run protocol: The trained model will beat the zero-shot baseline on `unsupported` F1 because it has seen Hacker News agreement, jokes, and bare statements assigned to this deliberately broad category.

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.467 | 0.667 | +0.200 |
| Macro F1 | 0.461 | 0.503 | +0.042 |
| F1 — `analysis` | 0.538 | 0.769 | +0.231 |
| F1 — `question` | 0.444 | 0.000 | -0.444 |
| F1 — `unsupported` | 0.400 | 0.741 | +0.341 |

Both columns use exactly the original 30 Unit 5 test comments; the baseline used the exact label definitions, with no cap or fallback. The trained column is the original three-epoch seed-42 run, not the four-epoch comparison. The prediction held for unsupported F1, but training lost all question recall: the baseline has question F1 0.444 while the trained model never predicts question. A 20-point accuracy gain does not establish that training learned all three distinctions. Baseline prompts omit the longer boundary tie-breakers, as the assignment requests the one-sentence definitions; weak zero-shot performance alone is not proof the taxonomy is clear. These are local CPU runs and a single fixed test comparison, not three-seed baseline superiority.
