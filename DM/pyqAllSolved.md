# Data Mining PYQ All Solved (OCR Source Truth)

This file is built from OCR sources in `DM/ocr_output` and extraction in `DM/build`.
Question wording is normalized from repeated exam variants in `DataMining_combined.txt`.

## OCR Source Files Used
- `DM/ocr_output/DataMining_combined.txt`
- `DM/build/DataMiningCombined_unique_questions.json`
- `DM/build/DataMiningCombined_question_sources.json`
- `DM/ocr_output/CST466_DATA_MINING,_JUNE_2023.txt`
- `DM/ocr_output/CST466_DATA_MINING,_MAY_2024.txt`
- `DM/ocr_output/CST466_DATA_MINING,_APRIL_2025.txt`
- `DM/ocr_output/Data-Mining-Module-1-Important-Topics-PYQs.txt`
- `DM/ocr_output/Data-Mining-Module-2-Important-Topics-PYQs.txt`
- `DM/ocr_output/mod3.txt`
- `DM/ocr_output/Data-Mining-Module-4-Important-Topics-PYQs.txt`
- `DM/ocr_output/Data-Mining-Module-5-Important-Topics-PYQs.txt`

---

## Section 1: Module-wise Unique Question Bank

## Module 1

### Part A (5-mark style)
- M1A1. List any three applications of data mining in day-to-day life.
- M1A2. Explain roll-up and drill-down with suitable examples.
- M1A3. Illustrate the multi-dimensional data model with a neat figure.
- M1A4. Differentiate OLTP and OLAP.
- M1A5. List the major features/applications of a data warehouse.

### Part B (10-mark style)
- M1B1. Explain the three-tier architecture of a data warehouse with diagram.
- M1B2. Explain star schema, snowflake schema, and fact constellation with examples.
- M1B3. Explain OLAP operations and compare ROLAP, MOLAP, HOLAP.
- M1B4. Explain KDD stages / stages of data mining in BI with diagram.
- M1B5. Design a warehouse schema and list OLAP operations to answer managerial query.

## Module 2

### Part A (5-mark style)
- M2A1. Perform data smoothing by bin means/bin boundaries on 3 equi-width bins.
- M2A2. Explain concept hierarchy with examples.
- M2A3. Why is data preprocessing important before mining?
- M2A4. Explain sampling methods used in data reduction.
- M2A5. Explain purpose of data discretization and strategies.

### Part B (10-mark style)
- M2B1. Explain techniques to handle missing/noisy/inconsistent data.
- M2B2. Explain numerosity reduction and data transformation methods.
- M2B3. Explain discretization strategies and illustrate PCA.
- M2B4. Solve smoothing problem using bin means and bin boundaries.
- M2B5. Solve normalization problems (min-max, z-score, decimal scaling).

## Module 3

### Part A (5-mark style)
- M3A1. Compute Euclidean, Manhattan and Minkowski distances.
- M3A2. Precision vs recall for spam classifier: which is more important and why?
- M3A3. Draw confusion matrix and compute precision/recall.
- M3A4. Explain gain ratio and its advantage over information gain.
- M3A5. Requirements of a good clustering algorithm / issues in decision tree.

### Part B (10-mark style)
- M3B1. Use ID3 to find first splitting attribute for given dataset.
- M3B2. Compute gain (Gini/IG) and choose root attribute; explain DBSCAN.
- M3B3. Explain PAM and ROCK clustering with examples.
- M3B4. Explain SLIQ algorithm with example.
- M3B5. Build confusion matrix from retrieval problem and compute metrics.

## Module 4

### Part A (5-mark style)
- M4A1. Methods to improve efficiency of Apriori.
- M4A2. Define support, confidence, frequent itemset.
- M4A3. Explain dynamic itemset counting (DIC).
- M4A4. Explain bi-directional pruning in Pincer Search.
- M4A5. Compare partition algorithm with Apriori.

### Part B (10-mark style)
- M4B1. Apriori principle and frequent itemsets for given dataset.
- M4B2. Find frequent itemsets and strong rules (given minsup/minconf).
- M4B3. Explain partition algorithm and why it reduces Apriori cost.
- M4B4. Explain FP-Growth and solve frequent itemset mining on transaction set.
- M4B5. Explain DIC dashed/solid transition with example.

## Module 5

### Part A (5-mark style)
- M5A1. Explain web mining taxonomy.
- M5A2. Differentiate web content, structure, and usage mining.
- M5A3. Compare focused crawling and regular crawling.
- M5A4. Explain pre-processing and pattern analysis in web usage mining.
- M5A5. Explain text retrieval indexing and TF-IDF basics.

