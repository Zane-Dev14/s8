# STEP 4: Module 3 Crash Guide (Classification, Decision Trees, Clustering)

Module 3 focus:
- Decision tree metrics and implementation issues
- Confusion matrix, precision, recall
- Distance measures
- Clustering algorithms (K-Means, PAM, DBSCAN)
- SLIQ decision tree workflow

Mapped from OCR:
- DM/ocr_output/mod3.txt

---

## Topic 1: Requirements of a Good Clustering Algorithm

Write these points:
1. Scalability to large datasets
2. Handles different cluster shapes/sizes
3. Robust to noise and outliers
4. Minimal domain parameter dependence
5. Stable/reproducible output
6. High cluster quality (high intra-similarity, low inter-similarity)
7. Interpretability

---

## Topic 2: Decision Tree Implementation Issues

1. Overfitting
2. Instability due to small data changes
3. Bias toward attributes with many values
4. Data fragmentation after deep splits
5. Greedy local split may miss global best tree
6. Pruning difficulty

Short fix lines:
- Use pruning, validation, and better split constraints.

---

## Topic 3: Entropy, Information Gain, Gain Ratio, Gini

## Entropy
$$
Entropy(S) = -\sum_i p_i \log_2 p_i
$$

## Information Gain
$$
IG(S,A) = Entropy(S) - \sum_v \frac{|S_v|}{|S|}Entropy(S_v)
$$

## Split Information
$$
SplitInfo(S,A) = -\sum_v \frac{|S_v|}{|S|}\log_2\frac{|S_v|}{|S|}
$$

## Gain Ratio
$$
GainRatio(S,A) = \frac{IG(S,A)}{SplitInfo(S,A)}
$$

## Gini Index
$$
Gini(S) = 1 - \sum_i p_i^2
$$

Important note:
- Gain ratio reduces information gain bias toward high-cardinality attributes.

---

## Topic 4: Confusion Matrix, Precision, Recall

Confusion matrix terms:
1. TP: true positive
2. TN: true negative
3. FP: false positive
4. FN: false negative

Formulas:
$$
Precision = \frac{TP}{TP+FP}
$$
$$
Recall = \frac{TP}{TP+FN}
$$

Exam tip:
- Write matrix first, then substitute values.

---

## Topic 5: Distance Metrics

Given objects $X=(x_1,...,x_n)$ and $Y=(y_1,...,y_n)$:

## Euclidean
$$
D_E = \sqrt{\sum_i (x_i-y_i)^2}
$$

## Manhattan
$$
D_M = \sum_i |x_i-y_i|
$$

## Minkowski of order p
$$
D_p = \left(\sum_i |x_i-y_i|^p\right)^{1/p}
$$

---

## Topic 6: K-Means Clustering

Steps:
1. Choose k centroids
2. Assign each point to nearest centroid
3. Recompute centroid as mean of cluster
4. Repeat until assignments stop changing

Pros:
- Simple and fast.

Limitations:
- Needs k in advance, sensitive to initialization and outliers.

---

## Topic 7: PAM (Partitioning Around Medoids)

Key difference from K-means:
- Uses real data points (medoids), not means.

Steps:
1. Build phase: choose initial medoids
2. Swap phase: replace medoid with non-medoid if total distance improves
3. Repeat until no better swap

Strength:
- More robust to outliers than k-means.

---

## Topic 8: DBSCAN

Parameters:
1. Eps: neighborhood radius
2. MinPts: minimum points in Eps-neighborhood

Point types:
1. Core point
2. Border point
3. Noise point

Algorithm idea:
1. Start from unvisited point
2. If core point, expand cluster through density reachability
3. Otherwise mark as noise/border

Strength:
- Detects arbitrary-shaped clusters and handles outliers naturally.

---

## Topic 9: SLIQ Algorithm

What it is:
- Scalable decision tree induction for large datasets.

Workflow:
1. Presort numerical attributes once
2. Evaluate split criteria efficiently
3. Choose best split
4. Maintain class list for records
5. Build tree level-wise (breadth-first)
6. Recurse until stopping criteria

---

## Module 3 PYQ Attack Set

1. Requirements of good clustering algorithm
2. Decision tree implementation issues
3. Gain ratio and its advantage over information gain
4. Distance metric numerical
5. Confusion matrix + precision/recall
6. Information gain/Gini based first split
7. DBSCAN concept and advantages
8. ID3 first splitting attribute
9. K-means/PAM/SLIQ explanations

---

## Last-Minute Revision Grid

1. Memorize entropy/IG/gain-ratio/gini formulas.
2. Practice one confusion-matrix numerical.
3. Practice one distance-metric numerical.
4. Memorize DBSCAN core-border-noise definitions.
5. Keep k-means vs PAM 4-point comparison ready.
