# Data Mining PYQ Solved Master (OCR-Mapped)

Subject: Data Mining

Built from OCR sources:
- DM/ocr_output/Data-Mining-Module-1-Important-Topics-PYQs.txt
- DM/ocr_output/Data-Mining-Module-2-Important-Topics-PYQs.txt
- DM/ocr_output/mod3.txt
- DM/ocr_output/series1.txt

Purpose:
- Exam-ready answers in compact and long format
- Step-by-step solved numericals
- Mark-oriented structure for 3-mark and 14-mark questions

---

## How To Use

1. For 3-mark: use definition + 4 to 6 bullet points.
2. For 14-mark: use Definition -> Formula/Idea -> Steps -> Example -> Conclusion.
3. For numericals: write given values first, then formula, then substitution, then final answer.

---

## Module 1 Solved PYQs

### M1-Q1: List the three major features of a data warehouse

Answer:
1. Subject-oriented: organized around major business subjects such as customer, sales, product.
2. Integrated: combines data from multiple heterogeneous sources into a consistent repository.
3. Time-variant: stores historical data over long time horizons for trend analysis.

---

### M1-Q2: OLTP vs OLAP

Answer:
1. Purpose: OLTP handles daily transactions, OLAP supports analysis and decision making.
2. Data: OLTP uses current operational data, OLAP uses historical consolidated data.
3. Query type: OLTP has short frequent updates, OLAP has complex read-heavy queries.
4. Schema: OLTP often normalized ER; OLAP often star/snowflake multidimensional schema.
5. Users: OLTP for clerks/apps, OLAP for analysts/managers.

---

### M1-Q3: Star schema vs snowflake schema

Answer:
1. Star schema has one fact table with denormalized dimension tables.
2. Snowflake schema normalizes dimensions into sub-dimensions.
3. Star gives simpler joins and faster queries.
4. Snowflake reduces redundancy but increases join complexity.
5. Star is easier to understand and draw in exam.

---

### M1-Q4: Explain OLAP operations on multidimensional data

Answer:
1. Roll-up: aggregation to higher level (day -> month -> year).
2. Drill-down: detailed view (year -> quarter -> month -> day).
3. Slice: fix one dimension value (year=2023).
4. Dice: subcube by range/conditions on multiple dimensions.
5. Pivot: rotate axes for alternate view.

---

### M1-Q5: KDD process

Answer:
1. Data cleaning
2. Data integration
3. Data selection
4. Data transformation
5. Data mining
6. Pattern evaluation
7. Knowledge presentation

Note:
- Data mining is one stage of KDD, not the whole process.

---

### M1-Q6: Three-tier architecture of data warehouse

Answer:
1. Bottom tier: data sources + ETL + warehouse storage.
2. Middle tier: OLAP server (ROLAP/MOLAP/HOLAP).
3. Top tier: front-end tools for querying, reporting, dashboards, mining.

---

## Module 2 Solved PYQs

### M2-Q1: Justify significance of preprocessing before mining

Answer:
1. Real-world data is incomplete, noisy, and inconsistent.
2. Cleaning improves accuracy and reliability of mined patterns.
3. Integration removes source-level conflicts and redundancy.
4. Transformation makes data compatible with algorithms.
5. Reduction lowers storage/computation costs.
6. Better preprocessing leads to better model quality.

---

### M2-Q2: Data discretization purpose and strategies

Purpose:
1. Convert continuous values into intervals.
2. Reduce complexity and improve interpretability.
3. Improve performance of rule/tree-based mining.

Any four strategies:
1. Binning
2. Histogram-based
3. Clustering-based
4. Decision-tree-based
5. Correlation/ChiMerge-based

---

### M2-Q3: Explain two sampling methods in data reduction

Answer:
1. SRSWOR (without replacement): selected item cannot appear again.
2. SRSWR (with replacement): selected item is returned and may be selected again.
3. Cluster sampling: sample groups/clusters directly.
4. Stratified sampling: divide into strata and sample from each stratum.

