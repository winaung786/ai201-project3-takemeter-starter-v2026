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