### Part B (10-mark style)
- M5B1. Describe web content mining techniques and text mining approaches.
- M5B2. Describe text retrieval methods and relation among TM, IR, IE.
- M5B3. Explain HITS and CLEVER algorithms.
- M5B4. Explain web usage mining applications, traversal patterns, and discovery methods.
- M5B5. Compute TF-IDF from term-document matrix (stepwise).

---

## Section 2: Solved Answers

## Module 1 - Part A (5 points each)

### M1A1. Applications of Data Mining
1. Retail: market basket analysis for product bundling and cross-selling.
2. Banking: fraud detection and credit risk scoring.
3. Healthcare: disease prediction and treatment outcome analysis.
4. Telecom: churn prediction and customer segmentation.
5. E-commerce: recommendation systems and personalization.

### M1A2. Roll-up and Drill-down
1. Roll-up aggregates data from lower level to higher level.
2. Drill-down moves from summary to detailed levels.
3. Example dimension hierarchy: Day -> Month -> Quarter -> Year.
4. Roll-up example: sum daily sales to monthly sales.
5. Drill-down example: yearly sales to state -> city -> store level.

### M1A3. Multi-dimensional Data Model
1. Data is represented as cube with dimensions and measures.
2. Dimensions: Time, Product, Location.
3. Measures: sales amount, quantity, profit.
4. Each cell stores aggregated fact values.
5. Enables OLAP analysis through slice, dice, roll-up, drill-down.

### M1A4. OLTP vs OLAP
1. OLTP is transaction-oriented; OLAP is analysis-oriented.
2. OLTP uses current operational data; OLAP uses historical integrated data.
3. OLTP supports many short updates; OLAP supports complex read-heavy queries.
4. OLTP schema is normalized ER; OLAP schema is star/snowflake.
5. OLTP users are clerks/apps; OLAP users are analysts/managers.

### M1A5. Features of Data Warehouse
1. Subject-oriented: organized around business subjects.
2. Integrated: combines data from heterogeneous sources.
3. Time-variant: maintains historical snapshots.
4. Non-volatile: mostly read-only, periodic loading.
5. Supports strategic reporting, trend analysis, and BI dashboards.

## Module 1 - Part B (10+ points, diagram + formula)

### M1B1. Three-tier Data Warehouse Architecture
1. Bottom tier stores cleansed, integrated warehouse data.
2. ETL pipeline extracts, transforms, and loads source data.
3. Middle tier provides OLAP server for multidimensional analysis.
4. Top tier contains front-end tools (query, reporting, dashboard, mining).
5. Metadata repository stores schema, mappings, lineage.
6. Data marts can be created for departments.
7. Refresh can be batch/near-real-time.
8. Security controls access by role.
9. Performance improved by indexing/materialized views.
10. Architecture separates storage, computation, and presentation concerns.

Diagram:
```text
Operational DBs/Files/APIs
          |
         ETL
          |
+-----------------------+
| Bottom Tier: DW       |
| fact + dimensions     |
+-----------------------+
          |
+-----------------------+
| Middle Tier: OLAP     |
| ROLAP / MOLAP / HOLAP |
+-----------------------+
          |
+-----------------------+
| Top Tier: BI Tools    |
| reports, dashboards   |
+-----------------------+
```

Formula:
$$
\text{Warehouse Load Window} = \text{Extract Time} + \text{Transform Time} + \text{Load Time}
$$

### M1B2. Star, Snowflake, Fact Constellation
1. Star: one fact table connected to denormalized dimensions.
2. Snowflake: dimensions further normalized into sub-dim tables.
3. Fact constellation: multiple fact tables sharing dimensions.
4. Star has simpler joins and faster query.
5. Snowflake reduces redundancy but increases joins.
6. Constellation models multiple business processes.
7. Example star: SalesFact(Time, Product, Store, Amount).
8. Example snowflake: Product -> Brand -> Category tables.
9. Example constellation: SalesFact and InventoryFact share Time/Product.
10. Schema choice depends on performance vs storage/maintainability.

Diagram:
```text
Star:
          DimTime
             |
DimStore -- FactSales -- DimProduct
             |
          DimCustomer

Snowflake:
DimCategory <- DimProduct -> DimBrand
                 |
               FactSales
```

Formula:
$$
\text{Storage Redundancy} \propto \sum \text{duplicate dimension attribute values}
$$

### M1B3. OLAP Operations + ROLAP/MOLAP/HOLAP
1. Roll-up aggregates to higher hierarchy level.
2. Drill-down decomposes into lower level detail.
3. Slice fixes one dimension value to get sub-cube.
4. Dice selects ranges on multiple dimensions.
5. Pivot rotates axes for alternate view.
6. ROLAP stores in relational tables, SQL-based.
7. MOLAP stores in multidimensional cubes, very fast aggregates.
8. HOLAP combines relational detail + multidimensional summaries.
9. Query type and data volume decide architecture.
10. Pre-aggregation improves response for OLAP reports.

