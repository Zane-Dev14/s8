# STEP 9: Module 5 Crash Guide (Web and Text Mining)

Module 5 core area:
- Web usage mining, web structure mining, web content mining
- Text retrieval and text mining
- Focused crawling, HITS, CLEVER

OCR-mapped sources:
- DM/ocr_output/CST466_DATA_MINING,_JUNE_2023.txt
- DM/ocr_output/CST466_DATA_MINING,_MAY_2024.txt
- DM/ocr_output/CST466_DATA_MINING,_APRIL_2025.txt
- DM/ocr_output/Data-Mining-Module-5-Important-Topics-PYQs.txt
- DM/ocr_output/Data-Mining-Series-2-Important-Topics.txt

---

## Questions Asked (Put This At Top In Revision)

Part A repeats:
1. Briefly explain web mining taxonomy.
2. Differentiate web content mining and web structure mining.
3. Compare web structure mining and web usage mining.
4. Distinguish focused crawling and regular crawling.
5. Explain pre-processing and pattern analysis in web usage mining.

Part B repeats:
1. Explain web usage mining applications and activities.
2. Explain focused crawler and personalization context.
3. Explain text retrieval methods.
4. Relate text mining, information retrieval, and information extraction.
5. Explain HITS algorithm with example.
6. Write CLEVER algorithm for web structure mining.
7. Explain web usage data structures.
8. Explain traversal patterns and discovery methods.
9. Explain web content mining techniques.
10. Explain text mining approaches in detail.

---

## Part A: 5-Point Answer Capsules

## Q1) Web mining taxonomy
1. Web mining extracts knowledge from web data and services.
2. Web content mining analyzes page content such as text, images, and media.
3. Web structure mining analyzes hyperlink graph and document link topology.
4. Web usage mining analyzes user interaction logs and clickstreams.
5. Together they support search quality, recommendation, and personalization.

## Q2) Web content vs web structure mining
1. Content mining focuses on information inside pages.
2. Structure mining focuses on relationships among pages via links.
3. Content mining uses NLP/text analysis and media extraction methods.
4. Structure mining uses graph analysis and ranking algorithms.
5. Content answers what is written; structure answers how pages are connected.

## Q3) Focused vs regular crawling
1. Regular crawler aims broad coverage of the web.
2. Focused crawler collects pages relevant to a specific topic.
3. Regular crawling is exhaustive but resource intensive.
4. Focused crawling is selective and precision-oriented.
5. Focused crawling improves topical quality of indexed pages.

## Q4) Web usage mining activities
1. Pre-processing cleans and structures raw web log data.
2. User/session identification is performed after noise removal.
3. Pattern discovery mines association, clusters, sequences, and paths.
4. Pattern analysis filters useful behavioral knowledge.
5. Output is used for personalization, navigation design, and marketing.

## Q5) Text retrieval methods
1. Document selection uses strict query logic (Boolean model).
2. Document ranking orders results by relevance score.
3. Selection is exact but can miss partially relevant documents.
4. Ranking uses weighted matching (for example TF-IDF).
5. Most modern search systems use ranking-centric retrieval.

---

## Part B: 10-Point Exam Blueprints

## Q1) Web usage mining applications and activities
1. Web usage mining discovers behavior patterns from user interaction logs.
2. Main input sources are server logs, application logs, and clickstream data.
3. First stage is data cleaning to remove bots, duplicates, and noise.
4. Next stage identifies users and sessions from cleaned records.
5. Path completion reconstructs missing navigation steps.
6. Pattern discovery applies association rules, clustering, and sequential mining.
7. Pattern analysis evaluates discovered patterns for business relevance.
8. Applications include personalization, recommendation, site redesign, and marketing.
9. Example: repeated path product -> review -> cart supports targeted recommendations.
10. Conclude that usage mining converts traffic logs into actionable decisions.

