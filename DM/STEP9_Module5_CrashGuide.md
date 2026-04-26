# STEP 9: Module 5 Master Teaching Guide (Web and Text Mining)

This is a teaching-first guide, not a plain PYQ summary.
Goal: understand concepts, remember quickly, and write full-mark answers.

---

## 0) The Hook: Why This Module Exists

Imagine you run a search engine + e-commerce app.
You must answer:
1. What is on the web? (content)
2. How pages are connected? (structure)
3. How users actually behave? (usage)

Module 5 is this practical stack.
Memory hook:
- Module 5 = "Content, Connections, Clicks".

---

## 1) What They Ask in Exam (Complete Map)

## Part A asks
1. Web mining taxonomy.
2. Web content vs web structure mining.
3. Web structure vs web usage mining.
4. Focused crawling vs regular crawling.
5. Pre-processing and pattern analysis in web usage mining.

## Part B asks
1. Web usage mining activities and applications.
2. Focused crawler with personalization context.
3. Text retrieval methods.
4. Relationship among text mining, IR, IE.
5. HITS algorithm with example.
6. CLEVER algorithm for web structure mining.
7. Web usage data structures.
8. Traversal patterns and discovery methods.
9. Web content mining techniques.
10. Text mining approaches in detail.

---

## 2) Core Concepts from Zero

## 2.1 Web mining taxonomy
Acronym: CSU
- Content mining
- Structure mining
- Usage mining

1. Content mining = what is written in web pages.
2. Structure mining = how pages link to each other.
3. Usage mining = how users navigate and click.

## 2.2 Text retrieval basics
Two models:
1. Document selection (Boolean exact matching).
2. Document ranking (relevance score ranking).

## 2.3 TM, IR, IE relation
Acronym: R-E-K
- IR retrieves documents.
- IE extracts structured facts.
- TM discovers higher-level knowledge/patterns.

---

## 3) Must-Know Formulas and Metrics

## 3.1 TF-IDF
$$
TF(t,d)=\frac{f(t,d)}{|d|}
$$
$$
IDF(t)=\log\frac{N}{df(t)}
$$
$$
TF\text{-}IDF(t,d)=TF(t,d)\times IDF(t)
$$

Where:
- f(t,d): term frequency in document d
- |d|: total terms in d
- df(t): number of docs containing term t
- N: total docs

## 3.2 Precision and Recall (for retrieval quality)
$$
Precision=\frac{TP}{TP+FP}
$$
$$
Recall=\frac{TP}{TP+FN}
$$

---

## 4) Algorithms with Intuition + Acronym

## 4.1 Focused crawler vs regular crawler
Acronym: SCAN
- Seed -> Classify link -> Accept/Reject -> Next

Regular crawler:
- Broad web coverage; follows many links.

Focused crawler:
- Topic-specific; only high-relevance links expanded.

## 4.2 HITS algorithm
Acronym: HARN
- Hub-authority update -> Alternate update -> Normalize -> Repeat

Core equations:
$$
a(p)=\sum_{q\rightarrow p} h(q)
$$
$$
h(p)=\sum_{p\rightarrow r} a(r)
$$

Interpretation:
- Good hubs point to good authorities.
- Good authorities are pointed by good hubs.

## 4.3 CLEVER algorithm
Mental model:
- Topic-sensitive link analysis that extends hub-authority style ranking on focused subgraphs.

Use in answer:
- Seed pages -> focused graph -> iterative ranking -> authoritative topic pages.

---

## 5) Draw These Diagrams in Exam

## 5.1 Web mining taxonomy
```text
Web Mining
 |- Content Mining
 |- Structure Mining
 |- Usage Mining
```

## 5.2 Web usage mining pipeline
```text
Raw Logs -> Cleaning -> User/Session Identification -> Pattern Discovery -> Pattern Analysis -> Action
```

## 5.3 Focused crawler flow
```text
Seed URLs -> Fetch Page -> Score Relevance -> Keep/Discard Links -> Crawl Next
```

## 5.4 HITS mini graph
```text
Hub H1 -> A1, A2
Hub H2 -> A2
Authorities: A1, A2
```

---

## 6) Concept Teaching (Deep but Simple)

## 6.1 Web usage mining activities
1. Data collection from server/app/proxy logs.
2. Data cleaning: remove bots/noise.
3. User identification and sessionization.
4. Path completion for missing navigation steps.
5. Pattern discovery: association, clustering, sequential patterns.
6. Pattern analysis for actionable business insights.

