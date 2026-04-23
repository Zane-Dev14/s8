# STEP 3: Module 2 Crash Guide (Preprocessing, Reduction, Transformation)

Module focus:
- Cleaning real-world data
- Discretization and concept hierarchy
- Sampling and reduction
- Normalization and smoothing numericals

Questions asked repeatedly (non-duplicate):
Part A topics asked:
1. Importance of preprocessing before mining.
2. Smoothing by bin means/bin boundaries.
3. Min-max and z-score normalization basics.
4. Sampling methods in data reduction.
5. Purpose of discretization and concept hierarchy.

Part B topics asked:
1. Data preprocessing steps in detail.
2. Missing/noisy/inconsistent data cleaning approaches.
3. Numerosity reduction techniques.
4. Need for data transformation and methods.
5. Normalization numerical problems.
6. Sampling comparison with examples.
7. Discretization strategies and significance.
8. PCA for dimensionality reduction.

Answer format for this module:
- Part A: write exactly 5 points.
- Part B: write exactly 10 points.
- Numerical answers: formula line first, substitution next, final value last.

---

## 1) Why Preprocessing is Mandatory

Real data quality issues:
1. Incomplete: missing attribute values.
2. Noisy: random error and outliers.
3. Inconsistent: conflicting units/formats/rules.

Why marks are easy here:
- question appears often
- answer is structured list-based

---

## 2) Data Cleaning Approaches

## Missing values
1. Ignore tuple (if small impact).
2. Fill manually.
3. Global constant (Unknown).
4. Mean or median substitution.
5. Class-conditional mean.
6. Model-based prediction.

## Noisy data
1. Binning.
2. Regression smoothing.
3. Clustering-based outlier handling.

## Inconsistent data
1. Constraint checks.
2. Schema matching.
3. Unit and format standardization.
4. Rule-based correction.

---

## 3) Discretization and Concept Hierarchy

Definition:
Discretization converts continuous values into intervals or categories.

Why important:
1. Reduces model complexity.
2. Improves interpretability.
3. Helps rule and tree induction.

Common strategies:
1. Binning.
2. Histogram-based cuts.
3. Clustering-based cuts.
4. Decision-tree based cuts.
5. Correlation or ChiMerge based cuts.

Concept hierarchy example:
- Age: 16, 24, 35, 60 -> Young, Young, Middle-aged, Senior.
- Month: Jan-Mar -> Q1.

---

## 4) Sampling Methods

| Method | Core idea | Typical use |
|---|---|---|
| SRSWOR | Random sample without replacement | Avoid duplicate picks |
| SRSWR | Random sample with replacement | Probabilistic simulation settings |
| Cluster sampling | Sample entire groups | Naturally grouped data |
| Stratified sampling | Sample from each stratum | Preserve class distribution |

Exam tip:
If class balance matters, mention stratified sampling first.

---

## 5) Numerosity Reduction

## Parametric methods
1. Regression
2. Log-linear model

## Non-parametric methods
1. Histograms
2. Clustering
3. Sampling

Goal line:
Reduce data volume while preserving important information patterns.

---

## 6) Normalization Methods with Symbol Meaning

## Min-max normalization
$$
x' = \frac{x - x_{min}}{x_{max} - x_{min}}(new_{max}-new_{min}) + new_{min}
$$
For [0,1] range:
$$
x' = \frac{x - x_{min}}{x_{max} - x_{min}}
$$
Where:
- x is current value
- x_min and x_max are dataset extremes

## Z-score normalization
$$
x' = \frac{x - \mu}{\sigma}
$$
Where:
- mu is mean
- sigma is standard deviation

## Decimal scaling
$$
x' = \frac{x}{10^j}
$$
Choose smallest j such that all normalized values lie in (-1,1).

---

## 7) Worked Numerical 1: Smoothing by Bin Means

Given data:
[24, 27, 29, 16, 17, 31, 33, 29, 36, 37, 35, 44]

Step 1: Sort
[16, 17, 24, 27, 29, 29, 31, 33, 35, 36, 37, 44]

