# STEP 2: Module 1 Crash Guide (Data Warehouse, OLAP, KDD)

Module focus:
- Data warehouse fundamentals
- Multidimensional modeling and OLAP
- Warehouse architecture and schemas
- KDD process and mining functionalities

Questions asked repeatedly (non-duplicate):
- Applications/features of data warehouse
- OLTP vs OLAP
- Star schema vs snowflake schema
- Multidimensional model and OLAP operations
- Three-tier data warehouse architecture
- ROLAP vs MOLAP vs HOLAP
- KDD process and data mining functionalities

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