Applications:
1. Recommendation.
2. Personalization.
3. Website redesign.
4. Targeted marketing.

## 6.2 Web content vs structure vs usage
1. Content: text/media/records inside page.
2. Structure: hyperlink graph between pages.
3. Usage: behavior from clickstream/log sequences.

## 6.3 Traversal pattern types
1. Sequential patterns (order of pages).
2. Frequent patterns (commonly co-visited pages).
3. Cyclic patterns (periodic revisit behavior).
4. Path traversal patterns (common navigation routes).

## 6.4 Web usage data structures
1. Trie for path prefixes.
2. Compressed trie/suffix tree for efficient sequence search.
3. Session graph for transitions.

## 6.5 Text mining approaches
1. Preprocessing: tokenization, stopword removal, stemming.
2. Representation: TF-IDF vectors.
3. Retrieval/ranking.
4. Classification and clustering.
5. Information extraction.
6. Topic modeling and summarization.

---

## 7) Worked Mini Example (TF-IDF)

Suppose:
- N = 100 documents
- Term t appears in df(t)=5 docs
- In document d, term appears f(t,d)=6 times
- Document length |d| = 120 terms

Step 1: TF
$$
TF=\frac{6}{120}=0.05
$$

Step 2: IDF (log base 10 acceptable unless specified)
$$
IDF=\log\frac{100}{5}=\log(20)\approx 1.301
$$

Step 3: TF-IDF
$$
TF\text{-}IDF=0.05\times 1.301=0.06505
$$

Interpretation:
- Term is relatively important in this document.

---

## 8) Part A Topper Scripts (Exactly 5 points)

## Q1) Web mining taxonomy
1. Web mining extracts useful knowledge from web data.
2. Web content mining analyzes text/media/page data.
3. Web structure mining analyzes hyperlink relationships.
4. Web usage mining analyzes user click and session behavior.
5. Together they support search, recommendation, and personalization.

## Q2) Web content vs web structure mining
1. Content mining focuses on page internals.
2. Structure mining focuses on link graph topology.
3. Content methods use NLP/extraction techniques.
4. Structure methods use graph/link-ranking techniques.
5. Content answers what is on page; structure answers how pages connect.

## Q3) Focused vs regular crawling
1. Regular crawler aims broad web coverage.
2. Focused crawler targets a specific topic domain.
3. Regular crawling follows many discovered links.
4. Focused crawling filters links by relevance score.
5. Focused crawling yields higher topical precision.

## Q4) Pre-processing and pattern analysis in usage mining
1. Pre-processing cleans logs and removes noise.
2. User and session identification organize behavior data.
3. Path completion restores missing transitions.
4. Pattern discovery extracts useful behavior patterns.
5. Pattern analysis filters and converts patterns into decisions.

---

## 9) Part B Topper Scripts (Exactly 10 points each)

## B1) Web usage mining applications and activities
1. Define web usage mining from user interaction logs.
2. Collect logs from web, app, and proxy sources.
3. Clean bots, errors, and irrelevant accesses.
4. Identify users and sessions.
5. Complete navigation paths if missing.
6. Discover patterns using association/sequential/clustering.
7. Analyze patterns for relevance and value.
8. Apply to personalization and recommendation.
9. Apply to redesign and marketing optimization.
10. Conclude with measurable business impact.

## B2) Focused crawler and personalization
1. Define focused crawler as topic-aware crawler.
2. Start with seed URLs relevant to topic.
3. Fetch page and extract outgoing links.
4. Score links by topical relevance.
5. Keep only links above threshold.
6. Repeat crawl on selected links.
7. Build high-quality topical index.
8. Combine user behavior to personalize results.
9. Compare with regular crawler coverage strategy.
10. Conclude improved precision and resource efficiency.

## B3) Text retrieval methods
1. Define text retrieval as relevant document search.
2. Method 1: document selection (Boolean).
3. Method 2: document ranking (score-based).
4. Selection gives strict exact-match retrieval.
5. Ranking gives relevance-ordered outputs.
6. Build index structures for fast lookup.
7. Use TF-IDF or probabilistic scoring.
8. Return top-k ranked documents.
9. Evaluate with precision and recall.
10. Conclude method choice by query intent and use-case.

