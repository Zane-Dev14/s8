# STEP 2: Module 1 Crash Guide (Data Warehouse, OLAP, KDD)

Module 1 focus:
- Data warehouse basics
- OLTP vs OLAP
- Multidimensional model and OLAP operations
- Warehouse architecture and schemas
- KDD process and data mining functionalities

Mapped from OCR:
- DM/ocr_output/Data-Mining-Module-1-Important-Topics-PYQs.txt
- DM/ocr_output/series1.txt

---

## Topic 1: Three Major Features of Data Warehouse

Write these 3 with one line each:
1. Subject-oriented: organized around major subjects like customer, sales, product.
2. Integrated: data from multiple heterogeneous sources is unified into consistent format.
3. Time-variant: keeps historical data for trend analysis (not only current transaction state).

---

## Topic 2: OLTP vs OLAP (Guaranteed PYQ)

Quick comparison points:
1. OLTP supports day-to-day transactions, OLAP supports analysis/decision making.
2. OLTP data is current and frequently updated, OLAP data is historical and aggregated.
3. OLTP queries are short and fast; OLAP queries are complex and analytical.
4. OLTP schema often ER/normalized; OLAP schema often star/snowflake.
5. OLTP users are clerks/apps; OLAP users are analysts/managers.

Memory line:
- OLTP = run business
- OLAP = analyze business

---

## Topic 3: Multidimensional Model

Core terms:
1. Fact table: stores measures (sales amount, count).
2. Dimension table: stores context (time, product, location).
3. Data cube: multidimensional view of facts by dimensions.

Mini example:
- Dimensions: time, doctor, patient
- Measures: count, charge

---

## Topic 4: OLAP Operations (Must write all 5)

1. Roll-up (drill-up): move from detailed to summarized level.
   Example: day -> month -> year.
2. Drill-down: move from summary to detail.
   Example: year -> month -> day.
3. Slice: fix one dimension value.
   Example: year = 2023 only.
4. Dice: choose subcube by ranges on multiple dimensions.
   Example: years 2022-2023 and region South.
5. Pivot (rotate): change orientation for better visualization.

---

## Topic 5: Star Schema vs Snowflake Schema

## Star schema
- One central fact table + denormalized dimension tables.
- Simple joins, faster query response.
- More redundancy.

## Snowflake schema
- Dimension tables further normalized into sub-dimensions.
- Less redundancy, cleaner hierarchy.
- More joins, comparatively slower queries.

Exam tip:
- If asked to draw quickly, draw star first unless question explicitly asks snowflake.

---

## Topic 6: Three-Tier Architecture of Data Warehouse

1. Bottom tier:
   - Data warehouse server and source systems.
   - ETL happens here (extract, transform, load).
2. Middle tier:
   - OLAP server (ROLAP/MOLAP/HOLAP).
3. Top tier:
   - Reporting, query, dashboards, mining tools.

Diagram-friendly text:
- Sources/ETL -> Warehouse/OLAP -> User tools

---

## Topic 7: ROLAP vs MOLAP vs HOLAP

1. ROLAP: data in relational tables; scalable but may be slower for heavy aggregation.
2. MOLAP: data in multidimensional cubes; very fast query but higher storage/precompute cost.
3. HOLAP: hybrid approach combining both.

---

## Topic 8: KDD Process

Write in order:
1. Data cleaning
2. Data integration
3. Data selection
4. Data transformation
5. Data mining
6. Pattern evaluation
7. Knowledge presentation

Common mistake to avoid:
- Data mining is one step, not the whole KDD process.

---

## Topic 9: Data Mining Functionalities

High-score list:
1. Characterization
2. Discrimination
3. Classification
4. Prediction
5. Clustering
6. Association rule mining
7. Outlier analysis
8. Evolution/trend analysis

---

## Module 1 PYQ Attack Set

1. Features of data warehouse
2. OLTP vs OLAP
3. Star vs snowflake schema
4. Data cube and OLAP operations
5. Three-tier architecture
6. KDD stages
7. ROLAP/MOLAP/HOLAP differences
8. Data mining functionalities

---

## Last-Minute Revision Grid

1. Memorize 3 DW features exactly.
2. Practice one neat OLTP vs OLAP table.
3. Practice one schema diagram (star and snowflake).
4. Write OLAP operations with one example each.
5. Recite KDD steps in order without skipping.
