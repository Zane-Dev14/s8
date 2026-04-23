# STEP 8: Module 4 Crash Guide (Association Rule Mining)

Module 4 core area:
- Frequent pattern mining
- Apriori, FP-Growth, Pincer Search, DIC, Partition Algorithm

OCR-mapped sources:
- DM/ocr_output/CST466_DATA_MINING,_JUNE_2023.txt
- DM/ocr_output/CST466_DATA_MINING,_MAY_2024.txt
- DM/ocr_output/CST466_DATA_MINING,_APRIL_2025.txt
- DM/ocr_output/Data-Mining-Module-4-Important-Topics-PYQs.txt
- DM/ocr_output/Data-Mining-Series-2-Important-Topics.txt

---

## Questions Asked (Put This At Top In Revision)

Part A repeats:
1. Define support, confidence, and frequent itemset.
2. List methods to improve Apriori efficiency.
3. Explain bi-directional pruning in pincer search.
4. Explain significance of market basket analysis.

Part B repeats:
1. Apriori itemset + strong rule generation problem.
2. Pincer search algorithm with example.
3. FP-growth frequent itemset mining problem.
4. Dynamic Itemset Counting with dashed vs solid.
5. Partition algorithm and comparison with Apriori.
6. Apriori principle in candidate generation with minimum support.

---

## Part A: 5-Point Answer Capsules

## Q1) Support, confidence, frequent itemset
1. Support of an itemset is the fraction of transactions containing that itemset.
2. Confidence of A -> B is support(A union B) divided by support(A).
3. A frequent itemset is an itemset whose support is at least minimum support.
4. Support filters popularity while confidence filters rule reliability.
5. These three are the base metrics for association rule mining.

## Q2) Three methods to improve Apriori efficiency
1. Hash-based pruning removes low-potential candidate buckets early.
2. Transaction reduction drops transactions that cannot support larger itemsets.
3. Partitioning mines local frequent sets before final global verification.
4. Sampling can mine approximate frequent sets quickly on large data.
5. Dynamic itemset counting reduces repeated full database scans.

## Q3) Bi-directional pruning in pincer search
1. Pincer search performs bottom-up and top-down search simultaneously.
2. Bottom-up search grows frequent itemsets like Apriori.
3. Top-down search tracks maximal frequent itemset candidates.
4. Infrequent supersets and impossible subsets are pruned early from both ends.
5. This reduces candidate explosion compared to plain Apriori.

## Q4) Significance of market basket analysis
1. It discovers products commonly purchased together.
2. It helps cross-sell and bundle design in retail.
3. It improves shelf arrangement and recommendation systems.
4. It supports targeted promotions based on customer behavior.
5. It converts transaction logs into actionable business rules.

---

## Part B: 10-Point Exam Blueprints

## Q1) Apriori frequent itemsets and strong rules
1. Apriori finds frequent itemsets level-wise using candidate generation.
2. Apriori principle: every subset of a frequent itemset must be frequent.
3. Start with candidate 1-itemsets C1 and count support in one scan.
4. Keep only frequent 1-itemsets L1 using minimum support threshold.
5. Join L1 with itself to form C2, then prune by Apriori subset rule.
6. Count supports for C2 and keep frequent sets L2.
7. Repeat join-prune-count for C3, C4 until no frequent set remains.
8. Generate rules X -> Y from each frequent itemset where X union Y is that itemset.
9. Compute confidence and keep rules meeting minimum confidence threshold.
10. Conclude with final frequent itemsets and strong rules table.

## Q2) FP-Growth algorithm with advantages
1. FP-Growth mines frequent itemsets without candidate generation.
2. First scan computes item frequencies and removes infrequent items.
3. Sort frequent items in descending support order.
4. Build FP-tree by inserting reordered transactions through shared prefix paths.
5. Build header table with node links for each item.
6. Mine conditional pattern base for each item from bottom of header.
7. Build conditional FP-tree and recursively extract frequent patterns.
8. Repeat until tree is empty or single-path case is exhausted.
9. Advantage: fewer scans and compact tree-based representation.
10. Advantage: better performance than Apriori on dense/large datasets.

## Q3) Dynamic Itemset Counting (DIC)
1. DIC introduces candidates dynamically during database scan intervals.
2. It classifies itemsets as dashed-circle, dashed-square, solid-circle, solid-square.
3. Dashed structures are currently being counted; solid are finalized.
4. As support evidence grows, dashed candidates are promoted appropriately.
5. If a candidate crosses support while still scanning, supersets can be introduced early.
6. This overlaps counting and candidate generation.
7. Move dashed to solid when full pass/count condition is satisfied.
8. Prune candidates that cannot reach minimum support.
9. DIC reduces number of complete passes over transaction database.
10. Conclude by outputting all solid frequent itemsets.

## Q4) Partition algorithm and Apriori comparison
1. Partition algorithm divides the full database into disjoint partitions.
2. Each partition is mined locally for frequent itemsets.
3. Any globally frequent itemset must appear frequent in at least one partition.
4. Union of local frequent sets forms global candidate set.
5. One additional full scan verifies true global frequent itemsets.
6. Hence it usually needs only two scans of the full database.
7. Apriori needs multiple scans, one per itemset size level.
8. Partition method is generally scan-efficient on large datasets.
9. Candidate count and memory needs are often lower than Apriori.
10. Conclude using: partition = fewer scans, Apriori = simpler baseline logic.

## Q5) Pincer search algorithm flow
1. Pincer search combines bottom-up and top-down discovery.
2. Maintain MFCS (maximal frequent candidate set) from top side.
3. Maintain MFS (maximal frequent set) for confirmed maximal patterns.
4. Run Apriori-like candidate generation from lower levels.
5. Update MFCS using infrequent patterns to prune impossible supersets.
6. Update MFS when frequent maximal sets are found.
7. Use MFCS to prune bottom-up candidate generation aggressively.
8. Continue until no candidates remain or maximal sets stabilize.
9. Output all frequent itemsets or maximal frequent itemsets.
10. Conclude: best when long patterns exist and Apriori is too costly.

---

## Formula Block (Write Exactly)

1. Support:
support(A) = count(A)/N

2. Confidence:
confidence(A -> B) = support(A union B)/support(A)

3. Lift (bonus line if needed):
lift(A -> B) = confidence(A -> B)/support(B)

---

## Quick Comparison Table

| Algorithm | Candidate Generation | DB Scans | Strength |
|---|---|---|---|
| Apriori | Yes | Many | Simple and explainable |
| FP-Growth | No | Few | Fast on large/dense data |
| Pincer | Hybrid | Moderate | Good for maximal frequent sets |
| DIC | Dynamic | Fewer than Apriori | Early candidate introduction |
| Partition | Local then global | Usually 2 full scans | Scan efficient |

---

## Module 4 Memory Acronyms

1. APFDP chain:
- Apriori, Pincer, FP-Growth, DIC, Partition.

2. Rule triad:
- SCF = Support, Confidence, Frequent-itemset.

3. Apriori loop:
- JPC = Join, Prune, Count.

---

## Last-Minute Drill

1. Solve one Apriori numerical with confidence filtering.
2. Solve one FP-growth numerical with conditional pattern base.
3. Write DIC dashed/solid movement condition in 5 points.
4. Write partition vs Apriori comparison in 10 points.
