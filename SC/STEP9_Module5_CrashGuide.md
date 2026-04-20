## STEP 9: MODULE 5 CRASH GUIDE (HIGH-QUALITY VERSION)

Module focus:
- Multi-objective optimization problem (MOOP)
- Dominance and Pareto optimality
- Non-dominated set extraction (full steps)
- Convex vs non-convex understanding
- Genetic-neuro and neuro-fuzzy hybrid systems

How to use this file:
1. Always state objective direction (min or max) before dominance checks.
2. For numericals, show pairwise comparisons explicitly.
3. For long answers, include one clean Pareto-front diagram.

---

## Topic 1: MOOP Fundamentals

### Definition
A multi-objective optimization problem optimizes multiple objectives simultaneously.

### Standard form

$$
\text{Min/Max } F(x) = [f_1(x), f_2(x), \dots, f_m(x)]
$$

Subject to:

$$
g_j(x)\le 0,\quad h_k(x)=0
$$

Term meaning:
- x: decision vector
- f_i(x): i-th objective function
- g_j, h_k: inequality/equality constraints
- Feasible set: all x satisfying constraints

### Key idea
In MOOP, there is usually no single best point for all objectives. We seek trade-off solutions.

---

## Topic 2: Linear/Nonlinear and Convex/Non-convex MOOP

### Linear vs nonlinear

| Type | Condition |
|---|---|
| Linear MOOP | All objective and constraint expressions are linear |
| Nonlinear MOOP | At least one objective/constraint is nonlinear |

### Convex vs non-convex

| Type | Property |
|---|---|
| Convex | Any line segment between feasible points remains feasible |
| Non-convex | Convexity condition fails in at least one region |

Convexity condition for function f:

$$
f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda)f(y),\quad 0<\lambda<1
$$

Important result:
- In convex optimization, local minimum is global minimum.

---

## Topic 3: Dominance Relation

### Definition for minimization case
A dominates B if:
1. A is no worse in all objectives.
2. A is strictly better in at least one objective.

Mathematically:

$$
A \prec B \iff \forall i,\; f_i(A)\le f_i(B)\;\text{and}\;\exists j:\, f_j(A)<f_j(B)
$$

### Why dominance is central
1. It filters inferior solutions.
2. It builds non-dominated fronts.
3. It is used in Pareto ranking algorithms.

---

## Topic 4: Pareto Optimality

### Core definitions
- Non-dominated set in P: points in P not dominated by other points in P.
- Pareto-optimal set: non-dominated set in whole feasible space.
- Pareto front: objective-space image of Pareto-optimal set.

### Diagram

```text
f2 (min)
^
|  x x x   <- dominated region
|   o o o  <- Pareto front points
+------------------------------> f1 (min)
```

Interpretation:
- Moving along Pareto front improves one objective while worsening another.

---

## Topic 5: Full Procedure to Find Non-dominated Set

### Generic algorithm
1. List all candidate points with objective values.
2. Choose one point and compare with all others.
3. Mark points it dominates.
4. Repeat for each point.
5. Remove all dominated points.
6. Remaining points form non-dominated set.

### Worked numerical (all pairwise logic shown)

Objective: minimize (time, cost)

Given points:
- A(2,7.5), B(3,6), C(3,7.5), D(4,5), E(4,6.5), F(5,4.5), G(5,6), H(5,7), I(6,6.5)

Step 1: Compare B with others
- B dominates C: 3<=3 and 6<7.5
- B dominates E: 3<4 and 6<6.5
- B dominates G: 3<5 and 6<=6
- B dominates H: 3<5 and 6<7
- B dominates I: 3<6 and 6<6.5

Step 2: Compare D with others
- D dominates E: 4<=4 and 5<6.5
- D dominates G: 4<5 and 5<6
- D dominates H: 4<5 and 5<7
- D dominates I: 4<6 and 5<6.5

Step 3: Compare F with others
- F dominates G: 5<=5 and 4.5<6
- F dominates H: 5<=5 and 4.5<7
- F dominates I: 5<6 and 4.5<6.5

Step 4: Compare A
- A dominates C: 2<3 and 7.5<=7.5
- A does not dominate B, D, F due to trade-off

Step 5: Remove dominated points
Dominated = {C, E, G, H, I}

Step 6: Remaining set
Non-dominated set = {A, B, D, F}

This set is the Pareto set for the given candidate list.

---

## Topic 6: Properties of Dominance Relation

For strict dominance used in MOOP practice:
1. Not reflexive (A does not strictly dominate itself).
2. Not symmetric (if A dominates B, B cannot dominate A).
3. Transitive in practical pairwise comparisons used for ranking.

Exam note: always write objective direction before stating inequalities.

---

## Topic 7: Genetic-Neuro Hybrid System

### Definition
GA searches neural-network parameter space (weights/topology/hyperparameters), while ANN evaluates solution quality.

### Block diagram

```text
GA population -> Decode ANN params -> ANN training/evaluation -> Fitness -> GA selection/crossover/mutation -> next population
```

### Stepwise workflow
1. Encode ANN parameters as chromosomes.
2. Generate initial GA population.
3. Build/evaluate ANN for each chromosome.
4. Compute fitness (for example inverse error).
5. Select best chromosomes.
6. Apply crossover and mutation.
7. Repeat until stop criterion.

### Strengths and limits

| Strengths | Limits |
|---|---|
| Global search ability | Higher computation cost |
| Can optimize architecture + weights | Many hyperparameters to tune |
| Useful for non-convex error surfaces | Slower than local-only training |

---

## Topic 8: Neuro-Fuzzy Hybrid System

### Definition
Neuro-fuzzy combines fuzzy rule-based interpretability with neural learning/adaptation.

### Classification
1. Cooperative model
2. Concurrent model
3. Integrated model

### Comparison table

| Model | Main idea | Typical advantage |
|---|---|---|
| Cooperative | One system initializes/tunes the other | Simple pipeline |
| Concurrent | Both run together and exchange signals | Real-time adaptation |
| Integrated | Tightly fused architecture | Strong synergy |

### Why used
1. Handles uncertainty (fuzzy part).
2. Learns from data (neural part).
3. Keeps interpretability better than pure neural black-box approaches.

---

## PYQ Bottom Section (deduplicated answer drill)

### Part A quick set
1. Differentiate linear and nonlinear MOOP.
2. Explain dominance in multi-objective optimization.
3. State characteristics of neuro-fuzzy hybrid systems.

### Part B long set
1. Explain convex and non-convex MOOP and derive non-dominated set.
2. Explain Pareto optimality and dominance properties.
3. Explain genetic-neuro hybrid with block diagram.
4. Explain classifications of neuro-fuzzy hybrids.

14-mark answer sequence:
1. Definition and objective direction
2. Formula with symbol meanings
3. Table of candidate solutions
4. Pairwise dominance checks
5. Final Pareto/non-dominated set
6. Diagram and conclusion