Step 2: Compute bin width for 3 equal-width bins
- min = 16, max = 44, range = 28
- width approx = 28/3 = 9.33 (use practical width 10)

Step 3: Form bins
1. Bin1 (16-25): 16, 17, 24
2. Bin2 (26-35): 27, 29, 29, 31, 33, 35
3. Bin3 (36-45): 36, 37, 44

Step 4: Bin means
1. Mean1 = (16+17+24)/3 = 19
2. Mean2 = (27+29+29+31+33+35)/6 = 30.67
3. Mean3 = (36+37+44)/3 = 39

Step 5: Replace values with corresponding bin mean
Smoothed result:
[19, 19, 19, 30.67, 30.67, 30.67, 30.67, 30.67, 30.67, 39, 39, 39]

---

## 8) Worked Numerical 2: Min-max and Z-score for x = 145

Given cost prices:
100, 150, 140, 115, 190, 120, 130, 125, 135, 145, 140, 150, 165, 160, 170

Given:
- x = 145
- x_min = 100
- x_max = 190
- sigma = 120

Step 1: Min-max to [0,1]
$$
x' = \frac{145-100}{190-100} = \frac{45}{90} = 0.5
$$
Answer: 0.5

Step 2: Mean for z-score
- sum = 2135
- count = 15
$$
\mu = \frac{2135}{15} = 142.33
$$

Step 3: Z-score
$$
x' = \frac{145-142.33}{120} = 0.0223
$$
Answer: approximately 0.022

---

## 9) PCA (Principal Component Analysis)

Definition:
PCA projects data onto orthogonal directions with maximum variance.

Steps:
1. Standardize data.
2. Build covariance matrix.
3. Compute eigenvalues and eigenvectors.
4. Sort by eigenvalue descending.
5. Choose top k components.
6. Project original data onto selected components.

One-line benefit:
Maximum variance retained with lower dimensionality.

---

## 10) Attribute Subset Selection

Definition:
Find minimal relevant attribute subset that preserves predictive quality.

Methods:
1. Forward selection.
2. Backward elimination.
3. Stepwise selection.

Benefits:
1. Faster training.
2. Reduced overfitting risk.
3. Better interpretation.

---

## 11) Data Integration vs Data Transformation

| Topic | Data integration | Data transformation |
|---|---|---|
| Purpose | Merge multiple data sources | Convert format/scale for mining |
| Typical issues | Schema conflict, redundancy | Scaling, smoothing, discretization |
| Output | Unified dataset | Model-ready dataset |

---

## Module 2 Final Drill

1. Solve one bin means numerical fully.
2. Solve one min-max and one z-score numerical.
3. Recite four discretization methods.
4. Write integration vs transformation in 3 lines.

---

## Part B Complete Answer Bank (All Asked Questions)

Use acronym for long answers:
- CLEAN-STEP
- Collect, Locate issues, Eliminate noise, Align formats, Normalize, Select/Transform, Evaluate, Publish.

## Q1) Explain data preprocessing steps in detail (10 points)
1. Preprocessing prepares raw data for accurate and efficient mining.
2. Step 1 is data cleaning to handle missing, noisy, inconsistent values.
3. Step 2 is data integration to merge multi-source data into unified schema.
4. Step 3 is data selection to choose relevant tuples and attributes.
5. Step 4 is transformation for scaling, smoothing, and aggregation.
6. Step 5 is reduction to lower dimensionality and data volume.
7. Step 6 is discretization where useful for rule/tree-based models.
8. Step 7 is quality validation through summary statistics and visual checks.
9. Pipeline diagram:

```text
Raw Data -> Cleaning -> Integration -> Selection -> Transformation -> Reduction -> Mining-ready Data
```

10. Good preprocessing directly improves model reliability and interpretability.

## Q2) Cleaning incomplete, noisy, inconsistent data (10 points)
1. Incomplete data is handled by deletion, imputation, or model-based fill.
2. Simple imputations include mean, median, and class-conditional mean.
3. Noisy data is reduced using binning, regression smoothing, or clustering.
4. Outliers are detected by distance, density, or statistical threshold methods.
5. Inconsistency is fixed by schema matching and business-rule validation.
6. Unit conflicts are normalized (for example kg vs g, date formats).
7. Duplicate detection and entity resolution avoid repeated records.
8. Constraint checks catch impossible values and relationship violations.
9. Post-cleaning audit ensures no critical information loss.
10. Final cleaned dataset should be complete, consistent, and mining-ready.

