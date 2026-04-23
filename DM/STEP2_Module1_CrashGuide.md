# STEP 2: Module 1 Crash Guide (Data Warehouse, OLAP, KDD)

Module focus:
- Data warehouse fundamentals
- Multidimensional modeling and OLAP
- Warehouse architecture and schemas
- KDD process and mining functionalities

Questions asked repeatedly (non-duplicate):
Part A topics asked:
1. Applications and features of data warehouse.
2. OLTP vs OLAP differences.
3. Star schema vs snowflake schema.
4. Multidimensional data model basics.

Part B topics asked:
1. Data mining functionalities.
2. Three-tier data warehouse architecture with diagram.
3. Star vs snowflake schema with example.
4. OLAP operations with examples.
5. ROLAP vs MOLAP vs HOLAP.
6. KDD process and stages.
7. Key issues in data mining.
8. Scenario-based snowflake schema and OLAP operation sequence.

Answer format for this module:
- Part A: write exactly 5 points.
- Part B: write exactly 10 points.
- Include one small diagram/table in every Part B answer.

---

## 1) Three Major Features of Data Warehouse

Definition line:
A data warehouse is a subject-oriented, integrated, time-variant, and non-volatile repository for decision support.

Write these three first in exam:
1. Subject-oriented: organized by business subjects such as sales, customer, product.
2. Integrated: combines heterogeneous sources after cleaning and standardization.
3. Time-variant: stores historical snapshots for trend analysis over time.

Bonus point if needed:
4. Non-volatile: read-heavy; data is loaded and analyzed, not repeatedly updated like OLTP.

---

## 2) OLTP vs OLAP (Write as table for easy marks)

| Aspect | OLTP | OLAP |
|---|---|---|
| Purpose | Day-to-day transactions | Analysis and decision support |
| Data type | Current operational data | Historical and aggregated data |
| Query style | Short, frequent, update-heavy | Complex, read-heavy |
| Schema style | Usually normalized ER style | Usually star/snowflake style |
| Users | Clerks, apps, transaction systems | Analysts, managers, BI teams |

One-line conclusion:
OLTP runs business operations; OLAP analyzes business performance.

---

## 3) Multidimensional Data Model

Core entities:
1. Fact table: stores measurable quantities (for example sales amount, count, charge).
2. Dimension tables: describe context (for example time, location, product, doctor).
3. Data cube: conceptual n-dimensional organization of fact measures.

Mini exam example:
- Dimensions: time, doctor, patient
- Measures: count, charge

---

## 4) OLAP Operations (Must write all five)

1. Roll-up: aggregate from lower level to higher level.
Example: day to month to year.
2. Drill-down: move from summary to detail.
Example: year to quarter to month.
3. Slice: fix one dimension value.
Example: year = 2023.
4. Dice: choose subcube using multiple dimension conditions.
Example: year in {2022, 2023} and region = South.
5. Pivot: rotate cube axes for alternate view.

Quick mnemonic:
Roll, Drill, Slice, Dice, Pivot.

---

## 5) Star vs Snowflake Schema

| Point | Star schema | Snowflake schema |
|---|---|---|
| Dimension design | Denormalized dimensions | Normalized dimensions |
| Join complexity | Fewer joins | More joins |
| Query speed | Usually faster | Usually slower than star |
| Redundancy | Higher redundancy | Lower redundancy |
| Diagram simplicity | Easier to draw | More detailed hierarchy |

ASCII drawing guide:

Star:
```text
        Dim_Time
           |
Dim_Product- Fact_Sales -Dim_Customer
           |
       Dim_Region
```

Snowflake (one dimension normalized):
```text
Fact_Sales - Dim_Product - Dim_Category
            \
             Dim_Brand
```

---

## 6) Three-Tier Architecture of Data Warehouse

1. Bottom tier:
- Data sources, ETL, and warehouse database server.
2. Middle tier:
- OLAP server (ROLAP/MOLAP/HOLAP).
3. Top tier:
- Query, reporting, dashboards, mining tools.

Diagram line:
Sources and ETL -> Warehouse and OLAP -> End-user BI tools.

---

## 7) ROLAP vs MOLAP vs HOLAP

| Type | Storage style | Strength | Limitation |
|---|---|---|---|
| ROLAP | Relational tables | Scalable on large data | Slower aggregate queries |
| MOLAP | Multidimensional cubes | Very fast aggregate query | Higher precompute/storage cost |
| HOLAP | Hybrid approach | Balance of scale and speed | Design complexity |

---

## 8) KDD Process (Ordered Steps)

1. Data cleaning
2. Data integration
3. Data selection
4. Data transformation
5. Data mining
6. Pattern evaluation
7. Knowledge presentation

Important correction line:
Data mining is one stage inside KDD, not the full KDD pipeline.

---

## 9) Data Mining Functionalities (Long answer list)

1. Characterization
2. Discrimination
3. Classification
4. Prediction
5. Clustering
6. Association rule mining
7. Outlier analysis
8. Evolution and trend analysis

---

## 10) Worked OLAP Operation Question Pattern

Question style:
Starting with base cuboid [day, doctor, patient], list total fee collected by each doctor in 2023.

