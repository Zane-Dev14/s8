# Data Mining PYQ Solved Master (Full OCR-Mapped, Exam-Oriented)

Subject: CST466 Data Mining
Updated: 23 Apr 2026

Built from:
- 2023/2024/2025 DM question papers
- Sept 2025 OCR question text
- Module 1-5 important topic OCR
- Series 1 and Series 2 OCR

Mapping files:
- DM/build/dm_unique_questions.json
- DM/build/dm_topic_map.json

---

## How To Use This File

Part A (3 marks):
1. Write exactly 5 points.
2. Keep each point one sentence.
3. Use definition first.
4. Include formula where applicable.
5. End with one application line.

Part B (14 marks):
1. Write exactly 10 points.
2. Start with definition/core concept.
3. Give ordered steps/architecture/algorithm flow.
4. Add one example/table/diagram note.
5. End with one crisp conclusion.

---

## Section 1: Module-Wise Non-Duplicate Questions

## Module 1

Part A:
1. List and explain applications/features of data warehouse.
2. Differentiate OLTP and OLAP.
3. Compare star and snowflake schema.
4. Illustrate multidimensional data model.

Part B:
1. Explain data mining functionalities.
2. Explain three-tier data warehouse architecture with neat diagram.
3. Explain star schema and snowflake schema with example.
4. Explain OLAP operations in multidimensional data model.
5. Differentiate ROLAP, MOLAP, HOLAP.
6. Explain KDD process.
7. Explain key issues in data mining.
8. Draw snowflake schema for given case and state OLAP operation sequence.

## Module 2

Part A:
1. Explain two sampling methods used in data reduction.
2. Perform smoothing by bin means or boundaries.
3. Explain significance of data discretization and strategies.
4. Compute min-max and z-score normalization.

Part B:
1. Explain preprocessing steps in detail.
2. Explain cleaning approaches for incomplete/noisy/inconsistent data.
3. Explain numerosity reduction techniques.
4. Explain need and methods of data transformation.
5. Explain normalization methods with equations.
6. Compare SRSWOR, SRSWR, stratified sampling.
7. Illustrate PCA for dimensionality reduction.
8. Explain concept hierarchy with example.

## Module 3

Part A:
1. Explain gain ratio and advantage over information gain.
2. State requirements of good clustering algorithm.
3. Compute Euclidean/Manhattan/Minkowski distances.
4. Draw confusion matrix and compute precision/recall.
5. Explain significance of SLIQ or splitting indices.

Part B:
1. Construct confusion matrix and compute precision/recall/specificity.
2. Explain DBSCAN with advantages.
3. Explain PAM algorithm with example.
4. Explain ID3 first splitting attribute selection.
5. Compute information gain for given class-labeled dataset.
6. Explain SLIQ algorithm with example.
7. Explain partition clustering variants (PAM/ROCK style asks).

## Module 4

Part A:
1. Define support, confidence, and frequent itemset.
2. List methods to improve Apriori efficiency.
3. Explain bi-directional pruning in pincer search.
4. Explain significance of association rule mining in market basket analysis.

Part B:
1. Find frequent itemsets using Apriori and generate strong rules.
2. Explain pincer search algorithm with example.
3. Find frequent itemsets using FP-Growth.
4. Explain dynamic itemset counting and dashed-to-solid move.
5. Explain partition algorithm and compare with Apriori.
6. State Apriori principle and solve candidate generation problem.

## Module 5

Part A:
1. Briefly explain web mining taxonomy.
2. Differentiate web content and web structure mining.
3. Compare web structure and web usage mining.
4. Distinguish focused and regular crawling.
5. Explain pre-processing and pattern analysis in web usage mining.

Part B:
1. Explain web usage mining applications and activities.
2. Explain focused crawling in context/personalization.
3. Explain text retrieval methods.
4. Relate text mining, information retrieval, and information extraction.
5. Explain HITS with example.
6. Explain how web structure differs from content and usage mining.
7. Write CLEVER algorithm flow for web structure mining.
8. Explain web usage data structures.
9. Explain traversal patterns and discovery methods.
10. Explain web content mining and text mining approaches.

---

## Section 2: Part A 5-Point Capsules (High Yield)

## Module 1

OLTP vs OLAP:
1. OLTP supports day-to-day transactions.
2. OLAP supports analytical decision making.
3. OLTP uses current detailed operational data.
4. OLAP uses historical aggregated data.
5. OLTP is update-heavy; OLAP is read-heavy.

## Module 2

Data discretization significance:
1. Discretization converts continuous values to intervals.
2. It simplifies model representation.
3. It improves interpretability in rules and trees.
4. It reduces noise effect by grouping nearby values.
5. It supports concept hierarchy construction.

