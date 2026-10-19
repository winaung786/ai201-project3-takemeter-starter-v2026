# Acceptance criteria — TakeMeter

## 1.

Overall classification accuracy must reach at least 75% on the held-out test dataset for each of the three Unit 6 seeds individually.

**Why this target:** Hacker News comments frequently mix dry sarcasm, hedged critique, and strong technical opinions within the same paragraph. Requiring at least 75% accuracy across every individual Unit 6 seed ensures the classifier consistently beats a majority-class baseline regardless of initialization or split variance.

## 2.

Per-label F1-score for every category must reach at least 0.65 on the held-out test dataset for each of the three Unit 6 seeds individually.

**Why this target:** High overall accuracy can mask poor recall on less frequent label categories when a model defaults to predicting the most common label. Enforcing an F1-score floor of 0.65 per label on every single Unit 6 seed guarantees balanced precision and recall across all categories without relying on a lucky seed average.

## 3.

Label balance (class distribution) must keep every label between 15% and 45% of the 200-comment labeled dataset.

**Why this target:** While reading through the initial sample of raw Hacker News comments in our dataset, straightforward technical explanations and measured critiques appeared far more frequently than sharp, contrarian takes. Enforcing a 15% to 45% distribution band across the 200 labeled examples prevents the training set from mirroring that raw skew and starving the minority labels of training signal.

## 4.

Inter-annotator agreement (percent agreement) with a second human reviewer must reach at least 80% on a 30-to-50 comment validation sample.

**Why this target:** In the comments I read, borderline cases—such as a polite architectural critique that ends with a sweeping dismissal of a framework—are easy for two readers to categorize differently. Achieving 80% human agreement confirms that our label boundaries and tie-breaker rules are unambiguous before holding the model accountable to them.

## 5.

Average prediction confidence (softmax probability) on correctly classified test examples must reach at least 0.70, with fewer than 15% of test predictions falling below 0.50 confidence, for each of the three Unit 6 seeds individually.

**Why this target:** Several comments in our sample use hedged phrasing ("I might be wrong, but...", "In my experience...") that can pull a classifier toward near-uniform probabilities. Requiring a 0.70 mean confidence on correct predictions across each of the three Unit 6 seeds ensures the model learns decisive boundaries rather than winning labels by razor-thin margins.
