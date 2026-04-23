# STEP 4: Module 3 Crash Guide (Classification, Decision Trees, Clustering)

Module focus:
- Decision tree quality metrics
- Classification performance metrics
- Distance measures
- Clustering algorithms

Questions asked repeatedly (non-duplicate):
- Gain ratio and advantage over information gain
- Requirements of good clustering algorithm
- Distance metrics: Euclidean, Manhattan, Minkowski
- Confusion matrix with precision and recall
- DBSCAN with advantages
- PAM algorithm with example
- ID3 first splitting attribute
- SLIQ algorithm and implementation issues

Answer format for this module:
- Part A: write exactly 5 points.
- Part B: write exactly 10 points.
- For algorithm answers, write steps in numbered order.

---

## 1) Requirements of a Good Clustering Algorithm

Write any six to seven points:
1. Scalability to large datasets.
2. Handles different shapes and cluster sizes.
3. Robust to noise and outliers.
4. Minimal parameter dependence.
5. High intra-cluster similarity.
6. Low inter-cluster similarity.
7. Interpretability and stability.

---

## 2) Decision Tree Implementation Issues

1. Overfitting in deep trees.
2. Instability due to small data changes.
3. Bias toward attributes with many distinct values.
4. Data fragmentation at deeper levels.
5. Greedy splitting may miss global optimum.
6. Pruning strategy selection is non-trivial.

Mitigation line:
Use pre-pruning, post-pruning, and validation-based split control.

---

## 3) Core Formulas with Symbol Explanation

## Entropy
$$
H(S) = -\sum_i p_i\log_2 p_i
$$
- p_i: class probability in set S.

## Information Gain
$$
IG(S,A) = H(S) - \sum_v \frac{|S_v|}{|S|}H(S_v)
$$
- S_v: subset after split on attribute value v.

## Split Information
$$
SplitInfo(S,A) = -\sum_v \frac{|S_v|}{|S|}\log_2\left(\frac{|S_v|}{|S|}\right)
$$

## Gain Ratio
$$
GR(S,A) = \frac{IG(S,A)}{SplitInfo(S,A)}
$$

## Gini
$$
Gini(S) = 1 - \sum_i p_i^2
$$

Why gain ratio is preferred in many cases:
It penalizes attributes that create too many tiny partitions.

---

## 4) Confusion Matrix, Precision, Recall

Confusion matrix terms:
1. TP: true positives
2. TN: true negatives
3. FP: false positives
4. FN: false negatives

Formulas:
$$
Precision = \frac{TP}{TP+FP}
$$
$$
Recall = \frac{TP}{TP+FN}
$$

Worked question:
Total = 80, Relevant = 55, Retrieved = 50, Relevant retrieved = 40.

Step solution:
1. TP = 40
2. FP = 50 - 40 = 10
3. FN = 55 - 40 = 15
4. TN = 80 - (40+10+15) = 15

Table:

|  | Predicted Relevant | Predicted Irrelevant |
|---|---:|---:|
| Actual Relevant | TP = 40 | FN = 15 |
| Actual Irrelevant | FP = 10 | TN = 15 |

Metrics:
$$
Precision = \frac{40}{50} = 0.8
$$
$$
Recall = \frac{40}{55} = 0.727
$$

---

## 5) Distance Metrics with Full Numerical

Given:
X = (22, 1, 42, 10), Y = (20, 0, 36, 8)
Difference vector = (2, 1, 6, 2)

## Euclidean
$$
D_E = \sqrt{2^2+1^2+6^2+2^2} = \sqrt{45} = 6.708
$$

## Manhattan
$$
D_M = |2|+|1|+|6|+|2| = 11
$$

## Minkowski (p=3)
$$
D_3 = (2^3+1^3+6^3+2^3)^{1/3} = (233)^{1/3} = 6.154
$$

Final answers:
- Euclidean = 6.708
- Manhattan = 11
- Minkowski (order 3) = 6.154

---

## 6) K-means Clustering

Steps:
1. Initialize k centroids.
2. Assign each point to nearest centroid.
3. Recompute each centroid as cluster mean.
4. Repeat assignment and update until convergence.

Strength:
Simple and fast.

Limitation:
Sensitive to initial centroids and outliers.

---

## 7) PAM (Partitioning Around Medoids)

Core difference from K-means:
PAM uses actual data points (medoids), not arithmetic means.

Steps:
1. Build phase: choose initial medoids.
2. Swap phase: test medoid and non-medoid swaps.
3. Keep swap if total dissimilarity decreases.
4. Stop when no improving swap exists.

Strength:
More robust to outliers than K-means.

---

## 8) DBSCAN

Parameters:
1. Eps: neighborhood radius.
2. MinPts: minimum neighborhood size to be core.

Point types:
1. Core point
2. Border point
3. Noise point

Procedure:
1. Pick unvisited point.
2. If core, expand cluster via density reachability.
3. If not core and not reachable, mark noise.

Advantages:
1. Finds arbitrary-shape clusters.
2. Handles outliers naturally.
3. No need to predefine number of clusters.

---

## 9) SLIQ (Scalable decision tree)

Workflow:
1. Presort numeric attributes once.
2. Evaluate split criteria efficiently.
3. Select best split.
4. Maintain class list for efficient bookkeeping.
5. Grow tree breadth-first.

Use case line:
SLIQ is designed for large datasets where scalability is critical.

---

## Module 3 Final Drill

1. Memorize entropy, IG, gain ratio, and Gini formulas.
2. Solve one confusion matrix numerical.
3. Solve one distance-metric numerical.
4. Write K-means, PAM, DBSCAN in algorithm style.