---

### M2-Q4: Data smoothing by bin means (Solved)

Given data:
[24, 27, 29, 16, 17, 31, 33, 29, 36, 37, 35, 44]

Step 1: Sort data
[16, 17, 24, 27, 29, 29, 31, 33, 35, 36, 37, 44]

Step 2: Build 3 equal-width bins
- min = 16, max = 44, range = 28
- width approx = 28/3 = 9.33 (use practical bins)

Bins:
1. Bin1: 16, 17, 24
2. Bin2: 27, 29, 29, 31, 33, 35
3. Bin3: 36, 37, 44

Step 3: Bin means
1. Mean1 = (16+17+24)/3 = 19
2. Mean2 = (27+29+29+31+33+35)/6 = 30.67
3. Mean3 = (36+37+44)/3 = 39

Step 4: Replace each bin value by mean
Smoothed data:
[19, 19, 19, 30.67, 30.67, 30.67, 30.67, 30.67, 30.67, 39, 39, 39]

---

### M2-Q5: Normalization numerical for value 145 (Solved)

Given cost price values:
100,150,140,115,190,120,130,125,135,145,140,150,165,160,170

#### Part (i): Min-Max normalization to [0,1]
Formula:
$$
v' = \frac{v-min}{max-min}
$$
Here: $v=145$, $min=100$, $max=190$
$$
v' = \frac{145-100}{190-100} = \frac{45}{90} = 0.5
$$
Final: Min-Max normalized value = 0.5

#### Part (ii): Z-score normalization (given standard deviation = 120)
First compute mean:
- Sum = 2135
- Count = 15
$$
\mu = \frac{2135}{15} = 142.33
$$
Formula:
$$
v' = \frac{v-\mu}{\sigma}
$$
$$
v' = \frac{145-142.33}{120} = \frac{2.67}{120} = 0.0223
$$
Final: Z-score value approx = 0.022

---

### M2-Q6: Approaches to clean incomplete, noisy, inconsistent data

Answer:
1. Missing values: ignore tuple, mean/median, class mean, model-based prediction.
2. Noisy data: binning, regression, clustering/outlier treatment.
3. Inconsistent data: rule checks, schema matching, constraint-based correction.

---

### M2-Q7: Explain PCA for dimensionality reduction

Answer:
1. Standardize/normalize attributes.
2. Compute covariance matrix.
3. Compute eigenvalues and eigenvectors.
4. Sort components by eigenvalue.
5. Select top k principal components.
6. Project original data into reduced k-dimensional space.

Benefit:
- Retains maximum variance with fewer dimensions.

---

## Module 3 Solved PYQs

### M3-Q1: What are the requirements for a good clustering algorithm?

Answer:
1. Scalable to large datasets.
2. Handles different cluster shapes and sizes.
3. Robust to noise and outliers.
4. Requires minimal domain-specific tuning.
5. Produces stable and interpretable clusters.
6. Ensures high intra-cluster similarity and low inter-cluster similarity.

---

### M3-Q2: Issues in implementing decision trees

Answer:
1. Overfitting with deep trees.
2. Instability from small data changes.
3. Bias toward high-cardinality attributes.
4. Data fragmentation after repeated splitting.
5. Greedy local decisions may miss globally optimal tree.
6. Pruning and generalization control are non-trivial.

---

### M3-Q3: Gain Ratio calculation and advantage over Information Gain

Formulas:
$$
IG(S,A) = Entropy(S) - \sum_v \frac{|S_v|}{|S|}Entropy(S_v)
$$
$$
SplitInfo(S,A) = -\sum_v \frac{|S_v|}{|S|}\log_2\frac{|S_v|}{|S|}
$$
$$
GainRatio(S,A) = \frac{IG(S,A)}{SplitInfo(S,A)}
$$

Advantage:
- Information Gain tends to favor attributes with many distinct values.
- Gain Ratio penalizes such splits using SplitInfo, giving more balanced attribute selection.