Diagram:
```text
3D Cube (Time, Product, Region)
- Slice: Time = 2024
- Dice: Product in {A,B}, Region in {N,S}
- Roll-up: Month -> Quarter
- Drill-down: Year -> Quarter -> Month
```

Formula:
$$
\text{Roll-up Aggregate} = \sum_{i=1}^{n} x_i, \quad \text{Average} = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

### M1B4. KDD Process with Stages
1. Data cleaning removes noise/missing inconsistencies.
2. Data integration merges multiple sources.
3. Data selection chooses relevant subsets.
4. Data transformation normalizes/aggregates/constructs features.
5. Data mining applies algorithms for patterns.
6. Pattern evaluation filters useful knowledge.
7. Knowledge presentation visualizes discovered patterns.
8. Iterative feedback improves quality.
9. Domain knowledge is used across stages.
10. Final output supports decision making.

Diagram:
```text
Sources -> Cleaning -> Integration -> Selection
       -> Transformation -> Mining -> Evaluation -> Presentation
```

Formula:
$$
\text{Interestingness Score} = f(\text{support},\ \text{confidence},\ \text{lift})
$$

### M1B5. Warehouse Design + OLAP Operations for Query
1. Identify dimensions (time, doctor, patient) and measure (charge).
2. Build fact table with foreign keys and measure attributes.
3. Create star/snowflake dimension hierarchy (day->month->year).
4. Load transactional visit records into fact table.
5. Start from base cuboid [day, doctor, patient].
6. Slice by year = 2023.
7. Roll-up day -> month -> year for charge summary.
8. Dice optional by specialty/hospital branch.
9. Group by doctor to get total fee per doctor.
10. Validate totals with source ledger.

Diagram:
```text
DimTime(day,month,year)
DimDoctor(doctor_id,specialty)
DimPatient(patient_id,age_group)
          \      |      /
           \   FactVisit(charge,count)
```

Formula:
$$
\text{Total Fee by Doctor} = \sum_{v \in \text{visits of doctor}} \text{charge}(v)
$$

---

## Module 2 - Part A (5 points each)

### M2A1. Data Smoothing by Binning
1. Sort data first.
2. Split into equal-width bins.
3. Bin means: replace values by bin average.
4. Bin boundaries: replace by nearest boundary value.
5. Smoothing reduces local noise and outlier influence.

### M2A2. Concept Hierarchy
1. Concept hierarchy generalizes low-level data to higher abstraction.
2. Example: street -> city -> state -> country.
3. Example: day -> month -> quarter -> year.
4. It reduces cardinality and improves mining speed.
5. Useful in roll-up and data cube operations.

### M2A3. Significance of Preprocessing
1. Real data has missing values and noise.
2. Inconsistencies produce misleading patterns.
3. Normalization prevents attribute-scale dominance.
4. Reduction/discretization improves computation efficiency.
5. Better preprocessing improves model accuracy and interpretability.

### M2A4. Sampling Methods
1. SRSWOR: random sample without replacement.
2. SRSWR: random sample with replacement.
3. Cluster sampling: sample groups, not individual tuples.
4. Stratified sampling: sample within each stratum.
5. Sampling lowers cost while preserving distribution.

### M2A5. Data Discretization Purpose
1. Converts continuous attributes into intervals/categories.
2. Reduces number of distinct values.
3. Improves performance of rule/tree algorithms.
4. Helps interpretability (e.g., age group).
5. Strategies: top-down splitting, bottom-up merging, entropy/binning.

## Module 2 - Part B (10+ points, diagram + formula)

### M2B1. Handling Missing, Noisy, Inconsistent Data
1. Missing values can be ignored, imputed, or predicted.
2. Mean/median/mode imputation used for numeric/categorical.
3. Class-wise mean gives better contextual fill.
4. Regression/kNN imputation can model dependencies.
5. Noise handled using binning, regression, clustering.
6. Outliers detected by z-score/IQR.
7. Inconsistency resolved by constraints and domain rules.
8. Deduplication and schema alignment remove integration conflicts.
9. Data cleaning log must track each correction.
10. Clean data directly improves downstream model reliability.

Diagram:
```text
Raw Data -> Missing Handler -> Noise Filter -> Consistency Check -> Clean Data
```

Formula:
$$
z = \frac{x - \mu}{\sigma}, \quad |z| > 3 \Rightarrow \text{possible outlier}
$$

### M2B2. Numerosity Reduction and Data Transformation
1. Numerosity reduction compresses dataset while preserving information.
2. Parametric methods: regression, log-linear model.
3. Non-parametric methods: histograms, clustering, sampling.
4. Data transformation includes normalization and aggregation.
5. Smoothing reduces random variation.
6. Attribute construction creates useful derived features.
7. Generalization maps detailed values to higher concepts.
8. Transformation improves algorithm compatibility.
9. Reduction lowers memory and execution time.
10. Choice depends on objective and acceptable information loss.