## Module 3

Gain ratio advantage:
1. Information gain may favor high-cardinality attributes.
2. Gain ratio divides IG by split information.
3. Split information penalizes over-fragmented splits.
4. Gain ratio prefers balanced informative splits.
5. It usually improves decision-tree generalization.

## Module 4

Support, confidence, frequent itemset:
1. Support is transaction fraction containing itemset.
2. Confidence is conditional reliability of rule A -> B.
3. Frequent itemset satisfies minimum support.
4. Support controls popularity, confidence controls strength.
5. These metrics drive association rule mining.

## Module 5

Focused vs regular crawling:
1. Regular crawling aims broad web coverage.
2. Focused crawling aims topic-specific pages.
3. Regular crawler follows almost all discovered links.
4. Focused crawler filters off-topic links early.
5. Focused crawling gives higher topical precision.

---

## Section 3: Part B 10-Point Answer Blueprints

## Module 1 Blueprint: Three-tier DW architecture
1. Data warehouse supports integrated analytical decision making.
2. Architecture has bottom, middle, and top tiers.
3. Bottom tier collects source data through ETL process.
4. ETL performs extraction, cleaning, transformation, loading.
5. Warehouse repository stores integrated historical data.
6. Middle tier provides OLAP server functionality.
7. OLAP supports roll-up, drill-down, slice, dice, pivot.
8. Top tier provides query, reporting, dashboard, and mining tools.
9. Draw a 3-level block diagram with arrows bottom to top.
10. Conclude that tier separation improves scalability and manageability.

## Module 2 Blueprint: Data cleaning + transformation
1. Real-world data is incomplete, noisy, and inconsistent.
2. Missing values handled by mean/median/model/ignore strategies.
3. Noisy data handled by binning, regression, clustering-based smoothing.
4. Inconsistency handled by constraints, schema matching, unit normalization.
5. Transformation includes normalization, aggregation, discretization.
6. Min-max formula maps values to a fixed range.
7. Z-score formula standardizes by mean and standard deviation.
8. Decimal scaling shifts decimal point by power of 10.
9. Mention one short numerical substitution example.
10. Conclude preprocessing quality controls mining quality.

## Module 3 Blueprint: Confusion matrix and metrics
1. Confusion matrix evaluates classifier retrieval/performance.
2. Matrix entries are TP, FP, FN, TN.
3. Read TP directly from given statement.
4. Compute FP as retrieved minus TP.
5. Compute FN as relevant minus TP.
6. Compute TN as total minus TP, FP, FN.
7. Precision = TP/(TP+FP).
8. Recall = TP/(TP+FN).
9. Specificity = TN/(TN+FP) when asked.
10. Conclude by reporting metric values and interpretation.

## Module 3 Blueprint: DBSCAN algorithm
1. DBSCAN is density-based clustering algorithm.
2. Inputs are Eps radius and MinPts threshold.
3. Classify points as core, border, or noise.
4. Start from unvisited point and check neighborhood size.
5. If core, start cluster and expand using density reachability.
6. Add directly density-reachable points to current cluster.
7. Continue expansion recursively from new core points.
8. Mark sparse unclustered points as noise.
9. Mention strengths: arbitrary-shape clusters and outlier handling.
10. Conclude that DBSCAN avoids predefining number of clusters.

## Module 4 Blueprint: Apriori with strong rules
1. Apriori mines frequent itemsets level by level.
2. Use minimum support to filter frequent itemsets.
3. Generate C1 and count supports in database scan.
4. Keep L1 frequent sets only.
5. Join and prune to form C2 using Apriori principle.
6. Repeat until no new frequent sets.
7. Generate candidate rules from frequent itemsets.
8. Compute confidence and apply minimum confidence threshold.
9. Report final frequent itemsets and strong rules.
10. Conclude with business meaning of one strong rule.

## Module 4 Blueprint: FP-Growth
1. FP-Growth mines frequent itemsets without candidate explosion.
2. Scan once for item frequency and remove infrequent items.
3. Sort frequent items by descending support.
4. Build FP-tree from reordered transactions.
5. Maintain header table with node links.
6. Create conditional pattern base for each item.
7. Build conditional FP-tree recursively.
8. Extract frequent patterns from conditional trees.
9. Mention lower scan overhead than Apriori.
10. Conclude FP-Growth is efficient for large dense datasets.

## Module 5 Blueprint: Text retrieval + TM/IR/IE
1. Information retrieval finds relevant documents for query.
2. Text mining extracts patterns/knowledge from text corpus.
3. Information extraction pulls structured facts from text.
4. Document selection method uses Boolean exact matching.
5. Document ranking method orders by relevance score.
6. TF-IDF is common ranking weight mechanism.
7. IR typically provides candidate documents first.
8. IE structures entities/relations from candidate documents.
9. TM combines IR, IE, and analytics tasks.
10. Conclude by distinguishing find, extract, and discover roles.