Step solution:
1. Slice time dimension where year = 2023.
2. Roll-up day to year level if needed.
3. Roll-up patient dimension to ALL (aggregate across patients).
4. Keep doctor dimension as analysis axis.
5. Aggregate measure charge using SUM.
6. Present result table: doctor vs total_charge_2023.

Why this gets full method marks:
- operation names are explicit
- order of operations is explicit
- aggregation function is explicit

---

## Module 1 Final Drill

1. Write one clean OLTP vs OLAP table.
2. Draw one star and one snowflake schema.
3. Recite KDD steps in exact order.
4. Write all five OLAP operations with one example each.

---

## Part B Complete Answer Bank (All Asked Questions)

Use acronym for long answers:
- DAFS-STEP-EC
- Definition, Architecture, Flow, Steps, Example, Table, End-Conclusion.

## Q1) Explain data mining functionalities (10 points)
1. Data mining functionality means the type of pattern/task performed on data.
2. Descriptive functionalities summarize existing data behavior.
3. Predictive functionalities estimate unknown or future values.
4. Characterization summarizes general properties of target class.
5. Discrimination compares target class against contrasting class.
6. Association mining finds co-occurring item relationships.
7. Classification learns labels from training data.
8. Prediction estimates continuous values and trends.
9. Clustering groups similar data without predefined labels.
10. Outlier and evolution analysis detect anomalies and temporal changes.

## Q2) Three-tier data warehouse architecture with diagram (10 points)
1. A data warehouse is organized in bottom, middle, and top tiers.
2. Bottom tier integrates source data through ETL into warehouse storage.
3. ETL does extraction, cleaning, transformation, and loading.
4. Warehouse server stores integrated, historical, subject-oriented data.
5. Middle tier hosts OLAP server for multidimensional analytics.
6. OLAP supports roll-up, drill-down, slice, dice, and pivot.
7. Top tier provides reporting, dashboard, query, and mining tools.
8. Metadata repository supports governance and schema understanding.
9. Diagram:

```text
Sources -> ETL -> Warehouse DB -> OLAP Server -> Reports/BI/Mining
```

10. This separation improves scalability, maintainability, and query performance.

## Q3) Star schema vs snowflake schema with example (10 points)
1. Both schemas model multidimensional data around fact tables.
2. Star schema keeps dimension tables denormalized.
3. Snowflake schema normalizes dimensions into sub-dimensions.
4. Star gives fewer joins and faster simple OLAP queries.
5. Snowflake reduces redundancy and improves data consistency.
6. Star is easier to understand and draw in exams.
7. Snowflake is better for complex hierarchies and governance.
8. Example star: Sales_Fact linked to Time, Product, Customer, Region.
9. Example snowflake: Product dimension split to Category and Brand tables.
10. Choose star for speed/readability and snowflake for normalization depth.

## Q4) OLAP operations with ROLAP/MOLAP/HOLAP comparison (10 points)
1. OLAP analyzes measures across multiple business dimensions.
2. Roll-up aggregates data from detail to summary levels.
3. Drill-down navigates from summary to finer granularity.
4. Slice fixes one dimension value and forms a reduced cube.
5. Dice filters multiple dimensions to obtain a subcube.
6. Pivot rotates analysis axes for alternate perspective.
7. ROLAP stores data in relational tables and scales well.
8. MOLAP stores data in multidimensional cubes for speed.
9. HOLAP combines relational storage and cube-based aggregates.
10. Selection depends on scale, latency target, and storage budget.

## Q5) KDD process (10 points)
1. KDD is full knowledge discovery pipeline from raw data to insight.
2. Data cleaning removes missing values, noise, and inconsistency.
3. Data integration merges multiple heterogeneous sources.
4. Data selection picks relevant tuples and attributes.
5. Data transformation prepares normalized/aggregated model-ready data.
6. Data mining stage applies algorithms to discover patterns.
7. Pattern evaluation filters useful and interesting discoveries.
8. Knowledge presentation communicates insights via charts and reports.
9. Flow diagram:

```text
Cleaning -> Integration -> Selection -> Transformation -> Mining -> Evaluation -> Presentation
```

10. Data mining is a stage inside KDD, not the whole process.

## Q6) Key issues in data mining (10 points)
1. Data quality issue: missing, noisy, and inconsistent records.
2. Data integration issue: schema and semantic conflicts.
3. Scalability issue: very large high-dimensional datasets.
4. Pattern evaluation issue: interestingness and false discovery.
5. Overfitting issue: overly specific models with weak generalization.
6. Interpretability issue: black-box outputs hard for decision makers.
7. Privacy and security issue: sensitive data exposure risks.
8. Dynamic data issue: concept drift in changing environments.
9. Heterogeneous data issue: text, image, stream, graph variations.
10. Robust mining needs quality control, validation, and governance.

## Q7) Scenario answer: snowflake schema + OLAP operations (10 points)
1. Identify fact table using quantitative measures from question.
2. Identify dimensions and hierarchy levels from context.
3. Draw snowflake with normalized dimension sub-tables.
4. Set base cuboid at most detailed grain.
5. Use slice on fixed filter (for example course type or region).
6. Use dice to restrict multiple dimension conditions.
7. Use roll-up to aggregate to requested summary level.
8. Use drill-down only if question requests detailed breakdown.
9. Use pivot to present final result view cleanly.
10. End with final table/list exactly matching asked metric.