Diagram:
```text
High-volume Data -> Reduction Layer -> Compact Representation -> Mining
```

Formula:
$$
\text{Compression Ratio} = \frac{\text{Original Size}}{\text{Reduced Size}}
$$

### M2B3. Discretization Strategies + PCA
1. Discretization by binning (equal width/equal frequency).
2. Histogram-based discretization using frequency buckets.
3. Entropy-based split using class information gain.
4. ChiMerge merges adjacent intervals statistically.
5. PCA reduces dimensionality while preserving variance.
6. Standardize variables before PCA.
7. Compute covariance matrix and eigen decomposition.
8. Sort eigenvalues; pick top-k principal components.
9. Project original data onto chosen components.
10. Reduced data is compact and less noisy.

Diagram:
```text
X (n x d) -> Standardize -> Covariance -> Eigenvectors -> Top-k PCs -> X' (n x k)
```

Formula:
$$
X' = XW_k, \quad \text{Explained Variance Ratio}_i = \frac{\lambda_i}{\sum_j \lambda_j}
$$

### M2B4. Numerical: Smoothing by Bin Means and Bin Boundaries
Given sorted data from OCR style question:
[4, 8, 9, 15, 21, 21, 24, 25, 26, 28, 29, 34], 3 bins.

Step table 1: Create bins (equal frequency, 4 per bin)

| Bin | Values |
|---|---|
| B1 | 4, 8, 9, 15 |
| B2 | 21, 21, 24, 25 |
| B3 | 26, 28, 29, 34 |

Step table 2: Bin means

| Bin | Mean |
|---|---|
| B1 | (4+8+9+15)/4 = 9 |
| B2 | (21+21+24+25)/4 = 22.75 |
| B3 | (26+28+29+34)/4 = 29.25 |

Smoothed by bin means:
[9, 9, 9, 9, 22.75, 22.75, 22.75, 22.75, 29.25, 29.25, 29.25, 29.25]

Step table 3: Bin boundaries

| Bin | Lower | Upper | Replacements |
|---|---:|---:|---|
| B1 | 4 | 15 | 4,4,4,15 |
| B2 | 21 | 25 | 21,21,25,25 |
| B3 | 26 | 34 | 26,26,26,34 |

Smoothed by bin boundaries:
[4, 4, 4, 15, 21, 21, 25, 25, 26, 26, 26, 34]

Diagram:
```text
Raw -> Sort -> Bin -> (Mean or Boundary Replace) -> Smoothed Data
```

Formula:
$$
\text{Bin Mean} = \frac{1}{k}\sum_{i=1}^{k} x_i, \quad
\text{Boundary Replace}(x)=\arg\min_{b \in \{L,U\}}|x-b|
$$

### M2B5. Numerical: Normalization (Min-Max, Z-score, Decimal)
Question style 1: normalize x=145 in [100,150,140,115,190,120,130,125,135,145,140,150,165,160,170].

Step table 1: Basic stats

| Item | Value |
|---|---:|
| min | 100 |
| max | 190 |
| x | 145 |

Min-max to [0,1]:
$$
x' = \frac{x-min}{max-min} = \frac{145-100}{190-100} = \frac{45}{90}=0.5
$$

If mean = 145 and sigma = 120 (as given):
$$
z = \frac{x-\mu}{\sigma} = \frac{145-145}{120}=0
$$

Question style 2: x=550 in [50,150,250,350,450,550,650,700,850,950,1000].

Step table 2: Min-max

| x | min | max | x' |
|---:|---:|---:|---:|
| 550 | 50 | 1000 | (550-50)/(1000-50)=500/950=0.5263 |

Step table 3: Decimal scaling

| max abs value | j | x' |
|---:|---:|---:|
| 1000 | 4 | 550/10^4 = 0.055 |

Diagram:
```text
Original x -> [Choose method] -> Normalized x'
```

Formula:
$$
\text{MinMax: }x' = \frac{x-min}{max-min}, \quad
\text{Z-score: }z = \frac{x-\mu}{\sigma}, \quad
\text{Decimal: }x' = \frac{x}{10^j}
$$

---

## Module 3 - Part A (5 points each)

### M3A1. Distance Measures
1. Euclidean distance: straight-line metric in feature space.
2. Manhattan distance: sum of absolute coordinate differences.
3. Minkowski generalizes both with order p.
4. Higher p emphasizes larger coordinate deviations.
5. Distances are used in clustering and nearest-neighbor classification.

### M3A2. Precision vs Recall for Spam
1. Precision: fraction of predicted spam that is truly spam.
2. Recall: fraction of true spam detected.
3. If missing spam is costly, prioritize recall.
4. If false blocking of legitimate mails is costly, prioritize precision.
5. Practical systems optimize F1 or tune threshold by business objective.

