# STEP 1: Data Mining Priority Topics (Full OCR-Mapped Plan)

Subject: Data Mining (CST466)
Date mapped: 23 Apr 2026

OCR sources covered:
- DM/ocr_output/CST466_DATA_MINING,_JUNE_2023.txt
- DM/ocr_output/CST466_DATA_MINING,_MAY_2024.txt
- DM/ocr_output/CST466_DATA_MINING,_APRIL_2025.txt
- DM/ocr_output/Data-Mining-September2025.txt
- DM/ocr_output/Data-Mining-Module-1-Important-Topics-PYQs.txt
- DM/ocr_output/Data-Mining-Module-2-Important-Topics-PYQs.txt
- DM/ocr_output/mod3.txt
- DM/ocr_output/Data-Mining-Module-4-Important-Topics-PYQs.txt
- DM/ocr_output/Data-Mining-Module-5-Important-Topics-PYQs.txt
- DM/ocr_output/series1.txt
- DM/ocr_output/Data-Mining-Series-2-Important-Topics.txt

Generated map artifacts:
- DM/build/dm_unique_questions.json
- DM/build/dm_topic_map.json
- DM/build/DM_OCR_Unique_Question_Map.md

---

## Exam Writing Contract (Use Everywhere)

Part A target (3 marks):
- Write exactly 5 points.
- Point 1 must be a definition line.
- Point 2 should be formula/criterion (if any).
- Points 3 and 4 should be concept or method details.
- Point 5 should be one mini example/use-case/conclusion.

Part B target (14 marks):
- Write exactly 10 points.
- Point 1: direct intro/definition.
- Point 2: architecture/formula/core idea.
- Points 3 to 8: ordered method/algorithm/explanation.
- Point 9: example, diagram note, or comparison table.
- Point 10: final conclusion line.

Fast mnemonic:
- Part A: DFCEX = Definition, Formula, Concept, Concept, Example.
- Part B: DAFSTEPXFC = Definition, Architecture, Flow, Steps, Example, Table, Final, Conclusion.

---

## Module-Wise Priority Map (From OCR Frequency)

## Module 1 (DW + OLAP + KDD)

Top repeated asks:
1. Data warehouse features and applications.
2. OLTP vs OLAP.
3. Star schema vs snowflake schema.
4. Three-tier architecture.
5. OLAP operations and ROLAP/MOLAP/HOLAP.
6. KDD process.
7. Data mining functionalities.

Topic-frequency hint (from map):
- data warehouse: very high
- olap/oltp: very high
- schema questions: high

## Module 2 (Preprocessing + Reduction)

Top repeated asks:
1. Data cleaning for missing/noisy/inconsistent data.
2. Binning and smoothing numericals.
3. Min-max and z-score normalization numericals.
4. Sampling methods (SRSWOR/SRSWR/stratified).
5. Numerosity reduction techniques.
6. Discretization and concept hierarchy.
7. PCA and dimensionality reduction.

Topic-frequency hint:
- normalization: very high
- discretization/sampling/numerosity: high

## Module 3 (Classification + Clustering)

Top repeated asks:
1. Gain ratio and advantage over information gain.
2. Confusion matrix with precision/recall.
3. Distance metrics (Euclidean/Manhattan/Minkowski).
4. DBSCAN concept and advantages.
5. PAM algorithm.
6. ID3 splitting attribute.
7. SLIQ algorithm.

Topic-frequency hint:
- clustering + SLIQ + decision tree: very high

## Module 4 (Association Mining)

Top repeated asks:
1. Apriori efficiency improvements.
2. Support, confidence, frequent itemset.
3. Pincer search and bi-directional pruning.
4. Apriori frequent-itemset problems with support/confidence.
5. FP-Growth and advantages.
6. Dynamic itemset counting (dashed vs solid).
7. Partition algorithm and Apriori comparison.

Topic-frequency hint:
- apriori: dominant
- fp-growth/pincer/dic: high

## Module 5 (Web + Text Mining)

Top repeated asks:
1. Web usage mining activities and applications.
2. Web content vs structure vs usage mining.
3. Focused crawler vs regular crawler.
4. Text retrieval methods.
5. Relationship: text mining vs IR vs IE.
6. HITS/CLEVER algorithms.
7. Traversal patterns and discovery methods.
8. Web usage data structures.

Topic-frequency hint:
- web usage/structure/content: dominant
- text retrieval and crawler questions: high

---

## Priority Buckets (What To Finish First)

Critical (do first):
1. M1: OLTP-OLAP, schemas, OLAP ops, three-tier architecture.
2. M2: cleaning + normalization + binning + sampling.
3. M3: gain ratio + confusion matrix + DBSCAN + SLIQ.
4. M4: Apriori + FP-growth + DIC + partition.
5. M5: web mining types + text retrieval + crawler comparison.

High:
1. M1 KDD and functionalities.
2. M2 PCA and discretization strategy variants.
3. M3 ID3 and PAM worked style.
4. M5 HITS and CLEVER algorithm flow.

Medium:
1. Extra comparisons and alternate examples.
2. Extended derivation details beyond exam depth.

---

## One-Line Memory Acronyms

1. KDD flow: CISTMEP
- Cleaning, Integration, Selection, Transformation, Mining, Evaluation, Presentation.

2. OLAP ops: RDSDP
- Roll-up, Drill-down, Slice, Dice, Pivot.

3. Clustering set: KPD-S
- K-means, PAM, DBSCAN, SLIQ.

4. Association set: APFDP
- Apriori, Pincer, FP-Growth, DIC, Partition.

5. Web mining triad: C-S-U
- Content, Structure, Usage.

---

## 48-Hour Score Plan

Day 1:
1. Finish all critical Module 1 and Module 2 theory + numericals.
2. Solve at least one normalization and one confusion matrix question from memory.
3. Write one full 10-point answer each for KDD, cleaning, and three-tier architecture.

Day 2:
1. Finish Module 3, 4, 5 algorithm answers in 10-point format.
2. Practice one Apriori, one FP-growth, one crawler comparison answer.
3. Revise only the non-duplicate PYQ set in STEP5.

---

## Safety Check Before Exam

1. Can you write 5 points for every Part A short-note topic?
2. Can you write 10 points for each core long-answer topic in each module?
3. Can you solve normalization and confusion matrix without reference?
4. Can you write Apriori and FP-growth steps in order?
5. Can you compare web mining types and focused-vs-regular crawling in table form?

If yes to all, exam coverage is strong.
