# STEP 3: Module 2 Crash Guide (Preprocessing, Reduction, Transformation)

Module 2 focus:
- Data cleaning and preprocessing
- Sampling and numerosity reduction
- Discretization and normalization
- PCA and attribute subset selection

Mapped from OCR:
- DM/ocr_output/Data-Mining-Module-2-Important-Topics-PYQs.txt
- DM/ocr_output/series1.txt

---

## Topic 1: Why Data Preprocessing is Mandatory

Real-world data is:
1. Incomplete (missing values)
2. Noisy (random errors/outliers)
3. Inconsistent (conflicting formats/rules)

Preprocessing improves mining accuracy, speed, and reliability.

---

## Topic 2: Data Cleaning Approaches

## Missing values handling
1. Ignore tuple (if very few missing rows)
2. Fill manually
3. Global constant (Unknown)
4. Attribute mean/median
5. Class-specific mean/median
6. Most probable value (model-based)

## Noisy data handling
1. Binning
2. Regression
3. Clustering-based outlier handling

## Inconsistent data handling
1. Constraint checking
2. Rule-based correction
3. Schema/format standardization

---

## Topic 3: Data Discretization

Definition:
- Convert continuous values into intervals/categories.

Purpose:
1. Reduces distinct values
2. Makes patterns easier
3. Supports rule/tree models

Common strategies:
1. Binning (equal width/equal frequency)
2. Histogram-based
3. Clustering-based
4. Decision-tree-based splits
5. Correlation/ChiMerge-based

---

## Topic 4: Sampling Methods

1. SRSWOR: simple random sample without replacement
2. SRSWR: simple random sample with replacement
3. Cluster sampling: sample entire groups
4. Stratified sampling: sample from each stratum

When to use stratified:
- If classes are imbalanced and each class must be represented.

---

## Topic 5: Numerosity Reduction

## Parametric methods
1. Regression
2. Log-linear models

## Non-parametric methods
1. Histograms
2. Clustering
3. Sampling

Goal:
- Smaller data size while preserving core information.

---

## Topic 6: Data Normalization Methods

## Min-Max normalization
Formula:
$$
v' = \frac{v - min_A}{max_A - min_A}(new\_max_A - new\_min_A) + new\_min_A
$$
If range is [0,1]:
$$
v' = \frac{v - min_A}{max_A - min_A}
$$

## Z-score normalization
Formula:
$$
v' = \frac{v - \mu}{\sigma}
$$
where $\mu$ = mean, $\sigma$ = standard deviation.

## Decimal scaling
Formula:
$$
v' = \frac{v}{10^j}
$$
Choose smallest $j$ so all normalized values are in (-1,1).

---

## Topic 7: Data Smoothing by Bin Means

Procedure:
1. Sort data
2. Form bins (equal width or equal frequency)
3. Compute mean of each bin
4. Replace each value in bin with bin mean

Exam tip:
- Always show bin construction before smoothed output.

---

## Topic 8: PCA (Principal Component Analysis)

Definition:
- Dimensionality reduction by projecting data on orthogonal directions with max variance.

Steps:
1. Standardize data
2. Compute covariance matrix
3. Find eigenvalues/eigenvectors
4. Sort by eigenvalue descending
5. Select top k components
6. Project original data to k-dimensional space

---

## Topic 9: Attribute Subset Selection

Definition:
- Select minimal relevant attributes that preserve predictive performance.

Methods:
1. Forward selection
2. Backward elimination
3. Stepwise selection

Benefits:
1. Faster training
2. Better interpretability
3. Less overfitting risk

---

## Topic 10: Data Integration vs Data Transformation

## Data integration
- Merge data from multiple sources into unified schema.
- Handle naming conflicts, redundancy, and unit mismatches.

## Data transformation
- Convert data format/scale for mining.
- Includes normalization, aggregation, smoothing, discretization.

---

## Module 2 PYQ Attack Set

1. Significance of preprocessing
2. Missing/noisy/inconsistent data handling
3. Discretization purpose + strategies
4. Sampling method differences
5. Smoothing by bin means numerical
6. Min-max and z-score numerical
7. Numerosity reduction techniques
8. PCA with example
9. Attribute subset selection
10. Data integration vs transformation

---

## Last-Minute Revision Grid

1. Memorize normalization formulas exactly.
2. Practice one binning numerical end-to-end.
3. Practice one min-max and one z-score numerical.
4. Memorize 4 discretization strategies.
5. Keep 3-line differentiation for integration vs transformation.