### M3A3. Confusion Matrix Basics
1. TP: positive predicted positive.
2. TN: negative predicted negative.
3. FP: negative predicted positive.
4. FN: positive predicted negative.
5. Precision = TP/(TP+FP), Recall = TP/(TP+FN).

### M3A4. Gain Ratio
1. Information gain prefers attributes with many values.
2. Gain ratio normalizes information gain using split info.
3. It penalizes highly fragmented splits.
4. Better attribute selection for decision trees.
5. Commonly used in C4.5.

### M3A5. Good Clustering + Decision Tree Issues
1. Clustering should be scalable and robust to noise.
2. Should detect arbitrary shapes and different densities.
3. Decision trees can overfit without pruning.
4. Trees can be unstable for small data perturbations.
5. Attribute bias (many-valued attributes) affects split quality.

## Module 3 - Part B (10+ points, diagram + formula)

### M3B1. ID3 First Splitting Attribute
1. Compute entropy of class labels in whole dataset.
2. For each attribute, partition dataset by attribute values.
3. Compute entropy of each partition.
4. Compute weighted entropy after split.
5. Information gain = parent entropy - weighted entropy.
6. Repeat for all candidate attributes.
7. Attribute with highest gain becomes root.
8. Continue recursively for child nodes.
9. Stop if node is pure or no attribute remains.
10. Apply pruning to avoid overfitting.

Diagram:
```text
Dataset S
  |
IG(Age), IG(Outlook), IG(Humidity), ...
  |
Best IG -> Root Node
```

Formula:
$$
H(S) = -\sum_{c} p(c)\log_2 p(c), \quad
IG(S,A)=H(S)-\sum_{v\in Values(A)}\frac{|S_v|}{|S|}H(S_v)
$$

### M3B2. Gain (Gini/IG) + DBSCAN
1. Gini impurity measures class mixing in node.
2. Split with lowest weighted Gini is better.
3. Information gain uses entropy reduction.
4. Compare both metrics for attributes A and B.
5. Root chosen by best impurity reduction.
6. DBSCAN is density-based clustering.
7. Parameters: eps and MinPts.
8. Point types: core, border, noise.
9. Finds arbitrary shape clusters.
10. Handles outliers naturally.

Diagram:
```text
Dense region -> Core points
Boundary around dense region -> Border points
Far isolated points -> Noise
```

Formula:
$$
\text{Gini}(S)=1-\sum_c p(c)^2, \quad
\Delta\text{Gini}(A)=\text{Gini}(S)-\sum_v \frac{|S_v|}{|S|}\text{Gini}(S_v)
$$

### M3B3. PAM and ROCK
1. PAM chooses actual data points as medoids.
2. Build phase picks initial k medoids.
3. Swap phase tries medoid/non-medoid exchanges.
4. Keep swap if total dissimilarity reduces.
5. PAM is robust vs k-means for outliers.
6. ROCK clusters categorical data using links.
7. Link count = common neighbors between points.
8. Merge clusters maximizing goodness measure.
9. Suitable when distance is not ideal for categories.
10. Both are partition-style but with different similarity logic.

Diagram:
```text
PAM: points -> choose medoids -> assign -> swap optimize
ROCK: graph nodes -> links -> agglomerative merge
```

Formula:
$$
\text{PAM Cost} = \sum_{i=1}^{n} d(x_i, m(x_i)), \quad
\text{ROCK Link}(x_i,x_j)=|N(x_i)\cap N(x_j)|
$$

### M3B4. SLIQ Algorithm
1. SLIQ is a scalable decision tree algorithm.
2. Uses presorted attribute lists for numeric attributes.
3. Maintains separate class list for tuple class labels.
4. Evaluates split candidates efficiently without repeated sorting.
5. Uses Gini index for split quality.
6. Grows tree in breadth-first manner.
7. Handles large datasets better than naive tree induction.
8. Uses disk-friendly data structures.
9. Supports pruning phase to reduce overfitting.
10. Produces interpretable decision rules.

Diagram:
```text
Attribute Lists + Class List -> Best Split -> BFS Tree Growth -> Pruning
```

Formula:
$$
\text{Best Split} = \arg\min_s \left(\frac{|L_s|}{|S|}\text{Gini}(L_s)+\frac{|R_s|}{|S|}\text{Gini}(R_s)\right)
$$

### M3B5. Numerical: Retrieval Confusion Matrix (80,55,50,40)
Given:
- Total records = 80
- Relevant records = 55
- Retrieved = 50
- Retrieved relevant = 40

Step table 1: Derive confusion entries

