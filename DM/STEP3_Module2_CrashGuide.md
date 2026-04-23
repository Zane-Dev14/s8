# STEP 3: Module 2 Crash Guide (Preprocessing, Reduction, Transformation)

Module focus:
- Cleaning real-world data
- Discretization and concept hierarchy
- Sampling and reduction
- Normalization and smoothing numericals

Questions asked repeatedly (non-duplicate):
- Importance of preprocessing before mining
- Methods for handling missing/noisy/inconsistent data
- Smoothing by bin means/bin boundaries numerical
- Min-max, z-score, decimal scaling numerical
- Sampling methods: SRSWOR, SRSWR, stratified
- Numerosity reduction techniques
- Discretization significance and strategies
- PCA for dimensionality reduction

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