## Module 5 Blueprint: HITS/CLEVER style link analysis
1. Link mining analyzes graph structure among web pages.
2. HITS uses hub and authority scores.
3. Authority page is pointed by good hubs.
4. Hub page points to good authorities.
5. Initialize scores and iterate mutually reinforcing updates.
6. Normalize scores after each iteration.
7. Continue until convergence.
8. CLEVER applies focused link-analysis for topic-sensitive ranking.
9. Mention use in web structure mining and ranking.
10. Conclude with final ranked hubs and authorities.

---

## Section 4: Rapid Formula Box

1. Min-max normalization:
x' = (x - xmin)/(xmax - xmin)

2. Z-score:
x' = (x - mu)/sigma

3. Entropy:
H(S) = -sum(pi log2 pi)

4. Information gain:
IG(S,A) = H(S) - sum((|Sv|/|S|)H(Sv))

5. Gain ratio:
GR(S,A) = IG(S,A)/SplitInfo(S,A)

6. Precision:
TP/(TP+FP)

7. Recall:
TP/(TP+FN)

8. Support:
count(itemset)/total transactions

9. Confidence:
support(A union B)/support(A)

---

## Section 5: Revision Loop

1. Revise non-duplicate question set from STEP5.
2. For each module, practice one 5-point and one 10-point answer.
3. Re-solve one numerical from Module 2 and one from Module 3 daily.
4. Rehearse Apriori and FP-Growth flow in sequence.
5. Rehearse web mining comparison tables before exam.

---

## Final End Section: All Part B Answers (Quick-Write Completion)

This end-section gives a direct 10-point writing skeleton for every major Part B family asked in DM PYQs.

## Module 1 Part B families
1. Data mining functionalities: define, classify descriptive/predictive, list key functionalities, conclude by use.
2. Three-tier architecture: bottom ETL, middle OLAP, top BI/mining, draw linear tier diagram.
3. Star vs snowflake: normalization, joins, speed, redundancy, diagram pair, conclude selection criteria.
4. OLAP + ROLAP/MOLAP/HOLAP: five OLAP operations, then three storage paradigms and use-case fit.
5. KDD process: CISTMEP flow with clean stage-wise explanation and final insight line.

## Module 2 Part B families
1. Preprocessing pipeline: cleaning, integration, selection, transformation, reduction.
2. Data cleaning: missing/noisy/inconsistent methods with examples.
3. Numerosity reduction: regression, histograms, clustering, sampling, cube aggregation.
4. Transformation and normalization: min-max, z-score, decimal scaling formulas and use.
5. Sampling and discretization: SRSWOR/SRSWR/stratified plus interval strategies.
6. PCA: standardize, covariance, eigendecompose, select k, project.

## Module 3 Part B families
1. Confusion matrix numerical: TP/FP/FN/TN then precision/recall/specificity.
2. DBSCAN: Eps, MinPts, core-border-noise, expansion steps, strengths.
3. PAM: build and swap phases, medoid objective, outlier robustness.
4. ID3 first split: entropy, weighted entropy, maximum IG selection.
5. Information gain derivation: compute per attribute and compare.
6. SLIQ: presort, class-list, split evaluation, breadth-first growth.

## Module 4 Part B families
1. Apriori frequent itemsets + strong rules: join-prune-count loop.
2. Pincer search: bidirectional pruning with MFCS/MFS logic.
3. FP-Growth: FP-tree construction and conditional mining.
4. DIC: dashed/solid structures and dynamic candidate progression.
5. Partition algorithm: local mining + global verification and Apriori comparison.
6. Apriori principle candidate-generation problems: subset-pruning-first logic.

## Module 5 Part B families
1. Web usage mining activities and applications: log-to-insight pipeline.
2. Focused crawling and personalization: relevance-driven crawl expansion.
3. Text retrieval methods: selection vs ranking with TF-IDF idea.
4. TM-IR-IE relationship: retrieval, extraction, and knowledge discovery stack.
5. HITS and CLEVER: hub-authority iterative ranking and topic-sensitive graph mining.
6. Web mining comparison: content vs structure vs usage.
7. Web usage data structures and traversal discovery methods.
8. Web content and text mining approaches in detail.

Final rule for all Part B answers:
1. Write exactly 10 numbered points.
2. Add one diagram/table wherever applicable.
3. Add formula block in numerical or metric questions.
4. End with one-line conclusion tied to application.