| Metric | Value | Reason |
|---|---:|---|
| TP | 40 | retrieved and relevant |
| FP | 10 | retrieved - TP = 50-40 |
| FN | 15 | relevant - TP = 55-40 |
| TN | 15 | total - TP - FP - FN = 80-40-10-15 |

Step table 2: Evaluation metrics

| Metric | Formula | Value |
|---|---|---:|
| Precision | TP/(TP+FP) | 40/50 = 0.80 |
| Recall | TP/(TP+FN) | 40/55 = 0.7273 |
| Specificity | TN/(TN+FP) | 15/25 = 0.60 |
| Accuracy | (TP+TN)/Total | 55/80 = 0.6875 |

Diagram:
```text
                Predicted +    Predicted -
Actual +            TP=40          FN=15
Actual -            FP=10          TN=15
```

Formula:
$$
\text{Precision}=\frac{TP}{TP+FP},\quad
\text{Recall}=\frac{TP}{TP+FN},\quad
\text{Specificity}=\frac{TN}{TN+FP}
$$

---

## Module 4 - Part A (5 points each)

### M4A1. Apriori Efficiency Improvements
1. Hash-based candidate pruning.
2. Transaction reduction between passes.
3. Partition-based frequent itemset filtering.
4. Sampling to cut candidate generation cost.
5. Dynamic itemset counting to reduce full scans.

### M4A2. Support, Confidence, Frequent Itemset
1. Support is occurrence frequency in all transactions.
2. Confidence is conditional probability of RHS given LHS.
3. Frequent itemset satisfies minimum support.
4. Rules are generated from frequent itemsets.
5. Lift can be used to measure true association strength.

### M4A3. Dynamic Itemset Counting
1. DIC introduces candidates during scan intervals.
2. Avoids strict pass-wise Apriori level barrier.
3. Uses dashed and solid boxes for itemset states.
4. Promotes itemset when enough evidence appears.
5. Reduces number of complete database scans.

### M4A4. Pincer Search Bi-directional Pruning
1. Bottom-up search from small frequent itemsets.
2. Top-down search over maximal frequent candidates.
3. If subset infrequent, supersets are pruned.
4. If maximal set frequent, subsets can be skipped.
5. Bidirectional pruning reduces candidate explosion.

### M4A5. Partition vs Apriori
1. Apriori performs many full scans.
2. Partition algorithm scans full DB only twice.
3. Local frequent itemsets are mined per partition.
4. Global candidates are union of local frequent sets.
5. Better I/O efficiency on large databases.

## Module 4 - Part B (10+ points, diagram + formula)

### M4B1. Apriori Principle + Frequent Itemsets (min support count = 2)
Dataset used (clean OCR variant):
T1 {A,B}
T2 {B,C}
T3 {A,C}
T4 {A,B,C}
T5 {A,B,C,E}

Step table 1: C1/L1

| Item | Support |
|---|---:|
| A | 4 |
| B | 4 |
| C | 4 |
| E | 1 |

L1 = {A,B,C}

Step table 2: C2/L2

| Itemset | Support |
|---|---:|
| {A,B} | 3 |
| {A,C} | 3 |
| {B,C} | 3 |

L2 = all above

Step table 3: C3/L3

| Itemset | Support |
|---|---:|
| {A,B,C} | 2 |

L3 = {{A,B,C}}

Final frequent itemsets: {A}, {B}, {C}, {A,B}, {A,C}, {B,C}, {A,B,C}

Diagram:
```text
L1 -> join -> C2 -> prune -> L2 -> join -> C3 -> prune -> L3
```

Formula:
$$
\text{Apriori Property: } (X \text{ frequent}) \Rightarrow (\forall Y\subset X,\ Y \text{ frequent})
$$

### M4B2. Strong Rules (minsup 33.33%, minconf 60%)
Using frequent itemsets from M4B1 with N=6 style threshold, minsup count approx 2.

Step table 1: Rule confidence

| Rule | Support(XY) | Support(X) | Confidence |
|---|---:|---:|---:|
| A -> B | 3 | 4 | 75% |
| B -> A | 3 | 4 | 75% |
| A -> C | 3 | 4 | 75% |
| C -> A | 3 | 4 | 75% |
| B -> C | 3 | 4 | 75% |
| C -> B | 3 | 4 | 75% |
| AB -> C | 2 | 3 | 66.67% |
| AC -> B | 2 | 3 | 66.67% |
| BC -> A | 2 | 3 | 66.67% |

All above satisfy minconf 60%.

Diagram:
```text
Frequent Itemsets -> Candidate Rules -> Confidence Filter -> Strong Rules
```

Formula:
$$
\text{support}(X\Rightarrow Y)=\frac{\sigma(X\cup Y)}{N},\quad
\text{confidence}(X\Rightarrow Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}
$$