## Q2) Text retrieval methods and relation of TM-IR-IE
1. Information retrieval (IR) finds relevant documents for user queries.
2. Text mining (TM) extracts hidden patterns/knowledge from text corpora.
3. Information extraction (IE) extracts structured facts/entities/relations from text.
4. Retrieval methods are mainly document selection and document ranking.
5. Selection uses Boolean logic with exact matching constraints.
6. Ranking uses weighted relevance scores (for example TF-IDF and vector models).
7. IR supplies candidate documents for deeper mining.
8. IE structures specific details such as names, dates, and relations.
9. TM integrates IR plus IE plus analytics tasks like clustering/classification.
10. Conclude: IR finds documents, IE structures facts, TM discovers knowledge.

## Q3) HITS algorithm with example flow
1. HITS computes two scores: authority and hub.
2. Authority page is cited by many good hubs.
3. Hub page points to many good authorities.
4. Start with root set from query-matched pages.
5. Expand to base set by adding linked neighbors.
6. Initialize all authority and hub scores equally.
7. Iteratively update authority from incoming hub scores.
8. Iteratively update hub from outgoing authority scores.
9. Normalize scores each iteration until convergence.
10. Output top authority and hub pages for the topic.

## Q4) CLEVER algorithm for web structure mining
1. CLEVER is a link-analysis approach extending topic-sensitive hyperlink mining.
2. It uses seed pages relevant to a query/topic.
3. It builds a focused subgraph around seeds.
4. Authorities are pages pointed by many strong hubs.
5. Hubs are pages pointing to many strong authorities.
6. Iterative propagation updates hub/authority influence values.
7. Irrelevant/noisy links are filtered to preserve topic focus.
8. The method supports community discovery and quality ranking.
9. It improves query-dependent ranking beyond simple keyword matching.
10. Conclude: CLEVER is graph-structure intelligence for topic-centric ranking.

## Q5) Web structure vs web content vs web usage
1. Web content mining analyzes page data itself.
2. Web structure mining analyzes hyperlink graph connectivity.
3. Web usage mining analyzes user behavior and session logs.
4. Content methods use NLP and feature extraction.
5. Structure methods use graph centrality and link ranking.
6. Usage methods use sequence mining and clustering.
7. Content helps understand what pages say.
8. Structure helps identify authority and community.
9. Usage helps personalize and optimize user journeys.
10. Conclude all three are complementary layers of web intelligence.

---

## Must-Know Technical Blocks

## TF-IDF recap
1. Term Frequency (TF) captures term importance inside a document.
2. Inverse Document Frequency (IDF) downweights very common terms.
3. TF-IDF weight highlights terms that are locally frequent but globally selective.

## Web usage data structures
1. Trie for sequence/path prefix storage.
2. Suffix tree or compressed trie for efficient pattern/path queries.
3. Graph/session trees for clickstream traversal analysis.

## Traversal patterns
1. Sequential patterns.
2. Frequent patterns.
3. Cyclic patterns.
4. Path traversal patterns.

---

## Quick Comparison Tables

## Focused vs Regular Crawler

| Aspect | Focused crawler | Regular crawler |
|---|---|---|
| Objective | Topic-specific pages | Broad web coverage |
| Precision | Higher topical precision | Lower topical precision |
| Resource use | Efficient for narrow domain | High for full-web coverage |
| Typical use | Domain search, research portals | General search engines |

## Content vs Structure vs Usage

| Type | Data source | Typical methods | Output |
|---|---|---|---|
| Content | Page text/media | NLP, extraction, classification | Topic/content insight |
| Structure | Hyperlinks/graph | Link analysis, ranking | Authority/hub/community |
| Usage | Logs/clickstreams | Sequence mining, clustering | Behavior/personalization |

---

## Module 5 Memory Acronyms

1. WSU triad:
- Web Content, Web Structure, Web Usage.

2. Search stack:
- IR -> IE -> TM.

3. Ranking pair:
- HA = Hub and Authority.

4. Crawl pair:
- FR = Focused and Regular.

---

## Last-Minute Drill

1. Write one 5-point answer: focused crawler vs regular crawler.
2. Write one 10-point answer: text retrieval + TM/IR/IE relation.
3. Write one 10-point answer: HITS or CLEVER.
4. Draw one clean comparison table for content/structure/usage.
