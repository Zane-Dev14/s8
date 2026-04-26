# STEP 8: Module 4 Master Teaching Guide (Association Rule Mining)

This is a teaching-first guide, not just a PYQ list.
Goal: understand deeply, remember fast, and write full-mark answers in exam.

---

## 0) The Hook: Why This Module Exists

Imagine you run a supermarket.
Every day, thousands of bills are generated.
You want answers to these business questions:
1. Which products are frequently bought together?
2. If customer buys A, what is likely to be bought next?
3. How can we do this fast on huge data?

Module 4 is exactly this:
- Find frequent patterns
- Convert them to useful rules
- Do it efficiently at scale

Memory hook sentence:
- Module 4 = "Find patterns, form rules, do it fast."

---

## 1) What They Ask in Exam (Complete Map)

## Part A asks
1. Define support, confidence, and frequent itemset.
2. List methods to improve Apriori efficiency.
3. Explain bi-directional pruning in pincer search.
4. Explain significance of market basket analysis.

## Part B asks
1. Apriori frequent itemset mining + strong association rules.
2. Pincer search algorithm with example.
3. FP-Growth frequent itemset mining with example.
4. Dynamic Itemset Counting (DIC) with dashed/solid condition.
5. Partition algorithm for large itemsets.
6. Partition algorithm vs Apriori comparison.
7. Apriori principle and candidate generation problem.

---

## 2) Core Concepts from Zero

## 2.1 Transaction and Itemset
1. Transaction: one bill/record.
2. Itemset: set of items in a transaction.
3. k-itemset: itemset containing k items.

Example:
- T1 = {Milk, Bread, Butter}
- {Milk, Bread} is a 2-itemset.

## 2.2 Support
$$
Support(A)=\frac{count(A)}{N}
$$
- count(A) = transactions containing A
- N = total transactions

## 2.3 Confidence
$$
Confidence(A\rightarrow B)=\frac{Support(A\cup B)}{Support(A)}
$$
Interpretation:
- Among people who bought A, how many also bought B?

## 2.4 Lift (bonus metric)
$$
Lift(A\rightarrow B)=\frac{Confidence(A\rightarrow B)}{Support(B)}
$$
Interpretation:
- Lift > 1 means positive association.

## 2.5 Frequent Itemset and Strong Rule
1. Frequent itemset: support >= minsup.
2. Strong rule: support >= minsup and confidence >= minconf.

---

## 3) Big Algorithms with Intuition + Acronym

## 3.1 Apriori (bottom-up level-wise)
Acronym: JPC
- Join -> Prune -> Count

Mental model:
- Build from 1-itemsets to 2-itemsets to 3-itemsets...

Apriori principle (must memorize exact line):
- Every non-empty subset of a frequent itemset must also be frequent.

Why powerful:
- Removes impossible candidates before counting.

## 3.2 FP-Growth (tree-based mining)
Acronym: CSTM
- Count -> Sort -> Tree -> Mine

Mental model:
- Compress transactions into FP-tree and mine without huge candidate generation.

Why faster:
- Usually fewer scans and smaller search space than Apriori.

## 3.3 Pincer Search (two-direction search)
Acronym: BTM
- Bottom-up + Top-down + Meet

Mental model:
- Search from both ends to prune faster.

## 3.4 DIC (Dynamic Itemset Counting)
Acronym: DPSC
- Dynamic -> Promote -> Solidify -> Count

Mental model:
- Do not wait for full level completion; introduce new candidates during scanning.

## 3.5 Partition Algorithm
Acronym: LUGV
- Local mining -> Union -> Global verify

Mental model:
- Split DB, mine locally, combine, verify once globally.

---

## 4) Draw These Diagrams in Exam

## 4.1 Apriori flow diagram
```text
C1 -> L1 -> C2 -> L2 -> C3 -> L3 -> Rules
      Join/Prune at each level
```

## 4.2 FP-tree sketch
```text
NULL
 |- Bread:4
 |   |- Milk:3
 |       |- Butter:2
 |   |- Butter:1
```

## 4.3 Pincer bidirectional idea
```text
Bottom-up: 1-item -> 2-item -> 3-item
Top-down : Max-set -> subsets
Meeting zone -> faster pruning
```