### M4B3. Partition Algorithm for Large Itemsets
1. Divide DB into non-overlapping partitions.
2. Mine frequent itemsets locally in each partition.
3. Union local frequent itemsets as global candidate set.
4. Scan full DB once more to verify global support.
5. Any globally frequent itemset must be locally frequent in at least one partition.
6. So candidate set is far smaller than full combinatorial set.
7. Reduces repeated full-database scans.
8. Works well with distributed processing.
9. Compatible with Apriori-like counting in each partition.
10. Main advantage is I/O reduction.

Diagram:
```text
DB -> P1,P2,...,Pk -> Local Frequent Sets -> Union Candidates -> Global Count
```

Formula:
$$
X \in L_{global} \Rightarrow \exists i,\ X \in L_i
$$

### M4B4. FP-Growth with Example
Dataset (clean OCR variant):
T1 {milk,bread,eggs}
T2 {milk,bread,butter}
T3 {bread,butter}
T4 {milk,bread}
T5 {bread,eggs}
min support = 40% of 5 = 2

Step table 1: Frequent 1-items

| Item | Support |
|---|---:|
| bread | 5 |
| milk | 3 |
| eggs | 2 |
| butter | 2 |

Step table 2: Frequent 2-items

| Itemset | Support |
|---|---:|
| {bread,milk} | 3 |
| {bread,eggs} | 2 |
| {bread,butter} | 2 |
| {milk,butter} | 1 (not frequent) |
| {milk,eggs} | 1 (not frequent) |

Step table 3: Frequent 3-items

| Itemset | Support |
|---|---:|
| {bread,milk,eggs} | 1 (not frequent) |
| {bread,milk,butter} | 1 (not frequent) |

Final frequent itemsets: {bread}, {milk}, {eggs}, {butter}, {bread,milk}, {bread,eggs}, {bread,butter}

Diagram:
```text
DB Scan -> Header Table -> FP-Tree -> Conditional Pattern Base -> Frequent Itemsets
```

Formula:
$$
\sigma(X)=|\{t \in D: X\subseteq t\}|,\quad X\text{ is frequent if }\sigma(X)\ge minsup
$$

### M4B5. Dynamic Itemset Counting (DIC)
1. DIC splits DB scan into checkpoints.
2. Itemsets tracked in dashed circles while still counting.
3. Once support crosses minsup and full scan condition met, move to solid frequent set.
4. If cannot reach minsup, move to solid infrequent set.
5. New candidate supersets may be generated during same pass.
6. Reduces waiting for full pass completion.
7. Useful when DB is very large and incremental counts matter.
8. Dashed->solid transition depends on count + scan completion.
9. Maintains candidate state machine for each itemset.
10. Practical speedup over strict pass-level Apriori.

Diagram:
```text
Dashed Circle (candidate counting)
   | if count>=minsup and checkpoint condition met
   v
Solid Circle (confirmed frequent)

Dashed Square (candidate)
   | if impossible to reach minsup
   v
Solid Square (confirmed infrequent)
```

Formula:
$$
\text{Promote to frequent if }\sigma_t(X)\ge minsup\ \text{and required scan window completed}
$$

---

## Module 5 - Part A (5 points each)

### M5A1. Web Mining Taxonomy
1. Web content mining analyzes page content (text/media).
2. Web structure mining analyzes hyperlink graph.
3. Web usage mining analyzes clickstream/log behavior.
4. All three complement each other for web intelligence.
5. Applications include search ranking, personalization, and recommendation.

### M5A2. Content vs Structure vs Usage
1. Content uses textual/multimedia features.
2. Structure uses node-link relationships.
3. Usage uses session and navigation logs.
4. Content answers what, structure answers authority/connectivity.
5. Usage answers how users actually browse.

### M5A3. Focused vs Regular Crawling
1. Regular crawler explores broad web coverage.
2. Focused crawler follows topic-relevant links only.
3. Focused crawling has higher precision.
4. Regular crawling has broader recall.
5. Focused approach reduces bandwidth/storage cost.

### M5A4. Usage Mining Activities
1. Preprocessing: log cleaning and robot filtering.
2. User identification and sessionization.
3. Path completion to repair missing references.
4. Pattern discovery via rules/clusters/sequences.
5. Pattern analysis for actionable website decisions.

### M5A5. Text Retrieval Indexing + TF-IDF
1. Inverted index maps term -> posting list (docs).
2. Signature file uses hashed bit patterns.
3. TF counts term occurrence in document.
4. IDF penalizes common terms across corpus.
5. TF-IDF gives balanced term importance for ranking.

## Module 5 - Part B (10+ points, diagram + formula)