---

### M3-Q4: Distance metrics for tuples (22,1,42,10) and (20,0,36,8)

Given:
- A=(22,1,42,10)
- B=(20,0,36,8)
- Differences: (2,1,6,2)

#### (i) Euclidean distance
$$
D_E = \sqrt{2^2+1^2+6^2+2^2} = \sqrt{4+1+36+4} = \sqrt{45} = 6.708
$$

#### (ii) Manhattan distance
$$
D_M = |2|+|1|+|6|+|2| = 11
$$

#### (iii) Minkowski distance of order 3
$$
D_3 = (|2|^3+|1|^3+|6|^3+|2|^3)^{1/3}
= (8+1+216+8)^{1/3} = 233^{1/3} = 6.154
$$

Final:
- Euclidean = 6.708
- Manhattan = 11
- Minkowski (p=3) = 6.154

---

### M3-Q5: Confusion matrix + precision + recall (Solved)

Given:
- Total records = 80
- Relevant records = 55
- Retrieved records = 50
- Relevant among retrieved = 40

Find TP, FP, FN, TN:
1. TP = 40
2. FP = retrieved - relevant retrieved = 50 - 40 = 10
3. FN = relevant total - TP = 55 - 40 = 15
4. TN = total - (TP+FP+FN) = 80 - 65 = 15

Confusion matrix:

|                | Predicted Relevant | Predicted Irrelevant |
|---|---:|---:|
| Actual Relevant   | TP = 40 | FN = 15 |
| Actual Irrelevant | FP = 10 | TN = 15 |

Precision:
$$
Precision = \frac{TP}{TP+FP} = \frac{40}{40+10} = 0.8
$$

Recall:
$$
Recall = \frac{TP}{TP+FN} = \frac{40}{40+15} = \frac{40}{55} = 0.727
$$

Final:
- Precision = 0.80 (80%)
- Recall = 0.727 (72.7%)

---

### M3-Q6: Explain DBSCAN with advantages

Key parameters:
1. Eps: neighborhood radius
2. MinPts: minimum neighbors for dense region

Point types:
1. Core point: has at least MinPts neighbors in Eps radius
2. Border point: fewer neighbors but reachable from core point
3. Noise point: not density-reachable

Algorithm flow:
1. Start with unvisited point.
2. If core, expand cluster via density-reachability.
3. If not core and not reachable, mark noise.

Advantages:
1. Finds arbitrary-shaped clusters.
2. Automatically handles noise/outliers.
3. Does not require specifying number of clusters in advance.

---

### M3-Q7: K-Means clustering (short answer)

Steps:
1. Choose k initial centroids.
2. Assign each point to nearest centroid.
3. Recompute centroids as cluster means.
4. Repeat until convergence.

Limitations:
- Sensitive to initial centroids and outliers.
- Best suited for compact, spherical clusters.

---

### M3-Q8: PAM algorithm (short answer)

Steps:
1. Build phase: choose initial medoids.
2. Swap phase: test medoid replacements to reduce total dissimilarity.
3. Stop when no better swap exists.

Key advantage:
- Uses real points as cluster centers, so more robust than k-means for outliers.

---

### M3-Q9: SLIQ algorithm working

Answer:
1. Presorts continuous attributes once.
2. Uses class list to track records and labels.
3. Evaluates split criteria efficiently.
4. Selects best split and grows tree breadth-first.
5. Repeats recursively on child nodes.

Why used:
- Designed for large datasets with improved scalability.

---

## Final 30-Minute Exam Drill

1. Memorize module-wise formulas:
   - Min-max, z-score, IG, gain ratio, precision/recall, distance metrics.
2. Practice one full numerical from module 2 and one from module 3.
3. Practice one comparison table (OLTP vs OLAP or star vs snowflake).
4. Keep one algorithm skeleton each for K-means, DBSCAN, SLIQ.
5. In every long answer, keep structure fixed and neat.