## 4.4 Partition flow
```text
Database -> P1, P2, P3
P1 local F, P2 local F, P3 local F
Union candidates -> One global scan -> Final frequent sets
```

---

## 5) Full Worked Example (Apriori + Rules)

Given transactions:
- T1: {A, B, C}
- T2: {A, C}
- T3: {A, B}
- T4: {B, C}
- T5: {A, B, C}
- T6: {A, B, D}

Let:
- minsup = 33.33% (support count >= 2)
- minconf = 60%
- N = 6

## Step 1: C1 and L1
Counts:
- A:5, B:5, C:4, D:1
L1 (count >= 2):
- {A}, {B}, {C}

## Step 2: C2 from L1
Candidates:
- {A,B}, {A,C}, {B,C}
Counts:
- AB:4 (T1,T3,T5,T6)
- AC:3 (T1,T2,T5)
- BC:3 (T1,T4,T5)
L2:
- {AB}, {AC}, {BC}

## Step 3: C3 from L2
Candidate:
- {ABC}
Check subsets AB, AC, BC all frequent -> keep candidate.
Count:
- ABC:2 (T1,T5)
L3:
- {ABC}

No higher candidate possible.
Final frequent itemsets:
- A, B, C, AB, AC, BC, ABC

## Step 4: Generate strong rules (minconf 60%)
From AB:
- A -> B = support(AB)/support(A) = 4/5 = 80% strong
- B -> A = 4/5 = 80% strong

From AC:
- A -> C = 3/5 = 60% strong
- C -> A = 3/4 = 75% strong

From BC:
- B -> C = 3/5 = 60% strong
- C -> B = 3/4 = 75% strong

From ABC:
- AB -> C = 2/4 = 50% not strong
- AC -> B = 2/3 = 66.7% strong
- BC -> A = 2/3 = 66.7% strong

---

## 6) FP-Growth Worked Style (How to Present)

1. Scan DB and count frequencies.
2. Remove infrequent items.
3. Sort items in each transaction by global frequency.
4. Build FP-tree with shared paths.
5. Build header table.
6. For each item, build conditional pattern base.
7. Build conditional FP-tree.
8. Extract conditional frequent patterns.
9. Combine to final frequent itemsets.
10. Mention advantage over Apriori (candidate explosion avoided).

Exam tip:
- If numbers are large, at least show one conditional base clearly.

---

## 7) DIC Dashed vs Solid (Clear and Scorable)

You can write this exact meaning block:
1. Dashed = counting still in progress.
2. Solid = counting status finalized.
3. Dashed-frequent can become solid-frequent after completion condition.
4. Dashed-infrequent can become solid-infrequent after completion condition.
5. New larger candidates can be introduced dynamically while scanning.

One-line scoring sentence:
- DIC overlaps candidate generation and counting to reduce repeated full scans.

---

## 8) Partition vs Apriori (High-Score Table)

| Aspect | Apriori | Partition |
|---|---|---|
| Full scans | Many (level-wise) | Usually 2 |
| Candidate explosion | High on dense data | Lower after local filtering |
| Scalability | Moderate | Better for very large DB |
| Parallelism | Limited | Natural (partition-wise) |
| Simplicity | Very easy | Slightly more involved |

Conclusion line:
- Partition is scan-efficient; Apriori is conceptually simplest baseline.

---

## 9) Part A Topper Scripts (Exactly 5 points)

## Q1) Support, confidence, frequent itemset
1. Support is fraction of transactions containing an itemset.
2. Confidence is conditional strength of rule A -> B.
3. Frequent itemset has support at least minsup.
4. Support captures popularity; confidence captures reliability.
5. These metrics are core to association rule mining.

## Q2) Apriori efficiency improvements
1. Hash-based pruning removes weak candidate buckets.
2. Transaction reduction removes irrelevant transactions.
3. Partitioning mines local frequent sets first.
4. Sampling gives fast approximate candidates.
5. DIC introduces candidates dynamically during scan.