### M5B1. Web Content Mining + Text Mining Techniques
1. Unstructured mining processes free text using NLP.
2. Structured mining extracts data from HTML tables/forms.
3. Semi-structured mining handles XML/JSON/DOM patterns.
4. Tokenization, stop-word removal, stemming are core preprocessing steps.
5. Feature extraction uses n-grams and embeddings.
6. Classification groups documents by topic.
7. Clustering discovers latent document groups.
8. Sentiment analysis extracts opinion polarity.
9. Named entity extraction identifies people/orgs/locations.
10. Topic modeling gives compact thematic summaries.

Diagram:
```text
Web Pages -> Parse -> Clean Text -> Feature Extraction -> Classification/Clustering
```

Formula:
$$
w_{t,d}=tf_{t,d}\cdot idf_t
$$

### M5B2. Text Retrieval and Relation among TM, IR, IE
1. IR focuses on retrieving relevant documents for query.
2. TM focuses on pattern/knowledge extraction from text corpus.
3. IE extracts structured facts (entities, relations, events).
4. Document selection and ranking are key IR stages.
5. Boolean model, vector space model, probabilistic ranking are methods.
6. TM often uses IR output as input corpus.
7. IE can enrich IR indexes with entity-aware retrieval.
8. Combined pipeline improves both relevance and explainability.
9. Evaluation uses precision, recall, MAP, NDCG.
10. Real systems integrate IR+IE+TM in search assistants.

Diagram:
```text
Query -> IR Retrieve -> TM Analyze Themes -> IE Extract Facts -> Ranked Insights
```

Formula:
$$
\text{Cosine}(d,q)=\frac{\sum_i w_{i,d}w_{i,q}}{\sqrt{\sum_i w_{i,d}^2}\sqrt{\sum_i w_{i,q}^2}}
$$

### M5B3. HITS and CLEVER
1. HITS computes hub and authority scores on link graph.
2. Authority: page linked by good hubs.
3. Hub: page linking to good authorities.
4. Iterative mutual reinforcement updates scores.
5. CLEVER extends link analysis with focused subgraph selection.
6. Start with root set from query results.
7. Expand to base set using in-links/out-links.
8. Apply HITS-style updates on focused graph.
9. Rank high-authority pages as primary results.
10. Useful for topic-specific structure mining.

Diagram:
```text
Root Set -> Base Set Graph -> Iterative Hub/Authority Update -> Ranked Pages
```

Formula:
$$
a(p)=\sum_{q\to p} h(q), \quad h(p)=\sum_{p\to r} a(r)
$$

### M5B4. Web Usage Mining: Applications and Patterns
1. Personalization recommends pages/products from behavior history.
2. Website redesign uses frequent navigation paths.
3. Marketing campaign optimization uses user segments.
4. Fraud/anomaly detection uses unusual click patterns.
5. Sequential pattern mining captures common click orders.
6. Association rules capture co-visited pages.
7. Clustering groups users with similar browsing profiles.
8. Classification predicts conversion/churn.
9. Traversal patterns include frequent, sequential, and cyclic paths.
10. Business KPIs improve using discovered behavior insights.

Diagram:
```text
Web Logs -> Preprocess -> Session DB -> Pattern Discovery -> Action (UX/Marketing)
```

Formula:
$$
\text{Support}(P_i\to P_j)=\frac{\#\text{sessions containing transition }P_i\to P_j}{\#\text{all sessions}}
$$

### M5B5. Numerical: TF-IDF (step tables)
Example mini matrix (same style as OCR term-document table):

| Term/Doc | D1 | D2 | D3 |
|---|---:|---:|---:|
| T1 | 2 | 1 | 0 |
| T2 | 0 | 3 | 1 |
| T3 | 1 | 0 | 2 |
| T4 | 0 | 1 | 4 |

Find TF-IDF for T4 in D3.

Step table 1: TF

| Term | Doc | Raw count |
|---|---|---:|
| T4 | D3 | 4 |

So, $TF(T4,D3)=4$ (or normalized variant if required).

Step table 2: IDF

| Quantity | Value |
|---|---:|
| Total docs N | 3 |
| docs containing T4, df(T4) | 2 (D2,D3) |
| IDF | $\log_{10}(3/2)=0.1761$ |

Step table 3: TF-IDF

| TF | IDF | TF-IDF |
|---:|---:|---:|
| 4 | 0.1761 | 0.7044 |

Final answer: $TFIDF(T4,D3)=0.7044$ (using base-10 log and raw TF).

Diagram:
```text
Term-Document Matrix -> TF + DF -> IDF -> TF*IDF Weight
```

Formula:
$$
TFIDF(t,d)=TF(t,d)\cdot \log\left(\frac{N}{df(t)}\right)
$$

---

## Final Exam Writing Notes (Applied in This File)
- Part A answers are structured as 5 direct scoring points.
- Part B answers are expanded for 10+ mark depth.
- Every Part B answer includes a diagram and at least one formula.
- Numerical answers include stepwise tables and explicit final values.
- Question wording is normalized from OCR duplicates, preserving exam intent.