## B4) Relationship among TM, IR, IE
1. IR retrieves relevant document set.
2. IE extracts entities/relations/facts from text.
3. TM discovers broader patterns and knowledge.
4. IR is retrieval layer.
5. IE is structuring layer.
6. TM is insight layer.
7. Pipeline commonly starts with IR.
8. IE output improves mining quality.
9. TM outputs support decision analytics.
10. Conclude they are complementary pipeline stages.

## B5) HITS algorithm with example
1. Define hubs and authorities.
2. Build root set using query retrieval.
3. Expand to base set via neighbors.
4. Initialize all hub and authority scores.
5. Update authority by incoming hub scores.
6. Update hub by outgoing authority scores.
7. Normalize scores each iteration.
8. Repeat until convergence.
9. Rank pages by final scores.
10. Conclude top authority and top hub pages.

## B6) CLEVER algorithm for structure mining
1. Define CLEVER as topic-sensitive link analysis.
2. Choose seed pages for topic query.
3. Build focused web subgraph.
4. Compute authority/hub style scores iteratively.
5. Filter noisy and off-topic links.
6. Reinforce high-quality hubs and authorities.
7. Continue update until stable scores.
8. Extract top authoritative pages.
9. Use ranking for query-focused retrieval.
10. Conclude improved topic-centric structure mining.

## B7) Web structure vs usage vs content mining
1. Content mining analyzes page content itself.
2. Structure mining analyzes links between pages.
3. Usage mining analyzes user navigation behavior.
4. Content uses NLP/extraction techniques.
5. Structure uses graph and ranking methods.
6. Usage uses sequence and clustering methods.
7. Content identifies topics and facts.
8. Structure identifies authority and communities.
9. Usage identifies behavior and intent patterns.
10. Conclude combined use gives complete web intelligence.

## B8) Web usage data structures and traversal methods
1. Trie stores user path prefixes efficiently.
2. Compressed trie/suffix tree improves sequence lookup.
3. Session graph models page-to-page transitions.
4. Sequential patterns find common ordered flows.
5. Frequent patterns find repeatedly co-visited pages.
6. Cyclic patterns find periodic revisits.
7. Path traversal patterns identify bottlenecks.
8. Use association for co-occurrence insight.
9. Use clustering/classification for user segments.
10. Conclude structures plus patterns enable personalization.

## B9) Web content mining techniques
1. Define web content mining on textual/media content.
2. Unstructured text mining uses NLP and IR.
3. Structured mining extracts table/record fields.
4. Semi-structured mining parses HTML/XML tags.
5. Classification labels pages by category.
6. Clustering groups similar pages.
7. IE extracts entities and relations.
8. Summarization reduces long content.
9. Sentiment mining captures user opinion.
10. Conclude with search/recommendation applications.

## B10) Text mining approaches in detail
1. Perform text preprocessing pipeline.
2. Build term/feature vectors.
3. Apply retrieval and ranking models.
4. Apply classification for supervised labeling.
5. Apply clustering for unsupervised grouping.
6. Apply topic modeling for latent themes.
7. Apply IE for structured knowledge extraction.
8. Evaluate using precision, recall, F-score.
9. Deploy on dashboards and decision systems.
10. Conclude with practical domain impact.

---

## 10) High-Retention Memory Hooks and Acronyms

1. CSU: Content, Structure, Usage.
2. R-E-K: Retrieve, Extract, Know.
3. SCAN crawler flow: Seed, Classify, Accept, Next.
4. HARN for HITS: Hub-authority, Alternate update, Normalize, Repeat.
5. PADS for usage pipeline: Preprocess, Analyze sessions, Discover, Summarize action.

---

## 11) Common Mistakes (Avoid These)

1. Mixing content mining and usage mining definitions.
2. Forgetting to mention user/session identification in usage mining.
3. Writing HITS without iterative update and normalization.
4. Writing TM/IR/IE as synonyms (they are different layers).
5. Not adding one comparison table in long answers.

---

## 12) Active Recall Drill (Self-Test)

1. Can you explain CSU taxonomy in 30 seconds?
2. Can you compare focused vs regular crawler in 4 lines?
3. Can you write HITS update equations from memory?
4. Can you state TM-IR-IE pipeline in order?
5. Can you write one 10-point answer without notes?

If all 5 are yes, Module 5 is exam-ready.

---

## 13) 30-Second Revision Strip

1. CSU taxonomy and one-line definition each.
2. Focused crawler vs regular crawler.
3. HITS and CLEVER one-liner difference.
4. TM/IR/IE pipeline and TF-IDF formula.
5. One table: content vs structure vs usage.