## Q3) Bi-directional pruning in pincer
1. Pincer combines bottom-up and top-down search.
2. Bottom-up finds frequent sets level-wise.
3. Top-down tracks maximal candidate sets.
4. Information from both sides prunes earlier.
5. It reduces candidate explosion compared to plain Apriori.

## Q4) Market basket significance
1. Finds items bought together frequently.
2. Enables cross-sell and bundle offers.
3. Improves shelf arrangement strategy.
4. Drives recommender systems.
5. Converts transaction data into actionable business insight.

---

## 10) Part B Topper Scripts (Exactly 10 points each)

## B1) Apriori + strong rules
1. State minsup and minconf.
2. Generate C1 and count supports.
3. Keep L1 frequent sets.
4. Generate C2 by joining L1.
5. Prune C2 using Apriori principle.
6. Count and keep L2.
7. Generate higher levels until stop.
8. Generate rules from frequent itemsets.
9. Compute confidence and filter strong rules.
10. Present final frequent sets and strong rules in table.

## B2) Pincer search with example
1. Define pincer as bidirectional frequent pattern mining.
2. Maintain MFCS and MFS sets.
3. Run bottom-up candidate generation.
4. Count supports each level.
5. Use infrequent sets to prune MFCS.
6. Use frequent maximal sets to update MFS.
7. Prune bottom-up candidates using top-down info.
8. Continue until no candidates remain.
9. Output frequent/maximal frequent itemsets.
10. Conclude faster pruning than Apriori in long-pattern data.

## B3) FP-Growth frequent itemsets
1. Count item frequencies.
2. Remove infrequent items by minsup.
3. Sort items by descending frequency.
4. Build FP-tree from sorted transactions.
5. Build header links.
6. Extract conditional pattern base item-wise.
7. Build conditional FP-tree.
8. Mine frequent patterns recursively.
9. Aggregate all mined frequent itemsets.
10. Conclude no heavy candidate generation required.

## B4) DIC with dashed/solid move
1. Define dynamic counting during scans.
2. Start with low-level candidates.
3. Track dashed/solid status.
4. Promote dashed candidates based on support progress.
5. Move to solid when completion condition satisfied.
6. Prune impossible candidates.
7. Introduce larger candidates during scan.
8. Continue until stable frequent set output.
9. Mention reduced scan overhead.
10. Output final solid-frequent itemsets.

## B5) Partition algorithm
1. Partition full DB into disjoint blocks.
2. Mine local frequent sets per block.
3. Union local frequent sets into global candidates.
4. Run one global verification scan.
5. Keep globally frequent sets only.
6. State theoretical guarantee clearly.
7. Mention lower full-scan cost.
8. Mention better scalability and parallelism.
9. Compare briefly with Apriori.
10. Conclude with final frequent itemset output.

## B6) Apriori principle and candidate generation
1. State Apriori principle exactly.
2. Generate C1 and L1.
3. Join L(k-1) to create Ck.
4. Prune candidate whose any subset is infrequent.
5. Count supports on surviving candidates.
6. Keep frequent itemsets Lk.
7. Repeat until Lk is empty.
8. If asked, generate rules from frequent sets.
9. Use confidence threshold for strong rules.
10. Present L1, L2, L3 in clean table.

---

## 11) Common Mistakes (Avoid These)

1. Writing formulas without defining minsup/minconf.
2. Forgetting subset-pruning in Apriori.
3. Mixing support count and support percentage.
4. Generating rules from non-frequent itemsets.
5. Not giving final boxed list of frequent sets and strong rules.

---

## 12) Active Recall Drill (Self-Test)

1. Can you state Apriori principle exactly in one line?
2. Can you solve one C1-L1-C2-L2 table without notes?
3. Can you explain why FP-Growth avoids candidate explosion?
4. Can you distinguish dashed vs solid in DIC clearly?
5. Can you write partition guarantee statement exactly?

If all 5 are yes, Module 4 is exam-ready.

---

## 13) 30-Second Revision Strip

1. Formulas: support, confidence, lift.
2. Acronyms: JPC, CSTM, BTM, DPSC, LUGV.
3. One flow: Apriori and FP-Growth.
4. One compare: Apriori vs Partition.
5. One line each: pincer, DIC, market basket value.