## Q3) Numerosity reduction techniques (10 points)
1. Numerosity reduction decreases data volume while preserving information.
2. Parametric approach: regression models approximate data behavior.
3. Parametric approach: log-linear models for multidimensional count data.
4. Non-parametric approach: histograms summarize value distributions.
5. Non-parametric approach: clustering replaces points by centroids/medoids.
6. Non-parametric approach: sampling keeps representative subset.
7. Data cube aggregation reduces granular measures to summaries.
8. Compression methods reduce storage and transfer overhead.
9. Quality is checked via error bounds and retained pattern fidelity.
10. Goal is faster mining with minimal accuracy degradation.

## Q4) Why data transformation is needed and methods (10 points)
1. Transformation aligns data with algorithm assumptions.
2. Smoothing removes random variation and local noise.
3. Aggregation summarizes detailed data to useful levels.
4. Generalization converts low-level values to higher-level categories.
5. Normalization scales attributes to comparable ranges.
6. Attribute construction creates informative derived features.
7. Discretization converts continuous values into intervals.
8. Encoding transforms categorical data for algorithm compatibility.
9. Transformation improves convergence speed and model stability.
10. Without transformation, model bias and poor generalization may occur.

## Q5) Normalization methods with solved pattern (10 points)
1. Min-max maps values to a predefined range, commonly [0,1].
2. Formula: x' = (x - xmin)/(xmax - xmin).
3. Z-score standardizes relative to mean and standard deviation.
4. Formula: x' = (x - mu)/sigma.
5. Decimal scaling shifts decimal by factor 10^j.
6. Formula: x' = x/10^j.
7. For x=145, xmin=100, xmax=190: min-max = (145-100)/(190-100)=0.5.
8. For mu=142.33 and sigma=120: z-score=(145-142.33)/120=0.0223.
9. Choose min-max for bounded features, z-score for normal-like distributions.
10. Always write formula first, substitution second, final value last.

## Q6) Sampling methods comparison with examples (10 points)
1. Sampling reduces computation by using representative subsets.
2. SRSWOR selects without replacement, so no repeated element.
3. SRSWR selects with replacement, so repeats are possible.
4. Stratified sampling preserves class distribution across strata.
5. Cluster sampling selects full groups instead of individual records.
6. For imbalanced classes, stratified is usually preferred.
7. SRS methods are unbiased but may miss minority groups by chance.
8. Cluster sampling is cost-effective when natural grouping exists.
9. Sample size should balance variance and computational budget.
10. State method choice based on data objective and class balance.

## Q7) Discretization significance and strategies (10 points)
1. Discretization converts continuous attributes into interval labels.
2. It simplifies model structure and improves interpretability.
3. It is useful in rule mining and decision-tree induction.
4. Equal-width binning divides range into fixed-size intervals.
5. Equal-frequency binning divides data into equal-count bins.
6. Histogram-based methods locate cut points from distribution shape.
7. Clustering-based discretization uses natural group boundaries.
8. Entropy/ChiMerge methods optimize class-separability at boundaries.
9. Concept hierarchy links intervals to semantic categories.
10. Discretization balances simplicity, noise reduction, and information retention.

## Q8) PCA for dimensionality reduction (10 points)
1. PCA transforms correlated variables into orthogonal principal components.
2. Standardize data so variables contribute comparably.
3. Compute covariance matrix on standardized features.
4. Compute eigenvalues and eigenvectors of covariance matrix.
5. Sort eigenvalues in descending order of explained variance.
6. Select top-k eigenvectors as principal component basis.
7. Project original data onto selected component space.
8. Retain maximum variance with fewer dimensions.
9. Diagram:

```text
Data -> Standardize -> Covariance -> Eigen Decomposition -> Select Top-k -> Projected Data
```

10. PCA reduces overfitting risk and improves training efficiency.
