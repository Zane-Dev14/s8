# STEP 4: Module 3 Crash Guide (Classification, Decision Trees, Clustering)

Module focus:
- Decision tree quality metrics
- Classification performance metrics
- Distance measures
- Clustering algorithms

Questions asked repeatedly (non-duplicate):
Part A topics asked:
1. Gain ratio and advantage over information gain.
2. Requirements of good clustering algorithm.
3. Distance metrics: Euclidean, Manhattan, Minkowski.
4. Confusion matrix with precision and recall.
5. Decision-tree splitting indices and SLIQ significance.

Part B topics asked:
1. Confusion matrix with precision/recall/specificity numerical.
2. DBSCAN algorithm with advantages.
3. PAM algorithm with example.
4. ID3 first splitting attribute finding.
5. Information gain calculation for given attribute.
6. SLIQ algorithm with construction steps.
7. Partition clustering variants and comparison asks.

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

---

## Part B Complete Answer Bank (All Asked Questions)

Use acronym for algorithms:
- DSRC
- Define, Steps, Result, Conclusion.

## Q1) Confusion matrix with precision, recall, specificity (10 points)
1. Build confusion matrix from TP, FP, FN, TN values.
2. Given: total=80, relevant=55, retrieved=50, relevant-retrieved=40.
3. TP = 40.
4. FP = retrieved - TP = 50 - 40 = 10.
5. FN = relevant - TP = 55 - 40 = 15.
6. TN = total - (TP+FP+FN) = 80 - 65 = 15.
7. Precision = TP/(TP+FP) = 40/50 = 0.80.
8. Recall = TP/(TP+FN) = 40/55 = 0.727.
9. Specificity = TN/(TN+FP) = 15/25 = 0.60.
10. Conclude: precision is high, recall is moderate, specificity is lower.

## Q2) DBSCAN algorithm with advantages (10 points)
1. DBSCAN is a density-based clustering method.
2. Input parameters are Eps and MinPts.
3. If neighborhood size >= MinPts, point is a core point.
4. Border points are not core but lie within core neighborhood.
5. Noise points are neither core nor border.
6. Start with an unvisited point and mark visited.
7. If core, expand cluster through density-reachable points.
8. Continue expansion iteratively for all reachable core neighbors.
9. Advantages: arbitrary-shape cluster discovery and outlier handling.
10. No need to specify number of clusters in advance.

## Q3) PAM algorithm with example flow (10 points)
1. PAM stands for Partitioning Around Medoids.
2. Medoid is an actual data point minimizing cluster dissimilarity.
3. Build phase chooses initial k medoids.
4. Assign each point to nearest medoid.
5. Swap phase tests medoid and non-medoid exchange.
6. Compute total dissimilarity after each candidate swap.
7. Accept swap if objective value decreases.
8. Repeat swap search until no improvement.
9. PAM is robust to outliers compared to K-means.
10. Draw two-cluster medoid assignment sketch for scoring.

## Q4) ID3 first splitting attribute (10 points)
1. ID3 selects attribute with maximum information gain.
2. Compute entropy of full dataset first.
3. Formula: H(S) = -sum(pi log2 pi).
4. For each attribute A, partition dataset by attribute values.
5. Compute weighted entropy after split on A.
6. Formula: IG(S,A)=H(S)-sum((|Sv|/|S|)H(Sv)).
7. Evaluate IG for all candidate attributes.
8. Attribute with highest IG becomes root split.
9. Draw one-level tree with selected root attribute.
10. Recursively repeat process for child subsets.

## Q5) Information gain for attribute age (10 points)
1. Count class distribution yes/no for entire dataset.
2. Compute overall entropy H(S).
3. Split records by age categories: youth, middle-aged, senior.
4. Compute entropy for each age subset.
5. Compute weighted subset entropy using subset proportions.
6. Subtract weighted entropy from H(S) to get IG(age).
7. Compare IG(age) with other attribute gains.
8. If IG(age) is maximum, age is selected for split.
9. Mention gain ratio if tie-breaking against high-cardinality attributes.
10. Conclude with exact IG value and rank position in answer.

## Q6) SLIQ algorithm with construction steps (10 points)
1. SLIQ is scalable decision-tree algorithm for large datasets.
2. It presorts numerical attributes once to reduce repeated sorting.
3. It maintains class list to track node-class membership.
4. For each node, evaluate candidate splits efficiently.
5. Use Gini-based split selection for best partition quality.
6. Apply chosen split and update class list entries.
7. Build tree level by level (breadth-first growth).
8. Continue until stopping criteria or pure nodes.
9. SLIQ scales better than naive recursive sort-based trees.
10. Draw flow: Presort -> Class list -> Split eval -> BFS growth.

## Q7) Partition clustering and comparison-style answer (10 points)
1. Partition methods divide data into k disjoint clusters.
2. Objective is to minimize within-cluster distance.
3. K-means uses centroid means and is computationally fast.
4. PAM uses medoids and is more robust to outliers.
5. K-means can fail on non-spherical cluster shapes.
6. PAM handles noisy points better but costs more computation.
7. Initialization quality strongly affects both methods.
8. Distance metric choice changes assignment behavior.
9. Use comparison table in exam for full marks.
10. Conclude by choosing method based on scale and noise profile.
